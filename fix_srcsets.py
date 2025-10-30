#!/usr/bin/env python3
"""
Fix srcsets in HTML files to only include sizes that actually exist
"""

import os
import re
from pathlib import Path

def check_webp_exists(base_name, base_dir):
    """Check which responsive WebP sizes exist for an image."""
    # Remove extension and get just the base name
    name_without_ext = os.path.splitext(base_name)[0]
    
    sizes = {}
    for size in ['thumb', 'small', 'medium', 'large', 'full']:
        webp_path = os.path.join(base_dir, 'responsive_images', size, f'{name_without_ext}.webp')
        sizes[size] = os.path.exists(webp_path)
    
    return sizes, f'{name_without_ext}.webp'


def fix_picture_srcset(html_content, base_dir):
    """Fix picture tags to only include sizes that actually exist."""
    
    # Pattern to match picture tags with source srcset
    pattern = r'<picture>\s*<source\s+srcset="([^"]+)"\s+sizes="([^"]*)"\s+type="image/webp">\s*<img\s+src="([^"]+)"([^>]*)>\s*</picture>'
    
    def replace_picture(match):
        old_srcset = match.group(1)
        sizes_attr = match.group(2)
        img_src = match.group(3)
        img_attrs = match.group(4)
        
        # Extract image base name from img src or first srcset entry
        # Try to get from img src first
        base_name = os.path.basename(img_src)
        
        # If img src doesn't have jpg, extract from srcset
        if not base_name.endswith('.jpg'):
            # Get first entry in srcset to determine image name
            first_entry = old_srcset.split(',')[0].strip()
            srcset_path = first_entry.split()[0]
            webp_name = os.path.basename(srcset_path)
            base_name = webp_name.replace('.webp', '.jpg')
        
        # Check which sizes exist
        webp_exists, webp_name = check_webp_exists(base_name, base_dir)
        
        # Build new srcset with fallback strategy:
        # If a size doesn't exist, use the next smallest available size
        # If no smaller size exists, use 'full' as fallback
        size_info = {
            'thumb': 300,
            'small': 640,
            'medium': 1024,
            'large': 1920,
            'full': 2560
        }
        
        # Find which sizes exist
        available_sizes = [size for size in size_info.keys() if webp_exists.get(size)]
        
        if not available_sizes:
            print(f"  ⚠ No WebP sizes found for {base_name}")
            return match.group(0)  # Return original
        
        new_srcset_parts = []
        for size, width in size_info.items():
            if webp_exists.get(size):
                # Size exists, use it directly
                new_srcset_parts.append(f"responsive_images/{size}/{webp_name} {width}w")
            else:
                # Size doesn't exist, find fallback
                # Try to find the next smallest available size
                fallback_size = None
                size_order = ['thumb', 'small', 'medium', 'large', 'full']
                size_index = size_order.index(size)
                
                # Look for smaller sizes first
                for i in range(size_index - 1, -1, -1):
                    if webp_exists.get(size_order[i]):
                        fallback_size = size_order[i]
                        break
                
                # If no smaller size, use 'full' as ultimate fallback
                if not fallback_size and webp_exists.get('full'):
                    fallback_size = 'full'
                elif not fallback_size:
                    # Find any available size
                    fallback_size = available_sizes[0] if available_sizes else None
                
                if fallback_size:
                    new_srcset_parts.append(f"responsive_images/{fallback_size}/{webp_name} {width}w")
        
        if not new_srcset_parts:
            print(f"  ⚠ No WebP sizes found for {base_name}")
            return match.group(0)  # Return original
        
        new_srcset = ', '.join(new_srcset_parts)
        
        # Rebuild picture tag
        new_picture = f'<picture>\n              <source srcset="{new_srcset}" sizes="{sizes_attr}" type="image/webp">\n              <img src="{img_src}"{img_attrs}>\n            </picture>'
        
        # Check if srcset changed
        if old_srcset != new_srcset:
            print(f"  ✓ Fixed srcset for {base_name}")
            print(f"    Old: {old_srcset}")
            print(f"    New: {new_srcset}")
            return new_picture
        
        return match.group(0)
    
    return re.sub(pattern, replace_picture, html_content, flags=re.DOTALL)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("="*60)
    print("Fix Responsive Image Srcsets")
    print("="*60)
    
    # Find all HTML files
    html_files = list(Path(script_dir).glob('*.html'))
    
    for html_file in html_files:
        print(f"\nProcessing: {html_file.name}")
        
        # Read file
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix srcsets
        new_content = fix_picture_srcset(content, script_dir)
        
        # Write back if changed
        if new_content != content:
            # Create backup
            backup_path = str(html_file) + '.backup_srcset'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  📁 Created backup: {os.path.basename(backup_path)}")
            
            # Write new content
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✅ Updated {html_file.name}")
        else:
            print(f"  ℹ No changes needed")
    
    print("\n" + "="*60)
    print("✅ Done!")
    print("="*60)


if __name__ == "__main__":
    main()
