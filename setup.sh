git clone https://github.com/ATNoG/Raspi-TV.git
pip install -r Raspi-TV/requirements.txt
chown -R pi:pi Raspi-TV 
echo "Please change directory to Raspi-TV:"
echo "cd Raspi-TV"
echo "Then, issue:"
echo "python setup.py create database"
echo "python setup.py create user"
echo "python setup.py create cronjobs"

