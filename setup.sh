sudo apt-get -y update
sudo apt-get remove --purge node
sudo apt-get install -y build-essential zlib1g-dev git-core gnupg2 libpq-dev nodejs npm postgresql python-pip python-dev libffi-dev curl nodejs-legacy
npm set registry http://registry.npmjs.org
sudo npm install -g n
sudo n 0.12.7
npm set registry https://registry.npmjs.org
sudo npm install -g bower
sudo pip install -r requirements/dev.txt
bower install
