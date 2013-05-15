import os
import sys
import arcpy
 
""" Recibe un .shp y un field. Genera un .shp por cada valor distinto
de field.
"""
try:
	shapeAdividir = arcpy.GetParameterAsText(0)
	field = arcpy.GetParameterAsText(1)

	# obtención de fieldDistinto 
	listaFieldDistintos = []
	totalFields = arcpy.SearchCursor(shapeAdividir, None, None, field)
	for valor in totalFields:
		if valor.getValue(field) not in listaFieldDistintos:
			listaFieldDistintos.append(valor.getValue(field))
			
	c = 0
	for fieldDistinto in listaFieldDistintos:
		# nombre del nuevo shape generado
		nombreNuevoShape = shapeAdividir + field + str(c) + '.shp'
		c = c+1
		# generación del nuevo shape
		where_clause = '"'+ field + '"=\'' + fieldDistinto + '\''
		arcpy.Select_analysis(shapeAdividir, nombreNuevoShape, where_clause)


# manejo de excepciones
except arcpy.ExecuteError:
	print arcpy.GetMessages(2)
	arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
	print e.args[0]
	arcpy.AddError(e.args[0])
