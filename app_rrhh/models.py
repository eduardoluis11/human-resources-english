from django.db import models

""" Usar esta biblioteca para usar "date.today" si me sale un error con el DateField (fuente:
https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateField) . REsulta que lo que tuve que usar 
fue "from datetime import date" (fuente: https://docs.python.org/3/library/datetime.html#datetime.date.today .)
"""
# import datetime.date.today()
from datetime import date

""" Para registrar usuarios y dejarles que inicien sesión, voy a usar la biblioteca "Abstract User", ya que me deja 
hacer esto muy rápidamente (fuente: https://docs.djangoproject.com/en/4.1/topics/auth/customizing/)
"""
from django.contrib.auth.models import AbstractUser

# Create your models here.

""" Modelo para almacenar usuarios (fuente: https://docs.djangoproject.com/en/4.1/topics/auth/customizing/).

Esto me dejará tanto registrar usuarios, como dejarles iniciar sesión.
"""
class User(AbstractUser):
    pass

""" Modelo para registrar sanciones.

Los campos que necesito son:
•	Nombre.
•	Apellidos.
•	Cédula.
•	Sanción a aplicar.
•	Motivo de la sanción.
•	Fecha del incidente.
•	Fecha del momento en el que se cree este registro (se hace con un dateTime.now(), para obtener un timestamp).

El formato de las fechas que usaré es el que viene por defecto en Django. Pero, para “fecha del incidente”, pondré solo 
la fecha, NO la hora (no se como, y no tengo tiempo para ver como implementarlo). Entonces, usaré algo como “date” como 
tipo de campo para la fecha del incidente.

Las sanciones y el motivo de las sanciones pueden ser tan largas como el usuario quiera escribirlas, por lo que serán
TextField (acepta más de 255 caracteres). Para el resto de los campos con texto, un CharField es suficiente.
"""
class Sancion(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=15)
    sancion_a_aplicar = models.TextField(blank=True)
    motivo_de_sancion = models.TextField(blank=True)
    fecha_del_incidente = models.DateField(default=date.today)
    timestamp = models.DateTimeField(auto_now_add=True)

""" Modelo de las bonificaciones familiares.

Los campos que usaré serán: nombre, apellidos, cédula, número de hijos menores, número de hijos mayores con 
discapacidades, el salario mínimo mensual vigente, el número total de hijos que cualifican para la bonificación familiar
(la suma de los hijos menores más los hijos mayores con discapacidades), la bonificación familiar a recibir, y,
de preferencia, el timestamp (para saber cuando se registró la bonificación familiar).

El cálculo de la bonificación familiar será el total de multiplicar por 5% por el salario mínimo y por el 
número total de hijos que cualifiquen para la bonificación familiar.

El número total de hijos y la bonificación familiar NO SE DEBEN EDITAR. Esos campos se rellenarán automáticamente
después de que el usuario rellene el resto del formulario.

Voy a usar el DecimalField para almacenar los salarios, y le voy a dejar dos decimales. “Max digits” es obligatorio 
para el DecimalField.

10 millones de usd es igual a: 69.155.320.000,00 guaraní. Con los decimales, esa cantidad es de 13 digitos. Voy a poner 13 
o 14 digitos como maximo numero de digitos para decimalField.

Existe el IntegerField, el cual almacena números enteros. Lo voy a usar para el número de hijos. 

"""
class BonificacionFamiliar(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=15)
    hijos_menores = models.IntegerField(default=0)
    hijos_mayores_discapacitados = models.IntegerField(default=0)
    total_hijos_para_bonificacion = models.IntegerField(default=0)
    fecha_a_pagar = models.DateField(default=date.today)
    salario_minimo_mensual_vigente = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    bonificacion_familiar = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)

""" Modelo de Permisos para ausentarse de los trabajadores.

En principio, solo le pondré un solo campo: el de la imagen (se hace con un ImageField). Le pondré un “upload_to” como 
atributo para ver si se me crea la carpeta en donde se subirá el archivo (fuente: 
https://www.youtube.com/watch?v=ygzGr51dbsY).

Las imágenes que subiré serán las firmas en jpg del trabajador a ausentarse, y el encargado que le dió el permiso de
ausentarse.

Voy a agregar un campo para decir si se le aplicará un descuento al trabajador por faltar esos días (sí/no). Como
quiero agregar "sí" o "no" como registro para este campo, lo almacenaré como un CharField de máximo 2 caracteres.
Prefiero eso a un Booleano, porque "sí" o "no" es más fácil de entender que "True" o "False". 

Voy a darle la posibilidad de descontarle dinero del salario al trabajador por los días que se ausente. Pero, esa
casilla será opcional. Para ello, usaré "blank=true" o algo similar. Y le pondré un DecimalField, para contar
los decimales del pago.

Solo pondre desde que fecha se ausentará y la fecha de reincorporación. No especificaré la hora por los momentos.

Usaré el timestamp para indicar cuando se firmó el permiso.

Como ya había creado un registro, ahora tengo que ponerle un valor por defecto a todos los campos. Para ello, usaré
'default'.
"""
class Permiso(models.Model):
    nombre = models.CharField(max_length=50, default='')
    apellidos = models.CharField(max_length=50, default='')
    cedula = models.CharField(max_length=15, default='')
    fecha_inicio_ausencia = models.DateField(default=date.today)    # fecha desde que se va a ausentar
    fecha_reincorporacion = models.DateField(default=date.today)    # fecha en la que regresará
    motivo_ausencia = models.TextField(default='')
    recibira_descuento = models.CharField(max_length=2, default='')  # "Sí" o "no"
    descuento = models.DecimalField(blank=True, max_digits=14, decimal_places=2, default=0.00)
    foto_firma_trabajador = models.ImageField(upload_to="images/", default='')
    foto_firma_encargado_rrhh = models.ImageField(upload_to="images/", default='')
    timestamp = models.DateTimeField(default=date.today)  # Cuando se firmó el permiso

