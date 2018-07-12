import setuptools


with open("README.md", "r") as readme:
    long_description = readme.read()


setuptools.setup(
    name="porfavor",
    version="0.3.0",
    author="osherdp",
    author_email="osherdepaz@gmail.com",
    url="https://github.com/osherdp/porfavor",
    description="Publishing static documentation the easy way",
    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    package_data={"porfavor": ["static/**", "templates/**"]},
    entry_points={
        "console_scripts": [
            "porfavor= porfavor:main",
        ]
    },

    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*",
    install_requires=["flask", "tqdm", "rpyc", "docopt"],

    classifiers=(
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
