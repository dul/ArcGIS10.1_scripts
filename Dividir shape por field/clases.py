#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import arcpy
from os.path import basename


class CreadorDeDirectorio(object):
    """ Crea un nuevo directorio """
    
    def __init__(self, ubicacion, nombre=None):
        """
        initializes the class
        """
        self.ubicacion = ubicacion
        self.nombre = nombre
        # Dejo posicionado en el directorio ubicacion
        os.chdir(self.ubicacion)
    
    def nombrar_directorio (self, cadena):
		self.nombre = cadena
		
    def chequear_si_ya_existe (self):
		"""Devuelve true si ya existe el self.nombre en self.ubicacion"""
		return os.path.exists(self.nombre)
		
    def redefinir_nombre (self):
		"""Pre: self.nombre ya existe"""
 		i = 1
		nuevo_nombre = self.nombre+str(i)
		while (os.path.exists(nuevo_nombre)):
			i += 1
			nuevo_nombre = self.nombre+str(i)
		self.nombrar_directorio(nuevo_nombre)
		
    def crear_directorio (self):
		if self.chequear_si_ya_existe():
			self.redefinir_nombre()
		os.mkdir(self.nombre)
		return os.path.abspath(self.nombre)
    
    def borrar_directorio (self):
		if self.chequear_si_ya_existe():
			os.rmdir(self.nombre)
		else:
			raise TypeError	



class CreadorDeDirectorio_PorField (CreadorDeDirectorio):
	""" Crea un nuevo directorio con la palabra "_divididoPor_" """
	def nombrar_directorio (self, cadena1, cadena2):
		self.nombre = cadena1 + '_divididoPor_' + cadena2
		
	def redefinir_nombre (self):
		"""Pre: self.nombre ya existe"""
 		i = 1
		nuevo_nombre = self.nombre+str(i)
		while (os.path.exists(nuevo_nombre)):
			i += 1
			nuevo_nombre = self.nombre+str(i)
		self.nombre = nuevo_nombre


class ExtractorDeCampos (object):
	""" Recibe un field y una  feature class, shapefile, o tabla, usa 
	SearchCursor para guardar la lista de campos. """
	
	def __init__(self, in_feature, field):
		self.in_feature = in_feature
		self.field = field
		
		self.cursor = None
		self.listaFieldDistintos = []
	
	"""Setea un nuevo cursor en self.cursor"""
	def obtener_cursor (self):
		self.cursor = arcpy.SearchCursor(self.in_feature, None, None, self.field)
		
	"""Llama a obtener_cursor y devuelve la lista de campos únicos"""
	def obtener_lista (self):
		self.obtener_cursor()
		for valor in self.cursor:
			valori = valor.getValue(self.field)
			if valori not in self.listaFieldDistintos:
				self.listaFieldDistintos.append(valori)
		return self.listaFieldDistintos

class DivisorDeShapePorCampo (object):
	def __init__(self, shapeAdividir, campo):
		self.shapeAdividir = shapeAdividir
		self.campo = campo
		
	def dividir (self):
		creadorDeDirectorio = CreadorDeDirectorio_PorField (os.path.dirname(self.shapeAdividir))	
		carpetaDeDestino = creadorDeDirectorio.crear_directorio()

		generador = GeneradorDeNuevosShapes(self.shapeAdividir, self.campo, carpetaDeDestino)
		generador.generar()


class GeneradorDeNuevosShapes (object):
	
	def __init__ (self, shapeOriginal, field, ubicacion):

		self.shapeOriginal = shapeOriginal
		self.field = field
		self.carpetaDeDestino = ubicacion
	
	def generar (self):
		extractorDeCampos = ExtractorDeCampos(self.shapeAdividir, self.campo)
		lista = extractorDeCampos.obtener_lista()
		
