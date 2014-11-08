#!/bin/bash
# Mit diesem Skript wird ein startklarer Odoo-Server zusammen gestellt
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
myadpath=$mybasepath"/odoo-addons"
mybackuppath=$mybasepath"/backup"

echo "Basepath: "$mybasepath
echo "Sourcepath: "$mysourcepath
echo "Serverpath: "$myserverpath
echo "Equitania addons path: "$myadpath
echo "Backup path: "$mybackuppath


cd $mybasepath
# Alte Installation entfernen
if [ -d $myserverpath ]; then
  rm -rf $myserverpath
  echo "Remove old server files.."
fi

if [ ! -d $mybackuppath ]; then
  echo "Backup-Ordner anlegen"
  mkdir $mybackuppath
fi

echo "Geben Sie eine Datenbank an, die Sie  mit -u all aktualisieren wollen:"
read mydb

if [ "$mydb" != "" ]; then
  echo "$mydb wird jetzt gesichert..."
  now=$(date +"%Y-%m-%d-%S.%N")
  filename="$mydb.$now.gz"
  mybackup=$mybackuppath"/"$filename
  pg_dump $mydb | gzip > $mybackup
  echo "Backup liegt unter der Bezeichnung $mybackup zu finden..."
else
  echo "Es werden keine Backups durchgeführt!"
fi

mkdir $myserverpath
echo "Create odoo-server"

if [ -d $mysourcepath ]; then
  cd $mysourcepath
  git pull https://github.com/equitania/odoo.git
  echo "Pull lastest branch odoo.."
else
  cd $mybasepath
  git clone -b 8.0 --single-branch https://github.com/equitania/odoo.git
  echo "Clone lastest branch odoo.."
fi

if [ -d $myadpath ]; then
  cd $myadpath
  git pull https://github.com/equitania/odoo-addons.git
  echo "Pull lastest branch odoo-addons.."
else
  cd $mybasepath
  git clone -b master --single-branch https://github.com/equitania/odoo-addons.git
  echo "Clone lastest branch odoo-addons.."
fi


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

if [ $mybasepath/config.py ]; then
  echo "Replace config.py"
  cp  $mybasepath/config.py $myserverpath/openerp/tools
fi
if [ $mybasepath/favicon.ico ]; then
  echo "Replace favicon.ico"
  cp  $mybasepath/favicon.ico $myserverpath/addons/web/static/src/img/
fi

echo "Copy equitania addons"
cp -r $myadpath/eq_no_ad $myserverpath/addons
cp -r $myadpath/equitania $myserverpath/addons
cp -r $myadpath/eq_mail_extension $myserverpath/addons

if [ "$mydb" != "" ]; then
  echo "$mydb wird jetzt aktualisiert..."
  echo "Wechsele Pfad.."
  cd $myserverpath
  ./openerp-server -u all -d $mydb
else
  echo "Es werden keine Aktualisierungen durchgeführt!"
fi


echo "Finished!"
