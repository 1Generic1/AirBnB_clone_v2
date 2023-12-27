#!/usr/bin/env bash
# this script sets up your web servers for the deployment of web_static

sudo apt-get update
sudo apt-get -y install nginx

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo touch /data/web_static/releases/test/index.html
echo "<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    <p>Nginx server test</p>
  </body>
</html>" | tee /data/web_static/releases/test/index.html
# Create symbolic link
sudo rm -f /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current
# Give ownership to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/
# Update Nginx configuration
nginx_config="/etc/nginx/sites-available/default"
sudo sed -i '39 i\ \tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n' $nginx_config
sudo service nginx restart
