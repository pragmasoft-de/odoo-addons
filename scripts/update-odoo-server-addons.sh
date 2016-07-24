#!/bin/bash
# Mit diesem Skript wird Ihr Odoo-Server geupdated
# Zuvor Dienst als root stoppen mit /etc/init.d/openerp-server stop
# Start als odoo Benutzer
# Debian su odoo / Ubuntu sudo su odoo, danach $ ./update-odoo-server-addons.sh
# Wenn "Computing parent left and right for table ir_ui_menu..." [crtl]+[c] drücken,
# da das Update fertig ist. Danach als root User den Server wieder starten.
# /etc/init.d/odoo-server start
# Version 1.2.4 - Stand 30.03.2016
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
mysourcepath=$mybasepath"/myodoo-server"
myserverpath=$mybasepath"/odoo-server"
myaddpath=$mybasepath"/odoo-addons"
mybackuppath=$mybasepath"/backup"
my3rdpath=$mybasepath"/odoo-third-party-modules"
myocapath=$mybasepath"/oca-modules"

echo "Basepath: "$mybasepath
echo "Sourcepath: "$mysourcepath
echo "Serverpath: "$myserverpath
echo "Equitania addons path: "$myadpath
echo "Backup path: "$mybackuppath
echo "odoo-third-party-modules path: "$my3rdpath
echo "oca-modules path: "$myocapath

if [ ! -d $mybackuppath ]; then
  echo "Backup-Ordner anlegen"
  mkdir $mybackuppath
fi


cd $mybasepath
# Alte Installation entfernen
if [ -d $myserverpath ]; then
  echo "$myserverpath wird jetzt gesichert..."
  now=$(date +"%Y-%m-%d_%H-%M-%S")
  filename="odoo-server.$now.zip"
  mybackup=$mybackuppath"/"$filename
  zip -r "$mybackup"  "$myserverpath/"
  echo "Backup des Servers ist unter der Bezeichnung $mybackup zu finden..."
  rm -rf $myserverpath
  echo "Remove old server files.."
fi

echo "Geben Sie eine Datenbank an, die Sie  mit -u all aktualisieren wollen:"
read mydb

if [ "$mydb" != "" ]; then
  echo "$mydb wird jetzt gesichert..."
  now=$(date +"%Y-%m-%d_%H-%M-%S")
  filename="$mydb.$now.gz"
  mybackup=$mybackuppath"/"$filename
  pg_dump $mydb | gzip > $mybackup
  echo "Backup ist unter der Bezeichnung $mybackup zu finden..."
else
  echo "Es werden keine Backups durchgeführt!"
fi

mkdir $myserverpath
echo "Create odoo-server"

if [ -d $mysourcepath ]; then
  cd $mysourcepath
  git pull https://github.com/equitania/myodoo-server.git
  echo "Pull lastest branch myodoo-server.."
else
  cd $mybasepath
  git clone -b 8.0 --single-branch https://github.com/equitania/myodoo-server.git
  echo "Clone lastest branch myodoo-server.."
fi

if [ -d $myaddpath ]; then
  cd $myaddpath
  git pull https://github.com/equitania/odoo-addons.git
  echo "Pull lastest branch odoo-addons.."
else
  cd $mybasepath
  git clone -b master --single-branch https://github.com/equitania/odoo-addons.git
  echo "Clone lastest branch odoo-addons.."
fi

if [ -d $my3rdpath ]; then
  cd $my3rdpath
  git pull https://github.com/equitania/odoo-third-party-modules.git
  echo "Pull lastest branch odoo-third-party-modules.."
else
  cd $mybasepath
  git clone -b master --single-branch https://github.com/equitania/odoo-third-party-modules.git
  echo "Clone lastest branch odoo-third-party-modules.."
fi

if [ -d $myocapath ]; then
  cd $myocapath
  git pull https://github.com/equitania/oca-modules.git
  echo "Pull lastest branch oca-modules.."
else
  cd $mybasepath
  git clone -b master --single-branch https://github.com/equitania/oca-modules.git
  echo "Clone lastest branch oca-modules.."
fi

cp -r $mysourcepath/addons $myserverpath
echo "Copy addons..."
cp -r $mysourcepath/doc $myserverpath
echo "Copy doc..."
cp -r $mysourcepath/openerp $myserverpath
echo "Copy openerp..."
echo "Copy files..."
cp  $mysourcepath/openerp-wsgi.py $myserverpath
cp  $mysourcepath/odoo.py $myserverpath
cp  $mysourcepath/openerp-gevent $myserverpath

