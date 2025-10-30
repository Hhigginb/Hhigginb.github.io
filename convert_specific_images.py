"""
Convert specific images to responsive WebP formats
Perfect for adding new images to your website!
"""

import os
from PIL import Image, ImageOps

# Define responsive sizes
SIZES = {
    'thumb': 300,
    'small': 640,
    'medium': 1024,
    'large': 1920,
}

def create_responsive_versions(input_path, output_folder, quality=85):
    """Create multiple sized versions of an image with proper orientation"""
    try:
        filename = os.path.basename(input_path)
        name_only = os.path.splitext(filename)[0]
        
        print(f"\n{'='*70}")
        print(f"Processing: {filename}")
        print(f"{'='*70}")
        
        with Image.open(input_path) as img:
            # Fix orientation based on EXIF data
            oriented_img = ImageOps.exif_transpose(img)
            if oriented_img is None:
                oriented_img = img
            
            # Convert to RGB
            if oriented_img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', oriented_img.size, (255, 255, 255))
                if oriented_img.mode == 'P':
                    oriented_img = oriented_img.convert('RGBA')
                background.paste(oriented_img, mask=oriented_img.split()[-1] if oriented_img.mode in ('RGBA', 'LA') else None)
                oriented_img = background
            elif oriented_img.mode != 'RGB':
                oriented_img = oriented_img.convert('RGB')
            
            orig_width, orig_height = oriented_img.size
            print(f"Original size: {orig_width}x{orig_height}")
            
            # Create each size
            for size_name, max_width in SIZES.items():
                if orig_width <= max_width and size_name != 'thumb':
                    print(f"  Skipping {size_name} (original is smaller)")
                    continue
                
                # Calculate new dimensions
                if orig_width > max_width:
                    ratio = max_width / orig_width
                    new_width = max_width
                    new_height = int(orig_height * ratio)
                else:
                    new_width = orig_width
                    new_height = orig_height
                
                # Create folder
                size_folder = os.path.join(output_folder, size_name)
                os.makedirs(size_folder, exist_ok=True)
                
                # Resize and save
                resized = oriented_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                output_path = os.path.join(size_folder, f"{name_only}.webp")
                resized.save(output_path, 'WEBP', quality=quality, method=6)
                
                file_size = os.path.getsize(output_path) / 1024
                print(f"  ✅ Created {size_name}: {new_width}x{new_height} ({file_size:.1f} KB)")
            
            # Full size version
            full_folder = os.path.join(output_folder, 'full')
            os.makedirs(full_folder, exist_ok=True)
            full_path = os.path.join(full_folder, f"{name_only}.webp")
            oriented_img.save(full_path, 'WEBP', quality=quality, method=6)
            file_size = os.path.getsize(full_path) / 1024
            print(f"  ✅ Created full: {orig_width}x{orig_height} ({file_size:.1f} KB)")
            
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def main():
    """Main function - convert specific images"""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_base = os.path.join(script_dir, "responsive_images")
    
    print("=" * 70)
    print("CONVERT SPECIFIC IMAGES TO RESPONSIVE WEBP")
    print("=" * 70)
    print()
    print("This tool converts only the images you specify.")
    print("Perfect for adding new images without reprocessing everything!")
    print()
    print(f"Output folder: {output_base}")
    print()
    
    # Method 1: User enters filenames
    print("Enter the filenames of images to convert (one per line).")
    print("Filenames should be in the current directory.")
    print("Type 'done' when finished.")
    print()
    print("Examples:")
    print("  project-photo.jpg")
    print("  adventure-2025.JPG")
    print("  artwork.png")
    print()
    
    images_to_process = []
    
    while True:
        filename = input("Enter filename (or 'done'): ").strip()
        
        if filename.lower() == 'done':
            break
        
        if not filename:
            continue
        
        # Check if file exists
        filepath = os.path.join(script_dir, filename)
        
        if os.path.exists(filepath):
            images_to_process.append(filepath)
            print(f"  ✅ Added: {filename}")
        else:
            print(f"  ❌ File not found: {filename}")
            print(f"     Make sure the file is in: {script_dir}")
    
    if not images_to_process:
        print()
        print("No images specified. Exiting.")
        return
    
    # Confirm
    print()
    print("=" * 70)
    print(f"Ready to process {len(images_to_process)} image(s):")
    for img_path in images_to_process:
        print(f"  • {os.path.basename(img_path)}")
    print()
    print("Each image will be converted to 5 sizes:")
    print("  - thumb (300px) - for gallery thumbnails")
    print("  - small (640px) - for mobile devices")
    print("  - medium (1024px) - for tablets")
    print("  - large (1920px) - for desktops")
    print("  - full (original size) - for lightbox/modal")
    print()
    
    response = input("Continue? (y/n): ").strip().lower()
    if response != 'y':
        print("Cancelled.")
        return
    
    # Process images
    print()
    print("Processing images...")
    
    success_count = 0
    fail_count = 0
    
    for img_path in images_to_process:
        if create_responsive_versions(img_path, output_base):
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print()
    print("=" * 70)
    print("CONVERSION COMPLETE!")
    print("=" * 70)
    print(f"✅ Successfully processed: {success_count}")
    if fail_count > 0:
        print(f"❌ Failed: {fail_count}")
    print()
    print(f"Output location: {output_base}")
    print()
    print("Your responsive images are in:")
    print("  responsive_images/thumb/")
    print("  responsive_images/small/")
    print("  responsive_images/medium/")
    print("  responsive_images/large/")
    print("  responsive_images/full/")
    print()
    print("Next step: Add these images to your HTML!")
    print("See ADD_NEW_IMAGES_GUIDE.md for HTML examples.")
    print()


if __name__ == "__main__":
    main()
