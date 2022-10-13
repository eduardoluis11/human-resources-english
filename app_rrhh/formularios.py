# Esto me deja usar los formularios de Django
from django import forms

# import datetime.date.today()
from datetime import date

""" Formulario para registrar una sanción.

El "widget=forms.Textarea" es para que el motivo y la sancion a aplicar sean un <textarea>.

El timestamp se creará automáticamente, por lo que no lo pondré aquí.

De verdad quiero poner un placeholder en la fecha del incidente, para que así los usuarios no se confundan al 
escribirlo. Dejame ver como hacer eso con formularios de Django (fuente del código:
https://code.djangoproject.com/ticket/16304 ).

"""
class FormularioRegistrarSancion(forms.Form):
    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    cedula_de_identidad = forms.CharField(max_length=15)
    motivo_de_la_sancion = forms.CharField(widget=forms.Textarea)
    sancion_que_se_le_aplicara = forms.CharField(widget=forms.Textarea)
    fecha_del_incidente = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

""" Formulario para registrar las bonificaciones familiares de un trabajador.

Los formularios de Django tienen DecimalField, y se usan exactamente igual que los DecimalField de los modelos de 
Django. Entonces, usaré exactamente lo mismo en DecimalField para los campos con números de bonificaciones familiares 
de los modelos que en los formularios de Django (con los 14 digitos).  

Usare el IntegerField del formulario de django para meter los números de hijos. 

No debo usar "default" en los formularios.

Voy a deshabilitar las casillas con el número total de hijos, y con la bonificación familiar total. voy a agregar el 
Disabled a las casillas que no quiero que se editen, y agregaré el código JS para rellenar automáticamente las casillas 
de números de hijos y de la bonificación familiar.

Para evitar que me salga NaN al sumar 2 casillas y 1 de ellas este vacia, voy a agregar por defecto el valor 0 en 
todas las casillas con números. Usar “initial” dento de campo del formulario con el número me funcionó a la perfección 
(fuente: https://stackoverflow.com/questions/604266/django-set-default-form-values ).

Perdí demsiado tiempo, y mi calculadora esta buggy (no me calcula el salario de manare correcta). Simplemente eliminare 
las casillas que están deshabilitadas, y pondré el calculo directamente en la bbdd. El calculo lo hare server side,
desde el view.

"""
class FormularioRegistrarBonificacion(forms.Form):
    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    cedula_de_identidad = forms.CharField(max_length=15)
    fecha_a_pagar = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    numero_de_hijos_menores = forms.IntegerField(initial = 0)
    numero_de_hijos_mayores_con_discapacidades = forms.IntegerField(initial = 0)
    salario_minimo_mensual_vigente = forms.DecimalField(max_digits=14, decimal_places=2, initial = 0)

    # numero_total_de_hijos_que_cualifican_para_la_bonificacion_familiar = forms.IntegerField(disabled=True,initial = 0)
    # bonificacion_familiar_a_recibir = forms.DecimalField(max_digits=14, decimal_places=2, disabled=True, initial = 0)

    # No funciona como quiero
    # numero_de_hijos_menores = forms.IntegerField(widget=forms.TextInput({"value": 0}))

""" Formulario para registrar un permiso para ausentarse.

Tengo que buscar como crear un campo en los formulario de Django que me permitan escoger una opción, ya sea con 
<select>, o con radio Check boxes. Tengo que usar un parámetro llamado “choices”, y usar 
“ChoiceField(choice=tupla_con_elecciones)”. La opción que está a la izquierda de la tupla es lo que se insertará
en la base de datos, mientras que lo que está en la derecha es lo que verá el usuario en el formulario.

Para que un campo sea opcional en los formularios de django, tengo que poner “required=false” 
"""
class FormularioRegistrarPermiso(forms.Form):

    # Opciones para el campo que pregunta si se le dará un descuento al trabajador
    RECIBIRA_DESCUENTO_CHOICES = [
        ('Sí', 'Sí'),
        ('No', 'No'),
    ]

    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    cedula_de_identidad = forms.CharField(max_length=15)
    fecha_de_inicio_de_la_ausencia = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))    # fecha desde que se va a ausentar
    fecha_de_reincorporacion = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))    # fecha en la que regresará
    motivo_de_la_ausencia = forms.CharField(widget=forms.Textarea)

    recibira_descuento = forms.ChoiceField(choices=RECIBIRA_DESCUENTO_CHOICES)  # "Sí" o "no"

    descuento_que_se_le_aplicara = forms.DecimalField(max_digits=14, decimal_places=2, initial = 0)
    foto_de_la_firma_del_trabajador_que_se_ausentara = forms.ImageField()
    foto_de_la_firma_del_encargado_que_le_concedio_el_permiso = forms.ImageField()

