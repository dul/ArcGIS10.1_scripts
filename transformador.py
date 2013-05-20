# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# transformador.py
# Description: Recibe un directorio de entrada. Busca todos los archivos .shp en el directorio
# y les ejecuta la funcion Proyectar. Crea un nuevo directorio hermano del de
# entrada y pone los archivos de salida en éste.
# Ejemplo de ejecución unitaria de Proyectar:
#~ # Local variables:
#~ Complejo_de_Energia_Ene = "Complejo_de_Energia_Ene"
#~ f3 = "C:\\Documents and Settings\\mlauria\\Escritorio\\pruebas sig\\SIG_IGN2011_24nov11\\f3"
#~ # Process: Proyectar
#~ arcpy.Project_management(Complejo_de_Energia_Ene, f3, "PROJCS['POSGAR_1994_Argentina_Zone_3',GEOGCS['GCS_POSGAR_1994',DATUM['D_POSGAR_1994',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',3500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-66.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',-90.0],UNIT['Meter',1.0]]", "POSGAR_1994_To_WGS_1984_1", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433],METADATA['World',-180.0,-90.0,180.0,90.0,0.0,0.0174532925199433,0.0,1262]]")
# Notas: si algún archivo necesita del parámetro Transformación geográfica,
# no lo convertirá. Genera un mensaje informativo por cada archivo no
# convertido. 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os


try:
	directorioDeEntrada = arcpy.GetParameterAsText(0)
	sistemaDeCoordenadasDeEntrada = arcpy.GetParameterAsText(1) #opcional
	sistemaDeCoordenadasDeSalida = arcpy.GetParameterAsText(2)
	#~ transformacionGeografica = arcpy.GetParameterAsText(3) #opcional

	# creacion de nuevo directorio
	os.chdir(os.path.dirname(directorioDeEntrada))
	nuevoDirectorio = directorioDeEntrada + 'Proyectado'
	os.mkdir(nuevoDirectorio)

	# obtencion de archivos .shp en directorioDeEntrada
	listaArchivos = []
	for archivo in os.listdir(directorioDeEntrada):
		if archivo.endswith(".shp"):
			# ejecucion de Proyectar
			nombreNuevoShape = os.path.join(nuevoDirectorio, archivo)
			try:
				arcpy.Project_management(archivo, nombreNuevoShape, sistemaDeCoordenadasDeSalida, None, sistemaDeCoordenadasDeEntrada)
			except:
				 arcpy.AddMessage("El archivo " + archivo + " no pudo ser convertido.")

# manejo de excepciones
except arcpy.ExecuteError:
	print arcpy.GetMessages(2)
	arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
	print e.args[0]
	arcpy.AddError(e.args[0])
