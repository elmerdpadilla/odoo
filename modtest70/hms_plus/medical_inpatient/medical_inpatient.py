import time
from mx import DateTime
import datetime
from osv import fields, osv
from tools.translate import _

import sys


class inpatient_registration (osv.osv):

	
# Method to check for availability and make the hospital bed reservation

	def registration_confirm(self, cr, uid, ids, context={}):
		for reservation in self.browse(cr,uid,ids):
			bed_id= str(reservation.bed.id)
			cr.execute("select count (*) from medical_inpatient_registration where (hospitalization_date::timestamp,discharge_date::timestamp) overlaps ( timestamp %s , timestamp %s ) and state= %s and bed = cast(%s as integer)", (reservation.hospitalization_date,reservation.discharge_date,'confirmed',bed_id))
			res = cr.fetchone()
	
		if res[0] > 0:
			raise osv.except_osv('Warning', 'Bed has been already reserved in this period' ) 
		else:
			self.write(cr, uid, ids, {'state':'confirmed'})
		return True

	def patient_discharge(self, cr, uid, ids, context={}):
		self.write(cr, uid, ids, {'state':'free'})
		return True

	def registration_cancel(self, cr, uid, ids, context={}):
		self.write(cr, uid, ids, {'state':'cancelled'})
		return True

	def registration_admission(self, cr, uid, ids, context={}):
		self.write(cr, uid, ids, {'state':'hospitalized'})
		return True

	_name = "medical.inpatient.registration"
	_description = "Patient admission History"
	_columns = {
		'name' : fields.char ('Registration Code',size=128),
		'patient' : fields.many2one ('medical.patient','Patient'),
		'admission_type' : fields.selection([('routine','Routine'),('maternity','Maternity'),('elective','Elective'),('urgent','Urgent'),('emergency','Emergency')],'Admission type'),
		'hospitalization_date' : fields.datetime ('Hospitalization date'),
		'discharge_date' : fields.datetime ('Discharge date'),
		'attending_physician' : fields.many2one ('medical.physician','Attending Physician'),
		'operating_physician' : fields.many2one ('medical.physician','Operating Physician'),
		'admission_reason' : fields.many2one ('medical.pathology','Reason for Admission', help="Reason for Admission"),
		'bed' : fields.many2one ('medical.hospital.bed','Hospital Bed'),
		'nursing_plan' : fields.text ('Nursing Plan'),
		'discharge_plan' : fields.text ('Discharge Plan'),

		'info' : fields.text ('Extra Info'),
		'state': fields.selection((('free','Free'),('cancelled','Cancelled'),('confirmed','Confirmed'),('hospitalized','Hospitalized')),'Status'),
		}

	_defaults = {
		'name': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'medical.inpatient.registration'),
		'state': lambda *a : 'free'
	}
	_sql_constraints = [
                ('name_uniq', 'unique (name)', 'The Registration code already exists')]

inpatient_registration ()
	

class appointment (osv.osv):
	_name = "medical.appointment"
	_inherit = "medical.appointment"
	_columns = {
			'inpatient_registration_code' : fields.many2one ('medical.inpatient.registration','Inpatient Registration',help="Enter the patient hospitalization code"),
	}

appointment ()


# Add the patient status to the partner

class patient_data (osv.osv):

	_name = "medical.patient"
	_inherit = "medical.patient"
	_description = "Patient related information"

	def _get_patient_status (self, cr, uid, ids,name, arg, context={}):

		def get_hospitalization_status (patient_dbid):

			cr.execute ( 'select state from medical_inpatient_registration where patient=%s and state=\'hospitalized\'', (patient_dbid,))  


			try:
				patient_status = str(cr.fetchone()[0])
			except:
				patient_status = "outpatient"

			return patient_status

		result={}

# Get the patient (DB) id to be used in the search on the medical inpatient registration table lookup

	        for patient_data in self.browse(cr, uid, ids, context=context):
			patient_dbid = patient_data.id

			if patient_dbid:
	        		result[patient_data.id] = get_hospitalization_status (patient_dbid)
	        return result


	_columns = {
		'patient_status': fields.function(_get_patient_status, method=True, type='char', string='Hospitalization Status', help="Shows whether the patient is hospitalized"),
		 
		    }



patient_data ()


