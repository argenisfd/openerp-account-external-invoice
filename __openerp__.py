# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2011 Vauxoo C.A. (http://openerp.com.ve/) All Rights Reserved.
#                    Luis Escobar <luis@vauxoo.com>
#                    Tulio Ruiz <tulio@vauxoo.com>
# 
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

{
	"name" : "Registro de Facturas",
	"version" : "1.0",
	"author" : "argenisfd",
	"category" : "Generic Modules/Accounting",
	"website" : "http://argenisfd.wordpress.com",
	"depends" : [
				 "base",
				 "account_accountant", 
				 "report_aeroo",
				 "report_aeroo_ooo"
				 ],
	"description" : "Adecuacion para contadores independientes",
	"demo_xml" : [],
	"init_xml" : [],
	"update_xml" : [
					"account_external_invoice_view.xml", 
					"wizard/wizard_report_period_book.xml", 
					#"wizard/wizard_print_period_report.xml",
					"report/reports.xml"
					],
	"active" : True,
	"installable" : True,
}