from PIL import Image
import os
from pathlib import Path

# Define size configurations
sizes = {
    'thumb': 300,
    'small': 640,
    'medium': 1024,
    'large': 1920,
    'full': 2560
}

def create_responsive_from_optimized(source_folder, output_base_folder, image_names):
    """
    Create responsive versions of images from optimized folder
    
    Args:
        source_folder: Path to optimized folder containing WebP images
        output_base_folder: Base path for responsive_images folder
        image_names: List of image filenames (without extension)
    """
    
    processed = 0
    skipped = 0
    
    for name in image_names:
        source_path = os.path.join(source_folder, f"{name}.webp")
        
        if not os.path.exists(source_path):
            print(f"Warning: {source_path} not found, skipping")
            skipped += 1
            continue
        
        try:
            # Open source image
            img = Image.open(source_path)
            original_width, original_height = img.size
            
            print(f"\nProcessing {name}.webp ({original_width}x{original_height})")
            
            # Create each size
            for size_name, target_width in sizes.items():
                # Skip if original is smaller than target
                if original_width <= target_width and size_name != 'full':
                    print(f"  Skipping {size_name} (original too small)")
                    continue
                
                # Create output folder if it doesn't exist
                output_folder = os.path.join(output_base_folder, size_name)
                os.makedirs(output_folder, exist_ok=True)
                
                output_path = os.path.join(output_folder, f"{name}.webp")
                
                # Skip if already exists
                if os.path.exists(output_path):
                    print(f"  Skipping {size_name} (already exists)")
                    continue
                
                # For 'full' size, just copy if smaller than 2560, otherwise resize
                if size_name == 'full':
                    if original_width <= target_width:
                        img.save(output_path, 'WEBP', quality=85, method=6)
                        print(f"  Created {size_name}: {original_width}x{original_height}")
                    else:
                        # Calculate new dimensions
                        aspect_ratio = original_height / original_width
                        new_width = target_width
                        new_height = int(target_width * aspect_ratio)
                        
                        # Resize and save
                        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        resized.save(output_path, 'WEBP', quality=85, method=6)
                        print(f"  Created {size_name}: {new_width}x{new_height}")
                else:
                    # Calculate new dimensions
                    aspect_ratio = original_height / original_width
                    new_width = target_width
                    new_height = int(target_width * aspect_ratio)
                    
                    # Resize and save
                    resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    resized.save(output_path, 'WEBP', quality=85, method=6)
                    print(f"  Created {size_name}: {new_width}x{new_height}")
            
            processed += 1
            
        except Exception as e:
            print(f"Error processing {name}: {e}")
            skipped += 1
    
    print(f"\n{'='*60}")
    print(f"Processed: {processed} images")
    print(f"Skipped: {skipped} images")
    print(f"{'='*60}")

if __name__ == '__main__':
    # Define image names
    tokyo_images = ['tokyo1', 'tokyo2', 'tokyo3', 'tokyo4', 'tokyo5', 'tokyo7', 'tokyo9', 'tokyo10']
    hk_images = ['hk1', 'hk2', 'hk3', 'hk4', 'hk5', 'hk6']
    
    all_images = tokyo_images + hk_images
    
    source_folder = 'optimized'
    output_folder = 'responsive_images'
    
    print(f"Creating responsive versions from {source_folder}...")
    print(f"Output folder: {output_folder}")
    print(f"Images to process: {len(all_images)}")
    
    create_responsive_from_optimized(source_folder, output_folder, all_images)
    
    print("\nDone!")
