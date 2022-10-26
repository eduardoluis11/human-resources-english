from django.shortcuts import render

""" I will have to use the HTTP Response Redirect feature, so it will be included right now (source: 
https://docs.djangoproject.com/en/4.1/topics/http/urls/ .)
"""
from django.http import HttpResponseRedirect

# I learned how to use "authenticate" a "IntegrityError" from here:
# https://cdn.cs50.net/web/2020/spring/projects/4/network.zip

# This lets me sign in and sign out.
from django.contrib.auth import authenticate, login, logout

# This allows me to go back to the home page more quickly.
from django.urls import reverse

# This detects if there are two users with the same username.
from django.db import IntegrityError

# This allows me to use the decorator that asks the user to log in to see a view.
from django.contrib.auth.decorators import login_required

# This will let me get the current date and time.
import datetime

# This allows me to show flash messages and redirect the user to another page (source: https://youtu.be/8kBo91L8JTY )
from django.contrib import messages
from django.shortcuts import redirect

# This will allow me to use the Django forms from forms.py
from .formularios import FormularioRegistrarSancion, FormularioRegistrarBonificacion, FormularioRegistrarPermiso, \
    FormularioPerfilDeCargo, FormularioJustificacion, FormularioDescuentos, FormularioIngresosExtras, \
    FormularioVacaciones, FormularioCurriculum, FormularioAguinaldos, FormularioFechas, FormularioAsistencias, \
    FormularioLiquidacionDelPersonal, FormularioLiquidacionDeSalario, FormularioDatosPersonalesLegajo, \
    FormularioInformacionJuridicaLegajo, FormularioAdministracionEmpresaLegajo, FormularioOtrosDatosLegajo, \
    FormularioDatosPersonalesContrato, FormularioDatosDelContrato, FormularioInformeWeb, \
    FormularioEmpleadosMinisterioDeTrabajo, FormularioSueldosMinisterioDeTrabajo, FormularioResumenGeneralOrden1, \
    FormularioResumenGeneralOrden2, FormularioResumenGeneralOrden3, FormularioResumenGeneralOrden4, \
    FormularioResumenGeneralOrden5, FormularioPlanillaIPS


# This imports the models (source: https://docs.djangoproject.com/en/4.1/topics/db/models/ )
from .models import User, Sancion, BonificacionFamiliar, Permiso, PerfilDeCargo, JustificacionDePermiso, Descuentos, \
    IngresoExtra, Vacacion, Curriculum, Aguinaldo, FechaAsistencia, Asistencia, LiquidacionDelPersonal, \
    LiquidacionDeSalario, Legajo, Contrato, InformeWeb, PlanillaEmpleadosMinisterioDeTrabajo, \
    PlanillaResumenGeneralMinisterioDeTrabajo, PlanillaSueldosMinisterioDeTrabajo, PlanillaIPS


# Create your views here.

""" Home page
"""
def index(request):
    return render(request, 'index.html')

""" Function for letting a user to create an account.

This function will allow me to both enter into the register.html page, as well as create a user account for a user (I 
will have to use "else"). 

I need to grab the data from the 4 fields on the form POST of register.html. 

The request.method will detect whether I did a POST request (source: 
https://docs.djangoproject.com/en/4.1/ref/request-response/ ). 

If the user writes 2 different passwords in "password"  and in "confirm password," I will show an error message. 

If the user fills in the 4 fields correctly and clicks 
"Register," I will check to see if the user's name is not already registered. If it is, I will show an error message. 
To do this, I will use a "try" and "except." If someone else is using that user name, I will execute an error in the 
snippet that has the line "except" (source: https://www.w3schools.com/python/python_try_except.asp .) 

The rest of the code (the create_user, the IntegrityError, and the login) were taken from 
https://cdn.cs50.net/web/2020/spring/projects/4/network.zip , which comes from this link: 
https://cs50.harvard.edu/web/2020/projects/4/network/
"""
def registrar(request):

    # This detects if the user clicked on "Register" (if they submitted the Sign Up form)
    if request.method == "POST":

        # This gets the information typed into each of the four input fields on the form.
        nombre_usuario = request.POST["nombre_usuario"]
        email = request.POST["email"]
        contrasena = request.POST["contrasena"]
        confirmar_contrasena = request.POST["confirmar_contrasena"]

        # This checks that the two passwords written in the form are the same.
        if contrasena != confirmar_contrasena:
            return render(request, "registrar.html", {
                "mensaje": "Las dos contraseñas deben ser iguales."
            })

        # This will create a user, or print an error message if the user uses a username that is repeated
        try:
            usuario = User.objects.create_user(nombre_usuario, email, contrasena)
            usuario.save()
        except IntegrityError:
            return render(request, "registrar.html", {
                "mensaje": "Error: Este nombre de usuario está siendo usado por otra persona."
            })
        login(request, usuario)
        return HttpResponseRedirect(reverse("index"))

    # This will render the page register.html (the page for signing up)
    else:
        return render(request, 'registrar.html')

""" Log In view

This view will be somewhat similar to registering. There is an if statement with two conditions: if the user has not 
sent a POST request, they will be shown the login page; while if they send a POST request, the user will be logged in, 
and redirected to the home page.

The "authenticate" function reads the username and password, and checks to see if it is in the database (source: 
https://docs.djangoproject.com/en/dev/topics/auth/default/ .)

The "login" function will allow the user to login.

The "is not None" check will see if there is a record with that username and password for that user.
"""
def iniciar_sesion(request):

    # If the user clicks the "Log In" submit button, this will be activated.
    if request.method == "POST":
        nombre_usuario = request.POST["nombre_usuario"]
        contrasena = request.POST["contrasena"]

        # Search the database for this user if they exist.
        usuario = authenticate(request, username=nombre_usuario, password=contrasena)

        # If the user exists, this user can log in
        if usuario is not None:
            login(request, usuario)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "iniciar-sesion.html", {
                "mensaje": "Nombre de usuario y/o contraseña incorrectos."
            })

    # This opens the log in page if the user enters the URL of this page.
    else:
        return render(request, 'iniciar-sesion.html')

""" View for closing the user's session.

The "logout()" function will close the session (source: https://docs.djangoproject.com/en/dev/topics/auth/default/ ).
"""
def cerrar_sesion(request):
    logout(request)

    # This redirects the user to the home page.
    return HttpResponseRedirect(reverse("index"))

""" View for displaying the list of sanctions for all employees.

I am going to put the “login required” decorator on all 18 functions so that only registered users can see the web app's
content and data for all employees.

To render all the sanctions, I will use: “Tabla.objects.all()”.
"""
@login_required
# lista_sanciones
def sanctions_list(request):

    return render(request, "sancion/lista-sanciones.html", {
        "sanciones": Sancion.objects.all()
    })

""" View for registering sanctions.

I have to modify the view so that it enters the form data into the database.

If I want to show a flash message to the user and redirect them to another page at the same time, I must use "messages"
and "redirect". In the "redirect", I have to put the URL of the page to which I want to redirect the user, NOT
the name of the HTML file.

"""
@login_required
# registrar_sancion
def register_sanction(request):

    # Esto me llama el formulario de Django para registrar sanciones
    # This calls the Django form for registering sanctions
    formulario = FormularioRegistrarSancion()

    if request.method == "POST":
        nombre = request.POST["name"]
        apellidos = request.POST["last_name"]
        cedula = request.POST["id_number"]
        motivo_de_sancion = request.POST["reason_for_the_sanction"]
        sancion_a_aplicar = request.POST["sanction_that_will_be_applied"]
        fecha_del_incidente = request.POST["date_of_the_incident"]

        # This gets the current date and time.
        timestamp = datetime.datetime.now()

        # This will prepare the data before inserting it into the database.
        nueva_sancion = Sancion(nombre=nombre, apellidos=apellidos, cedula=cedula, motivo_de_sancion=motivo_de_sancion,
                                sancion_a_aplicar=sancion_a_aplicar, fecha_del_incidente=fecha_del_incidente,
                                timestamp=timestamp)

        # This inserts the fields into the database.
        nueva_sancion.save()

        # Flash confirmation message
        messages.success(request, "A new sanction has been successfully registered.")

        # This redirects the user to the list of sanctions.
        return redirect('sanctions_list')

    # This renders the page for registering sanctions.
    else:
        return render(request, "sancion/registrar-sancion.html", {
            "formulario": formulario,
        })

""" View for deleting sanctions.

I need the ID of the sanction to delete that sanction specifically, and not delete the other sanctions by accident. 
Therefore, I need to use a second argument, which will take the ID of the sanction.
"""
@login_required
# borrar_sancion
def delete_sanction(request, id_sancion):

    # Esto agarra la sanción que quiero borrar
    sancion_actual = Sancion.objects.filter(id=id_sancion)

    # Si el usuario hace clic en "Borrar", se borrará la sanción
    if request.method == "POST":
        sancion_actual.delete()   # Esto borra la sanción de la base de datos

        # Mensaje flash de confirmación
        messages.success(request, "The selected sanction has been deleted.")

        # messages.success(request, "Se ha borrado la sanción seleccionada.")

        # Esto redirige al usuario a la lista de sanciones
        return redirect('sanctions_list')

    # Esto renderiza la página que te pregunta si quieres borrar la sanción
    else:
        return render(request, "sancion/borrar-sancion.html", {
            "sancion_actual": sancion_actual
        })

""" View that displays all the details of a sanction.

To enter to this page, I will make the user click on "Detailed View".

One of the things I have to do is like in "delete sanction": I have to put the number of the sanction in the URL and
in the second argument of the view to see the sanction in detail. After that, I will to show all the data
of that sanction.
"""
@login_required
# ver_sancion
def view_sanction(request, id_sancion):

    # Esto agarra la sanción que quiero borrar
    sancion_actual = Sancion.objects.filter(id=id_sancion)

    # Esto renderiza la página y todos los datos de la sancion
    return render(request, "sancion/ver-sancion.html", {
        "sancion_actual": sancion_actual
    })

""" View that displays the list of Large Family Bonuses for each month for all employees. 
"""
@login_required
# lista_bonificaciones_familiares
def lista_bonificaciones_familiares(request):

    return render(request, "bonificacion-familiar/lista-bonificaciones-familiares.html", {
        "bonificaciones_familiares": BonificacionFamiliar.objects.all()
    })

