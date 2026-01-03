# Contributing Guide

Thank you for your interest in contributing to WakeUp Schedule!

## Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🏫 Add support for your university
- 💻 Submit code improvements

## Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/wakeup-schedule.git
cd wakeup-schedule
```

### 2. Set Up Development Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
pip install pytest pytest-cov  # Dev dependencies
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

## Code Guidelines

### Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and small

### Example

```python
def calculate_week(start_date: date, current_date: date) -> int:
    """
    Calculate the current week number.
    
    Args:
        start_date: Semester start date
        current_date: Date to calculate week for
        
    Returns:
        Week number (1-based)
    """
    delta = (current_date - start_date).days
    return (delta // 7) + 1
```

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add Excel import support
fix: correct week calculation for odd weeks
docs: update installation guide
refactor: simplify conflict detection logic
test: add tests for HTML importer
```

## Testing

### Run Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_models.py

# With coverage
pytest --cov=src --cov-report=html
```

### Write Tests

- Add tests for new features
- Ensure existing tests pass
- Aim for good coverage of edge cases

```python
def test_week_calculation():
    from datetime import date
    from src.core.week_calculator import WeekCalculator
    
    calc = WeekCalculator(date(2025, 9, 1))
    
    # Week 1
    assert calc.get_week_for_date(date(2025, 9, 1)) == 1
    assert calc.get_week_for_date(date(2025, 9, 7)) == 1
    
    # Week 2
    assert calc.get_week_for_date(date(2025, 9, 8)) == 2
```

## Submitting Changes

### 1. Push Your Branch

```bash
git push origin feature/your-feature-name
```

### 2. Create Pull Request

1. Go to the repository on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill in the PR template

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactoring

## Testing
- [ ] Tests pass locally
- [ ] New tests added (if applicable)

## Screenshots (if UI changes)
```

## Reporting Issues

### Bug Reports

Include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- System info (OS, Python version)

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternatives considered

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn

## Questions?

- Open a [Discussion](https://github.com/Ricraft/wakeup-schedule/discussions)
- Check existing [Issues](https://github.com/Ricraft/wakeup-schedule/issues)

Thank you for contributing! 🎉
