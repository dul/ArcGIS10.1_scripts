import arcpy
import renameFields_logica
import os
from os import path


#~ Version 2

import csv, codecs, cStringIO


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, encoding, f, dialect=csv.excel, **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
        self.encoding = encoding

    def writerow(self, row):
        self.writer.writerow([s.encode("cp1252") for s in row])
        # Fetch cp1252 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("cp1252")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_#
#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_#
#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_#


def obtener_lista_de_Campos (inFeature):
	return arcpy.ListFields(inFeature)

def crear_csv_escritura (nombre, outLocation):
	nombre = os.path.join(outLocation,nombre+'.csv')
	archivo_csv = open(nombre, 'wb')

	return archivo_csv

def cerrar_csv_escritura (archivo):
	archivo.close()


"""Recibe una lista con los campos correctos, una lista con los campos
incorrectos y un archivo abierto. Escribe ambas listas encolumnadas
una al lado de la otra."""
def escribir_listas_archivo (listaDeCamposCorrectos, listaDeCamposIncorrectos, archivo):
	my_writer = UnicodeWriter("cp1252", archivo, delimiter= ';')
	my_writer.writerow(['Nombre de atributo en Shapefile','Nombre de atributo en GDB'])
	i = 0
	while i < len(listaDeCamposIncorrectos):
		my_writer.writerow([ listaDeCamposIncorrectos[i].name, listaDeCamposCorrectos[i].name])
		i=i+1
	if (len(listaDeCamposIncorrectos) < len(listaDeCamposCorrectos)):
		while i < len(listaDeCamposCorrectos):
			my_writer.writerow(['???',listaDeCamposCorrectos[i].name])
			i = i+1

"""Recibe una GDB y una carpeta de salida. Se recorren todos los datasets
de la gdb y se obtienen todas las features que contienen. Por cada una de
ellas, se la exporta a shapefile en la carpeta de salida y se genera un 
.csv con las listas de atributos como aparecen en la gdb y de los mismos 
tal cual aparecen en el shapefile exportado. Los archivos .csv son 
nombrados agregando _atributos.csv al final del nombre de la feature
y se ubican en la misma carpeta de salida de exportación."""
def escribir_archivos_atributos (GDB, outLocation):
	arcpy.env.workspace = GDB
	datasets = arcpy.ListDatasets('','Feature')

	for dataset in datasets:
		arcpy.env.workspace = GDB + '\'' + dataset
		for feature in arcpy.ListFeatureClasses():
		
			# Reseteo listas
			lista_nombres_correctos = []
			lista_nombres_incorrectos = []
			
			# Obtengo los nombres de los campos tal cual figuran en la gdb
			lista_nombres_correctos = obtener_lista_de_Campos(feature)
			
			# Exporto con FeatureClassToFeatureClass
			nuevo_nombre = feature+'_exp.shp'
			arcpy.conversion.FeatureClassToFeatureClass(feature, outLocation, nuevo_nombre)

			# Obtengo los nombres de los campos como figuran en el shapefile
			# recién creado
			lista_nombres_incorrectos = obtener_lista_de_Campos(os.path.join(outLocation, nuevo_nombre))
			
			# Chequeo que se hayan exportado todos los campos desde la gdb.
			# Si algunos campos se perdieron en la exportación, aviso.
			if len(lista_nombres_incorrectos) != len(lista_nombres_correctos):
				arcpy.AddWarning("En el archivo "+ nuevo_nombre + " la lista de campos exportados es de largo "+str(len(lista_nombres_incorrectos))+" mientras que la cantidad de campos original era "+str(len(lista_nombres_correctos)))
			
			# Creo y escribo en un archivo feature_atributos.csv las 
			# listas de atributos
			archivo_atributos = crear_csv_escritura(os.path.basename(feature)+'_atributos', outLocation)
			escribir_listas_archivo (lista_nombres_correctos, lista_nombres_incorrectos, archivo_atributos)
			cerrar_csv_escritura(archivo_atributos)




"""Recibe una lista de objetos tipo domain y un archivo csv abierto vacío.
Escribe los atributos name, description, value y description por c/1"""
def escribir_archivo_dominios (domains, archivo):
	my_writer = UnicodeWriter("cp1252", archivo, delimiter= ';')
	my_writer.writerow(['Nombre del dominio', 'Descripcion del dominio','Codigo','Descripcion del codigo'])
	for domain in domains:
		if domain.domainType == 'CodedValue':
			coded_values = domain.codedValues
			for val, desc in coded_values.iteritems():
				if type(val) == int:
					val = str(val)
				my_writer.writerow([domain.name, domain.description, val, desc])

		elif domain.domainType == 'Range':
			my_writer.writerow([domain.name, domain.description, 'Min: ',domain.range[0]])
			my_writer.writerow([domain.name, domain.description, 'Max: ',domain.range[1]])



"""Recibe la direccion de una geodatabase y una carpeta outLocation.
Crea y abre un archivo .csv vacio llamado GDB[:-4]_dominios.csv en outLocation
Llama a escribir_archivo_dominios y cierra el archivo"""
def logica_dominios (GDB, outLocation):
	# Obtengo dominios DE TODA LA GEODATABASE
	dict_dominios = arcpy.da.ListDomains(GDB)
	# Creo archivo GDB[:-4]_dominios.csv en outLocation y lo abro en forma de escritura.
	archivo_dominios = crear_csv_escritura(os.path.basename(GDB)[:-4]+'_dominios', outLocation)
	escribir_archivo_dominios (dict_dominios, archivo_dominios)
	cerrar_csv_escritura(archivo_dominios)



try:

	GDB = arcpy.GetParameterAsText(0)
	outLocation = arcpy.GetParameterAsText(1)
	
	escribir_archivos_atributos (GDB, outLocation)
	logica_dominios (GDB, outLocation) 

	

# manejo de excepciones
except arcpy.ExecuteError:
	print arcpy.GetMessages(2)
	arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
	print e.args[0]
	arcpy.AddError(e.args[0])




