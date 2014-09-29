from osv import osv, fields, orm
import time
from tools.translate import _
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
	def _get_type(self, cr, uid, context=None):
		if context is None:
			context = {}
		return context.get('type', 'out_invoice')

	def _get_journal(self, cr, uid, context=None):
		if context is None:
			context = {}
		type_inv = context.get('type', 'out_invoice')
		user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
		company_id = context.get('company_id', user.company_id.id)
		type2journal = {'out_invoice': 'sale', 'in_invoice': 'purchase', 'out_refund': 'sale_refund', 'in_refund': 'purchase_refund'}
		journal_obj = self.pool.get('account.journal')
		res = journal_obj.search(cr, uid, [('type', '=', type2journal.get(type_inv, 'sale')),
											('company_id', '=', company_id)],
											limit=1)
		return res and res[0] or False
	_columns = {
		'type': fields.selection([('out_invoice','Venta'), ('in_invoice','Compra')], 'Sale / Buy', required=True, readonly=False, select=False, help='Si es de venta o compra'),
        'company_id': fields.many2one('res.company', 'Company', required=True, change_default=False, readonly=False),
		'doc_type': fields.selection( ( ('F', "FACTURA" ), 
										('NC', "NOTA DE CREDITO"),
										('ND',"NOTA DE DEBITO"),
										('RIV',"RETENCION DE IVA")
										)
		                             ,"Tipo Doc"),
		'invoice_number': fields.char('Nro. Factura', size=20, required=True),
		'control_number': fields.char('Nro. Control', size=20, required=False),
		'date_invoice': fields.date('Invoice Date', readonly=False, select=True, help="Fecha de la Factura"),
		'period_id': fields.many2one('account.period', 'Period', required=True, readonly=False),
		'journal_id': fields.many2one('account.journal', 'Journal', required=True, readonly=False ),
		'partner_id': fields.many2one('res.partner', 'Partner', change_default=True, readonly=False, required=True),
		'account_id' : fields.many2one('account.account', 'Account', required=True, ondelete="cascade"),
		'inverse_account_id' : fields.many2one('account.account', 'Inverse Account', required=True, ondelete="cascade"),
		'no_tax': fields.float('No Gravado', required=True, digits=(14,2), help='Monto sin derecho a credito fiscal'),
		'base': fields.float('BIG', required=True, digits=(14,4), help='Base Imponible'),
		'tax_id': fields.many2one('account.tax', 'Tax', help="The tax basis of the tax declaration.", required=True),
		'tax_amount': fields.float('Total IVA', required=True, digits=(14,2), help='Tax Amount'),
		'total_amount': fields.function(_cal_total_amount, digits=(14,2), string='Total Amount', store=False),
		'retention_amount': fields.float('Retention Amount', required=True, digits=(14,2), help='Monto de la Retencion'),
		'state': fields.selection([('pending_entry','Pendiente'), ('entry','Asentado')], 'State', required=True, readonly=True,help='Estatus en el que se ecuentra'),
		'import': fields.boolean('Importacion'),
		'reg': fields.char('Reg', size=8, required=True)

		#'total_amount': fields.float('Total', required=False, readonly=True digits=(14,4),  help='Total del Documento'),
		#'total_amount': fields.float('Total', required=False, readonly=True digits=(14,4),  help='Total del Documento'),
		}
		
	_order = "period_id"

	_defaults= {
		'type':_get_type,
		'state': 'pending_entry',
		'journal_id': _get_journal,
        'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'account.invoice', context=c),
        'doc_type': 'F',
        'import': False,
        'reg': "01-REG",
        'tax_amount': 0.00,
        'retention_amount': 0.00,
        'base': 0.00,
        'no_tax': 0.00

		}

	def onchange_iva(self, cr, uid, ids, base,no_tax, context=None):
		iva=0.00
		total=0.00
		iva=base*0.12
		total=base+iva+no_tax
		return {
				'value': {'tax_amount': iva, 'total_amount': total},
				'domain': {'tax_id': [("type_tax_use","=","purchase")] } }

	def onchange_total_iva(self, cr, uid, ids, base,tax_amount,no_tax, context=None):
		return {'value': { 'total_amount': base+tax_amount+no_tax } }

	def onchange_doc_type(self, rc, uid, ids, doc_type, context=None ):
		values={};
		if doc_type == 'RIV':
			values["base"]=0.00
			values["tax_amount"]=0.00
			values["total_amount"]=0.00
			values["no_tax"]=0.00
			values["control_number"]=""
		else:
			values["retention_amount"]=0.00

		return {'value': values}
		

	def onchange_partner_id(self, cr, uid, ids, partner_id,company_id,context=None):
		if context is None:
			context = {}
		values_ret={}
		user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
		company_id = context.get('company_id', user.company_id.id)
		type = context.get('type', 'out_invoice')
		acc_id = False
		if partner_id:
			p = self.pool.get('res.partner').browse(cr, uid, partner_id)
			#if len(p.ref) == 9:
			#	values_ret[""]
				 
			#print "----------------------"
			#print p.ref
			#print p.ref[0:1].upper()
			#print "*************************"
			if company_id:
				if p.property_account_receivable.company_id.id != company_id and p.property_account_payable.company_id.id != company_id:
					property_obj = self.pool.get('ir.property')
					rec_pro_id = property_obj.search(cr,uid,[('name','=','property_account_receivable'),('res_id','=','res.partner,'+str(partner_id)+''),('company_id','=',company_id)])
					pay_pro_id = property_obj.search(cr,uid,[('name','=','property_account_payable'),('res_id','=','res.partner,'+str(partner_id)+''),('company_id','=',company_id)])
					if not rec_pro_id:
						rec_pro_id = property_obj.search(cr,uid,[('name','=','property_account_receivable'),('company_id','=',company_id)])
					if not pay_pro_id:
						pay_pro_id = property_obj.search(cr,uid,[('name','=','property_account_payable'),('company_id','=',company_id)])
					rec_line_data = property_obj.read(cr,uid,rec_pro_id,['name','value_reference','res_id'])
					pay_line_data = property_obj.read(cr,uid,pay_pro_id,['name','value_reference','res_id'])
					rec_res_id = rec_line_data and rec_line_data[0].get('value_reference',False) and int(rec_line_data[0]['value_reference'].split(',')[1]) or False
					pay_res_id = pay_line_data and pay_line_data[0].get('value_reference',False) and int(pay_line_data[0]['value_reference'].split(',')[1]) or False
					if not rec_res_id and not pay_res_id:
						raise osv.except_osv(_('Configuration Error !'),
							_('Can not find a chart of accounts for this company, you should create one.'))
					account_obj = self.pool.get('account.account')
					rec_obj_acc = account_obj.browse(cr, uid, [rec_res_id])
					pay_obj_acc = account_obj.browse(cr, uid, [pay_res_id])
					p.property_account_receivable = rec_obj_acc[0]
					p.property_account_payable = pay_obj_acc[0]
			if type in ('out_invoice', 'out_refund'):
				acc_id = p.property_account_receivable.id
			else:
				acc_id = p.property_account_payable.id

		values_ret['account_id']=acc_id
		result = { 'value': values_ret }
		return result

	def create_movement(self, cr, uid, context=None, name=''):
		#return "Return de prueba para que no cree el movimientos mientras"
		if context is None:
			context = {}

		types = {'out_invoice': -1, 'in_invoice': 1}
		direction = types[context.get('type','')]
		ref= context.get('invoice_number')
		company_id=context.get('company_id')
		account_id=context.get('account_id')
		inverse_account_id=context.get('inverse_account_id')
		journal_id=context.get('journal_id')
		period_id = context.get('period_id')
		date_invoice = context.get('date_invoice')
		partner_id = context.get('partner_id')
		no_tax_amount=context.get('no_tax')
		base_amount=context.get('base')
		tax_amount=context.get('tax_amount')
		tax_id=context.get('tax_id');
		total_amount=base_amount+tax_amount+no_tax_amount
		move_obj = self.pool.get('account.move'),
		tax_obj = self.pool.get('account.tax').browse(cr, uid, tax_id, context=None);
		l1 = {
			'debit': direction * total_amount<0 and - direction * total_amount,
			'credit': direction * total_amount>0 and direction * total_amount,
			'name': ref,
			'ref':ref,
			'account_id': inverse_account_id,
			'partner_id': partner_id,
			'date': date_invoice,
			'currency_id':None,
			#'amount_currency':total_amount and direction * total_amount or 0.0,
			'company_id': company_id,
		}
		
		l2 = {
			'debit': direction * tax_amount>0 and direction * tax_amount,
			'credit': direction * tax_amount<0 and - direction * tax_amount,
			'name': tax_obj.name,
			'ref':ref,
			'account_id': tax_obj.account_paid_id.id,
			#'account_tax_id': tax_obj.id,
			'tax_code_id':tax_obj.tax_code_id.id,
			'tax_amount': tax_amount,
			'partner_id': partner_id,
			'date': date_invoice,
			'currency_id':None,
			#'amount_currency':total_amount and direction * total_amount or 0.0,
			'company_id': company_id,
		}
		#lines = [(0, 0, l1), (0, 0, l2)]
		lines =  [(0, 0, l1), (0, 0, l2)]
		if no_tax_amount>0:
			l3 = {
				'debit': direction * no_tax_amount>0 and direction * no_tax_amount,
				'credit': direction * no_tax_amount<0 and - direction * no_tax_amount,
				'name': ref,
				'ref':ref,
				'account_id': account_id,
				'partner_id': partner_id,
				'date': date_invoice,
				'currency_id':None,
				#'amount_currency':total_amount and direction * total_amount or 0.0,
				'company_id': company_id,
			}
			lines.append((0,0,l3));

		if base_amount>0:
			l4 = {
				'debit': direction * base_amount>0 and direction * base_amount,
				'credit': direction * base_amount<0 and - direction * base_amount,
				'name': ref,
				'ref':ref,
				'account_id': account_id,
				'partner_id': partner_id,
				'date': date_invoice,
				'currency_id':None,
				'tax_amount': base_amount,
				'tax_code_id': tax_obj.base_code_id.id,
				#'amount_currency':total_amount and direction * total_amount or 0.0,
				'company_id': company_id,
			}
			lines.append((0,0,l4));

		

		
		move = {
				'name': ref,
				'ref': ref,
				'company_id': company_id,
				'journal_id': journal_id,
				'period_id':  period_id,
				'narration':  "Factura de prueba",
				'date': 	  date_invoice,
				'line_id': 	  lines,
				'partner_id': partner_id,
				'to_check':   True,
			}
		

		print move
		self.pool.get("account.move").create(cr, uid, move, context=context)
		print "move is created";
		return True


	def create_account_movement(self, cr, uid, ids, context=None):
		doc = self.browse(cr, uid, ids, context=context)[0]
		
		if context is None:
			context = {}

		lines =  self.get_movements_lines(doc)
		ref= doc.invoice_number

		move = {
				'name': ref,
				'ref': ref,
				'company_id': doc.company_id.id,
				'journal_id': doc.journal_id.id,
				'period_id':  doc.period_id.id,
				'narration':  "Factura de prueba",
				'date': 	  doc.date_invoice,
				'line_id': 	  lines,
				'partner_id': doc.partner_id.id,
				'to_check':   True,
			}
		print move;
		self.pool.get("account.move").create(cr, uid, move, context=context)
		self.write( cr, uid, ids, {"state": "entry" }, context=context)
		return True


	def get_movements_lines( self, doc ):
		doc_type_behavior={}
		if doc.type == 'in_invoice' :
			doc_type_behavior= {'F': [-1, 'amount','-amount'], 'NC': [1,'-amount','amount'], 'ND': [-1,'amount','-amount'], 'RIV': [1,'-amount','-amount'] }
			return self.get_dynamic_movements_lines(doc,{'doc_type_behavior': doc_type_behavior }) 
		if doc.type == 'out_invoice':
			doc_type_behavior= {'F': [-1, 'amount','-amount'], 'NC': [1,'-amount','amount'], 'ND': [-1,'amount','-amount'], 'RIV': [1,'-amount','-amount'] }
			return self.get_dynamic_movements_lines(doc, {'doc_type_behavior': doc_type_behavior })
		return False

	def get_dynamic_movements_lines(self, doc, params):
		doc_type_behavior= params['doc_type_behavior']
		direction = doc_type_behavior[doc.doc_type][0]
		ref= doc.invoice_number
		lines=[]

		amounts={"amount": self.get_total_without_tax(doc),
				"-amount": self.get_total_conciliation(doc) }


		lmain_amount=amounts[doc_type_behavior[doc.doc_type][1]]
		lconciliation_ammount=amounts[doc_type_behavior[doc.doc_type][2]]
		l_main = {
			'debit': lmain_amount,
			'credit': False,
			'name': ref,
			'ref':ref,
			'account_id': doc.account_id.id,
			'partner_id': doc.partner_id.id,
			'date': doc.date_invoice,
			'currency_id':None,
			#'amount_currency':total_amount and direction * total_amount or 0.0,
			'company_id': doc.company_id.id,
		}
		lines.append((0,0,l_main))
		tax_amount= self.get_total_tax_amount(doc)
		if tax_amount > 0 :
			l_tax={
				'debit': direction * tax_amount<0 and - direction * tax_amount,
				'credit': direction * tax_amount>0 and  direction * tax_amount,
				'name': doc.tax_id.name,
				'ref':ref,
				'account_id': doc.tax_id.account_paid_id.id,
				#'account_tax_id': tax_obj.id,
				'tax_code_id':doc.tax_id.tax_code_id.id,
				'tax_amount': tax_amount,
				'partner_id': doc.partner_id.id,
				'date': doc.date_invoice,
				'currency_id':None,
				#'amount_currency':total_amount and direction * total_amount or 0.0,
				'company_id': doc.company_id.id,
			}
			lines.append((0,0,l_tax))
		# la cuenta que cuadra
		
		
		l_conciliation_account= {
			'debit': False,
			'credit': lconciliation_ammount,
			'name': ref,
			'ref':ref,
			'account_id': doc.inverse_account_id.id,
			'partner_id': doc.partner_id.id,
			'date': doc.date_invoice,
			'currency_id':None,
			#'amount_currency':total_amount and direction * total_amount or 0.0,
			'company_id': doc.company_id.id,
		}
		lines.append((0,0,l_conciliation_account))
		return lines

	def get_movements_lines_purchases(self, doc):
		doc_types = {'F': [-1, 'amount','-amount'], 'NC': [1,'-amount','amount'], 'ND': [-1,'amount','-amount'], 'RIV': [1,'-amount','-amount'] }
		direction = doc_types[doc.doc_type][0]
		ref= doc.invoice_number
		lines=[]

		amounts={"amount": self.get_total_without_tax(doc),
				"-amount": self.get_total_conciliation(doc) }


		lmain_amount=amounts[doc_types[doc.doc_type][1]]
		lconciliation_ammount=amounts[doc_types[doc.doc_type][2]]
		l_main = {
			'debit': lmain_amount,
			'credit': False,
			'name': ref,
			'ref':ref,
			'account_id': doc.account_id.id,
			'partner_id': doc.partner_id.id,
			'date': doc.date_invoice,
			'currency_id':None,
			#'amount_currency':total_amount and direction * total_amount or 0.0,
			'company_id': doc.company_id.id,
		}
		lines.append((0,0,l_main))
		tax_amount= self.get_total_tax_amount(doc)
		if tax_amount > 0 :
			l_tax={
				'debit': direction * tax_amount<0 and - direction * tax_amount,
				'credit': direction * tax_amount>0 and  direction * tax_amount,
				'name': doc.tax_id.name,
				'ref':ref,
				'account_id': doc.tax_id.account_paid_id.id,
				#'account_tax_id': tax_obj.id,
				'tax_code_id':doc.tax_id.tax_code_id.id,
				'tax_amount': tax_amount,
				'partner_id': doc.partner_id.id,
				'date': doc.date_invoice,
				'currency_id':None,
				#'amount_currency':total_amount and direction * total_amount or 0.0,
				'company_id': doc.company_id.id,
			}
			lines.append((0,0,l_tax))
		# la cuenta que cuadra
		
		
		l_conciliation_account= {
			'debit': False,
			'credit': lconciliation_ammount,
			'name': ref,
			'ref':ref,
			'account_id': doc.inverse_account_id.id,
			'partner_id': doc.partner_id.id,
			'date': doc.date_invoice,
			'currency_id':None,
			#'amount_currency':total_amount and direction * total_amount or 0.0,
			'company_id': doc.company_id.id,
		}
		lines.append((0,0,l_conciliation_account))
		return lines



	def get_total_without_tax(self, doc):
		return doc.base + doc.no_tax + doc.retention_amount

	def get_total_tax_amount(self, doc):
		return doc.tax_amount

	def get_total_conciliation(self, doc):
		return self.get_total_without_tax(doc) + self.get_total_tax_amount(doc)


	def create(self, cr, uid, vals, context=None):
		if context is None:
			context = {}
		res = super(account_external_invoice, self).create(cr, uid,vals, context=context)
		to_move_ctx=context.copy();
		to_move_ctx.update(vals)
		#self.create_movement(cr, uid, context=to_move_ctx, name='')
		return res
		try:
			print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
			res = super(account_external_invoice, self).create(cr, uid,vals, context=context)
			to_move_ctx=context.copy();
			to_move_ctx.update(vals)
			self.create_movement(cr, uid, context=to_move_ctx, name='')
			"""for inv_id, name in self.name_get(cr, uid, [res], context=context):
				ctx = context.copy()
				if vals.get('type', 'in_invoice') in ('out_invoice', 'out_refund'):
					ctx = self.get_log_context(cr, uid, context=ctx)
				message = _("Invoice '%s' is waiting for validation.") % name
				self.log(cr, uid, inv_id, message, context=ctx)"""
			return res
		except Exception, e:
			print vars(e)
			if '"journal_id" viol' in e.args[0]:
				raise orm.except_orm(_('Configuration Error!'),
					_('There is no Accounting Journal of type Sale/Purchase defined!'))
			else:
				raise orm.except_orm(_('Unknown Error'), str(e))