""" Modelo de Perfil de Cargo.

Necesito los campos: Nombre del cargo, Experiencia Laboral Requerida, Conocimientos Técnicos Requeridos, 
Rango Salarial, Nivel de Estudios, Si el candidato requiere de tener auto propio, Otros Requisitos.

El rango salarial lo puedo poner como un <textarea> o un simple input de texto. No lo voy a meter como números.

Le meteré el timestamp para saber desde qué fecha la compañía está buscando un candidato que cumpla con
las especificaciones de ese perfil de cargo.

Lo del auto propio será un "sí" o "no".

Como la planilla del ministerio de Trabajo muestra que el nombre de un Cargo es de 100 caracteres maximo, también 
lo voy a poner así en el nombre del cargo.
"""
class PerfilDeCargo(models.Model):
    nombre_del_cargo = models.CharField(max_length=100)
    experiencia_requerida = models.TextField()
    conocimientos_requeridos = models.TextField()
    nivel_de_estudios = models.TextField()
    rango_salarial = models.TextField()
    requiere_tener_auto_propio = models.CharField(max_length=2)  # "Sí" o "no"
    otros_requisitos = models.TextField()
    timestamp = models.DateTimeField(default=date.today)

""" Modelo de Justificación de Permiso.

Los campos que necesitaré serán:
•	Nombre del trabajador.
•	Apellidos.
•	Cédula.
•	Fecha de inicio de ausencia.
•	Fecha de Reincorporación.
•	Archivo (PDF o Imagen Escaneada) con la justificación del permiso.
•	Si existe alguna discrepancia entre el permiso y la justificación (si/no).
•	Firma del encargado que registró la justificación.
•	Timestamp.
"""
class JustificacionDePermiso(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=15)

    fecha_inicio_ausencia = models.DateField(default=date.today)    # fecha desde que se ausentó
    fecha_reincorporacion = models.DateField(default=date.today)    # fecha en la que regresó

    archivo_con_justificacion = models.FileField(upload_to="documentos/")   # Archivo con justificación

    existe_discrepancia_permiso_y_justificacion = models.CharField(max_length=2)  # "Sí" o "no"

    foto_firma_encargado_rrhh = models.ImageField(upload_to="images/")

    timestamp = models.DateTimeField(default=date.today)

""" Modelo de Descuentos.

Los campos que agregaré serán los siguientes:
•	Nombre.
•	Apellidos.
•	Cédula.
•	Fecha en el que se le hará el pago con el descuento.
•	Salario base (sin ingresos extras ni descuentos).
•	Salario con los ingresos extras (para calcular cuota del IPS). 
•	Descuento de la cuota del IPS.
•	Descuento por sanciones.
•	Descuentos por inasistencias.
•	Otros descuentos (<textarea>).
•	Descuentos totales (suma de todos los descuentos).
•	Timestamp.

Para los descuentos y el salario, usaré el mismo tipo de campo que he usado para los salarios en modelos anteriores
(DecimalField).

Idealmente, el descuento total lo debería calcular en mi código. Sin embargo, dado a que le dejaré la opción de agregar
descuentos extras en un <textarea> (del cual es muy difícil saca números para hacer cálculos), y debido a falta de 
tiempo, el usuario tendrá que hacer manualmente todos los cálculos, y luego escribirlos en el formulario para 
registrar los descuentos.

Algunos descuentos serán opcionales. Sin embargo, en el formulario, pondré mínimo un 0 en todos los descuentos.
"""
class Descuentos(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=15)

    fecha_aplicar_descuento = models.DateField(default=date.today)  # fecha en que se aplicará descuento

    salario_base = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    salario_con_ingresos_extras = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    # Descuentos
    descuento_cuota_ips = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    descuento_sanciones = models.DecimalField(blank=True, max_digits=14, decimal_places=2, default=0.00)
    descuento_inasistencias = models.DecimalField(blank=True, max_digits=14, decimal_places=2, default=0.00)
    otros_descuentos = models.TextField(blank=True)   # Se meteran en un <textarea>
    descuentos_totales = models.DecimalField(max_digits=14, decimal_places=2, default=0.00) # Total de descuentos

    timestamp = models.DateTimeField(default=date.today)

""" Modelo de Ingresos Extras.

Los campos que necesitaré serán:
•	Nombre.
•	Apellidos.
•	Cédula.
•	Salario base.
•	Fecha a pagar los ingresos extras (para saber el mes a pagar).
•	Horas extras trabajadas (opcional).
•	Bonificación Familiar.
•	Aguinaldos (este será opcional, ya que es 1 vez al año).
•	Otros ingresos (<textarea>) (Opcional).
•	Ingresos extras totales.
•	Timestamp.

Como ya expliqué en “Descuentos”, si hay varios tipos de ingresos extras a agregar, no pondré una función de agregar 
nuevos campos de manera dinámica porque no se como hacerlo y no tengo tiempo de implementarlo. En su lugar, lo meteré 
en un Text Area. No podré hacer cálculos con las cantidades ahí escritas, pero es la manera más fácil de dejarle al 
usuario escribir todos los ingresos extras adicionales que quiera.
"""
class IngresoExtra(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=15)
    salario_base = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    fecha_aplicar_ingresos_extras = models.DateField(default=date.today)  # fecha en que se pagarán ingresos extras

    # Ingresos Extras
    ingresos_por_horas_extras = models.DecimalField(blank=True, max_digits=14, decimal_places=2, default=0.00)
    bonificacion_familiar = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    aguinaldos = models.DecimalField(blank=True, max_digits=14, decimal_places=2, default=0.00)
    otros_ingresos_extras = models.TextField(blank=True)  # Se meterán en un <textarea>
    ingresos_extras_totales = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)  # Total

    timestamp = models.DateTimeField(default=date.today)

