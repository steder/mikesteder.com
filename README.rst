mikesteder.com
-------------------------------------

My "professional" web presence

Ynot
==============================

Ynot is my extremely simple attempt at
a very basic static site generator.  Unlike other
static site generators I really very few assumptions
and place no convention on how you organize your
content.

The only assumption for now that your templates
are in the `templates` directory.

Ynot depends on jinja2

Dependencies
==============================

Building this site depends on the following:

 * python2.7
 * jinja2
 * lessc
 * uglifyjs

Soon I'll be using sphinx and pygments to
update my python tutorials and then I'll also
be dependent on:

 * sphinx
 * pygments

Building
==============================

Everything is static content generated through the included
makefile(s).

The main pages of the site is a simple bootstrap site
and my own little jinja2 template renderer.

The files in templates are rendered using jinja2 and
dropped in the root directory so::

    templates/index.jinja2 -> index.html

This allows stuff like the navigation elements to
be written once in `templates/_base.jinja2` and
be included in all the other files.

Templates prefixed with `_` are skipped by `ynot`.

Usage
=================================

Just run the following commands::

    make

