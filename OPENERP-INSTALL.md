Instalando Ubuntu
Instalar ubuntu server 12.4 LTS
#instalar solo los modulos de DNS (opcional)
# Postgress
# OpenSSH

user: openerp
passw: pass*1946


	sudo mkdir /var/www/openerp-6.1
    chmod 0777 /var/www/openerp-6.1

# configurar postgres
	 $ sudo su postgres
	 $ createuser openerp
	 - Shall the new role be a superuser? (y/n) y
	 psql -l
	 psql template1
Usa el siguiente comando para aplicar los permisos de acceso al rol openerp para que la base de datos la cual será creada desde el cliente de OpenERP:
	template1=# alter role openerp with password 'pass*254$';
	- ALTER ROLE


# Instalar los paquetes necesarios

Python 2.6 o posterior es requerido para OpenERP 6.1. Esta instalado en la versión de Ubuntu versión 10.04 y posterior. Unas cuantas librerías de Python tambien son requeridas, como se listan a continuación.

En las distribuciones basadas en Debian puedes instalar todas las dependencias requeridas con un comando sencillo:
	$ sudo apt-get upgrate

	$ sudo apt-get install python-dateutil python-feedparser python-gdata python-ldap python-libxslt1 python-lxml python-mako python-openid python-psycopg2 python-pybabel python-pychart python-pydot python-pyparsing python-reportlab python-simplejson python-tz python-vatnumber python-vobject python-webdav python-werkzeug python-xlwt python-yaml python-zsi

NOTA: si da problemas con las dependencias de paquetes correr los siguiente comando y continuar ([Fuente][1])
	sudo rm /var/lib/apt/lists/* -vf
	sudo apt-get clean
	sudo apt-get autoremove
	sudo apt-get update
	//el siguente comando No lo ejecuté (rechacé cuando me preguntó [intentó actualizar a ubuntu 14 ])
	sudo apt-get dist-upgrade 


Instalando openerp
	$ tar -xzf openerp-6.1-latest.tar.gz
	$ sudo chmod -R 0777 /var/www/openerp-6.1
	$ cp -R openerp-6.1-20140405-232737/* /var/www/openerp-6.1/
	$ cd /var/www/openerp-6.1/
	$ sudo python setup.py install
	//mensaje final: Finished processing dependencies for openerp==6.1-20140405-232737

Es probable es el comando anterior de erro de que no existe setuptool, para corregislo ejecutar lo siguiente

	sudo apt-install python-setuptools

ejecutar el siguiente comando para crear el archivo de configuracion
	
	$ openerp-server -s -c erp.conf

Abrir el nuevoo archivo generado y modificar los siguientes valores
	//erp.conf
	db_user = openerp
	db_password = 1234

Iniciar el servicor
	openerp-server -c erp.conf

# Instalando git
	$ sudo apt-get install git


# Instalando Aeroo Report [Fuente][install-aero]

## Dependencias Aeroo 
	$ sudo apt-get install openoffice.org python-genshi python-cairo python-openoffice python-lxml python-uno
	$ sudo apt-get install zip bzr

Descargar la libreria  aeroo desde launchpad  e instalar como un módule de python

	cd ~
	bzr branch lp:aeroolib
	cd aeroolib/aeroolib/
	sudo python ./setup.py install
	Create a new folder and download a

[1]: http://askubuntu.com/questions/297757/why-after-fresh-ubuntu-12-04-installation-update-arent-being-installed
[install-aeroo]: https://www.odoo.com/es_ES/forum/help-1/question/how-to-install-aeroo-reports-2780
