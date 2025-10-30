"""
Create responsive image sizes for efficient web loading
Generates thumbnail, small, medium, and large versions of images
"""

import os
from PIL import Image, ImageOps
import glob

# Define responsive sizes
SIZES = {
    'thumb': 300,    # Thumbnails for gallery previews
    'small': 640,    # Mobile devices
    'medium': 1024,  # Tablets and small desktops
    'large': 1920,   # Large desktops and high-res displays
}

def create_responsive_versions(input_path, output_folder, quality=85):
    """
    Creates multiple sized versions of an image with proper orientation
    
    Args:
        input_path: Path to the original image
        output_folder: Base folder for output (will create size subfolders)
        quality: WebP quality (default 85)
    """
    try:
        # Get filename without extension
        filename = os.path.basename(input_path)
        name_only = os.path.splitext(filename)[0]
        
        print(f"Processing: {filename}")
        
        # Open and orient the image
        with Image.open(input_path) as img:
            # Fix orientation based on EXIF data
            oriented_img = ImageOps.exif_transpose(img)
            
            if oriented_img is None:
                oriented_img = img
            
            # Convert RGBA to RGB if needed
            if oriented_img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', oriented_img.size, (255, 255, 255))
                if oriented_img.mode == 'P':
                    oriented_img = oriented_img.convert('RGBA')
                background.paste(oriented_img, mask=oriented_img.split()[-1] if oriented_img.mode in ('RGBA', 'LA') else None)
                oriented_img = background
            elif oriented_img.mode != 'RGB':
                oriented_img = oriented_img.convert('RGB')
            
            # Get original dimensions
            orig_width, orig_height = oriented_img.size
            print(f"  Original size: {orig_width}x{orig_height}")
            
            # Create each size
            for size_name, max_width in SIZES.items():
                # Skip if original is smaller than target size
                if orig_width <= max_width and size_name != 'thumb':
                    print(f"  Skipping {size_name} (original is smaller)")
                    continue
                
                # Calculate new dimensions (maintain aspect ratio)
                if orig_width > max_width:
                    ratio = max_width / orig_width
                    new_width = max_width
                    new_height = int(orig_height * ratio)
                else:
                    new_width = orig_width
                    new_height = orig_height
                
                # Create size-specific folder
                size_folder = os.path.join(output_folder, size_name)
                os.makedirs(size_folder, exist_ok=True)
                
                # Resize image
                resized = oriented_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Save as WebP
                output_path = os.path.join(size_folder, f"{name_only}.webp")
                resized.save(output_path, 'WEBP', quality=quality, method=6)
                
                # Get file size
                file_size = os.path.getsize(output_path) / 1024  # KB
                print(f"  Created {size_name}: {new_width}x{new_height} ({file_size:.1f} KB)")
            
            # Also save a full-size version (original dimensions, just converted to WebP)
            full_folder = os.path.join(output_folder, 'full')
            os.makedirs(full_folder, exist_ok=True)
            full_path = os.path.join(full_folder, f"{name_only}.webp")
            oriented_img.save(full_path, 'WEBP', quality=quality, method=6)
            file_size = os.path.getsize(full_path) / 1024
            print(f"  Created full: {orig_width}x{orig_height} ({file_size:.1f} KB)")
            
        return True
        
    except Exception as e:
        print(f"ERROR processing {input_path}: {str(e)}")
        return False


def main():
    """Main function to process all images"""
    
    # Input/output configuration
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_base = os.path.join(script_dir, "responsive_images")
    
    print("=" * 70)
    print("RESPONSIVE IMAGE GENERATOR")
    print("=" * 70)
    print(f"Output folder: {output_base}")
    print()
    
    # Find all image files (only in main directory, not subfolders)
    extensions = ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG', '*.png', '*.PNG']
    all_images = []
    
    for ext in extensions:
        pattern = os.path.join(script_dir, ext)
        found_files = glob.glob(pattern)
        
        # Filter to only main directory (exclude subdirectories)
        found_files = [f for f in found_files 
                      if os.path.dirname(f) == script_dir]
        
        all_images.extend(found_files)
    
    # Remove duplicates and sort
    all_images = sorted(list(set(all_images)))
    
    print(f"Found {len(all_images)} images to process")
    print()
    
    if len(all_images) == 0:
        print("No images found! Make sure you have JPG or PNG files in the main directory.")
        return
    
    # Ask for confirmation
    print("This will create 5 versions of each image:")
    print("  - thumb (300px width) - for gallery thumbnails")
    print("  - small (640px width) - for mobile devices")
    print("  - medium (1024px width) - for tablets")
    print("  - large (1920px width) - for desktops")
    print("  - full (original size) - for lightbox/modal view")
    print()
    
    response = input("Continue? (y/n): ").strip().lower()
    if response != 'y':
        print("Cancelled.")
        return
    
    print()
    print("Processing images...")
    print()
    
    # Process each image
    success_count = 0
    fail_count = 0
    
    for img_path in all_images:
        if create_responsive_versions(img_path, output_base):
            success_count += 1
        else:
            fail_count += 1
        print()  # Blank line between images
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Successfully processed: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"Total images: {len(all_images)}")
    print()
    print(f"Output location: {output_base}")
    print()
    print("Folder structure:")
    print("  responsive_images/")
    print("    ├── thumb/     (300px - gallery thumbnails)")
    print("    ├── small/     (640px - mobile)")
    print("    ├── medium/    (1024px - tablet)")
    print("    ├── large/     (1920px - desktop)")
    print("    └── full/      (original size - lightbox)")
    print()
    print("Next step: Update your HTML to use responsive images.")
    print("See RESPONSIVE_IMAGES_GUIDE.md for instructions.")


if __name__ == "__main__":
    main()
