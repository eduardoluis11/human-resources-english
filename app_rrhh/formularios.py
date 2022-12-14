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
    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    id_number = forms.CharField(max_length=15)
    reason_for_the_sanction = forms.CharField(widget=forms.Textarea)
    sanction_that_will_be_applied = forms.CharField(widget=forms.Textarea)
    date_of_the_incident = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

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
    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    id_number = forms.CharField(max_length=15)

    # fecha_a_pagar
    date_to_make_the_payment = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    # numero_de_hijos_menores
    number_of_underage_children = forms.IntegerField(initial=0)

    # numero_de_hijos_mayores_con_discapacidades
    number_of_adult_children_with_disabilities = forms.IntegerField(initial=0)

    # salario_minimo_mensual_vigente
    current_monthly_minimum_wage = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

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
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    id_number = forms.CharField(max_length=15)

    # fecha_de_inicio_de_la_ausencia
    absence_start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))    # fecha desde que se va a ausentar

    # fecha_de_reincorporacion
    absence_end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))    # fecha en la que regresará

    # motivo_de_la_ausencia
    reason_for_the_absence = forms.CharField(widget=forms.Textarea)

    # recibira_descuento
    will_they_receive_a_discount = forms.ChoiceField(choices=RECIBIRA_DESCUENTO_CHOICES)  # "Sí" o "no"

    # descuento_que_se_le_aplicara
    discount_that_will_be_applied = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # foto_de_la_firma_del_trabajador_que_se_ausentara
    signature_of_the_employee_that_will_be_absent = forms.ImageField()

    # foto_de_la_firma_del_encargado_que_le_concedio_el_permiso
    signature_of_the_manager_that_game_them_the_permission_to_leave = forms.ImageField()

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
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    id_number = forms.CharField(max_length=15)
    absence_start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))    # fecha desde que se va a ausentar
    absence_end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))    # fecha en la que regresará

    # "Sí" o "no"
    is_there_a_discrepancy_between_the_permission_and_the_proof_of_leave = forms.ChoiceField(choices=DISCREPANCIA_CHOICES)

    signature_of_the_manager_that_checked_the_proof = forms.ImageField()

    file_with_the_scanned_proof_of_leave_of_absence = forms.FileField()   # Archivo con justificación

""" Formulario para registrar los Descuentos de un trabajador.

Para que un campo sea opcional en los formularios de django, tengo que poner “required=False”.
"""
class FormularioDescuentos(forms.Form):
    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    id_number = forms.CharField(max_length=15)

    # fecha_a_aplicar_el_descuento
    date_to_apply_discount = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    base_salary = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # salario_con_ingresos_extras
    salary_with_extra_income = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # descuento_por_cuota_del_ips
    social_security_discount = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # descuento_por_sanciones
    discounts_due_to_sanctions = forms.DecimalField(required=False, max_digits=14, decimal_places=2, initial=0)

    # descuento_por_inasistencias
    discounts_due_to_nonattendances = forms.DecimalField(required=False, max_digits=14, decimal_places=2, initial=0)

    # otros_descuentos
    other_discounts = forms.CharField(required=False, widget=forms.Textarea)  # Se meteran en un <textarea>

    # Suma de todos los descuentos
    # suma_total_de_todos_los_descuentos_para_este_trabajador
    sum_of_all_the_discounts_for_this_employee = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

""" Formulario para registrar los Ingresos Extras de un trabajador.

Va a ser muy similar al formulario de descuentos.

Voy a ver si la respuesta de Ten en este post me ayuda a poner un Date Picker para seleccionar la fecha (fuente: 
https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django .)
"""
class FormularioIngresosExtras(forms.Form):
    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    id_number = forms.CharField(max_length=15)

    # fecha_a_pagar_ingresos_a_trabajador = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    date_in_which_the_payment_will_be_made = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    base_salary = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # ingresos_por_horas_extras
    income_from_extra_hours = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # bonificacion_familiar
    income_from_large_family_bonus = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # aguinaldos
    income_from_christmas_bonus = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # otros_ingresos_extras
    other_supplemental_income = forms.CharField(required=False, widget=forms.Textarea)  # Se meteran en un <textarea>

    # Suma de todos los ingresos extras
    # ingresos_extras_totales_para_este_trabajador
    total_supplemental_income = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