echo "Copy equitania addons"
cp -r $myaddpath/base_report_to_printer $myserverpath/addons
cp -r $myaddpath/eq_google_shopping_feed $myserverpath/addons
cp -r $myaddpath/eq_info_for_product_product $myserverpath/addons
cp -r $myaddpath/eq_mail_extension $myserverpath/addons
cp -r $myaddpath/eq_no_ad $myserverpath/addons
cp -r $myaddpath/eq_plain_reports $myserverpath/addons
cp -r $myaddpath/eq_quotation_enhancement $myserverpath/addons
cp -r $myaddpath/eq_stock_account_compatibility $myserverpath/addons
cp -r $myaddpath/eq_snom $myserverpath/addons
cp -r $myaddpath/equitania $myserverpath/addons
cp -r $myaddpath/equitania_limit_address_sale $myserverpath/addons
cp -r $myaddpath/web_clean_navbar $myserverpath/addons

echo "Copy third party addons"
cp -r $my3rdpath/dlt_germany_cities $myserverpath/addons
cp -r $my3rdpath/mail_check_immediately $myserverpath/addons
cp -r $my3rdpath/mail_delete_access_link $myserverpath/addons
cp -r $my3rdpath/mail_delete_odoo_footer $myserverpath/addons
cp -r $my3rdpath/mail_delete_sent_by_footer $myserverpath/addons
cp -r $my3rdpath/mail_fix_553 $myserverpath/addons
cp -r $my3rdpath/mail_fix_empty_body $myserverpath/addons
cp -r $my3rdpath/mail_html_widget_template $myserverpath/addons
cp -r $my3rdpath/mail_outgoing $myserverpath/addons
cp -r $my3rdpath/res_users_clear_access_rights $myserverpath/addons
cp -r $my3rdpath/smsclient $myserverpath/addons
cp -r $my3rdpath/sync_mail_forward $myserverpath/addons
cp -r $my3rdpath/web_easy_switch_company $myserverpath/addons
cp -r $my3rdpath/web_polymorphic_field $myserverpath/addons

echo "Copy oca addons"
cp -r $myocapath/attachment_preview $myserverpath/addons
cp -r $myocapath/auditlog $myserverpath/addons
cp -r $myocapath/crm_action $myserverpath/addons
cp -r $myocapath/crm_lead_code $myserverpath/addons
cp -r $myocapath/currency_rate_update $myserverpath/addons
cp -r $myocapath/database_cleanup $myserverpath/addons
cp -r $myocapath/disable_openerp_online $myserverpath/addons
cp -r $myocapath/email_template_template $myserverpath/addons
cp -r $myocapath/lettermgmt $myserverpath/addons
cp -r $myocapath/mass_editing $myserverpath/addons
cp -r $myocapath/product_attribute_multi_type $myserverpath/addons
cp -r $myocapath/product_customer_code $myserverpath/addons
cp -r $myocapath/product_variant_cost_price $myserverpath/addons
cp -r $myocapath/project_analytic_line_view $myserverpath/addons
cp -r $myocapath/project_categ $myserverpath/addons
cp -r $myocapath/project_classification $myserverpath/addons
cp -r $myocapath/project_description $myserverpath/addons
cp -r $myocapath/project_gtd $myserverpath/addons
cp -r $myocapath/project_task_code $myserverpath/addons
cp -r $myocapath/project_task_materials $myserverpath/addons
cp -r $myocapath/project_task_materials_stock $myserverpath/addons
cp -r $myocapath/report_custom_filename $myserverpath/addons
cp -r $myocapath/sale_order_project $myserverpath/addons
cp -r $myocapath/sale_order_revision $myserverpath/addons
cp -r $myocapath/web_context_tunnel $myserverpath/addons
cp -r $myocapath/web_dialog_size $myserverpath/addons
cp -r $myocapath/web_export_view $myserverpath/addons
cp -r $myocapath/web_hide_db_manager_link $myserverpath/addons
cp -r $myocapath/web_last_viewed_records $myserverpath/addons
cp -r $myocapath/web_searchbar_full_width $myserverpath/addons
cp -r $myocapath/web_sheet_full_width $myserverpath/addons
cp -r $myocapath/web_shortcuts $myserverpath/addons
cp -r $myocapath/web_translate_dialog $myserverpath/addons

if [ $mybasepath/config.py ]; then
  echo "Replace config.py"
  cp  $mybasepath/config.py $myserverpath/openerp/tools
fi
if [ $mybasepath/favicon.ico ]; then
  echo "Replace favicon.ico"
  cp  $mybasepath/favicon.ico $myserverpath/addons/web/static/src/img/
fi

if [ "$mydb" != "" ]; then
  echo "$mydb wird jetzt aktualisiert..."
  echo "Wechsele Pfad.."
  cd $myserverpath
  ./odoo.py --update=all --workers=0 --no-xmlrpc --stop-after-init --database=$mydb
else
  echo "Es werden keine Aktualisierungen durchgeführt!"
fi


echo "Finished!"
