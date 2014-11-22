#!/bin/bash
# Mit diesem Skript wird ein Backup einer Odoo Datenbank erstellt
# With this script a backup for your odoo db will create
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
mybackuppath=$mybasepath"/backup"

echo "Basepath: "$mybasepath
echo "Backup path: "$mybackuppath

if [ ! -d $mybackuppath ]; then
  echo "Create a backup folder..."
  mkdir $mybackuppath
fi

echo "For which odoo db you will create the backup:"
read mydb

if [ "$mydb" != "" ]; then
  echo "$mydb backup in progress..."
  now=$(date +"%Y-%m-%d_%H-%M-%S")
  filename="$mydb.$now.gz"
  mybackup=$mybackuppath"/"$filename
  pg_dump $mydb | gzip > $mybackup
  echo "The backup file is named $mybackup ..."
else
  echo "No backup!"
fi

echo "Finished!"
