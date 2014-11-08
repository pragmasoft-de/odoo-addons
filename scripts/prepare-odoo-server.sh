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

echo "Prepare Ubuntu"
apt-get update && apt-get dist-upgrade && apt-get autoremove

echo "Tools zip, unzip, mc(Midnight Comander) und htop werden installiert..."
apt-get install mc zip unzip htop

echo "Wollen Sie die PostgreSQL-DB installieren (j/n):"
read mypsql

if [ "$mypsql" = "j" ]; then
  echo "PostgreSQL wird installiert..."
  apt-get install postgresql
else
  echo "PostgreSQL wird nicht installiert!"
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

pip install passlib beautifulsoup4 evdev reportlab

echo "Wollen Sie die Barcodes installieren (j/n):"
read myfonts

if [ "$myfonts" = "j" ]; then
  echo "Barcodes werden installiert..."
  wget http://www.reportlab.com/ftp/pfbfer.zip
  unzip pfbfer.zip -d fonts
  mv fonts /usr/lib/python2.7/dist-packages/reportlab/
  rm pfbfer.zip
else
  echo "Barcodes werden nicht installiert!"
fi


echo "Wollen Sie das Modul HTML2PDF installieren (j/n):"
read mypdf

if [ "$mypdf" = "j" ]; then
  echo "HTML2PDF wird installiert..."
  wget http://downloads.sourceforge.net/project/wkhtmltopdf/0.12.1/wkhtmltox-0.12.1_linux-trusty-amd64.deb
  dpkg -i wkhtmltox-0.12.1_linux-trusty-amd64.deb
  rm wkhtmltox-0.12.1_linux-trusty-amd64.deb
else
  echo "HTML2PDF wird nicht installiert!"
fi

echo "Wollen Sie die PostgreSQL-Einstellungen optimieren (j/n):"
read mysql

if [ "$mysql" = "j" ]; then
  echo "PostgreSQL wird optimiert..."
  apt-get install pgtune
  sudo pgtune -i /etc/postgresql/9.3/main/postgresql.conf -o /etc/postgresql/9.3/main/postgresql.conf.tuned
  sudo mv /etc/postgresql/9.3/main/postgresql.conf  /etc/postgresql/9.3/main/postgresql.conf.old
  sudo mv /etc/postgresql/9.3/main/postgresql.conf.tuned  /etc/postgresql/9.3/main/postgresql.conf
  sudo /etc/init.d/postgresql stop
  sudo /etc/init.d/postgresql start 
  sudo cat /etc/postgresql/9.3/main/postgresql.conf
else
  echo "PostgreSQL wird nicht optimiert!"
fi



echo "Finished!"
