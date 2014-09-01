
import wizard

class wizard_print_period_report (wizard.interface):
	form = """<?xml version="1.0"?>
	<form title="Reconciliation">
	<separator string="Reconciliation transactions" colspan="4"/>
	<field name="trans_nbr"/>
	<newline/>
	<field name="credit"/>
	<field name="debit"/>
	<field name="state"/>
	<separator string="Write-Off" colspan="4"/>
	<field name="writeoff"/>
	<newline/>
	<field name="writeoff_acc_id" colspan="3"/>
	</form>
"""
	_transaction_fields = {
	'trans_nbr': {'string':'# of Transaction', 'type':'integer', 'readonly':True},
	'credit': {'string':'Credit amount', 'type':'float', 'readonly':True},
	'debit': {'string':'Debit amount', 'type':'float', 'readonly':True},
	'state': {
		'string':"Date/Period Filter",
		'type':'selection',
		'selection':[('bydate','By Date'),
		('byperiod','By Period'),
		('all','By Date and Period'),
		('none','No Filter')],
		'default': lambda *a:'none'
		},
	'writeoff': {'string':'Write-Off amount', 'type':'float', 'readonly':True},
	'writeoff_acc_id': {'string':'Write-Off account',
		'type':'many2one',
		'relation':'account.account'
		}
	}
	def _trans_rec_get(self, uid, data, res_get=False):
		print "Hola";
	_transction_form ="HOla"
	_trans_rec_reconcile="Hola2"
	states= {
		'init':{
			'actions':[_trans_rec_get],
			'result': { 'type':'form',
						'arch': _transction_form,
						'fields': _transaction_fields,
						'state': [('rencile','Reconcile'),('end','Cancel')]
			}
		},
		'reconcile': {
			'actions': [_trans_rec_reconcile],
			'result': {'type':'state', 'state': 'end'}
		}
	}
	
wizard_print_period_report('account.move.line.reconcile')