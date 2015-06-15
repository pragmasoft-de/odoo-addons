#!/bin/bash
# Mit diesem Skript wird ein Restore einer Odoo Datenbank durchgeführt
# Verwenden Sie den Benutzer odoo > sudo su odoo
# With this script you can restore a odoo db on postgresql
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
export PGPASSWORD=odoo2015
mybackuppath="$PWD"
mybasepath="$HOME"

echo "Your home path is: "$mybasepath 
echo "Your backup path is: "$mybackuppath
echo "So your zip file should store there!"

echo "Name of the new db:"
read mydb

echo "Delete the old version of $mydb [Y/n]:"
read mydel

if [ "$mydel" == "Y" ] || [ "$mydel" == "y" ]; then
  dropdb -U odoo $mydb
  echo "Drop is done."
fi

echo "Name of the backupfile (path: $mybackuppath):"
read mybackupzip

if [ "$mydb" != "" ]; then
  echo "Unzip $mybackuppath/$mybackupzip.."
  cd $mybackuppath
  unzip $mybackuppath/$mybackupzip
  mybackup=dump.sql
  echo "Create DB $mydb with $mybackup file.."
  createdb -U odoo -T template0 $mydb
  echo "Restore DB $mydb"
  psql -U odoo -f $mybackuppath/$mybackup -d $mydb -h localhost -p 5432
  filestorepath="$mybasepath/.local/share/Odoo/filestore/$mydb"
  rm -rf $mybasepath/.local/share/Odoo/sessions/
  if [ -d $filestorepath ]; then
    rm -rf $filestorepath
  else
    mkdir -p $filestorepath
  fi
  cp -r $mybackuppath/filestore $filestorepath
  rm $mybackuppath/$mybackup
  rm $mybackuppath/manifest.json
  rm -rf $mybackuppath/filestore
  echo "Do you want to deactivate cronjob functions in $mydb [Y/n]:"
  read mycron
  if [ "$mycron" == "Y" ] || [ "$mycron" == "y" ]; then 
    psql -d $mydb -U odoo -c $'UPDATE ir_cron SET active = FALSE;'
  fi  
  echo "Restore is done."
else
  echo "No restore."
fi

cd $mybasepath
echo "Finished!"