""" Formulario para registrar un Perfil de Cargo.
"""
class FormularioPerfilDeCargo(forms.Form):
    # Opciones para el campo que pregunta si el trabajador necesita tener auto
    REQUIERE_AUTO_PROPIO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    job_title = forms.CharField(max_length=100)

    experience_required = forms.CharField(widget=forms.Textarea)
    technical_skills_required = forms.CharField(widget=forms.Textarea)
    education = forms.CharField(widget=forms.Textarea)
    salary_range = forms.CharField(widget=forms.Textarea)

    other_requirements = forms.CharField(widget=forms.Textarea)

    does_it_require_having_a_car = forms.ChoiceField(choices=REQUIERE_AUTO_PROPIO_CHOICES)  # "Sí" o "no"

""" Formulario para registrar la Justificación de un Permiso.
"""
class FormularioJustificacion(forms.Form):
    # Opciones para el campo que pregunta si hay una diferencia entre lo que dice el permiso y el justificante
    DISCREPANCIA_CHOICES = [
        ('Sí', 'Sí'),
        ('No', 'No'),
    ]
    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    cedula_de_identidad = forms.CharField(max_length=15)
    fecha_de_inicio_de_la_ausencia = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))    # fecha desde que se va a ausentar
    fecha_de_reincorporacion = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))    # fecha en la que regresará

    # "Sí" o "no"
    existe_discrepancia_entre_el_permiso_y_la_justificacion = forms.ChoiceField(choices=DISCREPANCIA_CHOICES)

    foto_de_la_firma_del_encargado_que_reviso_la_justificacion = forms.ImageField()

    archivo_con_la_justificacion_del_permiso = forms.FileField()   # Archivo con justificación

""" Formulario para registrar los Descuentos de un trabajador.

Para que un campo sea opcional en los formularios de django, tengo que poner “required=False”.
"""
class FormularioDescuentos(forms.Form):
    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    cedula_de_identidad = forms.CharField(max_length=15)

    fecha_a_aplicar_el_descuento = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    salario_base = forms.DecimalField(max_digits=14, decimal_places=2, initial = 0)
    salario_con_ingresos_extras = forms.DecimalField(max_digits=14, decimal_places=2, initial = 0)
    descuento_por_cuota_del_ips = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    descuento_por_sanciones = forms.DecimalField(required=False, max_digits=14, decimal_places=2, initial=0)
    descuento_por_inasistencias = forms.DecimalField(required=False, max_digits=14, decimal_places=2, initial=0)

    otros_descuentos = forms.CharField(required=False, widget=forms.Textarea)  # Se meteran en un <textarea>

    # Suma de todos los descuentos
    suma_total_de_todos_los_descuentos_para_este_trabajador = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

""" Formulario para registrar los Ingresos Extras de un trabajador.

Va a ser muy similar al formulario de descuentos.

Voy a ver si la respuesta de Ten en este post me ayuda a poner un Date Picker para seleccionar la fecha (fuente: 
https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django .)
"""
class FormularioIngresosExtras(forms.Form):
    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    cedula_de_identidad = forms.CharField(max_length=15)

    # fecha_a_pagar_ingresos_a_trabajador = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    fecha_a_pagar_ingresos_a_trabajador = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    salario_base = forms.DecimalField(max_digits=14, decimal_places=2, initial = 0)

    ingresos_por_horas_extras = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    bonificacion_familiar = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    aguinaldos = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    otros_ingresos_extras = forms.CharField(required=False, widget=forms.Textarea)  # Se meteran en un <textarea>

    # Suma de todos los ingresos extras
    ingresos_extras_totales_para_este_trabajador = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

