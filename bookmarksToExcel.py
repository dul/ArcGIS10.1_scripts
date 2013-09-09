import os
import sys
import csv
import arcpy
"""
Summary
"""


try:
	archivoMapa = arcpy.GetParameterAsText(0)
	csv_out1 = arcpy.GetParameterAsText(1)
	
	
	mapa = arcpy.mapping.MapDocument(archivoMapa)
	csv_out = open(csv_out1, 'wb')
	my_writer = csv.writer(csv_out, delimiter=';')
	
	for marcador in arcpy.mapping.ListBookmarks(mapa):
		my_writer.writerow([marcador.name, marcador.extent.XMax, marcador.extent.XMin, marcador.extent.YMax, marcador.extent.YMin])
	
	csv_out.close()
	

# manejo de excepciones
except arcpy.ExecuteError:
	print arcpy.GetMessages(2)
	arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
	print e.args[0]
	arcpy.AddError(e.args[0])
