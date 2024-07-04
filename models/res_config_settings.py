from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    promotion_button_visible = fields.Boolean(
        string="Show Promotion Buttons",
        config_parameter='employee_promotion.promotion_button_visible',
        default=True)

