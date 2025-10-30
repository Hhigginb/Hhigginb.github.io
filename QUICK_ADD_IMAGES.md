# ⚡ QUICK REFERENCE: Adding 3 New Images

## 📋 Checklist

### Before You Start:
- [ ] Have your 3 images ready
- [ ] Rename them to descriptive names (e.g., `pottery-bowl.jpg`)
- [ ] Place them in the main folder (not a subfolder)

---

## 🚀 3-Minute Workflow

### Step 1: Place Images
Copy your 3 images to:
```
c:\Users\h0100\OneDrive - Massachusetts Institute of Technology\Documents\GitHub\Hhigginb.github.io\
```

### Step 2: Convert Images
**Double-click:** `CONVERT_SPECIFIC_IMAGES.bat`

When prompted, enter each filename:
```
Enter filename (or 'done'): your-image-1.jpg
  ✅ Added: your-image-1.jpg
Enter filename (or 'done'): your-image-2.jpg
  ✅ Added: your-image-2.jpg
Enter filename (or 'done'): your-image-3.png
  ✅ Added: your-image-3.png
Enter filename (or 'done'): done
```

Type `y` to confirm and convert!

### Step 3: Add to HTML
Copy this template and customize:

**For gallery thumbnails (hand.html, heart.html):**
```html
<div class="w3-col l3 m6 w3-margin-bottom">
  <img src="responsive_images/thumb/YOUR-IMAGE.webp" 
       srcset="responsive_images/thumb/YOUR-IMAGE.webp 300w,
               responsive_images/small/YOUR-IMAGE.webp 640w"
       sizes="(max-width: 640px) 50vw, 25vw"
       alt="YOUR DESCRIPTION" 
       style="width:100%" 
       onclick="document.getElementById('modal-YOUR-ID').style.display='block'" 
       class="w3-hover-opacity" 
       loading="lazy">
</div>
```

**For modal/lightbox:**
```html
<div id="modal-YOUR-ID" class="w3-modal" onclick="this.style.display='none'">
  <span class="w3-button w3-hover-red w3-xlarge w3-display-topright">&times;</span>
  <div class="w3-modal-content w3-animate-zoom">
    <img src="responsive_images/full/YOUR-IMAGE.webp" 
         style="width:100%"
         loading="lazy">
  </div>
</div>
```

**Replace:**
- `YOUR-IMAGE` → your filename without extension (e.g., `pottery-bowl`)
- `YOUR DESCRIPTION` → descriptive alt text
- `YOUR-ID` → unique modal ID (e.g., `pottery`)

### Step 4: Test
- Open HTML in browser
- Verify images appear correctly
- Try clicking them (modal should open)
- Resize window to test responsive loading

---

## 📝 Full Example

### Your image: `hiking-2025.jpg`

**Gallery thumbnail:**
```html
<div class="w3-col l3 m6 w3-margin-bottom">
  <img src="responsive_images/thumb/hiking-2025.webp" 
       srcset="responsive_images/thumb/hiking-2025.webp 300w,
               responsive_images/small/hiking-2025.webp 640w"
       sizes="(max-width: 640px) 50vw, 25vw"
       alt="Hiking Mt. Washington 2025" 
       style="width:100%" 
       onclick="document.getElementById('modal-hiking2025').style.display='block'" 
       class="w3-hover-opacity" 
       loading="lazy">
</div>
```

**Modal:**
```html
<div id="modal-hiking2025" class="w3-modal" onclick="this.style.display='none'">
  <span class="w3-button w3-hover-red w3-xlarge w3-display-topright">&times;</span>
  <div class="w3-modal-content w3-animate-zoom">
    <img src="responsive_images/full/hiking-2025.webp" 
         style="width:100%"
         loading="lazy">
  </div>
</div>
```

---

## 🎯 Where to Add in HTML

### For Projects/Handiwork:
→ Edit `hand.html`
→ Look for `<!-- Projects Gallery -->` or `<!-- Athletics Gallery -->`

### For Adventures:
→ Edit `heart.html`
→ Look for `<!-- Adventures Gallery -->`

### For Research/Courses:
→ Edit `mind.html`

---

## 💡 Tips

### Image Names
- ✅ `pottery-wheel-2025.jpg`
- ✅ `mt-washington-hike.jpg`
- ❌ `IMG_1234.jpg`
- ❌ `DSC_5678.JPG`

### Alt Text
- ✅ "Pottery bowl on wheel"
- ✅ "Hiking Mt. Washington summit"
- ❌ "Image"
- ❌ "Photo"

### Modal IDs
- ✅ `modal-pottery`
- ✅ `modal-hike2025`
- ❌ `modal-1`
- ❌ `modal`

Make them unique and descriptive!

---

## ⏱️ Time Estimate

- Place images: **30 seconds**
- Run converter: **1 minute**
- Add to HTML: **5 minutes** (1-2 min per image)
- Test: **1 minute**

**Total: ~7-8 minutes for 3 images**

---

## 🆘 Troubleshooting

**"File not found"**
→ Check the image is in the main folder (not a subfolder)

**"Images still rotated"**
→ This shouldn't happen! The script fixes orientation automatically

**"Images not showing in browser"**
→ Check the file paths in your HTML
→ Make sure `responsive_images/` folder exists
→ Verify the webp files were created

**"Modal not opening"**
→ Check modal ID matches between thumbnail and modal div
→ Ensure onclick attribute is correct

---

## ✅ Success Checklist

After adding your images:

- [ ] All 3 images converted (check `responsive_images/thumb/`)
- [ ] HTML updated for all 3 images
- [ ] Images display in browser
- [ ] Modals open when clicked
- [ ] No console errors (F12 → Console tab)
- [ ] Images look correct (not rotated)
- [ ] Responsive loading works (resize window)

---

## 🎉 You're Done!

Your 3 new images are now:
- ✅ Properly oriented (no rotation)
- ✅ Optimized for web (WebP format)
- ✅ Responsive (right size for each device)
- ✅ Fast loading (lazy loaded)

**Commit and push to GitHub Pages to go live!**

---

## 📚 More Help

- **HTML Examples:** `RESPONSIVE_IMAGES_GUIDE.md`
- **Full Process:** `ADD_NEW_IMAGES_GUIDE.md`
- **Complete Guide:** `COMPLETE_GUIDE.md`
