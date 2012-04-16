#!/usr/bin/env python

#    Copyright (C) 2006  Andrew Straw  <strawman@astraw.com>
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.
#

import os, stat, errno, sys
import fuse
from fuse import Fuse
import requests

if not hasattr(fuse, '__version__'):
    raise RuntimeError, \
        "your fuse-py doesn't know of fuse.__version__, probably it's too old."

fuse.fuse_python_api = (0, 2)

output = open("hello.log", "w")
sys.stdout = output
sys.stderr = output

def get_content(path):
    if path == '/':
        return ""
    else:
        path = path[1:] # strip the leading slash
        return requests.get("http://%s" % path).content

class MyStat(fuse.Stat):
    def __init__(self):
        print "MyState.__init__"
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0

class HelloFS(Fuse):

    def getattr(self, path):
        print "getattr"
        content = get_content(path)
        st = MyStat()
        if path == '/':
            st.st_mode = stat.S_IFDIR | 0755
            st.st_nlink = 2
        else:
            st.st_mode = stat.S_IFREG | 0444
            st.st_nlink = 1
            st.st_size = len(content)
        return st

    def readdir(self, path, offset):
        print "readdir"
        for r in  '.', '..', 'google':
            yield fuse.Direntry(r)

    def open(self, path, flags):
        print "open"
        pass
    
    def read(self, path, size, offset):
        print "read"
        content = get_content(path)
        slen = len(content)
        if offset < slen:
            if offset + size > slen:
                size = slen - offset
            buf = content[offset:offset+size]
        else:
            buf = ''
        return buf
        
def main():
    usage="""
Userspace hello example

""" + Fuse.fusage
    server = HelloFS(version="%prog " + fuse.__version__,
                     usage=usage,
                     dash_s_do='setsingle')

    server.parse(errex=1)
    server.main()

if __name__ == '__main__':
    main()
