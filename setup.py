# Path: facebook-scraper-python/setup.py

"""Setup configuration for Facebook Scraper SDK."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read version from __version__.py
version = {}
with open("facebook_scraper_sdk/__version__.py") as f:
    exec(f.read(), version)

setup(
    name="facebook-scraper-sdk",
    version=version['__version__'],
    author=version['__author__'],
    author_email=version['__author_email__'],
    description=version['__description__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=version['__url__'],
    project_urls={
        "Bug Tracker": "https://github.com/OussemaFr/facebook-scraper-api-python/issues",
        "Documentation": "https://github.com/OussemaFr/facebook-scraper-api-python#readme",
        "Source Code": "https://github.com/OussemaFr/facebook-scraper-api-python",
        "Changelog": "https://github.com/OussemaFr/facebook-scraper-api-python/blob/main/CHANGELOG.md",
        "RapidAPI": "https://rapidapi.com/oussemaf/api/facebook-scraper-api4",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0,<3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "isort>=5.11.0",
            "mypy>=0.990",
            "twine>=4.0.0",
            "build>=0.10.0",
        ],
    },
    keywords=[
        "facebook",
        "scraper",
        "api",
        "sdk",
        "social-media",
        "data-extraction",
        "rapidapi",
        "facebook-api",
        "facebook-scraper",
        "web-scraping",
    ],
    include_package_data=True,
    zip_safe=False,
)