""" Formulario para registrar Vacaciones de un trabajador.

Ahora, haré el formulario. Todos los campos son obligatorios. NO pondré la casilla de los días restantes de vacaciones. 
Eso se calculará automáticamente  en el lado del servidor usando el view para registrar las vacaciones.
"""
class FormularioVacaciones(forms.Form):
    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    cedula_de_identidad = forms.CharField(max_length=15)

    # Días de vacaciones
    total_de_dias_de_vacaciones_disponibles_inicialmente = forms.IntegerField()
    dias_que_se_tomara_de_vacaciones = forms.IntegerField()

    # Fecha de inicio y fin de vacaciones
    fecha_de_inicio_de_sus_vacaciones = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    fecha_de_reincorporacion_al_trabajo = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    # Firmas
    foto_de_la_firma_del_trabajador_que_se_ausentara = forms.ImageField()
    foto_de_la_firma_del_encargado_que_le_concedio_las_vacaciones = forms.ImageField()

""" Formulario para Currículums.

Serán 14 campos (ya que no quiero el timestamp). RECUERDA poner “required=False” en los campos opcionales.

El sexo y si el candidato tiene auto lo meteré en dos tuplas distintas. Dejaré que el usuario los seleccione con un 
<select>.

La opción que está a la izquierda de la tupla es lo que se insertará en la base de datos, mientras que lo que está en 
la derecha es lo que verá el usuario en el formulario.

"""
class FormularioCurriculum(forms.Form):

    # Opciones para el campo que pregunta si el candidato tiene auto
    TIENE_AUTO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('DA', 'Did Not Answer')
    ]

    # Opciones para el campo que pregunta si el candidato es hombre o mujer
    SEXO_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    # Datos personales
    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    id_number = forms.CharField(max_length=15)
    sex = forms.ChoiceField(choices=SEXO_CHOICES)
    date_of_birth = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(widget=forms.Textarea, max_length=100)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField(required=False, max_length=254)

    job_position = forms.CharField(max_length=100)

    # Datos laborales
    experience = forms.CharField(widget=forms.Textarea)
    education = forms.CharField(widget=forms.Textarea)
    additional_information = forms.CharField(required=False, widget=forms.Textarea)
    has_their_own_car = forms.ChoiceField(choices=TIENE_AUTO_CHOICES)

    # PDF con curriculum (opcional)
    resume_in_pdf = forms.FileField(required=False)

""" Formulario de Aguinaldos.

No voy a poner ni el timestamp ni el total de aguinaldos. Los aguinaldos los calculare en el view, es decir, 
en el lado del servidor.
"""
class FormularioAguinaldos(forms.Form):
    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    cedula_de_identidad = forms.CharField(max_length=15)

    # Año en el que se pagarán los aguinaldos
    anno_al_que_corresponden = forms.IntegerField(initial=0)

    # Salario de cada mes del trabajador
    salario_enero = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    salario_febrero = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    salario_marzo = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    salario_abril = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    salario_mayo = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    salario_junio = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    salario_julio = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    salario_agosto = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    salario_septiembre = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    salario_octubre = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    salario_noviembre = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    salario_diciembre = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

""" Formulario para agregar Días para la Asistencia.

Solo necesito la fecha. No necesito la hora.
"""
class FormularioFechas(forms.Form):
    attendance_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

