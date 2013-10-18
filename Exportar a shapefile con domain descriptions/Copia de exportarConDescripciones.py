import arcpy
import renameFields_logica

# Recibe el nombre de un field de códigos, y el nombre de un field con
# descripciones. Devuelve True si el field con descripciones corresponde
# al field de códigos.
# Criterio de decisión: los fields con descripciones son nombrados con con
# 'd_'+ nombre de field con código. Además, son truncados a 10 caracteres.
# Por lo tanto, busco que coincida field_de_codigo[:8] con
# field_de_descripcion[2:10]
def corresponde ( field_de_codigo, field_con_descripcion ):
	if field_de_codigo[:8] == field_con_descripcion[2:10]:
		return True
	return False

# Recibe una feature class y guarda en un diccionario todos los campos de 
# código que serán borrados luego. Las key del diccionario son los nombres
# de los campos de descripciones, los valores son los nombres de los 
# campos con código (a borrar)
def obtener_dict_de_fields_a_borrar (outName):
	
	dict_de_fields_a_borrar = {} # { 'field_d':'field_c', ...}
	
	# Por cada campo que empiece con d_
	for field_d in arcpy.ListFields(outName, 'd_*'):
		# Itero sobre todos los campos
		for field_c in arcpy.ListFields(outName):
			# Si coinciden los primeros 8 caracteres de field_c, lo
			# guardo en la lista_de_fields_a_borrar
			if (corresponde(field_c.name, field_d.name)):
				dict_de_fields_a_borrar[field_d.name] = field_c.name

	return dict_de_fields_a_borrar


# Recibe una feature class y un diccionario con los pares: 
# {'campo de descripciones':'campo de codigos',...}
# Por cada fila de la feature class, si el valor en campo de descripciones 
# es vacío (como guarda un caracter espacio ' ', considero vacío si largo
# <=1 ), guardo ahi el valor que tiene el campo de códigos.
def transferir_valores_si_null (outName, dict_de_fields_a_borrar):
	rows = arcpy.UpdateCursor (outName)
	for row in rows:
		for key in dict_de_fields_a_borrar.iterkeys():
			if len(row.getValue(key)) <= 1:
				row.setValue(key, row.getValue(dict_de_fields_a_borrar[key]))
				rows.updateRow(row)
	



try:

	inFeatures = arcpy.GetParameterAsText(0)
	outLocation = arcpy.GetParameterAsText(1)
	outName = arcpy.GetParameterAsText(2)
	
	#--- Logica de conversion ---#
	# Seteo la transferencia de dominios en True para que se copien las
	# columnas con descripciones de los códigos
	arcpy.env.transferDomains = True	
	arcpy.conversion.FeatureClassToFeatureClass(inFeatures, outLocation, outName)
	
	
	#--- Limpiado de tablas de salida ---#
	# Me muevo al directorio de salida
	arcpy.env.workspace = outLocation
	dict_de_fields_a_borrar = obtener_dict_de_fields_a_borrar(outName)
	# Si hay valores en el campo de descripciones que quedaron vacios,
	# copio los que tiene el campo a borrar
	transferir_valores_si_null(outName, dict_de_fields_a_borrar)
	# Elimino todos los fields de la lista
	for field in dict_de_fields_a_borrar.values():
		arcpy.DeleteField_management(outName, field)

	#--- Restauracion de nombres de campos ---#
	for key in dict_de_fields_a_borrar.iterkeys():
		renameFields_logica.renameFields(outName, key, dict_de_fields_a_borrar[key])

	

	
# manejo de excepciones
except arcpy.ExecuteError:
	print arcpy.GetMessages(2)
	arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
	print e.args[0]
	arcpy.AddError(e.args[0])

