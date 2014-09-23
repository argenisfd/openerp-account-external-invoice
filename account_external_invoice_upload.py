from osv import osv, fields, orm
import tempfile
import csv
import time
import base64

class account_external_invoice_upload(osv.osv):
	_name = 'account.external.invoice.upload'
	_description = "Register invoice from File"

	_columns = {
		'file': fields.binary("Data"),
		'company_id': fields.many2one('res.company', 'Company', required=True, change_default=False, readonly=False),
		'period_id': fields.many2one('account.period', 'Period', required=True, readonly=False),
		'journal_id': fields.many2one('account.journal', 'Journal', required=True, readonly=False ),
		'tax_id': fields.many2one('account.tax', 'Tax', help="The tax basis of the tax declaration.", required=True),
		'account_id' : fields.many2one('account.account', 'Account', required=True, ondelete="cascade"),
		'inverse_account_id' : fields.many2one('account.account', 'Inverse Account', required=True, ondelete="cascade"),
		'state': fields.selection([('pending','Pendiente'), ('entry','Asentado')], 'State', required=True, readonly=True,help='Estatus en el que se ecuentra')
		}
	_defaults= {
		'state': 'pending',
		'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'account.invoice', context=c),
		}
	def create (self, cr, uid, vals, context=None):
		newId = super(account_external_invoice_upload, self).create(cr, uid,vals, context=context)
		newObj=self.pool.get('account.external.invoice.upload').browse(cr, uid, newId, context=None)
		print newId;
		print tempfile.gettempdir() # prints the current temporary directory
		f = tempfile.TemporaryFile(prefix='invoice_upload_', suffix='.scv', dir=tempfile.gettempdir())
		#f= open("/var/www/openerp-6.1/temp_files/tttttttttttemp_openerp.csv","w+")
		cont=base64.decodestring(newObj.file)
		f.write(cont)
		f.seek(0)
		cols = {'fecha':1,  
			"nro_doc": 2, 
			"nro_control": 3,
			"company_name": 6,
			"rif": 7,
			"tipo_trans":8,
			"exento":10,
			"base": 11,
			"tax_amount": 13
		}
		reader = csv.reader(f,delimiter=',')
		readed_obj={}
		print cols
		for row in reader:



			print row
			fecha = row[cols["fecha"]]
			fechaArray = fecha.split("/")
			if len(fechaArray) != 3:
				continue
			fecha= fechaArray[2]+"-"+fechaArray[1]+"-"+fechaArray[0]
			nro_doc= row[cols["nro_doc"]]
			nro_control= row[cols["nro_control"]]
			company_rif= row[cols["rif"]]
			company_name= row[cols["company_name"]]
			exento= float(row[cols["exento"]].replace(",","."))
			base= float(row[cols["base"]].replace(",","."))
			tax_amount= float(row[cols["tax_amount"]].replace(",","."))

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
					'opt_output': False
					}, context=context)
				company=self.getompany(cr, uid, company_rif)

			self.createExternalInvoiceRow(cr, uid,{
				'type': 'out_invoice',
				'doc_type':'F',
				'invoice_number': nro_doc,
				'control_number': nro_control,
				'date_invoice': fecha,
				'period_id': vals['period_id'],
				'journal_id': vals['journal_id'],
				'partner_id': company[0],
				'account_id': vals['journal_id'],
				'inverse_account_id': vals['inverse_account_id'],
				'no_tax': exento,
				'base': base,
				'tax_id': vals['tax_id'],
				'tax_amount':tax_amount,

				'retention_amount': 0.00,
				'state':  'pending_entry',
				'import': False,
				'reg': '01-REG',
				}, context)
		f.close();
		return newId

	def getompany(self, cr, uid, rif ):

		obj=self.pool.get('res.partner').search(cr, uid, [('ref','=', rif )], 0, 1)
		print obj
		return obj
	def createcompany(self, cr, uid, vals, context=None):
		self.pool.get('res.partner').create(cr, uid, vals, context=context)

	def createExternalInvoiceRow(self, cr, uid, vals, context=None):
		print 
		self.pool.get('account.external.invoice').create(cr, uid, vals, context=context)
	#def getiva(self, cr, uid, amount, type="sales", context=None):
	#	obj=self.pool.get('res.partner').search(cr, uid, [('amount','=', amount ), 'type'], 0, 1)
