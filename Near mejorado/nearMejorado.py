import os
import sys
import arcpy
import ntpath
import shutil
"""
Summary

	Recibe
	- Capa de entidades salvaobstaculos (punto): capa de salvaobstaculos
	cuyas posiciones se quiere estudiar
	- Capa de entidades lineas1 (línea): primera capa de líneas sobre la 
	cual deberían ubicarse los puntos de salvaobstaculos
	- Capa de entidades lineas2 (línea): segunda capa de líneas sobre la 
	cual deberían ubicarse los puntos de salvaobstaculos
	- Carpeta carpetaDeDestino: directorio donde se desea colocar
	los archivos producidos por esta herramienta
	
	Devuelve
	Crea 3 archivos en carpetaDeDestino:
	- Capa de entidades InterseccionLinea1Linea2 (punto): contiene todos los puntos de intersección
	entre las capas lineas1 y lineas2 recibidas por parámetro.
	- Capa de entidades (punto): contiene todos los puntos en común entre
	la capa InterseccionLinea1Linea2 creada y la capa salvaobstaculos
	recibida por parámetro. Advertencia: SUELE QUEDAR VACÍA porque raramente
	hay un salvaobstáculos "bien" puesto...
	- Capa de entidades (polígonos): capa de anillos al rededor de los puntos
	de InterseccionLinea1Linea2. Los anillos se ubican a 10, 50, 100 y 200
	metros del centro. Sirve como referencia para comparar con la capa 
	salvaobstaculos.

	Especificación:
	1) Creo capa InterseccionLinea1Linea2 que contiene los puntos de interseccion
	entre dos capas de lineas Linea1 y Linea2
	2) Creo capa InterseccionInterseccionesSalvaobstaculos que conteine los puntos
	que coinciden entre los de la capa InterseccionLinea1Linea2 y los de la capa
	Salvaobstaculos
	3) Creo capa bufferInterseccionLinea1Linea2 con la herramienta
	MultipleRingBuffer_analysis, que crea polígonos circulares a 200,100,50,10
	metros de los puntos de InterseccionLinea1Linea2

"""


try:
	# Obtencion de los parámetros
	salvaobstaculos = arcpy.GetParameterAsText(0) # salvaosbstaculos
	lineas1 = arcpy.GetParameterAsText(1)
	lineas2 = arcpy.GetParameterAsText(2)
	carpetaDeDestino = arcpy.GetParameterAsText(3)

	# 1) Creo capa InterseccionLinea1Linea2 que contiene los puntos de interseccion
	# entre dos capas de lineas Linea1 y Linea2
	#~ nombreArchivoIntermedio = arcpy.ValidateTableName(ntpath.basename(lineas1)[:-4]+ntpath.basename(lineas2)[:-4])
	nombreArchivoIntermedio = arcpy.ValidateTableName('intermedio')
	nombreNuevoShape1 = os.path.join(carpetaDeDestino, nombreArchivoIntermedio)	
	arcpy.Intersect_analysis([lineas1,lineas2], nombreNuevoShape1, "ALL", "", "POINT")
	arcpy.AddMessage("primer intersect")
	# 2) Creo capa InterseccionInterseccionesSalvaobstaculos que conteine los puntos
	# que coinciden entre los de la capa InterseccionLinea1Linea2 y los de la capa
	# Salvaobstaculos
	nombreArchivoFinal = arcpy.ValidateTableName('final')
	nombreNuevoShape2 = os.path.join(carpetaDeDestino, nombreArchivoFinal)
	arcpy.Intersect_analysis([nombreNuevoShape1,salvaobstaculos], nombreNuevoShape2, "ALL", "", "POINT")
	arcpy.AddMessage("segundo intersect")
	# 3) Creo capa bufferInterseccionLinea1Linea2 con la herramienta
	# MultipleRingBuffer_analysis, que crea polígonos circulares a 200,100,50,10
	# metros de los puntos de InterseccionLinea1Linea2
	nombreArchivoBuffer = arcpy.ValidateTableName('buffer'+nombreArchivoIntermedio[:-4])
	nombreNuevoShape2 = os.path.join(carpetaDeDestino, nombreArchivoBuffer)
	arcpy.MultipleRingBuffer_analysis(nombreArchivoIntermedio, nombreNuevoShape2, [200,100,50,10], "Meters", None, None, None)




	#~ # 3) Agrego un campo "Coincide con interseccion" a Salvaobstaculos. Default: -1
	#~ arcpy.AddField_management(salvaobstaculos, "COINCIDE", "TEXT", "", "", "", "Ubicado sobre interseccion: 0", "", "")
	#~ arcpy.AssignDefaultToField_management (salvaobstaculos, "COINCIDE", "-1","")
	#~ # 4) A cada elemento de Salvaconductos que se halle en
	#~ # InterseccionInterseccionesSalvaconductos le pongo el valor 0 en "COINCIDE"
	#~ # al resto le pongo -1.
	#~ rowsSalvaobs = arcpy.UpdateCursor(salvaobstaculos)
	#~ for rowS in rowsSalvaobs: 
		#~ rowsIntersect = arcpy.SearchCursor(intersect_L1_l2_S)
		#~ for rowI in rowsIntersect:
			#~ if rowI.FID == rowS.FID:
				#~ rowS.COINCIDE = 0
				#~ rowsSalvaobs.updateRow(rowS)
		

# manejo de excepciones
except arcpy.ExecuteError:
	print arcpy.GetMessages(2)
	arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
	print e.args[0]
	arcpy.AddError(e.args[0])
