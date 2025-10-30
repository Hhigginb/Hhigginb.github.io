"""
Automatically update HTML files to use responsive images
BACKUP YOUR FILES FIRST!
"""

import os
import re
from datetime import datetime

def backup_file(filepath):
    """Create a backup of the HTML file"""
    backup_path = filepath + '.backup_' + datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Backup created: {backup_path}")
    return backup_path


def update_gallery_thumbnails(html_content):
    """
    Update gallery thumbnail images to use responsive images
    Looks for patterns like: <img src="bass.jpg" ... loading="lazy">
    """
    
    # Pattern for gallery thumbnails (images with onclick for modal)
    pattern = r'<img\s+src="([^"]+\.(?:jpg|jpeg|png|JPG|JPEG|PNG))"\s+([^>]*?)loading="lazy"([^>]*)>'
    
    def replace_func(match):
        original_src = match.group(1)
        before_loading = match.group(2)
        after_loading = match.group(3)
        
        # Get filename without extension
        basename = os.path.splitext(os.path.basename(original_src))[0]
        
        # Check if this is in a modal (onclick present) - use thumb for gallery
        if 'onclick' in before_loading or 'onclick' in after_loading:
            # Gallery thumbnail - use thumb and small
            new_img = (
                f'<img src="responsive_images/thumb/{basename}.webp" '
                f'srcset="responsive_images/thumb/{basename}.webp 300w, '
                f'responsive_images/small/{basename}.webp 640w" '
                f'sizes="(max-width: 640px) 50vw, 25vw" '
                f'{before_loading}loading="lazy"{after_loading}>'
            )
        else:
            # Regular image - use small, medium, large
            new_img = (
                f'<img src="responsive_images/medium/{basename}.webp" '
                f'srcset="responsive_images/small/{basename}.webp 640w, '
                f'responsive_images/medium/{basename}.webp 1024w, '
                f'responsive_images/large/{basename}.webp 1920w" '
                f'sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw" '
                f'{before_loading}loading="lazy"{after_loading}>'
            )
        
        return new_img
    
    updated_content = re.sub(pattern, replace_func, html_content)
    return updated_content


def update_modal_images(html_content):
    """
    Update modal/lightbox images to use full-size responsive images
    Looks for images inside modal divs
    """
    
    # Pattern for images in modals (typically have style="width:100%" and no loading attribute)
    # Modal pattern: <div id="modal-xxx" ... > <img src="xxx.jpg" ...> </div>
    
    pattern = r'(<div[^>]+class="[^"]*w3-modal[^"]*"[^>]*>.*?)<img\s+src="([^"]+\.(?:jpg|jpeg|png|JPG|JPEG|PNG))"\s+([^>]*?)>(.*?</div>)'
    
    def replace_func(match):
        before_img = match.group(1)
        original_src = match.group(2)
        img_attrs = match.group(3)
        after_img = match.group(4)
        
        # Get filename without extension
        basename = os.path.splitext(os.path.basename(original_src))[0]
        
        # Use full-size image for modal
        new_img = f'<img src="responsive_images/full/{basename}.webp" {img_attrs} loading="lazy">'
        
        return before_img + new_img + after_img
    
    updated_content = re.sub(pattern, replace_func, html_content, flags=re.DOTALL)
    return updated_content


def update_html_file(filepath, dry_run=True):
    """
    Update a single HTML file with responsive images
    
    Args:
        filepath: Path to HTML file
        dry_run: If True, only show changes without saving
    """
    
    print(f"\n{'='*70}")
    print(f"Processing: {os.path.basename(filepath)}")
    print(f"{'='*70}")
    
    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # Apply updates
    updated_content = original_content
    updated_content = update_gallery_thumbnails(updated_content)
    updated_content = update_modal_images(updated_content)
    
    # Count changes
    if updated_content == original_content:
        print("No changes needed.")
        return False
    
    # Count number of img tags changed
    original_imgs = len(re.findall(r'<img[^>]+>', original_content))
    updated_imgs = len(re.findall(r'<img[^>]+>', updated_content))
    changed_imgs = len(re.findall(r'responsive_images/', updated_content))
    
    print(f"\nSummary:")
    print(f"  Total images in file: {original_imgs}")
    print(f"  Images updated: {changed_imgs}")
    
    if dry_run:
        print(f"\n⚠️  DRY RUN MODE - No files modified")
        print(f"Changes would be made. Review and run with dry_run=False to apply.")
        
        # Show a sample of changes
        print(f"\nSample changes (first 500 characters):")
        print("-" * 70)
        
        # Find first responsive_images reference
        idx = updated_content.find('responsive_images/')
        if idx > 0:
            start = max(0, idx - 100)
            end = min(len(updated_content), idx + 400)
            print(updated_content[start:end])
        print("-" * 70)
        
    else:
        # Create backup
        backup_path = backup_file(filepath)
        
        # Save updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"\n✅ File updated successfully!")
        print(f"Backup saved: {os.path.basename(backup_path)}")
    
    return True


def main():
    """Main function"""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("="*70)
    print("HTML RESPONSIVE IMAGE UPDATER")
    print("="*70)
    print()
    print("⚠️  WARNING: This will modify your HTML files!")
    print("⚠️  Backups will be created automatically.")
    print()
    
    # Find HTML files
    html_files = [f for f in os.listdir(script_dir) 
                  if f.endswith('.html') and os.path.isfile(os.path.join(script_dir, f))]
    
    if not html_files:
        print("No HTML files found in current directory.")
        return
    
    print(f"Found {len(html_files)} HTML files:")
    for i, filename in enumerate(html_files, 1):
        print(f"  {i}. {filename}")
    print()
    
    # Check if responsive_images folder exists
    responsive_folder = os.path.join(script_dir, 'responsive_images')
    if not os.path.exists(responsive_folder):
        print("❌ ERROR: 'responsive_images' folder not found!")
        print("Please run CREATE_RESPONSIVE_IMAGES.bat first.")
        return
    
    print("✅ 'responsive_images' folder found.")
    print()
    
    # Ask user which mode
    print("Select mode:")
    print("  1. DRY RUN - Preview changes without modifying files (RECOMMENDED FIRST)")
    print("  2. APPLY CHANGES - Actually modify the HTML files")
    print()
    
    mode = input("Enter choice (1 or 2): ").strip()
    
    if mode == '1':
        dry_run = True
        print("\n🔍 Running in DRY RUN mode...\n")
    elif mode == '2':
        print("\n⚠️  This will MODIFY your HTML files!")
        confirm = input("Are you sure? Type 'YES' to confirm: ").strip()
        if confirm != 'YES':
            print("Cancelled.")
            return
        dry_run = False
        print("\n✏️  Applying changes...\n")
    else:
        print("Invalid choice. Cancelled.")
        return
    
    # Process each file
    modified_count = 0
    for filename in html_files:
        filepath = os.path.join(script_dir, filename)
        if update_html_file(filepath, dry_run=dry_run):
            modified_count += 1
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"Files processed: {len(html_files)}")
    print(f"Files with changes: {modified_count}")
    
    if dry_run:
        print(f"\n✅ Dry run complete. No files were modified.")
        print(f"Run again with mode 2 to apply changes.")
    else:
        print(f"\n✅ All changes applied!")
        print(f"Backups created with .backup_YYYYMMDD_HHMMSS extension")
        print(f"\nNext steps:")
        print(f"  1. Open your HTML files in a browser")
        print(f"  2. Test the responsive images")
        print(f"  3. Check DevTools → Network to verify correct sizes load")
        print(f"  4. If everything works, you can delete the .backup files")


if __name__ == "__main__":
    main()