""" Formulario para registrar Vacaciones de un trabajador.

Ahora, haré el formulario. Todos los campos son obligatorios. NO pondré la casilla de los días restantes de vacaciones. 
Eso se calculará automáticamente  en el lado del servidor usando el view para registrar las vacaciones.
"""
class FormularioVacaciones(forms.Form):
    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    id_number = forms.CharField(max_length=15)

    # Días de vacaciones
    initial_number_of_vacation_days = forms.IntegerField()
    number_of_vacation_days_that_they_will_take = forms.IntegerField()

    # Fecha de inicio y fin de vacaciones
    vacation_start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    vacation_end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    # Firmas
    signature_of_the_employee_that_will_be_on_vacation = forms.ImageField()

    # foto_de_la_firma_del_encargado_que_le_concedio_las_vacaciones
    signature_of_the_manager_that_authorized_their_vacation = forms.ImageField()

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
    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    id_number = forms.CharField(max_length=15)

    # Año en el que se pagarán los aguinaldos
    # anno_al_que_corresponden
    year_of_the_christmas_bonus_payment = forms.IntegerField(initial=0)

    # Salario de cada mes del trabajador
    # salario_enero
    income_from_january = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    income_from_february = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    income_from_march = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    income_from_april = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    income_from_may = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    income_from_june = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    income_from_july = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    income_from_august = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    income_from_september = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    income_from_october = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    income_from_november = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    income_from_december = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

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

    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    id_number = forms.CharField(max_length=15)

    did_they_come_to_work = forms.ChoiceField(choices=VINO_AL_TRABAJO_CHOICES)

    # Horas de entrada y salida (pueden estar vacíos)
    arrival_time = forms.TimeField(initial='01:00', widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
    exit_time = forms.TimeField(initial='01:00', widget=forms.widgets.TimeInput(attrs={'type': 'time'}))

""" Formulario para registrar la Liquidación del Personal.

Pondré un placeholder para “tipo de salario” que diga “mensual, jornal, etc”.

No pondré ni el timestamp, ni el salario total que debe ser liquidado. Esto ultimo se calcula en el view.
"""
class FormularioLiquidacionDelPersonal(forms.Form):
    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    id_number = forms.CharField(max_length=15)

    # cargo_del_trabajador
    job_position_of_the_employee = forms.CharField(max_length=100)

    # fecha_de_inicio_del_contrato
    start_date_of_the_contract = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    # fecha_de_fin_del_contrato
    end_date_of_the_contract = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    # motivo_de_la_finalizacion_de_su_contrato
    reason_for_leaving_the_company = forms.CharField(widget=forms.Textarea)

    # Pondre un placeholder (mensuual, jornal, quincenal, etc.)
    # tipo_de_salario
    salary_type = forms.CharField(max_length=200, widget=forms.TextInput({
        "placeholder": "i.e: Monthly, Daily, etc"
    }))

    # Salarios para sumar para calcular la liquidación
    # salario_mensual
    monthly_salary = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # vacaciones_no_disfrutadas
    income_from_unused_vacation_days = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # aguinaldos
    accrued_christmas_bonus = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # salario_por_horas_extras
    income_from_working_extra_hours = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # otros_ingresos
    other_supplemental_income = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # Descuentos (debo restarlo a los ingresos)
    # descuentos_en_total
    total_amount_to_discount = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # Foto del encargado que calculó el total a liquidar
    # firma_del_encargado_que_le_calculo_la_liquidacion
    signature_of_the_manager_that_authorized_the_final_pay = forms.ImageField()

""" Formulario para Liquidación de Salarios.

No pondré ni el timestamp, ni el salario total a pagar.
"""
class FormularioLiquidacionDeSalario(forms.Form):
    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    id_number = forms.CharField(max_length=15)

    # Salarios para sumar para calcular la liquidación
    monthly_wage = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)
    supplemental_income = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # Descuentos (debo restarlo a los ingresos)
    discounts = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # Fecha en la que se hará el pago
    payment_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    # Foto del encargado que calculó el total a liquidar
    # firma_del_encargado_que_le_calculo_la_liquidacion
    signature_of_the_manager_that_created_the_payroll_report = forms.ImageField()

