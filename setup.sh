#!/usr/bin/env bash


# This file should fully setup Raspi-TV on a new Raspberry.
# For more information visit https://github.com/ATNoG/Raspi-TV.git

echo "If you haven't done it yet don't forget to run raspi-config and update/upgrade"
echo "your distribution."
echo "If you encounter any problems during this setup please look at 'setup.log'."
echo -n "Continuing in 10 seconds... "
sleep 10s
echo "Done."

# Cloning Raspi-TV repository
echo -n "Cloning Raspi-TV repository... "
git clone https://github.com/ATNoG/Raspi-TV.git &> setup.log
echo "Done."

# Set pi as the owner of Raspi-TV and cd to this directory
chown -R pi:pi Raspi-TV
pushd Raspi-TV/

# Installing distribution dependencies
echo -n "Installing dependencies... "
apt-get -y install $(cat dependencies.txt | grep -v "^#") &>> setup.log
echo "Done."

# Installing Python dependencies
echo -n "Installing Python requirements... "
pip install -r app/requirements.txt &>> setup.log
echo "Done."

# Add reboot job as root
echo "Adding root cronjobs."
(crontab -l; echo "@reboot 0 0 * * * /sbin/reboot")| crontab -          # Reboot at midnight

# Stop the screen from going blank + hide the mouse
echo "Configuring other settings."z
sed '/\[SeatDefaults\]/a xserver-command=X -s 0 -dpms' -i.old /etc/lightdm/lightdm.conf
sed '/@xscreensaver -no-splash/d' -i.old /etc/xdg/lxsession/LXDE/autostart
echo "@unclutter -idle 0.1 -root" >> /etc/xdg/lxsession/LXDE-pi/autostart

# Change user (don't need root for now)
sudo -u pi bash << EOF

# Adding cronjobs
echo "Adding pi cronjobs."
(crontab -l; echo "@reboot python $(pwd)/app/app.py &")| crontab -      # At every reboot start the server
(crontab -l; echo "@reboot $(pwd)/fullscreen.sh &")| crontab -          # At every reboot start epiphany (web browser)
(crontab -l; echo "* * * * * python $(pwd)/app/cron.py &")| crontab -   # Update Tweets + Dropbox files every minute

EOF
popd

# Create database + user
echo "Please change directory to $(pwd)/Raspi-TV and:"
echo "Create a new database"
echo "  python setup.py create database"
echo "Add a new admin user"
echo "  python setup.py create user"

echo "Reboot after you've done the above."
