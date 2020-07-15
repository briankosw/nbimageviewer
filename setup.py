from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="nbimageviewer",
    version="0.1.0",
    description="nbimageviewer is a Python library for rapid and efficient image visualization for Jupyter Notebooks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Brian Ko",
    author_email="briankosw@gmail.com",
    url="https://github.com/briankosw/nbimageviewer",
    download_url="https://github.com/briankosw/nbimageviewer/archive/0.1.0.tar.gz",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="jupyter, notebook, visualization, images",
    install_requires=["Pillow", "numpy", "IPython", "tornado"],
    license="MIT",
)
