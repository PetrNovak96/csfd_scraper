# Automatically created by: shub deploy
# python3 setup.py bdist_egg
# setup.py se samo nevytvoří

from setuptools import setup, find_packages

setup(
    name         = 'csfd_scraper',
    version      = '1',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = csfd_scraper.settings']},
)
