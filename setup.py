import setuptools
with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "tmartial",
    version = "0.0.1",
    author = "tmartial",
    author_email = "thomas.martial@insa-lyon.fr",
    description = "Module addition",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/tmartial/Projet_SD",
    packages=setuptools.find_packages(),
    classifiers =[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)