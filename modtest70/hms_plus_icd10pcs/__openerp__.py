# -*- encoding: utf-8 -*-
{

	'name' : 'HMS Procedure Coding System - ICD10-PCS',  
	'version' : '1.0',
	'author' : 'The Proven Technology',
	'category' : 'Generic Modules/Medical',
	'depends' : ['hms_plus'],
	'description' : """

Procedure Coding System for Medical : ICD-10-PCS

The ICD-10 Procedure Coding System (ICD-10-PCS) is system of medical classification used for procedural codes. The National Center for Health Statistics (NCHS) received permission from the World Health Organization (WHO) (the body responsible for publishing the International Classification of Diseases [ICD]) to create the ICD-10-PCS as a successor to Volume 3 of ICD-9-CM and a clinical modification of the original ICD-10.

Each code consists of seven alphanumeric characters. The second through seventh characters mean the same thing within each section, but may mean different things in other sections. Each character can be any of 34 possible values the ten digits 0-9 and the 24 letters A-H,J-N and P-Z may be used in each character. The letters O and I excluded to avoid confusion with the numbers 0 and 1. There are no decimals in ICD-10-PCS

Check http://en.wikipedia.org/wiki/ICD-10_Procedure_Coding_System

""",
	"website" : "http://www.theproventechnology.com",
	"init" : [],
	"data" : ["data/icd_10_pcs_2009_part1.xml","data/icd_10_pcs_2009_part2.xml","data/icd_10_pcs_2009_part3.xml"],
	"active": False 
}
