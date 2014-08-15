import logging

from osv import fields, osv
import pooler
from tools.translate import _

logging.basicConfig(level=logging.DEBUG)

class make_medical_appointment_invoice(osv.osv_memory):
	_name="medical.appointment.invoice"

	def create_invoice(self, cr, uid, ids, context={}):
		invoice_obj = self.pool.get('account.invoice')
		appointment_obj = self.pool.get('medical.appointment')

		apps = context.get ('active_ids')
		pats = []
		for app_id in apps:
			pats.append(appointment_obj.browse( cr, uid, app_id).patient.name.id)

		if pats.count(pats[0]) == len(pats):
			invoice_data={}
			for app_id in apps:
				appointment = appointment_obj.browse( cr, uid, app_id)

# Check if the appointment is invoice exempt, and stop the invoicing process
				if appointment.no_invoice :
					raise  osv.except_osv(_('UserError'), _('The appointment is invoice exempt'))				

				if appointment.validity_status=='invoiced':
					if len(apps) > 1:
						raise  osv.except_osv(_('UserError'),_('At least one of the selected appointments is already invoiced'))
					else:
						raise  osv.except_osv(_('UserError'),_('Appointment already invoiced'))
				if appointment.validity_status=='no':
					if len(apps) > 1:
						raise  osv.except_osv(_('UserError'),_('At least one of the selected appointments can not be invoiced'))
					else:
						raise  osv.except_osv(_('UserError'),_('You can not invoice this appointment'))

			if appointment.patient.name.id:
				invoice_data['partner_id'] = appointment.patient.name.id
				res = self.pool.get('res.partner').address_get(cr, uid, [appointment.patient.name.id], ['contact', 'invoice'])
				invoice_data['address_contact_id'] = res['contact']
				invoice_data['address_invoice_id'] = res['invoice']
				invoice_data['account_id'] = appointment.patient.name.property_account_receivable.id
				invoice_data['fiscal_position'] = appointment.patient.name.property_account_position and appointment.patient.name.property_account_position.id or False
				invoice_data['payment_term'] = appointment.patient.name.property_payment_term and appointment.patient.name.property_payment_term.id or False

			prods_data = {}
			for app_id in apps:
				appointment = appointment_obj.browse( cr, uid, app_id)
				logging.debug('appointment = %s; appointment.consultations = %s', appointment, appointment.consultations)
				if appointment.consultations:
					logging.debug('appointment.consultations = %s; appointment.consultations.id = %s', appointment.consultations, appointment.consultations.id)
					if prods_data.has_key(appointment.consultations.id):
						prods_data[appointment.consultations.id]['quantity'] += 1
					else:
						a = appointment.consultations.product_tmpl_id.property_account_income.id
						if not a:
							a = appointment.consultations.categ_id.property_account_income_categ.id
						prods_data[appointment.consultations.id] = {'product_id':appointment.consultations.id,
										'name':appointment.consultations.name,
										'quantity':1,
										'account_id':a,
										'price_unit':appointment.consultations.lst_price}
				else:
					raise osv.except_osv(_('UserError'),_('No consultation service is connected with the selected appointments'))

			product_lines = []
			for prod_id, prod_data in prods_data.items():
				product_lines.append((0,0,{'product_id':prod_data['product_id'],
						'name':prod_data['name'],
						'quantity':prod_data['quantity'],
						'account_id':prod_data['account_id'],
						'price_unit':prod_data['price_unit']}))
				
			invoice_data['invoice_line'] = product_lines
			invoice_id = invoice_obj.create(cr, uid, invoice_data)
			
			appointment_obj.write(cr, uid, apps, {'validity_status':'invoiced'})

			return {
				'domain': "[('id','=', "+str(invoice_id)+")]",
				'name': 'Create invoice',
				'view_type': 'form',
				'view_mode': 'tree,form',
				'res_model': 'account.invoice',
				'type': 'ir.actions.act_window'
			}

		else:
			raise  osv.except_osv(_('UserError'),_('When multiple appointments are selected, patient must be the same'))

make_medical_appointment_invoice()