""" Vista para registrar una bonificación familiar.

Haré el cálculo del número total de hijos que cualifican para la bonificacion familiar, y el calculo de la 
bonificacion familiar directamente desde aquí, y lo meteré a la base de datos.

Cuando uso "reverse redirect", debo poner el nombre del view, NO de la URL.
"""
@login_required
def registrar_bonificacion_familiar(request):

    # Esto me llama el formulario de Django para registrar sanciones
    formulario = FormularioRegistrarBonificacion()

    # Si el usuario envía el formulario
    if request.method == "POST":
        nombre = request.POST["name"]
        apellidos = request.POST["last_name"]
        cedula = request.POST["id_number"]

        fecha_a_pagar = request.POST["date_to_make_the_payment"]
        hijos_menores = request.POST["number_of_underage_children"]
        hijos_mayores_discapacitados = request.POST["number_of_adult_children_with_disabilities"]
        salario_minimo_mensual_vigente = request.POST["current_monthly_minimum_wage"]

        # Esto me agarra la fecha y la hora actual
        timestamp = datetime.datetime.now()

        # El numero total de hijos y la bonificacion familiar las debo calcular

        # Esto suma la cantidad de hios menores y mayores
        total_hijos_para_bonificacion = int(hijos_menores) + int(hijos_mayores_discapacitados)

        # Para debuggear
        # print(total_hijos_para_bonificacion)

        # Esto calcula la bonificacion familiar (5% salario minimo multiplicado por el numero de hijos)
        bonificacion_familiar = total_hijos_para_bonificacion * (5 / 100) * float(salario_minimo_mensual_vigente)

        # Para debuggear
        # print(bonificacion_familiar)


        # Esto prepara los datos antes de meterlos a la base de datos
        nueva_bonificacion = BonificacionFamiliar(nombre=nombre, apellidos=apellidos, cedula=cedula,
                                fecha_a_pagar=fecha_a_pagar, hijos_menores=hijos_menores,
                                hijos_mayores_discapacitados=hijos_mayores_discapacitados,
                                salario_minimo_mensual_vigente=salario_minimo_mensual_vigente,
                                total_hijos_para_bonificacion=total_hijos_para_bonificacion,
                                bonificacion_familiar=bonificacion_familiar, timestamp=timestamp)

        # Esto inserta los campos en la base de datos
        nueva_bonificacion.save()

        # Mensaje flash de confirmación
        # messages.success(request, "Se ha registrado una nueva bonificación familiar correctamente.")
        messages.success(request, "A new large family bonus report has been successfully registered.")

        # Esto redirige al usuario a la lista de bonificaciones
        return redirect('lista_bonificaciones_familiares')

    # Esto renderiza la pagina para registrar sanciones
    else:
        return render(request, "bonificacion-familiar/registrar-bonificacion-familiar.html", {
            "formulario": formulario,
        })

""" Vista para ver en detalle la bonificación familiar de un trabajador
"""
@login_required
def ver_bonificacion(request, id_bonificacion):

    # Esto agarra la bonificacion que quiero borrar
    bonificacion_actual = BonificacionFamiliar.objects.filter(id=id_bonificacion)

    # Esto renderiza la página y todos los datos de la sancion
    return render(request, "bonificacion-familiar/ver-bonificacion-familiar.html", {
        "bonificacion_actual": bonificacion_actual
    })

""" Vista para ver todos los permisos de todo el personal.
"""
@login_required
def lista_permisos(request):

    return render(request, "permisos/lista-permisos.html", {
        "permisos": Permiso.objects.all()
    })

""" Vista para registrar permisos.

Recuerda que para las imagenes, debo usar "request.FILE", NO "request.POST".
"""
@login_required
def registrar_permiso(request):

    # Esto me llama el formulario de Django para registrar sanciones
    formulario = FormularioRegistrarPermiso()

    # Si el usuario envía el formulario
    if request.method == "POST":
        nombre = request.POST["name"]
        apellidos = request.POST["last_name"]
        cedula = request.POST["id_number"]

        fecha_inicio_ausencia = request.POST["absence_start_date"]
        fecha_reincorporacion = request.POST["absence_end_date"]
        motivo_ausencia = request.POST["reason_for_the_absence"]
        recibira_descuento = request.POST["will_they_receive_a_discount"]
        descuento = request.POST["discount_that_will_be_applied"]

        # Esto me agarra las fotos de las firmas
        foto_firma_trabajador = request.FILES["signature_of_the_employee_that_will_be_absent"]
        foto_firma_encargado_rrhh = request.FILES["signature_of_the_manager_that_game_them_the_permission_to_leave"]

        # Esto me agarra la fecha y la hora actual
        timestamp = datetime.datetime.now()

        # Para debuggear
        # print(total_hijos_para_bonificacion)

        # Para debuggear
        # print(bonificacion_familiar)

        # Esto prepara los datos antes de meterlos a la base de datos
        nuevo_permiso = Permiso(nombre=nombre, apellidos=apellidos, cedula=cedula,
                                fecha_inicio_ausencia=fecha_inicio_ausencia,
                                fecha_reincorporacion=fecha_reincorporacion, motivo_ausencia=motivo_ausencia,
                                recibira_descuento=recibira_descuento, descuento=descuento,
                                foto_firma_trabajador=foto_firma_trabajador,
                                foto_firma_encargado_rrhh=foto_firma_encargado_rrhh,
                                timestamp=timestamp)

        # Esto inserta los campos en la base de datos
        nuevo_permiso.save()

        # Mensaje flash de confirmación
        # messages.success(request, "Se ha registrado un nuevo permiso correctamente.")
        messages.success(request, "A new permission to leave has been successfully registered.")

        # Esto redirige al usuario a la lista de bonificaciones
        return redirect('lista_permisos')

    # Esto renderiza la pagina para registrar sanciones
    else:
        return render(request, "permisos/registrar-permiso.html", {
            "formulario": formulario
        })

""" Vista para ver permiso de manera detallada
"""
@login_required
def ver_permiso(request, id_permiso):

    # Esto agarra la bonificacion que quiero borrar
    permiso_seleccionado = Permiso.objects.filter(id=id_permiso)

    # Esto renderiza la página y todos los datos de la sancion
    return render(request, "permisos/ver-permiso.html", {
        "permiso_seleccionado": permiso_seleccionado
    })

""" Vista de Perfiles de Cargos.
"""
@login_required
# lista_perfiles_cargos
def job_profile_list(request):

    return render(request, "perfil-de-cargo/lista-perfiles-cargos.html", {
        "perfiles": PerfilDeCargo.objects.all()
    })

""" Vista para registrar un nuevo Perfil de Cargo
"""
@login_required
# registrar_perfil_cargo
def register_job_profile(request):

    # Esto me llama el formulario de Django para registrar perfiles de cargo
    formulario = FormularioPerfilDeCargo()

    # Si el usuario envía el formulario
    if request.method == "POST":
        nombre_del_cargo = request.POST["job_title"]
        experiencia_requerida = request.POST["experience_required"]
        conocimientos_requeridos = request.POST["technical_skills_required"]
        nivel_de_estudios = request.POST["education"]
        rango_salarial = request.POST["salary_range"]
        requiere_tener_auto_propio = request.POST["does_it_require_having_a_car"]
        otros_requisitos = request.POST["other_requirements"]

        # Esto me agarra la fecha y la hora actual
        timestamp = datetime.datetime.now()

        # Esto prepara los datos antes de meterlos a la base de datos
        nuevo_cargo = PerfilDeCargo(nombre_del_cargo=nombre_del_cargo, experiencia_requerida=experiencia_requerida,
                                conocimientos_requeridos=conocimientos_requeridos, nivel_de_estudios=nivel_de_estudios,
                                rango_salarial=rango_salarial, requiere_tener_auto_propio=requiere_tener_auto_propio,
                                otros_requisitos=otros_requisitos, timestamp=timestamp)

        # Esto inserta los campos en la base de datos
        nuevo_cargo.save()

        # Mensaje flash de confirmación
        messages.success(request, "A new job profile has been successfully registered.")

        # Esto redirige al usuario a la lista de perfiles de cargo
        return redirect('job_profile_list')

    # Esto renderiza la pagina para registrar sanciones
    else:
        return render(request, "perfil-de-cargo/registrar-perfil-cargo.html", {
            "formulario": formulario
        })

""" Vista para ver detalladamente un Perfil de Cargo
"""
@login_required
# ver_cargo
def view_job_profile(request, id_cargo):

    # Esto agarra la bonificacion que quiero borrar
    cargo_seleccionado = PerfilDeCargo.objects.filter(id=id_cargo)

    # Esto renderiza la página y todos los datos de la sancion
    return render(request, "perfil-de-cargo/ver-perfil-cargo.html", {
        "cargo_seleccionado": cargo_seleccionado
    })

""" Vista de Lista de Justificaciones de Permisos
"""
@login_required
# lista_justificaciones
def list_of_proofs_of_leaves(request):

    return render(request, "justificacion-de-permiso/lista-justificaciones.html", {
        "justificaciones": JustificacionDePermiso.objects.all()
    })

""" Vista para Registrar una Justificación de Permiso.

Voy a aceptar PDFs o imágenes para los justificantes. Creo que debo usar el campo FileField. Para usarlo, debe ser 
similar al ImageField de los formularios de Django (tengo que usar “request.FILES” en el view, y “enctype” en el 
<form> en HTML).
"""
@login_required
# registrar_justificacion_permiso
def register_proof_of_leave(request):

    # Esto me llama el formulario de Django para registrar perfiles de cargo
    formulario = FormularioJustificacion

    # Si el usuario envía el formulario
    if request.method == "POST":
        nombre = request.POST["name"]
        apellidos = request.POST["last_name"]
        cedula = request.POST["id_number"]

        fecha_inicio_ausencia = request.POST["absence_start_date"]
        fecha_reincorporacion = request.POST["absence_end_date"]

        existe_discrepancia_permiso_y_justificacion = request.POST["is_there_a_discrepancy_between_the_permission_and_the_proof_of_leave"]

        # Necesito usar FILES para agarrar el archivo con la justificación escaneada
        archivo_con_justificacion = request.FILES["file_with_the_scanned_proof_of_leave_of_absence"]

        foto_firma_encargado_rrhh = request.FILES["signature_of_the_manager_that_checked_the_proof"]

        # Esto me agarra la fecha y la hora actual
        timestamp = datetime.datetime.now()

        # Esto prepara los datos antes de meterlos a la base de datos
        nueva_justificacion = JustificacionDePermiso(nombre=nombre,apellidos=apellidos, cedula=cedula,
                                    fecha_inicio_ausencia=fecha_inicio_ausencia,
                                    fecha_reincorporacion=fecha_reincorporacion,
                                    existe_discrepancia_permiso_y_justificacion=existe_discrepancia_permiso_y_justificacion,
                                    archivo_con_justificacion=archivo_con_justificacion,
                                    foto_firma_encargado_rrhh=foto_firma_encargado_rrhh,
                                    timestamp=timestamp)

        # Esto inserta los campos en la base de datos
        nueva_justificacion.save()

        # Mensaje flash de confirmación
        messages.success(request, "A new proof of leave of absence has been successfully registered.")

        # Esto redirige al usuario a la lista de bonificaciones
        return redirect('list_of_proofs_of_leaves')

    # Esto renderiza la pagina para registrar sanciones
    else:
        return render(request, "justificacion-de-permiso/registrar-justificacion.html", {
            "formulario": formulario
        })

""" Vista para Ver de manera detallada una Justificacion de un Permiso
"""
@login_required
# ver_justificacion
def view_proof_of_leave(request, id_justificacion):

    # Esto agarra la justificacion que quiero ver
    justificacion_seleccionada = JustificacionDePermiso.objects.filter(id=id_justificacion)

    # Esto renderiza la página y todos los datos de la justificacion
    return render(request, "justificacion-de-permiso/ver-justificacion.html", {
        "justificacion_seleccionada": justificacion_seleccionada
    })

