import os
import sys
import csv
import arcpy
from os import remove
from shutil import move

"""
Summary
	Recibe un mapa .mxd y el nombre un archivo .csv que puede ser nuevo
	o pre-existente (ubicado en el directorio del mapa). 
	Copia los marcadores del mapa en el .csv, conservando
	la información de los marcadores pre-existentes si existían.
	Por cada marcador (chequeado por nombre) nuevo, si ya se encuentra en 
	el archivo viejo, copia la info adicional (Estado / Observaciones) 
	del viejo al nuevo; si no se encuentra, lo agrega. Los marcadores 
	presentes en el viejo que no aparecen en el nuevo, no se agregan 
	(se consideran borrados).
Para el seteo de Parámetros:
	1er parámetro: Mapa (Documento de ArcMap).
		Propiedades:
			Tipo: Required
			Dirección: Input
			Valor múltiple: No
			Filtro: Ninguno
	2do parámetro: Nombre de archivo .csv (Cadena de caracteres). Ejemplo:
	"marcadores.csv". Se buscará en el directorio donde se encuentra el 
	mapa y se creará en el mismo si todavía no existe.
		Propiedades:
			Tipo: Required
			Dirección: Input
			Valor múltiple: No
			Filtro: Ninguno
"""

"""Recibe un archivo csv nuevo (vacio) en modo lectura, la ruta csv_in donde se escribirá
y el mapa .mxd. Escribe todos los marcadores del mapa en csv_in."""
def escribir_sobre_archivo_nuevo(csv_in_lectura, csv_in, mapa):
	#Cierro 'csv_in_lectura'
	csv_in_lectura.close()
	#Abro 'csv_in' en modo escritura en 'csv_in_escritura'
	csv_in_escritura = open(csv_in, 'wb')
	my_writer = csv.writer(csv_in_escritura, delimiter=';')
	# Escribo header en el archivo nuevo
	my_writer.writerow(["Nombre del marcador", "Estado", "Observaciones"])
	#Tomo los marcadores del mapa y los escribo en el archivo 
	#'csv_in_escritura'
	for marcador in arcpy.mapping.ListBookmarks(mapa):
		arcpy.AddMessage("Voy a escribir "+marcador.name)
		my_writer.writerow([marcador.name])
	#Cierro 'csv_in_escritura'
	csv_in_escritura.close()

"""Encargado de la logística de actualización de lista de marcadores. 
Agrega los nuevos y mantiene los comentarios de los pre-existentes."""
def actualizar_lista_de_marcadores(my_writer, my_reader, mapa):
	# Escribo header en el archivo nuevo
	my_writer.writerow(["Nombre del marcador", "Estado", "Observaciones"])
	#Por cada marcador del mapa:
	for marcador in arcpy.mapping.ListBookmarks(mapa):
		#Si está en el archivo 'csv_in_lectura':
		encontrado = False
		for row in my_reader:
			if my_reader.line_num == 0:
				pass
			elif marcador.name==row[0]:
				encontrado = True
				#Copio toda la línea que figura en 'csv_in_ectura' para 
				#ese marcador en 'csv_out_escritura'
				my_writer.writerow(row)
				break

		#Si no está en el archivo 'csv_in_lectura':
		if encontrado == False:
			#Agrego el marcador a 'csv_out'
			my_writer.writerow([marcador.name])


"""Recibe un archivo csv no vacío en modo lectura, la ruta csv_in donde 
se escribirá y el mapa .mxd. Escribe todos los marcadores nuevos del mapa 
en csv_in conservando los comentarios de los marcadores pre-existentes 
en el csv_in (llamando a actualizar_lista_de_marcadores)"""
def escribir_sobre_archivo_no_vacio (csv_in_lectura, mapa, csv_in):
	#Creo un archivo nuevo en modo escritura en 'csv_out_escritura', 
	#llamado 'temp.csv'
	csv_out_escritura = open('temp.csv','wb')
	my_writer = csv.writer(csv_out_escritura, delimiter=';')
	#Cierro csv_in como 'ab' y abro como 'rb'
	csv_in_lectura.close()
	csv_in_lectura = open(csv_in, 'rb')
	my_reader = csv.reader(csv_in_lectura, delimiter=';')
	
	actualizar_lista_de_marcadores(my_writer, my_reader, mapa)

	#Cierro 'csv_out_escritura'
	csv_out_escritura.close()
	#Cierro 'csv_in_lectura'
	csv_in_lectura.close()
	#Sobreescribo el contenido de 'csv_in' con el contenido de 'csv_out'
	remove(csv_in)
	move('temp.csv', csv_in)



try:
	#Recibo un mapa y el nombre de un archivo .csv que guardo en la 
	#variable 'csv_in'
	archivoMapa = arcpy.GetParameterAsText(0)
	csv_in = arcpy.GetParameterAsText(1)
	
	#Chequeo que el formato del archivo sea .csv
	if csv_in.endswith(".csv")== False:
		arcpy.AddWarning("El formato del archivo ingresado no es valido. Ingrese unicamente archivos .csv")
		arcpy.AddError(arcpy.GetMessages(2))
	else:
		mapa = arcpy.mapping.MapDocument(archivoMapa)
		#Abro 'csv_in' en modo lectura en 'csv_in_lectura'
		csv_in_lectura = open(csv_in, 'ab')
		#Si el csv_in no está vacío:
		if os.path.getsize(csv_in) > 0:
			escribir_sobre_archivo_no_vacio(csv_in_lectura, mapa, csv_in)
			
		# Si el csv_in está vacío:
		else:
			escribir_sobre_archivo_nuevo(csv_in_lectura, csv_in, mapa)


# manejo de excepciones
except arcpy.ExecuteError:
	arcpy.AddError(arcpy.GetMessages(2))
except csv.Error as e:
	arcpy.AddWarning("Error al intentar escribir sobre el archivo .csv.")
	arcpy.AddError(e.args[0])
except IOError as e:
	arcpy.AddWarning("Error. Puede ser que otro programa esté usando el archivo. Ciérrelo y vuelva a ejecutar la herramienta.")
	arcpy.AddError(e.args[0])
except Exception as e:
	arcpy.AddWarning("Error no identificado.")
	arcpy.AddError(e.args[0])
