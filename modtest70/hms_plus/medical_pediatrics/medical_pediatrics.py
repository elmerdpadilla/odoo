from osv import fields, osv
from openerp import pooler
from openerp.tools.translate import _

class medical_newborn(osv.osv):
    _name="medical.newborn"
    _description = "Newborn Information"
    _columns = {
        'name': fields.char ('Newborn ID', size=128, help="Enter Newborn ID",required=True),        
        'mother': fields.many2one ('medical.patient', 'Mother'),
        'newborn_name': fields.char ('Baby\'s name', size=128),
        'birth_date': fields.datetime ('Date Of Birth', required=True),
        'photo' : fields.binary('Picture'),
        'sex' : fields.selection([
                        ('m', 'Male'),
                        ('f', 'Female'),
                        ('a', 'Ambiguous genitalia')
                        ], 'Sex', required=True),
        'cephalic_perimeter' : fields.integer('Cephalic Perimeter',help="Perimeter in centimeters (cm)"),
        'length' : fields.integer('Length', help="Perimeter in centimeters (cm)"),
        'weight' : fields.integer('Weight', help="Weight in grams (g)"),
        'apgar1' : fields.integer('APGAR 1st minute'),
        'apgar5' : fields.integer('APGAR 5th minute'),
        'apgar_scores' : fields.one2many('medical.neonatal.apgar', 'name','APGAR scores'),
        'meconium' : fields.boolean('Meconium'),
        'congenital_diseases' : fields.one2many('medical.patient.disease','newborn_id', 'Congenital diseases'),
        'reanimation_stimulation' : fields.boolean('Stimulation'),
        'reanimation_aspiration' : fields.boolean('Aspiration'),
        'reanimation_intubation' : fields.boolean('Intubation'),
        'reanimation_mask' : fields.boolean('Mask'),
        'reanimation_oxygen' : fields.boolean('Oxygen'),
        'test_vdrl' : fields.boolean('VDRL'),
        'test_toxo' : fields.boolean('Toxoplasmosis'),
        'test_chagas' : fields.boolean('Chagas'),
        'test_billirubin' : fields.boolean('Billirubin'),
        'test_audition' : fields.boolean('Audition'),
        'test_metabolic' : fields.boolean('Metabolic ("heel stick screening")',
            help="Test for Fenilketonuria, Congenital Hypothyroidism, "
            "Quistic Fibrosis, Galactosemia"),
        'neonatal_ortolani' : fields.boolean('Positive Ortolani'),
        'neonatal_barlow' : fields.boolean('Positive Barlow'),
        'neonatal_hernia' : fields.boolean('Hernia'),
        'neonatal_ambiguous_genitalia' : fields.boolean('Ambiguous Genitalia'),
        'neonatal_erbs_palsy' : fields.boolean('Erbs Palsy'),
        'neonatal_hematoma' : fields.boolean('Hematomas'),
        'neonatal_talipes_equinovarus' : fields.boolean('Talipes Equinovarus'),
        'neonatal_polydactyly' : fields.boolean('Polydactyly'),
        'neonatal_syndactyly' : fields.boolean('Syndactyly'),
        'neonatal_moro_reflex' : fields.boolean('Moro Reflex'),
        'neonatal_grasp_reflex' : fields.boolean('Grasp Reflex'),
        'neonatal_stepping_reflex' : fields.boolean('Stepping Reflex'),
        'neonatal_babinski_reflex' : fields.boolean('Babinski Reflex'),
        'neonatal_blink_reflex' : fields.boolean('Blink Reflex'),
        'neonatal_sucking_reflex' : fields.boolean('Sucking Reflex'),
        'neonatal_swimming_reflex' : fields.boolean('Swimming Reflex'),
        'neonatal_tonic_neck_reflex' : fields.boolean('Tonic Neck Reflex'),
        'neonatal_rooting_reflex' : fields.boolean('Rooting Reflex'),
        'neonatal_palmar_crease' : fields.boolean('Transversal Palmar Crease'),
        'medication' : fields.one2many('medical.patient.medication','newborn_id', 'Medication'),
        'responsible' : fields.many2one('medical.physician', 'Doctor in charge',help="Signed by the health professional"),
        'dismissed' : fields.datetime('Discharged'),
        'bd' : fields.boolean('Stillbirth'),
        'died_at_delivery' : fields.boolean('Died at delivery room'),
        'died_at_the_hospital' : fields.boolean('Died at the hospital'),
        'died_being_transferred' : fields.boolean('Died being transferred',help="The baby died being transferred to another health institution"),
        'tod' : fields.datetime('Time of Death'),
        'cod' : fields.many2one('medical.pathology', 'Cause of death'),
        'notes' : fields.text('Notes'),
    }
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The Newborn ID must be unique !'),
    ]
    
    def print_card(self, cr, uid, ids, context=None):        
        assert len(ids) == 1, 'This option should only be used for a single id at a time'        
        datas = {
                 'model': 'medical.newborn',
                 'ids': ids,
                 'form': self.read(cr, uid, ids[0], context=context),
        }
        return {'type': 'ir.actions.report.xml', 'report_name': 'newborn.card', 'datas': datas, 'nodestroy': True}

