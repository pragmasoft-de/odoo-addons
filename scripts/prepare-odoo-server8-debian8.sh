#!/bin/bash
# Mit diesem Skript werden alle Pakete für den Odoo Betrieb unter Debian installiert
# Skript muss mit root-Rechten ausgeführt werden
# Version 1.3.1 - Stand 29.01.2017
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
		ca-certificates \
		ghostscript \
		graphviz \
		antiword  \
		poppler-utils \
		mtr \
		dnsutils \
		curl \
		postgresql-client-9.4 \
		build-essential \
		libfreetype6-dev \
		libjpeg-dev \
		libpq-dev \
		python-dev \
		libxml2-dev \
		libxslt1-dev \
		libldap2-dev \
		libsasl2-dev \
		libffi-dev \
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

echo "apt-get python packages will be install.."
apt-get install -y --no-install-recommends \
		python-software-properties \
		python-pip  \
		python-psycopg2 \
		python-ldap \
		python-magic \
		python-libxslt1 \
		python-imaging \
		python-openssl \
		python-renderpm \
		python-reportlab-accel \
		python-support \
		python-tz \
		python-zsi \
		python-webdav

echo "pip packages will be install.."
pip install --upgrade pip
pip install Babel==2.3.4
pip install decorator==4.0.10
pip install docutils==0.12
pip install feedparser==5.2.1
pip install gevent==1.1.2
pip install greenlet==0.4.10
pip install jcconv==0.2.3
pip install Jinja2==2.8
pip install lxml==3.6.4
pip install Mako==1.0.4
pip install MarkupSafe==0.23
pip install mock==2.0.0
pip install ofxparse==0.15
pip install passlib==1.6.5
pip install Pillow==3.4.1
pip install psutil==4.3.1
pip install psycogreen==1.0
pip install pydot==1.2.3
pip install pyparsing==2.1.10
pip install pyPdf==1.13
pip install pyserial==3.1.1
pip install Python-Chart==1.39
pip install python-dateutil==2.5.3
pip install python-openid==2.2.5
pip install pytz==2016.7
pip install pyusb==1.0.0
pip install PyYAML==3.12
pip install qrcode==5.3
pip install reportlab==3.3.0
pip install requests==2.11.1
pip install six==1.10.0
pip install suds-jurko==0.6
pip install vatnumber==1.2
pip install vobject==0.9
pip install Werkzeug==0.11.11
pip install wsgiref==0.1.2
pip install XlsxWriter==0.9.3
pip install xlwt==1.1.2
pip install gdata
pip install simplejson
pip install unittest2
pip install pdftools
pip install matplotlib
pip install beautifulsoup4
pip install evdev
pip install polib
pip install unidecode
pip install validate_email
pip install pyDNS
pip install python-slugify
pip install paramiko==1.9.0
pip install pycrypto==2.6
pip install pyinotify
pip install ecdsa==0.11
pip install sphinx
pip install Pygments==2.0
pip install egenix-mx-base
pip install pypdf2
pip install odoorpc
pip install pyelasticsearch
pip install openpyxl
pip install phonenumbers
pip install pysftp

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
