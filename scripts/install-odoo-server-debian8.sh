#!/bin/bash
# Mit diesem Skript installiert Odoo unter /opt/odoo und bindet es in den Autostart ein
# Skript muss mit root-Rechten ausgeführt werden
# Version 1.2.1 - Stand 29.03.2016
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

myscriptpath="$PWD"
mybasepath="/opt/odoo"
mysourcepath=$mybasepath"/myodoo-server"
myserverpath=$mybasepath"/odoo-server"
myaddpath=$mybasepath"/odoo-addons"
my3rdpath=$mybasepath"/odoo-third-party-modules"
myocapath=$mybasepath"/oca-modules"
myhelpers=$myaddpath"/scripts/server-install-helpers"

echo "Basepath: "$mybasepath
echo "Sourcepath: "$mysourcepath
echo "Serverpath: "$myserverpath
echo "odoo-addons path: "$myaddpath
echo "odoo-third-party-modules path: "$my3rdpath
echo "oca-modules path: "$myocapath

# Check if git is installed
if [ "$(dpkg -s git|grep -c installed)" = 0 ]; then
	echo "Das Paket git ist auf ihrem System nicht vorhanden. Es wird jetzt installiert ..."
	apt-get update && apt-get install git -y
fi

echo "Prepare PostgreSQL"
adduser odoo --home /opt/odoo --gecos "" --disabled-login

echo "Geben Sie das Passwort für den User odoo innerhalb der PostgreSQL an (Leerlassen für kein Passwort): "
read myodoopwd

if [ "$myodoopwd" != "" ]; then
  echo "PostgreSQL Passwort odoo wird gesetzt ..."
  su postgres -c "psql --command \"CREATE USER odoo WITH PASSWORD '$myodoopwd'\""
  su postgres -c "psql --command \"ALTER USER odoo CREATEDB\""
fi

echo "Geben Sie das Passwort für den User postgres innerhalb der PostgreSQL an (Leerlassen für kein Passwort): "
read mypsqlpwd

if [ "$mypsqlpwd" != "" ]; then
  echo "PostgreSQL Passwort postgres wird gesetzt ..."
  su postgres -c "psql --command \"ALTER USER postgres WITH PASSWORD '$mypsqlpwd'\""
fi

cd $mybasepath
git clone -b 8.0 --single-branch https://github.com/equitania/myodoo-server.git
echo "Clone lastest branch myodoo.."

cd $mybasepath
git clone -b 8.0 --single-branch https://github.com/equitania/odoo-addons.git
echo "Clone lastest branch odoo-addons.."

cd $mybasepath
git clone -b 8.0 --single-branch https://github.com/equitania/odoo-third-party-modules.git
echo "Clone lastest branch odoo-third-party-modules.."

cd $mybasepath
git clone -b 8.0 --single-branch https://github.com/equitania/oca-modules.git
echo "Clone lastest branch oca-modules.."

mkdir $myserverpath
echo "Create odoo-server"

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
cp -r $my3rdpath/auto_backup $myserverpath/addons
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
cp -r $myocapath/web_context_tunnel $myserverpath/addons
cp -r $myocapath/web_dialog_size $myserverpath/addons
cp -r $myocapath/web_export_view $myserverpath/addons
cp -r $myocapath/web_hide_db_manager_link $myserverpath/addons
cp -r $myocapath/web_last_viewed_records $myserverpath/addons
cp -r $myocapath/web_searchbar_full_width $myserverpath/addons
cp -r $myocapath/web_sheet_full_width $myserverpath/addons
cp -r $myocapath/web_shortcuts $myserverpath/addons
cp -r $myocapath/web_translate_dialog $myserverpath/addons

echo "Insert the password for the databasemanager | Geben Sie das Passwort für den Databasemanager ein (Leerlassen für kein Passwort): "
read myadminpwd

old="'admin_passwd': 'admin'"
new="'admin_passwd': '$myadminpwd'"

echo "Changing databasemanager password / Ändere das Kennwort des Datenbankmanagers ..."
cp  $myserverpath/openerp/tools/config.py $mybasepath/config.py
sed -i "s/$old/$new/g" $mybasepath/config.py
cp  $mybasepath/config.py $myserverpath/openerp/tools

echo "Preparing favicon for later exchange ..."
cp  $myserverpath/addons/web/static/src/img/favicon.ico $mybasepath/

echo "Changing rights / Ändere Ordner-Rechte ..."
chown -R odoo:odoo $myserverpath
chown -R odoo:odoo $mysourcepath
chown -R odoo:odoo $mybasepath

echo "Kopiere Serverkonfiguration ..."
cp $myhelpers/odoo-server.conf /etc/odoo-server.conf
chown odoo:odoo /etc/odoo-server.conf
chmod 640 /etc/odoo-server.conf

echo "Prepare logfile / Bereite Lagdatei vor ..."
mkdir /var/log/odoo
chown odoo:root /var/log/odoo
cp $myhelpers/logrotate /etc/logrotate.d/odoo-server
chmod 755 /etc/logrotate.d/odoo-server

echo "Prepare odoo-server as service / Bereite odoo-server als Service vor ..."
cp $myhelpers/odoo.init.d /etc/init.d/odoo-server
chmod +x /etc/init.d/odoo-server
update-rc.d odoo-server defaults

echo "Finished!"
