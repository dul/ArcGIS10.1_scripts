import arcpy
import os
from os import path

class ToolValidator(object):
	"""Class for validating a tool's parameter values and controlling
	the behavior of the tool's dialog."""

	def __init__(self):
		"""Setup arcpy and the list of tool parameters."""
		self.params = arcpy.GetParameterInfo()

	def initializeParameters(self):
		"""Refine the properties of a tool's parameters.  This method is
		called when the tool is opened."""
		return
	
	def updateParameters(self):
		if self.params[0].value:
			if not self.params[0].altered:
				self.params[0].value = []
			else:
				gdb = self.params[0].value
				lista = []
				for dirpath, dirnames, filenames in arcpy.da.Walk(gdb, datatype="FeatureClass"):
					for filename in filenames:
						lista.append(os.path.join(dirpath, filename))
				lista = sorted(set(lista))
			
				for val in lista:
					val = str(val.encode('cp1252'))

				self.params[2].filter.list = lista
				#~ if self.params[2].value not in self.params[2].filter.list:
					#~ self.params[2].value = self.params[2].filter.list[0]

					
		return


	def updateMessages(self):
		"""Modify the messages created by internal validation for each tool
		parameter.  This method is called after internal validation."""
		return





import arcpy
import os
from os import path

class ToolValidator(object):
	"""Class for validating a tool's parameter values and controlling
	the behavior of the tool's dialog."""

	def __init__(self):
		"""Setup arcpy and the list of tool parameters."""
		self.params = arcpy.GetParameterInfo()

	def initializeParameters(self):
		"""Refine the properties of a tool's parameters.  This method is
		called when the tool is opened."""
		return
	
	def updateParameters(self):
		if self.params[0].value:
			if not self.params[0].altered:
				self.params[0].value = []
			else:
				gdb = self.params[0].value
				lista = []
				for dirpath, dirnames, filenames in arcpy.da.Walk(gdb, datatype="FeatureClass"):
					for filename in filenames:
						lista.append(os.path.join(dirpath, filename))
				lista = sorted(set(lista))
			
				for val in lista:
					val = str(val.encode('cp1252'))

				self.params[2].filter.list = lista
				try:
					if self.params[2].value not in self.params[2].filter.list:
						self.params[2].value = self.params[2].filter.list[0]

				except Exception:
					raise NameError(self.params[2].filter.list)
					
		return
import arcpy
import os
from os import path

class ToolValidator(object):
	"""Class for validating a tool's parameter values and controlling
	the behavior of the tool's dialog."""

	def __init__(self):
		"""Setup arcpy and the list of tool parameters."""
		self.params = arcpy.GetParameterInfo()

	def initializeParameters(self):
		"""Refine the properties of a tool's parameters.  This method is
		called when the tool is opened."""
		return
	
	def updateParameters(self):
		if self.params[0].value:
			if not self.params[0].altered:
				self.params[0].value = []
			else:
				gdb = self.params[0].value
				lista = []
				for dirpath, dirnames, filenames in arcpy.da.Walk(gdb, datatype="FeatureClass"):
					for filename in filenames:
						lista.append(os.path.join(dirpath, filename))
				lista = sorted(set(lista))
			
				for val in lista:
					val = str(val.encode('cp1252'))

				self.params[2].value = lista

					
		return


	def updateMessages(self):
		"""Modify the messages created by internal validation for each tool
		parameter.  This method is called after internal validation."""
		return

	def updateMessages(self):
		"""Modify the messages created by internal validation for each tool
		parameter.  This method is called after internal validation."""
		return






a = 'C:\\Documents and Settings\\mlauria\\Escritorio\\SIG IGN octubre 12 2012\\BDSGIGN.gdb'
>>> for each in arcpy.Describe(a).children:
...     if each.dataType == "FeatureDataset":
...         print each.file
...         
Comunicacion
Energia
Estructuras_Economicas
Habitacional_y_Cultural
Hidrografia
Hojas
Instituciones_Publicas_y_de_Seg
Limite
Localidad
Redes_Geodesicas
Relieve
Reservorio_de_Agua
Suelos
Transporte
Vegetacion