"""
            name character varying(64) NOT NULL, -- Number
  state character varying NOT NULL, -- State
  ref character varying(64), -- Reference
  company_id integer, -- Company
  journal_id integer NOT NULL, -- Journal
  period_id integer NOT NULL, -- Period
  narration text, -- Internal Note
  date date NOT NULL, -- Date
  balance numeric, -- balance
  partner_id integer, -- Partner
  to_check boolean, -- To Review"""
"""l1 = {
	'debit': direction * self.total_amount>0 and direction * self.total_amount,
	'credit': direction * self.total_amount<0 and - direction * self.total_amount,
	'account_id': src_account_id,
	'partner_id': self.account_id,
	'ref':ref,
	'date': self.date_invoice,
	'currency_id':currency_id,
	'amount_currency':self.total_amount and direction * amount_currency or 0.0,
	'company_id': self.company_id,
}

l2 = {
	'debit': direction * self.total_amount<0 and - direction * self.total_amount,
	'credit': direction * self.total_amount>0 and direction * self.total_amount,
	'account_id': pay_account_id,
	'partner_id': self.partner_id,
	'ref':ref,
	'date': self.date_invoice,
	'currency_id':currency_id,
	'amount_currency':amount_currency and - direction * amount_currency or 0.0,
	'company_id': invoice.company_id.id,


}"""
	

account_external_invoice()




"""[(0, 0, {'currency_id': None, 'credit': 100.0,  'debit': False, 'ref': u'OMAL-COMP-NC2', 'company_id': 1, 'account_id': 78}), 
 (0, 0, { 'tax_amount': 6.0,  'credit': 6.0,    'debit': False, 'ref': u'OMAL-COMP-NC2'}), 
 (0, 0, {'currency_id': None, 'credit': False,  'debit': 106.0, 'ref': u'OMAL-COMP-NC2', 'company_id': 1, 'account_id': 47})]
"""

[(0, 0, {'currency_id': None, 'credit': 100.0, 'debit': 0, 'date': '2014-09-09', 'partner_id': 4, 'ref': u'OMAL-COMP-F1', 'company_id': 1, 'account_id': 47}), 
 (0, 0, {'tax_amount': 6.0,   'credit': False, 'debit': 6.0, 'ref': u'OMAL-COMP-F1'}), 
 (0, 0, {'currency_id': None, 'credit': 0,     'debit': 106.0, 'date': '2014-09-09', 'partner_id': 4, 'ref': u'OMAL-COMP-F1', 'company_id': 1, 'account_id': 78})]