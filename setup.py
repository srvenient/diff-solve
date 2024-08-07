import os
import re

import setuptools

# for simplicity, we actually store the version in the __version__ attribute in the source
here = os.path.realpath(os.path.dirname(__file__))
with open(os.path.join(here, 'app', '__init__.py')) as f:
    meta_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if meta_match:
        version = meta_match.group(1)
    else:
        raise RuntimeError("Unable to find __version__ string.")

with open(os.path.join(here, 'README.md')) as f:
    readme = f.read()

setuptools.setup(
    name='Diff Solve',
    version=version,
    author='Nelson Rodriguez Roa',
    author_email="nrodriguezr2006@gmail.com",
    description='Differential equations solver',
    long_description=readme,
    url='https://github.com/srvenient/differential-equations',
    packages=setuptools.find_packages('app'),
    install_requires=[
        'sympy >= 1.13.1',
        'flask >= 3.0.3',
        'matplotlib >= 3.9.1',
    ],
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ]
)