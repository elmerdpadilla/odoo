import time

from openerp.report import report_sxw

class new_born_card(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(new_born_card, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
        })

report_sxw.report_sxw('report.newborn.card','medical.newborn','addons/hms_plus/medical_pediatrics/report/new_born_card.rml',parser=new_born_card,header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