""" Formulario para agregar las Asistencias de cada trabajador.

Una vez mas, usaré el “TimeField” para los campos de la hora y la salida.

No pondre ni el timestamp, ni la fecha de la asistencia.
"""
class FormularioAsistencias(forms.Form):

    # Opciones "si/no" para saber si el trabajador vino a trabajar
    VINO_AL_TRABAJO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    cedula_de_identidad = forms.CharField(max_length=15)

    vino_a_trabajar = forms.ChoiceField(choices=VINO_AL_TRABAJO_CHOICES)

    # Horas de entrada y salida (pueden estar vacíos)
    hora_de_llegada = forms.TimeField(initial='01:00', widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
    hora_de_salida = forms.TimeField(initial='01:00', widget=forms.widgets.TimeInput(attrs={'type': 'time'}))

""" Formulario para registrar la Liquidación del Personal.

Pondré un placeholder para “tipo de salario” que diga “mensual, jornal, etc”.

No pondré ni el timestamp, ni el salario total que debe ser liquidado. Esto ultimo se calcula en el view.
"""
class FormularioLiquidacionDelPersonal(forms.Form):
    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    cedula_de_identidad = forms.CharField(max_length=15)

    cargo_del_trabajador = forms.CharField(max_length=100)

    fecha_de_inicio_del_contrato = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    fecha_de_fin_del_contrato = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    motivo_de_la_finalizacion_de_su_contrato = forms.CharField(widget=forms.Textarea)

    # Pondre un placeholder (mensuual, jornal, quincenal, etc.)
    tipo_de_salario = forms.CharField(max_length=200, widget=forms.TextInput({"placeholder": "Ej: Mensual, Jornal, etc"}))

    # Salarios para sumar para calcular la liquidación
    salario_mensual = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    vacaciones_no_disfrutadas = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    aguinaldos = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    salario_por_horas_extras = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    otros_ingresos = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # Descuentos (debo restarlo a los ingresos)
    descuentos_en_total = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # Foto del encargado que calculó el total a liquidar
    firma_del_encargado_que_le_calculo_la_liquidacion = forms.ImageField()

""" Formulario para Liquidación de Salarios.

No pondré ni el timestamp, ni el salario total a pagar.
"""
class FormularioLiquidacionDeSalario(forms.Form):
    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    cedula_de_identidad = forms.CharField(max_length=15)

    # Salarios para sumar para calcular la liquidación
    salario_mensual = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    ingresos_extras = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # Descuentos (debo restarlo a los ingresos)
    descuentos = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # Fecha en la que se hará el pago
    fecha_de_pago = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    # Foto del encargado que calculó el total a liquidar
    firma_del_encargado_que_le_calculo_la_liquidacion = forms.ImageField()

""" Crearé 4 formularios para el Legajo. Eso lo haré para asignarle un título distinto a cada grupo de casillas
de cada formulario (ej: "Datos Personales, Otros Datos de interes", etc.)
"""

""" Formulario de Datos Personales del Legajo.

Quiero que el domicilio sea un <textarea>.
"""
class FormularioDatosPersonalesLegajo(forms.Form):

    # Opciones para el campo que pregunta si el trabajador es hombre o mujer
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    cedula_de_identidad = forms.CharField(max_length=15)
    fecha_de_vencimiento_de_la_cedula = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    fecha_de_nacimiento = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    sexo = forms.ChoiceField(choices=SEXO_CHOICES)
    nacionalidad = forms.CharField(max_length=20)
    domicilio = forms.CharField(widget=forms.Textarea)
    telefono = forms.CharField(max_length=20)
    correo_electronico = forms.EmailField(required=False, max_length=254)
    curriculum = forms.FileField()  # PDF con currículum
    titulo_o_nivel_maximo_de_educacion_obtenido = forms.CharField(max_length=100)

""" Formulario de Información Jurídica del Legajo.
"""
class FormularioInformacionJuridicaLegajo(forms.Form):

    # Opciones para el campo que pregunta si el trabajador tiene antecedentes penales
    ANTECEDENTES_CHOICES = [
        ('Sí', 'Sí'),
        ('No', 'No'),
    ]

    tiene_antecedentes_penales = forms.ChoiceField(choices=ANTECEDENTES_CHOICES)
    numero_del_ips = forms.CharField(max_length=30)

""" Formulario de Datos de la Administracion Interna de la Empresa del Legajo.
"""
class FormularioAdministracionEmpresaLegajo(forms.Form):
    permisos_que_ha_tomado_para_ausentarse = forms.CharField(required=False, widget=forms.Textarea) # Opcional
    evaluacion_de_desempeno = forms.FileField(required=False)  # Archivo con evaluación de desempeño (opcional)
    sanciones = forms.CharField(required=False, widget=forms.Textarea)  # Opcional
    cargo = forms.CharField(max_length=100)

""" Formulario de Datos de Otros Datos de Interés del Legajo (opcional).
"""
class FormularioOtrosDatosLegajo(forms.Form):
    otros_datos_de_interes = forms.CharField(required=False, widget=forms.Textarea)  # Opcional

""" Formulario de Datos Personales para Registrar un Contrato.
"""
class FormularioDatosPersonalesContrato(forms.Form):
    # Opciones para el campo que pregunta si el trabajador es hombre o mujer
    SEXO_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    id_number = forms.CharField(max_length=15)
    date_of_birth = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    sex = forms.ChoiceField(choices=SEXO_CHOICES)
    address = forms.CharField(widget=forms.Textarea)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField(required=False, max_length=254)
    degree_or_maximum_level_of_education_achieved = forms.CharField(max_length=100)
    social_security_number = forms.CharField(max_length=30)
    bank_account_number = forms.CharField(max_length=30)

""" Formulario de Datos del Contrato para Registrar un Contrato.

No pondré el timestamp.
"""
class FormularioDatosDelContrato(forms.Form):

    # Opciones para el campo que pregunta si el trabajador va a trabajar a tiempo parcial o completo
    TIEMPO_COMPLETO_O_PARCIAL_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
    ]

    job_title = forms.CharField(max_length=100)
    job_type = forms.ChoiceField(choices=TIEMPO_COMPLETO_O_PARCIAL_CHOICES)
    contract_clauses = forms.FileField()  # Archivo con clausulas del contrato
    signature_of_the_recruit = forms.ImageField()
    signature_of_the_manager_who_created_the_contract = forms.ImageField()

