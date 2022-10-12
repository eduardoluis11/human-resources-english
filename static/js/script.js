/* Veré si esto me agrega el onchange al formulario de django de la bonificacion familiar. Lo necesito para que,
cada vez que escriba algo en una casilla para realizar un cálculo, se haga el cálculo (fuente:
https://groups.google.com/g/django-users/c/znTgVB4tIfc).

La funcion calculadora_bonificacion_familiar es una calculadora para calcular el número de hijos y la bonificación
total en el formulario para registrarbonificaciones familiares.

Una vez que el usuario escriba algo en las casillas con los números de hijos y el salario minimo, se rellenará
automáticamente el número de hios que cualifican para la bonificacion, y se calculará la bonificacion familiar.

La bonificación familar equivale al 5% del salario mínimo vigente multiplicado por el número total de hijos que
sean menores de edad, y/o que sean mayores de edad que sufran de discapacidades.

Se va a activar "on input", es decir, a penas el usuario teclee cualquier cosa en las casillas "numero de hijos
menores", "numero de hijos con discapacidades", y en "salario minimo vigente".

Para transformar un número en un entero en Js, debo usar parseInt.

NO DEBO USAR getElementByID. Debo usar querySelector. Sino, me sale un error en la consola
*/
//window.onload = function()
//    {
//
//        // Si el usuario teclea en la casilla de hijos menores
//        document.getElementById("id_numero_de_hijos_menores").onchange = function calculadora_bonificacion_familiar()
//        {
//
//        // Esto agarra el valor de las 3 casillas que teclee el usuario
//        let hijos_menores = document.querySelector("#id_numero_de_hijos_menores").value;
//        let hijos_con_discapacidades = document.querySelector("#id_numero_de_hijos_mayores_con_discapacidades").value;
//        let salario_minimo_mensual_vigente = document.querySelector("#id_salario_minimo_mensual_vigente").value;
//
//        // Esto agarra las 2 casillas en las cuales debo mostrar el cálculo
//        let bonificacion_familiar = document.querySelector("#id_bonificacion_familiar_a_recibir");
//        let total_hijos = document.querySelector("#id_numero_total_de_hijos_que_cualifican_para_la_bonificacion_familiar");
//
//        // Esto suma el número de hijos menores y con discapacidades
//        total_hijos.value = parseInt(hijos_menores) + parseInt(hijos_con_discapacidades)
//
//        let suma_hijos = total_hijos.value
//
//        // Esto calcula la bonificacion familiar (mutiplicando el 5% de lsalario minimo por el numero de hijos)
//        bonificacion_familiar.value = (5 / 100) * suma_hijos
//
////        console.log(parseInt(hijos_menores) + parseInt(hijos_con_discapacidades))
//
//        }
//
//        // Si el usuario teclea en la casilla de hijos con discapacidades
//        document.getElementById("id_numero_de_hijos_mayores_con_discapacidades").onchange = function calculadora_bonificacion_familiar()
//        {
//
//            // Esto agarra el valor de las 3 casillas que teclee el usuario
//            let hijos_menores = document.querySelector("#id_numero_de_hijos_menores").value;
//            let hijos_con_discapacidades = document.querySelector("#id_numero_de_hijos_mayores_con_discapacidades").value;
//            let salario_minimo_mensual_vigente = document.querySelector("#id_salario_minimo_mensual_vigente").value;
//
//            // Esto agarra las 2 casillas en las cuales debo mostrar el cálculo
//            let bonificacion_familiar = document.querySelector("#id_bonificacion_familiar_a_recibir");
//            let total_hijos = document.querySelector("#id_numero_total_de_hijos_que_cualifican_para_la_bonificacion_familiar");
//
//            // Esto suma el número de hijos menores y con discapacidades
//            total_hijos.value = parseInt(hijos_menores) + parseInt(hijos_con_discapacidades)
//
//            let suma_hijos = total_hijos.value
//
//            // Esto calcula la bonificacion familiar (mutiplicando el 5% de lsalario minimo por el numero de hijos)
//            bonificacion_familiar.value = (5 / 100) * suma_hijos
//
//        }
//
//        // Si el usuario teclea en la casilla de salario minimo
//        document.getElementById("id_numero_total_de_hijos_que_cualifican_para_la_bonificacion_familiar").onchange = function calculadora_bonificacion_familiar()
//        {
//
//            // Esto agarra el valor de las 3 casillas que teclee el usuario
//            let hijos_menores = document.querySelector("#id_numero_de_hijos_menores").value;
//            let hijos_con_discapacidades = document.querySelector("#id_numero_de_hijos_mayores_con_discapacidades").value;
//            let salario_minimo_mensual_vigente = document.querySelector("#id_salario_minimo_mensual_vigente").value;
//
//            // Esto agarra las 2 casillas en las cuales debo mostrar el cálculo
//            let bonificacion_familiar = document.querySelector("#id_bonificacion_familiar_a_recibir");
//            let total_hijos = document.querySelector("#id_numero_total_de_hijos_que_cualifican_para_la_bonificacion_familiar");
//
//            // Esto suma el número de hijos menores y con discapacidades
//            total_hijos.value = parseInt(hijos_menores) + parseInt(hijos_con_discapacidades)
//
//            let suma_hijos = total_hijos.value
//
//            // Esto calcula la bonificacion familiar (mutiplicando el 5% de lsalario minimo por el numero de hijos)
//            bonificacion_familiar.value = (5 / 100) * suma_hijos
//
//        }

//        document.getElementById("id_numero_de_hijos_mayores_con_discapacidades").onchange = prueba()

//        prueba()
//    };
//




/* Esto es para probar si el JS me funciona */
function prueba() {
    console.log("El JS del static funciona.")
}

