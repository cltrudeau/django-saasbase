# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

import os
import sys

CUR_DIR = os.path.join(os.path.dirname(__file__))
APP_DIR = os.path.abspath(os.path.join(CUR_DIR, 'saasbase'))
sys.path.insert(0, os.path.abspath('..'))
import django
from django.conf import settings
settings.configure(
    BASE_DIR=APP_DIR,
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.admin',

        'awl',

        'saasbase',
    ),
)
django.setup()

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'SaaSBase'
author = 'Christopher Trudeau'
from datetime import datetime
years = '2019'
this_year = '%s' % datetime.now().year
if this_year != years:
    years = '%s-%s' % (years, this_year)
copyright = '%s, %s' % (years, author)

import imp
mod = imp.load_source('saasbase', '../saasbase/__init__.py')
version = mod.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
