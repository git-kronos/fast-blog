sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv
sudo apt install -y postgresql postgresql-contrib
#sudo cat /etc/passwd
su - postgres
#psql -U postgres
#\password postgres
#\q
git clone git@gitlab.com:git-kronos/fastapi.git
cd fastapi
python3 -m venv venv
source venv/bin/activate

pip install -U pip
pip install -r requirements.txt

make run

#possible library
#sudo apt install libpq-dev