""" Vista de Lista de Descuentos
"""
@login_required
# lista_descuentos
def discount_list(request):

    return render(request, "descuentos/lista-descuentos.html", {
        "descuentos": Descuentos.objects.all()
    })

""" Vista para registrar Descuentos
"""
@login_required
# registrar_descuentos
def register_discounts(request):

    formulario = FormularioDescuentos()

    # Si el usuario envía el formulario
    if request.method == "POST":
        nombre = request.POST["name"]
        apellidos = request.POST["last_name"]
        cedula = request.POST["id_number"]

        fecha_aplicar_descuento = request.POST["date_to_apply_discount"]

        salario_base = request.POST["base_salary"]
        salario_con_ingresos_extras = request.POST["salary_with_extra_income"]

        descuento_cuota_ips = request.POST["social_security_discount"]
        descuento_sanciones = request.POST["discounts_due_to_sanctions"]
        descuento_inasistencias = request.POST["discounts_due_to_nonattendances"]
        otros_descuentos = request.POST["other_discounts"]
        descuentos_totales = request.POST["sum_of_all_the_discounts_for_this_employee"]

        # Esto me agarra la fecha y la hora actual
        timestamp = datetime.datetime.now()

        # Esto prepara los datos antes de meterlos a la base de datos
        nuevos_descuentos = Descuentos(nombre=nombre, apellidos=apellidos, cedula=cedula,
                                    fecha_aplicar_descuento=fecha_aplicar_descuento, salario_base=salario_base,
                                    salario_con_ingresos_extras=salario_con_ingresos_extras,
                                    descuento_cuota_ips=descuento_cuota_ips, descuento_sanciones=descuento_sanciones,
                                    descuento_inasistencias=descuento_inasistencias, otros_descuentos=otros_descuentos,
                                    descuentos_totales=descuentos_totales,
                                    timestamp=timestamp)

        # Esto inserta los campos en la base de datos
        nuevos_descuentos.save()

        # Mensaje flash de confirmación
        messages.success(request, "A new discount has been successfully registered.")

        # messages.success(request, "Se han registrado nuevos descuentos correctamente.")

        # Esto redirige al usuario a la lista de bonificaciones
        return redirect('discount_list')

    else:
        return render(request, "descuentos/registrar-descuentos.html", {
            "formulario": formulario
        })

""" Vista para ver los Descuentos 
"""
@login_required
# ver_descuentos
def view_discount_statement(request, id_descuento):

    # Esto agarra el descuento que quiero ver
    descuento_seleccionado = Descuentos.objects.filter(id=id_descuento)

    # Esto renderiza la página y todos los datos del descuento
    return render(request, "descuentos/ver-descuentos-trabajador.html", {
        "descuento_seleccionado": descuento_seleccionado
    })

""" Vista de lista de Ingresos extras del personal.
"""
@login_required
# lista_ingresos_extras
def supplemental_income_statements_list(request):

    return render(request, "ingresos-extras/lista-ingresos-extras.html", {
        "ingresos_extras": IngresoExtra.objects.all()
    })

""" Vista para registrar Ingresos Extras
"""
@login_required
# registrar_ingresos_extras
def register_supplemental_income_statement(request):

    formulario = FormularioIngresosExtras()

    # Si el usuario envía el formulario
    if request.method == "POST":
        nombre = request.POST["name"]
        apellidos = request.POST["last_name"]
        cedula = request.POST["id_number"]
        fecha_aplicar_ingresos_extras = request.POST["date_in_which_the_payment_will_be_made"]
        salario_base = request.POST["base_salary"]
        ingresos_por_horas_extras = request.POST["income_from_extra_hours"]
        bonificacion_familiar = request.POST["income_from_large_family_bonus"]
        aguinaldos = request.POST["income_from_christmas_bonus"]
        otros_ingresos_extras = request.POST["other_supplemental_income"]
        ingresos_extras_totales = request.POST["total_supplemental_income"]

        # Esto me agarra la fecha y la hora actual
        timestamp = datetime.datetime.now()

        # Esto prepara los datos antes de meterlos a la base de datos
        nuevos_ingresos_extras = IngresoExtra(nombre=nombre,apellidos=apellidos, cedula=cedula,
                                    fecha_aplicar_ingresos_extras=fecha_aplicar_ingresos_extras,
                                    salario_base=salario_base, ingresos_por_horas_extras=ingresos_por_horas_extras,
                                    bonificacion_familiar=bonificacion_familiar, aguinaldos=aguinaldos,
                                    otros_ingresos_extras=otros_ingresos_extras,
                                    ingresos_extras_totales=ingresos_extras_totales, timestamp=timestamp)

        # Esto inserta los campos en la base de datos
        nuevos_ingresos_extras.save()

        # Mensaje flash de confirmación
        # messages.success(request, "Se han registrado nuevos ingresos extras correctamente.")
        messages.success(request, "A new supplemental income statement has been successfully registered.")

        # Esto redirige al usuario a la lista de bonificaciones
        return redirect('supplemental_income_statements_list')

    else:
        return render(request, "ingresos-extras/registrar-ingresos-extras.html", {
            "formulario": formulario
        })

""" Vista para ver los Ingresos Extras de manera detallada.
"""
@login_required
# ver_ingreso_extra
def view_supplemental_income_statement(request, id_ingreso):

    # Esto agarra el descuento que quiero ver
    ingreso_seleccionado = IngresoExtra.objects.filter(id=id_ingreso)

    # Esto renderiza la página y todos los datos del descuento
    return render(request, "ingresos-extras/ver-ingresos-extras.html", {
        "ingreso_seleccionado": ingreso_seleccionado
    })

""" Vista de lista de Ingresos extras del personal.
"""
@login_required
def lista_vacaciones(request):

    return render(request, "vacaciones/lista-vacaciones.html", {
        "vacaciones": Vacacion.objects.all()
    })

""" Vista para Registrar Vacaciones.

Lo que puedo hacer es crear un campo llamado “días restantes de vacaciones”, el cual se calculará, y el cual el 
usuario NO puede editar. Simplemente se me será directamente en la base de datos. 

Los días de vacaciones que le quedarán al empleado después de tomar sus vacaciones lo calcularé restando el total
de días de vacaciones que tenía inicialmente y el número de días de vacaciones que tomó.
"""
@login_required
def registrar_vacaciones(request):

    # Esto me llama el formulario de Django para registrar perfiles de cargo
    formulario = FormularioVacaciones

    # Si el usuario envía el formulario
    if request.method == "POST":
        nombre = request.POST["name"]
        apellidos = request.POST["last_name"]
        cedula = request.POST["id_number"]

        # Fechas de inicio y fin de vacaciones
        fecha_inicio_vacaciones = request.POST["vacation_start_date"]
        fecha_fin_vacaciones = request.POST["vacation_end_date"]

        # Días de vacaciones
        cantidad_inicial_dias_vacaciones = request.POST["initial_number_of_vacation_days"]
        dias_que_se_tomara_vacaciones = request.POST["number_of_vacation_days_that_they_will_take"]

        # Los días que les quedarán de vacaciones al empleado los calcularé aquí en el back end
        dias_restantes_vacaciones = int(cantidad_inicial_dias_vacaciones) - int(dias_que_se_tomara_vacaciones)

        # Firmas del trabajador y del encargado de RRHH
        foto_firma_trabajador = request.FILES["signature_of_the_employee_that_will_be_on_vacation"]
        foto_firma_encargado_rrhh = request.FILES["signature_of_the_manager_that_authorized_their_vacation"]

        # Esto me agarra la fecha y la hora actual
        timestamp = datetime.datetime.now()

        # Esto prepara los datos antes de meterlos a la base de datos
        nuevas_vacaciones = Vacacion(nombre=nombre, apellidos=apellidos, cedula=cedula,
                                    fecha_inicio_vacaciones=fecha_inicio_vacaciones, 
                                    fecha_fin_vacaciones=fecha_fin_vacaciones, 
                                    cantidad_inicial_dias_vacaciones=cantidad_inicial_dias_vacaciones,
                                    dias_que_se_tomara_vacaciones=dias_que_se_tomara_vacaciones,
                                    dias_restantes_vacaciones=dias_restantes_vacaciones, 
                                    foto_firma_trabajador=foto_firma_trabajador,
                                    foto_firma_encargado_rrhh=foto_firma_encargado_rrhh,
                                    timestamp=timestamp)

        # Esto inserta los campos en la base de datos
        nuevas_vacaciones.save()
    
        # Mensaje flash de confirmación
        # messages.success(request, "Se han registrado unas nuevas vacaciones correctamente.")
        messages.success(request, "A new vacation record has been successfully registered.")
    
        # Esto redirige al usuario a la lista de bonificaciones
        return redirect('lista_vacaciones')

    # Esto renderiza la pagina para registrar vacaciones
    else:
        return render(request, "vacaciones/registrar-vacaciones.html", {
            "formulario": formulario
        })

""" Vista para Ver Vacaciones seleccionadas.
"""
@login_required
def ver_vacacion(request, id_vacacion):

    # Esto agarra el descuento que quiero ver
    vacacion_seleccionada = Vacacion.objects.filter(id=id_vacacion)

    # Esto renderiza la página y todos los datos del descuento
    return render(request, "vacaciones/ver-vacacion.html", {
        "vacacion_seleccionada": vacacion_seleccionada
    })

""" Vista de lista de Currículums.
"""
@login_required
# lista_curriculums
def list_of_resumes(request):

    return render(request, "curriculum/lista-curriculums.html", {
        "curriculums": Curriculum.objects.all()
    })

""" Vista para Registrar un Curriculum.

Recuerda usar "request.FILES" para el campo que agarra el PDF.
"""
@login_required
# registrar_curriculum
def register_a_resume(request):

    formulario = FormularioCurriculum

    # Si el usuario envía el formulario
    if request.method == "POST":

        # Datos personales
        nombre = request.POST["name"]
        apellidos = request.POST["last_name"]
        cedula = request.POST["id_number"]
        sexo = request.POST["sex"]
        fecha_nacimiento = request.POST["date_of_birth"]
        domicilio = request.POST["address"]
        email = request.POST["email"]
        telefono = request.POST["phone"]

        # Nombre del cargo para el candidato
        nombre_del_cargo = request.POST["job_position"]

        # Información laboral
        experiencia_laboral = request.POST["experience"]
        nivel_de_estudios = request.POST["education"]
        otros_datos_interes = request.POST["additional_information"]
        tiene_auto_propio = request.POST["has_their_own_car"]

        # PDF con el currículum
        pdf_con_curriculum = request.FILES["resume_in_pdf"]

        timestamp = datetime.datetime.now()

        # Esto prepara los datos antes de meterlos a la base de datos
        nuevo_curriculum = Curriculum(nombre=nombre, apellidos=apellidos, cedula=cedula, sexo=sexo,
                                    fecha_nacimiento=fecha_nacimiento, domicilio=domicilio, email=email,
                                    telefono=telefono, nombre_del_cargo=nombre_del_cargo,
                                    experiencia_laboral=experiencia_laboral, nivel_de_estudios=nivel_de_estudios,
                                    otros_datos_interes=otros_datos_interes, tiene_auto_propio=tiene_auto_propio,
                                    pdf_con_curriculum=pdf_con_curriculum, timestamp=timestamp)

        # Esto inserta los campos en la base de datos
        nuevo_curriculum.save()

        # Mensaje flash de confirmación
        messages.success(request, "A new resume has been submitted successfully.")

        # Esto redirige al usuario a la lista de bonificaciones
        return redirect('list_of_resumes')

    # Esto renderiza la pagina para registrar el currículum
    else:
        return render(request, "curriculum/registrar-curriculum.html", {
            "formulario": formulario
        })

