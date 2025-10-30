#!/usr/bin/env python3
"""
Fix modal images in mind.html to use responsive WebP with JPG fallback
"""

import os
import re

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
            # Find fallback
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


def fix_modal_images(html_content, base_dir):
    """Fix picture tags in modals that reference optimized folder."""
    
    # Pattern for old optimized format with responsive img src
    pattern = r'<picture>\s*<source\s+srcset="optimized/([^"]+)\.webp"[^>]*>\s*<img\s+src="responsive_images/[^"]+\.webp"([^>]*)>\s*</picture>'
    
    def replace_picture(match):
        webp_base = match.group(1)
        img_attrs = match.group(2)
        
        base_name = webp_base + '.jpg'
        
        # Create responsive srcset
        new_srcset, jpg_src = create_responsive_srcset(base_name, base_dir)
        
        if not new_srcset:
            print(f"  ⚠ No responsive images found for {base_name}")
            return match.group(0)
        
        # Extract attributes from img_attrs
        srcset_match = re.search(r'srcset="[^"]*"', img_attrs)
        sizes_match = re.search(r'sizes="[^"]*"', img_attrs)
        
        # Remove old srcset and sizes from img_attrs
        clean_attrs = re.sub(r'\s*srcset="[^"]*"', '', img_attrs)
        clean_attrs = re.sub(r'\s*sizes="[^"]*"', '', clean_attrs)
        
        # Build new picture tag
        new_picture = f'''<picture>
            <source srcset="{new_srcset}" sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw" type="image/webp">
            <img src="{jpg_src}"{clean_attrs}>
          </picture>'''
        
        print(f"  ✓ Fixed modal image: {base_name}")
        return new_picture
    
    return re.sub(pattern, replace_picture, html_content, flags=re.DOTALL)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(script_dir, 'mind.html')
    
    print("="*60)
    print("Fix Modal Images in mind.html")
    print("="*60)
    
    # Read file
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix modal images
    new_content = fix_modal_images(content, script_dir)
    
    # Write back if changed
    if new_content != content:
        # Create backup
        backup_path = html_file + '.backup_modal'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  📁 Created backup: {os.path.basename(backup_path)}")
        
        # Write new content
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"\n✅ Updated mind.html")
    else:
        print("  ℹ No changes needed")
    
    print("="*60)
    print("✅ Done!")
    print("="*60)


if __name__ == "__main__":
    main()