""" Modelo para las Vacaciones.

Los campos serán:
•	Nombre.
•	Apellidos.
•	Cédula de identidad.
•	Días totales de vacaciones para este año.
•	Días que se tomará de vacaciones.
•	Días de vacaciones restantes (NO se pondrá en el formulario. Se calculará).
•	Fecha de inicio de vacaciones.
•	Fecha de reincorporación.
•	Firma el trabajador que se irá de vacaciones.
•	Firma del encargado que autorizó las vacaciones.
•	Timestamp.

Los días los almacenaré como un entero, Y sí: dejaré que se metan números negativos al campo “días restantes”. Eso le 
indicaría al personal de recursos humanos que el trabajador usó más días de vacaciones de lo que debía, y se le pueden 
restar días de vacaciones al año que viene.

Todos los campos serán obligatorios.
"""
class Vacacion(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=15)

    # Días de vacaciones
    cantidad_inicial_dias_vacaciones = models.IntegerField(default=0)
    dias_que_se_tomara_vacaciones = models.IntegerField(default=0)
    dias_restantes_vacaciones = models.IntegerField(default=0)  # Se calculará y no estaré en formulario

    # Fecha de inicio y fin de vacaciones
    fecha_inicio_vacaciones = models.DateField(default=date.today)
    fecha_fin_vacaciones = models.DateField(default=date.today)

    # Fotos de firmas
    foto_firma_trabajador = models.ImageField(upload_to="images/")
    foto_firma_encargado_rrhh = models.ImageField(upload_to="images/")
    timestamp = models.DateTimeField(auto_now_add=True)

""" Modelo de Currículum.

Los campos que necesitaré son:
•	PDF con el currículum.
•	Cargo al que está aplicando.
•	Nombre.
•	Apellidos.
•	Sexo.
•	Cédula.
•	Fecha de nacimiento.
•	Domicilio.
•	Correo Electrónico (opcional).
•	Teléfono.
•	Si tiene auto propio (Opcional).
•	Experiencia Laboral (<textarea>).
•	Nivel de Estudios (<textarea>).
•	Otros datos de interés(<textarea>) (Opcional).
•	Timestamp.

Subiré el currículum en PDF a una carpeta llamada "curriculums". Lo puedo hacer opcional.

Para el resto de los campos de la información personal, voy a tomar los mismos tipos de datos que lso que debo usar
para la planilla el ministerio de trabajo (ver el ejemplo que tengo, que ahí me dice los tipos de datos que necesito.)

Pondré "Sexo". Dejaré s opciones: hombre, mujer, ya que así aparece en la planilla del ministerio de trabajo.

Después de pensarlo, mejor pondré el domicilio en un solo campo en un <textarea> de 100 caracteres (como en la
planilla del ministerio de trabajo.)

Puedo meter el email en un EmailField de Django.

Pondre 20 caracteres para los teléfonos, por si acaso.
"""
class Curriculum(models.Model):

    # Datos personales
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=15)
    sexo = models.CharField(max_length=1)
    fecha_nacimiento = models.DateField(default=date.today)
    domicilio = models.CharField(max_length=100)
    email = models.EmailField(blank=True, max_length=254)
    telefono = models.CharField(max_length=20)

    nombre_del_cargo = models.CharField(max_length=100)

    # Información laboral del candidato (se meterán en un <textarea>)
    experiencia_laboral = models.TextField()
    nivel_de_estudios = models.TextField()
    otros_datos_interes = models.TextField(blank=True)
    tiene_auto_propio = models.CharField(blank=True, max_length=2)  # "Sí" o "no", o "NR" (no respondió).

    pdf_con_curriculum = models.FileField(blank=True, upload_to="curriculums/")   # PDF con currículum
    timestamp = models.DateTimeField(auto_now_add=True)

""" Modelo de Aguinaldos.

Para no complicarme, pondre 12 casillas para que el usuario pueda poner el salario de cada mes de ese empleado. Así, no 
tendré que crear 2 formularios para los aguinaldos.
Los campos que pondré serán:
•	Nombre.
•	Apellidos.
•	Cédula.
•	Salario de Enero.
•	Salario de febrero.
•	Salario de marzo.
•	Salario de abril.
•	Salario de mayo.
•	Salario de junio.
•	Salario de julio.
•	Salario de agosto.
•	Salario de septiembre.
•	Salario de octubre.
•	Salario de noviembre.
•	Salario de diciembre.
•	Total de aguinaldos.
•	Año en el que se pagarán.
•	Timestamp.

El año será máximo 4 caracteres, y será un entero.

Voy a modificar el modelo para que me quite todos los meses de salario. No los necesito meter en la base de datos.
"""
class Aguinaldo(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=15)

    # Salario durante cada mes del año
    salario_enero = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    salario_febrero = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    salario_marzo = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    salario_abril = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    salario_mayo = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    salario_junio = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    salario_julio = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    salario_agosto = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    salario_septiembre = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    salario_octubre = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    salario_noviembre = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    salario_diciembre = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    # Aguinaldos a pagar
    aguinaldos = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    # Año al que corresponden los aguinaldos
    anno = models.IntegerField(default=0)

    timestamp = models.DateTimeField(auto_now_add=True)

""" Modelo para agregar Fechas para las Asistencias.
La primera tabla (la tabla de dias), solo tendra un formulario que dira "agregar dia/fecha". Lo único que haras sera 
registrar una fecha en esa tabla.

Entonces, agregaré dos archivos de listas: uno con la lista de días, y otro con la lista de empleados que asistieron 
ese día.
	
Además, crearé dos archivos HTML para registrar: uno para registrar días, y otro para registrar a cada empleado que 
asistió ese día.
	
El archivo de “ver en detalle” de la lista de días será el archivo HTML con la lista de empleados que fueron a trabajar 
ese día.
	
Entonces, tendré que crear dos archivos HTML de listas, uno de “ver detalle”, y dos formularios para registrar (5 
archivos en total).
	
No pondré un timestamp en el formulario para crear días, pero si crearé uno para registrar la asistencia de un empleado.
"""
class FechaAsistencia(models.Model):
    fecha_asistencias = models.DateField(default=date.today)


