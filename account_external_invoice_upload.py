from osv import osv, fields, orm
import tempfile
import csv
import time

class account_external_invoice_upload(osv.osv):
	_name = 'account.external.invoice.upload'
	_description = "Register invoice from File"

	_columns = {
		'file': fields.binary("Data"),
		'company_id': fields.many2one('res.company', 'Company', required=True, change_default=False, readonly=False),
		'period_id': fields.many2one('account.period', 'Period', required=True, readonly=False),
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
		#f = tempfile.TemporaryFile(prefix='invoice_upload_', suffix='.scv', dir=tempfile.gettempdir())
		f= open("/var/www/openerp-6.1/temp_files/tttttttttttemp_openerp.csv","w")
		print newObj.file
		f.write(newObj.file)
		print newObj
		print f
		f.seek(0)
		reader = csv.reader(f)
		for row in reader:
			print row
		print "INICIOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
		
		time.sleep(60)
		f.close();
		print "FINNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN"
		return newId
