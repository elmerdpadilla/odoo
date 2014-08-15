from osv import fields, osv


class perinatal_monitor (osv.osv):
	_name = "medical.perinatal.monitor"
	_description = "Perinatal monitor"
	_columns = {
		'name' : fields.char ('Internal code',size=128),
		'date' : fields.datetime ('Date and Time'),
		'systolic' : fields.integer ('Systolic Pressure'),
		'diastolic' : fields.integer ('Diastolic Pressure'),
		'contractions' : fields.integer ('Contractions'),
		'frequency' : fields.integer ('Mother\'s Heart Frequency'),
		'dilation' : fields.integer ('Cervix dilation'),
		'f_frequency' : fields.integer ('Fetus Heart Frequency'),
                'meconium' : fields.boolean('Meconium'),
		'bleeding' : fields.boolean ('Bleeding'),
		'fundal_height' : fields.integer ('Fundal Height'),
		'fetus_position' : fields.selection ([
			('n','Correct'),
			('o', 'Occiput / Cephalic Posterior'),
			('fb', 'Frank Breech'),
			('cb', 'Complete Breech'),
			('t', 'Transverse Lie'),
			('t', 'Footling Breech'),
			], 'Fetus Position', select=True),

		}

perinatal_monitor ()

class puerperium_monitor (osv.osv):
	_name = "medical.puerperium.monitor"
	_description = "Puerperium Monitor"
	_columns = {
		'name' : fields.char ('Internal code',size=64),
		'date' : fields.datetime ('Date and Time', required=True),
		'systolic' : fields.integer ('Systolic Pressure'),
		'diastolic' : fields.integer ('Diastolic Pressure'),
		'frequency' : fields.integer ('Heart Frequency'),
		'lochia_amount' : fields.selection([
                                ('n','normal'),
                                ('e','abundant'),
                                ('h','hemorrhage'),
                                ], 'Lochia amount', select=True),

		'lochia_color' : fields.selection([
                                ('r','rubra'),
                                ('s','serosa'),
                                ('a','alba'),
                                ], 'Lochia color', select=True),

		'lochia_odor' : fields.selection([
                                ('n','normal'),
                                ('o','offensive'),
                                ], 'Lochia odor', select=True),

		'uterus_involution' : fields.integer ('Fundal Height', help="Distance between the symphysis pubis and the uterine fundus (S-FD) in cm"),
		'temperature' : fields.float ('Temperature'),
		}

puerperium_monitor ()



class perinatal (osv.osv):
	_name = "medical.perinatal"
	_description = "perinatal information"
	_columns = {
		'name' : fields.char ('code',size=128),
                'gravida_number' : fields.integer('Gravida #'),
                'abortion' : fields.boolean('Abortion'),
		'admission_date' : fields.datetime ('Admission date',help="Date when she was admitted to give birth"),
		'prenatal_evaluations' : fields.integer ('Prenatal evaluations',help="Number of visits to the doctor during pregnancy"),
		'start_labor_mode' : fields.selection ([
                                ('n','Normal'),
                                ('i','Induced'),
                                ('c','c-section'),
                                ], 'Labor mode', select=True),
		'gestational_weeks' : fields.integer ('Gestational weeks'),
		'gestational_days' : fields.integer ('Gestational days'),
		'fetus_presentation' : fields.selection ([
			('n','Correct'),
			('o', 'Occiput / Cephalic Posterior'),
			('fb', 'Frank Breech'),
			('cb', 'Complete Breech'),
			('t', 'Transverse Lie'),
			('t', 'Footling Breech'),
			], 'Fetus Presentation', select=True),
		'placenta_incomplete' : fields.boolean('Incomplete Placenta'),
		'placenta_retained' : fields.boolean('Retained Placenta'),
		'episiotomy' : fields.boolean('Episiotomy'),
		'vaginal_tearing' : fields.boolean('Vaginal tearing'),
                'forceps' : fields.boolean('Use of forceps'),
		'monitoring' : fields.many2many('medical.perinatal.monitor', 'patient_perinatal_monitor_rel','patient_id','monitor_ids','Monitors'),
		'newborn' : fields.many2many('medical.newborn', 'patient_newborn_rel','patient_id','newborn_ids','Newborn info'),
		'puerperium_monitor' : fields.many2many('medical.puerperium.monitor', 'patient_puerperium_monitor_rel','patient_id','puerperium_ids','Puerperium monitor'),
		'medication' : fields.many2many('medical.medicament', 'patient_labor_rel','medicament_id','patient_id','Medicaments and anesthesics'),
		'dismissed' : fields.datetime('Dismissed from hospital'),
		'died_at_delivery' : fields.boolean ('Died at delivery room'),
		'died_at_the_hospital' : fields.boolean ('Died at the hospital'),
		'died_being_transferred' : fields.boolean ('Died being transferred',help="The mother died being transferred to another health institution"),
		'notes' : fields.text ('Notes'),
	}

perinatal ()






# Add to the Medical patient_data class (medical.patient) the gynecological and obstetric fields.

class medical_patient (osv.osv):
	_name = "medical.patient"
	_inherit = "medical.patient"
	_columns = {
		'currently_pregnant' : fields.boolean ('Currently Pregnant'),
		'fertile' : fields.boolean ('Fertile', help="Check if patient is in fertile age"),
		'menarche' : fields.integer ('Menarche age'),
		'menopausal' : fields.boolean ('Menopausal'),
		'menopause' : fields.integer ('Menopause age'),
		'mammography' : fields.boolean ('Mammography',help="Check if the patient does periodic mammographys"),
		'mammography_last' : fields.date ('Last mammography',help="Enter the date of the last mammography"),
		'breast_self_examination' : fields.boolean ('Breast self-examination',help="Check if the patient does and knows how to self examine her breasts"),		
		'pap_test' : fields.boolean ('PAP test',help="Check if the patient does periodic cytologic pelvic smear screening"),
		'pap_test_last' : fields.date ('Last PAP test',help="Enter the date of the last Papanicolau test"),		
		'colposcopy' : fields.boolean ('Colposcopy',help="Check if the patient has done a colposcopy exam"),
		'colposcopy_last' : fields.date ('Last colposcopy',help="Enter the date of the last colposcopy"),		
		'gravida' : fields.integer ('Gravida',help="Number of pregnancies"),
		'premature' : fields.integer ('Premature',help="Premature Deliveries"),
		'abortions' : fields.integer ('Abortions'),
		'full_term' : fields.integer ('Full Term', help="Full term pregnancies"),
		'gpa' :fields.char ('GPA',size=32,help="Gravida, Para, Abortus Notation. For example G4P3A1 : 4 Pregnancies, 3 viable and 1 abortion"),
		'born_alive' : fields.integer ('Born Alive'),
		'deaths_1st_week' : fields.integer ('Deceased during 1st week',help="Number of babies that die in the first week"),
		'deaths_2nd_week' : fields.integer ('Deceased after 2nd week',help="Number of babies that die after the second week"),
		'perinatal' : fields.many2many ('medical.perinatal', 'patient_perinatal_rel','patient_id','perinatal_id', 'Perinatal Info'),
		
	}

medical_patient ()