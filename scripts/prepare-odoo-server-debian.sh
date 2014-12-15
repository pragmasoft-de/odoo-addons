#!/bin/bash
# Mit diesem Skript werden alle Pakete für den Odoo Betrieb unter Ubuntu installiert
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

echo "Prepare Debian/Ubuntu"
apt-get update && apt-get dist-upgrade && apt-get autoremove

echo "Tools zip, unzip, mc(Midnight Comander) and htop will be install.."
apt-get install mc zip unzip htop

echo "Do you want install postgresql ? / Wollen Sie die PostgreSQL-DB installieren  (Y/n):"
read mypsql

if [ "$mypsql" = "Y" ]; then
  echo "PostgreSQL will be install..."
  sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
  apt-get install wget ca-certificates
  wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
  apt-get update
  apt-get upgrade
  apt-get install postgresql-9.3 pgadmin3
else
  echo "PostgreSQL is not installed!"
fi

apt-get install ghostscript graphviz antiword git libpq-dev poppler-utils \
 python-pip build-essential libfreetype6-dev 

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

pip install passlib beautifulsoup4 evdev reportlab qrcode

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
  wget http://downloads.sourceforge.net/project/wkhtmltopdf/0.12.1/wkhtmltox-0.12.1_linux-wheezy-amd64.deb
  dpkg -i wkhtmltox-0.12.1_linux-wheezy-amd64.deb
  rm wkhtmltox-0.12.1_linux-wheezy-amd64.deb
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
  apt-get install pgtune
  pgtune -i /etc/postgresql/9.3/main/postgresql.conf -o /etc/postgresql/9.3/main/postgresql.conf.tuned
  mv /etc/postgresql/9.3/main/postgresql.conf  /etc/postgresql/9.3/main/postgresql.conf.old
  mv /etc/postgresql/9.3/main/postgresql.conf.tuned  /etc/postgresql/9.3/main/postgresql.conf
  /etc/init.d/postgresql stop
  /etc/init.d/postgresql start 
  cat /etc/postgresql/9.3/main/postgresql.conf
else
  echo "PostgreSQL is not optimized!"
fi



echo "Finished!"