""" Vista para Ver un Currículum. 
"""
@login_required
# ver_curriculum
def view_resume(request, id_curriculum):

    # Esto agarra el descuento que quiero ver
    curriculum_seleccionado = Curriculum.objects.filter(id=id_curriculum)

    # Esto renderiza la página y todos los datos del descuento
    return render(request, "curriculum/ver-curriculum.html", {
        "curriculum_seleccionado": curriculum_seleccionado
    })

""" Vista para ver Lista de Aguinaldos.
"""
@login_required
# lista_aguinaldos
def list_of_christmas_bonus(request):

    return render(request, "aguinaldos/lista-aguinaldos.html", {
        "aguinaldos": Aguinaldo.objects.all()
    })

""" Vista para calcular y registrar los Aguinaldos en la base de datos.

Puedo hacer el cálculo directamente en el servidor para ahorrarme tiempo. NO mostraré la cantidad de aguinaldos que le 
corresponde al usuario sino hasta que llegue a la lista de aguinaldos, o a la vista detallada de un aguinaldo.

Para calcular el aguinaldo total, tengo que sumar todos los salarios de todos los meses, y debo dividirlo entre 12.

Dado a que voy a generar una planilla, prefiero meter los 12 meses de salario.
"""
@login_required
# registrar_aguinaldos
def register_christmas_bonus(request):

    formulario = FormularioAguinaldos

    # Si el usuario envía el formulario
    if request.method == "POST":
        nombre = request.POST["name"]
        apellidos = request.POST["last_name"]
        cedula = request.POST["id_number"]

        # Año de los aguinaldos
        anno = request.POST["year_of_the_christmas_bonus_payment"]

        # Salario de cada mes
        salario_enero = request.POST["income_from_january"]
        salario_febrero = request.POST["income_from_february"]
        salario_marzo = request.POST["income_from_march"]
        salario_abril = request.POST["income_from_april"]
        salario_mayo = request.POST["income_from_may"]
        salario_junio = request.POST["income_from_june"]
        salario_julio = request.POST["income_from_july"]
        salario_agosto = request.POST["income_from_august"]
        salario_septiembre = request.POST["income_from_september"]
        salario_octubre = request.POST["income_from_october"]
        salario_noviembre = request.POST["income_from_november"]
        salario_diciembre = request.POST["income_from_december"]


        # Cálculo de los aguinaldos basado en el salario (sumar los salarios y dividirlos entre 12)
        suma_salarios = float(salario_enero) + float(salario_febrero) + float(salario_marzo) + float(
            salario_abril) + float(salario_mayo) + float(salario_junio) + float(salario_julio) + float(
            salario_agosto) + float(salario_septiembre) + float(salario_octubre) + float(salario_noviembre) + float(
            salario_diciembre)

        aguinaldos = suma_salarios / 12

        timestamp = datetime.datetime.now()

        # Esto prepara los datos antes de meterlos a la base de datos
        nuevos_aguinaldos = Aguinaldo(nombre=nombre, apellidos=apellidos, cedula=cedula, anno=anno,
                                salario_enero=salario_enero, salario_febrero=salario_febrero,
                                salario_marzo=salario_marzo, salario_abril=salario_abril, salario_mayo=salario_mayo,
                                salario_junio=salario_junio, salario_julio=salario_julio, salario_agosto=salario_agosto,
                                salario_septiembre=salario_septiembre, salario_octubre=salario_octubre,
                                salario_noviembre=salario_noviembre, salario_diciembre=salario_diciembre,
                                aguinaldos=aguinaldos, timestamp=timestamp)

        # Esto inserta los campos en la base de datos
        nuevos_aguinaldos.save()

        # Mensaje flash de confirmación
        # messages.success(request, "Se ha registrado unos nuevos aguinaldos correctamente.")
        messages.success(request, "A new Christmas Bonus report has been successfully registered.")

        # Esto redirige al usuario a la lista de bonificaciones
        return redirect('list_of_christmas_bonus')

    # Esto renderiza la página para registrar el currículum
    else:
        return render(request, "aguinaldos/registrar-aguinaldos.html", {
            "formulario": formulario
        })

""" Vista para ver Planilla de Aguinaldos.
"""
@login_required
# ver_aguinaldo
def view_christmas_bonus(request, id_aguinaldo):

    # Esto agarra el descuento que quiero ver
    aguinaldo_seleccionado = Aguinaldo.objects.filter(id=id_aguinaldo)

    # Esto renderiza la página y todos los datos del descuento
    return render(request, "aguinaldos/ver-aguinaldo.html", {
        "aguinaldo_seleccionado": aguinaldo_seleccionado
    })

""" Esto me dejará Registrar las Fechas para las Asistencias.
"""
@login_required
# registrar_dia_asistencia
def register_attendance_date(request):

    formulario = FormularioFechas

    # Si el usuario envía el formulario
    if request.method == "POST":

        # Fecha de la asistencia
        fecha_asistencias = request.POST["attendance_date"]

        # Esto prepara los datos antes de meterlos a la base de datos
        nueva_fecha = FechaAsistencia(fecha_asistencias=fecha_asistencias)

        # Esto inserta los campos en la base de datos
        nueva_fecha.save()

        # Mensaje flash de confirmación
        messages.success(request, "A new date has been successfully registered.")

        # Esto redirige al usuario a la lista de bonificaciones
        return redirect('attendance_dates_list')

    # Esto renderiza la página para registrar el currículum
    # else:
    return render(request, "asistencias/registrar-dia.html", {
        "formulario": formulario
    })

""" Lista de fechas en las que se tomó asistencia.
"""
@login_required
# lista_dias_asistencia
def attendance_dates_list(request):

    return render(request, "asistencias/lista-dias.html", {
        "fechas": FechaAsistencia.objects.all()
    })

""" View for registering Attendances.

To register attendance on one day, I will have to pass an argument, which will be the id of that date. That is where 
I will be able to register which employees were working that day.

For example, to see the list of employees who went to work on August 19, and since August 19 has the id 
"1", then the list of employees who attended that day will be in the URL "1/list-of-attendances"

And, to register an employee who attended that day, I will put it in "1/register-attendance" (to register 
attendance).

To use a foreign key, I have to use notation like this:
variable = Table_FK.objects.filter (FK_field__field_of_the_original_table = desired_value)

Documentation of "return redirect": https://docs.djangoproject.com/en/4.1/topics/http/shortcuts/

Now that I remember: this that I am doing with the FK only works if I already have at least one record in the 
Attendance table. And I HAVE NO RECORD IN THAT TABLE. The FK would serve me is for the lists and show the attendance 
of that list. To get the date of attendance, I will have to use another method 
(for example, attendance_date = day_id).

I will take with a "get ()" an instance of a date from the Date Attendance table. The date I will take will be the one 
that has as ID the ID that appears in the URL (the 2nd parameter). Then, I will put that instance as the date 
in the Attendances table.

If I call a view to show the list of attendance after registering an employee, I will not be able to register more 
employees. So, I'm just going to redirect the user to the list of days with redirect.
"""
@login_required
# registrar_asistencia
def register_attendance_entry(request, id_dia):

    formulario = FormularioAsistencias

    # Esto me agarra una instancia de "Fecha Asistencia". En este caso, será el del ID que tengo en la URL
    fecha_seleccionada = FechaAsistencia.objects.get(id=id_dia)

    # Si el usuario envía el formulario
    if request.method == "POST":
        nombre = request.POST["name"]
        apellidos = request.POST["last_name"]
        cedula = request.POST["id_number"]

        # Esto agarra si asistió al trabajo (sí/no)
        vino_a_trabajar = request.POST["did_they_come_to_work"]

        # Horas de entrada y de salida del trabajador (pueden estar vacíos)
        hora_llegada = request.POST["arrival_time"]
        hora_salida = request.POST["exit_time"]

        # Mensaje de debugueo
        print(hora_salida)

        # Fecha de la asistencia (tomada como clave foránea).
        # AQUI HABIA UN BUG
        # fecha_asistencia = id_dia

        # Mensaje de debugueo
        # print(fecha_asistencia)

        timestamp = datetime.datetime.now()


        # Esto prepara los datos antes de meterlos a la base de datos
        nueva_asistencia = Asistencia(nombre=nombre, apellidos=apellidos, cedula=cedula,
                                vino_a_trabajar=vino_a_trabajar, hora_llegada=hora_llegada, hora_salida=hora_salida,
                                fecha_asistencia=fecha_seleccionada, timestamp=timestamp)

        # Esto inserta los campos en la base de datos
        nueva_asistencia.save()

        # Mensaje flash de confirmación
        # messages.success(request, "Se ha registrado una nueva asistencia correctamente.")
        messages.success(request, "A new attendance entry has been successfully registered.")

        # Mensaje de debuggeo. ESTO SE EJECUTA
        print("Se almacenó correctamente el mensaje de confirmación de asistencias.")

        # Esto redirige al usuario a la lista asistencias de ese día
        return redirect('attendance_dates_list')

        # HAY UN BUG AQUI.

        # return lista_asistencias(request, id_dia)

        # Esto me lleva a '/1/<str:id_dia>/lista-asistencias'
        # return redirect('<str:id_dia>/lista-asistencias', id_dia=id_dia)

        # Esto me lleva a '/1/1/lista-asistencias'. BUG
        # url_lista_asistencias = id_dia + '/lista-asistencias'
        #
        # return redirect(url_lista_asistencias)

        # return redirect('lista-asistencias', id_dia=id_dia)

    # Esto renderiza la página para registrar el currículum
    else:
        return render(request, "asistencias/registrar-asistencia.html", {
            "formulario": formulario
        })

""" Vista con la lista de Asistencias para ese día.

Como quiero solo las asistencias registradas para un día en específico, no puedo mostrar toooodas las asistencias
guardadas en la base de datos. Entonces, tendré que poner un filtro que me muestre las asistencias que sean solo 
de un día en específico (que en mi caso, es del segundo parámetro que pasaré en esta vista.)
"""
@login_required
# lista_asistencias
def attendance_list(request, id_dia):
    return render(request, "asistencias/lista-asistencias-por-dia.html", {
        "asistencias_del_dia": Asistencia.objects.filter(fecha_asistencia__id=id_dia),
        "dia": id_dia
    })

