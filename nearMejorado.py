import os
import sys
import arcpy

"""
Summary

Análisis de la problemática:
Se quiere analizar la distancia X que puede eventualmente existir entre 
elementos de una capa de salvaobstáculos y las intersecciones entre los
elementos lineales sobre los cuales deberían estar ubicados. Se entiende 
que si un salvaobstáculos está perfectamente ubicado sobre el obstáculo 
correspondiente, dicha distancia X sería nula.
Ejemplo: dadas dos capas de líneas 'Ríos' y 'Calles' y una capa de puntos
'Puentes'. Un puente P (de la capa 'Puentes') debería ubicarse en la 
posición donde se intersecan el río R (de la capa 'Ríos') y la calle C 
(de la capa 'Calles'). 
	Si X = 0, P se encuentra efectivamente bien posicionado	sobre R y C 
	simultaneamente. En este caso P no será resaltado pues no se debe 
	realizar ninguna corrección en el elemento. 
	Si X > 0, P aparece corrido a una distancia X de la intersección entre
	R y C y debe ser analizado por el corrector.
El objetivo de esta herramienta es identificar cada puente de la capa 
'Puentes' para el cual el valor X sea mayor a cero, señalando también
el punto de la intersección cercana a la que se asume que deberia acercarse.

Nota: en lugar de considerar que un salvaobstáculos está correctamente
posicionado si y solo si X = 0, se puede establecer un radio de tolerancia
Z especificado por el usuario, de manera que si el salvaobstáculos se
encuentra a una distancia menor a Z del obstáculo correspondiente, se 
considera correctamente posicionado.

Diseño:
Para la solución de esta problemática se nos sugirió basarnos en la
herramienta Near (Cercano) nativa de ArcGis. Sin embargo, encontramos
que esta herramienta solamente considera las distancias que se establecen
entre capas, y no entre cada elemento de cada capa. Con lo cual surgen 
inconvenientes inmediatos como por ejemplo: si el río R tiene intersección
con más de un elemento de 'Calles' (por ejemplo cruza con C1, C2 y C3),
la herramienta dará al campo NEAR_DIST valor 0 (lo cual es correcto,
porque Near está encontrando que la distancia entre una capa y otra es nula)
pero eligirá al azar uno de los tres elementos C1, C2 y C3 para indicar 
como referencia de elemento de la capa 'Calles' al cual la distancia es 
mínima. Con esto se pierde información sobre las otras 2 intersecciones 
existentes y no se podrá analizar la situación de los salvaobstáculos 
correspondientes a ellas.
Por esta razón, la solución que estamos diseñando incluye una combinación 
de ejecuciones de la herramienta Intersect y la herramienta Buffer, entre 
otras, y no utiliza (al menos por el momento) Near.

1) Creo una capa que contiene los puntos donde se intersecan 2 capas de lineas
(ejemplo, guardo las intersecciones entre Red_Vial y Cursos_Agua)
2) Ejecuto la herramienta Buffer sobre la capa de intersecciones, para que me
genere polígonos de radio X al rededor de cada putno de intersección
3) 



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
