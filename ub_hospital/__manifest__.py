{
    'name': "Hospital Management",

    'summary': """
        Basic logic for hospital management
    """,

    'description': """
        Basic logic for hospital management
    """,

    'author': "MasterFilin",
    'category': 'Uncategorized',
    'version': '15.0.0.1',
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],

    'demo': [
        'demo/hospital_doctor_position.xml',
        'demo/hospital_doctor.xml',
        'demo/hospital_patient.xml',
    ],

    'data': [
        # Data
        'data/hospital_disease_data.xml',

        # Security
        'security/ir.model.access.csv',

        # Views
        'views/hospital_doctor.xml',
        'views/hospital_doctor_position.xml',
        'views/hospital_patient.xml',
        'views/hospital_disease.xml',
        'views/hospital_patient_visit.xml',
        'wizard/hospital_report.xml',
        'views/menus.xml',

    ],
}
