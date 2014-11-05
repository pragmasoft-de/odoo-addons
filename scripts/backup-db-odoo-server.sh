#!/bin/bash
# Mit diesem Skript wird ein Backup einer Odoo Datenbank erstellt
# With this script a backup for your odoo db will create

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
  now=$(date +"%Y-%m-%d-%S.%N")
  filename="$mydb.$now.gz"
  mybackup=$mybackuppath"/"$filename
  pg_dump $mydb | gzip > $mybackup
  echo "The backup file is named $mybackup ..."
else
  echo "No backup!"
fi

echo "Finished!"
