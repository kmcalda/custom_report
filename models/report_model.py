from odoo import models, api


class CustomReport(models.AbstractModel):
    """ Creating abstract model for custom_reports query """
    _name = "custom.report"

    @api.model
    def get_all(self):
        """
        Query all data
        :return: object
        """
        cr = self.env.cr
        query = """
        SELECT 
            comp.name AS distributor_name,
            partner1.ref AS reference,
            move.invoice_partner_display_name AS customer_name,
            indust.name AS industry,
            prod_prod.default_code AS item_code,
            prod_temp.name AS item_name,
            line.quantity,
            uom.name AS  uom,
            line.price_unit AS unit_price,
            line.ref AS reference_invoice,
            line.discount,
            move.ks_global_discount_rate AS special_discount,
            line.price_subtotal,
            TO_CHAR(move.invoice_date, 'MM-DD-YYYY') as invoice_date,
			partner2.name AS salesman
        FROM
            account_move_line AS line
            JOIN account_move AS move ON line.move_id = move.id
            JOIN res_partner AS partner1 ON move.partner_id = partner1.id
            JOIN res_company AS comp ON	move.company_id = comp.id
            JOIN res_partner_industry AS indust ON partner1.industry_id = indust.id
            JOIN product_product AS prod_prod ON line.product_id = prod_prod.id
            JOIN product_template AS prod_temp ON prod_prod.product_tmpl_id = prod_temp.id
            JOIn uom_uom AS uom ON line.product_uom_id = uom.id
			JOIN res_users AS userid ON move.invoice_user_id = userid.id
            JOIN res_partner AS partner2 ON userid.partner_id = partner2.id
        WHERE
            line.account_id = 55
            AND move.state = 'posted' AND move.type = 'out_invoice'
        ORDER BY
            move.name
        """
        cr.execute(query)
        query_result = cr.dictfetchall()
        return query_result

    @api.model
    def get_by_date(self, *args):
        """
        Query all data base on date provided
        :param args: object
        :return: object
        """
        cr = self.env.cr
        query = """
                SELECT 
                    comp.name AS distributor_name,
                    partner1.ref AS reference,
                    move.invoice_partner_display_name AS customer_name,
                    indust.name AS industry,
                    prod_prod.default_code AS item_code,
                    prod_temp.name AS item_name,
                    line.quantity,
                    uom.name AS  uom,
                    line.price_unit AS unit_price,
                    line.discount,
                    move.ks_global_discount_rate AS special_discount,
                    line.price_subtotal,
                    TO_CHAR(move.invoice_date, 'MM-DD-YYYY') as invoice_date,
                    line.ref AS reference_invoice,
                    partner2.name AS salesman
                FROM
                    account_move_line AS line
                    JOIN account_move AS move ON line.move_id = move.id
                    JOIN res_partner AS partner1 ON move.partner_id = partner1.id
                    JOIN res_company AS comp ON	move.company_id = comp.id
                    JOIN res_partner_industry AS indust ON partner1.industry_id = indust.id
                    JOIN product_product AS prod_prod ON line.product_id = prod_prod.id
                    JOIN product_template AS prod_temp ON prod_prod.product_tmpl_id = prod_temp.id
                    JOIn uom_uom AS uom ON line.product_uom_id = uom.id
                    JOIN res_users AS userid ON move.invoice_user_id = userid.id
                    JOIN res_partner AS partner2 ON userid.partner_id = partner2.id
                WHERE
                    line.account_id = 55 AND
                    move.invoice_date BETWEEN SYMMETRIC '%s' AND '%s'
                    AND move.state = 'posted' AND move.type = 'out_invoice'

                ORDER BY
                    move.name
                """ % (args[0]['date_start'], args[0]['date_end'])
        cr.execute(query)
        query_result = cr.dictfetchall()
        return query_result
