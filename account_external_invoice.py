from osv import osv, fields
import time
class account_external_invoice(osv.osv):
	_name = 'account.external.invoice'
	_description = "Register Invoice"

	def _cal_total_amount(self, cr, uid, ids, name, args, context=None):
		res = {}
		for invoice in self.browse(cr, uid, ids, context=context):
			res[invoice.id]=0.0
			res[invoice.id]=invoice.base+invoice.tax_amount+invoice.no_tax
			#for line in invoice.invoice_line:
			#    res[invoice.id]['amount_untaxed'] += line.price_subtotal
			#for line in invoice.tax_line:
			#    res[invoice.id]['amount_tax'] += line.amount
			#res[invoice.id]['amount_total'] = res[invoice.id]['amount_tax'] + res[invoice.id]['amount_untaxed']
		return res
	_columns = {
		'invoice_number': fields.char('Nro. Factura', size=20, required=True),
		'control_number': fields.char('Nro. Control', size=20, required=False),
		'date_invoice': fields.date('Invoice Date', readonly=False, select=True, help="Fecha de la Factura"),
		'period_id': fields.many2one('account.period', 'Period', required=True, readonly=False),
		'journal_id': fields.many2one('account.journal', 'Journal', required=True, readonly=False ),
		'partner_id': fields.many2one('res.partner', 'Partner', change_default=True, readonly=False, required=True),
		'no_tax': fields.float('No Gravado', required=True, digits=(14,2), help='Monto sin derecho a credito fiscal'),
		'base': fields.float('BIG', required=True, digits=(14,4), help='Base Imponible'),
		'tax_id': fields.many2one('account.tax', 'Tax', help="The tax basis of the tax declaration.", required=True),
		'tax_amount': fields.float('Total IVA', required=True, digits=(14,2), help='Tax Amount'),
		'total_amount': fields.function(_cal_total_amount, digits=(14,2), string='Total Amount', store=False),
		#'total_amount': fields.float('Total', required=False, readonly=True digits=(14,4),  help='Total del Documento'),
		#'total_amount': fields.float('Total', required=False, readonly=True digits=(14,4),  help='Total del Documento'),
		}
	_order = "period_id"

	def onchange_iva(self, cr, uid, ids, base,no_tax, context=None):
		iva=0.00
		total=0.00
		iva=base*0.12
		total=base+iva+no_tax
		return {'value': {'tax_amount': iva, 'total_amount': total } }

	def onchange_total_iva(self, cr, uid, ids, base,tax_amount,no_tax, context=None):
		return {'value': { 'total_amount': base+tax_amount+no_tax } }
account_external_invoice()