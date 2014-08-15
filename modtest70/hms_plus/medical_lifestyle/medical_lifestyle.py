from osv import fields, osv


class drugs_recreational (osv.osv):
	_name="medical.drugs_recreational"
	_columns = {
		'name': fields.char ('Name', size=128, help="Name of the drug"),
		'street_name': fields.char ('Street names', size=256, help="Common name of the drug in street jargon"),
		'toxicity' : fields.selection([
                                ('0','None'),
                                ('1','Low'),
                                ('2','High'),
                                ('3','Extreme'),
                                ], 'Toxicity', select=True),		
		'addiction_level' : fields.selection([
                                ('0','None'),
                                ('1','Low'),
                                ('2','High'),
                                ('3','Extreme'),
                                ], 'Dependence', select=True),		
		'legal_status' : fields.selection([
                                ('0','Legal'),
                                ('1','Illegal'),
                                ], 'Legal Status', select=True),

        'category' : fields.selection([
                        ('cannabinoid','Cannabinoids'),
                        ('depressant','Depressants'),
                        ('dissociative','Dissociative Anesthetics'),
                        ('hallucinogen','Hallucinogens'),
                        ('opioid','Opioids'),
                        ('stimulant','Stimulants'),
                        ('other','Others'),
                        ], 'Category', select=True),
        'withdrawal_level' : fields.integer ("Withdrawal",help="Presence and severity ofcharacteristic withdrawal symptoms.\nUsing Henningfield rating. 1=highest and 6=lowest"),
        'reinforcement_level' : fields.integer ("Reinforcement",help="A measure of the substance's ability to get users to take it again and again, and in preference to other substances.\nUsing Henningfield rating. 1=highest and 6=lowest"),
        'tolerance_level' : fields.integer ("Tolerance",help="How much of the substance is needed to satisfy increasing cravings for it, and the level of stable need that is eventually reached.\nUsing Henningfield rating. 1=highest and 6=lowest"),
        'dependence_level' : fields.integer ("Dependence",help="How difficult it is for the user to quit, the relapse rate, the percentage of people who eventually become dependent, the rating users give their own need for the substance and the degree to which the substance will be used in the face of evidence that it causes harm.\nUsing Henningfield rating. 1=highest and 6=lowest"),
        'intoxication_level' : fields.integer ("Intoxication",help="the level of intoxication is associated with addiction and increases the personal and social damage a substance may do. \nUsing Henningfield rating. 1=highest and 6=lowest"),
        'route_oral' : fields.boolean ('Oral', help=""),
        'route_popping' : fields.boolean ('Skin Popping', help="Subcutaneous or Intradermical administration"),
        'route_inhaling' : fields.boolean ('Smoke / Inhale', help="Insufflation, exluding nasal"),
        'route_sniffing' : fields.boolean ('Sniffing',help="Also called snorting - inhaling through the nares  "),
        'route_injection' : fields.boolean ('Injection', help="Injection - Intravenous, Intramuscular..."),
		'dea_schedule_i' : fields.boolean ('DEA schedule I',help="Schedule I and II drugs have a high potential for abuse. They require greater storage security and have a quota on manufacturing, among other restrictions. Schedule I drugs are available for research only and have no approved medical use; Schedule II drugs are available only by prescription (unrefillable) and require a form for ordering. Schedule III and IV drugs are available by prescription, may have five refills in 6 months, and may be ordered orally. Some Schedule V drugs are available over the counter"),
		'dea_schedule_ii' : fields.boolean ('II',help="Schedule I and II drugs have a high potential for abuse. They require greater storage security and have a quota on manufacturing, among other restrictions. Schedule I drugs are available for research only and have no approved medical use; Schedule II drugs are available only by prescription (unrefillable) and require a form for ordering. Schedule III and IV drugs are available by prescription, may have five refills in 6 months, and may be ordered orally. Some Schedule V drugs are available over the counter"),
		'dea_schedule_iii' : fields.boolean ('III',help="Schedule I and II drugs have a high potential for abuse. They require greater storage security and have a quota on manufacturing, among other restrictions. Schedule I drugs are available for research only and have no approved medical use; Schedule II drugs are available only by prescription (unrefillable) and require a form for ordering. Schedule III and IV drugs are available by prescription, may have five refills in 6 months, and may be ordered orally. Some Schedule V drugs are available over the counter"),
		'dea_schedule_iv' : fields.boolean ('IV',help="Schedule I and II drugs have a high potential for abuse. They require greater storage security and have a quota on manufacturing, among other restrictions. Schedule I drugs are available for research only and have no approved medical use; Schedule II drugs are available only by prescription (unrefillable) and require a form for ordering. Schedule III and IV drugs are available by prescription, may have five refills in 6 months, and may be ordered orally. Some Schedule V drugs are available over the counter"),
		'dea_schedule_v' : fields.boolean ('V',help="Schedule I and II drugs have a high potential for abuse. They require greater storage security and have a quota on manufacturing, among other restrictions. Schedule I drugs are available for research only and have no approved medical use; Schedule II drugs are available only by prescription (unrefillable) and require a form for ordering. Schedule III and IV drugs are available by prescription, may have five refills in 6 months, and may be ordered orally. Some Schedule V drugs are available over the counter"),
		'info' : fields.text ('Extra Info'),
		}

drugs_recreational ()



# lifestyle section

