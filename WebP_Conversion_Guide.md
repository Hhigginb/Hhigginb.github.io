# WebP Conversion Results and Manual Commands

## Why the PowerShell script didn't work:
The PowerShell script isn't executing properly in your conda environment. This is a common issue when conda's Python environment interferes with PowerShell script execution.

## Manual Conversion Results So Far:

### File Size Comparison:
| Original File | Original Size | WebP File | WebP Size | Savings |
|---------------|---------------|-----------|-----------|---------|
| hk1.HEIC | 2,112,472 bytes (2.01 MB) | hk1.webp | 1,337,820 bytes (1.28 MB) | 36.7% |
| hk2.HEIC | 947,891 bytes (0.90 MB) | hk2.webp | 561,292 bytes (0.53 MB) | 40.8% |
| tokyo1.HEIC | 1,575,076 bytes (1.50 MB) | tokyo1.webp | 1,000,336 bytes (0.95 MB) | 36.5% |

**Total savings so far: ~37% size reduction**

## Manual Commands to Convert Your Images:

### Convert remaining HEIC files:
```powershell
./cwebp.exe -q 85 hk3.HEIC -o optimized/hk3.webp
./cwebp.exe -q 85 hk4.HEIC -o optimized/hk4.webp
./cwebp.exe -q 85 hk5.HEIC -o optimized/hk5.webp
./cwebp.exe -q 85 tokyo2.HEIC -o optimized/tokyo2.webp
./cwebp.exe -q 85 tokyo3.HEIC -o optimized/tokyo3.webp
./cwebp.exe -q 85 tokyo4.HEIC -o optimized/tokyo4.webp
./cwebp.exe -q 85 tokyo5.HEIC -o optimized/tokyo5.webp
./cwebp.exe -q 85 tokyo9.HEIC -o optimized/tokyo9.webp
./cwebp.exe -q 85 tokyo10.HEIC -o optimized/tokyo10.webp
```

### Convert important JPG files (examples):
```powershell
./cwebp.exe -q 85 tbl_logo.jpg -o optimized/tbl_logo.webp
./cwebp.exe -q 85 h4h.jpg -o optimized/h4h.webp
./cwebp.exe -q 85 gbfb.jpg -o optimized/gbfb.webp
./cwebp.exe -q 85 nz3.jpg -o optimized/nz3.webp
./cwebp.exe -q 85 nz22.jpg -o optimized/nz22.webp
./cwebp.exe -q 85 nz2.jpg -o optimized/nz2.webp
```

### Convert PNG files (higher quality for graphics):
```powershell
./cwebp.exe -q 90 tbl.png -o optimized/tbl.webp
./cwebp.exe -q 90 fung2.png -o optimized/fung2.webp
./cwebp.exe -q 90 fung3.png -o optimized/fung3.webp
```

## Batch Convert All Files (Copy and paste this into PowerShell):

```powershell
# Convert all HEIC files
Get-ChildItem -Filter "*.HEIC" | ForEach-Object { 
    $output = "optimized/$($_.BaseName).webp"
    Write-Host "Converting $($_.Name) to $output"
    ./cwebp.exe -q 85 $_.Name -o $output
}

# Convert all JPG files
Get-ChildItem -Filter "*.jpg" | ForEach-Object { 
    $output = "optimized/$($_.BaseName).webp"
    Write-Host "Converting $($_.Name) to $output"
    ./cwebp.exe -q 85 $_.Name -o $output
}

# Convert all JPG files (uppercase)
Get-ChildItem -Filter "*.JPG" | ForEach-Object { 
    $output = "optimized/$($_.BaseName).webp"
    Write-Host "Converting $($_.Name) to $output"
    ./cwebp.exe -q 85 $_.Name -o $output
}

# Convert all PNG files
Get-ChildItem -Filter "*.png" | ForEach-Object { 
    $output = "optimized/$($_.BaseName).webp"
    Write-Host "Converting $($_.Name) to $output"
    ./cwebp.exe -q 90 $_.Name -o $output
}
```

## Next Steps:
1. Run the batch commands above to convert all your images
2. Update your HTML to use the WebP files (see below)
3. Test your website to ensure images load correctly

## HTML Update Example:
Replace:
```html
<img src="hk1.HEIC" style="max-width:250px" alt="hk1">
```

With:
```html
<picture>
  <source srcset="optimized/hk1.webp" type="image/webp">
  <img src="hk1.HEIC" style="max-width:250px" alt="hk1" loading="lazy">
</picture>
```

This provides WebP for modern browsers with fallback to original files for older browsers.
