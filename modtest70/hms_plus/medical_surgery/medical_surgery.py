from osv import fields, osv


class surgery (osv.osv):
	_name = "medical.surgery"
	_description = "Surgery"
	_columns = {
		'name' : fields.many2one ('medical.procedure','Code', help="Procedure Code, for example ICD-10-PCS Code 7-character string"),
		'pathology' : fields.many2one ('medical.pathology','Base condition', help="Base Condition / Reason"),
		'classification' : fields.selection ([
				('o','Optional'),
				('r','Required'),
				('u','Urgent'),
                                ], 'Surgery Classification', select=True),
		'surgeon' : fields.many2one('medical.physician','Surgeon', help="Surgeon who did the procedure"),
		'date': fields.datetime ('Date of the surgery'),
		'age': fields.char ('Patient age',size=3,help='Patient age at the moment of the surgery. Can be estimative'),
		'description' : fields.char ('Description', size=128),
		'extra_info' : fields.text ('Extra Info'),
		}

surgery()

# Add to the Medical patient_data class (medical.patient) the surgery field.

class medical_patient (osv.osv):
	_name = "medical.patient"
	_inherit = "medical.patient"
	_columns = {
		'surgery' : fields.many2many ('medical.surgery', 'patient_surgery_rel','patient_id','surgery_id', 'Surgeries'),
		
	}
medical_patient ()




