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
    path('login', views.log_in_view, name='log_in_view'),
    path('cerrar-sesion', views.cerrar_sesion, name='cerrar_sesion'),

    path('sanctions-list', views.sanctions_list, name='sanctions_list'),
    path('register-sanction', views.register_sanction, name='register_sanction'),
    path('<str:id_sancion>/delete-sanction/', views.delete_sanction, name='delete_sanction'),
    path('<str:id_sancion>/view-sanction/', views.view_sanction, name='view_sanction'),

    path('large-family-bonus-reports-list', views.large_family_bonus_reports_list,
         name='large_family_bonus_reports_list'),
    path('register-large-family-bonus-report', views.register_large_family_bonus_report,
         name='register_large_family_bonus_report'),
    path('<str:id_bonificacion>/view-large-family-bonus-report/', views.view_large_family_bonus_report,
         name='view_large_family_bonus_report'),

    path('list-of-permissions', views.list_of_permissions, name='list_of_permissions'),
    path('register-permission', views.register_permission, name='register_permission'),
    path('<str:id_permiso>/view-permission/', views.view_permission, name='view_permission'),

    path('job-profile-list', views.job_profile_list, name='job_profile_list'),
    path('register-job-profile', views.register_job_profile, name='register_job_profile'),
    path('<str:id_cargo>/view-job-profile', views.view_job_profile, name='view_job_profile'),

    path('list-of-proofs-of-leaves', views.list_of_proofs_of_leaves, name='list_of_proofs_of_leaves'),
    path('register-proof-of-leave', views.register_proof_of_leave, name='register_proof_of_leave'),
    path('<str:id_justificacion>/view-proof-of-leave', views.view_proof_of_leave, name='view_proof_of_leave'),

    path('discount-list', views.discount_list, name='discount_list'),
    path('register-discounts', views.register_discounts, name='register_discounts'),
    path('<str:id_descuento>/view-discount-statement', views.view_discount_statement, name='view_discount_statement'),

    path('supplemental-income-statements-list', views.supplemental_income_statements_list,
         name='supplemental_income_statements_list'),
    path('register-supplemental-income-statement', views.register_supplemental_income_statement,
         name='register_supplemental_income_statement'),
    path('<str:id_ingreso>/view-supplemental-income-statement', views.view_supplemental_income_statement,
         name='view_supplemental_income_statement'),

    path('vacation-report-list', views.vacation_report_list, name='vacation_report_list'),
    path('register-vacation-report', views.register_vacation_report, name='register_vacation_report'),
    path('<str:id_vacacion>/view-vacation-report', views.view_vacation_report, name='view_vacation_report'),

    path('list-of-resumes', views.list_of_resumes, name='list_of_resumes'),
    path('register-a-resume', views.register_a_resume, name='register_a_resume'),
    path('<str:id_curriculum>/view-resume', views.view_resume, name='view_resume'),

    path('list-of-christmas-bonus', views.list_of_christmas_bonus, name='list_of_christmas_bonus'),
    path('register-christmas-bonus', views.register_christmas_bonus, name='register_christmas_bonus'),
    path('<str:id_aguinaldo>/view-christmas-bonus', views.view_christmas_bonus, name='view_christmas_bonus'),

    path('attendance-dates-list', views.attendance_dates_list, name='attendance_dates_list'),
    path('register-attendance-date', views.register_attendance_date, name='register_attendance_date'),
    path('<str:id_dia>/register-attendance-entry', views.register_attendance_entry, name='register_attendance_entry'),
    path('<str:id_dia>/attendance-list', views.attendance_list, name='attendance_list'),

    path('final-pay-forms-list', views.final_pay_forms_list, name='final_pay_forms_list'),
    path('register-final-pay', views.register_final_pay, name='register_final_pay'),
    path('<str:id_liquidacion>/view-final-pay-form', views.view_final_pay_form, name='view_final_pay_form'),

    path('payroll-statement-list', views.payroll_statement_list, name='payroll_statement_list'),
    path('register-payroll-statement', views.register_payroll_statement, name='register_payroll_statement'),
    path('<str:id_liquidacion>/view-payroll-statement', views.view_payroll_statement, name='view_payroll_statement'),

    path('dossier-list', views.dossier_list, name='dossier_list'),
    path('register-dossier', views.register_dossier, name='register_dossier'),
    path('<str:id_legajo>/view-dossier', views.view_dossier, name='view_dossier'),

    path('contract-list', views.contract_list, name='contract_list'),
    path('register-contract', views.register_contract, name='register_contract'),
    path('<str:id_contrato>/view-contract', views.view_contract, name='view_contract'),

    path('web-report-list', views.web_report_list, name='web_report_list'),
    path('register-web-report', views.register_web_report, name='register_web_report'),
    path('<str:id_informe>/view-web-report', views.view_web_report, name='view_web_report'),

    path('department-labor-form-list', views.department_labor_form_list, name='department_labor_form_list'),
    path('register-department-of-labor-forms', views.register_department_of_labor_forms,
         name='register_department_of_labor_forms'),
    path('<str:id_planilla>/view-employees-form-department-of-labor', views.view_employees_form_department_of_labor,
         name='view_employees_form_department_of_labor'),
    path('<str:id_planilla>/view-summary-form-department-of-labor', views.view_summary_form_department_of_labor,
         name='view_summary_form_department_of_labor'),
    path('<str:id_planilla>/view-salary-form-department-of-labor', views.view_salary_form_department_of_labor,
         name='view_salary_form_department_of_labor'),

    path('social-security-forms-list', views.social_security_forms_list, name='social_security_forms_list'),
    path('register-social-security-form', views.register_social_security_form, name='register_social_security_form'),
    path('<str:id_planilla>/view-social-security-form', views.view_social_security_form,
         name='view_social_security_form'),
]