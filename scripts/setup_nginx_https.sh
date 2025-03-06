# ****************************************
# Setting up a server block
# ****************************************

domain='api.docusensa.com' # enter domain name without www. prefix
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
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
    }
}""" | sudo tee /etc/nginx/sites-available/$domain
# To redirect http requests to https add the following at the end of location / block
# return 301 $domain$request_uri;

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

# ****************************************
# Using Let's Encrypt to obtain an SSL Certificate
# ****************************************

# 1. Installing Certbot and its nginx plugin
sudo apt install certbot python3-certbot-nginx -y

sudo ufw allow 'Nginx Full'
sudo ufw delete allow 'Nginx HTTP'

sudo ufw status
sudo certbot --nginx -d $domain -d 'www.'$domain

# Verifying Certbot Auto-Renewal
sudo systemctl status certbot.timer

# test the renewal process
sudo certbot renew --dry-run
# There should be no errors.