""" Modelo para registrar las Asistencias durante cada día.

Los campos para el modelo que registra las asistencias de cada empleado son:
•	Nombre.
•	Apellidos.
•	Cédula.
•	Hora de entrada.
•	Hora de salida.
•	Si asistió al trabajo (sí/no).
•	Timestamp.
•	Dia de la asistencia (lo tomaré como foreign key de "Fecha Asistencias").

El timestamp es para saber cuando se registró esa asistencia, para verificar que nadie agregue de forma sospechosa una 
asistencia.

El campo de la fecha puede ser vacío, en caso de que el trabajador no asista al trabajo.

Hay un modelo de Django que acepta horas. Se llama TimeField.

El día se escoge de manera automática, y se escoge en el lado del servidor. El usuario no tendrá que teclear nada
para meter la fecha de la asistencia en la bbdd. Igual, lo único que me interesa aquí es el formato, que es una fecha
o DateField. La fecha se meterá en el view, NO aquí.

Tengo que modificar mis modelo de asistencias para incluir la fecha como un foreign key. 
"""
class Asistencia(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=15)

    # Fecha de la asistencia (tomada como clave foránea)
    fecha_asistencia = models.ForeignKey("FechaAsistencia", on_delete=models.CASCADE,
                                         related_name="asistencias_de_trabajadores")

    # Horas de entrada y de salida del trabajador (pueden estar vacíos)
    hora_llegada = models.TimeField(blank=True, auto_now=False, auto_now_add=False)
    hora_salida = models.TimeField(blank=True, auto_now=False, auto_now_add=False)

    # Esto agarra si asistió al trabajo (sí/no)
    vino_a_trabajar = models.CharField(max_length=2)

    timestamp = models.DateTimeField(auto_now_add=True)

""" Modelo para la Liquidación del Personal

Los campos que necesito son:
•	Nombre.
•	Apellidos.
•	Cédula.
•	Cargo del trabajador.
•	Fecha de inicio del contrato (usando el date picker).
•	Fecha de fin de contrato.
•	Motivo de la finalización de contrato (<textarea>).
•	Tipo de salario (mensual, jornal, quincenal, etc).
•	Salario mensual.
•	Vacaciones no disfrutadas (es un salario).
•	Aguinaldos de lo que va de año.
•	Salario percibido por horas extras.
•	Otros ingresos extras (total) (DecimalField).
•	Total de Descuentos (si aplican).
•	Salario total a liquidar (se calculará).
•	Firma del encargado de recursos humanos.
•	Timestamp.

No le veo la razón del porqué el trabajador que abandona la empresa deba firmar esto, por lo que no incluiré su firma. 
Solo la del encargado que le hizo la liquidación.

No usaré un <textarea> para los “otros ingresos extras”, ya que quiero convertir esto en una calculadora (usando el 
view y el back end). Entonces, le pondré un DecimalField, y tomaré todos los montos escritos en este formulario para 
calcular el sueldo total a liquidar.

Obviamente restaré los descuentos.

El tipo de dato para el tipo de salario lo dejare como un varchar, ya que no se si hayan otros tipos de salarios. 

Todos los datos tendrán valores por defecto para evitar errores tipo NaN al momento de calcular el salario a liquidar
(aunque el valor sea 0).
"""
class LiquidacionDelPersonal(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=15)

    nombre_del_cargo = models.CharField(max_length=100)

    fecha_inicio_contrato = models.DateField(default=date.today)
    fecha_fin_contrato = models.DateField(default=date.today)

    motivo_de_finalizacion_contrato = models.TextField()

    # Salarios a usar para calcular la liquidación
    tipo_de_salario = models.CharField(max_length=200)
    salario_mensual = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    vacaciones_no_disfrutadas = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    aguinaldos = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    salario_por_horas_extras = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    otros_ingresos = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    # Descuentos (debo restarlo a los ingresos)
    descuentos_en_total = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    # Total a liquidar (se calculará)
    salario_total_a_liquidar = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    # Foto del encargado que calculó el total a liquidar
    foto_firma_encargado_rrhh = models.ImageField(upload_to="images/")

    timestamp = models.DateTimeField(auto_now_add=True)

""" Modelo para Gestionar la Liquidacion de los Salarios.

Los campos que usaré son:
•	Nombre.
•	Apellidos.
•	Cédula.
•	Salario mensual.
•	Ingresos extras.
•	Descuentos.
•	Salario total a pagar/liquidar. (Se calculará).
•	Fecha en la que se hará el pago.
•	Firma del encargado que calculó el salario a pagar.
•	Timestamp.

Es súper simple, pero no me queda más tiempo para arreglarlo.
"""
class LiquidacionDeSalario(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=15)

    # Salarios a sumar
    salario_mensual = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    ingresos_extras = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    # Descuentos (debo restarlo a los ingresos)
    descuentos = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    # Total a liquidar (se calculará)
    salario_total_a_liquidar = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    # Fecha en la que se hara el pago
    fecha_de_pago = models.DateField(default=date.today)

    # Foto del encargado que calculó el total a liquidar
    foto_firma_encargado_rrhh = models.ImageField(upload_to="images/")

    timestamp = models.DateTimeField(auto_now_add=True)

