from odoo import models, fields, api
from datetime import timedelta


class HospitalPatientVisit(models.Model):
    _name = 'hospital.patient.visit'
    _description = 'Patient Visit'

    name = fields.Char(
        string='Name',
        compute='compute_name',
        store=True
    )

    active = fields.Boolean(
        default=True
    )

    visit_datetime = fields.Datetime(
        string='Visit Date',
        default=fields.Datetime.now
    )

    duration = fields.Float(
        string='Duration in Minutes',
        default=15
    )

    visit_datetime_end = fields.Datetime(
        string='Visit End Date',
        compute='compute_visit_datetime_end',
        store=True
    )

    is_old = fields.Boolean(
        string='Is Old',
        compute='compute_is_old',
    )

    patient_id = fields.Many2one(
        'hospital.patient',
        string='Patient'
    )

    doctor_id = fields.Many2one(
        'hospital.doctor',
        string='Doctor'
    )

    disease_ids = fields.Many2many(
        'hospital.disease',
        string='Diseases'
    )

    diagnosis = fields.Text(
        string='Diagnosis'
    )

    notes = fields.Text(
        string='Notes'
    )

    treatment = fields.Text(
        string='Treatment'
    )

    @api.depends('visit_datetime', 'duration')
    def compute_visit_datetime_end(self):
        for rec in self:
            if rec.visit_datetime and rec.duration:
                rec.visit_datetime_end = rec.visit_datetime + timedelta(minutes=rec.duration)
            else:
                rec.visit_datetime_end = False

    @api.depends('patient_id', 'visit_datetime', 'doctor_id', 'doctor_id.display_name')
    def compute_name(self):
        for rec in self:
            rec.name = f'{rec.patient_id.phone or ""} - {rec.visit_datetime or ""} - ' \
                       f'{rec.doctor_id.display_name or ""}'

    def unlink(self):
        for rec in self:
            if rec.diagnosis:
                raise models.ValidationError('You cannot delete a visit that has a diagnosis')
        return super().unlink()

    def toggle_active(self):
        for rec in self:
            if rec.diagnosis and rec.active:
                raise models.ValidationError('You cannot archive a visit that has a diagnosis')
        return super().toggle_active()

    def compute_is_old(self):
        for rec in self:
            if rec.visit_datetime and fields.Datetime.now() > rec.visit_datetime:
                rec.is_old = True
            else:
                rec.is_old = False
