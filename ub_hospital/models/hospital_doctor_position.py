from odoo import models, fields


class HospitalDoctorPosition(models.Model):
    _name = 'hospital.doctor.position'
    _description = 'Doctor Position'

    name = fields.Char(
        string='Name',
        required=True
    )

    code = fields.Char(
        string='Code'
    )

    notes = fields.Text(
        string='Notes'
    )

    disease_ids = fields.Many2many(
        'hospital.disease',
        string='Diseases'
    )
