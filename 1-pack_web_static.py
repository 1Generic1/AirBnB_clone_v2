#!/usr/bin/python3
"""Generates a .tgz archive from the contents of the web_static folder."""
from fabric.api import *
from datetime import datetime
import os


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    local('sudo mkdir -p versions')
    t = datetime.now()
    t_str = t.strftime('%Y%m%d%H%M%S')
    local("sudo tar -cvzf versions/web_static_{}.tgz web_static".format(t_str))

    f_path = "versions/web_static_{}.tgz".format(t_str)
    f_size = os.path.getsize(f_path)
    print(f"web_static packed: {f_path} -> {f_size}Bytes")
    return f_path
