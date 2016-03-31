sudo apt-get -y update
sudo apt-get remove --purge node
sudo apt-get install -y build-essential zlib1g-dev git-core gnupg2 libpq-dev nodejs nodejs npm postgresql python-pip
sudo ln -s /usr/bin/nodejs /usr/bin/node
sudo npm install -g bower
pip install -r requirements/dev.txt
bower install
