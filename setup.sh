git clone https://github.com/ATNoG/Raspi-TV.git
echo "Installing dependencies"
apt-get install python-dev python-pip sqlite3 libffi-dev libssl-dev xautomation
pip install -r Raspi-TV/requirements.txt
chown -R pi:pi Raspi-TV
echo "Issue 'sudo raspi-config', select 'Enable Boot to Desktop', and choose 'Desktop Log in as user pi at the GUI'"
echo "Add the following lines to '/etc/xdg/lxsession/LXDE-pi/autostart':"
echo "@xset s off"
echo "@xset -dpms"
echo "@xset s noblank"
echo "@epiphany-browser localhost:8080"
echo "@xte 'sleep 10' 'key F11'"
echo "Now please change directory to Raspi-TV:"
echo "cd Raspi-TV"
echo "Then, issue:"
echo "python setup.py create database"
echo "python setup.py create user"
echo "python setup.py create cronjobs"
