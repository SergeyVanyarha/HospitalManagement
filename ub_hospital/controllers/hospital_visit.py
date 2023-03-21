import json
from odoo import http
from odoo.http import request, Response
from datetime import datetime
from pytz import timezone
from typing import List, Optional
from pydantic import BaseModel, PositiveInt


class Visit(BaseModel):
    patient_name: Optional[str] = ''
    patient_phone: str
    doctor_name: Optional[str] = ''
    doctor_phone: Optional[str] = ''
    doctor_position: Optional[str] = ''
    disease: List[str]
    date: str
    duration: Optional[PositiveInt] = 15
    diagnosis: Optional[str] = ''
    treatment: Optional[str] = ''
    notes: Optional[str] = ''


class HospitalVisit(http.Controller):
    @http.route(['/hospital/visit'], type='json', auth='user', methods=['POST', 'PUT'])
    def register_hospital_visit(self, **kwargs):
        """
            This endpoint for registering a hospital visit.
            You can use it with POST or PUT methods.

            Example of request:
            {
                "patient_name": "Kyrylo",
                "patient_phone": "+380501234567",
                "doctor_name": "Elizabeth",
                "doctor_phone": "+380501234567",
                "doctor_position": "Surgeon",
                "disease": ["Flu"],
                "date": "2021-01-01T12:00:00+02:00",
                "duration": 15,
                "diagnosis": "Flu",
                "treatment": "Bed rest",
                "notes": "Some notes"
            }
        """
        # Parse request data into object
        data = Visit.parse_obj(json.loads(request.httprequest.data.decode('utf-8')))

        # Find or create patient
        patient_id = request.env['hospital.patient'].search([('phone', '=', data.patient_phone)], limit=1)
        if not patient_id:
            patient_id = request.env['hospital.patient'].create({
                'phone': data.patient_phone,
                'name': data.patient_name,
            })

        # Find doctor
        doctor_domain = []
        if data.doctor_name:
            doctor_domain.append(('name', '=', data.doctor_name))
        if data.doctor_phone:
            doctor_domain.append(('phone', '=', data.doctor_phone))
        if data.doctor_position:
            doctor_position_id = request.env['hospital.doctor.position'].search([('name', '=', data.doctor_position)],
                                                                                limit=1)
            doctor_domain.append(('position_id', '=', doctor_position_id.id))
        doctor_id = request.env['hospital.doctor'].search(doctor_domain)
        if doctor_id and len(doctor_id) > 1:
            return {'status_code': 400, 'message': 'Too many doctors found'}
        elif not doctor_id:
            return {'status_code': 404, 'domain': doctor_domain, 'message': 'Doctor not found'}

        # Find or create visit
        disease_ids = request.env['hospital.disease'].search([('name', 'in', data.disease)])
        utc = timezone('UTC')
        visit_datetime = datetime.strftime(datetime.fromisoformat(data.date).astimezone(utc), '%Y-%m-%d %H:%M:%S')
        visit_id = request.env['hospital.patient.visit'].search([('patient_id', '=', patient_id.id),
                                                                 ('doctor_id', '=', doctor_id.id),
                                                                 ('visit_datetime', '=', visit_datetime)], limit=1)
        if visit_id:
            visit_id.write({
                'diagnosis': data.diagnosis,
                'treatment': data.treatment,
                'notes': data.notes,
                'disease_ids': [(4, disease.id) for disease in disease_ids],
            })
            return {'status_code': 200, 'message': 'Visit updated'}
        else:
            request.env['hospital.patient.visit'].create({
                'patient_id': patient_id.id,
                'doctor_id': doctor_id.id,
                'visit_datetime': visit_datetime,
                'diagnosis': data.diagnosis,
                'treatment': data.treatment,
                'notes': data.notes,
                'disease_ids': [(4, disease.id) for disease in disease_ids],
            })
            return {'status_code': 201, 'message': 'Visit created'}
