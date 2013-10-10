import arcpy

def renameFields (inFeature, field_original, nuevo_nombre):
	
	nuevo_alias = nuevo_nombre
	
	fields = arcpy.ListFields(inFeature, field_original)
	field = fields[0]
	
	# Obtengo propiedades del field original
	domain = field.domain
	isNullable = field.isNullable
	length = field.length
	precision = field.precision
	required = field.required
	scale = field.scale
	type_ = field.type
	
	# Creo nuevo field con esas propiedades y nuevo_nombre
	arcpy.AddField_management(inFeature, nuevo_nombre, type_, precision, scale, length, nuevo_alias, isNullable, required, domain)
	
	# Itero con un UpdateCuror en el field original y pongo los valores
	# en el nuevo field
	rows = arcpy.UpdateCursor(inFeature)
	for row in rows:
		row.setValue (nuevo_nombre, row.getValue(field_original))
		rows.updateRow(row)
		
	# Borro el field original
	arcpy.DeleteField_management(inFeature, field_original)
