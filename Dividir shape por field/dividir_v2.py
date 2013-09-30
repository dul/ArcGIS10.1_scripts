import os
import sys
import arcpy
import shutil
import ntpath

"""
Version 2
Updates: CAMBIAR NOMBRE DE OUTPUTS. En lugar de shapeAdividir + field + número + .shp
que sea shapeAdividir + field + valorDeField + .shp

Summary
	Recibe un .shp y un field. Genera un .shp por cada valor distinto de field.
	Los archivos generados se nombran: shapeAdividir + field + número + .shp
	y se ubican en un direcotrio nuevo llamado shapeAdividir + '_divididoPor_' + field
	Si el directorio ya existe, creo otro con el numero de copia al final del nombre.
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
	# Obtencion de los parámetros
	shapeAdividir = arcpy.GetParameterAsText(0)
	field = arcpy.GetParameterAsText(1)
	
	# creacion de nuevo directorio con nombre shapeAdividir + '_divididoPor_' + field
	os.chdir(os.path.dirname(shapeAdividir))
	nuevoDirectorio = shapeAdividir[:-4] + '_divididoPor_' + field
	# Si el directorio ya existe, creo otro con el numero de copia al final del nombre
	if (os.path.exists(nuevoDirectorio)):
		i = 1
		while (os.path.exists(nuevoDirectorio+str(i))):
			i = i+1
		nuevoDirectorio = nuevoDirectorio + str(i)
	os.mkdir(nuevoDirectorio)
	
	# obtencion de fieldDistinto 
	listaFieldDistintos = []
	totalFields = arcpy.SearchCursor(shapeAdividir, None, None, field)
	for valor in totalFields:
		if valor.getValue(field) not in listaFieldDistintos:
			listaFieldDistintos.append(valor.getValue(field))

	#~ c = 0
	for fieldDistinto in listaFieldDistintos:
		# nombre del nuevo shape generado
		nombreNuevoArchivo = arcpy.ValidateFieldName(ntpath.basename(shapeAdividir)[:-4] + fieldDistinto)
		nombreNuevoShape = os.path.join(nuevoDirectorio, nombreNuevoArchivo)
		arcpy.AddMessage(nombreNuevoShape)

		#~ c = c+1
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
