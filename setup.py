#!/usr/bin/env python3

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smartrenamer",
    version="0.0.1",
    author="Fabrice Quenneville",
    author_email="fab@fabq.ca",
    url="https://github.com/fabquenneville/smartrenamer",
    download_url="",
    project_urls={
        "Bug Tracker": "https://github.com/fabquenneville/smartrenamer/issues",
        "Documentation": "https://fabquenneville.github.io/smartrenamer/",
        "Source Code": "https://github.com/fabquenneville/smartrenamer",
    },
    description="smartrenamer is a tool used to automatically clean and unify the file names in a file tree.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    entry_points = {
        'console_scripts': [''],
    },
    keywords=[],
    install_requires=[],
    license='GPL-3.0',
    python_requires='>=3.9',
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=True,
)