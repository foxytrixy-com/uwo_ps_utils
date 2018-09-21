import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uwo_ps_utils",
    version="0.2",
    author="Azza",
    author_email="ommokazza@gmail.com",
    description="Common utility modules to help UWO Price Share Aide",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ommokazza/uwo_ps_utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Windows",
    ],
)