for path, path_names, data_names in arcpy.da.Walk(gdb_path, datatype= "FeatureClass"):
...     print path
...     for each in data_names:
...         print each
C:\Documents and Settings\mlauria\Escritorio\SIG IGN octubre 12 2012\BDSGIGN.gdb
Zonaplan2012
Zona_de_Trabajo
Z_Vargas
C:\Documents and Settings\mlauria\Escritorio\SIG IGN octubre 12 2012\BDSGIGN.gdb\Comunicacion
Lineas_de_Transmision_com
Obras_de_Comunicacion_com
C:\Documents and Settings\mlauria\Escritorio\SIG IGN octubre 12 2012\BDSGIGN.gdb\Energia
Complejo_de_Energia_Ene
Area_de_Energia_Ene
Líneas_de_Conduccion_Ene
C:\Documents and Settings\mlauria\Escritorio\SIG IGN octubre 12 2012\BDSGIGN.gdb\Estructuras_Economicas
Areas_Actividades_Economicas
Areas_Actividades_Agropecuarias
Actividades_Economicas
Actividades_Agropecuarias
C:\Documents and Settings\mlauria\Escritorio\SIG IGN octubre 12 2012\BDSGIGN.gdb\Habitacional_y_Cultural
Edif_Construcciones_Turisticas
Otras_Edificaciones
Edif_Religiosos
Edif_Educacion
Edif_Depor_y_Esparcimiento
Areas_de_Educacion
Areas_Religiosas
Areas_Deportivas_y_Esparcimiento
AOE
C:\Documents and Settings\mlauria\Escritorio\SIG IGN octubre 12 2012\BDSGIGN.gdb\Hidrografia
Espejos_de_Agua_Hid
Curso_de_Agua_Hid
Nodos_Red_Hid
Rapido_Hid
Isla_Hid
Banco_de_Arena
Obra_Portuaria_Hid
Fuente_De_Agua_Hid
Caida_de_Agua
C:\Documents and Settings\mlauria\Escritorio\SIG IGN octubre 12 2012\BDSGIGN.gdb\Hojas
Zona_Santa_Fe
Hojas500
Hojas250
Hojas100
Hojas050
Hojas025
C:\Documents and Settings\mlauria\Escritorio\SIG IGN octubre 12 2012\BDSGIGN.gdb\Instituciones_Publicas_y_de_Seg
Edificio_Publico_IPS
Edificio_de_Seguridad_IPS
Edificio_de_Salud_IPS
Area_Pública_IPS
Area_Seguridad_IPS
Area_de_Salud_IPS
Area_Militar_IPS
C:\Documents and Settings\mlauria\Escritorio\SIG IGN octubre 12 2012\BDSGIGN.gdb\Limite
Pais_Lim
Municipio_Departamento_Comunas_Lim
Limite_Político_Administrativo_Lim
Unidades_Conservacion_Lim
Limite_de_Parcela_Rural
LPA_Publi
provincias_Lim
C:\Documents and Settings\mlauria\Escritorio\SIG IGN octubre 12 2012\BDSGIGN.gdb\Localidad
Ejido
Localidad
LocalidadAnno
C:\Documents and Settings\mlauria\Escritorio\SIG IGN octubre 12 2012\BDSGIGN.gdb\Redes_Geodesicas
Rg
RR
C:\Documents and Settings\mlauria\Escritorio\SIG IGN octubre 12 2012\BDSGIGN.gdb\Relieve
Curvas_de_Nivel
Puntos_del_Terreno
Marcas_y_Señales
Puntos_de_alturas_Topograficas
Acc_Terreno
Acc_Terreno_Pol
C:\Documents and Settings\mlauria\Escritorio\SIG IGN octubre 12 2012\BDSGIGN.gdb\Reservorio_de_Agua
Areas_Reservorio_Agua
Estructuras_Reservorio_de_Agua
C:\Documents and Settings\mlauria\Escritorio\SIG IGN octubre 12 2012\BDSGIGN.gdb\Suelos
Sue_Hidromorfologico
Sue_Costero
Sue_Consolidado
Sue_Congelado
Sue_No_Consolidado
C:\Documents and Settings\mlauria\Escritorio\SIG IGN octubre 12 2012\BDSGIGN.gdb\Transporte
Calle
Muro_Embalse
Edificios_Ferroviarios
Infraestuctura_Hidro
Señalizaciones
Estructuras_Portuarias
Infraest_aeroportuaria_Punto
Infraest_aeroportuaria_Linea
Red_Ferroviaria
Estructura_de_Transporte_Poligono
Estructura_de_Transporte_Puntos
Infraestructura_Ferroviaria
Nodo_Red_Ferroviaria
Nodo_Red_Vial
Puente_Red_Vial_Linea
Puente_Red_Vial_Punto
Salvado_de_Obstaculo
Vias_Secundarias
Red_Vial
Estructuras_Portuarias_Poligono
Estructuras_Portuarias_linea
Infraest_aeroportuaria_Poly
C:\Documents and Settings\mlauria\Escritorio\SIG IGN octubre 12 2012\BDSGIGN.gdb\Vegetacion
Veg_Arbustiva
Veg_Arborea
Veg_Culltivos
Veg_Herbacea
Veg_Hidrofila
Veg_Suelo_Desnudo

