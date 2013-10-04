######################## TESTS ############################
import clases
import arcpy 

def print_test( mensaje, expresion ):
	if expresion:
		print mensaje + ": OK"
	else:
		print mensaje + ": ERROR"
		
def ejecutarSetDePruebasCreadoresDeDirectorio( mensaje, objeto ):
	print mensaje
	objeto.test_chequear_si_ya_existe_Posititvo()
	objeto.test_chequear_si_ya_existe_Negativo()
	objeto.test_redefinir_nombre()
	objeto.test_crear_directorio()
	objeto.test_borrar_directorio()

class TestCreadorDeDirectorio(object):
	def __init__(self):
		self.creadorTesteado = clases.CreadorDeDirectorio('C:\Documents and Settings\mlauria\Mis documentos\GitHub\ArcGIS10.1_scripts\Dividir shape por field\Pruebas')
		self.nombre_inexistente = 'no_existe'
		self.nombre_existente = 'existe'
		
	def test_chequear_si_ya_existe_Posititvo(self):
		self.creadorTesteado.nombrar_directorio(self.nombre_existente)
		print_test("Ya existe (positivo)", self.creadorTesteado.chequear_si_ya_existe())

	def test_chequear_si_ya_existe_Negativo(self):
		self.creadorTesteado.nombrar_directorio(self.nombre_inexistente)
		print_test("Ya existe (negativo)",not self.creadorTesteado.chequear_si_ya_existe())
	
	def test_redefinir_nombre(self):
		self.creadorTesteado.nombrar_directorio(self.nombre_existente)
		self.creadorTesteado.redefinir_nombre()
		print_test("Redefinir nombre", self.creadorTesteado.nombre == self.nombre_existente+str(1))

	def test_crear_directorio(self):
		self.creadorTesteado.nombrar_directorio(self.nombre_inexistente)
		self.creadorTesteado.crear_directorio()
		print_test("Crear directorio (nombre inexistente)",self.creadorTesteado.chequear_si_ya_existe())
		self.creadorTesteado.borrar_directorio()
	
	def test_borrar_directorio(self):
		self.creadorTesteado.nombrar_directorio(self.nombre_inexistente)
		self.creadorTesteado.crear_directorio()
		print_test("Borrar directorio (Parte 1)",self.creadorTesteado.chequear_si_ya_existe())
		self.creadorTesteado.borrar_directorio()
		print_test("Borrar directorio (Parte 2)",not self.creadorTesteado.chequear_si_ya_existe())




class TestCreadorDeDirectorio_PorField(object):
	def __init__(self):
		self.creadorTesteado = clases.CreadorDeDirectorio_PorField('C:\Documents and Settings\mlauria\Mis documentos\GitHub\ArcGIS10.1_scripts\Dividir shape por field\Pruebas')
		self.nombre_inexistente = 'no_existe_divididoPor_esto'
		self.nombre_existente = 'existe_divididoPor_esto'
		
	def test_chequear_si_ya_existe_Posititvo(self):
		self.creadorTesteado.nombrar_directorio('existe', 'esto')
		print_test("Ya existe (positivo)",self.creadorTesteado.chequear_si_ya_existe())

	def test_chequear_si_ya_existe_Negativo(self):
		self.creadorTesteado.nombrar_directorio('no_existe', 'esto')
		print_test("Ya existe (negativo)",not self.creadorTesteado.chequear_si_ya_existe())
	
	def test_redefinir_nombre(self):
		self.creadorTesteado.nombrar_directorio('existe', 'esto')
		self.creadorTesteado.redefinir_nombre()
		print_test("Redefinir nombre", self.creadorTesteado.nombre == self.nombre_existente+str(1))

	def test_crear_directorio(self):
		self.creadorTesteado.nombrar_directorio('no_existe', 'esto')
		self.creadorTesteado.crear_directorio()
		print_test("Crear directorio (nombre inexistente)",self.creadorTesteado.chequear_si_ya_existe())
		self.creadorTesteado.borrar_directorio()
	
	def test_borrar_directorio(self):
		self.creadorTesteado.nombrar_directorio('no_existe', 'esto')
		self.creadorTesteado.crear_directorio()
		print_test("Borrar directorio (Parte 1)",self.creadorTesteado.chequear_si_ya_existe())
		self.creadorTesteado.borrar_directorio()
		print_test("Borrar directorio (Parte 2)",not self.creadorTesteado.chequear_si_ya_existe())


def ejecutarSetDePruebasExtractorDeCampo( mensaje, objeto ):
	print mensaje
	objeto.test_obtener_cursor()

class TestExtractorDeCampos (object):
	def __init__(self):
		self.extractor = clases.ExtractorDeCampos(r"C:\Documents and Settings\mlauria\Mis documentos\GitHub\ArcGIS10.1_scripts\Dividir shape por field\Pruebas\007_Puentes.dbf", "MATERIAL")
		print self.extractor.in_feature
		
	def test_obtener_cursor(self):
		self.extractor.obtener_cursor()
		print type(self.extractor.cursor)
		print_test( "Obtener cursor", type(self.extractor.cursor) == 'arcpy.arcobjects.arcobjects.Cursor')


#~ ejecutarSetDePruebasCreadoresDeDirectorio("Pruebas Creador de Directorio",TestCreadorDeDirectorio())
#~ ejecutarSetDePruebasCreadoresDeDirectorio("Pruebas Creador de Directorio Por Field",TestCreadorDeDirectorio_PorField())

ejecutarSetDePruebasExtractorDeCampo("Pruebas Extractor de Campos",TestExtractorDeCampos())
