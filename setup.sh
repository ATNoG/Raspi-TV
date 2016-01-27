#!/usr/bin/env bash


# This file should fully setup Raspi-TV on a new Raspberry.
# For more information visit https://github.com/ATNoG/Raspi-TV.git

echo "If you haven't done it yet don't forget to run raspi-config and update/upgrade your distribution"
echo "Continuing in 10 seconds..."
sleep 10s

# Cloning Raspi-TV repository
echo "Cloning Raspi-TV repository"
git clone https://github.com/ATNoG/Raspi-TV.git

# Set pi as the owner of Raspi-TV and cd to this directory
chown -R pi:pi Raspi-TV
pushd Raspi-TV/

# Installing distribution dependencies
echo "Installing dependencies (this requires root privileges)"
apt-get -y install $(cat dependencies.txt | grep -v "^#")

# Installing Python dependencies
echo "Installing Python requirements to user pi"
pip install -r app/requirements.txt

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

# Create database + user
echo "Please create a new database:"
echo "python setup.py create database"
echo "And then add a new admin user:"
echo "python setup.py create user"

EOF
popd

echo "Rebooting in 1 minute"
echo "If you've got unsaved work either save it or execute (as root):"
echo "killall shutdown"
shutdown -r +1