import arcpy
class ToolValidator(object):
	"""Class for validating a tool's parameter values and controlling
	the behavior of the tool's dialog."""

	def __init__(self):
		"""Setup arcpy and the list of tool parameters."""
		self.params = arcpy.GetParameterInfo()

	def initializeParameters(self):
		"""Refine the properties of a tool's parameters.  This method is
		called when the tool is opened."""
		return

	def updateParameters(self):
		"""Modify the values and properties of parameters before internal
		validation is performed.  This method is called whenever a parmater
		has been changed."""
		if self.params[0].value:
			if self.params[0].altered: # Si cambia la entrada de GDB
				gdb = self.params[0].value
				for path, path_names, data_names in arcpy.da.Walk(gdb, datatype= "FeatureClass"):
					try:
						if self.params[2].values:
							oldValues = self.params[2].values
					except Exception:
						pass
					values = set()
					newValues = self.params[2].filter.list
					try:
						if len(oldValues):
							self.params[2].values = [v for v in oldVaues if v in newValues]
					except Exception:
						pass
		return
		
	def updateParameters(self):
		if self.params[0].value:
			if self.params[0].altered:
				gdb = self.params[0].value
				lista = []
				for dirpath, dirnames, filenames in arcpy.da.Walk(gdb, datatype="FeatureClass"):
					for filename in filenames:
						lista.append(os.path.join(dirpath, filename))
				lista = sorted(set(lista))
			
				for val in lista:
					val = str(val.encode('cp1252'))

				self.params[2].filter.list = lista
			
				if self.params[2].value not in self.params[2].filter.list:
					self.params[2].value = self.params[2].filter.list[0]
			
		return
gdb = a
lista = []
for dirpath, dirnames, filenames in arcpy.da.Walk(gdb, datatype="FeatureClass"):
	for filename in filenames:
		lista.append(os.path.join(dirpath, filename))
lista = sorted(set(lista))
try:
	for val in lista:
		val = val.encode('cp1252')
	print lista

except Execution Error:
	print 'Error. Tipo de lista: '+ type(lista)+' , tipo de val: '+ type(val)



	def updateMessages(self):
		"""Modify the messages created by internal validation for each tool
		parameter.  This method is called after internal validation."""
		return


def updateParameters(self):
    # Update the value list filter in the second parameter based on the
    #   shape type in the first parameter
    #     
    gdb = self.params[0].value # agarro al gdb
	for path, path_names, data_names in arcpy.da.Walk(gdb_path, datatype= "FeatureClass"):
		print path
		for each in data_names:
			print each
    return