""" Vista para Registrar la Liquidacion del Personal.

Recuerda usar "request.FILES" para la firma del encargado.
"""
@login_required
# registrar_liquidacion_personal
def register_final_pay(request):

    formulario = FormularioLiquidacionDelPersonal

    # Si el usuario envía el formulario
    if request.method == "POST":
        nombre = request.POST["name"]
        apellidos = request.POST["last_name"]
        cedula = request.POST["id_number"]
        nombre_del_cargo = request.POST["job_position_of_the_employee"]
        fecha_inicio_contrato = request.POST["start_date_of_the_contract"]
        fecha_fin_contrato = request.POST["end_date_of_the_contract"]
        motivo_de_finalizacion_contrato = request.POST["reason_for_leaving_the_company"]

        tipo_de_salario = request.POST["salary_type"]

        # Salarios a usar y sumar para calcular la liquidación
        salario_mensual = request.POST["monthly_salary"]
        vacaciones_no_disfrutadas = request.POST["income_from_unused_vacation_days"]
        aguinaldos = request.POST["accrued_christmas_bonus"]
        salario_por_horas_extras = request.POST["income_from_working_extra_hours"]
        otros_ingresos = request.POST["other_supplemental_income"]

        # Descuentos (debo restarlo a los ingresos)
        descuentos_en_total = request.POST["total_amount_to_discount"]

        # Foto del encargado que calculó el total a liquidar
        foto_firma_encargado_rrhh = request.FILES["signature_of_the_manager_that_authorized_the_final_pay"]

        timestamp = datetime.datetime.now()

        # Total a liquidar. Sumare los ingresos, y a todo eso lo restaré los descuentos.
        salario_total_a_liquidar = float(salario_mensual) + float(vacaciones_no_disfrutadas) + float(
            aguinaldos) + float(salario_por_horas_extras) + float(otros_ingresos) - float(descuentos_en_total)

        # MENSAJE DE DEBUGGEO
        print(salario_total_a_liquidar)

        # Metere el calculo de la liquidacion en el campo con el salario a liquidar
        nueva_liquidacion = LiquidacionDelPersonal(nombre=nombre, apellidos=apellidos, cedula=cedula,
                                nombre_del_cargo=nombre_del_cargo, fecha_inicio_contrato=fecha_inicio_contrato,
                                fecha_fin_contrato=fecha_fin_contrato,
                                motivo_de_finalizacion_contrato=motivo_de_finalizacion_contrato,
                                tipo_de_salario=tipo_de_salario, salario_mensual=salario_mensual,
                                vacaciones_no_disfrutadas=vacaciones_no_disfrutadas, aguinaldos=aguinaldos,
                                salario_por_horas_extras=salario_por_horas_extras, otros_ingresos=otros_ingresos,
                                descuentos_en_total=descuentos_en_total,
                                salario_total_a_liquidar=salario_total_a_liquidar,
                                foto_firma_encargado_rrhh=foto_firma_encargado_rrhh, timestamp=timestamp)

        # Esto inserta los campos en la base de datos
        nueva_liquidacion.save()

        # Mensaje flash de confirmación
        # messages.success(request, "Se ha registrado una nueva liquidación de personal correctamente.")
        messages.success(request, "A new Final Pay report has been successfully registered.")

        # Esto redirige al usuario a la lista asistencias de ese día
        return redirect('final_pay_forms_list')

    # Esto renderiza la página para registrar la liquidacion del personal
    else:
        return render(request, "liquidacion-personal/registrar-liquidacion-personal.html", {
            "formulario": formulario
        })

""" Vista para ver Lista de Planillas de Liquidación del Personal.
"""
@login_required
# lista_liquidacion_personal
def final_pay_forms_list(request):

    return render(request, "liquidacion-personal/lista-liquidaciones-personales.html", {
        "liquidacion_de_todo_el_personal": LiquidacionDelPersonal.objects.all()
    })

""" Vista para ver una planilla de Liquidacion de Personal en detalle.
"""
@login_required
# ver_liquidacion_personal
def view_final_pay_form(request, id_liquidacion):

    # Esto agarra el descuento que quiero ver
    liquidacion_seleccionada = LiquidacionDelPersonal.objects.filter(id=id_liquidacion)

    return render(request, "liquidacion-personal/ver-liquidacion-personal.html", {
        "liquidacion_seleccionada": liquidacion_seleccionada
    })

""" Vista para registrar la Liquidación de Salarios.
"""
@login_required
def registrar_liquidacion_salario(request):

    formulario = FormularioLiquidacionDeSalario

    # Si el usuario envía el formulario
    if request.method == "POST":
        nombre = request.POST["name"]
        apellidos = request.POST["last_name"]
        cedula = request.POST["id_number"]

        # Fecha de pago
        fecha_de_pago = request.POST["payment_date"]

        # Salarios a usar y sumar para calcular la liquidación
        salario_mensual = request.POST["monthly_wage"]
        ingresos_extras = request.POST["supplemental_income"]

        # Descuentos (debo restarlo a los ingresos)
        descuentos = request.POST["discounts"]

        # Foto del encargado que calculó el total a liquidar
        foto_firma_encargado_rrhh = request.FILES["signature_of_the_manager_that_created_the_payroll_report"]

        timestamp = datetime.datetime.now()

        # Total a liquidar. Se calcula restándole los descuentos a todos los ingresos
        salario_total_a_liquidar = float(salario_mensual) + float(ingresos_extras) - float(descuentos)

        # MENSAJE DE DEBUGGEO
        print(salario_total_a_liquidar)

        # Metere el calculo de la liquidacion en el campo con el salario a liquidar
        nueva_liquidacion = LiquidacionDeSalario(nombre=nombre, apellidos=apellidos, cedula=cedula,
                                fecha_de_pago=fecha_de_pago, salario_mensual=salario_mensual,
                                ingresos_extras=ingresos_extras, descuentos=descuentos,
                                salario_total_a_liquidar=salario_total_a_liquidar,
                                foto_firma_encargado_rrhh=foto_firma_encargado_rrhh, timestamp=timestamp)

        # Esto inserta los campos en la base de datos
        nueva_liquidacion.save()

        # Mensaje flash de confirmación
        # messages.success(request, "Se ha registrado una nueva liquidación de salario correctamente.")
        messages.success(request, "A new payroll statement has been successfully registered.")

        # Esto redirige al usuario a la lista asistencias de ese día
        return redirect('lista_liquidacion_salarios')

    # Esto renderiza la página para registrar la liquidacion del salario
    else:
        return render(request, "liquidacion-salarios/registrar-liquidacion-salario.html", {
            "formulario": formulario
        })

""" Vista para ver Lista de Planillas de Liquidación del Salarios.
"""
@login_required
def lista_liquidacion_salarios(request):

    return render(request, "liquidacion-salarios/lista-liquidacion-salarios.html", {
        "liquidacion_de_salarios": LiquidacionDeSalario.objects.all()
    })

""" Vista para ver Lista de Planillas de Liquidación de Salarios.
"""
@login_required
def ver_liquidacion_salario(request, id_liquidacion):

    # Esto agarra el descuento que quiero ver
    liquidacion_seleccionada = LiquidacionDeSalario.objects.filter(id=id_liquidacion)

    return render(request, "liquidacion-salarios/ver-liquidacion-salario.html", {
        "liquidacion_seleccionada": liquidacion_seleccionada
    })

""" Vista para Registrar un Legajo.
"""
@login_required
def registrar_legajo(request):

    formulario_datos_personales = FormularioDatosPersonalesLegajo
    formulario_informacion_juridica = FormularioInformacionJuridicaLegajo
    formulario_empresa = FormularioAdministracionEmpresaLegajo
    formulario_otros_datos = FormularioOtrosDatosLegajo

    # Si el usuario envía el formulario
    if request.method == "POST":

        # Datos Personales
        nombre = request.POST["name"]
        apellidos = request.POST["last_name"]
        cedula = request.POST["id_number"]
        sexo = request.POST["gender"]
        fecha_nacimiento = request.POST["date_of_birth"]
        domicilio = request.POST["address"]
        email = request.POST["email"]
        telefono = request.POST["phone"]
        nacionalidad = request.POST["nationality"]
        fecha_de_vencimiento_cedula = request.POST["expiry_date_of_the_id"]
        curriculum = request.FILES["resume"]
        nivel_maximo_de_educacion_obtenido = request.POST["degree_or_maximum_level_of_education_achieved"]

        # Información Jurídica
        tiene_antecedentes_penales = request.POST["do_they_have_a_criminal_record"]
        numero_ips = request.POST["social_security_number"]

        # Datos de la administración interna de la empresa
        cargo = request.POST["job_title"]
        evaluacion_de_desempeno = request.FILES["performance_appraisal_report"]
        sanciones = request.POST["sanctions"]
        permisos_para_ausentarse = request.POST["leaves_of_absence_taken"]

        # Otros datos de interés de la empresa
        otros_datos = request.POST["other_data"]

        timestamp = datetime.datetime.now()

        # Preparando los datos para meterlos en la base de datos
        nuevo_legajo = Legajo(nombre=nombre, apellidos=apellidos, cedula=cedula, sexo=sexo,
                                fecha_nacimiento=fecha_nacimiento, domicilio=domicilio, email=email, telefono=telefono,
                                nacionalidad=nacionalidad, fecha_de_vencimiento_cedula=fecha_de_vencimiento_cedula,
                                curriculum=curriculum,
                                nivel_maximo_de_educacion_obtenido=nivel_maximo_de_educacion_obtenido,
                                tiene_antecedentes_penales=tiene_antecedentes_penales, numero_ips=numero_ips,
                                cargo=cargo, evaluacion_de_desempeno=evaluacion_de_desempeno, sanciones=sanciones,
                                permisos_para_ausentarse=permisos_para_ausentarse, otros_datos=otros_datos,
                                timestamp=timestamp)

        # Esto inserta los campos en la base de datos
        nuevo_legajo.save()

        # Mensaje flash de confirmación
        # messages.success(request, "Se ha registrado un nuevo legajo correctamente.")
        messages.success(request, "A new dossier has been successfully registered.")

        # Esto redirige al usuario a la lista de legajos
        return redirect('lista_legajos')

    # Esto renderiza la página para registrar los legajos
    else:
        return render(request, "legajo/registrar-legajo.html", {
            "formulario_datos_personales": formulario_datos_personales,
            "formulario_informacion_juridica": formulario_informacion_juridica,
            "formulario_empresa": formulario_empresa,
            "formulario_otros_datos": formulario_otros_datos
        })

""" Vista para ver Lista de Legajos.
"""
@login_required
def lista_legajos(request):

    return render(request, "legajo/lista-legajos.html", {
        "legajos": Legajo.objects.all()
    })

""" Vista para Ver un Legajo en Detalle.
"""
@login_required
def ver_legajo(request, id_legajo):

    # Esto agarra el descuento que quiero ver
    legajo_seleccionado = Legajo.objects.filter(id=id_legajo)

    return render(request, "legajo/ver-legajo.html", {
        "legajo_seleccionado": legajo_seleccionado
    })

