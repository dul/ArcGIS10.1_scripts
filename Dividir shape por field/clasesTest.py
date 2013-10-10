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
		print_test("Crea directorio en el lugar correcto",r'C:\Documents and Settings\mlauria\Mis documentos\GitHub\ArcGIS10.1_scripts\Dividir shape por field\Pruebas\no_existe_divididoPor_esto' == self.creadorTesteado.crear_directorio())
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
	objeto.test_obtener_lista_1()
	objeto.test_obtener_lista_2()

class TestExtractorDeCampos (object):
	def __init__(self):
		self.extractor = None
		
	def test_obtener_cursor(self):
		self.extractor = clases.ExtractorDeCampos(r"C:\Documents and Settings\mlauria\Mis documentos\GitHub\ArcGIS10.1_scripts\Dividir shape por field\Pruebas\007_Puentes.dbf", "MATERIAL")
		self.extractor.obtener_cursor()
		print_test("Obtener cursor. Tipo correcto", type(self.extractor.cursor) == arcpy.arcobjects.Cursor)

	def test_obtener_lista_1(self):
		self.extractor = clases.ExtractorDeCampos(r"C:\Documents and Settings\mlauria\Mis documentos\GitHub\ArcGIS10.1_scripts\Dividir shape por field\Pruebas\007_Puentes.dbf", "MATERIAL")
		lista = self.extractor.obtener_lista()
		lista_correcta = [u'SIN DATO', u'PIEDRA', u'HIERRO', u'MAMPOSTERIA', u'MADERA', u'PIRINCHO']
		print_test("Obtener lista (simple)", lista == lista_correcta)
		
	def test_obtener_lista_2(self):
		self.extractor = clases.ExtractorDeCampos(r"C:\Documents and Settings\mlauria\Mis documentos\GitHub\ArcGIS10.1_scripts\Dividir shape por field\Pruebas\007_Puentes.dbf", "HOJA")
		lista = self.extractor.obtener_lista()
		lista_correcta = [u'2366-I', u'2569-II', u'2566-I', u'2569-IV', u'2366-II', u'2363-I', u'2366-IV', u'2363-III', u'2566-II', u'2563-I', u'2363-II', u'2363-IV', u'2563-II', u'2560-I', u'2560-II', u'2557-I', u'2566-III', u'2566-IV', u'2563-III', u'2563-IV', u'2560-III', u'2560-IV', u'2557-III', u'2554-III', u'2766-I', u'2766-II', u'2763-I', u'2760-I', u'2760-II', u'2757-I', u'2754-I', u'2754-II', u'2769-IV', u'2766-III', u'2766-IV', u'2763-III', u'2760-III', u'2760-IV', u'2757-III', u'2757-IV', u'2754-III', u'2969-I', u'2969-II', u'2966-I', u'2966-II', u'2963-I', u'2963-II', u'2960-II', u'2957-I', u'2957-II', u'2969-III', u'2969-IV', u'2966-III', u'2966-IV', u'2963-III', u'2963-IV', u'2960-III', u'2960-IV', u'2957-III', u'2957-IV', u'3169-I', u'3166-I', u'3166-II', u'3163-I', u'3163-II', u'3160-I', u'3160-II', u'3157-I', u'3169-III', u'3169-IV', u'3166-III', u'3166-IV', u'3163-III', u'3163-IV', u'3160-III', u'3160-IV', u'3369-I', u'3369-II', u'3366-I', u'3366-II', u'3363-I', u'3363-II', u'3360-I', u'3360-II', u'3357-I', u'3369-III', u'3369-IV', u'3366-III', u'3366-IV', u'3363-III', u'3363-IV', u'3360-III', u'3360-IV', u'3569-I', u'3569-II', u'3566-I', u'3566-II', u'3563-I', u'3563-II', u'3560-I', u'3560-II', u'3557-I', u'3569-III', u'3569-IV', u'3563-IV', u'3560-III', u'3560-IV', u'3557-III', u'3772-II', u'3769-I', u'3763-II', u'3760-I', u'3760-II', u'3757-I', u'3757-II', u'3772-IV', u'3769-III', u'3769-IV', u'3769-II', u'3766-III', u'3963-I', u'3966-II', u'3969-II', u'3766-I', u'3766-IV', u'3966-I', u'3763-III', u'3963-III', u'3763-IV', u'3760-III', u'3760-IV', u'3757-III', u'3972-II', u'3969-I', u'3963-II', u'3960-I', u'3960-II', u'3957-I', u'3972-IV', u'3969-III', u'3969-IV', u'3966-III', u'3966-IV', u'3963-IV', u'4172-II', u'4169-I', u'4166-I', u'4166-II', u'4163-I', u'4163-II', u'4172-IV', u'4169-III', u'4169-IV', u'4166-IV', u'4372-II', u'4369-I', u'4372-IV', u'4366-I', u'4369-III', u'4369-IV', u'4366-III', u'4366-IV', u'4572-II', u'4569-I', u'4566-II', u'4566-I', u'4572-IV', u'4569-III', u'4569-IV', u'4769-I', u'4772-II', u'4769-II', u'4772-III', u'4772-IV', u'4972-I', u'4972-II', u'4969-I', u'4972-III', u'4972-IV', u'4766-III', u'4969-II', u'4969-IV', u'5169-I', u'5169-III', u'5169-IV', u'5369-IV', u'4969-III', u'5172-I', u'5172-II', u'5172-III', u'5172-IV', u'5569-II', u'5566-I', u'3157-III', u'3566-III', u'5160-III', u'5160-IV', u'5157-III', u'5360-II']
		print_test("Obtener lista (caracteres criticos)", lista == lista_correcta)
	
#~ ejecutarSetDePruebasCreadoresDeDirectorio("Pruebas Creador de Directorio",TestCreadorDeDirectorio())
ejecutarSetDePruebasCreadoresDeDirectorio("Pruebas Creador de Directorio Por Field",TestCreadorDeDirectorio_PorField())

#~ ejecutarSetDePruebasExtractorDeCampo("Pruebas Extractor de Campos",TestExtractorDeCampos())
