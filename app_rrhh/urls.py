from django.urls import path
from . import views

""" URLs de los distintos views/vistas.

El enlace a la página para registrarse será /registrar.

Si el usuario entra al enlace "cerrar-sesion", automáticamente cerrará su sesión.

Para borrar una sanción, voy a necesitar la ID de esa sanción. Por lo tanto, tengo que pasar la ID como un argumento en 
la URL usando "str".

Para registrar asistencias en un dia, tendre que pasar un argumento, el cual sera la id de esa fecha. Ahi, es donde 
podre registrar cuales empleados fueron a trabajar ese dia

Por ejemplo, para ver la lista de empleados que fueron a ttabajar el 19 de agosto, y como el 19 de agosto tiene de id 
"1", entonces la lista de empleados que asistio ese dia estara en la URL "1/lista-asistencias"

Y, para registrar a un empleado que asistio ese dia, lo pondre en "1/registrar-asistencia" (para registrarle la 
asistencia).
"""
urlpatterns = [
    path('', views.index, name='index'),
    path('registrar', views.registrar, name='registrar'),
    path('iniciar-sesion', views.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar-sesion', views.cerrar_sesion, name='cerrar_sesion'),
    path('lista-sanciones', views.lista_sanciones, name='lista_sanciones'),
    path('registrar-sancion', views.registrar_sancion, name='registrar_sancion'),
    path('<str:id_sancion>/borrar-sancion/', views.borrar_sancion, name='borrar_sancion'),
    path('<str:id_sancion>/ver-sancion/', views.ver_sancion, name='ver_sancion'),
    path('lista-bonificaciones', views.lista_bonificaciones_familiares, name='lista_bonificaciones_familiares'),
    path('registrar-bonificacion', views.registrar_bonificacion_familiar, name='registrar_bonificacion_familiar'),
    path('<str:id_bonificacion>/ver-bonificacion/', views.ver_bonificacion, name='ver_bonificacion'),
    path('lista-permisos', views.lista_permisos, name='lista_permisos'),
    path('registrar-permiso', views.registrar_permiso, name='registrar_permiso'),
    path('<str:id_permiso>/ver-permiso/', views.ver_permiso, name='ver_permiso'),

    path('lista-de-perfiles', views.lista_perfiles_cargos, name='lista_perfiles_cargos'),
    path('registrar-perfil-cargo', views.registrar_perfil_cargo, name='registrar_perfil_cargo'),
    path('<str:id_cargo>/ver-perfil-cargo', views.ver_cargo, name='ver_cargo'),

    path('lista-justificaciones', views.lista_justificaciones, name='lista_justificaciones'),
    path('registrar-justificacion', views.registrar_justificacion_permiso, name='registrar_justificacion_permiso'),
    path('<str:id_justificacion>/ver-justificacion', views.ver_justificacion, name='ver_justificacion'),

    path('lista-descuentos', views.lista_descuentos, name='lista_descuentos'),
    path('registrar-descuentos', views.registrar_descuentos, name='registrar_descuentos'),
    path('<str:id_descuento>/ver-descuento', views.ver_descuentos, name='ver_descuentos'),

    path('lista-ingresos-extras', views.lista_ingresos_extras, name='lista_ingresos_extras'),
    path('registrar-ingresos-extras', views.registrar_ingresos_extras, name='registrar_ingresos_extras'),
    path('<str:id_ingreso>/ver-ingreso-extra', views.ver_ingreso_extra, name='ver_ingreso_extra'),

    path('lista-vacaciones', views.lista_vacaciones, name='lista_vacaciones'),
    path('registrar-vacaciones', views.registrar_vacaciones, name='registrar_vacaciones'),
    path('<str:id_vacacion>/ver-vacacion', views.ver_vacacion, name='ver_vacacion'),

    path('lista-curriculums', views.lista_curriculums, name='lista_curriculums'),
    path('registrar-curriculum', views.registrar_curriculum, name='registrar_curriculum'),
    path('<str:id_curriculum>/ver-curriculum', views.ver_curriculum, name='ver_curriculum'),

    path('lista-aguinaldos', views.lista_aguinaldos, name='lista_aguinaldos'),
    path('registrar-aguinaldos', views.registrar_aguinaldos, name='registrar_aguinaldos'),
    path('<str:id_aguinaldo>/ver-aguinaldo', views.ver_aguinaldo, name='ver_aguinaldo'),

    path('lista-dias-asistencia', views.lista_dias_asistencia, name='lista_dias_asistencia'),
    path('registrar-dia-asistencia', views.registrar_dia_asistencia, name='registrar_dia_asistencia'),
    path('<str:id_dia>/registrar-asistencia', views.registrar_asistencia, name='registrar_asistencia'),
    path('<str:id_dia>/lista-asistencias', views.lista_asistencias, name='lista_asistencias'),

    path('lista-liquidacion-personal', views.lista_liquidacion_personal, name='lista_liquidacion_personal'),
    path('registrar-liquidacion-personal', views.registrar_liquidacion_personal, name='registrar_liquidacion_personal'),
    path('<str:id_liquidacion>/ver-liquidacion-personal', views.ver_liquidacion_personal, name='ver_liquidacion_personal'),

    path('lista-liquidacion-salarios', views.lista_liquidacion_salarios, name='lista_liquidacion_salarios'),
    path('registrar-liquidacion-salario', views.registrar_liquidacion_salario, name='registrar_liquidacion_salario'),
    path('<str:id_liquidacion>/ver-liquidacion-salario', views.ver_liquidacion_salario, name='ver_liquidacion_salario'),

    path('lista-legajos', views.lista_legajos, name='lista_legajos'),
    path('registrar-legajo', views.registrar_legajo, name='registrar_legajo'),
    path('<str:id_legajo>/ver-legajo', views.ver_legajo, name='ver_legajo'),

    path('lista-contratos', views.lista_contratos, name='lista_contratos'),
    path('registrar-contrato', views.registrar_contrato, name='registrar_contrato'),
    path('<str:id_contrato>/ver-contrato', views.ver_contrato, name='ver_contrato'),

    path('lista-informes-web', views.lista_informes, name='lista_informes'),
    path('registrar-informe-web', views.registrar_informe_web, name='registrar_informe_web'),
    path('<str:id_informe>/ver-informe', views.ver_informe, name='ver_informe'),

    path('lista-ministerio-trabajo', views.lista_ministerio_trabajo, name='lista_ministerio_trabajo'),
    path('registrar-planillas-ministerio-trabajo', views.registrar_planillas_ministerio_trabajo, name='registrar_planillas_ministerio_trabajo'),
    path('<str:id_planilla>/ver-planilla-empleado-ministerio', views.ver_planilla_empleado_ministerio, name='ver_planilla_empleado_ministerio'),
    path('<str:id_planilla>/ver-planilla-resumen-ministerio', views.ver_planilla_resumen_ministerio, name='ver_planilla_resumen_ministerio'),
    path('<str:id_planilla>/ver-planilla-sueldo-ministerio', views.ver_planilla_sueldo_ministerio, name='ver_planilla_sueldo_ministerio'),

    path('lista-planillas-ips', views.lista_ips, name='lista_ips'),
    path('registrar-planilla-ips', views.registrar_ips, name='registrar_ips'),
    path('<str:id_planilla>/ver-planilla-ips', views.ver_planilla_ips, name='ver_planilla_ips'),
]