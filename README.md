# Mattilda API - Prueba Técnica

<h1 id="indice">Indice</h1>

- [Vista General](#vista_general)
- [¿Cómo correr este proyecto?](#run_project)
- [Creación del diagrama ER](#er)


<h1 id="fin">Vista General</h1>

Proyecto realizado para llevar a cabo la prueba técnica de Mattilda. Aquí encontrará el proceso para llevar a cabo el levantamiento del proyecto para validar su función. Así como observaciones, mejoras y decisiones técnicas tomadas durante el desarrollo.

<h1 id="run_project">¿Cómo correr este proyecto?</h1>

> NOTA: Si no quieres levantar el proyecto para probarlo en local. Puedes consumir la API directamente desde Internet. Pasa al apartado: **¿Cómo consumir los endpoints?** para ver cómo hacerlo.

Para poder llevar a cabo los siguientes pasos, es necesario contar con las siguientes herramientas instaladas en el sistema:
- Docker
- Python >= 3.11, <4.0

<h2 id="config_docker">Modo Dockerizado y recomendado</h2>

1. **Lo primero que se debe de realizar es la clonación de este proyecto.**


> Por favor ejecuta los comandos en orden.

```Bash
# Creacion de una carpeta para trabajo
mkdir Work
cd Work
# Descarga del proyecto
git clone <URL DEL PROYECTO>
cd API_tilda
```
Una vez realizado lo anterior y posicionados en la carpeta del proyecto, procedemos con la preparación de docker.

2. **Preparación de Docker y levantamiento.**

> **!** Antes de levantar el contenedor. Por favor revisa el archivo .env.txt en la ruta **src/config**.

Es necesario revisar y hacer lo que se pide en el archivo .env.txt. Ya que es un archivo que se usa internamente en los contenedores. Grosso modo, eliminar la extensión.

Puedes hacer: `mv .env.txt .env`

Una vez hecho, vuelvete a posicionar al mismo nivel de la carpeta src.

De tal manera que si haces: `ls`
obtengas de salida algo similar a:

`Dockerfile README.md docker-compose.yml img_docs poetry.lock pyproject.toml src`

Notese que la variable de entorno del archivo **.env** no es crítica. Se ha añadido para facilitar la revisión a la persona que revise este proyecto. Pero en **un entorno de producción, añadir las variables en el repositorio es una mala práctica.**

Continuemos.

```bash
# creación de la red útilizada en los contenedores
docker network create mattilda-network

# levantar los contenedores
docker compose up --build
```
Si todo salio bien. Deberíamos de ver algo como lo siguiente:
![Ejecución de docker build docker build.](img_docs/docker_build.png)


3. **Conexión a la base de datos mediante pgadmin (opcional).**

> Este paso es opcional, si quieres visualizar los datos en el administrador de postgres.
En caso de que no quieras, puedes pasar al paso 4.

Lo anterior nos realizará el levantamiento de los tres contenedores.****
- Nuestra API (local_fast_api).
- Nuestra base de datos en PostgreSQL (local_pgdb_admin)
- Nuestra interfaz para administrar postgresql (local_pgadmin4_container)
![Servicios levantados.](img_docs/docker_ps.png)


Ahora nos dirigimos a nuestro navegador y accedemos a la ruta: http://localhost:8888/ para acceder al panel de administración con pgadmin.

Las credenciales para acceder son las que hemos puesto en nuestro archivo docker:
![Login de pgadmin.](img_docs/pgadmin_1_login.png)

**username:** mattilda@email.com
**password:** mattilda

Una vez que hemos logrado acceder a PGAdmin, procedemos a crear la base de datos de la siguiente manera. Nos dirigimos a **register server** (click derecho sobre Servers -> Register -> Server) y registramos un nuevo servidor llamado: **_LOCAL_mattilda_db_**

![Registro de nuevo server.](img_docs/pgadmin_2_creaciondb.jpeg)

Posteriormente, en la pestaña de **Connection**, llenamos los datos con los que hemos especificado en el **docker compose** para realizar la conexión.
> **Host name/address = local_pgdb_admin** (que es el container name de nuestra bd en el archivo docker-compose)

> **Username y Password = toor** (que son los valores POSTGRES_USER y POSTGRES_PASSWORD en el archivo docmer-compose)

![Registro de conexión.](img_docs/pgadmin_3_registerdb.jpeg
)

Si todo ha salidos bien, debemos de ser capaces de ver la base de datos **toor** entre las bases de datos (guiño a tor browser).

![base de datos creada.](img_docs/pgadmin_4_db.jpeg)

> La URL de las bases de datos en PostgreSQL se compone de la siguiente manera:
> **"postgresql://USERNAME:PASSWORD@localhost:5432/NAME_DB"**

> Sin embargo, como estamos utilizando contenedores, en lugar de localhost, debe ir el nombre del contenedor de la base de datos, quedando de la siguiente forma de acuerdo a nuestro contenedor: **"postgresql://toor:toor@db:5432/toor"**


<h1 id="er">Creación del diagrama ER para la base de datos</h1>

## Diccionario de datos utilizado para la base de datos

- **Tipo de base de datos:** Relacional.
- **Sistema de base de datos:** PostgreSQL.

## Estructura de las tablas

### colegios

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | VARCHAR(36) | 🔑 PK, not null, unique |  |Identificador único del colegio. |
| **clave_cct** | VARCHAR(20) | not null, unique |  |Clave de centro de trabajo. Valor único en México.  |
| **nombre** | VARCHAR(255) | not null |  |Nombre oficial de la escuela. |
| **nivel_educativo** | VARCHAR(50) | not null |  |Opciones: Preescolar, Primaria, Secundaria, Universidad. |
| **calle** | VARCHAR(255) | null |  |Dirección: Calle y Número. |
| **colonia** | VARCHAR(255) | null |  |Colonia o barrio.  |
| **municipio** | VARCHAR(100) | null |  |Municipio o alcaldía. |
| **estado** | VARCHAR(100) | null |  |Estado de la república. |
| **codigo_postal** | VARCHAR(10) | null |  |Código postal. |
| **latitud** | DECIMAL(9,6) | not null |  |Coordenada geográfica. |
| **longitud** | DECIMAL(9,6) | not null |  |Coordenada geográfica. |
| **telefono** | VARCHAR(20) | null |  |Teléfono de contacto. |
| **correo_electronico** | VARCHAR(100) | not null, unique |  |Correo de contacto oficial. |
| **nombre_director** | VARCHAR(255) | not null |  |Nombre del director o responsable. |
| **turno** | VARCHAR(20) | not null |  |Opciones: Matutino, Vespertino, Mixto. |
| **estatus** | VARCHAR(20) | not null |  |Opciones: Activa, Suspendida, Cerrada. |


### estudiantes

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | VARCHAR(36) | 🔑 PK, not null, unique |  |Identificador único del estudiante. |
| **nombre** | VARCHAR(100) | not null |  |Nombre completo del estudiante. |
| **apellido_paterno** | VARCHAR(100) | not null |  |Apellido paterno del estudiante. |
| **apellido_materno** | VARCHAR(100) | not null |  |Apellido materno del estudiante. |
| **fecha_nacimiento** | DATE | not null |  |Fecha de nacimiento del estudiante. |
| **genero** | VARCHAR(20) | not null |  |Genero del estudiante. Opciones: Femenino, Masculino, Otro. |
| **curp** | VARCHAR(18) | not null |  |Identificación única en México. |
| **fecha_inscripcion** | DATE | not null |  |Fecha en que es inscribió el estudiante. |
| **grado_escolar** | VARCHAR(50) | not null |  |Grado escolar actual del estudiante. |
| **especialidad** | VARCHAR(255) | null |  |Especialidad del estudiante. |
| **promedio_general** | DECIMAL(2,2) | not null |  |Promedio general del estudiante. |
| **carrera** | VARCHAR(150) | null |  |Carrera del estudiante. |
| **id_escuela** | VARCHAR(36) | not null, unique | fk_estudiantes_id_escuela_colegios |Clave foránea. Identificador único de un colegio.  |


### facturas

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | VARCHAR(36) | 🔑 PK, not null, unique |  |Identificador único de una factura.  |
| **fecha_emision** | DATE | not null |  |Fecha de emisión de la factura.  |
| **fecha_vencimiento** | DATE | not null |  |Fecha de vencimiento de la factura. |
| **concepto** | VARCHAR(255) | not null |  |Concepto de la factura.  |
| **monto** | DECIMAL(10,2) | not null |  |Monto de la factura. |
| **monto_pagado** | DECIMAL(10,2) | not null |  |Monto pagado de la factura. |
| **estatus** | VARCHAR(20) | not null |  |Estado de la factura. Opciones: Pendiente, Pagada, Vencida. |
| **id_estudiante** | VARCHAR(36) | not null, unique | fk_facturas_id_estudiante_estudiantes |Clave foránea. Identificador único de un estudiante. |


### pagos

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | VARCHAR(36) | 🔑 PK, not null, unique |  |Identificador único de un pago parcial o completo para una factura. |
| **fecha_pago** | DATE | not null |  |Fecha en que se realizo el pago.  |
| **monto_pagado** | DECIMAL(10,2) | not null |  |Monto del pago abonado hacia la factura. |
| **metodo_pago** | VARCHAR(50) | not null |  |Método para realizar el pago. Opciones: Efectivo, Tarjeta, Transferencia. |
| **referencia_pago** | VARCHAR(70) | not null |  |Referencia del pago.  |
| **id_factura** | VARCHAR(36) | not null, unique | fk_pagos_id_factura_facturas |Clave foránea. Identificador único de la factura asociada al pago.  |
| **cuenta_beneficiaria** | VARCHAR(25) | not null |  |CLABE, tarjeta de débito o número de celular. |
| **institucion_emisora** | VARCHAR(100) | null |  |Institución emisora del pago. |
| **institucion_receptora** | VARCHAR(100) | not null |  |Institución receptora del pago. |



## Relaciones

- **estudiantes a colegios**: 1:N - Un estudiante solo puede estar inscrito en un colegio, pero un colegio puede tener N estudiantes inscritos.
- **facturas a estudiantes**: 1:N - Una factura solo puede pertenecer a un estudiante, pero un estudiante puede tener múltiples facturas.
- **pagos a facturas**: N:1 - Una factura puede tener muchos pagos (abonos) que en conjunto suman el total de la factura pero un pago solo puede pertenecer a una factura.


## Diagrama de la base de datos

![Registro de conexión.](img_docs/Diagrama_ER_mattilda.png)

### Notas sobre el diseño del diagrama ER de la base de datos

- Se ha elegido utilizar un id del tipo UUID4 como primary key en lugar de un tipo INT autoincremental, con la finalidad de mitigar un posible ataque Insecure Direct Object Reference ([IDOR | CWE-639](https://cwe.mitre.org/data/definitions/639.html)) al momento de consultar los registros mediante la API.
- Se ha añadido una cuarta tabla (pagos) además de las principales, esto con la finalidad de permitir al estudiante los pagos parciales hacía sus facturas.
- Notese que los datos útilizados en la tabla pagos, son los minimos necesarios para emitir el Comprobante Electrónico de Pago en México (CEP).
![Rastreo banco de méxico.](img_docs/banco_mex_rastreo.png)