""" Modelo para el Legajo.

Los campos que voy a introducir son:
•	Nombre.
•	Apellidos.
•	Cédula.
•	Fecha de vencimiento de la cédula/documento de identidad.
•	Fecha de nacimiento.
•	Nacionalidad.
•	Sexo.
•	Domicilio. (El usuario lo podrá escribir todo aquí, como en la planilla del ministerio de trabajo.)
•	Número de teléfono.
•	Correo electrónico (opcional).
•	Currículum (en PDF).
•	Título / Nivel máximo de educación obtenido.
•	Antecedentes penales (sí/no).
•	Número de IPS (número de seguridad social).
•	Permisos para salir del trabajo (para saber las veces que ha tenido que ausentarse del trabajo). (En <textarea>)
•	Evaluación de desempeño (para saber si su productividad ha subido o bajado) (en PDF).
•	Sanciones. (En <textarea>)
•	Nombre del cargo.
•	Otros datos de interés. (En <textarea>).
•	Timestamp.

Pondre 20 caracteres y usaré varchar para la nacionalidad, porque así está en la planilla del Ministerio de Trabajo.

Pondre una casilla de 30 caracteres (varchar) para el numero del IPS.
"""
class Legajo(models.Model):

    # Datos personales
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=15)

    sexo = models.CharField(max_length=1)
    fecha_nacimiento = models.DateField(default=date.today)
    domicilio = models.CharField(max_length=100)
    email = models.EmailField(blank=True, max_length=254)
    telefono = models.CharField(max_length=20)
    nacionalidad = models.CharField(max_length=20)
    fecha_de_vencimiento_cedula = models.DateField(blank=True, default=date.today)
    curriculum = models.FileField(blank=True, upload_to="curriculums/")   # PDF con currículum
    nivel_maximo_de_educacion_obtenido = models.CharField(max_length=100)

    # Información Jurídica
    tiene_antecedentes_penales = models.CharField(max_length=2)  # "Sí" o "no"
    numero_ips = models.CharField(max_length=30)


    # Datos de la administración interna de la empresa
    cargo = models.CharField(max_length=100)
    evaluacion_de_desempeno = models.FileField(upload_to="documentos/")  # Archivo con evaluacion de desempeño
    sanciones = models.TextField(blank=True)
    permisos_para_ausentarse = models.TextField(blank=True)

    # Otros datos de interés de la empresa
    otros_datos = models.TextField(blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

""" Modelo para el Contrato.

Los campos que necesito son:
•	Nombre.
•	Apellidos.
•	Fecha de nacimiento.
•	Cédula de identidad.
•	Sexo.
•	Domicilio.
•	Email (opcional).
•	Teléfono.
•	Nivel de estudios terminados.
•	Número de IPS.
•	Número de cuenta bancaria. (Opcional en caso de que el pago se haga en efectivo.)
•	Cargo al que está aplicando.
•	Tipo de jornada (Tiempo completo o tiempo parcial, solo pondré 2 elecciones.)
•	Cláusulas del contrato (le pediré que se suban como un PDF. Pueden ser muy largas.)
•	Firma del trabajador.
•	Firma del encargado que le hizo el contrato.
•	Timestamp.

A 'tipo de jornada' le pondre un varchar como tipo de dato, y como 20 caracteres (quiero meter "Tiempo completo" 
y "tiempo parcial" en este campo)

Pondre el sexo del trabajador porque ya igual estoy poniendo todos sus datos personales. 

Pondre como varchar el numero de la cuenta bancaria, ya que muchas cuentas bancarias combinan letras con números. 
Le pondre 100 caracteres por si acaso. 

Se me olvidó agregar una cosa: las cláusulas del contrato.

Para simplificar las cosas, voy a agregar un PDF, el cual contendrá las clásulas del contrato. El usuario tendrá que 
descargarlo y leerlo. Recuerda que las cláusulas pueden ser bastante largas.

"""
class Contrato(models.Model):

    # Datos personales
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=15)
    sexo = models.CharField(max_length=1)
    fecha_nacimiento = models.DateField(default=date.today)
    domicilio = models.CharField(max_length=100)
    email = models.EmailField(blank=True, max_length=254)
    telefono = models.CharField(max_length=20)
    nivel_maximo_de_educacion_obtenido = models.CharField(max_length=100)
    numero_ips = models.CharField(max_length=30)
    numero_cuenta_bancaria = models.CharField(blank=True, max_length=100)

    # Datos del Contrato
    cargo = models.CharField(max_length=100)
    tiempo_completo_o_parcial = models.CharField(max_length=20)
    clausulas_del_contrato = models.FileField(default='', upload_to="documentos/")  # Archivo con cláusulas del contrato
    firma_trabajador = models.ImageField(upload_to="images/")
    firma_encargado_rrhh = models.ImageField(upload_to="images/")
    timestamp = models.DateTimeField(auto_now_add=True)

""" Modelo para el Informe web.

Solo haré el informe anual. Iba a poner también un informe mensual, pero, debido a falta de tiempo, no lo voy a incluir.

Voy a añadir un campo adicional que diga algo como “Otros datos de interés”, y que sea un <textarea>. Es para escribir 
cualquier cosa que se me haya olvidado.

Los campos que incluiré serán los siguientes:
•	Año del informe
•	Evaluación de desempeño anual de todo el personal (PDF).
•	 Número de trabajadores contratados en el año (no el número total de trabajadores, sino el número de trabajadores 
que se unieron a la compañía ese año).
•	Número de trabajadores que salieron de la compañía (por renuncias o despidos).
•	Edad promedio de todos los trabajadores.
•	Tasa de absentismo (para saber si los trabajadores están faltando cada vez más al trabajo).
•	Salario promedio de todos los trabajadores.
•	Número de días que pasaron desde que un cargo se hizo vacante hasta que se pudo contratar a alguien para ese cargo.
•	Número de años que tiene el trabajador que ha trabajado por más tiempo en la compañía.
•	Número de cursos ofrecidos a los trabajadores.
•	Timestamp.

Son 11 campos en total.

Dado que una empresa puede contratar a muchas personas en un solo año, entonces me saldría mejor pedirle al usuario
que escriba el promedio de días que toma contratar a alguien para un cargo vacante.
"""
class InformeWeb(models.Model):
    anno = models.IntegerField(default=0)   # Año del informe
    evaluacion_de_desempeno_personal = models.FileField(upload_to="documentos/")  # Archivo con evaluacion de desempeño
    trabajadores_contratados = models.IntegerField(default=0)
    trabajadores_que_salieron = models.IntegerField(default=0)
    edad_promedio_personal = models.IntegerField(default=0)
    tasa_absentismo = models.CharField(max_length=20)
    salario_promedio_personal = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    promedio_dias_para_ocupar_cargo_vacante = models.IntegerField(default=0)
    annos_de_trabajador_con_mas_tiempo_en_empresa = models.IntegerField(default=0)
    numero_cursos_ofrecidos_trabajadores = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