""" Formulario para Registrar un Informe Web Anual.
"""
class FormularioInformeWeb(forms.Form):
    anno_del_informe = forms.IntegerField(initial=0)
    evaluacion_de_desempeno_anual_de_todo_el_personal = forms.FileField()  # Archivo con clausulas del contrato
    salario_promedio_de_todo_el_personal = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    tasa_de_absentismo = forms.CharField(max_length=20)
    trabajadores_contratados = forms.IntegerField(initial=0)
    trabajadores_que_salieron = forms.IntegerField(initial=0)
    edad_promedio_del_personal = forms.IntegerField(initial=0)
    promedio_de_dias_para_contratar_a_alguien_para_un_cargo_vacante = forms.IntegerField(initial=0)
    annos_que_ha_trabajado_el_trabajador_con_mas_tiempo_en_la_empresa = forms.IntegerField(initial=0)
    numero_de_cursos_ofrecidos_al_personal = forms.IntegerField(initial=0)

""" Aquí pondré los 5 formularios de la planilla "Resumen General" del Ministerio de Trabajo
El número de los ordenes se meteran automaticamente a la base de datos. NO lo pondre en los formularios.

Tengo que escribir el numero de orden en el formulario tambien, ya que el view tiene que saber que campo en
específico tiene que agarrar para meterlo a la base de datos.
"""

# Orden 1: Cantidad de empleados
class FormularioResumenGeneralOrden1(forms.Form):
    numero_patronal_orden_1 = forms.IntegerField(initial=0)
    anno_orden_1 = forms.IntegerField(initial=0)
    supervisores_o_jefes_varones_orden_1 = forms.IntegerField(initial=0)
    supervisores_o_jefes_mujeres_orden_1 = forms.IntegerField(initial=0)
    empleados_varones_orden_1 = forms.IntegerField(initial=0)
    empleados_mujeres_orden_1 = forms.IntegerField(initial=0)
    empleadas_mujeres_orden_1 = forms.IntegerField(initial=0)
    obreros_hombres_orden_1 = forms.IntegerField(initial=0)
    obreras_mujeres_orden_1 = forms.IntegerField(initial=0)
    menores_varones_orden_1 = forms.IntegerField(initial=0)
    menores_mujeres_orden_1 = forms.IntegerField(initial=0)

