# Adding New School Support

This guide explains how to add support for your university's academic portal.

## Overview

WakeUp Schedule uses a modular importer architecture. If your school uses the QiangZhi system, you can usually add support with minimal configuration.

## Method 1: Configure QiangZhi Parameters

If your school uses QiangZhi system (URL typically contains `/jsxsd/`), you can extend `QiangZhiImporter`.

### Steps

1. Create a new file in `src/importers/`, e.g., `your_school_importer.py`

2. Inherit from `QiangZhiImporter`:

```python
from .qiangzhi_importer import QiangZhiImporter

class YourSchoolImporter(QiangZhiImporter):
    def __init__(self):
        super().__init__(
            school_name="Your University",
            sunday_first=False,       # Does schedule start with Sunday?
            first_col_is_header=True  # Is first column a header (period numbers)?
        )
    
    def get_importer_name(self) -> str:
        return "Your University Portal"
```

3. Register in `src/importers/html_importer.py`

### Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `sunday_first` | Schedule starts with Sunday column | `False` |
| `first_col_is_header` | First column contains period numbers | `False` |
| `table_id` | HTML ID of schedule table | `kbtable` |
| `cell_class` | CSS class of course cells | `kbcontent` |
| `week_pattern` | Regex for week range | `r'([\d\-,]+)\(周\)'` |
| `section_pattern` | Regex for class periods | `r'\[(\d+)-(\d+)节\]'` |

## Method 2: Create Custom Importer

For non-QiangZhi systems, create a custom importer.

### Steps

1. Inherit from `BaseImporter`:

```python
from typing import List, Tuple
from .base_importer import BaseImporter
from ..models.course_base import CourseBase
from ..models.course_detail import CourseDetail
from ..utils.color_manager import ColorManager

class CustomImporter(BaseImporter):
    
    def __init__(self):
        self.color_manager = ColorManager()
    
    def get_supported_formats(self) -> List[str]:
        return ['.html', '.htm']
    
    def get_importer_name(self) -> str:
        return "Custom University Portal"
    
    def validate(self, content: str) -> Tuple[bool, str]:
        """
        Validate if content is from this system.
        
        Returns:
            (True, "") if valid
            (False, "error message") if invalid
        """
        # Check for unique identifiers in the HTML
        if "unique_identifier" in content:
            return True, ""
        return False, "Not a valid schedule page"
    
    def parse(self, content: str) -> Tuple[List[CourseBase], List[CourseDetail]]:
        """
        Parse schedule content.
        
        Returns:
            (list of CourseBase, list of CourseDetail)
        """
        bases = []
        details = []
        
        # Your parsing logic here
        # 1. Parse HTML with BeautifulSoup
        # 2. Extract course information
        # 3. Create CourseBase and CourseDetail objects
        
        return bases, details
```

2. Implement `validate()` to detect your system's HTML

3. Implement `parse()` to extract course data

### Data Models

**CourseBase** - Basic course info:
```python
CourseBase(
    name="Calculus",
    course_id="unique-id",
    color="#4CAF50",
    note=""
)
```

**CourseDetail** - Schedule details:
```python
CourseDetail(
    course_id="unique-id",
    teacher="Prof. Smith",
    location="Room 101",
    day_of_week=1,      # 1=Monday, 7=Sunday
    start_section=1,    # Starting period
    step=2,             # Duration in periods
    start_week=1,
    end_week=16,
    week_type=WeekType.EVERY_WEEK
)
```

## Testing Your Importer

1. Save a schedule page from your portal as HTML

2. Create test file `tests/test_your_school_importer.py`:

```python
import pytest
from src.importers.your_school_importer import YourSchoolImporter

def test_basic_parse():
    importer = YourSchoolImporter()
    
    with open('tests/fixtures/your_school_sample.html', 'r') as f:
        content = f.read()
    
    valid, msg = importer.validate(content)
    assert valid, f"Validation failed: {msg}"
    
    bases, details = importer.parse(content)
    assert len(bases) > 0, "No courses parsed"
    assert len(details) > 0, "No course details parsed"
```

3. Run tests:
```bash
pytest tests/test_your_school_importer.py -v
```

## Adding to WebView Dialog

To add your school to the WebView dropdown:

1. Open `src/ui/webview_import_dialog.py`

2. Add to `COMMON_URLS` dictionary:
```python
COMMON_URLS = {
    "Your University": "https://jwxt.your-university.edu.cn/",
    # ... other schools
}
```

## Contributing

1. Fork the repository
2. Create branch: `git checkout -b feature/add-your-school`
3. Add your importer and tests
4. Submit a Pull Request

### PR Checklist

- [ ] Importer class created
- [ ] Tests pass
- [ ] No personal data in test fixtures
- [ ] Documentation updated

We welcome contributions for more universities!
