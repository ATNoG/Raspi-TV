git clone https://github.com/ATNoG/Raspi-TV.git
echo "Installing dependencies"
apt-get install python-dev python-pip sqlite3 chromium
pip install -r Raspi-TV/requirements.txt
chown -R pi:pi Raspi-TV
echo "Add the following line to '/etc/xdg/lxsession/LXDE-pi/autostart':"
echo "/usr/bin/chromium --kiosk --ignore-certificate-errors --disable-restore-session-state \"http://localhost:8080/\""
echo "Please change directory to Raspi-TV:"
echo "cd Raspi-TV"
echo "Then, issue:"
echo "python setup.py create database"
echo "python setup.py create user"
echo "python setup.py create cronjobs"