class medical_patient (osv.osv):
	_name = "medical.patient"
	_inherit = "medical.patient"
	_columns = {
		'excercise' : fields.boolean ('Excersise'),
		'excercise_minutes_day' : fields.integer ('Minutes / day',help="How many minutes a day the patient excersises"),
		'sleep_hours' : fields.integer ('Hours of sleep',help="Average hours of sleep per day"),
		'sleep_during_daytime' : fields.boolean ('Sleeps at daytime',help="Check if the patient sleep hours are during daylight rather than at night"),		
		'number_of_meals' : fields.integer ('Meals per day'),
		'eats_alone' : fields.boolean ('Eats alone',help="Check this box if the patient eats by him / herself."),
		'salt' : fields.boolean ('Salt',help="Check if patient consumes salt with the food"),
		'coffee' : fields.boolean ('Coffee'),
		'coffee_cups' : fields.integer ('Cups per day',help="Number of cup of coffee a day"),
		'soft_drinks' : fields.boolean ('Soft drinks (sugar)',help="Check if the patient consumes soft drinks with sugar"),
		'diet' : fields.boolean ('Currently on a diet',help="Check if the patient is currently on a diet"),
		'diet_info' : fields.char ('Diet info',size=256,help="Short description on the diet"),
		'smoking' : fields.boolean ('Smokes'),
		'smoking_number' : fields.integer ('Cigarretes a day'),
		'ex_smoker' : fields.boolean ('Ex-smoker'),
		'second_hand_smoker' : fields.boolean ('Passive smoker', help="Check it the patient is a passive / second-hand smoker"),
		'age_start_smoking' : fields.integer ('Age started to smoke'),
		'age_quit_smoking' : fields.integer ('Age of quitting',help="Age of quitting smoking"),
		'alcohol' : fields.boolean ('Drinks Alcohol'),
		'age_start_drinking' : fields.integer ('Age started to drink ',help="Date to start drinking"),
		'age_quit_drinking' : fields.integer ('Age quit drinking ',help="Date to stop drinking"),
		'ex_alcoholic' : fields.boolean ('Ex alcoholic'),
		'alcohol_beer_number' : fields.integer ('Beer / day'),
		'alcohol_wine_number' : fields.integer ('Wine / day'),
		'alcohol_liquor_number' : fields.integer ('Liquor / day'),
		'drug_usage' : fields.boolean ('Drug Habits'),
		'ex_drug_addict' : fields.boolean ('Ex drug addict'),
		'drug_iv' : fields.boolean ('IV drug user',help="Check this option if the patient injects drugs"),
		'age_start_drugs' : fields.integer ('Age started drugs ',help="Age of start drugs"),
		'age_quit_drugs' : fields.integer ('Age quit drugs ',help="Date of quitting drugs"),
		'drugs' : fields.many2many ('medical.drugs_recreational','patient_drugs_recreational_rel','patient_id','drugs_recreational_id','Drugs', help="Name of drugs that the patient consumes"), 

		'traffic_laws' : fields.boolean ('Obeys Traffic Laws', help="Check if the patient is a safe driver"),
		'car_revision' : fields.boolean ('Car Revision', help="Maintain the vehicle. Do periodical checks - tires, engine, breaks ..."),
		'car_seat_belt' : fields.boolean ('Seat belt', help="Safety measures when driving : safety belt"),
		'car_child_safety' : fields.boolean ('Car Child Safety', help="Safety measures when driving : child seats, proper seat belting, not seating on the front seat, ...."),
		'home_safety' : fields.boolean ('Home safety', help="Keep safety measures for kids in the kitchen, correct storage of chemicals, ..."),
		'motorcycle_rider' : fields.boolean ('Motorcycle Rider', help="The patient rides motorcycles"),		
		'helmet' : fields.boolean ('Uses helmet', help="The patient uses the proper motorcycle helmet"),		
				
		'lifestyle_info' :fields.text ('Extra Information'),


		'sexual_preferences' : fields.selection([
                                ('h','Heterosexual'),
                                ('g','Homosexual'),
				('b','Bisexual'),
				('t','Transexual'),
                                ], 'Sexual Orientation'),

		'sexual_practices' : fields.selection([
                                ('s','Safe / Protected sex'),
                                ('r','Risky / Unprotected sex'),
				], 'Sexual Practices'),

		'sexual_partners': fields.selection([
				('m','Monogamous'),
				('t','Polygamous'),
                                ], 'Sexual Partners'),

		'sexual_partners_number': fields.integer ('Number of sexual partners'),

		'first_sexual_encounter': fields.integer ('Age first sexual encounter'),

		'anticonceptive': fields.selection ([
			('0','None'),
			('1','Pill / Minipill'),
			('2','Male condom'),
			('3','Vasectomy'),
			('4','Female sterilisation'),
			('5','Intra-uterine device'),
			('6','Withdrawal method'),
			('7','Fertility cycle awareness'),
			('8','Contraceptive injection'),
			('9','Skin Patch'),
			('10','Female condom'),
			], 'Anticonceptive Method'),

		'sex_oral': fields.selection ([
			('0','None'),
			('1','Active'),
			('2','Passive'),
			('3','Both'),			
			], 'Oral Sex'),

		'sex_anal': fields.selection ([
			('0','None'),
			('1','Active'),
			('2','Passive'),
			('3','Both'),			
			], 'Anal Sex'),
			
		'prostitute' : fields.boolean ('Prostitute', help="Check if the patient (he or she) is a prostitute"),
		'sex_with_prostitutes' : fields.boolean ('Sex with prostitutes', help="Check if the patient (he or she) has sex with prostitutes"),

		'sexuality_info' :fields.text ('Extra Information'),

	}

medical_patient ()