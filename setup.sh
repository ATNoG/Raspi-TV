#!/usr/bin/env bash


# This file should fully setup Raspi-TV on a new Raspberry.
# For more information visit https://github.com/ATNoG/Raspi-TV.git

# Clone Raspi-TV repository
git clone https://github.com/ATNoG/Raspi-TV.git

# Installing distribution dependencies
echo "Installing dependencies (this requires root privileges)"
apt-get install "$(grep -vE "^\s*#" dependencies.txt | tr "\n" " ")"

# Set pi as the owner of Raspi-TV and cd to this directory
chown -R pi:pi Raspi-TV
pushd Raspi-TV/

# Add reboot job as root
echo "Adding root cronjobs"
(crontab -l; echo "@reboot 0 0 * * * /sbin/reboot")| crontab -          # Reboot at midnight

# Change user (don't need root for now)
sudo -u pi bash << EOF

# Adding cronjobs
echo "Adding pi cronjobs"
(crontab -l; echo "@reboot python $(pwd)/app/app.py &")| crontab -      # At every reboot start the server
(crontab -l; echo "@reboot $(pwd)/fullscreen.sh")| crontab -            # At every reboot start epiphany (web browser)
(crontab -l; echo "* * * * * python $(pwd)/app/cron.py")| crontab -     # Update Tweets + Dropbox files every minute

# Installing Python dependencies
echo "Installing Python requirements to user pi"
pip install -r app/requirements.txt

# Create database + user
echo "Creating database"
python setup.py create database
echo "Creating user"
python setup.py create user

EOF
popd

echo "Cleaning up and scheduling a reboot in 1 minute"
echo "If you've got unsaved work execute (as root):"
echo "killall shutdown"
shutdown -r +1
rm -- "$0"