""" Crearé 4 formularios para el Legajo. Eso lo haré para asignarle un título distinto a cada grupo de casillas
de cada formulario (ej: "Datos Personales, Otros Datos de interes", etc.)
"""

""" Formulario de Datos Personales del Legajo.

Quiero que el domicilio sea un <textarea>.
"""
class FormularioDatosPersonalesLegajo(forms.Form):

    # Opciones para el campo que pregunta si el trabajador es hombre o mujer
    SEXO_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    id_number = forms.CharField(max_length=15)

    expiry_date_of_the_id = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    date_of_birth = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    gender = forms.ChoiceField(choices=SEXO_CHOICES)

    nationality = forms.CharField(max_length=20)

    address = forms.CharField(widget=forms.Textarea)

    phone = forms.CharField(max_length=20)

    email = forms.EmailField(required=False, max_length=254)

    resume = forms.FileField()  # PDF con currículum

    degree_or_maximum_level_of_education_achieved = forms.CharField(max_length=100)

""" Formulario de Información Jurídica del Legajo.
"""
class FormularioInformacionJuridicaLegajo(forms.Form):

    # Opciones para el campo que pregunta si el trabajador tiene antecedentes penales
    ANTECEDENTES_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    # tiene_antecedentes_penales
    do_they_have_a_criminal_record = forms.ChoiceField(choices=ANTECEDENTES_CHOICES)

    social_security_number = forms.CharField(max_length=30)

""" Formulario de Datos de la Administracion Interna de la Empresa del Legajo.
"""
class FormularioAdministracionEmpresaLegajo(forms.Form):

    # permisos_que_ha_tomado_para_ausentarse
    leaves_of_absence_taken = forms.CharField(required=False, widget=forms.Textarea)  # Opcional

    # evaluacion_de_desempeno
    performance_appraisal_report = forms.FileField(required=False)  # Archivo con evaluación de desempeño (opcional)

    sanctions = forms.CharField(required=False, widget=forms.Textarea)  # Opcional

    job_title = forms.CharField(max_length=100)

""" Formulario de Datos de Otros Datos de Interés del Legajo (opcional).
"""
class FormularioOtrosDatosLegajo(forms.Form):

    # otros_datos_de_interes
    other_data = forms.CharField(required=False, widget=forms.Textarea)  # Opcional

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

    # anno_del_informe
    year_of_the_report = forms.IntegerField(initial=0)

    # evaluacion_de_desempeno_anual_de_todo_el_personal
    annual_performance_appraisal_report_of_the_entire_staff = forms.FileField()  # Archivo con clausulas del contrato

    # salario_promedio_de_todo_el_personal
    average_monthly_salary_of_the_entire_staff = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    # tasa_de_absentismo
    absence_rate = forms.CharField(max_length=20)

    # trabajadores_contratados
    number_of_employees_hired = forms.IntegerField(initial=0)

    # trabajadores_que_salieron
    number_of_employees_that_left_the_company = forms.IntegerField(initial=0)

    average_age_of_the_entire_staff = forms.IntegerField(initial=0)

    # promedio_de_dias_para_contratar_a_alguien_para_un_cargo_vacante
    average_number_of_days_to_hire_a_recruit_for_a_vacant_position = forms.IntegerField(initial=0)

    # annos_que_ha_trabajado_el_trabajador_con_mas_tiempo_en_la_empresa
    number_of_years_of_the_longest_job_tenure_in_the_company = forms.IntegerField(initial=0)

    # numero_de_cursos_ofrecidos_al_personal
    number_of_courses_offered_to_the_staff = forms.IntegerField(initial=0)

