from odoo import api, fields, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class EmployeePromotion(models.Model):
    _name = 'employee.promotion'
    _description = 'Employee Promotion'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'
    _order = 'create_date desc'


    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    promotion_date = fields.Date(string='Promotion Date', required=True, default=fields.Date.today)
    current_job_title = fields.Char(string='Previous Job Position', compute='_compute_employee_details', store=True)
    new_job_position = fields.Many2one('hr.job', string='New Job Position', required=True)
    reason_for_promotion = fields.Text(string='Reason for Promotion')
    buttons_hidden = fields.Boolean(string="Buttons Hidden", default=False)
    company_id = fields.Many2one('res.company', string='Company', compute='_compute_employee_details', store=True, readonly=True)
    previous_department_id = fields.Many2one('hr.department', string='Previous Department', compute='_compute_employee_details', store=True, readonly=True)


    state = fields.Selection([
        ('draft', 'Draft'),

        ('approve', 'To Approve'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')

    def action_approve(self):
        self.state = 'approve'
        self.buttons_hidden = True

    def action_done(self):
        self.state = 'done'
        self.buttons_hidden = True

    def action_cancel(self):
        self.state = 'cancelled'
        self.buttons_hidden = False


    def promote_employee(self):
        self.state = 'done'
        for promotion in self:
            promotion.employee_id.job_id = promotion.new_job_position




    @api.depends('employee_id')
    def _compute_employee_details(self):
        for record in self:
            if record.employee_id:
                record.current_job_title = record.employee_id.job_id.name
                record.previous_department_id = record.employee_id.department_id.id
                record.company_id = record.employee_id.company_id.id
            else:
                record.current_job_title = False
                record.previous_department_id = False
                record.company_id = False


    @api.model
    def create(self, vals):
        return super(EmployeePromotion, self).create(vals)

    def unlink(self):
        return super(EmployeePromotion, self).unlink()

    promotion_button_visible = fields.Boolean(
        compute='_compute_promotion_button_visible',
        store=False  # No need to store, always fetch fresh from settings
    )

    def _compute_promotion_button_visible(self):
        self.promotion_button_visible = self.env['ir.config_parameter'].sudo().get_param(
            'employee_promotion.promotion_button_visible', default=True)

    def print_report(self):
        return self.env.ref('employee_promotions.report_employee_promotion').report_action(self)

