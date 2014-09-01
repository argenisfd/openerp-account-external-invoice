from osv import osv, fields, orm
class report_external_invoice_purchases_line(osv.osv):
	_name = "report.external.invoice.purchases.line"
	_description = "Vista para el reporte de Ventas" 
	_auto = False
	_columns= {
		'period_id': fields.many2one('account.period', 'Period',  readonly=True),
		'doc_date': fields.char('Invoice Date', size=20, readonly=True),
		'doc_number': fields.char('Invoice Number', size=20, readonly=True),
		'doc_control_number': fields.char('Control Number', size=20, readonly=True),
		'fact_afectada': fields.char('Factura afectada', size=20,  readonly=True),
		'partner_name': fields.char('Nombre del Provedor', size=150,  readonly=True),
		'partner_rif': fields.char('Rif del Proveedor', size=20, readonly=True),
		'partner_type_custom': fields.char('Juridico o Natural', size=1, readonly=True),
		'registro': fields.char('Reg-01', size=10, readonly=True),
		'total': fields.float('Total Compras', readonly=True, digits=(14,2)),
		"total_no_tax": fields.float('Exento Importacion', readonly=True, digits=(14,2)),
		"import_base": fields.float('Base Importacion', readonly=True, digits=(14,2)),
		"import_tax": fields.float('IVA Importacion', readonly=True, digits=(14,2)),
		"internal_base": fields.float('Base Interna', readonly=True, digits=(14,2)),
		"internal_tax": fields.float('IVA Interna', readonly=True, digits=(14,2))
	}

	def init(self, cr):
		print "#########----------EXECUTE ini---------#########"
		cr.execute("""
			CREATE OR REPLACE VIEW report_external_invoice_purchases_line AS (

				SELECT 
				ae.id AS id,
				ae.period_id,
				ae.date_invoice AS doc_date,
				ae.invoice_number AS doc_number,
				ae.control_number AS doc_control_number,
				'FACTURA AFECTADA'  AS fact_afectada,
				rp.name AS partner_name,
				rp.ref AS partner_rif ,
				UPPER(SUBSTRING(rp.ref from 1 for 1)) AS partner_type_custom,
				'01-REG' AS registro,
				ae.base + ae.no_tax + ae.tax_amount AS total,
				ae.no_tax AS total_no_tax,
				CASE WHEN ae.import=True THEN ae.base ELSE 0.0 END AS import_base,
				CASE WHEN ae.import= True THEN ae.tax_amount ELSE 0.0 END AS import_tax,
				CASE WHEN ae.import<>True THEN ae.base ELSE 0.0 END AS internal_base,
			 	CASE WHEN ae.import<>True THEN ae.tax_amount ELSE 0.0 END AS internal_tax

			 	FROM account_period AS ap
				INNER JOIN account_external_invoice ae
					ON ap.id= ae.period_id
				INNER JOIN res_partner AS rp
        			ON ae.partner_id = rp.id
				WHERE ae.type='in_invoice'

			)
			""")

report_external_invoice_purchases_line();