medical_newborn()

class medical_neonatalapgar(osv.osv):
    _name="medical.neonatal.apgar"
    _description = "Newborn Information"
    _columns = {
    'name' : fields.many2one('medical.newborn', 'Newborn ID',required=True),
    'apgar_minute' : fields.integer('Minute', required=True),
    'apgar_appearance' : fields.selection([
        ('0', 'central cyanosis'),
        ('1', 'acrocyanosis'),
        ('2', 'no cyanosis'),
        ], 'Appearance', required=True),

    'apgar_pulse' : fields.selection([
        ('0', 'Absent'),
        ('1', '< 100'),
        ('2', '> 100'),
        ], 'Pulse', required=True),

    'apgar_grimace' : fields.selection([
        ('0', 'No response to stimulation'),
        ('1', 'grimace when stimulated'),
        ('2', 'cry or pull away when stimulated'),
        ], 'Grimace', required=True),
                
    'apgar_activity' : fields.selection([
        ('0', 'None'),
        ('1', 'Some flexion'),
        ('2', 'flexed arms and legs'),
        ], 'Activity', required=True),

    'apgar_respiration' : fields.selection([
        ('0', 'Absent'),
        ('1', 'Weak / Irregular'),
        ('2', 'strong'),
        ], 'Respiration', required=True),

    'apgar_score' : fields.integer('APGAR Score'),
    }
    
    def on_change_with_apgar_score(self, cr, uid, ids, apgar_appearance,apgar_pulse,apgar_grimace,apgar_activity,apgar_respiration):
        apgar_appearance = apgar_appearance or '0'
        apgar_pulse = apgar_pulse or '0'
        apgar_grimace = apgar_grimace or '0'
        apgar_activity = apgar_activity or '0'
        apgar_respiration = apgar_respiration or '0'

        apgar_score = int(apgar_appearance) + int(apgar_pulse) + int(apgar_grimace) + int(apgar_activity) + int(apgar_respiration)

        return {'value': {'apgar_score': apgar_score}}
        
medical_neonatalapgar()

class medical_neonatalmedication(osv.osv):    
    _inherit = 'medical.patient.medication'
    _columns = {
        'newborn_id' : fields.many2one('medical.newborn', 'Newborn ID')
    }
medical_neonatalmedication()

class medical_neonatalcongenitaldiseases(osv.osv):    
    _inherit = 'medical.patient.disease'
    _columns = {
        'newborn_id' : fields.many2one('medical.newborn', 'Newborn ID')
    }
medical_neonatalcongenitaldiseases()

