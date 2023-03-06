# Holiday Auto Care.
Proyecto - Ingenieria del software 1 (CI3715)

***

## Holiday Internacional
Es una empresa de servicios mecanicos autonotrices. Esta dispone de un
modelo de negocios orientado en la digitalizacion de sus diferentes procesos, cuyos resultados 
son de alto valor agregado para el cliente.

***

## Objetivo
Desarrollar un sistema automatizado de gestion de talleres mecanico automotrices de alta gama
para la empresa Holiday Int

***

## Historias de usuario que el sistema de gestion satisface. 

## Iteracion 0
- Como *sistema*, puedo identificas a usuarios para controlar el acceso no autorizado al sistema
- Como *sistema*, puedo autenticar usuarios para controlar el acceso no autorizado al sistema.
- Como administrados, puedo crear perfiles de usuarios para controlar el acceso no autorizado al sistema
- Como *administrador*, puedo ingresar roles a los usuarios para controlar el acceso no autorizado al sistema.

### Iteracion 1
- Como *gerente*, puedo ingresar los parametros de un proyecto en el sistema para gestionar el portafolio de proyectos de un taller automotriz en particular.
- Como *sistema*, puedo registrar los diferentes eventos del sistema en un Logger para auditar el sistema.

### Iteracion 2
- Como *analista de operaciones*, puedo ingresar los datos de identificacion del vehiculo que ingresa al taller para registrar a los vehiculos de los clientes del taller del sistema.
- Como *analista de operaciones*, puedo ingresar los datos personales de diferentes clientes del taller para registrar a los vehiculos de los clientes del taller en el sistema.
- Como *analista de operaciones*, puedo ingresar los datos de un vehiculo automotor de un cliente del taller en particular para registrar a los vechiculos de los clientes del taller.

***

## Configuracion del ambiente de ejecucion
Se debe tener instalado Flask (al menos version 2.2.2) y sqlite3 (al menos version 3.37.2)

Antes de ejecutar la aplicacion, se debe de inicializar la base de datos con el siguiente comando:
    $ flask --app app init-db

Para la ejecucion de la aplicacion se debe ejecutar el siguiente comando:
    $ flask --app flaskr --debug run