""" Vista para Registrar un Contrato.

Son 17 campos.
"""
@login_required
# registrar_contrato
def register_contract(request):

    formulario_datos_personales = FormularioDatosPersonalesContrato
    formulario_datos_contrato = FormularioDatosDelContrato

    # Si el usuario envía el formulario
    if request.method == "POST":
    
        # Datos Personales
        nombre = request.POST["name"]
        apellidos = request.POST["last_name"]
        cedula = request.POST["id_number"]
        sexo = request.POST["sex"]
        fecha_nacimiento = request.POST["date_of_birth"]
        domicilio = request.POST["address"]
        email = request.POST["email"]
        telefono = request.POST["phone"]
        nivel_maximo_de_educacion_obtenido = request.POST["degree_or_maximum_level_of_education_achieved"]
        numero_ips = request.POST["social_security_number"]
        numero_cuenta_bancaria = request.POST["bank_account_number"]

        # Datos del Contrato
        cargo = request.POST["job_title"]
        tiempo_completo_o_parcial = request.POST["job_type"]
        clausulas_del_contrato = request.FILES["contract_clauses"]
        firma_trabajador = request.FILES["signature_of_the_recruit"]
        firma_encargado_rrhh = request.FILES["signature_of_the_manager_who_created_the_contract"]

        timestamp = datetime.datetime.now()
    
        # Preparando los datos para meterlos en la base de datos
        nuevo_contrato = Contrato(nombre=nombre, apellidos=apellidos, cedula=cedula, sexo=sexo,
                                fecha_nacimiento=fecha_nacimiento, domicilio=domicilio, email=email, telefono=telefono,
                                nivel_maximo_de_educacion_obtenido=nivel_maximo_de_educacion_obtenido,
                                numero_ips=numero_ips, numero_cuenta_bancaria=numero_cuenta_bancaria,
                                cargo=cargo, tiempo_completo_o_parcial=tiempo_completo_o_parcial,
                                clausulas_del_contrato=clausulas_del_contrato, firma_trabajador=firma_trabajador,
                                firma_encargado_rrhh=firma_encargado_rrhh, timestamp=timestamp)

    
        # Esto inserta los campos en la base de datos
        nuevo_contrato.save()
        
    
        # Mensaje flash de confirmación
        # messages.success(request, "Se ha registrado un nuevo contrato correctamente.")
        messages.success(request, "A new contract has been successfully registered.")
    
        # Esto redirige al usuario a la lista de contratos
        return redirect('contract_list')

    # Esto renderiza la página para registrar los contratos
    else:
        return render(request, "contrato/registrar-contrato.html", {
            "formulario_datos_personales": formulario_datos_personales,
            "formulario_datos_contrato": formulario_datos_contrato
        })

""" Vista para ver Lista de Contratos.
"""
@login_required
# lista_contratos
def contract_list(request):

    return render(request, "contrato/lista-contratos.html", {
        "contratos": Contrato.objects.all()
    })

""" Vista para Ver un Contrato en Detalle
"""
@login_required
# ver_contrato
def view_contract(request, id_contrato):

    # Esto agarra el descuento que quiero ver
    contrato_seleccionado = Contrato.objects.filter(id=id_contrato)

    return render(request, "contrato/ver-contrato.html", {
        "contrato_seleccionado": contrato_seleccionado
    })

""" Vista para Registrar un Informe Web.

La evaluacion de desempeño debe ir dentro de un "request.FILES".
"""
@login_required
def registrar_informe_web(request):

    formulario = FormularioInformeWeb

    # Si el usuario envía el formulario
    if request.method == "POST":
        anno = request.POST["year_of_the_report"]

        # Archivo PDF con el desempeño anual de todo el personal
        evaluacion_de_desempeno_personal = request.FILES["annual_performance_appraisal_report_of_the_entire_staff"]

        trabajadores_contratados = request.POST["number_of_employees_hired"]
        trabajadores_que_salieron = request.POST["number_of_employees_that_left_the_company"]
        tasa_absentismo = request.POST["absence_rate"]
        salario_promedio_personal = request.POST["average_monthly_salary_of_the_entire_staff"]
        promedio_dias_para_ocupar_cargo_vacante = request.POST["average_number_of_days_to_hire_a_recruit_for_a_vacant_position"]
        annos_de_trabajador_con_mas_tiempo_en_empresa = request.POST["number_of_years_of_the_longest_job_tenure_in_the_company"]
        numero_cursos_ofrecidos_trabajadores = request.POST["number_of_courses_offered_to_the_staff"]
        
        edad_promedio_personal = request.POST["average_age_of_the_entire_staff"]
        
        timestamp = datetime.datetime.now()
    
        # Preparando los datos para meterlos en la base de datos
        nuevo_informe = InformeWeb(anno=anno, evaluacion_de_desempeno_personal=evaluacion_de_desempeno_personal, 
                            trabajadores_contratados=trabajadores_contratados, 
                            trabajadores_que_salieron=trabajadores_que_salieron, tasa_absentismo=tasa_absentismo, 
                            salario_promedio_personal=salario_promedio_personal, 
                            promedio_dias_para_ocupar_cargo_vacante=promedio_dias_para_ocupar_cargo_vacante, 
                            annos_de_trabajador_con_mas_tiempo_en_empresa=annos_de_trabajador_con_mas_tiempo_en_empresa, 
                            numero_cursos_ofrecidos_trabajadores=numero_cursos_ofrecidos_trabajadores, 
                            edad_promedio_personal=edad_promedio_personal, timestamp=timestamp)

        # Esto inserta los campos en la base de datos
        nuevo_informe.save()
        
    
        # Mensaje flash de confirmación
        # messages.success(request, "Se ha registrado un nuevo informe web correctamente.")
        messages.success(request, "A new web report has been successfully registered.")
    
        # Esto redirige al usuario a la lista de contratos
        return redirect('lista_informes')

    # Esto renderiza la página para registrar los contratos
    else:
        return render(request, "informe-web/registrar-informe.html", {
            "formulario": formulario,
        })

""" Vista de Lista de Informes
"""
@login_required
def lista_informes(request):

    return render(request, "informe-web/lista-informes.html", {
        "informes": InformeWeb.objects.all()
    })

""" Vista para Ver un Informe Web en Detalle.
"""
@login_required
def ver_informe(request, id_informe):

    # Esto agarra el descuento que quiero ver
    informe_seleccionado = InformeWeb.objects.filter(id=id_informe)

    return render(request, "informe-web/ver-informe-anual.html", {
        "informe_seleccionado": informe_seleccionado
    })

""" Vista de Lista de Planillas del Ministerio de Trabajo.

Puedo crear una sola lista, y pondré en la tabla 3 casillas: “Ver planilla empleados”, “Ver planilla resumen”, y 
“Ver planilla sueldos”. Cada una de esas casillas tendría un enlace a una página distinta (a la vista detallada de 
cada una de esas planillas en formato para imprimir.) 

El primer campo de la planilla será “fecha”. 
"""
@login_required
# lista_ministerio_trabajo
def department_labor_form_list(request):

    return render(request, "ministerio-de-trabajo/lista-ministerio-trabajo.html", {
        # "informes": InformeWeb.objects.all()
        "planillas_resumen": PlanillaResumenGeneralMinisterioDeTrabajo.objects.all(),
        "planillas_empleados": PlanillaEmpleadosMinisterioDeTrabajo.objects.all(),
        "planillas_sueldos": PlanillaSueldosMinisterioDeTrabajo.objects.all(),
    })

