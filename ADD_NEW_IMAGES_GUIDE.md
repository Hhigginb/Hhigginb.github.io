# 📸 Adding New Images to Your Website

## Quick Guide: Add 3 New Images

### Option A: Quick & Easy (Recommended for a few images)

**Step 1:** Place your 3 new images in the main folder
```
your-folder/
├── new-image-1.jpg  ← Your new image
├── new-image-2.jpg  ← Your new image
├── new-image-3.jpg  ← Your new image
└── (existing images...)
```

**Step 2:** Create a script just for these 3 images

I'll create `CONVERT_NEW_IMAGES.bat` that only processes specific files.

**Step 3:** Run the script
- Double-click `CONVERT_NEW_IMAGES.bat`
- It will create responsive versions in `responsive_images/`

**Step 4:** Add to your HTML manually
```html
<img src="responsive_images/thumb/new-image-1.webp" 
     srcset="responsive_images/small/new-image-1.webp 640w,
             responsive_images/medium/new-image-1.webp 1024w,
             responsive_images/large/new-image-1.webp 1920w"
     sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
     alt="Your description" 
     loading="lazy">
```

---

### Option B: Rerun Full Conversion (Works for any number of images)

**Step 1:** Place your 3 new images in the main folder

**Step 2:** Run `CREATE_RESPONSIVE_IMAGES.bat`
- It will process ALL images (including the 3 new ones)
- Existing converted images won't be duplicated
- New images will be added to `responsive_images/`

**Step 3:** Manually add the HTML for the 3 new images

---

### Option C: Individual Image Converter (Most Flexible)

Create a script that lets you specify exactly which images to convert.

---

## Which Option Should You Choose?

| Situation | Best Option |
|-----------|-------------|
| Adding 1-5 images | **Option A** - Quick script for specific files |
| Already have `responsive_images/` folder | **Option B** - Rerun full script |
| Want maximum control | **Option C** - Individual converter |
| First time adding images | **Option A** |

---

## Detailed Steps for Option A (Recommended)

### 1. Place Your Images
Copy your 3 images to the main folder:
```
c:\Users\h0100\...\Hhigginb.github.io\
```

### 2. Create a List
I'll create a script that asks you which images to convert, or you can specify the filenames.

### 3. Run Conversion
The script will:
- ✅ Fix EXIF orientation
- ✅ Convert to WebP
- ✅ Create 5 sizes (thumb, small, medium, large, full)
- ✅ Place in `responsive_images/` folder

### 4. Update HTML
Add the responsive image code to `hand.html`, `heart.html`, or `mind.html`:

**Gallery Thumbnail Example:**
```html
<div class="w3-col l3 m6 w3-margin-bottom">
  <img src="responsive_images/thumb/your-image.webp" 
       srcset="responsive_images/thumb/your-image.webp 300w,
               responsive_images/small/your-image.webp 640w"
       sizes="(max-width: 640px) 50vw, 25vw"
       alt="Your description" 
       style="width:100%" 
       onclick="document.getElementById('modal-yourimage').style.display='block'" 
       class="w3-hover-opacity" 
       loading="lazy">
</div>
```

**Modal/Lightbox Example:**
```html
<div id="modal-yourimage" class="w3-modal" onclick="this.style.display='none'">
  <span class="w3-button w3-hover-red w3-xlarge w3-display-topright">&times;</span>
  <div class="w3-modal-content w3-animate-zoom">
    <img src="responsive_images/full/your-image.webp" 
         style="width:100%"
         loading="lazy">
  </div>
</div>
```

### 5. Test
- Open your HTML in a browser
- Verify images display correctly
- Check responsive behavior (resize window)

---

## Example: Adding 3 Specific Images

Let's say your images are:
- `project-new.jpg`
- `adventure-2025.jpg`
- `art-piece.png`

### Step-by-Step:

**1. Copy files to main folder**

**2. Run this command in PowerShell:**
```powershell
python create_responsive_images.py
```

Or use the batch file I'll create for you that only processes specific files.

**3. The script creates:**
```
responsive_images/
├── thumb/
│   ├── project-new.webp
│   ├── adventure-2025.webp
│   └── art-piece.webp
├── small/
│   └── (same files...)
├── medium/
│   └── (same files...)
├── large/
│   └── (same files...)
└── full/
    └── (same files...)
```

**4. Add HTML to your page**

---

## Time Required

- **Option A (3 images):** ~2-3 minutes
- **Option B (rerun all):** ~5-10 minutes
- **Manual HTML update:** ~5 minutes per image

**Total: ~10-15 minutes for 3 new images**

---

## Tips

### Naming Your Images
Use descriptive filenames:
- ✅ `pottery-bowl-2025.jpg`
- ✅ `hiking-mt-washington.jpg`
- ❌ `IMG_1234.jpg`
- ❌ `photo.jpg`

This makes HTML updates easier!

### Before Converting
1. Rename images to descriptive names
2. Check orientation (take a photo in landscape? portrait?)
3. Verify they're in the main folder (not subfolder)

### After Converting
1. Check `responsive_images/thumb/` to see if they converted
2. Open one in a browser to verify orientation is correct
3. Add to HTML and test!

---

## Quick Reference: File Locations

Your new images go here:
```
c:\Users\h0100\OneDrive - Massachusetts Institute of Technology\Documents\GitHub\Hhigginb.github.io\
```

Responsive versions appear here:
```
c:\Users\h0100\OneDrive - Massachusetts Institute of Technology\Documents\GitHub\Hhigginb.github.io\responsive_images\
```

Update HTML here:
```
hand.html   ← Projects & Athletics
heart.html  ← Outreach & Adventures  
mind.html   ← Courses & Research
```

---

## Need Help?

See:
- `RESPONSIVE_IMAGES_GUIDE.md` - HTML examples
- `COMPLETE_GUIDE.md` - Full workflow
- `VISUAL_WORKFLOW.md` - Diagrams

---

**Ready to add your 3 images? I can create a custom script for you!**
