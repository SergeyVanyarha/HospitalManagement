from odoo import models, fields


class HospitalDisease(models.Model):
    _name = 'hospital.disease'
    _description = 'Disease'

    name = fields.Char(
        string='Name',
        required=True
    )

    doctor_position_ids = fields.Many2many(
        'hospital.doctor.position',
        string='Doctor Positions'
    )
