"""
WakeUp 课表 Windows 版 - 安装配置
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wakeup-schedule",
    version="1.0.0",
    author="WakeUp Schedule Team",
    description="轻量级、美观的课程表管理应用程序",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YZune/WakeupSchedule_Kotlin",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.10",
    install_requires=[
        "PyQt6>=6.6.0",
        "PyQt6-WebEngine>=6.6.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "openpyxl>=3.1.0",
        "python-dateutil>=2.8.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "hypothesis>=6.92.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "wakeup-schedule=main:main",
        ],
    },
)
