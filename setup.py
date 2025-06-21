"""
Setup script для SEO-анализа конкурентов
"""
from setuptools import setup, find_packages
import os

# Чтение README
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Чтение requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="seo-analysis-kyrgyzstan",
    version="1.0.0",
    author="SEO Analysis Team",
    author_email="team@example.com",
    description="Комплексная программа для парсинга SEO-данных конкурентов в Кыргызстане",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/seo-analysis-project",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Marketing",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "selenium": [
            "selenium>=4.0.0",
            "webdriver-manager>=3.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "seo-analyzer=seo_analyzer:main",
            "seo-scheduler=scheduler:run_scheduler",
            "seo-dashboard=dashboard:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.yaml"],
    },
    keywords="seo, parsing, competitors, kyrgyzstan, google, yandex, analysis",
    project_urls={
        "Bug Reports": "https://github.com/your-username/seo-analysis-project/issues",
        "Source": "https://github.com/your-username/seo-analysis-project",
        "Documentation": "https://github.com/your-username/seo-analysis-project/blob/main/README.md",
    },
) 