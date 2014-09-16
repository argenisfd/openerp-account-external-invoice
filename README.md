Módulo de contabilidad Externa para OpenERP
===========================================

Módulo de openERP 6.1+ para registrar Facturas sin necesidard de Facturar, útil para contadores externos 
que deseen llevar la contabilidad de sus clientes a traves de OpenERP. (Adecuado a la contabilidad Venezolana)

Dependencias:
* [OpenERP 6.1+][1]  (unicamente ha sido probado en la versión 6.1) 
* [Aeroo Report][2] 
* Módulo de Contabilidad de OpenERP

1) Instalación
---------------

### Descargando el módulo

Una vez instalado OpenERP 6.1+ y Aeroo Report debes acceder al directorio addons/ de tu instalación de openERP
y ejecutar el siguiente comando para clonar el repositorio:
	
	git clone https://github.com/argenisfd/openerp-account-external-invoice.git account-external-invoice



### Instalando en OpenERP

* Si ya has iniciado OpenERP debes detener el proceso y volverlo a iniciar
* Entra como administrador a OpenERP entra en el menú `Configuación > Módulos > Actualizar Lista De Módulos`. clic en actualizar y luego aceptar
* Entra en `Configuración > Módulos > Modules`, desmarca la opción "Aplicaciones en Linea" y escribe "account-external-invoice" en el campo name [Enter], clic en instalar y seguir los pasos del wizard

### Agregando Reportes
	
Una vez instalado el módulo es hora de agregar el reporte al módulo de Aeroo Report:
entra en `Configuración > Perzonalización > Aeroo Report > Reports`, y crea un reporte con los siguientes datos:

	Nombre: [Nombre que mejor te parezca]
	Objeto: "account.period"
	Nombre del Servicio: "account.external.invoice.purshases.report"
	Template Mime-type: "ODF SpreadSheed (.ods)"
	Template Mime-type: [puedes seleccionar entre ODF y XLS]
	Template Source: Database
	Template Content: [Aquí selecciona el archivo que se encuente dentro la carpeta del modulo en {...}/report/report_account_external_invoice_purshases.ods]

Los demás campos los puedes dejar con los valores por defecto

2) Usando el nuevo módulo
---------------------------

Para usar el nuevo módulo instalado, debes ingresar al Menú `Contabilidad > Registro de Comprobantes` allí aparecen todas las opciones del módulo  


3) Instalando dependencias
----------------------------
### Instalar Bazar [Doc][3]

Fundamentalmente es ejecutar el siguiente comando 
	sudo apt-get install bzr

Para mayor información, consultar la documentación [Manual de instalación bazar][3]

### Instalar aeroo report [Doc][4]
Situarse en cualquier directorio

	$ bzr branch lp:aeroolib
	$ cd aeroolib/aeroolib
	$ sudo python ./setup.py install

Situarse en la carpeta de openerp y crear la parpeta "vendors" 
 	$ cd /var/www/openerp-6.1/
 	$ mkdir vendors

Ajecututar los siguientes comandos para descargar los módulos de aeroo

	$ cd vendors/
	$ bzr branch https://launchpad.net/aeroo --esto no se ejecuta
	$ bzr branch lp:aeroo/openerp6.1.x aeroo

	$ bzr branch https://launchpad.net/aeroolib

Agreagar la nueva vendors a las rutas de addons
	
	$ cd /var/www/openerp-6-1/
	$ nano erp.conf

-
	#erp.cong
	...
	[options]
	addons_path = /var/www/openerp-6.1/openerp/addons,/var/www/openerp-6.1/vendors/aeroo
	...

#Instalar dependencias de aeroo
 	$ sudo apt-get install python-genshi 



Entrar en OpenERP e instalar el módulo aeroo desde el gestor de paquetes No olvidar actualizar la lista de paquetes para que aparezca

[1]: http://nightly.openerp.com/6.1/releases/
[2]: http://www.alistek.com/wiki/index.php/Main_Page
[3]: https://help.ubuntu.com/10.04/serverguide/bazaar.html
[4]: http://www.alistek.com/wiki/index.php/Aeroo_Reports_Linux_server