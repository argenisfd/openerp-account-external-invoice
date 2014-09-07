from osv import osv, fields

class wizard_report_period_book(osv.osv_memory):
	_name="wizard.report.period_book"
	_description= 'Imprimir libro de Compra o Ventas'

	_columns= {
			  'company_id': fields.many2one('res.company', 'Company', required=True, change_default=False, readonly=False),
			  'period_id': fields.many2one('account.period', 'Period', required=True, readonly=False),
			  'report_type':fields.selection( ( ('V', "Libro de Ventas" ), 
										('C', "Libro de Compras")
										), required=True)
			 }

	_defaults= {
	 'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'account.invoice', context=c),
	 'report_type': 'V'
	}
	def print_report(self, cr, uid, ids, context):
		if context is None:
			context = {}		
		wiz = self.browse(cr, uid, ids, context=context)
		wiz= wiz[0]
		#return {
		#	'type':'ir.actions.report.xml',
		#	'report_name': 'period_report',
		#	'datas':{'ids': [4] }
		#
		print "HOLA-------------***********************--------------HOLA"
		#print wiz[0].period_id.id
		#print wiz.report_type
		#print wiz.period_id.id
		#print wiz
		#print context
		ret={'type': 'ir.actions.report.xml',
				  'report_name': "",
				  'datas': {'ids': [wiz.period_id.id] }
				  }

		if wiz.report_type == 'V':
			ret['report_name']='account.external.invoice.sales.report'
		else:
			if wiz.report_type == 'C':
				ret['report_name']='account.external.invoice.purshases.report'
			else: 
				print "ERRRROOOOOO EL TIPO DE DEPORTE DEBE SE V o C"

		return ret
		#return {
		#	'type': 'ir.actions.report.xml',
			# Este es para el reporte de Compras
			#'report_name': 'account.external.invoice.purshases.report',
		#	'report_name': 'account.external.invoice.sales.report',
		#	'datas': {'ids': wiz.period_id.id}
		#}

	def close(self, cr, uid, ids, context):
		return {'type':'ir.actions.act_window_close'}

wizard_report_period_book()		
