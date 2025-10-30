#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update HTML files to use responsive WebP images with JPG fallback.

This script:
1. Finds all <img> tags that reference JPG files in the main folder
2. Converts them to use responsive WebP images from the responsive_images subfolder
3. Wraps them in <picture> tags with proper srcset for different sizes
4. Provides JPG fallback for older browsers
"""
import sys
import io

# Set UTF-8 encoding for stdout to handle Unicode characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import re
import sys
from pathlib import Path
from datetime import datetime


def backup_file(filepath):
    """Create a backup of the original file."""
    backup_path = f"{filepath}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created backup: {os.path.basename(backup_path)}")
    return backup_path


def check_webp_exists(base_name, base_dir):
    """Check if WebP versions exist in responsive_images folder."""
    responsive_dir = os.path.join(base_dir, 'responsive_images')
    sizes = ['thumb', 'small', 'medium', 'large', 'full']
    
    webp_name = base_name.rsplit('.', 1)[0] + '.webp'
    exists = {}
    
    for size in sizes:
        size_dir = os.path.join(responsive_dir, size)
        webp_path = os.path.join(size_dir, webp_name)
        exists[size] = os.path.exists(webp_path)
    
    return exists, webp_name


def create_picture_tag(img_tag, base_name, base_dir, img_attributes):
    """Create a <picture> tag with WebP sources and JPG fallback."""
    webp_exists, webp_name = check_webp_exists(base_name, base_dir)
    
    # If no WebP versions exist, return original
    if not any(webp_exists.values()):
        print(f"  ⚠ No WebP versions found for {base_name}, skipping")
        return img_tag
    
    # Extract important attributes
    alt = img_attributes.get('alt', '')
    style = img_attributes.get('style', '')
    onclick = img_attributes.get('onclick', '')
    class_attr = img_attributes.get('class', '')
    loading = img_attributes.get('loading', 'lazy')
    
    # Build attribute strings
    attrs = []
    if alt:
        attrs.append(f'alt="{alt}"')
    if style:
        attrs.append(f'style="{style}"')
    if onclick:
        attrs.append(f'onclick="{onclick}"')
    if class_attr:
        attrs.append(f'class="{class_attr}"')
    if loading:
        attrs.append(f'loading="{loading}"')
    
    attr_string = ' '.join(attrs)
    
    # Build srcset based on available sizes
    webp_srcsets = []
    
    # Define size breakpoints
    size_info = {
        'thumb': 300,
        'small': 640,
        'medium': 1024,
        'large': 1920,
        'full': 2560
    }
    
    # Build WebP srcset
    for size, width in size_info.items():
        if webp_exists.get(size):
            webp_srcsets.append(f"responsive_images/{size}/{webp_name} {width}w")
    
    webp_srcset = ', '.join(webp_srcsets)
    
    # Determine sizes attribute based on context (simple heuristic)
    sizes_attr = '(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw'
    
    # Determine default src (JPG fallback in main folder)
    default_src = base_name
    
    # Create picture tag
    picture = f'''<picture>
              <source srcset="{webp_srcset}" sizes="{sizes_attr}" type="image/webp">
              <img src="{default_src}" {attr_string}>
            </picture>'''
    
    return picture


def extract_img_attributes(img_tag):
    """Extract attributes from an img tag."""
    attributes = {}
    
    # Extract common attributes
    patterns = {
        'src': r'src=["\']([^"\']+)["\']',
        'alt': r'alt=["\']([^"\']*)["\']',
        'style': r'style=["\']([^"\']+)["\']',
        'onclick': r'onclick=["\']([^"\']+)["\']',
        'class': r'class=["\']([^"\']+)["\']',
        'loading': r'loading=["\']([^"\']+)["\']',
        'srcset': r'srcset=["\']([^"\']+)["\']',
        'sizes': r'sizes=["\']([^"\']+)["\']',
    }
    
    for attr, pattern in patterns.items():
        match = re.search(pattern, img_tag, re.IGNORECASE)
        if match:
            attributes[attr] = match.group(1)
    
    return attributes


def process_html_file(filepath):
    """Process a single HTML file to convert JPG images to responsive WebP."""
    print(f"\n{'='*60}")
    print(f"Processing: {os.path.basename(filepath)}")
    print(f"{'='*60}")
    
    base_dir = os.path.dirname(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = 0
    
    # First, update existing picture tags that use the optimized folder
    picture_pattern = r'<picture>\s*<source\s+srcset=["\']optimized/([^"\']+)\.webp["\'][^>]*>\s*<img\s+src=["\']([^"\']+\.jpg)["\']([^>]*)>\s*</picture>'
    
    def replace_picture(match):
        nonlocal changes_made
        webp_base = match.group(1)  # filename without extension from optimized folder
        jpg_src = match.group(2)    # full jpg src
        img_rest = match.group(3)   # rest of img attributes
        
        base_name = os.path.basename(jpg_src)
        
        # Check if responsive WebP versions exist
        webp_exists, webp_name = check_webp_exists(base_name, base_dir)
        
        if not any(webp_exists.values()):
            print(f"  ⚠ No responsive WebP versions found for {base_name}, keeping as is")
            return match.group(0)
        
        # Extract img attributes from the rest of the tag
        full_img_tag = f'<img src="{jpg_src}"{img_rest}>'
        attributes = extract_img_attributes(full_img_tag)
        
        # Build srcset based on available sizes
        webp_srcsets = []
        size_info = {
            'thumb': 300,
            'small': 640,
            'medium': 1024,
            'large': 1920,
            'full': 2560
        }
        
        for size, width in size_info.items():
            if webp_exists.get(size):
                webp_srcsets.append(f"responsive_images/{size}/{webp_name} {width}w")
        
        webp_srcset = ', '.join(webp_srcsets)
        sizes_attr = '(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw'
        
        # Build attribute strings
        attrs = []
        if attributes.get('alt'):
            attrs.append(f'alt="{attributes["alt"]}"')
        if attributes.get('style'):
            attrs.append(f'style="{attributes["style"]}"')
        if attributes.get('onclick'):
            attrs.append(f'onclick="{attributes["onclick"]}"')
        if attributes.get('class'):
            attrs.append(f'class="{attributes["class"]}"')
        if attributes.get('loading'):
            attrs.append(f'loading="{attributes["loading"]}"')
        
        attr_string = ' '.join(attrs)
        
        new_picture = f'''<picture>
        <source srcset="{webp_srcset}" sizes="{sizes_attr}" type="image/webp">
        <img src="{jpg_src}" {attr_string}>
      </picture>'''
        
        changes_made += 1
        print(f"  ✓ Updated picture tag: {base_name} (optimized → responsive_images)")
        
        return new_picture
    
    # Replace picture tags using optimized folder
    content = re.sub(picture_pattern, replace_picture, content, flags=re.IGNORECASE | re.DOTALL)
    
    # Second, update picture tags where source uses optimized but img already uses responsive_images
    # Pattern: <picture><source srcset="optimized/XXX.webp"><img src="responsive_images/...webp" srcset="responsive_images/..."></picture>
    mixed_pattern = r'<picture>\s*<source\s+srcset=["\']optimized/([^"\']+)\.webp["\'][^>]*>\s*<img\s+src=["\']responsive_images/[^"\']+\.webp["\']([^>]*)>\s*</picture>'
    
    def replace_mixed_picture(match):
        nonlocal changes_made
        webp_base = match.group(1)  # filename without extension from optimized folder
        img_rest = match.group(2)   # rest of img attributes (including existing srcset)
        
        # Extract the base filename (without path and extension)
        base_name = webp_base + '.jpg'
        
        # Check if responsive WebP versions exist
        webp_exists, webp_name = check_webp_exists(base_name, base_dir)
        
        if not any(webp_exists.values()):
            print(f"  ⚠ No responsive WebP versions found for {webp_base}.webp, keeping as is")
            return match.group(0)
        
        # Parse img_rest to extract attributes and remove srcset (since we're creating a new one in source)
        full_img_tag = f'<img src="dummy"{img_rest}>'
        attributes = extract_img_attributes(full_img_tag)
        
        # Build attribute strings (excluding src and srcset)
        attrs = []
        if attributes.get('alt'):
            attrs.append(f'alt="{attributes["alt"]}"')
        if attributes.get('style'):
            attrs.append(f'style="{attributes["style"]}"')
        if attributes.get('onclick'):
            attrs.append(f'onclick="{attributes["onclick"]}"')
        if attributes.get('class'):
            attrs.append(f'class="{attributes["class"]}"')
        if attributes.get('loading'):
            attrs.append(f'loading="{attributes["loading"]}"')
        
        attr_string = ' '.join(attrs)
        
        # Build srcset based on available sizes
        webp_srcsets = []
        size_info = {
            'thumb': 300,
            'small': 640,
            'medium': 1024,
            'large': 1920,
            'full': 2560
        }
        
        for size, width in size_info.items():
            if webp_exists.get(size):
                webp_srcsets.append(f"responsive_images/{size}/{webp_name} {width}w")
        
        webp_srcset = ', '.join(webp_srcsets)
        sizes_attr = '(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw'
        
        new_picture = f'''<picture>
        <source srcset="{webp_srcset}" sizes="{sizes_attr}" type="image/webp">
        <img src="{base_name}" {attr_string}>
      </picture>'''
        
        changes_made += 1
        print(f"  ✓ Updated mixed picture tag: {webp_base}.webp (optimized source → responsive_images, img → jpg fallback)")
        
        return new_picture
    
    # Replace mixed picture tags
    content = re.sub(mixed_pattern, replace_mixed_picture, content, flags=re.IGNORECASE | re.DOTALL)
    
    # Third, find all img tags that reference JPG files (not already in responsive_images or picture tags)
    # IMPORTANT: Find matches AFTER the mixed_pattern replacement to get correct positions
    img_pattern = r'<img\s+[^>]*src=["\']([^"\']+\.jpg)["\'][^>]*>'
    
    # Find all matches in the UPDATED content
    matches = list(re.finditer(img_pattern, content, flags=re.IGNORECASE))
    
    # Process matches in reverse order to maintain position indices
    for match in reversed(matches):
        img_tag = match.group(0)
        src = match.group(1)
        
        # Skip if already in responsive_images folder
        if 'responsive_images/' in src:
            continue
        
        # Check if this img is already inside a picture tag
        pos = match.start()
        before_context = content[max(0, pos-1000):pos]
        
        # Count unclosed picture tags before this img
        open_tags = before_context.count('<picture>')
        close_tags_before = before_context.count('</picture>')
        
        # If there are more opening tags than closing tags, we're definitely inside a picture tag
        if open_tags > close_tags_before:
            continue
        # If counts are equal, check if the last picture tag before img is opening or closing
        elif open_tags == close_tags_before and open_tags > 0:
            last_close_pos = before_context.rfind('</picture>')
            last_open_pos = before_context.rfind('<picture>')
            if last_open_pos > last_close_pos:
                # Last tag before img is an opening tag, so we're inside it
                continue
        
        # Extract filename
        base_name = os.path.basename(src)
        
        # Extract attributes
        attributes = extract_img_attributes(img_tag)
        
        # Create picture tag
        new_tag = create_picture_tag(img_tag, base_name, base_dir, attributes)
        
        if new_tag != img_tag:
            changes_made += 1
            print(f"  ✓ Converting: {base_name}")
            
            # Replace this specific match in content
            content = content[:match.start()] + new_tag + content[match.end():]
    
    # Save if changes were made
    if changes_made > 0:
        # Create backup
        backup_file(filepath)
        
        # Write updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✓ Updated {changes_made} image(s) in {os.path.basename(filepath)}")
    else:
        print(f"\n  No changes needed for {os.path.basename(filepath)}")
    
    return changes_made


def main():
    """Main function to process all HTML files."""
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("\n" + "="*60)
    print("HTML Responsive Image Updater")
    print("Converting JPG images to responsive WebP with fallback")
    print("="*60)
    
    # Find all HTML files in the directory
    html_files = list(Path(script_dir).glob('*.html'))
    
    if not html_files:
        print("\n⚠ No HTML files found in the current directory")
        return
    
    print(f"\nFound {len(html_files)} HTML file(s):")
    for f in html_files:
        print(f"  - {f.name}")
    
    total_changes = 0
    
    # Process each HTML file
    for html_file in html_files:
        try:
            changes = process_html_file(str(html_file))
            total_changes += changes
        except Exception as e:
            print(f"\n✗ Error processing {html_file.name}: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total files processed: {len(html_files)}")
    print(f"Total images converted: {total_changes}")
    print("\n✓ Done!")
    
    if total_changes > 0:
        print("\nBackup files have been created with .backup_YYYYMMDD_HHMMSS extension")
        print("You can restore from backup if needed.")


if __name__ == '__main__':
    main()
