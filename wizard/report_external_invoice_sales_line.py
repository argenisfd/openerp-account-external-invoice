from osv import osv, fields, orm
class report_external_invoice_sales_line(osv.osv):
	_name = "report.external.invoice.sales.line"
	_description = "Vista para el reporte de Ventas" 
	_auto = False
	_columns= {
		'period_id': fields.many2one('account.period', 'Period',  readonly=True),
		'doc_date': fields.char('Invoice Date', size=20, readonly=True),
		'doc_number': fields.char('Invoice Number', size=20, readonly=True),
		'doc_control_number': fields.char('Control Number', size=20, readonly=True),
		'doc_type': fields.char('Doc Type', size=20, readonly=True),
		'affected_invoice': fields.char('Factura afectada', size=20,  readonly=True),
		'partner_name': fields.char('Nombre del Provedor', size=150,  readonly=True),
		'partner_rif': fields.char('Rif del Proveedor', size=20, readonly=True),
		'partner_type_custom': fields.char('Juridico o Natural', size=1, readonly=True),
		#'registro': fields.char('Reg-01', size=10, readonly=True),
		#Contribuyente
		'contributor_total': fields.float('Total Compras', readonly=True, digits=(14,2)),
		"contributor_no_tax": fields.float('Exento Importacion', readonly=True, digits=(14,2)),
		"contributor_base": fields.float('Base Importacion', readonly=True, digits=(14,2)),
		"contributor_tax_amount": fields.float('IVA Importacion', readonly=True, digits=(14,2)),
		#no contribuyente
		'no_contributor_total': fields.float('Total Compras', readonly=True, digits=(14,2)),
		"no_contributor_no_tax": fields.float('Exento Importacion', readonly=True, digits=(14,2)),
		"no_contributor_base": fields.float('Base Importacion', readonly=True, digits=(14,2)),
		"no_contributor_tax_amount": fields.float('IVA Importacion', readonly=True, digits=(14,2)),
		#Retenciones
		"retention_number": fields.char('Numero de la retencion', size=20, readonly=True),
		"retention_amount": fields.char('monto de la retencion', size=20, readonly=True),

		
	}

	def init(self, cr):
		
		cr.execute("""
		CREATE OR REPLACE VIEW report_external_invoice_sales_line AS (
			SELECT	ae.id,
					ae.period_id,
					ae.date_invoice AS doc_date, 
					ae.invoice_number AS doc_number,
					ae.control_number AS doc_control_number,
					ae.doc_type,
					'factura_afectada' AS affected_invoice,
					rp.name AS partner_name,
					rp.ref AS partner_rif,
					'tipo partner' AS partner_type_custom,
					-- Contribuyente
					CASE WHEN char_length(rp.ref)=9 THEN ae.base+ae.no_tax+ae.tax_amount END AS contributor_total,
					CASE WHEN char_length(rp.ref)=9 THEN ae.no_tax END AS contributor_no_tax,
					CASE WHEN char_length(rp.ref)=9 THEN ae.base END AS contributor_base,
					CASE WHEN char_length(rp.ref)=9 THEN ae.tax_amount END AS contributor_tax_amount,
					-- No contribuyente
					CASE WHEN char_length(rp.ref)<>9 THEN ae.base+ae.no_tax+ae.tax_amount END AS no_contributor_total,
					CASE WHEN char_length(rp.ref)<>9 THEN ae.no_tax END AS no_contributor_no_tax,
					CASE WHEN char_length(rp.ref)<>9 THEN ae.base END AS no_contributor_base,
					CASE WHEN char_length(rp.ref)<>9 THEN ae.tax_amount END AS no_contributor_tax_amount,
					-- Retenciones
					CASE WHEN ae.doc_type = 'RIV' THEN 'NRO DE COMPROBANTE' ELSE NULL END AS retention_number,
					CASE WHEN ae.doc_type = 'RIV' THEN ae.retention_amount ELSE NULL END AS retention_amount
			FROM account_external_invoice ae
			INNER JOIN res_partner rp ON ae.partner_id = rp.id
			WHERE ae.type ='out_invoice'
		)
			""")

report_external_invoice_sales_line();