# Quick Start Guide

Get WakeUp Schedule running in 5 minutes!

## Installation

### Option 1: Download Release (Recommended)

1. Go to [Releases](https://github.com/Ricraft/wakeup-schedule/releases)
2. Download `WakeUpSchedule_v2.5.0.zip`
3. Extract and run `WakeUpSchedule.exe`

### Option 2: Run from Source

```bash
# Clone repository
git clone https://github.com/Ricraft/wakeup-schedule.git
cd wakeup-schedule

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

## First Steps

### 1. Set Semester Start Date

1. Click **⚙️ Settings**
2. Go to **Semester Settings**
3. Select your semester start date
4. Click **Save**

### 2. Import Your Schedule

#### Method A: WebView Import (Easiest)

1. Click **📥 Import > Import from Portal**
2. Select your university from the dropdown
3. Login to your portal
4. Navigate to schedule page
5. Click **📥 Get Schedule**

#### Method B: HTML Import

1. Save your schedule page as HTML from browser
2. Click **📥 Import > HTML Import**
3. Select the saved file

#### Method C: Manual Entry

1. Click **➕ Add Course**
2. Fill in course details
3. Click **Save**

### 3. Customize Appearance

1. Click **🎨 Appearance** or **⚙️ Settings**
2. Choose a background image
3. Adjust transparency
4. Select theme mode

## Tips

- **Navigate weeks**: Use ◀ ▶ buttons or click week display
- **Edit course**: Click on any course card
- **Quick add**: Click on empty cell to add course at that time
- **Conflict detection**: App warns you about schedule conflicts

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Add Course | Ctrl+N |
| Save | Ctrl+S |
| Settings | Ctrl+, |
| Refresh | F5 |

## Troubleshooting

### App won't start
- Ensure Python 3.10+ is installed
- Check all dependencies are installed

### Import fails
- Try saving HTML with "Complete webpage" option
- Check if your university uses a supported system

### Display issues
- Try switching theme mode
- Reset background settings

## Next Steps

- Read the full [User Guide](IMPORT_GUIDE.md)
- Check [Theme System](THEME_SYSTEM.md) for customization
- See [Add New School](ADD_NEW_SCHOOL_GUIDE.md) to add your university
