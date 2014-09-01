from osv import osv, fields, orm
import os
import re
class custom_users(osv.osv):
	_inherit = 'res.users'
	_name = "res.users"
	def validar_password_seguro(self, cr, uid, ids, context=None):
		validar_numero= re.compile('(\d)')
		validar_letra= re.compile('([a-zA-Z])')
		validar_caracter_especial=re.compile('(\W)')
		validar_longitud= re.compile(".{5,}")

		record = self.browse(cr,uid,ids,context=context)
		for objvalid in record:
			print "search"
			print objvalid.password
			print validar_caracter_especial.search(objvalid.password)
			if validar_numero.search(objvalid.password) and validar_letra.search(objvalid.password) and validar_caracter_especial.search(objvalid.password) and validar_longitud.search(objvalid.password):
				return True
			else:
				return False

	_constraints = [(validar_password_seguro,"El password debe contener por lo menos un caracter especial, una letra y un numero",['new_password'] )]

custom_users();