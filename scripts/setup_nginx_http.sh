# ****************************************
# Enable HTTP, HTTPS and ssh
# ****************************************

# Adjusting the firewall
sudo ufw app list
# Allow port 80 and 22
sudo ufw allow 'Nginx HTTP'
sudo ufw allow 'Nginx HTTPS'
sudo ufw allow 'OpenSSH'
sudo ufw enable
sudo ufw status
# If there are other processes using the ports 80/443 they can be killed using:
# sudo fuser -k 80/tcp
# sudo fuser -k 443/tcp
sudo service nginx restart

# To display your public IP
curl -4 icanhazip.com

# Go to your browser and enter:
# http://your_server_ip
# Make sure that it is not redirected to https

# Setting up server blocks
# replace api.zopfind.com with the domain name

# ****************************************
# Setting up a server block
# ****************************************

domain='api.rdiff.ridiv.in' # enter domain name without www. prefix
application_port='http://0.0.0.0:8000'
sudo mkdir -p /var/www/$domain/html
sudo chown -R $USER:$USER /var/www/$domain/html
sudo chmod -R 755 /var/www/$domain
touch /var/www/$domain/html/index.html
echo """
<html>
    <head>
        <title>Welcome to Your Domain</title>
    </head>
    <body>
        <h1>Success.  The Your Domain server block is working</h1>
    </body>
</html>""" >> /var/www/$domain/html/index.html

sudo touch /etc/nginx/sites-available/$domain

echo """server {
    listen 80;
    listen [::]:80;
    root /var/www/$domain/html;
    index index.html index.htm index.nginx-debian.html;
    server_name $domain www.$domain;
    location / {
        proxy_pass $application_port;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$http_host;
        proxy_redirect off;
        uwsgi_pass_header HTTP_AUTHORIZATION;
        uwsgi_pass_request_headers on;
    }
}""" | sudo tee /etc/nginx/sites-available/$domain


# enable the file by creating a link from it to the sites-enabled directory, which Nginx reads from during startup:
sudo ln -s /etc/nginx/sites-available/$domain /etc/nginx/sites-enabled/

# this needs to be done manually
# sudo vim /etc/nginx/nginx.conf
# Uncomment the line
# http {
#     ...
#     server_names_hash_bucket_size 64;
#     ...
# }

sudo nginx -t
sudo systemctl restart nginx

# For uninstalling nginx
# sudo apt-get purge nginx nginx-common
# sudo apt-get autoremove

# for routing the static files through nginx, it is required to give the user www-data
# access to the folder where the static files are located.
# To check if the www-data user has access to the static folder, run the following command
# sudo -u www-data stat ~/zopfind-backend/backend/static/
# If it gives a permission denied error, add the www-data user to the current user group
# sudo gpasswd -a www-data ubuntu
# and then restart nginx
# sudo nginx -t
# sudo systemctl restart nginx
