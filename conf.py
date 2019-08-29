# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Veeam Best Practise 9.5u4a'
copyright = '2019, Paul Szelesi'
author = 'Paul Szelesi'

# The full version, including alpha/beta/rc tags
release = '1.0.0'


# -- General configuration ---------------------------------------------------
#Change Master doc to look for index not master_doc
master_doc = 'index'


# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []



# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "classic"

#Options for the them
html_theme_options = {
"rightsidebar": False,
# (True): Put the sidebar on the right side. Defaults to False.
"stickysidebar": True,
#(true or false): Make the sidebar “fixed” so that it doesn’t scroll out of view for long body content. This may not work well with all browsers. Defaults to False.
"collapsiblesidebar": True,
#(true or false): Add an experimental JavaScript snippet that makes the sidebar collapsible via a button on its side. Defaults to False.
"externalrefs": True,
#(true or false): Display external links differently from internal links. Defaults to False.
"footerbgcolor": 'white',
# (CSS color): Background color for the footer line.
"footertextcolor ": 'darkslategrey',
#(CSS color): Text color for the footer line.
"sidebarbgcolor": 'white',
# (CSS color): Background color for the sidebar.
"sidebarbtncolor": 'darkslategrey',
#(CSS color): Background color for the sidebar collapse button (used when collapsiblesidebar is True).
"sidebartextcolor": 'darkgreen',
#(CSS color): Text color for the sidebar.
"sidebarlinkcolor":'green',
#(CSS color): Link color for the sidebar.
"relbarbgcolor": 'darkslategrey',
#(CSS color): Background color for the relation bar.
"relbartextcolor": 'white',
#(CSS color): Text color for the relation bar.
"relbarlinkcolor": 'white',
#(CSS color): Link color for the relation bar.
"bgcolor": 'white',
#(CSS color): Body background color.
"textcolor": 'black',
#(CSS color): Body text color.
"linkcolor": 'darkgreen',
#(CSS color): Body link color.
"visitedlinkcolor": 'darkgreen',
#(CSS color): Body color for visited links.
"headbgcolor": 'white',
# (CSS color): Background color for headings.
#headtextcolor (CSS color): Text color for headings.
#headlinkcolor (CSS color): Link color for headings.
#codebgcolor (CSS color): Background color for code blocks.
#codetextcolor (CSS color): Default text color for code blocks, if not set differently by the highlighting style.
#bodyfont (CSS font-family): Font for normal text.
#headfont (CSS font-family): Font for headings.
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