# Orden 2: Horas trabajadas
class FormularioResumenGeneralOrden2(forms.Form):
    numero_patronal_orden_2 = forms.IntegerField(initial=0)
    anno_orden_2 = forms.IntegerField(initial=0)
    supervisores_o_jefes_varones_orden_2 = forms.IntegerField(initial=0)
    supervisores_o_jefes_mujeres_orden_2 = forms.IntegerField(initial=0)
    empleados_varones_orden_2 = forms.IntegerField(initial=0)
    empleados_mujeres_orden_2 = forms.IntegerField(initial=0)
    empleadas_mujeres_orden_2 = forms.IntegerField(initial=0)
    obreros_hombres_orden_2 = forms.IntegerField(initial=0)
    obreras_mujeres_orden_2 = forms.IntegerField(initial=0)
    menores_varones_orden_2 = forms.IntegerField(initial=0)
    menores_mujeres_orden_2 = forms.IntegerField(initial=0)

# Orden 3: Sueldos o jornales
class FormularioResumenGeneralOrden3(forms.Form):
    numero_patronal_orden_3 = forms.IntegerField(initial=0)
    anno_orden_3 = forms.IntegerField(initial=0)
    supervisores_o_jefes_varones_orden_3 = forms.IntegerField(initial=0)
    supervisores_o_jefes_mujeres_orden_3 = forms.IntegerField(initial=0)
    empleados_varones_orden_3 = forms.IntegerField(initial=0)
    empleados_mujeres_orden_3 = forms.IntegerField(initial=0)
    empleadas_mujeres_orden_3 = forms.IntegerField(initial=0)
    obreros_hombres_orden_3 = forms.IntegerField(initial=0)
    obreras_mujeres_orden_3 = forms.IntegerField(initial=0)
    menores_varones_orden_3 = forms.IntegerField(initial=0)
    menores_mujeres_orden_3 = forms.IntegerField(initial=0)

# Orden 4: Cantidad de ingresos
class FormularioResumenGeneralOrden4(forms.Form):
    numero_patronal_orden_4 = forms.IntegerField(initial=0)
    anno_orden_4 = forms.IntegerField(initial=0)
    supervisores_o_jefes_varones_orden_4 = forms.IntegerField(initial=0)
    supervisores_o_jefes_mujeres_orden_4 = forms.IntegerField(initial=0)
    empleados_varones_orden_4 = forms.IntegerField(initial=0)
    empleados_mujeres_orden_4 = forms.IntegerField(initial=0)
    empleadas_mujeres_orden_4 = forms.IntegerField(initial=0)
    obreros_hombres_orden_4 = forms.IntegerField(initial=0)
    obreras_mujeres_orden_4 = forms.IntegerField(initial=0)
    menores_varones_orden_4 = forms.IntegerField(initial=0)
    menores_mujeres_orden_4 = forms.IntegerField(initial=0)

# Orden 5: Cantidad de egresos
class FormularioResumenGeneralOrden5(forms.Form):
    numero_patronal_orden_5 = forms.IntegerField(initial=0)
    anno_orden_5 = forms.IntegerField(initial=0)
    supervisores_o_jefes_varones_orden_5 = forms.IntegerField(initial=0)
    supervisores_o_jefes_mujeres_orden_5 = forms.IntegerField(initial=0)
    empleados_varones_orden_5 = forms.IntegerField(initial=0)
    empleados_mujeres_orden_5 = forms.IntegerField(initial=0)
    empleadas_mujeres_orden_5 = forms.IntegerField(initial=0)
    obreros_hombres_orden_5 = forms.IntegerField(initial=0)
    obreras_mujeres_orden_5 = forms.IntegerField(initial=0)
    menores_varones_orden_5 = forms.IntegerField(initial=0)
    menores_mujeres_orden_5 = forms.IntegerField(initial=0)

# Fin de los 5 formularios para la planilla "Resumen General" del Ministerio de Trabajo

