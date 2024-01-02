# AirBnB_clone_v2

## prepare web servers 
## 0-setup_web_static.sh
	Write a Bash script that sets up your web servers for the deployment of web_static. It must:

	Install Nginx if it not already installed
	Create the folder /data/ if it doesn’t already exist
	Create the folder /data/web_static/ if it doesn’t already exist
	Create the folder /data/web_static/releases/ if it doesn’t already exist
	Create the folder /data/web_static/shared/ if it doesn’t already exist
	Create the folder /data/web_static/releases/test/ if it doesn’t already exist
	Create a fake HTML file /data/web_static/releases/test/index.html (with simple content, to test your Nginx configuration)
	Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder. If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
	Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and group exist). This should be recursive; everything inside should be created/owned by this user/group.
	Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static (ex: https://mydomainname.tech/hbnb_static). Don’t forget to restart Nginx after updating the configuration:
	Use alias inside your Nginx configuration
	Tip
	Your program should always exit successfully. Don’t forget to run your script on both of your web servers.

	In optional, you will redo this task but by using Puppet

## 1-pack_web_static.py

Write a Fabric script that generates a .tgz archive from the contents of the web_static folder of your AirBnB Clone repo, using the function do_pack.

Prototype: def do_pack():
All files in the folder web_static must be added to the final archive
All archives must be stored in the folder versions (your function should create this folder if it doesn’t exist)
The name of the archive created must be web_static_<year><month><day><hour><minute><second>.tgz
The function do_pack must return the arc

	guillaume@ubuntu:~/AirBnB_clone_v2$ fab -f 1-pack_web_static.py do_pack 
	Packing web_static to versions/web_static_20170314233357.tgz

## 2-do_deploy_web_static.py
Write a Fabric script (based on the file 1-pack_web_static.py) that distributes an archive to your web servers, using the function do_deploy:

Prototype: def do_deploy(archive_path):
Returns False if the file at the path archive_path doesn’t exist
The script should take the following steps:
Upload the archive to the /tmp/ directory of the web server
Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension> on the web server
Delete the archive from the web server
Delete the symbolic link /data/web_static/current from the web server
Create a new the symbolic link /data/web_static/current on the web server, linked to the new version of your code (/data/web_static/releases/<archive filename without extension>)
All remote commands must be executed on your both web servers (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
Returns True if all operations have been done correctly, otherwise returns False
You must use this script to deploy it on your servers: xx-web-01 and xx-web-02
In the following example, the SSH key and the username used for accessing to the server are passed in the command line. Of course, you could define them as Fabric environment variables (ex: env.user =...)

Disclaimer: commands execute by Fabric displayed below are linked to the way we implemented the archive function do_pack - like the mv command - depending of your implementation of it, you may don’t need it

	fab -f 2-do_deploy_web_static.py do_deploy:archive_path=versions/web_static_20170315003959.tgz -i my_ssh_private_key -u ubuntu

## 3-deploy_web_static.py
Write a Fabric script (based on the file 2-do_deploy_web_static.py) that creates and distributes an archive to your web servers, using the function deploy:

Prototype: def deploy():
The script should take the following steps:
Call the do_pack() function and store the path of the created archive
Return False if no archive has been created
Call the do_deploy(archive_path) function, using the new path of the new archive
Return the return value of do_deploy
All remote commands must be executed on both of web your servers (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
You must use this script to deploy it on your servers: xx-web-01 and xx-web-02
In the following example, the SSH key and the username used for accessing to the server are passed in the command line. Of course, you could define them as Fabric environment variables (ex: env.user =…)
	guillaume@ubuntu:~/AirBnB_clone_v2$ fab -f 3-deploy_web_static.py deploy -i my_ssh_private_key -u ubuntu

## 100-clean_web_static.py

Write a Fabric script (based on the file 3-deploy_web_static.py) that deletes out-of-date archives, using the function do_clean:

Prototype: def do_clean(number=0):
number is the number of the archives, including the most recent, to keep.
If number is 0 or 1, keep only the most recent version of your archive.
if number is 2, keep the most recent, and second most recent versions of your archive.
etc.
Your script should:
Delete all unnecessary archives (all archives minus the number to keep) in the versions folder
Delete all unnecessary archives (all archives minus the number to keep) in the /data/web_static/releases folder of both of your web servers
All remote commands must be executed on both of your web servers (using the env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
In the following example, the SSH key and the username used for accessing to the server are passed in the command line. Of course, you could define them as Fabric environment variables (ex: env.user =…)

	guillaume@ubuntu:~/AirBnB_clone_v2$ ls -ltr versions
	-rw-r--r-- 1 vagrant vagrant 27280335 Mar 15  2017 web_static_20170315015414.tgz
	-rw-r--r-- 1 vagrant vagrant 27280335 Mar 15  2017 web_static_20170315015448.tgz
	-rw-r--r-- 1 vagrant vagrant 27280335 Mar 15  2017 web_static_20170315015507.tgz
	-rw-r--r-- 1 vagrant vagrant 27280335 Mar 15  2017 web_static_20170315015620.tgz
	guillaume@ubuntu:~/AirBnB_clone_v2$ fab -f 100-clean_web_static.py do_clean:number=2 -i my_ssh_private_key -u ubuntu > /dev/null 2>&1
	guillaume@ubuntu:~/AirBnB_clone_v2$ ls -ltr versions
	-rw-r--r-- 1 vagrant vagrant 27280335 Mar 15  2017 web_static_20170315015507.tgz
	-rw-r--r-- 1 vagrant vagrant 27280335 Mar 15  2017 web_static_20170315015620.tgz
	guillaume@ubuntu:~/AirBnB_clone_v2$

## 101-setup_web_static.pp

Redo the task #0 but by using Puppet: 
