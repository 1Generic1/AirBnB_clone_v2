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
    Distributes an archive to web servers and deploys it
    """
    if not os_path_exists(archive_path):
        return False
    
    try:
        archive_name = archive_path.split('/')[-1]
        tmp_path = '/tmp/{}'.format(archive_name)
        put(archive_path, tmp_path, mode=0o644)
        release_path = '/data/web_static/releases/{}'.format(archive_name.split('.')[0])
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf {} -C {}'.format(tmp_path, release_path))
        run('rm {}'.format(tmp_path))
        current_link = '/data/web_static/current'
        run('rm -f {}'.format(current_link))
        run('ln -s {} {}'.format(release_path, current_link))
        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False
