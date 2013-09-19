import os
import sys
import arcpy

"""
Summary

"""


try:
	# Obtencion de los parámetros
	capa1 = arcpy.GetParameterAsText(0) # salvaosbstaculos
	capa2 = arcpy.GetParameterAsText(1)
	capa3 = arcpy.GetParameterAsText(2)
	search_radius = arcpy.GetParameterAsText(3)
	location = arcpy.GetParameterAsText(4)
	angle = arcpy.GetParameterAsText(5)
	
	arcpy.DeleteField_management(capa1, ["NEAR_DIST", "NEAR_FC", "NEAR_FID"])
	arcpy.DeleteField_management(capa2, ["NEAR_DIST", "NEAR_FC", "NEAR_FID"])
	arcpy.DeleteField_management(capa3, ["NEAR_DIST", "NEAR_FC", "NEAR_FID"])
	# En el campo NEAR_DIST de capa3, guardo las mínimas distancias con capa2
	arcpy.Near_analysis(capa3, capa2, search_radius, location, angle)
	arcpy.AddMessage("Paso el primer near")
	# Guardo en el nuevo shp 'temp.shp', los elementos de capa1
	# cuyo valor de NEAR_DIST sea 0
	temp = arcpy.Select_analysis(capa3, 'temp.shp', '"NEAR_DIST" < 0.5')
	arcpy.AddMessage("Paso el select")
	# En el campo NEAR_DIST de capa1, guardo las mínimas distancias con
	# 'temp.shp'
	arcpy.Near_analysis(capa1, temp, search_radius, location, angle)
	arcpy.AddMessage("Paso el segundo near")
	arcpy.Delete_management(temp)
	arcpy.AddMessage("Paso el delete")

# manejo de excepciones
except arcpy.ExecuteError:
	print arcpy.GetMessages(2)
	arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
	print e.args[0]
	arcpy.AddError(e.args[0])
