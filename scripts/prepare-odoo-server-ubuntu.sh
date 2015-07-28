#!/bin/bash
# Mit diesem Skript werden alle Pakete für den Odoo Betrieb unter Ubuntu installiert
# Skript muss mit root-Rechten ausgeführt werden also vorher sudo su eingeben!
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

echo "Prepare Ubuntu"
apt-get update && apt-get dist-upgrade && apt-get autoremove

echo "Tools zip, unzip, mc(Midnight Comander) and htop will be install.."
apt-get install mc zip unzip htop ntp

echo "Do you want install postgresql ? / Wollen Sie die PostgreSQL-DB installieren  (Y/n):"
read mypsql

if [ "$mypsql" = "Y" ]; then
  echo "PostgreSQL will be install..."
  apt-get install postgresql
else
  echo "PostgreSQL is not installed!"
fi

echo "apt-get packages will be install.."
apt-get install ghostscript graphviz antiword git libpq-dev poppler-utils \
 python-pip build-essential libfreetype6-dev npm python-magic

apt-get install python-dateutil python-pypdf python-requests \
 python-feedparser python-gdata python-ldap python-libxslt1 \
 python-lxml python-mako python-openid python-psycopg2 \
 python-pybabel python-pychart python-pydot python-pyparsing \
 python-reportlab python-simplejson python-tz python-vatnumber \
 python-vobject python-webdav python-werkzeug python-xlwt \
 python-yaml python-zsi python-docutils python-psutil \
 python-unittest2 python-mock python-jinja2 python-dev \
 python-pdftools python-decorator python-openssl python-babel \
 python-imaging python-reportlab-accel \
 python-paramiko python-software-properties

echo "pip packages will be install.."
pip install passlib beautifulsoup4 evdev reportlab qrcode polib unidecode validate_email pyDNS pysftp python-slugify

echo "npm packages will be install.."
npm install -g less less-plugin-clean-css
ln -s /usr/bin/nodejs /usr/bin/node

echo "Do you want install barcodes? / Wollen Sie die Barcodes installieren (Y/n):"
read myfonts

if [ "$myfonts" = "Y" ]; then
  echo "Barcodes will be install..."
  wget http://www.reportlab.com/ftp/pfbfer.zip
  unzip pfbfer.zip -d fonts
  mv fonts /usr/lib/python2.7/dist-packages/reportlab/
  rm pfbfer.zip
else
  echo "Barcodes is not installed!"
fi


echo "Do you want install module HTML2PDF? / Wollen Sie das Modul HTML2PDF installieren (Y/n):"
read mypdf

if [ "$mypdf" = "Y" ]; then
  echo "HTML2PDF will be install..."
  wget http://www.openerp24.de/fileadmin/content/dateien/wkhtmltox-0.12.2.1_linux-trusty-amd64.deb
  dpkg -i wkhtmltox-0.12.2.1_linux-trusty-amd64.deb
  rm wkhtmltox-0.12.2.1_linux-trusty-amd64.deb
  apt-get -f install
else
  echo "HTML2PDF is not installed!"
fi

echo "Do you want use the PointOfSale (PoS)? / Wollen Sie Odoo mit Kassenmodul verwenden(Y/n):"
read mypos

if [ "$mypos" = "Y" ]; then
  echo "PoS will be install..."
  sudo pip install pyserial
  sudo pip install --pre pyusb
else
  echo "PoS is not prepared!"
fi

echo "Do you want optimize postgres settings? / Wollen Sie die PostgreSQL-Einstellungen optimieren (Y/n)?:"
read mysql

if [ "$mysql" = "Y" ]; then
  echo "PostgreSQL will be optimized..."
  sudo apt-get install pgtune
  sudo pgtune -i /etc/postgresql/9.3/main/postgresql.conf -o /etc/postgresql/9.3/main/postgresql.conf.tuned
  sudo mv /etc/postgresql/9.3/main/postgresql.conf  /etc/postgresql/9.3/main/postgresql.conf.old
  sudo mv /etc/postgresql/9.3/main/postgresql.conf.tuned  /etc/postgresql/9.3/main/postgresql.conf
  sudo /etc/init.d/postgresql stop
  sudo /etc/init.d/postgresql start 
  sudo cat /etc/postgresql/9.3/main/postgresql.conf
else
  echo "PostgreSQL is not optimized!"
fi

echo "Python Image Library will be install.."
sudo wget http://effbot.org/downloads/Imaging-1.1.7.tar.gz
sudo tar fzvx Imaging-1.1.7.tar.gz
sudo cd Imaging-1.1.7
sudo python setup.py install
sudo cd ..
sudo rm Imaging-1.1.7.tar.gz
sudo rm –rf Imaging-1.1.7
sudo pip install -I pillow

echo "Finished!"
