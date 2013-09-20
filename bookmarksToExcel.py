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

import csv, codecs, cStringIO

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("latin-1")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="latin-1", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "latin-1") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="latin-1", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("latin-1") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("latin-1")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

"""Recibe un archivo csv nuevo (vacio) en modo lectura, la ruta csv_in donde se escribirá
y el mapa .mxd. Escribe todos los marcadores del mapa en csv_in."""
def escribir_sobre_archivo_nuevo(csv_in_lectura, csv_in, mapa):
	#Cierro 'csv_in_lectura'
	csv_in_lectura.close()
	#Abro 'csv_in' en modo escritura en 'csv_in_escritura'
	csv_in_escritura = open(csv_in, 'wb')
	my_writer = UnicodeWriter(csv_in_escritura, delimiter=';')
	# Escribo header en el archivo nuevo
	my_writer.writerow(["Nombre del marcador", "Estado", "Observaciones"])
	#Tomo los marcadores del mapa y los escribo en el archivo 
	#'csv_in_escritura'
	for marcador in arcpy.mapping.ListBookmarks(mapa):
		my_writer.writerow([marcador.name])
	#Cierro 'csv_in_escritura'
	csv_in_escritura.close()

"""Encargado de la logística de actualización de lista de marcadores. 
Agrega los nuevos y mantiene los comentarios de los pre-existentes."""
def actualizar_lista_de_marcadores(my_writer, my_reader, csv_in_lectura, mapa):
	# Escribo header en el archivo nuevo
	my_writer.writerow(["Nombre del marcador", "Estado", "Observaciones"])
	#Por cada marcador del mapa:
	for marcador in arcpy.mapping.ListBookmarks(mapa):
		#Si está en el archivo 'csv_in_lectura':
		
		encontrado = False
		for row in my_reader:
			nombreParaComparar = marcador.name.encode("latin-1")
			if nombreParaComparar==row["Nombre del marcador"]:
				encontrado = True
				#Copio toda la línea que figura en 'csv_in_ectura' para 
				#ese marcador en 'csv_out_escritura'
				if row["Estado"] == None:
					campoEstado = ""
				else:
					campoEstado = row["Estado"]
				if row["Observaciones"] == None:
					campoObs = ""
				else:
					campoObs = row["Observaciones"]
				
				valoresAescribir = [marcador.name,campoEstado,campoObs]
				my_writer.writerow(valoresAescribir)
				break

		#Si no está en el archivo 'csv_in_lectura':
		if encontrado == False:
			#Agrego el marcador a 'csv_out'
			my_writer.writerow([marcador.name])
		
		csv_in_lectura.seek(0)

"""Recibe un archivo csv no vacío en modo lectura, la ruta csv_in donde 
se escribirá y el mapa .mxd. Escribe todos los marcadores nuevos del mapa 
en csv_in conservando los comentarios de los marcadores pre-existentes 
en el csv_in (llamando a actualizar_lista_de_marcadores)"""
def escribir_sobre_archivo_no_vacio (csv_in_lectura, mapa, csv_in):
	#Creo un archivo nuevo en modo escritura en 'csv_out_escritura', 
	#llamado 'temp.csv'
	csv_out_escritura = open('temp.csv','wb')
	my_writer = UnicodeWriter(csv_out_escritura, delimiter=';')
	#Cierro csv_in como 'ab' y abro como 'rb'
	csv_in_lectura.close()
	csv_in_lectura = open(csv_in, 'rb')
	my_reader = csv.DictReader(csv_in_lectura, delimiter=';')
	
	actualizar_lista_de_marcadores(my_writer, my_reader, csv_in_lectura, mapa)

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
