#!/bin/bash
# Mit diesem Skript werden alle Pakete für den Odoo Betrieb unter Debian installiert
# Skript muss mit root-Rechten ausgeführt werden
# Version 1.3.0 - Stand 08.12.2016
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

echo "Prepare Debian"
apt-get update && apt-get dist-upgrade && apt-get autoremove

echo "Tools zip, unzip, mc(Midnight Comander) and htop will be install.."
apt-get install -y --no-install-recommends \
		needrestart \
		ca-certificates \
		ghostscript \
		graphviz \
		antiword  \
		poppler-utils \
		curl \
		build-essential \
		libfreetype6-dev \
		libjpeg-dev \
		python-dev \
		python-software-properties \
		python-pip  \
		wget \
		unzip \
		sqlite3 \
		nano \
		mc \
		geoip-bin \
		geoip-database \
		sudo \
		node-less \
		node-clean-css \
		tesseract-ocr \
		imagemagick \
		xfonts-75dpi \
		xfonts-base

while true; do
    read -p "Do you want install PostgreSQL? [y/n] / Wollen Sie die PostgreSQL-DB installieren? [j/n]: " yn
    case $yn in
        [YyJj]* ) echo "PostgreSQL will be install / PostgreSQL wird installiert ..."
                    apt-get install -y --no-install-recommends \
                            postgresql-9.4 \
                            postgresql-client-9.4
        break;;
        [Nn]* ) echo "PostgreSQL is not installed! / PostgreSQL wurde nicht installiert!"
                        break;;
        * ) echo "Please answer (y)es or (n)o. / Bitte antworten sie mit (j)a oder (n)ein";;
    esac
done


echo "pip packages will be install.."
pip install --upgrade pip \
		&& pip install Babel==1.3 \
		&& pip install argparse==1.2.1 \
		&& pip install decorator==3.4.0 \
		&& pip install docutils==0.12 \
		&& pip install feedparser==5.1.3 \
		&& pip install gevent==1.0.2 \
		&& pip install greenlet==0.4.7 \
		&& pip install jcconv==0.2.3 \
		&& pip install Jinja2==2.7.3 \
		&& pip install lxml==3.3.5 \
		&& pip install Mako==1.0.0 \
		&& pip install MarkupSafe==0.23 \
		&& pip install mock==1.0.1 \
		&& pip install ofxparse==0.15 \
		&& pip install passlib==1.6.2 \
		&& pip install Pillow==2.5.1 \
		&& pip install psutil==2.1.1 \
		&& pip install psycogreen==1.0 \
		&& pip install psycopg2==2.5.3 \
		&& pip install pydot==1.0.2 \
		&& pip install pyparsing==1.5.7 \
		&& pip install pyPdf==1.13 \
		&& pip install Python-Chart==1.39 \
		&& pip install python-dateutil==1.5 \
		&& pip install python-ldap==2.4.27 \
		&& pip install python-openid==2.2.5 \
		&& pip install pytz==2014.4 \
		&& pip install pyusb==1.0.0b1 \
		&& pip install PyYAML==3.11 \
		&& pip install pyserial==2.7 \
		&& pip install qrcode==5.0.1 \
		&& pip install reportlab==3.1.44 \
		&& pip install requests==2.6.0 \
		&& pip install six==1.7.3 \
		&& pip install suds-jurko==0.6 \
		&& pip install vatnumber==1.2 \
		&& pip install vobject==0.6.6 \
		&& pip install Werkzeug==0.9.6 \
		&& pip install wsgiref==0.1.2 \
		&& pip install XlsxWriter==0.9.3 \
		&& pip install xlwt==0.7.5 \
		&& pip install gdata==2.0.18 \
		&& pip install magic \
		&& pip install libxslt1 \
		&& pip install simplejson==3.5.3 \
		&& pip install webdav \
		&& pip install tz \
		&& pip install zsi \
		&& pip install unittest2==0.5.1 \
		&& pip install renderpm \
		&& pip install pdftools \
		&& pip install reportlab-accel \
		&& pip install openssl \
		&& pip install imaging \
		&& pip install matplotlib \
		&& pip install support \
		&& pip install beautifulsoup4 \
		&& pip install evdev \
		&& pip install polib \
		&& pip install unidecode \
		&& pip install validate_email \
		&& pip install pyDNS \
		&& pip install python-slugify \
		&& pip install paramiko==1.9.0 \
		&& pip install pycrypto==2.6 \
		&& pip install pyinotify \
		&& pip install ecdsa==0.11 \
		&& pip install sphinx \
		&& pip install Pygments==2.0 \
		&& pip install egenix-mx-base \
		&& pip install pypdf2 \
		&& pip install odoorpc \
		&& pip install phonenumbers

echo "OpenSans font will be install..."
wget https://release.myodoo.de/fonts/opensans.zip
unzip opensans.zip
mv opensans /usr/share/fonts/truetype/
rm opensans.zip

echo "Barcodes will be install..."
wget http://www.reportlab.com/ftp/pfbfer.zip
unzip pfbfer.zip -d fonts
mv fonts /usr/lib/python2.7/dist-packages/reportlab/
rm pfbfer.zip

# font cache empty
fc-cache -f -v


echo "WKHTML2PDF will be install..."
curl -k -o wkhtmltox.deb -SL https://release.myodoo.de/wkhtmltox-0.12.1.2_linux-jessie-amd64.deb \
    && echo '40e8b906de658a2221b15e4e8cd82565a47d7ee8 wkhtmltox.deb' | sha1sum -c - \
    && dpkg --force-depends -i wkhtmltox.deb \
    && apt-get -y install -f --no-install-recommends \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false -o APT::AutoRemove::SuggestsImportant=false npm \
    && rm -rf /var/lib/apt/lists/* wkhtmltox.deb

echo "System is prepared now for Odoo - System ist jetzt für Odoo vorbereitet!"