class medical_pediatricsymptomschecklist(osv.osv):
    _name = 'medical.patient.psc'
    _description = 'Pediatric Symptoms Checklist'
    _columns = {
        'patient' : fields.many2one('medical.patient', 'Patient', required=True),
        'evaluation_date' : fields.many2one('medical.appointment', 'Appointment Date',help="Enter or select the date / ID of the appointment related to this evaluation",required=True),
        'evaluation_start' : fields.datetime('Date', required=True),    
        'user_id' : fields.many2one('res.users', 'Healh Professional', readonly=True),
        'notes' : fields.text('Notes'),    
        'psc_aches_pains' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Complains of aches and pains'),
    
        'psc_spend_time_alone' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Spends more time alone'),
    
        'psc_tires_easily' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Tires easily, has little energy'),
    
        'psc_fidgety' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Fidgety, unable to sit still'),
    
        'psc_trouble_with_teacher' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Has trouble with teacher'),
    
        'psc_less_interest_in_school' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Less interested in school'),
    
        'psc_acts_as_driven_by_motor' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Acts as if driven by a motor'),
    
        'psc_daydreams_too_much' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Daydreams too much'),
    
        'psc_distracted_easily' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Distracted easily'),
    
        'psc_afraid_of_new_situations' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Is afraid of new situations'),
    
        'psc_sad_unhappy' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Feels sad, unhappy'),
    
        'psc_irritable_angry' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Is irritable, angry'),
    
        'psc_feels_hopeless' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Feels hopeless'),
    
        'psc_trouble_concentrating' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Has trouble concentrating'),
    
        'psc_less_interested_in_friends' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Less interested in friends'),
    
        'psc_fights_with_others' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Fights with other children'),
    
        'psc_absent_from_school' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Absent from school'),
    
        'psc_school_grades_dropping' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'School grades dropping'),
    
        'psc_down_on_self' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Is down on him or herself'),
    
        'psc_visit_doctor_finds_ok' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Visits the doctor with doctor finding nothing wrong'),
    
        'psc_trouble_sleeping' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Has trouble sleeping'),
    
        'psc_worries_a_lot' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Worries a lot'),
    
        'psc_wants_to_be_with_parents' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Wants to be with you more than before'),
    
        'psc_feels_is_bad_child' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Feels he or she is bad'),
    
        'psc_takes_unnecesary_risks' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Takes unnecessary risks'),
    
        'psc_gets_hurt_often' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Gets hurt frequently'),
    
        'psc_having_less_fun' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Seems to be having less fun'),
    
        'psc_act_as_younger' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Acts younger than children his or her age'),
    
        'psc_does_not_listen_to_rules' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Does not listen to rules'),
    
        'psc_does_not_show_feelings' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Does not show feelings'),
    
        'psc_does_not_get_people_feelings' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Does not get people feelings'),
    
        'psc_teases_others' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Teases others'),
    
        'psc_blames_others' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Blames others for his or her troubles'),
    
        'psc_takes_things_from_others' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Takes things that do not belong to him or her'),
    
        'psc_refuses_to_share' : fields.selection([
            (None, ''),
            ('0', 'Never'),
            ('1', 'Sometimes'),
            ('2', 'Often'),
            ], 'Refuses to share'),
    
        'psc_total' : fields.integer('PSC Total'),
    }
    _defaults = {
        'user_id': lambda obj, cr, uid, context: uid,
        'psc_total' : 0,
        'evaluation_start': fields.date.context_today,
    }
    
    def on_change_with_psc_total(self, cr, uid, ids,psc_aches_pains,psc_spend_time_alone,psc_tires_easily,psc_fidgety,psc_trouble_with_teacher,psc_less_interest_in_school,psc_acts_as_driven_by_motor,psc_daydreams_too_much,psc_distracted_easily,psc_afraid_of_new_situations,psc_sad_unhappy,psc_irritable_angry,psc_feels_hopeless,psc_trouble_concentrating,psc_less_interested_in_friends,psc_fights_with_others,psc_absent_from_school,psc_school_grades_dropping,psc_down_on_self,psc_visit_doctor_finds_ok,psc_trouble_sleeping,psc_worries_a_lot,psc_wants_to_be_with_parents,psc_feels_is_bad_child,psc_takes_unnecesary_risks,psc_gets_hurt_often,psc_having_less_fun,psc_act_as_younger,psc_does_not_listen_to_rules,psc_does_not_show_feelings,psc_does_not_get_people_feelings,psc_teases_others,psc_takes_things_from_others,psc_refuses_to_share,context=None):
            psc_aches_pains = psc_aches_pains or '0'
            psc_spend_time_alone = psc_spend_time_alone or '0'
            psc_tires_easily = psc_tires_easily or '0'
            psc_fidgety = psc_fidgety or '0'
            psc_trouble_with_teacher = psc_trouble_with_teacher or '0'
            psc_less_interest_in_school = psc_less_interest_in_school or '0'
            psc_acts_as_driven_by_motor = psc_acts_as_driven_by_motor or '0'
            psc_daydreams_too_much = psc_daydreams_too_much or '0'
            psc_distracted_easily = psc_distracted_easily or '0'
            psc_afraid_of_new_situations = psc_afraid_of_new_situations or '0'
            psc_sad_unhappy = psc_sad_unhappy or '0'
            psc_irritable_angry = psc_irritable_angry or '0'
            psc_feels_hopeless = psc_feels_hopeless or '0'
            psc_trouble_concentrating = psc_trouble_concentrating or '0'
            psc_less_interested_in_friends = psc_less_interested_in_friends or '0'
            psc_fights_with_others = psc_fights_with_others or '0'
            psc_absent_from_school = psc_absent_from_school or '0'
            psc_school_grades_dropping = psc_school_grades_dropping or '0'
            psc_down_on_self = psc_down_on_self or '0'
            psc_visit_doctor_finds_ok = psc_visit_doctor_finds_ok or '0'
            psc_trouble_sleeping = psc_trouble_sleeping or '0'
            psc_worries_a_lot = psc_worries_a_lot or '0'
            psc_wants_to_be_with_parents = psc_wants_to_be_with_parents or '0'
            psc_feels_is_bad_child = psc_feels_is_bad_child or '0'
            psc_takes_unnecesary_risks = psc_takes_unnecesary_risks or '0'
            psc_gets_hurt_often = psc_gets_hurt_often or '0'
            psc_having_less_fun = psc_having_less_fun or '0'
            psc_act_as_younger = psc_act_as_younger or '0'
            psc_does_not_listen_to_rules = psc_does_not_listen_to_rules or '0'
            psc_does_not_show_feelings = psc_does_not_show_feelings or '0'
            psc_does_not_get_people_feelings = psc_does_not_get_people_feelings or '0'
            psc_teases_others = psc_teases_others or '0'
            psc_takes_things_from_others = psc_takes_things_from_others or '0'
            psc_refuses_to_share = psc_refuses_to_share or '0'
            psc_total = int(psc_aches_pains) + int(psc_spend_time_alone) + \
                int(psc_tires_easily) + int(psc_fidgety) + \
                int(psc_trouble_with_teacher) + \
                int(psc_less_interest_in_school) + \
                int(psc_acts_as_driven_by_motor) + \
                int(psc_daydreams_too_much) + int(psc_distracted_easily) + \
                int(psc_afraid_of_new_situations) + int(psc_sad_unhappy) + \
                int(psc_irritable_angry) + int(psc_feels_hopeless) + \
                int(psc_trouble_concentrating) + \
                int(psc_less_interested_in_friends) + \
                int(psc_fights_with_others) + int(psc_absent_from_school) + \
                int(psc_school_grades_dropping) + int(psc_down_on_self) + \
                int(psc_visit_doctor_finds_ok) + int(psc_trouble_sleeping) + \
                int(psc_worries_a_lot) + int(psc_wants_to_be_with_parents) + \
                int(psc_feels_is_bad_child) + int(psc_takes_unnecesary_risks) + \
                int(psc_gets_hurt_often) + int(psc_having_less_fun) + \
                int(psc_act_as_younger) + int(psc_does_not_listen_to_rules) + \
                int(psc_does_not_show_feelings) + \
                int(psc_does_not_get_people_feelings) + \
                int(psc_teases_others) + \
                int(psc_takes_things_from_others) + \
                int(psc_refuses_to_share)
            
            #query = _("update medical_patient_psc set psc_total=%s where patient=%s and evaluation_date=%s")%(psc_total,str(patient),str(evaluation_date))
            #cr.execute(query)

            return {'value': {'psc_total': psc_total}}
medical_pediatricsymptomschecklist()   