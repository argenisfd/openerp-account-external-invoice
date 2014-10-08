from osv import osv, fields, orm 
from osv.orm import except_orm
import os
import re
from tools.translate import _
class custom_users(osv.osv):
	_inherit = 'res.users'
	_name = "res.users"

	def create(self, cr, uid, vals, context=None):
		if self.isSecurePassword(vals["new_password"]):
			print "El password es seguro"
		else:
			raise except_orm(_('ValidateError'), _('El password debe contener por lo menos un caracter especial, una letra y un numero. debe tener una longitud minima de 6 caracteres '))
		return super(custom_users, self).create(cr, uid,vals, context=context)

	def write(self, cr, uid, ids, vals, context=None):
		if self.isSecurePassword(vals["new_password"]):
			print "El password es seguro"
		else:
			raise except_orm(_('ValidateError'), _('El password debe contener por lo menos un caracter especial, una letra y un numero. debe tener una longitud minima de 6 caracteres '))
		return super(custom_users, self).write( cr, uid, ids, vals, context=context)



	"""
	def validar_password_seguro(self, cr, uid, ids, context=None):
		print "-------------Validadon el usuario-------------------"
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
	"""
	def isSecurePassword(self, password):
		validar_numero= re.compile('(\d)')
		validar_letra= re.compile('([a-zA-Z])')
		validar_caracter_especial=re.compile('(\W)')
		validar_longitud= re.compile(".{6,}")
		print "search"
		print password
		print validar_caracter_especial.search(password)
		if validar_numero.search(password) and validar_letra.search(password) and validar_caracter_especial.search(password) and validar_longitud.search(password):
			return True
		else:
			return False

	

custom_users();