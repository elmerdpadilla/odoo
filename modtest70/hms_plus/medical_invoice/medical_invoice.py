from osv import fields, osv
from tools.translate import _
from mx import DateTime
import datetime
import time

class patient_data (osv.osv):
	_name = "medical.patient"
	_inherit = "medical.patient"

	_columns = {
		'receivable' : fields.related('name','credit',type='float',string='Receivable',help='Total amount this patient owes you',readonly=True),
	}
patient_data()

# Add Invoicing information to the Appointment

class appointment (osv.osv):
	_name = "medical.appointment"
	_inherit = "medical.appointment"

	def copy(self, cr, uid, id, default=None, context={}):
		default.update({'validity_status':'tobe'})
		return super(appointment,self).copy(cr, uid, id, default, context)

	def onchange_appointment_date(self, cr, uid, ids, apt_date):
		if apt_date:
			validity_date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(apt_date,"%Y-%m-%d %H:%M:%S")))
			validity_date = validity_date+datetime.timedelta(days=7)
			v = {'appointment_validity_date':str(validity_date)}
			return {'value': v}
		return {}

	_columns = {
		'no_invoice' : fields.boolean ('Invoice exempt'),
		'appointment_validity_date' : fields.datetime ('Validity Date'),
		'validity_status' : fields.selection([('invoiced','Invoiced'),('tobe','To be Invoiced')],'Status'),
		'consultations' : fields.many2one ('product.product', 'Consultation Service', domain=[('type', '=', "service")], help="Consultation Services", required=True),
	}
	_defaults = {
		'validity_status': lambda *a: 'tobe',
		'no_invoice': lambda *a: False
	}

appointment ()

# Add Invoicing information to the Lab Test

class labtest (osv.osv):
	_name = "medical.patient.lab.test"
	_inherit = "medical.patient.lab.test"

	_columns = {
		'no_invoice' : fields.boolean ('Invoice exempt'),
		'invoice_status' : fields.selection([('invoiced','Invoiced'),('tobe','To be Invoiced')],'Invoice Status'),
        }

	_defaults={
		'invoice_status': lambda *a: 'tobe',
		'no_invoice': lambda *a: False
	   }
labtest()

class patient_prescription_order (osv.osv):

	_name = "medical.prescription.order"
	_inherit = "medical.prescription.order"

		
	_columns = {
		'no_invoice' : fields.boolean ('Invoice exempt'),
		'invoice_status' : fields.selection([('invoiced','Invoiced'),('tobe','To be Invoiced')],'Invoice Status'),
		}

	_defaults = {
		'invoice_status': lambda *a: 'tobe',
		'no_invoice': lambda *a: False
     }
patient_prescription_order ()