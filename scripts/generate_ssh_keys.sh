# Set up ssh keys for accessing the git repo using ssh
ssh-keygen -f /home/ubuntu/.ssh/id_ed25519 -t ed25519
# leave the passphrase empty
# This generates a public/private key pair and store it at the specified path.

cat ~/.ssh/id_ed25519.pub
# This will show the public key
# copy and paste this in the access key of the repository
# use the ssh url of the repository
