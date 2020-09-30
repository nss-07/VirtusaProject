import pandas as pd
import random
from datetime import datetime

# data
# convert to the same format, add in defaults in case of null values, convert to dataframe

from imblearn.ensemble import BalancedRandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

def callAI(claim):
    x = pd.read_csv('x.csv')
    y = pd.read_csv('y.csv')


    months_as_customer = random.randint(8,40)
    age = claim['age']
    policy_state = ['IL','IN','OH'][random.randint(0,3)]
    policy_csl = ('500/1000','100/300','250/500')[random.randint(0,3)]

    policy_deductable = 1000 * random.randint(0,10)

    policy_annual_premium = 500 * random.randint(0,10)

    umbrella_limit = 10000 * random.randint(0,3)

    insured_zip = random.randint(111111,999999)

    insured_sex = claim['insured_sex'].upper()

    edu = ('Masters', 'High School','Associate','JD','College', 'MD','PhD')
    insured_education_level = edu[random.randint(0,len(edu))]

    occupation = ('other-service','priv-house-serv','adm-clerical','handlers-cleaners','prof-specialty','protective-serv',
                    'machine-op-inspct','armed-forces','sales','tech-support','transport-moving','craft-repair',
                        'farming-fishing','exec-managerial')
    insured_occupation = occupation[random.randint(0,len(occupation))]

    hobbies = ('camping', 'kayaking', 'golf','dancing','bungie-jumping','movies', 'basketball','exercise','sleeping',
               'video-games','skydiving','paintball','hiking','base-jumping','reading','polo','board-games','yachting',
               'cross-fit','chess')
    insured_hobbies = hobbies[random.randint(0,len(hobbies))]

    insured_relationship = claim['insured_relationship']

    capital_gains = 500 * random.randint(0,10)

    capital_loss = 500 * random.randint(0,10)

    type_of_admission = claim['type_of_admission']

    type_of_visit = claim['type_of_visit']

    incident_severity = claim['incident_severity']

    source_of_admission = claim['source_of_admission']

    h_state = ('WV','NY','VA','PA','SC','NC','OH')
    hospital_state = h_state[random.randint(0,len(h_state))]

    h_city = ('Northbrook','Riverwood','Northbend','Springfield','Hillsdale','Columbus','Arlington')
    hospital_city = h_city[random.randint(0,len(h_city))]

    service_provider = "Long Island Medical Arts"
    hospitalized_hour_of_the_day = random.randint(0,25)

    status_when_brought_in = claim['status_when_brought_in']
    survival_status = claim['survival_status']
    duration_of_hospitalization = claim['duration_of_hospitalization']
    medical_staff = claim['medical_staff']
    total_claim_amount = claim['total_claim']
    board_claim = claim['board_claim']
    pharmacy_claim = claim['pharmacy_claim']
    doctor_consultation_claim = claim['doctor_claim']

    rsn = ('GORD','Appendectomy','Hemorrhoidectomy','Kidney','Cataract','Delivery',
            'Liver','Cancer','Lungs','Brain','Prosthetics','Heart','Stones','ALS')
    reason = rsn[random.randint(0,len(rsn))]

    r_type = ('B123','RSX','L1','J5','A12','H763','H445','CR362','D2','L14','C93','TL','A3','MDX','C736','J1','S9','E400',
            'H1','P1','S2','92x','A1','D1','X5','L72','M5','S1','A5','C633','LN142','F150','C300','ML350','LN132','X6')
    reason_type = r_type[random.randint(0,len(r_type))]

    diagnosed_year = random.randint(2007,2020)

    hospitalized_month = datetime.now().month

    hospitalized_day = datetime.now().day

    x_test = pd.DataFrame(columns = ['months_as_customer', 'age', 'policy_state', 'policy_csl',
           'policy_deductable', 'policy_annual_premium', 'umbrella_limit',
           'insured_zip', 'insured_sex', 'insured_education_level',
           'insured_occupation', 'insured_hobbies', 'insured_relationship',
           'capital-gains', 'capital-loss', 'type_of_admission', 'type_of_visit',
           'incident_severity', 'source_of_admission', 'hospital_state',
           'hospital_city', 'service_provider', 'hospitalized_hour_of_the_day',
           'status_when_brought_in', 'survival_status',
           'duration_of_hospitalization', 'medical_staff', 'total_claim_amount', 'board_claim',
           'pharmacy_claim', 'doctor_consultation_claim', 'reason', 'reason_type',
           'diagnosed_year', 'hospitalized_month', 'hospitalized_day'],index = ['a'])

    x_test.loc['a'] = [months_as_customer,age,policy_state,policy_csl,policy_deductable,policy_annual_premium,
                       umbrella_limit,insured_zip,insured_sex,insured_education_level,insured_occupation,
                       insured_hobbies,insured_relationship,capital_gains,capital_loss,type_of_admission,
                       type_of_visit,incident_severity,source_of_admission,hospital_state,hospital_city,service_provider,
                       hospitalized_hour_of_the_day,status_when_brought_in,survival_status,duration_of_hospitalization,
                       medical_staff,total_claim_amount,board_claim,pharmacy_claim,
                       doctor_consultation_claim,reason,reason_type,diagnosed_year,hospitalized_month,hospitalized_day]

    x_test['reason_type'] = x_test['reason_type'].replace(('B123','RSX','L1','J5','A12','H763',
                                    'H445','CR362','D2','L14','C93','TL','A3','MDX','C736','J1','S9','E400',
                                                       'H1','P1','S2','92x','A1','D1','X5','L72','M5','S1','A5',
                                                       'C633','LN142','F150','C300','ML350','LN132','X6'),
                (0.95,0.91, 0.90,0.88,0.87,0.86,0.85,0.85,0.84,0.83,0.81,0.80,0.78,0.77,0.77,0.76,0.75,0.74,
                     0.73,0.72,0.71,0.71,0.71,0.71,0.70,0.68,0.67,0.67,0.66,0.64,0.62,0.62,0.61,0.60,0.59,0.56))

    x_test['reason'] = x_test['reason'].replace(('GORD','Appendectomy','Hemorrhoidectomy','Kidney','Cataract','Delivery',
                                    'Liver','Cancer','Lungs','Brain','Prosthetics','Heart','Stones','ALS'),
                                                  (0.84,0.82,0.81,0.80,0.77,0.76,0.75,0.74,0.73,0.72,0.71,0.69,0.69,0.66))

    x_test['survival_status'] = x_test['survival_status'].replace(('NO','YES'),(0.76,0.74))

    x_test['hospital_city'] = x_test['hospital_city'].replace(('Northbrook','Riverwood','Northbend','Springfield',
                                        'Hillsdale','Columbus','Arlington'),(0.78,0.77,0.76,0.75,0.74,0.73,0.71))

    x_test['hospital_state'] = x_test['hospital_state'].replace(('WV','NY','VA','PA','SC','NC','OH'),
                                                            (0.82,0.77,0.76,0.73,0.70,0.69,0.56))

    x_test['source_of_admission'] = x_test['source_of_admission'].replace(('None','Self','Neighbor','Family','Ambulance','Other'),
                                                                          (1.0,0.93,0.79,0.73,0.70,0.68))

    x_test['incident_severity'] = x_test['incident_severity'].replace((1,3,5,4),(0.94,0.89,0.87,0.39))

    x_test['type_of_visit'] = x_test['type_of_visit'].replace(('V67', 'V55', 'V73'),(0.78,0.74,0.72))

    x_test['type_of_admission'] = x_test['type_of_admission'].replace(('AD3','AD6','AD8','AD1'),(0.91, 0.90, 0.72,0.70))

    x_test['insured_relationship'] = x_test['insured_relationship'].replace(('husband','own-child','unmarried',
                                            'not-in-family','wife','other-relative'),(0.79,0.78,0.75,0.74,0.72,0.70))

    x_test['insured_hobbies'] = x_test['insured_hobbies'].replace(('camping', 'kayaking', 'golf','dancing',
            'bungie-jumping','movies', 'basketball','exercise','sleeping','video-games','skydiving','paintball',
                'hiking','base-jumping','reading','polo','board-games','yachting', 'cross-fit','chess'),(0.91, 0.90,
                    0.89, 0.88,0.84,0.83,0.82,0.81,0.805,0.80,0.78,0.77,0.76,0.73,0.73,0.72,0.70,0.69,0.25,0.17))

    x_test['insured_occupation'] = x_test['insured_occupation'].replace(('other-service','priv-house-serv',
                            'adm-clerical','handlers-cleaners','prof-specialty','protective-serv',
                    'machine-op-inspct','armed-forces','sales','tech-support','transport-moving','craft-repair',
                        'farming-fishing','exec-managerial'),(0.84, 0.84,0.83, 0.79,0.78,0.77,0.76,0.75,0.72,0.71,
                                                              0.705,0.70,0.69,0.63))

    x_test['insured_education_level'] = x_test['insured_education_level'].replace(('Masters', 'High School','Associate',
                                            'JD','College', 'MD','PhD'),(0.78,0.77,0.76,0.74,0.73,0.72,0.71))

    x_test['insured_sex'] = x_test['insured_sex'].replace(('FEMALE','MALE'),(0.76,0.73))

    x_test['policy_csl'] = x_test['policy_csl'].replace(('500/1000','100/300','250/500'),(0.78,0.74,0.73))

    x_test['policy_state'] = x_test['policy_state'].replace(('IL','IN','OH'),(0.77,0.745,0.74))

    x_test['service_provider'] = x_test['service_provider'].replace(('Long Island Medical Arts','Francis W Iacobellis',
                                'Lenox Hill Hospital','Otis M Jones','Ms St Lukes And Roosevelt',
                                       'Mount Sinai Hospital','Nyp-Weill Cornell'),
                                                    (0.778,0.776,0.765,0.757,0.751,0.74,0.71))

    model = BalancedRandomForestClassifier(n_estimators = 100, random_state = 0)

    model.fit(x, y)
    y_pred_rf = model.predict(x_test)

    return y_pred_rf[0]