""" Vista para registrar las 3 planillas del Ministerio de Trabajo.

NOTA: lo ideal hubiese sido que creara 3 páginas y 3 vistas por separado para cada planilla. Y se que se ve feo tener
un formulario gigantesco en una sola página. Sin embargo, debido a falta de tiempo, no me queda de otra que meter
todos los formularios de las 3 planillas dentro de una sola página y dentro de una sola vista.

RECUERDA que tengo que calcula el 50% de los ingresos extras, y el total del salario recibido con los ingresos extras
sumados aquí en esta vista.

Dado que hay datos que se repiten (como el número patronal), NO voy a agarrar varias veces ese mismo dato. 
Lo agarraré una sola vez, y lo meteré en las 3 tablas.

Lo del numero patronal: para evitar confusiones, le pondré otro nombre de variable al numero patronal de cada tabla, y 
le cambiare el nombre en los formularios.
"""
@login_required
# registrar_planillas_ministerio_trabajo
def register_department_of_labor_forms(request):

    # Formularios de Resumen General
    formulario_orden_1 = FormularioResumenGeneralOrden1
    formulario_orden_2 = FormularioResumenGeneralOrden2
    formulario_orden_3 = FormularioResumenGeneralOrden3
    formulario_orden_4 = FormularioResumenGeneralOrden4
    formulario_orden_5 = FormularioResumenGeneralOrden5

    # Formulario de planilla de sueldos
    formulario_sueldos = FormularioSueldosMinisterioDeTrabajo

    # Formulario de planilla de empleados
    formulario_empleados = FormularioEmpleadosMinisterioDeTrabajo


    # Si el usuario envía el formulario, esto se ejecuta
    if request.method == "POST":

        # Planilla de Empleados
        numero_patronal_de_planilla_empleados = request.POST["employer_identification_number"]
        nombre = request.POST["name"]
        apellidos = request.POST["last_name"]
        cedula = request.POST["id_number"]
        sexo = request.POST["gender"]
        fecha_de_nacimiento = request.POST["date_of_birth"]
        domicilio = request.POST["address"]
        cantidad_hijos_menores = request.POST["number_of_underage_children"]
        fecha_nacimiento_del_menor = request.POST["date_of_birth_of_the_youngest_child"]
        estado_civil = request.POST["marital_status"]
        nacionalidad = request.POST["nationality"]
        horario_de_trabajo = request.POST["work_schedule"]
        cargo = request.POST["job_title"]
        profesion = request.POST["profession"]
        fecha_inicio_trabajo_del_menor = request.POST["employment_start_date_of_the_youngest_child"]
        situacion_escolar_menor = request.POST["school_grade_in_which_the_youngest_child_is_enrolled"]
        fecha_entrada = request.POST["date_of_hire"]
        fecha_salida = request.POST["date_in_which_they_left_the_company"]
        motivo_de_salida = request.POST["reason_for_leaving_the_company"]

        # El estado lo dejaré vacío
        estado = ''

        # El timestamp lo meteré en las 3 tablas de las 3 planillas
        timestamp = datetime.datetime.now()

        # Preparando los datos para meterlos en la Planilla de Empleados
        nueva_planilla_empleados = PlanillaEmpleadosMinisterioDeTrabajo(numero_patronal=numero_patronal_de_planilla_empleados,
                                    nombre=nombre, apellidos=apellidos, cedula=cedula, sexo=sexo,
                                    fecha_nacimiento=fecha_de_nacimiento, domicilio=domicilio,
                                    cantidad_hijos_menores=cantidad_hijos_menores,
                                    fecha_nacimiento_del_menor=fecha_nacimiento_del_menor, estado_civil=estado_civil,
                                    nacionalidad=nacionalidad, horario_de_trabajo=horario_de_trabajo, cargo=cargo,
                                    profesion=profesion, fecha_inicio_trabajo_del_menor=fecha_inicio_trabajo_del_menor,
                                    situacion_escolar_menor=situacion_escolar_menor, fecha_entrada=fecha_entrada,
                                    fecha_salida=fecha_salida, motivo_de_salida=motivo_de_salida,
                                    timestamp=timestamp)


        # Esto inserta los campos en la Planilla de Empleados
        nueva_planilla_empleados.save()     # Fin de Planilla Empleados



        # Planilla de Sueldos
        numero_patronal_de_planilla_sueldos = request.POST["employer_identification_number_for_the_salary_form"]
        forma_de_pago = request.POST["pay_frequency"]
        cedula_planilla_sueldos = request.POST["id_number_for_the_salary_form"]
        importe_unitario = request.POST["salary_per_day"]

        horas_trabajadas_enero = request.POST["hours_worked_in_january"]
        salario_percibido_enero = request.POST["salary_received_in_january"]

        horas_trabajadas_febrero = request.POST["hours_worked_in_february"]
        salario_percibido_febrero = request.POST["salary_received_in_february"]

        horas_trabajadas_marzo = request.POST["hours_worked_in_march"]
        salario_percibido_marzo = request.POST["salary_received_in_march"]

        horas_trabajadas_abril = request.POST["hours_worked_in_april"]
        salario_percibido_abril = request.POST["salary_received_in_april"]

        horas_trabajadas_mayo = request.POST["hours_worked_in_may"]
        salario_percibido_mayo = request.POST["salary_received_in_may"]

        horas_trabajadas_junio = request.POST["hours_worked_in_june"]
        salario_percibido_junio = request.POST["salary_received_in_june"]

        horas_trabajadas_julio = request.POST["hours_worked_in_july"]
        salario_percibido_julio = request.POST["salary_received_in_july"]

        horas_trabajadas_agosto = request.POST["hours_worked_in_august"]
        salario_percibido_agosto = request.POST["salary_received_in_august"]

        horas_trabajadas_septiembre = request.POST["hours_worked_in_september"]
        salario_percibido_septiembre = request.POST["salary_received_in_september"]

        horas_trabajadas_octubre = request.POST["hours_worked_in_october"]
        salario_percibido_octubre = request.POST["salary_received_in_october"]

        horas_trabajadas_noviembre = request.POST["hours_worked_in_november"]
        salario_percibido_noviembre = request.POST["salary_received_in_november"]

        horas_trabajadas_diciembre = request.POST["hours_worked_in_december"]
        salario_percibido_diciembre = request.POST["salary_received_in_december"]

        horas_extras_100_por_ciento_durante_anno = request.POST["one_hundred_percent_of_extra_hours_worked_during_the_year"]
        salario_percibido_horas_extras_100_por_ciento_anno = request.POST["one_hundred_percent_of_salary_received_from_working_extra_hours"]
        aguinaldo = request.POST["christmas_bonus"]
        beneficios = request.POST["severance_pay"]
        bonificaciones = request.POST["large_family_bonus"]
        vacaciones = request.POST["accrued_vacations"]
        horas_trabajadas_incluyendo_horas_extras = request.POST["hours_worked_including_extra_hours"]

        # Salario total recibido sin ingresos extras
        total_recibido_en_concepto_de_salario = request.POST["total_amount_received_from_salary_without_supplemental_income"]

        # Estos 2 campos se calculan dividiendo las horas extras y el salario al 100% entre 2
        horas_extras_50_por_ciento_durante_anno = float(horas_extras_100_por_ciento_durante_anno) / 2
        salario_percibido_horas_extras_50_por_ciento_anno = float(salario_percibido_horas_extras_100_por_ciento_anno) / 2

        # Esto lo calculare sumando Ingresos Totales con aguinaldos y otros ingresos
        total_incluyendo_ingresos_extras = float(total_recibido_en_concepto_de_salario) + float(aguinaldo) + float(
            beneficios) + float(bonificaciones) + float(vacaciones)


        # Preparando los datos para meterlos en la Planilla de Empleados
        nueva_planilla_sueldos = PlanillaSueldosMinisterioDeTrabajo(numero_patronal=numero_patronal_de_planilla_sueldos,
                                    forma_de_pago=forma_de_pago, importe_unitario=importe_unitario, cedula=cedula_planilla_sueldos,
                                    horas_trabajadas_enero=horas_trabajadas_enero,
                                    salario_percibido_enero=salario_percibido_enero,
                                    horas_trabajadas_febrero=horas_trabajadas_febrero,
                                    salario_percibido_febrero=salario_percibido_febrero,
                                    horas_trabajadas_marzo=horas_trabajadas_marzo,
                                    salario_percibido_marzo=salario_percibido_marzo,
                                    horas_trabajadas_abril=horas_trabajadas_abril,
                                    salario_percibido_abril=salario_percibido_abril,
                                    horas_trabajadas_mayo=horas_trabajadas_mayo,
                                    salario_percibido_mayo=salario_percibido_mayo,
                                    horas_trabajadas_junio=horas_trabajadas_junio,
                                    salario_percibido_junio=salario_percibido_junio,
                                    horas_trabajadas_julio=horas_trabajadas_julio,
                                    salario_percibido_julio=salario_percibido_julio,
                                    horas_trabajadas_agosto=horas_trabajadas_agosto,
                                    salario_percibido_agosto=salario_percibido_agosto,
                                    horas_trabajadas_septiembre=horas_trabajadas_septiembre,
                                    salario_percibido_septiembre=salario_percibido_septiembre,
                                    horas_trabajadas_octubre=horas_trabajadas_octubre,
                                    salario_percibido_octubre=salario_percibido_octubre,
                                    horas_trabajadas_noviembre=horas_trabajadas_noviembre,
                                    salario_percibido_noviembre=salario_percibido_noviembre,
                                    horas_trabajadas_diciembre=horas_trabajadas_diciembre,
                                    salario_percibido_diciembre=salario_percibido_diciembre,
                                    horas_extras_100_por_ciento_durante_anno=horas_extras_100_por_ciento_durante_anno,
                                    salario_percibido_horas_extras_100_por_ciento_anno=salario_percibido_horas_extras_100_por_ciento_anno,
                                    aguinaldo=aguinaldo, beneficios=beneficios, bonificaciones=bonificaciones,
                                    vacaciones=vacaciones,
                                    horas_trabajadas_incluyendo_horas_extras=horas_trabajadas_incluyendo_horas_extras,
                                    total_recibido_en_concepto_de_salario=total_recibido_en_concepto_de_salario,
                                    horas_extras_50_por_ciento_durante_anno=horas_extras_50_por_ciento_durante_anno,
                                    salario_percibido_horas_extras_50_por_ciento_anno=salario_percibido_horas_extras_50_por_ciento_anno,
                                    total_incluyendo_ingresos_extras= total_incluyendo_ingresos_extras,
                                    timestamp=timestamp)


        # Esto inserta los campos en la Planilla de Sueldos
        nueva_planilla_sueldos.save()     # Fin Planilla Sueldos


        # Planilla de Resumen en General
        # Orden 1: Cantidad de empleados
        numero_patronal_orden_1 = request.POST["employer_identification_number_for_order_1_form"]
        anno_orden_1 = request.POST["year_for_order_1_form"]
        supervisores_o_jefes_varones_orden_1 = request.POST["male_managers_or_bosses_for_order_1_form"]
        supervisores_o_jefes_mujeres_orden_1 = request.POST["female_managers_or_bosses_for_order_1_form"]
        empleados_varones_orden_1 = request.POST["male_assistants_for_order_1_form"]
        empleados_mujeres_orden_1 = request.POST["female_assistants_for_order_1_form"]
        empleadas_mujeres_orden_1 = request.POST["female_assistants_for_order_1_form"]
        obreros_hombres_orden_1 = request.POST["male_laborers_for_order_1_form"]
        obreras_mujeres_orden_1 = request.POST["female_laborers_for_order_1_form"]
        menores_varones_orden_1 = request.POST["underage_males_for_order_1_form"]
        menores_mujeres_orden_1 = request.POST["underage_females_for_order_1_form"]

        # Orden 1. Solo meteré un 1
        orden_1 = 1

        # Orden 2: Horas trabajadas
        numero_patronal_orden_2 = request.POST["employer_identification_number_for_order_2_form"]
        anno_orden_2 = request.POST["year_for_order_2_form"]
        supervisores_o_jefes_varones_orden_2 = request.POST["male_managers_or_bosses_for_order_2_form"]
        supervisores_o_jefes_mujeres_orden_2 = request.POST["female_managers_or_bosses_for_order_2_form"]
        empleados_varones_orden_2 = request.POST["male_assistants_for_order_2_form"]
        empleados_mujeres_orden_2 = request.POST["female_assistants_for_order_2_form"]
        empleadas_mujeres_orden_2 = request.POST["female_assistants_for_order_2_form"]
        obreros_hombres_orden_2 = request.POST["male_laborers_for_order_2_form"]
        obreras_mujeres_orden_2 = request.POST["female_laborers_for_order_2_form"]
        menores_varones_orden_2 = request.POST["underage_males_for_order_2_form"]
        menores_mujeres_orden_2 = request.POST["underage_females_for_order_2_form"]

        # Orden 2. Solo meteré un 2
        orden_2 = 2

        # Orden 3: Sueldos o jornales
        numero_patronal_orden_3 = request.POST["employer_identification_number_for_order_3_form"]
        anno_orden_3 = request.POST["year_for_order_3_form"]
        supervisores_o_jefes_varones_orden_3 = request.POST["male_managers_or_bosses_for_order_3_form"]
        supervisores_o_jefes_mujeres_orden_3 = request.POST["female_managers_or_bosses_for_order_3_form"]
        empleados_varones_orden_3 = request.POST["male_assistants_for_order_3_form"]
        empleados_mujeres_orden_3 = request.POST["female_assistants_for_order_3_form"]
        empleadas_mujeres_orden_3 = request.POST["female_assistants_for_order_3_form"]
        obreros_hombres_orden_3 = request.POST["male_laborers_for_order_3_form"]
        obreras_mujeres_orden_3 = request.POST["female_laborers_for_order_3_form"]
        menores_varones_orden_3 = request.POST["underage_males_for_order_3_form"]
        menores_mujeres_orden_3 = request.POST["underage_females_for_order_3_form"]

        # Orden 3. Solo meteré un 3
        orden_3 = 3

        # Orden 4: Cantidad de ingresos
        numero_patronal_orden_4 = request.POST["employer_identification_number_for_order_4_form"]
        anno_orden_4 = request.POST["year_for_order_4_form"]
        supervisores_o_jefes_varones_orden_4 = request.POST["male_managers_or_bosses_for_order_4_form"]
        supervisores_o_jefes_mujeres_orden_4 = request.POST["female_managers_or_bosses_for_order_4_form"]
        empleados_varones_orden_4 = request.POST["male_assistants_for_order_4_form"]
        empleados_mujeres_orden_4 = request.POST["female_assistants_for_order_4_form"]
        empleadas_mujeres_orden_4 = request.POST["female_assistants_for_order_4_form"]
        obreros_hombres_orden_4 = request.POST["male_laborers_for_order_4_form"]
        obreras_mujeres_orden_4 = request.POST["female_laborers_for_order_4_form"]
        menores_varones_orden_4 = request.POST["underage_males_for_order_4_form"]
        menores_mujeres_orden_4 = request.POST["underage_females_for_order_4_form"]

        # Orden 4. Solo meteré un 4
        orden_4 = 4

        # Orden 5: Cantidad de egresos
        numero_patronal_orden_5 = request.POST["employer_identification_number_for_order_5_form"]
        anno_orden_5 = request.POST["year_for_order_5_form"]
        supervisores_o_jefes_varones_orden_5 = request.POST["male_managers_or_bosses_for_order_5_form"]
        supervisores_o_jefes_mujeres_orden_5 = request.POST["female_managers_or_bosses_for_order_5_form"]
        empleados_varones_orden_5 = request.POST["male_assistants_for_order_5_form"]
        empleados_mujeres_orden_5 = request.POST["female_assistants_for_order_5_form"]
        empleadas_mujeres_orden_5 = request.POST["female_assistants_for_order_5_form"]
        obreros_hombres_orden_5 = request.POST["male_laborers_for_order_5_form"]
        obreras_mujeres_orden_5 = request.POST["female_laborers_for_order_5_form"]
        menores_varones_orden_5 = request.POST["underage_males_for_order_5_form"]
        menores_mujeres_orden_5 = request.POST["underage_females_for_order_5_form"]

        # Orden 5. Solo meteré un 5
        orden_5 = 5


        # Preparando los datos para meterlos en la Planilla de Resumen
        nueva_planilla_resumen = PlanillaResumenGeneralMinisterioDeTrabajo(
                                    numero_patronal_orden_1=numero_patronal_orden_1,
                                    anno_orden_1=anno_orden_1,
                                    supervisores_o_jefes_varones_orden_1=supervisores_o_jefes_varones_orden_1,
                                    supervisores_o_jefes_mujeres_orden_1=supervisores_o_jefes_mujeres_orden_1,
                                    empleados_varones_orden_1=empleados_varones_orden_1,
                                    empleados_mujeres_orden_1=empleados_mujeres_orden_1,
                                    empleadas_mujeres_orden_1=empleadas_mujeres_orden_1,
                                    obreros_hombres_orden_1=obreros_hombres_orden_1,
                                    obreras_mujeres_orden_1=obreras_mujeres_orden_1,
                                    menores_varones_orden_1=menores_varones_orden_1,
                                    menores_mujeres_orden_1=menores_mujeres_orden_1,
                                    orden_1=1,
                                    numero_patronal_orden_2=numero_patronal_orden_2,
                                    anno_orden_2=anno_orden_2,
                                    supervisores_o_jefes_varones_orden_2=supervisores_o_jefes_varones_orden_2,
                                    supervisores_o_jefes_mujeres_orden_2=supervisores_o_jefes_mujeres_orden_2,
                                    empleados_varones_orden_2=empleados_varones_orden_2,
                                    empleados_mujeres_orden_2=empleados_mujeres_orden_2,
                                    empleadas_mujeres_orden_2=empleadas_mujeres_orden_2,
                                    obreros_hombres_orden_2=obreros_hombres_orden_2,
                                    obreras_mujeres_orden_2=obreras_mujeres_orden_2,
                                    menores_varones_orden_2=menores_varones_orden_2,
                                    menores_mujeres_orden_2=menores_mujeres_orden_2,
                                    orden_2=2,
                                    numero_patronal_orden_3=numero_patronal_orden_3,
                                    anno_orden_3=anno_orden_3,
                                    supervisores_o_jefes_varones_orden_3=supervisores_o_jefes_varones_orden_3,
                                    supervisores_o_jefes_mujeres_orden_3=supervisores_o_jefes_mujeres_orden_3,
                                    empleados_varones_orden_3=empleados_varones_orden_3,
                                    empleados_mujeres_orden_3=empleados_mujeres_orden_3,
                                    empleadas_mujeres_orden_3=empleadas_mujeres_orden_3,
                                    obreros_hombres_orden_3=obreros_hombres_orden_3,
                                    obreras_mujeres_orden_3=obreras_mujeres_orden_3,
                                    menores_varones_orden_3=menores_varones_orden_3,
                                    menores_mujeres_orden_3=menores_mujeres_orden_3,
                                    orden_3=3,
                                    numero_patronal_orden_4=numero_patronal_orden_4,
                                    anno_orden_4=anno_orden_4,
                                    supervisores_o_jefes_varones_orden_4=supervisores_o_jefes_varones_orden_4,
                                    supervisores_o_jefes_mujeres_orden_4=supervisores_o_jefes_mujeres_orden_4,
                                    empleados_varones_orden_4=empleados_varones_orden_4,
                                    empleados_mujeres_orden_4=empleados_mujeres_orden_4,
                                    empleadas_mujeres_orden_4=empleadas_mujeres_orden_4,
                                    obreros_hombres_orden_4=obreros_hombres_orden_4,
                                    obreras_mujeres_orden_4=obreras_mujeres_orden_4,
                                    menores_varones_orden_4=menores_varones_orden_4,
                                    menores_mujeres_orden_4=menores_mujeres_orden_4,
                                    orden_4=4,
                                    numero_patronal_orden_5=numero_patronal_orden_5,
                                    anno_orden_5=anno_orden_5,
                                    supervisores_o_jefes_varones_orden_5=supervisores_o_jefes_varones_orden_5,
                                    supervisores_o_jefes_mujeres_orden_5=supervisores_o_jefes_mujeres_orden_5,
                                    empleados_varones_orden_5=empleados_varones_orden_5,
                                    empleados_mujeres_orden_5=empleados_mujeres_orden_5,
                                    empleadas_mujeres_orden_5=empleadas_mujeres_orden_5,
                                    obreros_hombres_orden_5=obreros_hombres_orden_5,
                                    obreras_mujeres_orden_5=obreras_mujeres_orden_5,
                                    menores_varones_orden_5=menores_varones_orden_5,
                                    menores_mujeres_orden_5=menores_mujeres_orden_5,
                                    orden_5=5,
                                    timestamp=timestamp)


        # Esto inserta los campos en la Planilla de Empleados
        nueva_planilla_resumen.save()     # Fin de Planilla Resumen

        # Mensaje flash de confirmación
        # messages.success(request, "Se ha registrado unas nuevas Planillas del Ministerio de Trabajo correctamente.")
        messages.success(request, "A new set of Department of Labor forms have been successfully registered.")

        # Esto redirige al usuario a la lista de contratos
        return redirect('department_labor_form_list')

    # Esto renderiza la página para registrar los contratos
    else:
        return render(request, "ministerio-de-trabajo/registrar-ministerio-trabajo.html", {
            "formulario_orden_1": formulario_orden_1,
            "formulario_orden_2": formulario_orden_2,
            "formulario_orden_3": formulario_orden_3,
            "formulario_orden_4": formulario_orden_4,
            "formulario_orden_5": formulario_orden_5,
            "formulario_sueldos": formulario_sueldos,
            "formulario_empleados": formulario_empleados
        })

