#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import *
import os
from datetime import datetime
from os.path import exists as os_path_exists
# Set the Fabric environment
env.hosts = ['54.165.14.143', '100.25.162.205']
env.user = 'ubuntu'

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

def do_deploy(archive_path):
    """
        Distribute archive.
    """
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        newest_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(newest_version))
        run("sudo tar -xzf {} -C {}/".format(archived_file,
                                             newest_version))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(newest_version,
                                                newest_version))
        run("sudo rm -rf {}/web_static".format(newest_version))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(newest_version))

        print("New version deployed!")
        return True

    return False
