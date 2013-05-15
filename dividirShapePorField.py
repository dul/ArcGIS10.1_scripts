import os
import sys
import arcpy
 
"""
Summary
	Recibe un .shp y un field. Genera un .shp por cada valor distinto de field.
	Los archivos generados se nombran: shapeAdividir + field + número + .shp. 
	Ejemplo: se ingresa el archivo 'Red_Vial.shp' y se lo quiere dividir por 
	el campo 'Tipo'. Los archivos generados serán: Red_VialTipo0.shp, Red_VialTipo1.shp...

Para el seteo de Parámetros:
	1er parámetro: Shape a dividir. Tipo: Capa de entidades.
		Propiedades:
			Tipo: Required
			Dirección: Input
			Valor múltiple: No
			Filtro: Ninguno
	2do parámetro: Campo. Tipo: Campo
		Propiedades:
			Tipo: Required
			Dirección: Input
			Valor múltiple: No
			Filtro: Ninguno
			Obtenido de: Shape_a_dividir (permite que al elegir el campo se desplieguen 
			las posibilidades de acuerdo a los campos que conteine el shape a dividir)
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