""" 3 Planillas del Ministerio de Trabajo.

Les pondré un timestamp a las 3 planillas para saber cuando fue que registra cada planilla.
"""
""" Modelo de la “Planilla de Empleados”.

    Para el , pondré los siguientes campos (me aseguraré de que tengan los mismos tipos 
de datos y limitaciones que en el ejemplo del Ministerio de Trabajo):
•	Número patronal. (Integer, 32 caracteres). X
•	Cédula. X
•	Nombre. X
•	Apellidos. X
•	Sexo. X 
•	Estado Civil. (Varchar, 1 carácter). X
•	Fecha de nacimiento. X
•	Nacionalidad. (Varchar, 20 caracteres). X
•	Domicilio. X
•	Fecha de nacimiento del menor. (OPCIONAL) X
•	Cantidad de hijos menores. (Integer, 32 caracteres). (OPCIONAL) X
•	Cargo. X
•	Profesión. (Varchar, 100 caracteres). X
•	Fecha de entrada. X
•	Horario de trabajo. (Varchar, 20 caracteres). X
•	Fecha de inicio de trabajo del menor. (Varchar, 20 caracteres). (OPCIONAL) X
•	Situación escolar del menor. (Varchar, 20 caracteres). (OPCIONAL) X
•	Fecha de salida. (OPCIONAL) X
•	Motivo de salida. (Varchar, 100 caracteres). (OPCIONAL) X
•	Estado (VACIO. NO SE PONDRA EN FORMULARIO). (Varchar, 1 caracter). (OPCIONAL) X
"""
class PlanillaEmpleadosMinisterioDeTrabajo(models.Model):
    numero_patronal = models.IntegerField(default=0)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=15)
    sexo = models.CharField(max_length=1)
    fecha_nacimiento = models.DateField(default=date.today)
    domicilio = models.CharField(max_length=100)
    cantidad_hijos_menores = models.IntegerField(default=0)
    fecha_nacimiento_del_menor = models.DateField(blank=True, default=date.today)
    estado_civil = models.CharField(max_length=1)
    nacionalidad = models.CharField(max_length=20)
    horario_de_trabajo = models.CharField(max_length=20)
    cargo = models.CharField(max_length=100)
    profesion = models.CharField(max_length=100)
    fecha_inicio_trabajo_del_menor = models.DateField(blank=True, default=date.today)
    situacion_escolar_menor = models.CharField(max_length=20)
    fecha_entrada = models.DateField(default=date.today)
    fecha_salida = models.DateField(blank=True, default=date.today)
    motivo_de_salida = models.CharField(blank=True, max_length=100)
    estado = models.CharField(blank=True, max_length=1)

    timestamp = models.DateTimeField(default=date.today)

