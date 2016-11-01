#!/bin/bash
# Mit diesem Skript werden alle Pakete für den Odoo Betrieb unter Debian installiert
# Skript muss mit root-Rechten ausgeführt werden
# Version 1.2.1 - Stand 13.06.2016
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
        mc \
        zip \
        unzip \
        htop \
        ca-certificates \
        ntp  \
        apt-transport-https \
        needrestart \
        curl \
        ghostscript \
        graphviz \
        antiword \
        poppler-utils \
        curl \
        build-essential \
        libfreetype6-dev \
        libjpeg-dev \
        wget \
        sqlite3 \
        geoip-bin \
        geoip-database \
        node-less \
        node-clean-css

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
        python-pip \
        python-magic \
        python-dateutil \
        python-pypdf \
        python-requests \
        python-feedparser \
        python-gdata \
        python-ldap \
        python-libxslt1 \
        python-lxml \
        python-mako \
        python-openid \
        python-psycopg2 \
        python-pybabel \
        python-pychart \
        python-pydot \
        python-pyparsing \
        python-reportlab \
        python-simplejson \
        python-tz \
        python-vatnumber \
        python-vobject \
        python-webdav \
        python-werkzeug \
        python-xlwt \
        python-yaml \
        python-zsi \
        python-docutils \
        python-psutil \
        python-unittest2 \
        python-mock \
        python-jinja2 \
        python-dev \
        python-pdftools \
        python-decorator \
        python-openssl \
        python-babel \
        python-imaging \
        python-reportlab-accel \
        python-paramiko \
        python-software-properties \
        python-matplotlib \
        python-support \
        python-passlib \
        python-pyinotify \
        python-gevent

echo "pip packages will be install.."
pip install passlib \
    && pip install beautifulsoup4 \
    && pip install evdev \
    && pip install reportlab \
    && pip install qrcode \
    && pip install polib \
    && pip install unidecode \
    && pip install validate_email \
    && pip install pyDNS \
    && pip install pysftp \
    && pip install python-slugify \
    && pip install six==1.4 \
    && pip install paramiko==1.9.0 \
    && pip install pycrypto==2.4 \
    && pip install pyinotify \
    && pip install ecdsa==0.11 \
    && pip install sphinx \
    && pip install babel==1.3 \
    && pip install Pygments==2.0 \
    && pip install docutils==0.11 \
    && pip install markupsafe \
    && pip install pytz \
    && pip install Jinja2==2.3 \
    && pip install odoorpc \
    && pip install egenix-mx-base \
    && pip install pillow==2.6.0 \
    && pip install pypdf2 \
    && pip install pyserial \
    && pip install pyusb \
    && pip install phonenumbers \
    && pip install psycogreen

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
