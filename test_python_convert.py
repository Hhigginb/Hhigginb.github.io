# Simple WebP Converter with Auto-Orient
# No external tools needed - just Python + Pillow
# Fixes rotation issues by reading EXIF and rotating pixel data

from PIL import Image, ImageOps
import os
import glob

def convert_with_orientation(input_path, output_path, quality=85):
    """Convert image to WebP with proper orientation."""
    try:
        with Image.open(input_path) as img:
            # Get original dimensions
            orig_width, orig_height = img.size
            
            # Auto-orient based on EXIF data
            oriented_img = ImageOps.exif_transpose(img)
            if oriented_img is None:
                oriented_img = img
            
            # Get new dimensions after orientation
            new_width, new_height = oriented_img.size
            
            # Convert to RGB if needed
            if oriented_img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', oriented_img.size, (255, 255, 255))
                if oriented_img.mode == 'P':
                    oriented_img = oriented_img.convert('RGBA')
                if 'A' in oriented_img.mode:
                    background.paste(oriented_img, mask=oriented_img.split()[-1])
                else:
                    background.paste(oriented_img)
                oriented_img = background
            elif oriented_img.mode != 'RGB':
                oriented_img = oriented_img.convert('RGB')
            
            # Save as WebP
            oriented_img.save(output_path, 'WEBP', quality=quality)
            
            # Show what happened
            if orig_width != new_width or orig_height != new_height:
                print(f"  Rotated: {orig_width}x{orig_height} -> {new_width}x{new_height}")
            else:
                print(f"  No rotation needed: {orig_width}x{orig_height}")
            
            return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def main():
    # Test with 3 images in current directory only (not subfolders)
    test_images = ['eu-ham4.jpg', 'eu-leu.jpg', 'nz3.jpg']
    
    # Create output folder
    output_dir = 'optimized_test_python'
    os.makedirs(output_dir, exist_ok=True)
    
    print("NOTE: Only converting files in current directory (not subfolders)")
    print()
    
    print("=" * 60)
    print("PYTHON WEBP CONVERTER - TEST BATCH")
    print("Using PIL/Pillow to fix orientation automatically")
    print("=" * 60)
    
    success_count = 0
    total_saved = 0
    
    for img_file in test_images:
        if not os.path.exists(img_file):
            print(f"\nSkipping {img_file} (not found)")
            continue
        
        output_file = os.path.join(output_dir, os.path.splitext(img_file)[0] + '.webp')
        
        print(f"\nConverting {img_file}...")
        
        orig_size = os.path.getsize(img_file)
        
        if convert_with_orientation(img_file, output_file, quality=85):
            new_size = os.path.getsize(output_file)
            saved = orig_size - new_size
            saved_pct = (saved / orig_size) * 100
            total_saved += saved
            success_count += 1
            
            print(f"  Size: {orig_size:,} -> {new_size:,} bytes")
            print(f"  Saved: {saved:,} bytes ({saved_pct:.1f}%)")
            print(f"  Output: {output_file}")
    
    print("\n" + "=" * 60)
    print(f"SUCCESS! Converted {success_count} of {len(test_images)} images")
    if success_count > 0:
        print(f"Total saved: {total_saved:,} bytes ({total_saved/1024/1024:.2f} MB)")
    print("=" * 60)
    print(f"\nCheck the '{output_dir}' folder to verify orientation!")
    print("If images look correct, run: python convert_all_images.py")

if __name__ == "__main__":
    main()