""" Modelo de Planilla de Sueldos.

Los campos que necesito son:
•	Número patronal. (Integer, 32 caracteres).  X
•	Cédula. X
•	Forma de pago. (Varchar, 1 carácter) (J o M). X
•	Importe unitario. (Integer, 32 caracteres). X
•	Horas trabajadas en enero. (Integer, 32 caracteres). X
•	Salario percibido en enero. (Integer, 32 caracteres). X
•	Horas trabajadas en febrero.
•	Salario percibido en febrero.
•	Horas trabajadas en marzo.
•	Salario percibido en marzo.
•	Horas trabajadas en abril.
•	Salario percibido en abril.
•	Horas trabajadas en mayo.
•	Salario percibido en mayo.
•	Horas trabajadas en junio.
•	Salario percibido en junio.
•	Horas trabajadas en agosto.
•	Salario percibido en agosto.
•	Horas trabajadas en septiembre.
•	Salario percibido en septiembre.
•	Horas trabajadas en octubre.
•	Salario percibido en octubre.
•	Horas trabajadas en noviembre.
•	Salario percibido en noviembre.
•	Horas trabajadas en diciembre. X
•	Salario percibido en diciembre. X
•	Horas extras al 50% trabajadas durante el año. (Integer, 32 caracteres). X
•	Salario percibido en concepto de horas extras al 50% trabajadas durante el año. (Integer, 32 caracteres). X
•	Horas extras al 100% trabajadas durante el año. (Integer, 32 caracteres).   X
•	Salario percibido en concepto de horas extras al 100% trabajadas durante el año. (Integer, 32 caracteres). X
•	Aguinaldo o aguinaldo proporcional. (Integer, 32 caracteres). X
•	Beneficios. (Integer, 32 caracteres). X
•	Bonificaciones. (Integer, 32 caracteres). X
•	Vacaciones. (Integer, 32 caracteres). X
•	Total horas trabajadas incluyendo horas extras. (Integer, 32 caracteres). X
•	Total de importe recibido en concepto de salario. (Integer, 32 caracteres).
•	Total percibido, incluyendo aguinaldo, beneficios, bonificaciones, y vacaciones. (Integer, 32 caracteres).
"""
class PlanillaSueldosMinisterioDeTrabajo(models.Model):
    numero_patronal = models.IntegerField(default=0)
    cedula = models.CharField(max_length=15)
    forma_de_pago = models.CharField(max_length=1)
    importe_unitario = models.IntegerField(default=0)
    horas_trabajadas_enero = models.IntegerField(default=0)
    salario_percibido_enero = models.IntegerField(default=0)
    horas_trabajadas_febrero = models.IntegerField(default=0)
    salario_percibido_febrero = models.IntegerField(default=0)
    horas_trabajadas_marzo = models.IntegerField(default=0)
    salario_percibido_marzo = models.IntegerField(default=0)
    horas_trabajadas_abril = models.IntegerField(default=0)
    salario_percibido_abril = models.IntegerField(default=0)
    horas_trabajadas_mayo = models.IntegerField(default=0)
    salario_percibido_mayo = models.IntegerField(default=0)
    horas_trabajadas_junio = models.IntegerField(default=0)
    salario_percibido_junio = models.IntegerField(default=0)
    horas_trabajadas_julio = models.IntegerField(default=0)
    salario_percibido_julio = models.IntegerField(default=0)
    horas_trabajadas_agosto = models.IntegerField(default=0)
    salario_percibido_agosto = models.IntegerField(default=0)
    horas_trabajadas_septiembre = models.IntegerField(default=0)
    salario_percibido_septiembre = models.IntegerField(default=0)
    horas_trabajadas_octubre = models.IntegerField(default=0)
    salario_percibido_octubre = models.IntegerField(default=0)
    horas_trabajadas_noviembre = models.IntegerField(default=0)
    salario_percibido_noviembre = models.IntegerField(default=0)
    horas_trabajadas_diciembre = models.IntegerField(default=0)
    salario_percibido_diciembre = models.IntegerField(default=0)
    horas_extras_50_por_ciento_durante_anno = models.IntegerField(default=0)
    salario_percibido_horas_extras_50_por_ciento_anno = models.IntegerField(default=0)
    horas_extras_100_por_ciento_durante_anno = models.IntegerField(default=0)
    salario_percibido_horas_extras_100_por_ciento_anno = models.IntegerField(default=0)
    aguinaldo = models.IntegerField(default=0)
    beneficios = models.IntegerField(default=0)
    bonificaciones = models.IntegerField(default=0)
    vacaciones = models.IntegerField(default=0)
    horas_trabajadas_incluyendo_horas_extras = models.IntegerField(default=0)
    total_recibido_en_concepto_de_salario = models.IntegerField(default=0)

    # Total percibido, incluyendo aguinaldo, beneficios, bonificaciones, y vacaciones. (Integer, 32 caracteres).
    total_incluyendo_ingresos_extras = models.IntegerField(default=0)

    timestamp = models.DateTimeField(default=date.today)