""" Aquí pondré los 5 formularios de la planilla "Resumen General" del Ministerio de Trabajo
El número de los ordenes se meteran automaticamente a la base de datos. NO lo pondre en los formularios.

Tengo que escribir el numero de orden en el formulario tambien, ya que el view tiene que saber que campo en
específico tiene que agarrar para meterlo a la base de datos.
"""

# Orden 1: Cantidad de empleados
class FormularioResumenGeneralOrden1(forms.Form):

    # numero_patronal_orden_1
    employer_identification_number_for_order_1_form = forms.IntegerField(initial=0)

    # anno_for_order_1_form
    year_for_order_1_form = forms.IntegerField(initial=0)

    # supervisores_o_jefes_varones_orden_1
    male_managers_or_bosses_for_order_1_form = forms.IntegerField(initial=0)

    # supervisores_o_jefes_mujeres_for_order_1_form
    female_managers_or_bosses_for_order_1_form = forms.IntegerField(initial=0)

    # empleados_varones_for_order_1_form
    male_assistants_for_order_1_form = forms.IntegerField(initial=0)

    # empleados_mujeres_for_order_1_form
    # female_assistants_for_order_1_form = forms.IntegerField(initial=0)

    # empleadas_mujeres_for_order_1_form
    female_assistants_for_order_1_form = forms.IntegerField(initial=0)

    # obreros_hombres_for_order_1_form
    male_laborers_for_order_1_form = forms.IntegerField(initial=0)

    # obreras_mujeres_for_order_1_form
    female_laborers_for_order_1_form = forms.IntegerField(initial=0)

    # menores_varones_for_order_1_form
    underage_males_for_order_1_form = forms.IntegerField(initial=0)

    # menores_mujeres_for_order_1_form
    underage_females_for_order_1_form = forms.IntegerField(initial=0)

# Orden 2: Horas trabajadas
class FormularioResumenGeneralOrden2(forms.Form):
    employer_identification_number_for_order_2_form = forms.IntegerField(initial=0)
    year_for_order_2_form = forms.IntegerField(initial=0)
    male_managers_or_bosses_for_order_2_form = forms.IntegerField(initial=0)
    female_managers_or_bosses_for_order_2_form = forms.IntegerField(initial=0)
    male_assistants_for_order_2_form = forms.IntegerField(initial=0)
    # empleados_mujeres_orden_2 = forms.IntegerField(initial=0)
    female_assistants_for_order_2_form = forms.IntegerField(initial=0)
    male_laborers_for_order_2_form = forms.IntegerField(initial=0)
    female_laborers_for_order_2_form = forms.IntegerField(initial=0)
    underage_males_for_order_2_form = forms.IntegerField(initial=0)
    underage_females_for_order_2_form = forms.IntegerField(initial=0)

# Orden 3: Sueldos o jornales
class FormularioResumenGeneralOrden3(forms.Form):
    employer_identification_number_for_order_3_form = forms.IntegerField(initial=0)
    year_for_order_3_form = forms.IntegerField(initial=0)
    male_managers_or_bosses_for_order_3_form = forms.IntegerField(initial=0)
    female_managers_or_bosses_for_order_3_form = forms.IntegerField(initial=0)
    male_assistants_for_order_3_form = forms.IntegerField(initial=0)
    # empleados_mujeres_orden_3 = forms.IntegerField(initial=0)
    female_assistants_for_order_3_form = forms.IntegerField(initial=0)
    male_laborers_for_order_3_form = forms.IntegerField(initial=0)
    female_laborers_for_order_3_form = forms.IntegerField(initial=0)
    underage_males_for_order_3_form = forms.IntegerField(initial=0)
    underage_females_for_order_3_form = forms.IntegerField(initial=0)

