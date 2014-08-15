{
	'name' : 'Hospital Management System (Plus)',  
	'version' : '1.0',
	'author' : 'The Proven Technology',
	'category' : 'Generic Modules/Medical',
	'depends' : ['base','sale','purchase','account','product','hr'],
	'summary' : 'Complete Hospital Information System',
	'description' : """

Hospital Management System (Plus) for OpenERP 7
=======================================================

Hospital Management System is a multi-user, highly scalable, centralized Electronic Medical Record (EMR) and Hospital Information System for openERP.
It provides a universal Health and Hospital Information System, so doctors and institutions all over the world will benefit from a centralized, high quality, secure and scalable system.


1) Main Module:


    * Strong focus in family medicine and Primary Health Care

    * Major interest in Socio-economics (housing conditions, substance abuse, education...)

    * Diseases and Medical procedures standards (like ICD-10 / ICD-10-PCS ...)

    * Patient Genetic and Hereditary risks : Over 4200 genes related to diseases (NCBI / Genecards)

    * Epidemiological and other statistical reports

    * 100% paperless patient examination and history taking

    * Patient Administration (creation, evaluations / consultations, history ... )

    * Doctor Administration

    * Lab Administration

    * Medicine / Drugs information

    * Medical stock and supply chain management

    * Hospital Financial Administration

    * Designed with industry standards in mind
    
2) Genetic Risks:

	* Family history, hereditary risks and genetic disorders. We included the NCBI and Genecard information, more than 4200 genes associated to diseases.

3) Lifestyle:

	* Eating habits and diets
	
	* Sleep patterns
		
	* Drug / alcohol addictions
	
	* Physical activity (workout / excercise )
	
	* Sexuality and sexual behaviours
	
4) Socioeconomics:

It takes care of the input of all the socio-economic factors that influence the health of the individual / family and society.
Among others, we include the following factors :

	* Living conditions
	
	* Educational level
	
	* Infrastructure (electricity, sewers, ... )
	
	* Family affection ( APGAR )
	
	* Drug addiction 
	
	* Hostile environment
	
	* Teenage Pregnancy
	
	* Working children

5) Inpatient Hospitalization:

	* Patient Registration
	
	* Bed reservation

	* Hospitalization

	* Nursing Plan
	
	* Discharge Plan
	
	* Reporting

6) Laboratory Management:
	
	* Lab test, reports and POS management
	
7) Invoice Management:

	* Create and manage invoices for Lab test, Appointments and Prescription.
	
	* Invoice of multiple appointments at a time.
	
8) Gynecology Management:

	* Gynecological & Obstetric Information.

	* Perinatal Information and Puerperium monitoring.

9) Surgery Management:

10) Pediatrics & Neonatology Management:

	* Pediatrics Systems Checklist
	* ASGAR Score Test
	* Newborn Management

""",
	"website" : "http://www.theproventechnology.com",
	"init" : [],
	"demo" : ["medical/demo/medical_demo.xml"],
	"data" : ["hms_menu.xml", "medical/medical_view.xml",
					"medical/medical_report.xml",
					"medical/data/medical_sequences.xml",					
					"medical/data/ethnic_groups.xml",
					"medical/data/occupations.xml",
					"medical/data/dose_units.xml",
					"medical/data/HL7_drug_administration_routes.xml",
					"medical/data/medicament_form.xml",
					"medical/data/snomed_frequencies.xml",
					"medical/data/medicament_categories.xml",
					"medical/data/WHO_list_of_essential_medicines.xml",
					"medical/data/WHO_medicaments.xml",
					"medical/data/medical_specialties.xml",
					"medical/data/dose_units.xml",					
					"medical_genetics/medical_genetics_view.xml",
					"medical_genetics/data/genetic_risks.xml",
					"medical_lifestyle/medical_lifestyle_view.xml",
					"medical_lifestyle/data/recreational_drugs.xml",
					"medical_socioeconomics/medical_socioeconomics_view.xml",
					"medical_inpatient/medical_inpatient_view.xml", 
					"medical_inpatient/data/medical_inpatient_sequence.xml",
					"medical_lab/medical_lab_report.xml",
					"medical_lab/data/medical_lab_sequences.xml", 
					"medical_lab/data/lab_test_data.xml",
					"medical_lab/wizard/create_lab_test.xml",
					"medical_lab/medical_lab_view.xml",					
					"medical_invoice/wizard/appointment_invoice.xml",
					"medical_invoice/wizard/prescription_invoice.xml",
					"medical_invoice/wizard/create_lab_invoice.xml",
					"medical_invoice/medical_invoice_view.xml",						
					"medical_surgery/medical_surgery_view.xml",
					"medical_pediatrics/medical_pediatrics_view.xml",
					"medical_pediatrics/medical_pediatrics_report.xml",
					"medical_gyneco/medical_gyneco_view.xml",
					"security/medical_security.xml",
					"security/ir.model.access.csv",
			],
	"active": False 
}
