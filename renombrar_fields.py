import arcpy
import renameFields_logica

try:
	inFeature = arcpy.GetParameterAsText(0)
	field_original = arcpy.GetParameterAsText(1)
	nuevo_nombre = arcpy.GetParameterAsText(2)
	
	renameFields_logica.renameFields(inFeature, field_original, nuevo_nombre)
	


# manejo de excepciones
except arcpy.ExecuteError:
	print arcpy.GetMessages(2)
	arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
	print e.args[0]
	arcpy.AddError(e.args[0])
