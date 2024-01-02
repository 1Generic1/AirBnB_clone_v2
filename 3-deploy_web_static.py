#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import env, put, run, local
import os
from datetime import datetime
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
    Distributes an archive to web servers and deploys it.
    """
    if not os.path.exists(archive_path):
        print(f"Error: Archive file '{archive_path}' does not exist.")
        return 1

    try:
        # Extract relevant information from the archive path
        archive_name = os.path.basename(archive_path)
        version_name = os.path.splitext(archive_name)[0]

        # Define paths
        tmp_path = '/tmp/{}'.format(archive_name)
        release_path = '/data/web_static/releases/{}'.format(version_name)
        current_link = '/data/web_static/current'

        # Upload archive to temporary location
        put(archive_path, tmp_path)

        # Create a directory for the new version
        run('sudo mkdir -p {}'.format(release_path))

        # Extract the contents of the archive
        run('sudo tar -xzf {} -C {}'.format
            (tmp_path, release_path))

        # Clean up temporary archive
        run('sudo rm {}'.format(tmp_path))

        # Move contents to the version directory
        run('sudo mv -n  {}/web_static/* {}'.format
            (release_path, release_path))

        # Remove unnecessary directory
        run('sudo rm -rf {}/web_static'.format(release_path))

        # Update symbolic link to the new version
        run('sudo rm -rf {}'.format(current_link))
        run('sudo ln -s {} {}'.format(release_path, current_link))

        print("New version deployed!")
        return 0
    except Exception as e:
        print(f"Error during deployment: {e}")
        return 1


def deploy():
    """
    Creates and distributes an archive to web servers.
    """

    # Call do_pack function and store the path of the created archive
    archive_path = do_pack()
    if not archive_path:
        return 1
    try:
        return do_deploy(archive_path)
    except Exception as e:
        print(f"Error during deployment: {e}")
        return 0
