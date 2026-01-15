# 🎨 Creating App Icons

## Quick Icon Creation

You need two PNG images for your PWA:
- `static/icon-192.png` (192x192 pixels)
- `static/icon-512.png` (512x512 pixels)

## Option 1: Online Icon Generators (Easiest)

### 1. **Favicon.io** (Recommended)
- Visit: https://favicon.io/favicon-generator/
- Choose "Text" option
- Enter: "🏭" or "IM" (Injection Moulding)
- Select colors (use #667eea for purple theme)
- Download and rename to icon-192.png and icon-512.png

### 2. **Canva** (Professional)
- Visit: https://www.canva.com
- Create 512x512 design
- Add factory icon 🏭 or company logo
- Use gradient background (#667eea to #764ba2)
- Download as PNG
- Resize to 192x192 for smaller version

### 3. **PWA Builder**
- Visit: https://www.pwabuilder.com/imageGenerator
- Upload any image
- Generates all required sizes automatically

## Option 2: Use Emoji as Icon

Create a simple HTML file and screenshot it:

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            width: 512px;
            height: 512px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .icon {
            font-size: 300px;
        }
    </style>
</head>
<body>
    <div class="icon">🏭</div>
</body>
</html>
```

Save as icon.html, open in browser, screenshot at 512x512.

## Option 3: Use Image Editor

### GIMP (Free):
1. Create new image: 512x512
2. Fill with gradient (#667eea to #764ba2)
3. Add text "IM" or factory icon
4. Export as PNG
5. Resize to 192x192 for smaller version

### Photoshop:
1. New document: 512x512
2. Add gradient background
3. Add icon/text
4. Save as PNG
5. Resize for 192x192 version

## Quick Placeholder Icons

For testing, you can use these emoji-based icons:

**Factory Icon**: 🏭
**Gear Icon**: ⚙️
**Tools Icon**: 🔧
**Chart Icon**: 📊

## Icon Design Tips

1. **Keep it simple** - Icons are small on home screen
2. **Use brand colors** - Match your app theme (#667eea)
3. **High contrast** - Ensure visibility on all backgrounds
4. **No text** (or minimal) - Hard to read at small sizes
5. **Square format** - Will be cropped to circle on some devices
6. **Test on device** - Check how it looks on actual phone

## Recommended Icon Content

For your injection moulding app:
- Factory building 🏭
- Injection mould machine
- Gear/cog ⚙️
- Company logo
- Letters "IM" (Injection Moulding)

## File Placement

Once created, place files here:
```
static/
  ├── icon-192.png
  ├── icon-512.png
  ├── manifest.json
  └── service-worker.js
```

## Testing Icons

After adding icons:
1. Restart Django server
2. Open app in Chrome
3. Check DevTools → Application → Manifest
4. Verify icons load correctly
5. Test "Add to Home Screen"

## Icon Checklist

- [ ] Created 192x192 PNG
- [ ] Created 512x512 PNG
- [ ] Placed in static/ folder
- [ ] Updated manifest.json (already done)
- [ ] Tested in browser
- [ ] Tested installation on Android
- [ ] Icon appears on home screen
- [ ] Icon looks good at small size
