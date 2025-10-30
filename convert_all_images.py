# Full WebP Converter - All Images with Auto-Orient
# Converts all JPG, JPEG, PNG, and HEIC files with proper orientation

from PIL import Image, ImageOps
import os
import glob

def convert_with_orientation(input_path, output_path, quality=85):
    """Convert image to WebP with proper orientation."""
    try:
        with Image.open(input_path) as img:
            # Auto-orient based on EXIF data
            oriented_img = ImageOps.exif_transpose(img)
            if oriented_img is None:
                oriented_img = img
            
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
            return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def main():
    # Output directory
    output_dir = 'optimized_python'
    os.makedirs(output_dir, exist_ok=True)
      # Get all image files in CURRENT DIRECTORY ONLY (not subfolders)
    extensions = ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG', '*.png', '*.PNG', '*.HEIC', '*.heic']
    all_images = []
    for ext in extensions:
        # glob.glob doesn't recurse by default, but let's be explicit
        found_files = glob.glob(ext)
        # Filter out any files that are in subdirectories
        found_files = [f for f in found_files if os.path.dirname(f) == '' or os.path.dirname(f) == '.']
        all_images.extend(found_files)
    
    print("=" * 70)
    print("PYTHON WEBP CONVERTER - FULL BATCH")
    print("=" * 70)
    print("NOTE: Only converting files in current directory (not subfolders)")
    print(f"Found {len(all_images)} images to convert")
    print(f"Output folder: {output_dir}\\")
    print("=" * 70)
    print()
    
    # Ask for confirmation
    response = input("Continue? (y/n): ").lower()
    if response != 'y':
        print("Cancelled.")
        return
    
    print()
    
    success_count = 0
    fail_count = 0
    total_orig_size = 0
    total_new_size = 0
    
    for i, img_file in enumerate(sorted(all_images), 1):
        basename = os.path.splitext(img_file)[0]
        output_file = os.path.join(output_dir, basename + '.webp')
        
        # Skip if already exists
        if os.path.exists(output_file):
            print(f"[{i}/{len(all_images)}] Skipping {img_file} (already converted)")
            continue
        
        print(f"[{i}/{len(all_images)}] Converting {img_file}...", end=' ')
        
        try:
            orig_size = os.path.getsize(img_file)
            
            # Determine quality based on file type
            quality = 90 if img_file.lower().endswith('.png') else 85
            
            if convert_with_orientation(img_file, output_file, quality=quality):
                new_size = os.path.getsize(output_file)
                saved = orig_size - new_size
                saved_pct = (saved / orig_size) * 100
                
                total_orig_size += orig_size
                total_new_size += new_size
                success_count += 1
                
                print(f"✓ {orig_size:,} -> {new_size:,} bytes ({saved_pct:+.1f}%)")
            else:
                fail_count += 1
                print("✗ FAILED")
        except Exception as e:
            fail_count += 1
            print(f"✗ ERROR: {e}")
    
    print()
    print("=" * 70)
    print("CONVERSION COMPLETE!")
    print("=" * 70)
    print(f"Successfully converted: {success_count} images")
    if fail_count > 0:
        print(f"Failed: {fail_count} images")
    
    if success_count > 0:
        total_saved = total_orig_size - total_new_size
        saved_pct = (total_saved / total_orig_size) * 100
        print(f"\nOriginal size: {total_orig_size:,} bytes ({total_orig_size/1024/1024:.2f} MB)")
        print(f"New size: {total_new_size:,} bytes ({total_new_size/1024/1024:.2f} MB)")
        print(f"Total saved: {total_saved:,} bytes ({total_saved/1024/1024:.2f} MB)")
        print(f"Reduction: {saved_pct:.1f}%")
    
    print(f"\nConverted files are in: {output_dir}\\")
    print("=" * 70)

if __name__ == "__main__":
    main()
