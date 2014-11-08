#!/bin/bash
# Mit diesem Skript installiert Odoo unter /opt/odoo und bindet es in den Autostart ein
# Skript muss mit root-Rechten ausgeführt werden
##############################################################################
#
#    Shell Script for Odoo, Open Source Management Solution
#    Copyright (C) 2014-now Equitania Software GmbH(<http://www.equitania.de>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

mybasepath="/opt/odoo"
mysourcepath=$mybasepath"/odoo"
myserverpath=$mybasepath"/odoo-server"

echo "Basepath: "$mybasepath
echo "Sourcepath: "$mysourcepath
echo "Serverpath: "$myserverpath

echo "Prepare PostgreSQL"

sudo adduser odoo --home /opt/odoo
sudo -u postgres createuser -s odoo

echo "Geben Sie das Passwort für den User odoo innerhalb der PostgreSQL an:"
read myodoopwd

if [ "$myodoopwd" != "" ]; then
  echo "PostgreSQL Passwort odoo wird gesetzt..."
  sudo -u postgres psql -c "ALTER USER odoo WITH PASSWORD '$myodoopwd';"
fi

echo "Geben Sie das Passwort für den User postgres innerhalb der PostgreSQL an:"
read mypsqlpwd

if [ "$mypsqlpwd" != "" ]; then
  echo "PostgreSQL Passwort postgres wird gesetzt..."
  sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD '$mypsqlpwd';"
fi

cd $mybasepath
git clone -b 8.0 --single-branch https://github.com/equitania/odoo.git
echo "Clone lastest branch odoo.."
mkdir $myserverpath
echo "Create odoo-server"

cp -r $mysourcepath/addons $myserverpath
echo "Copy addons..."
cp -r $mysourcepath/debian $myserverpath
echo "Copy debian..."
cp -r $mysourcepath/doc $myserverpath
echo "Copy doc..."
cp -r $mysourcepath/openerp $myserverpath
echo "Copy openerp..."
cp -r $mysourcepath/setup $myserverpath
echo "Copy setup..."
cp  $mysourcepath/odoo.py $myserverpath
echo "Copy files..."
cp  $mysourcepath/openerp-gevent $myserverpath
cp  $mysourcepath/openerp-server $myserverpath
cp  $mysourcepath/openerp-wsgi.py $myserverpath
cp  $mysourcepath/setup.py $myserverpath
cp  $mysourcepath/setup.cfg $myserverpath

echo "Geben Sie das Passwort für den Databasemanager ein:"
read myadminpwd

old="'admin_passwd': 'admin'"
new="'admin_passwd': '$myadminpwd'"

cp  $myserverpath/openerp/tools/config.py $mybasepath/config.py
sed -i "s/$old/$new/g" $mybasepath/config.py
cp  $mybasepath/config.py $myserverpath/openerp/tools

sudo chown -R odoo:odoo $myserverpath 
sudo chown -R odoo:odoo $mysourcepath 
sudo chown -R odoo:odoo $mybasepath 

sudo cp $mysourcepath/debian/openerp-server.conf /etc/odoo-server.conf
sudo chown odoo:odoo /etc/odoo-server.conf
sudo chmod 640 /etc/odoo-server.conf
sudo mkdir /var/log/odoo
sudo chown odoo:root /var/log/odoo
sudo cp $mysourcepath/debian/logrotate /etc/logrotate.d/odoo-server
chmod 755 /etc/logrotate.d/odoo-server
sudo cp $mysourcepath/debian/openerp.init.d /etc/init.d/openerp-server
sudo chmod +x /etc/init.d/openerp-server
sudo update-rc.d openerp-server defaults

echo "Finished!"
