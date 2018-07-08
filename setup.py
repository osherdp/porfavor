import setuptools


with open("README.md", "r") as readme:
    long_description = readme.read()


setuptools.setup(
    name="porfavor",
    version="0.0.1",
    author="osherdp",
    author_email="osherdepaz@gmail.com",
    url="https://github.com/osherdp/porfavor",

    description="Publishing static documentation the easy way",
    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "porfavor= porfavor:main",
        ]
    },
    install_requires=["flask", "tqdm", "rpyc", "docopt"],
    package_data={'': ['*.html', '*.css', '*.js']},

    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
