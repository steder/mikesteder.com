#!/usr/bin/env python
# nosy: commandline continuous integration for test driven development
#
# Copyright (C) 2008 Michael Steder <steder@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Nosy - Script to monitor changes to *.py files and rerun tests

NOTE: Credit for the idea goes to Jeff Wrinkler.  Today there are other versions of
this on PyPI (one called nosy and another called nosyd) but I didn't like the
config file required in both cases.

What makes this version different, and better IMHO, is that Nosy simply
acts as a passthrough to the underlying commandline test runner. You
don't have to learn how to use a new test tool and create a config file
you just replace the normal commandline with nosy and get on with your life.

So if you normally run nosetests like this::

  $ nosetests --nocapture --with-coverage --cover-package=<mypackage> mypackage

You can simply run nosy instead of nosetests like this to have your tests
rerun whenever the code changes::

  $ nosy --nocapture --with-coverage --cover-package=<mypackage> mypackage

Nosy currenly walks the working directory for *.py
files and only re-runs when *.py files change.

TODO:
 - integrate building documentation
 - run syntax checker (pyflakes / pylint)
 - rename and publish on pypi?
"""


__version__ = 1.0

import fnmatch
import os
import subprocess
import stat
import sys
import time


TEST_RUNNER = "bin/ynot"
PATTERNS = ["*.jinja2",]


def checksum_directory(directory):
    """
    Walk directory structure and return simple checksum based on
    file size and modified time.

    """
    file_checksums = []
    for dirpath, dirnames, filenames in os.walk(directory,
                                                topdown=False,
                                                onerror=None,
                                                followlinks=False):
        source_names = [name for pattern in PATTERNS
                        for name in filenames if fnmatch.fnmatch(name, pattern)]
        for source_name in source_names:
            source_path = os.path.join(dirpath, source_name)
            try:
                stats = os.stat(source_path)
            except OSError:
                # ignore temp files and files we don't
                # have perms to access
                continue
            file_checksums.append(
                stats[stat.ST_SIZE] + stats[stat.ST_MTIME])
    return sum(file_checksums)


def main():
    args = " ".join(sys.argv[1:])
    command = "%s %s"%(TEST_RUNNER, args)

    latest_checksum = checksum_directory(os.curdir)
    print "Nosy starting with: %s"%(command)
    print command
    subprocess.call(command.split())
    try:
        while (True):
            checksum = checksum_directory(os.curdir)
            if checksum != latest_checksum:
                print "Nosy detected a change and is rerunning tests with: %s"%(command)
                latest_checksum = checksum
                subprocess.call(command.split())
            time.sleep(1)
    except KeyboardInterrupt:
        print "Exiting Nosy..."


if __name__=="__main__":
    main()
