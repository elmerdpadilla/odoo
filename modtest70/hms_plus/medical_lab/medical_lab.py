import time
from mx import DateTime
import datetime
from osv import fields, osv
from tools.translate import _

# Add Lab test information to the Patient object

class patient_data (osv.osv):
	_name = "medical.patient"
	_inherit = "medical.patient"

	def name_get(self, cr, uid, ids, context={}):
		if not len(ids):
			return []
		rec_name = 'name'
		res = [(r['id'], r[rec_name][1]) for r in self.read(cr, uid, ids, [rec_name], context)]
		return res
		
	def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=80):
		if not args:
			args=[]
		if not context:
			context={}
		if name:
			ids = self.search(cr, user, [('patient_id','=',name)]+ args, limit=limit, context=context)
			if not len(ids):
				ids += self.search(cr, user, [('name',operator,name)]+ args, limit=limit, context=context)
		else:
			ids = self.search(cr, user, args, limit=limit, context=context)
		result = self.name_get(cr, user, ids, context)
		return result        

	_columns = {
		'lab_test_ids': fields.one2many('medical.patient.lab.test','patient_id','Lab Tests Required'),
		}

patient_data ()    

class test_type (osv.osv):
	_name = "medical.test_type"
	_description = "Type of Lab test"
	_columns = {
		'name' : fields.char ('Test',size=128,help="Test type, eg X-Ray, hemogram,biopsy..."),
		'code' : fields.char ('Code',size=128,help="Short name - code for the test"),
		'info' : fields.text ('Description'),
        'product_id' : fields.many2one('product.product', 'Service', required=True),
        'critearea': fields.one2many('medical_test.critearea','test_type_id','Test Cases'),
	}
	_sql_constraints = [
                ('code_uniq', 'unique (name)', 'The Lab Test code must be unique')]

test_type ()

class lab (osv.osv):
	_name = "medical.lab"
	_description = "Lab Test"
	_columns = {
		'name' : fields.char ('ID', size=128, help="Lab result ID"),
		'test' : fields.many2one ('medical.test_type', 'Test type', help="Lab test type"),
		'patient' : fields.many2one ('medical.patient', 'Patient', help="Patient ID"), 
		'pathologist' : fields.many2one ('medical.physician','Pathologist',help="Pathologist"),
		'requestor' : fields.many2one ('medical.physician', 'Physician', help="Doctor who requested the test"),
		'results' : fields.text ('Results'),
		'diagnosis' : fields.text ('Diagnosis'),
		'critearea': fields.one2many('medical_test.critearea','medical_lab_id','Test Cases'),
		'date_requested' : fields.datetime ('Date requested'),
		'date_analysis' : fields.datetime ('Date of the Analysis'),        
	}
	_defaults = {
        'date_requested': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'date_analysis': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'name' : lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'medical.lab'),         
    }
	_sql_constraints = [
                ('id_uniq', 'unique (name)', 'The test ID code must be unique')]
lab ()



class medical_lab_test_units(osv.osv):
	_name = "medical.lab.test.units"
	_columns = {
        'name' : fields.char('Unit', size=25),
        'code' : fields.char('Code', size=25),
        }
	_sql_constraints = [
            ('name_uniq', 'unique(name)', 'The Unit name must be unique')]
medical_lab_test_units()

class medical_test_critearea(osv.osv):
	_name = "medical_test.critearea"
	_description = "Lab Test Critearea"    
	_columns ={
       'name' : fields.char('Test', size=64),
       'result' : fields.text('Result'),
       'normal_range' : fields.text('Normal Range'),
       'units' : fields.many2one('medical.lab.test.units', 'Units'),
       'test_type_id' : fields.many2one('medical.test_type','Test type'),
       'medical_lab_id' : fields.many2one('medical.lab','Test Cases'),
       'sequence' : fields.integer('Sequence'),       
       }
	_defaults = {
         'sequence' : lambda *a : 1,        
         }
	_order="sequence"
medical_test_critearea()

class medical_patient_lab_test(osv.osv):
	_name = 'medical.patient.lab.test'
	def _get_default_dr(self, cr, uid, context={}):
		partner_id = self.pool.get('res.partner').search(cr,uid,[('user_id','=',uid)])
		if partner_id:
			dr_id = self.pool.get('medical.physician').search(cr,uid,[('name','=',partner_id[0])])
			if dr_id:
				return dr_id[0]
			#else:
			#    raise osv.except_osv(_('Error !'),
			#            _('There is no physician defined ' \
			#                    'for current user.'))
		else:
			return False
		
	_columns = {
        'name' : fields.many2one('medical.test_type','Test Type'),
        'date' : fields.datetime('Date'),
        'state' : fields.selection([('draft','Draft'),('tested','Tested'),('cancel','Cancel')],'State',readonly=True),
        'patient_id' : fields.many2one('medical.patient','Patient'),
        'doctor_id' : fields.many2one('medical.physician','Doctor', help="Doctor who Request the lab test."), 
		#'invoice_status' : fields.selection([('invoiced','Invoiced'),('tobe','To be Invoiced'),('no','No Invoice')],'Invoice Status'),
        }

	_defaults={
       'date' : lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
       'state' : lambda *a : 'draft',
       'doctor_id' : _get_default_dr,        
	   #'invoice_status': lambda *a: 'tobe',
       }
medical_patient_lab_test()