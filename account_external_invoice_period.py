from osv import osv, fields, orm
import time
from tools.translate import _
class  account_external_invoice_period(osv.osv):
	_name = "account.period"
	_inherit= "account.period"
	_columns={
		"external_invoice_line": fields.one2many('account.external.invoice','period_id', "External Invoices"),
		"report_purchases_line": fields.one2many('report.external.invoice.purchases.line','period_id', "Reporte de Ventas")
	}
account_external_invoice_period()