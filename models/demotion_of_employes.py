from odoo import api, fields, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class EmployeeDemotion(models.Model):
    _name = 'employee.demotion'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Employee Demotion'
    _rec_name = 'employee_id'
    _order = 'create_date desc'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    demotion_date = fields.Date(string='Demotion Date', required=True, default=fields.Date.today)
    previous_department_id = fields.Many2one('hr.department', string='Previous Department', compute='_compute_employee_details', store=True, readonly=True)
    previous_job_title = fields.Char(string='Previous Job Position', compute='_compute_employee_details', store=True, readonly=True)
    new_job_position = fields.Many2one('hr.job', string='New Job Position', required=True)
    reason_for_demotion = fields.Text(string='Reason for Demotion')
    buttons_hidden = fields.Boolean(string="Buttons Hidden", default=False)
    company_id = fields.Many2one('res.company', string='Company', compute='_compute_employee_details', store=True, readonly=True)

    promotion_button_visible = fields.Boolean(
        compute='_compute_promotion_button_visible',
        store=False
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'To Approve'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')

    def action_approve(self):
        self.state = 'approve'
        self.buttons_hidden = False

    def action_done(self):
        self.state = 'done'
        self.buttons_hidden = True

    def action_cancel(self):
        self.state = 'cancelled'
        self.buttons_hidden = True

    @api.depends('employee_id')
    def _compute_employee_details(self):
        for record in self:
            if record.employee_id:
                record.previous_job_title = record.employee_id.job_id.name
                record.previous_department_id = record.employee_id.department_id.id
                record.company_id = record.employee_id.company_id.id
            else:
                record.previous_job_title = False
                record.previous_department_id = False
                record.company_id = False

    def promote_employee(self):
        self.state = 'done'
        for demotion in self:
            demotion.employee_id.job_id = demotion.new_job_position

    @api.model
    def create(self, vals):
        return super(EmployeeDemotion, self).create(vals)

    def unlink(self):
        return super(EmployeeDemotion, self).unlink()

    def _compute_promotion_button_visible(self):
        self.promotion_button_visible = self.env['ir.config_parameter'].sudo().get_param(
            'employee_promotion.promotion_button_visible', default=True)