# Orden 4: Cantidad de ingresos
class FormularioResumenGeneralOrden4(forms.Form):
    employer_identification_number_for_order_4_form = forms.IntegerField(initial=0)
    year_for_order_4_form = forms.IntegerField(initial=0)
    male_managers_or_bosses_for_order_4_form = forms.IntegerField(initial=0)
    female_managers_or_bosses_for_order_4_form = forms.IntegerField(initial=0)
    male_assistants_for_order_4_form = forms.IntegerField(initial=0)
    # empleados_mujeres_orden_4 = forms.IntegerField(initial=0)
    female_assistants_for_order_4_form = forms.IntegerField(initial=0)
    male_laborers_for_order_4_form = forms.IntegerField(initial=0)
    female_laborers_for_order_4_form = forms.IntegerField(initial=0)
    underage_males_for_order_4_form = forms.IntegerField(initial=0)
    underage_females_for_order_4_form = forms.IntegerField(initial=0)

# Orden 5: Cantidad de egresos
class FormularioResumenGeneralOrden5(forms.Form):
    employer_identification_number_for_order_5_form = forms.IntegerField(initial=0)
    year_for_order_5_form = forms.IntegerField(initial=0)
    male_managers_or_bosses_for_order_5_form = forms.IntegerField(initial=0)
    female_managers_or_bosses_for_order_5_form = forms.IntegerField(initial=0)
    male_assistants_for_order_5_form = forms.IntegerField(initial=0)
    # empleados_mujeres_orden_5 = forms.IntegerField(initial=0)
    female_assistants_for_order_5_form = forms.IntegerField(initial=0)
    male_laborers_for_order_5_form = forms.IntegerField(initial=0)
    female_laborers_for_order_5_form = forms.IntegerField(initial=0)
    underage_males_for_order_5_form = forms.IntegerField(initial=0)
    underage_females_for_order_5_form = forms.IntegerField(initial=0)

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
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    # Opciones para el campo que pregunta el estado civil
    ESTADO_CIVIL_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widow(er)'),
    ]

    # numero_patronal_de_planilla_empleados
    employer_identification_number = forms.IntegerField(initial=0)

    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    id_number = forms.CharField(max_length=15)
    date_of_birth = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=SEXO_CHOICES)
    address = forms.CharField(widget=forms.Textarea)

    # cargo
    job_title = forms.CharField(max_length=100)

    profession = forms.CharField(max_length=100)

    nationality = forms.CharField(max_length=20)

    marital_status = forms.ChoiceField(choices=ESTADO_CIVIL_CHOICES)

    date_of_hire = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    # OPCIONAL
    date_in_which_they_left_the_company = forms.DateField(initial='0001-01-01', required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    number_of_underage_children = forms.IntegerField(required=False, initial=0)  # OPCIONAL

    reason_for_leaving_the_company = forms.CharField(required=False, max_length=100)  # OPCIONAL

    work_schedule = forms.CharField(max_length=20)

    school_grade_in_which_the_youngest_child_is_enrolled = forms.CharField(required=False, max_length=20)    # OPCIONAL

    # OPCIONAL
    date_of_birth_of_the_youngest_child = forms.DateField(initial='0001-01-01', required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    # OPCIONAL
    employment_start_date_of_the_youngest_child = forms.DateField(initial='0001-01-01', required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))


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
        ('M', 'Monthly'),
        ('D', 'Daily')
    ]

    # numero_patronal_de_planilla_sueldos
    employer_identification_number_for_the_salary_form = forms.IntegerField(initial=0)

    # forma_de_pago
    pay_frequency = forms.ChoiceField(choices=FORMA_PAGO_CHOICES)

    # cedula_planilla_sueldos
    id_number_for_the_salary_form = forms.CharField(max_length=15)

    # importe_unitario
    salary_per_day = forms.IntegerField(initial=0)

    # Horas trabajadas y salarios percibidos en el año
    # horas_trabajadas_enero
    hours_worked_in_january = forms.IntegerField(initial=0)

    # salario_percibido_enero
    salary_received_in_january = forms.IntegerField(initial=0)

    hours_worked_in_february = forms.IntegerField(initial=0)
    salary_received_in_february = forms.IntegerField(initial=0)

    hours_worked_in_march = forms.IntegerField(initial=0)
    salary_received_in_march = forms.IntegerField(initial=0)

    hours_worked_in_april = forms.IntegerField(initial=0)
    salary_received_in_april = forms.IntegerField(initial=0)

    hours_worked_in_may = forms.IntegerField(initial=0)
    salary_received_in_may = forms.IntegerField(initial=0)

    hours_worked_in_june = forms.IntegerField(initial=0)
    salary_received_in_june = forms.IntegerField(initial=0)

    hours_worked_in_july = forms.IntegerField(initial=0)
    salary_received_in_july = forms.IntegerField(initial=0)

    hours_worked_in_august = forms.IntegerField(initial=0)
    salary_received_in_august = forms.IntegerField(initial=0)

    hours_worked_in_september = forms.IntegerField(initial=0)
    salary_received_in_september = forms.IntegerField(initial=0)

    hours_worked_in_october = forms.IntegerField(initial=0)
    salary_received_in_october = forms.IntegerField(initial=0)

    hours_worked_in_november = forms.IntegerField(initial=0)
    salary_received_in_november = forms.IntegerField(initial=0)

    hours_worked_in_december = forms.IntegerField(initial=0)
    salary_received_in_december = forms.IntegerField(initial=0)  # Fin salarios y horas durante el año

    # horas_extras_100_por_ciento_durante_anno
    one_hundred_percent_of_extra_hours_worked_during_the_year = forms.IntegerField(initial=0)

    # salario_percibido_horas_extras_100_por_ciento_anno
    one_hundred_percent_of_salary_received_from_working_extra_hours = forms.IntegerField(initial=0)

    # aguinaldo
    christmas_bonus = forms.IntegerField(initial=0)

    # beneficios
    severance_pay = forms.IntegerField(initial=0)

    # bonificaciones
    large_family_bonus = forms.IntegerField(initial=0)

    # vacaciones
    accrued_vacations = forms.IntegerField(initial=0)

    # horas_trabajadas_incluyendo_horas_extras
    hours_worked_including_extra_hours = forms.IntegerField(initial=0)

    # Este es el salario total SIN los ingresos extras
    # total_recibido_en_concepto_de_salario_sin_ingresos_extras
    total_amount_received_from_salary_without_supplemental_income = forms.IntegerField(initial=0)


