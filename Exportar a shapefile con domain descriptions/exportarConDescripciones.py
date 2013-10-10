import arcpy

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

# Recibe una feature class y guarda en una lista todos los campos de código
# que serán borrados luego. Devuelve la lista.
def obtener_lista_de_fields_a_borrar (outName):
	lista_de_fields_a_borrar = []
	
	# Por cada campo que empiece con d_
	for field_d in arcpy.ListFields(outName, 'd_*'):
		campoActual = field_d.name
		
		# Itero sobre todos los campos
		for field_c in arcpy.ListFields(outName):
			# Si coinciden los primeros 8 caracteres de field_c, lo
			# guardo en la lista_de_fields_a_borrar
			if (corresponde(field_c.name, field_d.name)):
				lista_de_fields_a_borrar.append(field_c.name)

	return lista_de_fields_a_borrar




try:

	inFeatures = arcpy.GetParameterAsText(0)
	outLocation = arcpy.GetParameterAsText(1)
	outName = arcpy.GetParameterAsText(2)
	
	#--- Lógica de conversión ---#
	# Seteo la transferencia de dominios en True para que se copien las
	# columnas con descripciones de los códigos
	arcpy.env.transferDomains = True	
	arcpy.conversion.FeatureClassToFeatureClass(inFeatures, outLocation, outName)
	
	
	#--- Limpiado de tablas de salida ---#
	
	# Me muevo al directorio de salida
	arcpy.env.workspace = outLocation
	lista_de_fields_a_borrar = obtener_lista_de_fields_a_borrar(outName)
	# Elimino todos los fields de la lista
	for field in lista_de_fields_a_borrar:
		arcpy.DeleteField_management(outName, field)


	
# manejo de excepciones
except arcpy.ExecuteError:
	print arcpy.GetMessages(2)
	arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
	print e.args[0]
	arcpy.AddError(e.args[0])
