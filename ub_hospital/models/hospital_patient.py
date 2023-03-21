from odoo import models, fields, api
from datetime import date


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Record'
    _rec_name = 'phone'

    phone = fields.Char(
        string='Phone',
        required=True
    )

    name = fields.Char(
        string='Name',
    )

    age = fields.Integer(
        string='Age',
        compute='compute_age',
        store=True
    )

    birth_date = fields.Date(
        string='Birth Date'
    )

    notes = fields.Text(
        string='Notes'
    )

    contact_id = fields.Many2one(
        'res.partner',
        string='Contact'
    )

    main_doctor_id = fields.Many2one(
        'hospital.doctor',
        string='Main Doctor'
    )

    @api.depends('birth_date')
    def compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()
                if today.month < rec.birth_date.month or \
                        (today.month == rec.birth_date.month and today.day < rec.birth_date.day):
                    rec.age = today.year - rec.birth_date.year - 1
                else:
                    rec.age = today.year - rec.birth_date.year
            else:
                rec.age = 0

    def open_hospital_report(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Hospital Report',
            'res_model': 'hospital.visit.report',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_patient_id': self.id}
        }
