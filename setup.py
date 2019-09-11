from setuptools import setup, find_packages
import re

version = re.search(
    r'^__version__\s*=\s*"(.*)"',
    open('arachnid/arachnid.py').read(),
    re.M
    ).group(1)

with open("README.md", "r") as f:
    long_desc = f.read()


setup(
    name="arachnid-spider",
    packages=find_packages(exclude="test"),
    entry_points={
        "console_scripts": ["arachnid = arachnid.__main__:main"]
    },
    include_package_data=True,
    install_requires=[
        'requests',
        'beautifulsoup4',
        'tldextract',
        'ndg-httpsclient',
        'pyopenssl',
        'chardet',
        'pyasn1'
    ],
    version=version,
    python_requires=">=3.7",
    description="An OSINT tool to find data leaks on a targeted domain",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="Jacob Bickle, Tobin Shields",
    author_email="bickle.jake@gmail.com, tobin.shields@mhcc.edu",
    url="https://github.com/jake-bickle/Arachnid",
    license="GPLv3",
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 4 - Beta"
    ]
)