""" Formulario para Generar Planillas del IPS.

Para la Categoria y los Codigos, pondre un Choice/<select>.

•	Categoría (empleador/mensualero u obrero/destajo) (pondré esos 2 con un <select>). 

•	Códigos (1_Entrada, 2_Salida, 3_Vacaciones, 4_Reposo, 5_indemnizacion, y 6_Otras Causas) (los pondré con un 
        <select>).
"""
class FormularioPlanillaIPS(forms.Form):

    # Opciones para el campo del código
    CODIGO_CHOICES = [
        ('1', '1: Entry'),
        ('2', '2: Exit'),
        ('3', '3: Vacation'),
        ('4', '4: Rest'),
        ('5', '5: Compensation'),
        ('6', '6: Other causes')
    ]

    # Opciones para el campo del código
    CATEGORIA_CHOICES = [
        ('Employer/Supervisor', 'Employer/Supervisor'),
        ('Employee/Worker/Assistant', 'Employee/Worker/Assistant'),
    ]

    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    id_number = forms.CharField(max_length=15)

    # numero_de_asegurado
    social_security_number = forms.CharField(max_length=30)

    # numero_de_orden
    order_number = forms.IntegerField(initial=0)

    # dias_trabajados_mes_anterior
    number_of_days_worked_on_the_previous_month = forms.IntegerField(initial=0)

    # dias_trabajados_mes_actual
    days_worked_on_the_current_month = forms.IntegerField(initial=0)

    # salario_imponible
    taxable_income = forms.DecimalField(max_digits=14, decimal_places=2, initial=0)

    code = forms.ChoiceField(choices=CODIGO_CHOICES)

    # categoria
    category = forms.ChoiceField(choices=CATEGORIA_CHOICES)

    # reconocimiento_servicios_anteriores
    acknowledgement_of_services_done_prior_to_1974 = forms.CharField(widget=forms.Textarea)        # RSA (OPCIONAL)

    # firma_del_encargado_que_creo_la_planilla
    signature_of_the_manager_that_created_the_social_security_form = forms.ImageField()
