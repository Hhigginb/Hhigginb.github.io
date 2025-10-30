#!/usr/bin/env python3
"""
Convert all images in HTML files from optimized folder to responsive images with fallback
"""

import os
import re
from pathlib import Path

def check_webp_exists(base_name, base_dir):
    """Check which responsive WebP sizes exist for an image."""
    name_without_ext = os.path.splitext(base_name)[0]
    
    sizes = {}
    for size in ['thumb', 'small', 'medium', 'large', 'full']:
        webp_path = os.path.join(base_dir, 'responsive_images', size, f'{name_without_ext}.webp')
        sizes[size] = os.path.exists(webp_path)
    
    return sizes, f'{name_without_ext}.webp'


def create_responsive_srcset(base_name, base_dir):
    """Create srcset with fallback for missing sizes."""
    webp_exists, webp_name = check_webp_exists(base_name, base_dir)
    
    size_info = {
        'thumb': 300,
        'small': 640,
        'medium': 1024,
        'large': 1920,
        'full': 2560
    }
    
    available_sizes = [size for size in size_info.keys() if webp_exists.get(size)]
    
    if not available_sizes:
        return None, None
    
    srcset_parts = []
    for size, width in size_info.items():
        if webp_exists.get(size):
            # Size exists, use it
            srcset_parts.append(f"responsive_images/{size}/{webp_name} {width}w")
        else:
            # Find fallback - use next smallest available size
            fallback_size = None
            size_order = ['thumb', 'small', 'medium', 'large', 'full']
            size_index = size_order.index(size)
            
            # Look for smaller sizes first
            for i in range(size_index - 1, -1, -1):
                if webp_exists.get(size_order[i]):
                    fallback_size = size_order[i]
                    break
            
            # If no smaller size, use 'full' as fallback
            if not fallback_size and webp_exists.get('full'):
                fallback_size = 'full'
            elif not fallback_size:
                fallback_size = available_sizes[0] if available_sizes else None
            
            if fallback_size:
                srcset_parts.append(f"responsive_images/{fallback_size}/{webp_name} {width}w")
    
    return ', '.join(srcset_parts), base_name


def convert_optimized_to_responsive(html_content, base_dir):
    """Convert picture tags from optimized folder to responsive images."""
    
    # Pattern 1: <picture><source optimized/X.webp><img src="X.jpg"></picture>
    pattern1 = r'<picture>\s*<source\s+srcset=["\']optimized/([^"\']+)\.webp["\'][^>]*>\s*<img\s+src=["\']([^"\']+\.jpg)["\']([^>]*)>\s*</picture>'
    
    # Pattern 2: <picture><source optimized/X.webp><img src="responsive_images/X.webp" srcset="..."></picture>
    pattern2 = r'<picture>\s*<source\s+srcset=["\']optimized/([^"\']+)\.webp["\'][^>]*>\s*<img\s+src=["\']responsive_images/[^"\']+\.webp["\']([^>]*)>\s*</picture>'
    
    def replace_pattern1(match):
        webp_base = match.group(1)
        jpg_src = match.group(2)
        img_attrs = match.group(3)
        
        base_name = os.path.basename(jpg_src)
        
        # Create responsive srcset
        new_srcset, _ = create_responsive_srcset(base_name, base_dir)
        
        if not new_srcset:
            print(f"  ⚠ No responsive images found for {base_name}")
            return match.group(0)
        
        # Extract attributes
        attrs_str = img_attrs.strip()
        
        # Build new picture tag
        new_picture = f'<picture>\n        <source srcset="{new_srcset}" sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw" type="image/webp">\n        <img src="{base_name}"{attrs_str}>\n      </picture>'
        
        return new_picture
    
    def replace_pattern2(match):
        webp_base = match.group(1)
        img_attrs = match.group(2)
        
        base_name = webp_base + '.jpg'
        
        # Create responsive srcset
        new_srcset, jpg_fallback = create_responsive_srcset(base_name, base_dir)
        
        if not new_srcset:
            print(f"  ⚠ No responsive images found for {base_name}")
            return match.group(0)
        
        # Remove old srcset from img_attrs
        clean_attrs = re.sub(r'\s*srcset="[^"]*"', '', img_attrs)
        clean_attrs = re.sub(r'\s*sizes="[^"]*"', '', clean_attrs)
        
        # Build new picture tag
        new_picture = f'<picture>\n        <source srcset="{new_srcset}" sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw" type="image/webp">\n        <img src="{base_name}"{clean_attrs}>\n      </picture>'
        
        return new_picture
    
    # Apply pattern 1
    new_content = re.sub(pattern1, replace_pattern1, html_content, flags=re.IGNORECASE | re.DOTALL)
    
    # Apply pattern 2
    new_content = re.sub(pattern2, replace_pattern2, new_content, flags=re.IGNORECASE | re.DOTALL)
    
    return new_content


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("="*60)
    print("Convert Optimized Images to Responsive Format")
    print("="*60)
    
    # Process hand.html and heart.html
    for filename in ['hand.html', 'heart.html']:
        html_file = os.path.join(script_dir, filename)
        
        if not os.path.exists(html_file):
            print(f"\n⚠ {filename} not found, skipping")
            continue
        
        print(f"\nProcessing: {filename}")
        
        # Read file
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert images
        new_content = convert_optimized_to_responsive(content, script_dir)
        
        # Count changes
        old_optimized_count = content.count('optimized/')
        new_optimized_count = new_content.count('optimized/')
        changes = old_optimized_count - new_optimized_count
        
        # Write back if changed
        if new_content != content:
            # Create backup
            backup_path = html_file + '.backup_convert'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  📁 Created backup: {os.path.basename(backup_path)}")
            
            # Write new content
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"  ✅ Converted {changes} optimized references")
            print(f"  ✅ Updated {filename}")
        else:
            print("  ℹ No changes needed")
    
    print("\n" + "="*60)
    print("✅ Done!")
    print("="*60)


if __name__ == "__main__":
    main()
