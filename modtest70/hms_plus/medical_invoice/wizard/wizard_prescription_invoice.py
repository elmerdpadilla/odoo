import logging

from osv import fields, osv
import pooler
from tools.translate import _


logging.basicConfig(level=logging.DEBUG)


class make_medical_prescription_invoice(osv.osv_memory):
	_name="medical.prescription.invoice"

	def create_prescription_invoice(self, cr, uid, ids, context={}):
		
		invoice_obj = self.pool.get('account.invoice')
		pres_request_obj = self.pool.get('medical.prescription.order')
	
#		prescriptions = ids
# Don't use this. It will be 1 (and it would go to the invoice status of the first prescription )

# To get the IDs of the prescriptions, use the context value array for active_ids


		prescriptions = context.get ('active_ids')
	  	  
		pats = []



		for pres_id in prescriptions:
			pres=pres_request_obj.browse(cr, uid, pres_id)
			pats.append(pres.name)
			logging.debug('pres = %s; pats = %s', repr(pres), repr(pats))
	
		if pats.count(pats[0]) == len(pats):
			invoice_data = {}
			for pres_id in prescriptions:
				pres = pres_request_obj.browse(cr, uid, pres_id)

# Check if the prescription is invoice exempt, and stop the invoicing process
				if pres.no_invoice :
					raise  osv.except_osv(_('UserError'), _('The prescription is invoice exempt'))				
	
				if pres.invoice_status == 'invoiced':
					logging.debug('pres.invoice_status = %s', repr(pres.invoice_status))
					if len(prescriptions) > 1:
						raise  osv.except_osv(_('UserError'), _('At least one of the selected prescriptions is already invoiced'))
					else:
						raise  osv.except_osv(_('UserError'), _('Prescription already invoiced'))
				if pres.invoice_status == 'no':
					if len(prescriptions) > 1:
						raise  osv.except_osv(_('UserError'), _('At least one of the selected prescriptions can not be invoiced'))
					else:
						raise  osv.except_osv(_('UserError'), _('You can not invoice this prescription'))
	
			logging.debug('pres.name = %s', repr(pres.name))
			if pres.name.name.id:
				invoice_data['partner_id'] = pres.name.name.id
				res = self.pool.get('res.partner').address_get(cr, uid, [pres.name.name.id], ['contact', 'invoice'])
				invoice_data['address_contact_id'] = res['contact']
				invoice_data['address_invoice_id'] = res['invoice']
				invoice_data['account_id'] = pres.name.name.property_account_receivable.id
				invoice_data['fiscal_position'] = pres.name.name.property_account_position and pres.name.name.property_account_position.id or False
				invoice_data['payment_term'] = pres.name.name.property_payment_term and pres.name.name.property_payment_term.id or False
	
			prods_data = {}
			for pres_id in prescriptions:
				pres = pres_request_obj.browse(cr, uid, pres_id)
				logging.debug('pres.name = %s; pres.prescription_line = %s', pres.name, pres.prescription_line)
				
# Check for empty prescription lines

				if not pres.prescription_line:
					raise  osv.except_osv(_('UserError'), _('You need to have at least one prescription item in your invoice'))			
				
				for pres_line in pres.prescription_line:
					logging.debug('pres_line = %s; pres_line.medicament.name = %s; pres_line.quantity = %s', pres_line, pres_line.medicament.name, pres_line.quantity)
	
					if prods_data.has_key(pres_line.medicament.name):
						prods_data[pres_line.medicament.name]['quantity'] += pres_line.quantity
					else:
						a = pres_line.medicament.name.product_tmpl_id.property_account_income.id
						if not a:
							a = pres_line.medicament.name.categ_id.property_account_income_categ.id

						prods_data[pres_line.medicament.name] = {'product_id':pres_line.medicament.name.id,
										'name':pres_line.medicament.name.name,
										'quantity':pres_line.quantity,
										'account_id':a,
										'price_unit':pres_line.medicament.name.lst_price}
					
	
			product_lines = []
			for prod_id, prod_data in prods_data.items():
				logging.debug('product_id = %s', repr(prod_data['product_id']))
				product_lines.append((0, 0, {'product_id':prod_data['product_id'],
						'name':prod_data['name'],
						'quantity':prod_data['quantity'],
						'account_id':prod_data['account_id'],
						'price_unit':prod_data['price_unit']}))
				
			invoice_data['invoice_line'] = product_lines
			invoice_id = invoice_obj.create(cr, uid, invoice_data)
			
			pres_request_obj.write(cr, uid, prescriptions, {'invoice_status':'invoiced'})
	
			return {
				'domain': "[('id','=', " + str(invoice_id) + ")]",
				'name': 'Create Prescription Invoice',
				'view_type': 'form',
				'view_mode': 'tree,form',
				'res_model': 'account.invoice',
				'type': 'ir.actions.act_window'
			}
	
		else:
			raise  osv.except_osv(_('UserError'), _('When multiple prescriptions are selected, patient must be the same'))


make_medical_prescription_invoice()


