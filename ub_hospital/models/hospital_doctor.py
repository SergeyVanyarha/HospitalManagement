from odoo import models, fields, api


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor Record'
    _rec_name = 'display_name'

    display_name = fields.Char(
        string='Display Name',
        compute='compute_display_name',
        store=True
    )

    name = fields.Char(
        string='Name',
        required=True
    )

    phone = fields.Char(
        string='Phone'
    )

    email = fields.Char(
        string='Email'
    )

    notes = fields.Text(
        string='Notes'
    )

    position_id = fields.Many2one(
        'hospital.doctor.position',
        string='Position'
    )

    patient_ids = fields.One2many(
        'hospital.patient',
        'main_doctor_id',
        string='Patients'
    )

    @api.depends('name', 'position_id')
    def compute_display_name(self):
        for rec in self:
            rec.display_name = f'{rec.position_id.name}. {rec.name}' if rec.position_id else rec.name

    def open_hospital_report(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Hospital Report',
            'res_model': 'hospital.visit.report',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_doctor_id': self.id}
        }