""" Planilla de Empleados y Obreros del Ministerio de Trabajo.

NO voy a poner el "estado". Eso lo podnre automaticamente en la base de datos.

Recuerda que hay algunos campos aquí que son opcionales (por ejemplo, fecha de salida si el trabajador NO ha dejado
la compañía.)

O le dejo al usuario escribir la letra del estado civil, o la pongo como un <select> con CHOICES. Como ya salen 
las unicas 4 opciones que puedo poner en el ejemplo de la planilla del ministerio de trabajo (S, V, D, y C), 
usare un <selct>.

Dejame ver como poner una fecha por defecto en django. Sino, siempre tendre que poner una fecha de nacimiento de un 
hijo menor (aunque no lo tenga), o fecha de salida (aunque aun trabaje en la empresa). Esto me debería servir: 
https://stackoverflow.com/questions/36881089/django-form-setting-initial-value-on-datefield .
Usaré esta fecha por defecto: 
initial=0001-01-01 

"""
class FormularioEmpleadosMinisterioDeTrabajo(forms.Form):
    # Opciones para el campo que pregunta si el trabajador es hombre o mujer
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    # Opciones para el campo que pregunta el estado civil
    ESTADO_CIVIL_CHOICES = [
        ('S', 'Soltero'),
        ('C', 'Casado'),
        ('D', 'Divorciado'),
        ('V', 'Viuda'),
    ]

    numero_patronal_de_planilla_empleados = forms.IntegerField(initial=0)
    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    cedula_de_identidad = forms.CharField(max_length=15)
    fecha_de_nacimiento = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    sexo = forms.ChoiceField(choices=SEXO_CHOICES)
    domicilio = forms.CharField(widget=forms.Textarea)
    cargo = forms.CharField(max_length=100)
    profesion = forms.CharField(max_length=100)
    nacionalidad = forms.CharField(max_length=20)

    estado_civil = forms.ChoiceField(choices=ESTADO_CIVIL_CHOICES)

    fecha_entrada = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    # OPCIONAL
    fecha_salida = forms.DateField(initial='0001-01-01', required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    cantidad_hijos_menores = forms.IntegerField(required=False, initial=0)  # OPCIONAL
    motivo_de_salida = forms.CharField(required=False, max_length=100)  # OPCIONAL
    horario_de_trabajo = forms.CharField(max_length=20)
    situacion_escolar_menor = forms.CharField(required=False, max_length=20)    # OPCIONAL

    # OPCIONAL
    fecha_nacimiento_del_menor = forms.DateField(initial='0001-01-01', required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    # OPCIONAL
    fecha_inicio_trabajo_del_menor = forms.DateField(initial='0001-01-01', required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))


""" Planilla de Sueldos y Jornales del Ministerio de Trabajo.

Pondre a todos los campos un valor de "0" por defecto para no estar pendiente si un campo es opcional o no.

Tengo que crear un <select> para la forma de pago (J o M).

Los montos totales NO los voy a poner aquí (si los sé calcular): los calcularé en el view en el backend. 

El del sueldo en 50% por horas exras lo puedo calcular en el view en el back end dividiendo entre 2 el monto
total de los ingresos por horas extras. NO tengo porque ponerlo aquí.

El sueldo al 50%, y el total percibido incluyendo los aguinaldos y otros ingresos extras lo calculare en el view.
TODO lo demas se tendra que escribir en el formulario.
"""
class FormularioSueldosMinisterioDeTrabajo(forms.Form):
    # Opciones para el campo que pregunta la forma de pago
    FORMA_PAGO_CHOICES = [
        ('M', 'Mensual'),
        ('J', 'Jornal'),
    ]

    numero_patronal_de_planilla_sueldos = forms.IntegerField(initial=0)
    forma_de_pago = forms.ChoiceField(choices=FORMA_PAGO_CHOICES)
    cedula_planilla_sueldos = forms.CharField(max_length=15)

    importe_unitario = forms.IntegerField(initial=0)

    # Horas trabajadas y salarios percibidos en el año
    horas_trabajadas_enero = forms.IntegerField(initial=0)
    salario_percibido_enero = forms.IntegerField(initial=0)
    horas_trabajadas_febrero = forms.IntegerField(initial=0)
    salario_percibido_febrero = forms.IntegerField(initial=0)
    horas_trabajadas_marzo = forms.IntegerField(initial=0)
    salario_percibido_marzo = forms.IntegerField(initial=0)
    horas_trabajadas_abril = forms.IntegerField(initial=0)
    salario_percibido_abril = forms.IntegerField(initial=0)
    horas_trabajadas_mayo = forms.IntegerField(initial=0)
    salario_percibido_mayo = forms.IntegerField(initial=0)
    horas_trabajadas_junio = forms.IntegerField(initial=0)
    salario_percibido_junio = forms.IntegerField(initial=0)
    horas_trabajadas_julio = forms.IntegerField(initial=0)
    salario_percibido_julio = forms.IntegerField(initial=0)
    horas_trabajadas_agosto = forms.IntegerField(initial=0)
    salario_percibido_agosto = forms.IntegerField(initial=0)
    horas_trabajadas_septiembre = forms.IntegerField(initial=0)
    salario_percibido_septiembre = forms.IntegerField(initial=0)
    horas_trabajadas_octubre = forms.IntegerField(initial=0)
    salario_percibido_octubre = forms.IntegerField(initial=0)
    horas_trabajadas_noviembre = forms.IntegerField(initial=0)
    salario_percibido_noviembre = forms.IntegerField(initial=0)
    horas_trabajadas_diciembre = forms.IntegerField(initial=0)
    salario_percibido_diciembre = forms.IntegerField(initial=0) # Fin salarios y horas durante el año

    horas_extras_100_por_ciento_durante_anno = forms.IntegerField(initial=0)
    salario_percibido_horas_extras_100_por_ciento_anno = forms.IntegerField(initial=0)

    aguinaldo = forms.IntegerField(initial=0)
    beneficios = forms.IntegerField(initial=0)
    bonificaciones = forms.IntegerField(initial=0)
    vacaciones = forms.IntegerField(initial=0)
    horas_trabajadas_incluyendo_horas_extras = forms.IntegerField(initial=0)

    # Este es el salario total SIN los ingresos extras
    total_recibido_en_concepto_de_salario_sin_ingresos_extras = forms.IntegerField(initial=0)


""" Formulario para Generar Planillas del IPS.

Para la Categoria y los Codigos, pondre un Choice/<select>.

•	Categoría (empleador/mensualero u obrero/destajo) (pondré esos 2 con un <select>). 

•	Códigos (1_Entrada, 2_Salida, 3_Vacaciones, 4_Reposo, 5_indemnizacion, y 6_Otras Causas) (los pondré con un 
        <select>).
"""
class FormularioPlanillaIPS(forms.Form):

    # Opciones para el campo del código
    CODIGO_CHOICES = [
        ('1', '1: Entrada'),
        ('2', '2: Salida'),
        ('3', '3: Vacaciones'),
        ('4', '4: Reposo'),
        ('5', '5: Indemnización'),
        ('6', '6: Otras Causas'),
    ]

    # Opciones para el campo del código
    CATEGORIA_CHOICES = [
        ('Empleador/Mensualero', 'Empleador/Mensualero'),
        ('Obrero/Destajo', 'Obrero/Destajo'),
    ]

    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    cedula_de_identidad = forms.CharField(max_length=15)
    numero_de_asegurado = forms.CharField(max_length=30)
    numero_de_orden = forms.IntegerField(initial=0)
    dias_trabajados_mes_anterior = forms.IntegerField(initial=0)
    dias_trabajados_mes_actual = forms.IntegerField(initial=0)
    salario_imponible = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    codigo = forms.ChoiceField(choices=CODIGO_CHOICES)
    categoria = forms.ChoiceField(choices=CATEGORIA_CHOICES)
    reconocimiento_servicios_anteriores = forms.CharField(widget=forms.Textarea)        # RSA (OPCIONAL)
    firma_del_encargado_que_creo_la_planilla = forms.ImageField()