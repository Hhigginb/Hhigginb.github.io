import re
from datetime import datetime
import os

# Mapping of images to their available sizes
# Based on the script output, these images have different size availability
image_sizes = {
    'hk1': ['thumb', 'small', 'medium', 'large', 'full'],
    'hk2': ['thumb', 'small', 'medium', 'large', 'full'],
    'hk3': ['thumb', 'small', 'medium', 'large', 'full'],
    'hk4': ['thumb', 'small', 'medium', 'large', 'full'],
    'hk5': ['thumb', 'small', 'medium', 'large', 'full'],
    'hk6': ['thumb', 'small', 'full'],  # Too small for medium/large
    'tokyo1': ['thumb', 'small', 'medium', 'large', 'full'],
    'tokyo2': ['thumb', 'small', 'medium', 'large', 'full'],
    'tokyo3': ['thumb', 'small', 'medium', 'large', 'full'],
    'tokyo4': ['thumb', 'small', 'medium', 'large', 'full'],
    'tokyo5': ['thumb', 'small', 'medium', 'large', 'full'],
    'tokyo7': ['thumb', 'small', 'full'],  # Too small for medium/large
    'tokyo9': ['thumb', 'small', 'medium', 'large', 'full'],
    'tokyo10': ['thumb', 'small', 'medium', 'large', 'full'],
}

size_widths = {
    'thumb': '300w',
    'small': '640w',
    'medium': '1024w',
    'large': '1920w',
    'full': '2560w'
}

def build_srcset(image_name, available_sizes):
    """Build the srcset attribute based on available sizes"""
    srcset_parts = []
    for size in available_sizes:
        if size in ['thumb', 'small', 'medium', 'large', 'full']:
            srcset_parts.append(f"responsive_images/{size}/{image_name}.webp {size_widths[size]}")
    return ', '.join(srcset_parts)

def convert_heic_to_responsive(file_path):
    """Convert HEIC images from optimized to responsive format"""
    
    # Create backup
    backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Save backup
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Backup saved: {backup_path}")
    
    changes_made = 0
    
    # Pattern to match the optimized HEIC picture tags
    # Matches: <picture>\n<source srcset="optimized/NAME.webp" type="image/webp">\n<img src="NAME.HEIC" ...>
    pattern = re.compile(
        r'<picture>\s*\n\s*<source srcset="optimized/([a-zA-Z0-9_]+)\.webp" type="image/webp">\s*\n\s*<img src="\1\.HEIC"([^>]*)>',
        re.MULTILINE
    )
    
    def replace_func(match):
        nonlocal changes_made
        image_name = match.group(1)
        img_attributes = match.group(2)
        
        if image_name not in image_sizes:
            print(f"Warning: {image_name} not in image_sizes mapping, skipping")
            return match.group(0)
        
        available_sizes = image_sizes[image_name]
        srcset = build_srcset(image_name, available_sizes)
        
        # Build the new picture tag
        new_tag = f'''<picture>
            <source srcset="{srcset}" sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw" type="image/webp">
            <img src="{image_name}.HEIC"{img_attributes}>'''
        
        changes_made += 1
        print(f"Converted {image_name}.HEIC to responsive format")
        return new_tag
    
    # Apply the replacement
    new_content = pattern.sub(replace_func, content)
    
    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\nTotal conversions: {changes_made}")
    return changes_made

if __name__ == '__main__':
    file_path = 'heart.html'
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        exit(1)
    
    print(f"Converting HEIC images to responsive format in {file_path}...")
    changes = convert_heic_to_responsive(file_path)
    print(f"\nDone! Converted {changes} images.")