""" Vista para ver Planilla de Empleados del Ministerio de Trabajo
"""
@login_required
# ver_planilla_empleado_ministerio
def view_employees_form_department_of_labor(request, id_planilla):

    # Esto agarra el descuento que quiero ver
    planilla_seleccionada = PlanillaEmpleadosMinisterioDeTrabajo.objects.filter(id=id_planilla)

    return render(request, "ministerio-de-trabajo/ver-planilla-empleados.html", {
        "planilla_seleccionada": planilla_seleccionada
    })

""" Vista para ver Planilla de Resumen del Ministerio de Trabajo
"""
@login_required
# ver_planilla_resumen_ministerio
def view_summary_form_department_of_labor(request, id_planilla):

    # Esto agarra el descuento que quiero ver
    planilla_seleccionada = PlanillaResumenGeneralMinisterioDeTrabajo.objects.filter(id=id_planilla)

    return render(request, "ministerio-de-trabajo/ver-planilla-resumen.html", {
        "planilla_seleccionada": planilla_seleccionada
    })

""" Vista para ver Planilla de Sueldo del Ministerio de Trabajo.
"""
@login_required
# ver_planilla_sueldo_ministerio
def view_salary_form_department_of_labor(request, id_planilla):

    # Esto agarra el descuento que quiero ver
    planilla_seleccionada = PlanillaSueldosMinisterioDeTrabajo.objects.filter(id=id_planilla)

    return render(request, "ministerio-de-trabajo/ver-planilla-sueldos.html", {
        "planilla_seleccionada": planilla_seleccionada
    })

""" Vista para Registrar una Planilla del IPS
"""
@login_required
def registrar_ips(request):

    formulario = FormularioPlanillaIPS

    # Si el usuario envía el formulario
    if request.method == "POST":
        numero_de_orden = request.POST["order_number"]
        nombre = request.POST["name"]
        apellidos = request.POST["last_name"]
        cedula = request.POST["id_number"]

        # Imagen con la firma del encargado de recursos humanos
        firma_encargado_rrhh = request.FILES["signature_of_the_manager_that_created_the_social_security_form"]

        salario_imponible = request.POST["taxable_income"]
        numero_de_asegurado = request.POST["social_security_number"]
        categoria = request.POST["category"]
        codigo = request.POST["code"]
        dias_trabajados_mes_anterior = request.POST["number_of_days_worked_on_the_previous_month"]
        dias_trabajados_mes_actual = request.POST["days_worked_on_the_current_month"]

        # RSA
        reconocimiento_servicios_anteriores = request.POST["acknowledgement_of_services_done_prior_to_1974"]

        timestamp = datetime.datetime.now()

        # Preparando los datos para meterlos en la base de datos
        nuevo_ips = PlanillaIPS(numero_de_orden=numero_de_orden, nombre=nombre, apellidos=apellidos, cedula=cedula,
                        firma_encargado_rrhh=firma_encargado_rrhh, salario_imponible=salario_imponible,
                        numero_de_asegurado=numero_de_asegurado, categoria=categoria, codigo=codigo,
                        dias_trabajados_mes_anterior=dias_trabajados_mes_anterior,
                        dias_trabajados_mes_actual=dias_trabajados_mes_actual,
                        reconocimiento_servicios_anteriores=reconocimiento_servicios_anteriores, timestamp=timestamp)

        # Esto inserta los campos en la base de datos
        nuevo_ips.save()

        # Mensaje flash de confirmación
        # messages.success(request, "Se ha registrado una nueva planilla del IPS correctamente.")
        messages.success(request, "A new social security form has been successfully registered.")

        # Esto redirige al usuario a la lista de contratos
        return redirect('lista_ips')

    # Esto renderiza la página para registrar los contratos
    else:
        return render(request, "ips/registrar-ips.html", {
            "formulario": formulario,
        })

""" Vista para mostrar Lista de Planillas del IPS
"""
@login_required
def lista_ips(request):

    return render(request, "ips/lista-planillas-ips.html", {
        "planillas": PlanillaIPS.objects.all(),
    })

""" Vista para Ver Detalladamente las Planillas del IPS
"""
@login_required
def ver_planilla_ips(request, id_planilla):

    # Esto agarra el descuento que quiero ver
    planilla_seleccionada = PlanillaIPS.objects.filter(id=id_planilla)

    return render(request, "ips/ver-ips.html", {
        "planilla_seleccionada": planilla_seleccionada
    })