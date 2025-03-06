#!/bin/bash
# Create the EC2 instance with the following scripts in the user data.
# It will do the following operations:
# 1. Install Git
# 2. Install Docker
# 3. Enable and start docker service
# 4. Add ubuntu user to docker group
# 5. Install docker-compose
# 6. Install nginx

# 1. Install Git    *********** #
sudo apt-get install git -y

# 2. Install Docker*********** #

# Uninstall older version if installed
sudo apt-get remove docker docker-engine docker.io containerd runc

# Set up the docker repository
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

#Install docker engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y

# 3. Enable the docker service *********** #
# so that it can start automatically
sudo systemctl enable docker.service
sudo systemctl start docker.service

# 4. Add Ubuntu user to Docker group *********** #
# Adds ubuntu user to the docker group so it has access to run Docker containers.
sudo usermod -aG docker ubuntu

# 5. Install docker-compose *********** #
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
# Make docker-compose binary executable
sudo chmod +x /usr/local/bin/docker-compose

# 5.1. Sign Out *********** #
# so that the user group permissions are applied to the current user
# This step is required if the user scripts are not being used.
# exit


# 6. Install Nginx *********** #
sudo apt-get update
sudo apt-get install -y nginx


# ssh into the instance and
# sudo vim /var/log/cloud-init-output.log
# to see the log of startup scripts
