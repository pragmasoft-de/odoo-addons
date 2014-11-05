#!/bin/bash
# Mit diesem Skript wird ein Restore einer Odoo Datenbank durchgeführt
# With this script you can restore a odoo db on postgresql

mybasepath="/opt/odoo"
mybackuppath=$mybasepath"/backup"

echo "Basepath: "$mybasepath
echo "Backup path: "$mybackuppath


echo "Name of the new db:"
read mydb

echo "Name of the backupfile without .gz an (path: $mybackuppath):"
read mybackup

if [ "$mydb" != "" ]; then
  gunzip $mybackuppath/$mybackup".gz"
  createdb -U odoo -T template0 $mydb
  psql -f $mybackuppath/$mybackup -d $mydb -h localhost -p 5432
  echo "Restore is done."
else
  echo "No restore."
fi

echo "Finished!"
