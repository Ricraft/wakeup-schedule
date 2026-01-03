# 🎓 WakeUp Schedule - Windows Desktop Edition

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

A modern, feature-rich desktop course schedule management application for university students.  
Built with Python and PyQt6, featuring multiple import methods, smart conflict detection, and a beautiful UI.

[Features](#-features) • [Quick Start](#-quick-start) • [User Guide](#-user-guide) • [Development](#-development)

</div>

---

## ✨ Features

### 🎨 Modern UI Design

- **Frosted Glass Effect**: Translucent headers with 40% opacity for depth
- **Smart Text Colors**: Auto-adjusts text color based on background brightness
- **Rounded Corners**: 8px border-radius for a modern look
- **Theme System**: Light/Dark/Auto modes
- **Custom Backgrounds**: Support for static images and GIF animations
- **Adjustable Transparency**: Independent control for background and course cards

### 📚 Course Management

- ✅ Add, edit, and delete courses
- ✅ Batch management for multiple time slots
- ✅ Automatic color assignment (same course = same color)
- ✅ Smart conflict detection
- ✅ Week type support (Every/Odd/Even weeks)
- ✅ Auto-save with backup

### 📥 Multiple Import Methods

1. **WebView Import** - Login to your university portal directly in the app
2. **HTML Import** - Import from saved HTML files
3. **Excel Import** - Import from spreadsheet files
4. **Text Import** - Simple text format support

### ⚙️ Flexible Settings

- Semester start date configuration
- Custom time slots for each class period
- Appearance customization
- System tray support
- Course reminders

---

## 🚀 Quick Start

### Requirements

- Windows 10/11
- Python 3.10+
- 2GB RAM
- 100MB disk space

### Installation

```bash
# Clone the repository
git clone https://github.com/Ricraft/wakeup-schedule.git
cd wakeup-schedule

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Dependencies

- PyQt6 >= 6.6.0
- PyQt6-WebEngine >= 6.6.0
- beautifulsoup4 >= 4.12.0
- lxml >= 4.9.0
- openpyxl >= 3.1.0
- python-dateutil >= 2.8.0
- darkdetect >= 0.8.0

---

## 📖 User Guide

### Adding Courses

1. Click **➕ Add Course** in the toolbar
2. Fill in course details:
   - Course name (required)
   - Teacher name
   - Location
   - Day of week
   - Class periods
   - Week range
   - Week type (Every/Odd/Even)
3. Click **Save**

### Importing from University Portal

1. Click **Import > Import from Portal (WebView)**
2. Select your university or enter custom URL
3. Login to your portal
4. Navigate to the schedule page
5. Click **📥 Get Schedule**

### Customizing Appearance

1. Click **⚙️ Settings > Appearance**
2. Choose header style (Default/Translucent/Transparent)
3. Set background image
4. Adjust opacity sliders
5. Click **OK** to apply

---

## 🏗️ Project Structure

```
wakeup-schedule/
├── src/
│   ├── models/          # Data models
│   ├── core/            # Business logic
│   ├── ui/              # User interface
│   ├── storage/         # Data persistence
│   ├── importers/       # Import modules
│   └── utils/           # Utilities
├── tests/               # Test files
├── docs/                # Documentation
├── resources/           # Icons and assets
├── main.py              # Entry point
└── requirements.txt     # Dependencies
```

---

## 🛠️ Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

### Building Executable

```bash
pyinstaller build.spec
```

The executable will be created in the `dist/` folder.

---

## 🤖 AI-Assisted Development

This project was developed with AI assistance (Kiro/Claude) for:
- Code writing and optimization
- Documentation
- Test generation
- Bug fixing

All AI-generated code has been reviewed and tested.

---

## 🙏 Acknowledgments

- [WakeUp Schedule Kotlin](https://github.com/YZune/WakeupSchedule_Kotlin) for design inspiration and schedule parsing logic
- PyQt6 team for the excellent GUI framework
- Open source community

---

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details.

---

## 🤝 Contributing

Contributions are welcome! Please see [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
