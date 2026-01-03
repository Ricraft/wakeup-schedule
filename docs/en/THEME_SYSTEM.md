# Theme System Guide

WakeUp Schedule features a modern, customizable theme system.

## Theme Modes

### Light Mode
- Bright, clean interface
- Best for daytime use
- High contrast for readability

### Dark Mode
- Eye-friendly dark interface
- Best for nighttime use
- Reduces eye strain

### Auto Mode
- Follows system theme
- Requires `darkdetect` package
- Seamlessly switches with OS settings

## Header Styles

### Default (Solid)
- Traditional opaque header
- Best for simple backgrounds
- Maximum readability

### Translucent (Frosted Glass)
- 40% opacity white background
- Creates depth and layering
- Modern acrylic effect

### Transparent
- Fully transparent header
- Background image shows through
- Best for beautiful wallpapers

## Customization Options

### Background Image

**Supported Formats:**
- PNG, JPG, JPEG, BMP (static)
- GIF (animated)

**Setting Background:**
1. Go to **Settings > Appearance**
2. Click **Select Background Image**
3. Choose your image
4. Adjust opacity as needed

**Tips:**
- Use high-resolution images for best quality
- Landscape orientation works best
- GIFs add dynamic visual interest

### Background Opacity

Controls how visible the background image is.

| Value | Effect |
|-------|--------|
| 0% | Invisible |
| 50% | Semi-transparent |
| 100% | Fully visible |

**Recommended:** 30-60% for good balance

### Course Card Opacity

Controls transparency of course blocks.

| Value | Effect |
|-------|--------|
| 70% | More transparent, shows background |
| 85% | Balanced (recommended) |
| 100% | Fully opaque |

**Recommended:** 80-95% for readability

## Smart Text Colors

The app automatically adjusts text color based on background:

```
Brightness = 0.299*R + 0.587*G + 0.114*B

If Brightness > 128:
    Use dark text (#333333)
Else:
    Use light text (#FFFFFF)
```

This ensures text is always readable regardless of course color.

## Color Assignment

Courses are automatically assigned colors:
- Same course name = same color
- Colors are consistent across sessions
- 15 preset colors optimized for visibility

### Preset Color Palette

```
#F48FB1  Pink
#CE93D8  Purple
#B39DDB  Deep Purple
#9FA8DA  Indigo
#90CAF9  Blue
#81D4FA  Light Blue
#80DEEA  Cyan
#80CBC4  Teal
#A5D6A7  Green
#C5E1A5  Light Green
#E6EE9C  Lime
#FFF59D  Yellow
#FFE082  Amber
#FFCC80  Orange
#BCAAA4  Brown
```

## Configuration File

Theme settings are stored in `config.json`:

```json
{
    "theme_mode": "auto",
    "header_style": "translucent",
    "background_path": "/path/to/image.jpg",
    "background_opacity": 0.5,
    "course_opacity": 0.85
}
```

## Troubleshooting

### Background not showing
- Check file path is valid
- Ensure image format is supported
- Try increasing opacity

### Text hard to read
- Adjust course opacity higher
- Try different header style
- Choose background with less contrast

### GIF not animating
- Ensure file is valid GIF
- Check file isn't too large
- Try a different GIF

### Auto theme not working
- Install `darkdetect`: `pip install darkdetect`
- Check OS theme settings
- Restart the application

## Best Practices

1. **For productivity**: Use solid header, high opacity
2. **For aesthetics**: Use translucent header, custom background
3. **For eye comfort**: Use dark mode at night
4. **For presentations**: Use light mode, clean background