""" Modelo de Planilla de Resumen General.

•	Número patronal, Orden 1.
•	Año, Orden 1. (Integer, 32 caracteres).
•	Supervisores o jefes varones, Orden 1. (Integer, 32 caracteres).
•	Supervisores o jefes mujeres, Orden 1. (Integer, 32 caracteres).
•	Empleados varones, Orden 1. (Integer, 32 caracteres).
•	Empleadas mujeres, Orden 1. (Integer, 32 caracteres).
•	Obreros hombres, Orden 1. (Integer, 32 caracteres).
•	Obreras mujeres, Orden 1. (Integer, 32 caracteres).
•	Menores varones, Orden 1. (Integer, 32 caracteres).
•	Menores mujeres, Orden 1. (Integer, 32 caracteres).
•	Orden 1. (Solo meteré un 1). (Integer, 32 caracteres).
•	Número patronal, Orden 2.
•	Año, Orden 2. 
•	Supervisores o jefes varones, Orden 2. 
•	Supervisores o jefes mujeres, Orden 2.
•	Empleados varones, Orden 2. 
•	Empleadas mujeres, Orden 2. 
•	Obreros hombres, Orden 2. 
•	Obreras mujeres, Orden 2. 
•	Menores varones, Orden 2. 
•	Menores mujeres, Orden 2. 
•	Orden . (Solo meteré un 2).
•	REPETIR LOS MISMOS CAMPOS HASTA EL ORDEN 5. 

El número de los ordenes se meteran automaticamente a la base de datos. NO lo pondre en los formularios.
"""
class PlanillaResumenGeneralMinisterioDeTrabajo(models.Model):

    # Orden 1: Cantidad de empleados
    numero_patronal_orden_1 = models.IntegerField(default=0)
    anno_orden_1 = models.IntegerField(default=0)
    supervisores_o_jefes_varones_orden_1 = models.IntegerField(default=0)
    supervisores_o_jefes_mujeres_orden_1 = models.IntegerField(default=0)
    empleados_varones_orden_1 = models.IntegerField(default=0)
    empleados_mujeres_orden_1 = models.IntegerField(default=0)
    empleadas_mujeres_orden_1 = models.IntegerField(default=0)
    obreros_hombres_orden_1 = models.IntegerField(default=0)
    obreras_mujeres_orden_1 = models.IntegerField(default=0)
    menores_varones_orden_1 = models.IntegerField(default=0)
    menores_mujeres_orden_1 = models.IntegerField(default=0)

    # Orden 1. Solo meteré un 1
    orden_1 = models.IntegerField(default=0)

    # Orden 2: Horas trabajadas
    numero_patronal_orden_2 = models.IntegerField(default=0)
    anno_orden_2 = models.IntegerField(default=0)
    supervisores_o_jefes_varones_orden_2 = models.IntegerField(default=0)
    supervisores_o_jefes_mujeres_orden_2 = models.IntegerField(default=0)
    empleados_varones_orden_2 = models.IntegerField(default=0)
    empleados_mujeres_orden_2 = models.IntegerField(default=0)
    empleadas_mujeres_orden_2 = models.IntegerField(default=0)
    obreros_hombres_orden_2 = models.IntegerField(default=0)
    obreras_mujeres_orden_2 = models.IntegerField(default=0)
    menores_varones_orden_2 = models.IntegerField(default=0)
    menores_mujeres_orden_2 = models.IntegerField(default=0)

    # Orden 2. Solo meteré un 2
    orden_2 = models.IntegerField(default=0)

    # Orden 3: Sueldos o jornales
    numero_patronal_orden_3 = models.IntegerField(default=0)
    anno_orden_3 = models.IntegerField(default=0)
    supervisores_o_jefes_varones_orden_3 = models.IntegerField(default=0)
    supervisores_o_jefes_mujeres_orden_3 = models.IntegerField(default=0)
    empleados_varones_orden_3 = models.IntegerField(default=0)
    empleados_mujeres_orden_3 = models.IntegerField(default=0)
    empleadas_mujeres_orden_3 = models.IntegerField(default=0)
    obreros_hombres_orden_3 = models.IntegerField(default=0)
    obreras_mujeres_orden_3 = models.IntegerField(default=0)
    menores_varones_orden_3 = models.IntegerField(default=0)
    menores_mujeres_orden_3 = models.IntegerField(default=0)

    # Orden 3. Solo meteré un 3
    orden_3 = models.IntegerField(default=0)

    # Orden 4: Cantidad de ingresos
    numero_patronal_orden_4 = models.IntegerField(default=0)
    anno_orden_4 = models.IntegerField(default=0)
    supervisores_o_jefes_varones_orden_4 = models.IntegerField(default=0)
    supervisores_o_jefes_mujeres_orden_4 = models.IntegerField(default=0)
    empleados_varones_orden_4 = models.IntegerField(default=0)
    empleados_mujeres_orden_4 = models.IntegerField(default=0)
    empleadas_mujeres_orden_4 = models.IntegerField(default=0)
    obreros_hombres_orden_4 = models.IntegerField(default=0)
    obreras_mujeres_orden_4 = models.IntegerField(default=0)
    menores_varones_orden_4 = models.IntegerField(default=0)
    menores_mujeres_orden_4 = models.IntegerField(default=0)

    # Orden 4. Solo meteré un 4
    orden_4 = models.IntegerField(default=0)

    # Orden 5: Cantidad de egresos
    numero_patronal_orden_5 = models.IntegerField(default=0)
    anno_orden_5 = models.IntegerField(default=0)
    supervisores_o_jefes_varones_orden_5 = models.IntegerField(default=0)
    supervisores_o_jefes_mujeres_orden_5 = models.IntegerField(default=0)
    empleados_varones_orden_5 = models.IntegerField(default=0)
    empleados_mujeres_orden_5 = models.IntegerField(default=0)
    empleadas_mujeres_orden_5 = models.IntegerField(default=0)
    obreros_hombres_orden_5 = models.IntegerField(default=0)
    obreras_mujeres_orden_5 = models.IntegerField(default=0)
    menores_varones_orden_5 = models.IntegerField(default=0)
    menores_mujeres_orden_5 = models.IntegerField(default=0)

    # Orden 5. Solo meteré un 5
    orden_5 = models.IntegerField(default=0)

    timestamp = models.DateTimeField(default=date.today)

""" Modelo de la Planilla del IPS.

NOTA: Solo pondré los datos de cada empleado individual del IPS. No pondré ni los datos de la cabecera ni del pie de 
la planilla del IPS. Idealmente, Debería incluir también los datos de la cabecera y el pie de la planilla, para así 
colocar los datos de la empresa, y los datos de la cuota total que le debe la empresa al IPS. Y además, deberían haber 
20 empleados por hoja. 

Sin embargo, debido a falta de tiempo, no pondré ni los datos de la empresa, ni los datos de la cuota que le debe la 
empresa al IPS. 

Crearé el modelo para los empleados. Los campos que debo meter son:
•	Número de orden (del 1 al 20). Cada hoja solo deberia tener hasta 20 empleados. X
•	Cédula. X
•	Número de asegurado. X
•	Apellidos y Nombres. X
•	Días trabajados durante el mes anterior. X
•	Días trabajados durante el mes actual. X
•	Salario imponible. X
•	Categoría (empleador/mensualero u obrero/destajo) (pondré esos 2 con un <select>). X
•	Códigos (1_Entrada, 2_Salida, 3_Vacaciones, 4_Reposo, 5_indemnizacion, y 6_Otras Causas) (los pondré con un 
        <select>). X
•	RSA (Reconocimiento de Servicios Anteriores). (OPCIONAL) (<textarea>). Es anterior a 1974. X
•	Firma del encargado que deba entregar la planilla.  X
•	Timestamp. X

Pondre solo un caracter con un numero (integer) para los codigos, ya que solo aceptarán un numero del 1 al 6.

El numero de hoja tambien será un Integer.

Pondre una casilla de 30 caracteres para el numero del IPS.

Pondre Integers para los numeros de dias trabajados.
"""
class PlanillaIPS(models.Model):
    numero_de_orden = models.IntegerField(default=0)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    numero_de_asegurado = models.CharField(max_length=30)
    cedula = models.CharField(max_length=15)
    salario_imponible = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    categoria = models.CharField(max_length=50)
    codigo = models.IntegerField(default=0)
    dias_trabajados_mes_anterior = models.IntegerField(default=0)
    dias_trabajados_mes_actual = models.IntegerField(default=0)

    # RSA (OPCIONAL)
    reconocimiento_servicios_anteriores = models.TextField(blank=True)

    firma_encargado_rrhh = models.ImageField(upload_to="images/", default='')
    timestamp = models.DateTimeField(default=date.today)
