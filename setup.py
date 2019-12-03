# USAGE NOTES
#
# Make a PyPI release tarball with:
#
#     python setup.py sdist
#
# Upload to test PyPI with:
#
#     twine upload --repository-url https://test.pypi.org/legacy/ dist/*
#
# Install from test PyPI with:
#
#     pip install --index-url https://test.pypi.org/simple/ runviewer
#
# Upload to real PyPI with:
#
#     twine upload dist/*
#
# Build conda packages for all platforms (in a conda environment with setuptools_conda
# installed) with:
#
#     python setup.py dist_conda
#
# Upoad to your own account (for testing) on anaconda cloud (in a conda environment with
# anaconda-client installed) with:
#
#     anaconda upload --skip-existing conda_packages/*/*
#
# (Trickier on Windows, as it won't expand the wildcards)
#
# Upoad to the labscript-suite organisation's channel on anaconda cloud (in a
# conda environment with anaconda-client installed) with:
#
#     anaconda -c labscript-suite upload --skip-existing conda_packages/*/*
#
# If you need to rebuild the same version of the package for conda due to a packaging
# issue, you must increment CONDA_BUILD_NUMBER in order to create a unique version on
# anaconda cloud. When subsequently releasing a new version of the package,
# CONDA_BUILD_NUMBER should be reset to zero.

import os
from setuptools import setup
from runpy import run_path

try:
    from setuptools_conda import dist_conda
except ImportError:
    dist_conda = None

SETUP_REQUIRES = ['setuptools', 'setuptools_scm']

# TODO: add labscript suite deps once they are on PyPI/anaconda cloud
INSTALL_REQUIRES = [
    "pyqtgraph >=0.9.10",
    "numpy >=1.15",
    "scipy",
    "h5py",
    "qtutils >=2.0.0",
    "zprocess",
    # Not available on conda, but we don't build conda packages for Python 2:
    "autocython; sys_version == '2.7'" 
]

setup(
    name='runviewer',
    version=run_path(os.path.join('runviewer', '__version__.py'))['__version__'],
    description="A program to view shots compiled by labscript",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='The labscript suite community',
    author_email='labscriptsuite@googlegroups.com ',
    url='http://labscriptsuite.org',
    license="BSD",
    packages=["runviewer", "runviewer.resample"],
    zip_safe=False,
    setup_requires=SETUP_REQUIRES,
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5",
    install_requires=INSTALL_REQUIRES if 'CONDA_BUILD' not in os.environ else [],
    cmdclass={'dist_conda': dist_conda} if dist_conda is not None else {},
    command_options={
        'dist_conda': {
            'pythons': (__file__, ['3.6', '3.7', '3.8']),
            'platforms': (__file__, ['linux-64', 'win-32', 'win-64', 'osx-64']),
            'force_conversion': (__file__, True),
        },
    },
)
