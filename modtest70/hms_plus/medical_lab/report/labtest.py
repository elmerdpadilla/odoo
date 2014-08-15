import time
import datetime
from report import report_sxw
from osv import fields, osv
from tools.translate import _

class labtest_report(report_sxw.rml_parse):
        _name = 'report.patient.labtest'
        def __init__(self, cr, uid, name, context):
            super(labtest_report, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({
                'time': time,
                'get_test': self._get_test,
                'get_doctor' : self.get_doctor,
            })
            
        def _get_test(self, patient, ids={}):
            doctor_id = self.get_doctor_id()            
            if doctor_id:                
                test_ids = self.pool.get('medical.patient.lab.test').search(self.cr, self.uid, [('doctor_id','=',doctor_id),('patient_id','=',patient.id),('state','=','draft')])
                if test_ids:
                    return self.pool.get('medical.patient.lab.test').browse(self.cr, self.uid, test_ids)
            return []

        def get_doctor_id(self):            
            partner_id = self.pool.get('res.partner').search(self.cr,self.uid,[('user_id','=',self.uid)])
            if partner_id:
                physician_id = self.pool.get('medical.physician').search(self.cr, self.uid, [('name','in',partner_id)])                
                if physician_id:
                    return physician_id[0]
            return False

        def get_doctor(self):
            partner_id = self.pool.get('res.partner').search(self.cr,self.uid,[('user_id','=',self.uid)])
            if partner_id:
                return self.pool.get('res.partner').read(self.cr, self.uid, partner_id, ['name'])[0]['name']
            else:
                return ''        

report_sxw.report_sxw('report.patient.labtest', 'medical.patient', 'addons/hms_plus/medical_lab/report/labtest.rml', parser=labtest_report, header=False)