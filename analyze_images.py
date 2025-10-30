"""
Analyze current images and estimate responsive image savings
"""

import os
import glob
from PIL import Image

def format_size(bytes):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.1f} TB"

def analyze_images():
    """Analyze all images in the directory"""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("="*70)
    print("IMAGE ANALYSIS & SAVINGS ESTIMATOR")
    print("="*70)
    print()
    
    # Find all image files
    extensions = ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG', '*.png', '*.PNG']
    all_images = []
    
    for ext in extensions:
        pattern = os.path.join(script_dir, ext)
        found_files = glob.glob(pattern)
        found_files = [f for f in found_files if os.path.dirname(f) == script_dir]
        all_images.extend(found_files)
    
    all_images = sorted(list(set(all_images)))
    
    if not all_images:
        print("No images found in current directory.")
        return
    
    print(f"Found {len(all_images)} images\n")
    
    # Analyze each image
    total_size = 0
    total_pixels = 0
    sizes_info = []
    
    for img_path in all_images:
        try:
            file_size = os.path.getsize(img_path)
            total_size += file_size
            
            with Image.open(img_path) as img:
                width, height = img.size
                pixels = width * height
                total_pixels += pixels
                
                sizes_info.append({
                    'name': os.path.basename(img_path),
                    'size': file_size,
                    'width': width,
                    'height': height,
                    'pixels': pixels
                })
        except Exception as e:
            print(f"Error analyzing {os.path.basename(img_path)}: {e}")
    
    # Sort by size
    sizes_info.sort(key=lambda x: x['size'], reverse=True)
    
    # Show top 10 largest
    print("Top 10 Largest Images:")
    print("-" * 70)
    print(f"{'Filename':<30} {'Size':<12} {'Dimensions':<15}")
    print("-" * 70)
    
    for info in sizes_info[:10]:
        print(f"{info['name']:<30} {format_size(info['size']):<12} {info['width']}x{info['height']}")
    
    print()
    
    # Calculate statistics
    avg_size = total_size / len(all_images)
    avg_width = sum(info['width'] for info in sizes_info) / len(sizes_info)
    avg_height = sum(info['height'] for info in sizes_info) / len(sizes_info)
    
    print("Current Statistics:")
    print("-" * 70)
    print(f"Total images: {len(all_images)}")
    print(f"Total size: {format_size(total_size)}")
    print(f"Average size: {format_size(avg_size)}")
    print(f"Average dimensions: {avg_width:.0f}x{avg_height:.0f}")
    print()
    
    # Estimate responsive image savings
    print("Estimated Savings with Responsive Images:")
    print("-" * 70)
    
    # Estimate compression (WebP + smaller sizes)
    # Assumptions:
    # - WebP saves ~30% over JPEG at same quality
    # - Mobile users get small (640px) = ~10% of pixels
    # - Tablet users get medium (1024px) = ~25% of pixels  
    # - Desktop users get large (1920px) = ~60% of pixels
    
    # Distribution: 50% mobile, 30% tablet, 20% desktop
    mobile_ratio = 0.50
    tablet_ratio = 0.30
    desktop_ratio = 0.20
    
    # Size reductions (pixel count + WebP compression)
    mobile_reduction = 0.10 * 0.70  # 10% pixels, 70% quality
    tablet_reduction = 0.25 * 0.70
    desktop_reduction = 0.60 * 0.70
    
    avg_reduction = (mobile_ratio * mobile_reduction + 
                    tablet_ratio * tablet_reduction + 
                    desktop_ratio * desktop_reduction)
    
    estimated_new_size = total_size * avg_reduction
    savings = total_size - estimated_new_size
    savings_percent = (savings / total_size) * 100
    
    print(f"\nTraffic distribution assumption:")
    print(f"  📱 Mobile: {mobile_ratio*100:.0f}%")
    print(f"  📱 Tablet: {tablet_ratio*100:.0f}%")
    print(f"  💻 Desktop: {desktop_ratio*100:.0f}%")
    print()
    print(f"Current total size: {format_size(total_size)}")
    print(f"Estimated new size: {format_size(estimated_new_size)}")
    print(f"Estimated savings: {format_size(savings)} ({savings_percent:.0f}%)")
    print()
    
    # Per-user savings
    print("Per-User Savings:")
    print("-" * 70)
    
    mobile_current = total_size / len(all_images)
    mobile_new = mobile_current * mobile_reduction
    mobile_saved = mobile_current - mobile_new
    
    tablet_new = mobile_current * tablet_reduction
    tablet_saved = mobile_current - tablet_new
    
    desktop_new = mobile_current * desktop_reduction
    desktop_saved = mobile_current - desktop_new
    
    print(f"📱 Mobile user viewing all {len(all_images)} images:")
    print(f"   Before: {format_size(total_size)}")
    print(f"   After:  {format_size(mobile_new * len(all_images))}")
    print(f"   Saves:  {format_size(mobile_saved * len(all_images))} ({(mobile_saved/mobile_current)*100:.0f}%)")
    print()
    print(f"📱 Tablet user viewing all {len(all_images)} images:")
    print(f"   Before: {format_size(total_size)}")
    print(f"   After:  {format_size(tablet_new * len(all_images))}")
    print(f"   Saves:  {format_size(tablet_saved * len(all_images))} ({(tablet_saved/mobile_current)*100:.0f}%)")
    print()
    print(f"💻 Desktop user viewing all {len(all_images)} images:")
    print(f"   Before: {format_size(total_size)}")
    print(f"   After:  {format_size(desktop_new * len(all_images))}")
    print(f"   Saves:  {format_size(desktop_saved * len(all_images))} ({(desktop_saved/mobile_current)*100:.0f}%)")
    print()
    
    # Page load time estimate (assuming 4G mobile = 10 Mbps)
    mobile_speed_mbps = 10
    mobile_speed_bps = mobile_speed_mbps * 1024 * 1024 / 8  # bytes per second
    
    current_load_time = total_size / mobile_speed_bps
    new_load_time = (mobile_new * len(all_images)) / mobile_speed_bps
    time_saved = current_load_time - new_load_time
    
    print(f"Estimated Page Load Time (4G mobile, all images):")
    print(f"   Before: {current_load_time:.1f} seconds")
    print(f"   After:  {new_load_time:.1f} seconds")
    print(f"   Saves:  {time_saved:.1f} seconds ({(time_saved/current_load_time)*100:.0f}% faster)")
    print()
    
    print("="*70)
    print("Ready to optimize? Run CREATE_RESPONSIVE_IMAGES.bat")
    print("="*70)

if __name__ == "__main__":
    analyze_images()
