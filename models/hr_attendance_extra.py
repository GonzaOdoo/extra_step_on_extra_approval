from odoo import fields, models
from odoo.exceptions import AccessError
import logging

_logger = logging.getLogger(__name__)
class HrPayrollStructure(models.Model):
    _inherit = 'hr.attendance'

    overtime_status = fields.Selection(
        selection_add=[
            ('first_approved', 'Primera aprobación'),
        ],
        ondelete={
            'first_approved': 'set null',
        },
    )

    def action_first_approve_overtime(self):
        """Primera aprobación: jefe inmediato."""
        for attendance in self:
            if attendance.overtime_status not in ('to_approve', 'refused'):
                continue
    
            attendance.overtime_status = 'first_approved'
    
    
    def action_final_approve_overtime(self):
        """Segunda aprobación: Recursos Humanos."""
        for attendance in self:
            if attendance.overtime_status != 'first_approved':
                continue
    
            attendance.overtime_status = 'approved'
    
    
    def action_refuse_overtime(self):
        self.write({
            'overtime_status': 'refused',
        })

    def action_approve_overtime(self):
        if not self.env.user.has_group('hr_payroll.group_hr_payroll_manager'):
            raise AccessError(
                'Solo Recursos Humanos puede realizar la aprobación final.'
            )
    
        return super().action_approve_overtime()