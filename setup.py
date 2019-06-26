import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="listids",
    version="0.0.1",
    python_requires='>=3.6',
    author="Thomas Lemberger",
    author_email="thomas.lemberger@embo.org",
    description="Extract pmid - doi mapping for a given journal using EuropePMC.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/source-data/pmidoi",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests"
    ],
    entry_points = {
        'console_scripts': [
            'listids=src.cli:listids',
            'about=src.cli:about',
        ],
    },
    # keywords="",
    classifiers=(
        # full list: https://pypi.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.6",
        "License :: Other/Proprietary License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries",
    ),
)
