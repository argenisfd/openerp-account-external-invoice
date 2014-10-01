from osv import osv, fields, orm
import time
class account_external_invoice_confirm(osv.osv_memory):
    """
    This wizard will confirm the all the selected draft invoices
    """

    _name = "account.external.invoice.confirm"
    _description = "Confirm the selected invoices"

    def create_movement_confirm(self, cr, uid, ids, context=None):
        external_invoices=self.pool.get("account.external.invoice").browse(cr, uid, context.get("active_ids"))
        for doc in external_invoices:
            if doc.state not in ("entry"):
                self.pool.get("account.external.invoice").create_account_movement(cr, uid, [doc.id] , context=None)
            else:
                print "noooo"
        return {'type': 'ir.actions.act_window_close'}

        wf_service = netsvc.LocalService('workflow')
        if context is None:
            context = {}
        pool_obj = pooler.get_pool(cr.dbname)
        data_inv = pool_obj.get('account.invoice').read(cr, uid, context['active_ids'], ['state'], context=context)

        for record in data_inv:
            if record['state'] not in ('draft','proforma','proforma2'):
                raise osv.except_osv(_('Warning'), _("Selected Invoice(s) cannot be confirmed as they are not in 'Draft' or 'Pro-Forma' state!"))
            wf_service.trg_validate(uid, 'account.invoice', record['id'], 'invoice_open', cr)
        return {'type': 'ir.actions.act_window_close'}

account_external_invoice_confirm()