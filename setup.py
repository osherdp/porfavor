"""Define packaging-related data for deploying porfavor."""
from __future__ import absolute_import

import setuptools

__version__ = "0.5.0"

setuptools.setup(
    name="porfavor",
    version=__version__,
    author="osherdp",
    author_email="osherdepaz@gmail.com",
    url="https://github.com/osherdp/porfavor",
    description="Publishing static documentation the easy way",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",

    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    package_data={"porfavor": ["static/*",
                               "static/img/*",
                               "static/fonts/*",
                               "templates/*"]},
    entry_points={
        "console_scripts": [
            "porfavor=porfavor:main",
        ]
    },

    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*",
    install_requires=["flask",
                      "click",
                      "requests",
                      "requests_toolbelt"],
    extras_require={
        "dev": ["flake8",
                "pylint"]
    },

    classifiers=(
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
