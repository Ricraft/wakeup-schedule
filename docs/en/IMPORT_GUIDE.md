# Import Guide

This guide covers all methods to import your course schedule into WakeUp Schedule.

## Overview

WakeUp Schedule supports multiple import methods:

| Method | Best For | Difficulty |
|--------|----------|------------|
| WebView | Supported universities | ⭐ Easy |
| HTML | Any university | ⭐⭐ Medium |
| Excel | Custom schedules | ⭐⭐ Medium |
| Text | Quick entry | ⭐⭐⭐ Advanced |

---

## WebView Import (Recommended)

The easiest way to import - login directly in the app.

### Supported Systems

- **QiangZhi System** (强智教务系统)
- **ZhengFang System** (正方教务系统)
- Other compatible systems

### Steps

1. Click **📥 Import > Import from Portal (WebView)**
2. Select your university from dropdown, or enter custom URL
3. Login with your student credentials
4. Navigate to your schedule page
5. Click **📥 Get Schedule**
6. Review and confirm imported courses

### Tips

- Make sure you're on the schedule page (not the main portal)
- Select "All Weeks" view if available
- If import fails, try refreshing the page first

---

## HTML Import

Import from saved HTML files.

### Steps

1. Open your university portal in a browser
2. Navigate to schedule page
3. Save page: **Ctrl+S** → Select "Webpage, Complete"
4. In WakeUp Schedule: **📥 Import > HTML Import**
5. Select the saved `.html` file

### Supported Formats

- QiangZhi system HTML exports
- ZhengFang system HTML exports
- Generic table-based schedules

### Troubleshooting

**"Cannot parse schedule"**
- Try saving as "Webpage, HTML Only"
- Check if the page contains the actual schedule table

**Wrong day mapping**
- Some systems start with Sunday, others with Monday
- The importer auto-detects this, but may need manual adjustment

---

## Excel Import

Import from spreadsheet files.

### Supported Formats

- `.xlsx` (Excel 2007+)
- `.xls` (Excel 97-2003)

### Expected Format

| | Monday | Tuesday | Wednesday | ... |
|---|--------|---------|-----------|-----|
| 1-2 | Math<br>Room 101<br>Week 1-16 | | English<br>Room 202<br>Week 1-16 | |
| 3-4 | | Physics<br>Room 303<br>Week 1-8 | | |

### Creating a Template

```bash
python scripts/create_excel_template.py
```

This creates `examples/schedule_template.xlsx` you can fill in.

### Cell Format

Each cell should contain:
```
Course Name
Location (optional)
Week Range (e.g., 1-16, 1-8(odd))
```

---

## Text Import

Import from plain text files.

### Format

```
周一 1-2节 高等数学 张教授 A101 1-16周
周二 3-4节 英语 李老师 B202 1-16周
周三 5-6节 物理 王教授 C303 1-8周(单)
```

### Format Explanation

```
[Day] [Periods] [Course Name] [Teacher] [Location] [Weeks]
```

- **Day**: 周一/周二/周三/周四/周五/周六/周日
- **Periods**: X-Y节 (e.g., 1-2节, 3-4节)
- **Weeks**: X-Y周 or X-Y周(单) for odd weeks, X-Y周(双) for even weeks

---

## After Import

### Review Courses

After importing, review the schedule view to ensure:
- All courses are imported
- Days and times are correct
- Week ranges are accurate

### Edit if Needed

Click any course card to edit:
- Course name
- Teacher
- Location
- Time slot
- Week range

### Handle Conflicts

If conflicts are detected:
1. A warning dialog appears
2. Review conflicting courses
3. Choose to keep, modify, or remove

---

## Common Issues

### No courses imported

- Check if the source file contains schedule data
- Try a different import method
- Ensure the file encoding is UTF-8

### Wrong week numbers

- Verify semester start date in Settings
- Check if source uses different week numbering

### Missing courses

- Some systems split courses across multiple pages
- Try importing from "All Weeks" view

### Garbled text

- File encoding issue
- Re-save source file as UTF-8

---

## Need Help?

- Check [Troubleshooting Guide](../USC_TROUBLESHOOTING.md)
- Open an [Issue](https://github.com/Ricraft/wakeup-schedule/issues)
- See [Add New School Guide](ADD_NEW_SCHOOL_GUIDE.md) for unsupported systems
