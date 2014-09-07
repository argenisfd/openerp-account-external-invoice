from report import report_sxw
from report.report_sxw import rml_parse

class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
    	print context
    	print "----*************-------------**************-------------"
        super(Parser, self).__init__(cr, uid, name, context)
        self.context = context
        self.localcontext.update({})