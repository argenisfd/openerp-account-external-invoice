from osv import fields, osv
from tools.translate import _
from lxml import etree
class validate_account_move (osv.osv_memory):
	_name = "validate.account.move"
	_inherit = "validate.account.move"

	def  fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
		if context is None:
			context = {}

		res = super(validate_account_move,self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
		if view_type =="form":
			defaultCompany=self.pool.get('res.company')._company_default_get(cr, uid, 'account.invoice', context=context)
			doc = etree.XML(res['arch'])
			for node in doc.xpath("//field[@name='journal_id']"):
				domain = node.get('domain')
				if not domain:
					domain=""
				domain=domain.strip(" ") 
				if len(domain)>0:
					domain=domain[:-1]
					domain=domain+",('company_id', '=', "+str(defaultCompany)+")]"
				else:
					domain="[('company_id', '=', "+str(defaultCompany)+")]"
				node.set('domain', domain)
			for node in doc.xpath("//field[@name='period_id']"):
				domain = node.get('domain')
				if not domain:
					domain=""
				domain=domain.strip(" ")
				if len(domain)>0:
					domain=domain[:-1]
					domain=domain+",('company_id', '=', "+str(defaultCompany)+")]"
				else:
					domain="[('company_id', '=', "+str(defaultCompany)+")]"
				node.set('domain', domain)				
			res['arch'] = etree.tostring(doc)
			
		return res
validate_account_move()