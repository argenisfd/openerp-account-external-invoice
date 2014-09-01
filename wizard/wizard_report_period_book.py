from osv import osv, fields

class wizard_report_period_book(osv.osv_memory):
	_name="wizard.report.period_book"
	_description= 'Imprimir libro de Compra o Ventas'

	_columns= {
			  'period_id': fields.float('HOla', required=True, digits=(14,2), help='Monto sin derecho a credito fiscal'),

			 }

	def print_report(self, cr, uid, ids, context):
		#return {
		#	'type':'ir.actions.report.xml',
		#	'report_name': 'period_report',
		#	'datas':{'ids': [4] }
		#
		return {
			'type': 'ir.actions.report.xml',
			'report_name': 'account.external.invoice.compras.report',
			'datas': {'ids': [2]}
		}

	def close(self, cr, uid, ids, context):
		return {'type':'ir.actions.act_window_close'}

wizard_report_period_book()		