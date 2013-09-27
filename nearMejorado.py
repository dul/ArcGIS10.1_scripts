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

Opciones:
	1) Creo capa InterseccionLinea1Linea2 que contiene los puntos de interseccion
	entre dos capas de lineas Linea1 y Linea2
	2) Creo capa InterseccionInterseccionesSalvaconductos que conteine los puntos
	que coinciden entre los de la capa InterseccionLinea1Linea2 y los de la capa
	Salvaconductos
	3) Agrego un campo "Coincide con interseccion" a Salvaconductos
	4) A cada elemento de Salvaconductos que se halle en
	InterseccionInterseccionesSalvaconductos le pongo el valor TRUE en "Coincide..."
	al resto le pongo FALSE.
--------------------------------------------------------------------------------
	1) Creo una capa que contiene los puntos donde se intersecan 2 capas de lineas
	(ejemplo, guardo las intersecciones entre Red_Vial y Cursos_Agua) usando 
	arcpy.Intersect_analisys([Red_Vial, Cursos_Agua], "ALL", "POINT")
	2) Ejecuto la herramienta Buffer sobre la capa de intersecciones, para que me
	genere polígonos de radio X al rededor de cada punto de intersección
	Cada polígino tiene guardado en su tabla de atributos las coordenadas de
	su centro.
	3) Creo una capa "salvaobstaculosDeInteres" que resulta de aplicar Interesct 
	entre la capa de salvaobstáculos y la capa de polígonos circulares.
	4) Calculo las distancias entre cada salvaobstáculos y el centro del polígono
	con el que intersecan. Lo guardo en un nuevo campo de la tabla de atributos
	de salvaobstaculosDeInteres.
	5) Mergeo salvaobstaculosDeInteres con la capa de salvaobstaculos original.
--------------------------------------------------------------------------------
	Para cada puente, decime si interseca cona algún polígono. Si interseca,
	decime con cuál.
	El polígono tiene guardada referencia a la intersección. Tomo la intersección
	del polígono y ésta tiene referencia a las líneas que la generan.
	A cada puente que interseca con polígono le agrego 2 campos:
	- distancia con intersección
	- referencia a líneas de intersección

arcpy.SelectLayerByLocation_management("Puente_Red_Vial_Puntos", "INTERSECT", 'Red_VialAdministra2_Intersec1', "", "NEW_SELECTION")

"""


try:
	# Obtencion de los parámetros
	salvaobstaculos = arcpy.GetParameterAsText(0) # salvaosbstaculos
	lineas1 = arcpy.GetParameterAsText(1)
	lineas2 = arcpy.GetParameterAsText(2)
	search_radius = arcpy.GetParameterAsText(3)
	location = arcpy.GetParameterAsText(4)
	angle = arcpy.GetParameterAsText(5)
	# 1) Creo capa InterseccionLinea1Linea2 que contiene los puntos de interseccion
	# entre dos capas de lineas Linea1 y Linea2
	intersect_L1_L2 = 'interseccion_lineas1_lineas2.shp'
	arcpy.Intersect_analysis(lineas1;lineas2, intersect_L1_L2, "ALL", 1, "POINT")
	# 2) Creo capa InterseccionInterseccionesSalvaobstaculos que conteine los puntos
	# que coinciden entre los de la capa InterseccionLinea1Linea2 y los de la capa
	# Salvaobstaculos
	intersect_L1_l2_S = 'interseccion_lineas1_lineas2_Salvaobstaculos.shp'
	arcpy.Intersect_analysis(intersect_L1_L2;salvaobstaculos, intersect_L1_l2_S, "ALL", 1, "POINT")
	# 3) Agrego un campo "Coincide con interseccion" a Salvaobstaculos. Default: -1
	arcpy.AddField_management(salvaobstaculos, "COINCIDE", "TEXT", "", "", "", "Ubicado sobre interseccion: 0", "", "")
	arcpy.AssignDefaultToField_management (salvaobstaculos, "COINCIDE", "-1","")
	# 4) A cada elemento de Salvaconductos que se halle en
	# InterseccionInterseccionesSalvaconductos le pongo el valor 0 en "COINCIDE"
	# al resto le pongo -1.
	rowsSalvaobs = arcpy.UpdateCursor(salvaobstaculos)
	for rowS in rowsSalvaobs: 
		rowsIntersect = arcpy.SearchCursor(intersect_L1_l2_S)
		for rowI in rowsIntersect:
			if rowI.FID == rowS.FID:
				rowS.COINCIDE = 0
				rowsSalvaobs.updateRow(rowS)
		

# manejo de excepciones
except arcpy.ExecuteError:
	print arcpy.GetMessages(2)
	arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
	print e.args[0]
	arcpy.AddError(e.args[0])
