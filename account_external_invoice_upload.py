from osv import osv, fields, orm
import tempfile
import csv
import time
import base64

class account_external_invoice_upload(osv.osv):
	_name = 'account.external.invoice.upload'
	_description = "Register invoice from File"

	_columns = {
		'file': fields.binary("Data",required=True),
		'type': fields.selection([('out_invoice','Venta'), ('in_invoice','Compra')], 'Sale / Buy', required=True, readonly=False, select=False, help='Si es de venta o compra'),
		'company_id': fields.many2one('res.company', 'Company', required=True, change_default=False, readonly=False),
		'period_id': fields.many2one('account.period', 'Period', required=True, readonly=False, domain="[('company_id','=', company_id)]"),
		'journal_id': fields.many2one('account.journal', 'Journal', required=True, readonly=False, domain="[('company_id','=', company_id)]" ),
		'tax_id': fields.many2one('account.tax', 'Tax', help="The tax basis of the tax declaration.", required=True),
		'account_id' : fields.many2one('account.account', 'Account', required=True, ondelete="cascade",domain="[('company_id','=', company_id)]"),
		'inverse_account_id' : fields.many2one('account.account', 'Inverse Account', required=True, ondelete="cascade", domain="[('company_id','=', company_id)]"),
		'state': fields.selection([('pending','Pendiente'), ('proccessed','Procesado'), ('cancelled','Cancelado')], 'State', required=True, readonly=True,help='Estatus en el que se ecuentra'),
		'csv_separator': fields.selection([(',','comma (,)'), (';','punto y coma (;)')], 'CSV Seprator', required=True, readonly=False,help='Separador del Archivo CSV')
		}
	_defaults= {
		'state': 'pending',
		'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'account.invoice', context=c),
		}
	def create (self, cr, uid, vals, context=None):
		newId = super(account_external_invoice_upload, self).create(cr, uid,vals, context=context)
		newObj=self.pool.get('account.external.invoice.upload').browse(cr, uid, newId, context=None)
		return newId



	def getompany(self, cr, uid, rif ):

		obj=self.pool.get('res.partner').search(cr, uid, [('ref','=', rif )], 0, 1)
		print obj
		return obj
	def createcompany(self, cr, uid, vals, context=None):
		partner_id=self.pool.get('res.partner').create(cr, uid, vals, context=context)
		self.pool.get('res.partner.address').create(cr, uid, {'partner_id': partner_id}, context=context)


	def createExternalInvoiceRow(self, cr, uid, vals, context=None):
		self.pool.get('account.external.invoice').create(cr, uid, vals, context=context)
	

	def proccess_file(self, cr, uid, ids, context=None):
		newObj=self.pool.get('account.external.invoice.upload').browse(cr, uid,  ids[0], context=None)
		print tempfile.gettempdir() # prints the current temporary directory
		f = tempfile.TemporaryFile(prefix='invoice_upload_', suffix='.scv', dir=tempfile.gettempdir())
		#f= open("/var/www/openerp-6.1/temp_files/tttttttttttemp_openerp.csv","w+")
		cont=base64.decodestring(newObj.file)
		f.write(cont)
		f.seek(0)

		cols_mail = ('fecha_doc',  
			"nro_doc", 
			"nro_control",
			"cliente",
			"cliente_rif",
			"tipo_trans",
			"exento",
			"base",
			"iva_monto"
		)

		cols={}

		print "separator-----------------------"
		print newObj.csv_separator
		reader = csv.reader(f,delimiter=str(newObj.csv_separator))
		titles= reader.next()
		print "headers:"
		print titles
		i=0
		for keys in titles:
			if keys in cols_mail:
				cols[keys]=i
			i+=1	 

		readed_obj={}

		for row in reader:
			print row
			date_separator="/"
			fecha = row[cols["fecha_doc"]]

			print "---------------++++++++++FECHA++++++--------------"
			print fecha
			if fecha.find("/") != -1:
				date_separator="/"
			else:
				if fecha.find("-") != -1:
					date_separator="-"	
			
			fechaArray = fecha.split(date_separator)
			if len(fechaArray) != 3:
				continue
			fecha= fechaArray[2]+"-"+fechaArray[1]+"-"+fechaArray[0]
			nro_doc= row[cols["nro_doc"]]
			nro_control= row[cols["nro_control"]]
			company_rif= row[cols["cliente_rif"]]
			company_name= row[cols["cliente"]]
			exento= self.convertir_float(row[cols["exento"]])
			base= self.convertir_float(row[cols["base"]])
			tax_amount= self.convertir_float(row[cols["iva_monto"]])

			company=self.getompany(cr, uid, company_rif)
			if not company : 
				print "ETERRRRRRR";
				self.createcompany( cr, uid,
					{'active': True,
					'lang': 'es_VE',
					'customer': True,
					'credit_limit': 0,
					'name': company_name,
					'ref': company_rif,
					'opt_output': False,
					'supplier': True,
					'property_account_receivable': newObj.account_id.id,
					'property_account_payable': newObj.inverse_account_id.id,

					}, context=context)
				company=self.getompany(cr, uid, company_rif)

			self.createExternalInvoiceRow(cr, uid,{
				'type': newObj.type,
				'doc_type':'F',
				'invoice_number': nro_doc,
				'control_number': nro_control,
				'date_invoice': fecha,
				'period_id': newObj.period_id.id,
				'journal_id': newObj.journal_id.id,
				'partner_id': company[0],
				'account_id': newObj.account_id.id,
				'inverse_account_id': newObj.inverse_account_id.id,
				'no_tax': exento,
				'base': base,
				'tax_id': newObj.tax_id.id,
				'tax_amount':tax_amount,

				'retention_amount': 0.00,
				'state':  'pending_entry',
				'import': False,
				'reg': '01-REG',
				'_file_id': newObj.id 
				}, context)
		f.close();
		self.log(cr, uid, ids[0], "El Archivo se ha ")
		self.write( cr, uid, newObj.id, {"state": "proccessed"  }, context=context)


	def revert_external_invoice(self, cr, uid, ids, context=None):
		doc_ids=self.pool.get("account.external.invoice").search(cr, uid, [('_file_id', '=', ids[0]) ])
		docsArray=self.pool.get("account.external.invoice").unlink(cr, uid, doc_ids )
		self.log(cr, uid, ids[0], "Se ha eliminado correctamente")
		self.write( cr, uid, ids, {"state": "cancelled"  }, context=context)

	def convertir_float(self, param):
		if(param==""):
			return 0.0
		ret="";
		arr=param.split(".")
		if len(arr)>=2:
			if len(arr[1]) >= 3:
				for n in arr:
					ret= ret+n
			else :
				ret=arr[0]+","+arr[1]
		else:
			ret = param
		ret=ret.replace(",",".")
		return float(ret)
	#def getiva(self, cr, uid, amount, type="sales", context=None):
	#	obj=self.pool.get('res.partner').search(cr, uid, [('amount','=', amount ), 'type'], 0, 1)
