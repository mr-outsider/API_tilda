# Mattilda API - Prueba Técnica

<h1 id="indice">Indice</h1>

- [Vista General](#vista_general)
- [¿Cómo correr este proyecto?](#run_project)
- [Creación del diagrama ER](#er)
- - [Notas sobre el diagrama ER](#notesER)
- [Consumir endpoints](#endpoints)
- -  [Health Check Endpoint](#health)
- - [Colegio](#school)
- - [Estudiantes](#students)
- - [Facturas](#invoices)
- [Anexo](#anexo)
- - [Ejecución de linting](#linting)
- - [Ejecución de pruebas unitarias](#test)
- - [Pendientes en el desarrollo y mejoras](#pending)

<h1 id="fin">Vista General</h1>

Proyecto realizado para llevar a cabo la prueba técnica de Mattilda. Aquí encontrará el proceso para llevar a cabo el levantamiento del proyecto para validar su función. Así como observaciones, mejoras y decisiones técnicas tomadas durante el desarrollo.

<h1 id="run_project">¿Cómo correr este proyecto?</h1>

> NOTA: Si no quieres levantar el proyecto para probarlo en local. Puedes consumir la API directamente desde Internet. Pasa al apartado: **[Consumir endpoints](#endpoints)** para ver cómo hacerlo.

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

4. **Creación de tablas y populación de información**

TODO: Generar un script para crear las tablas y cargar información de prueba.

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
| **calle** | VARCHAR(255) |  |  |Dirección: Calle y Número. |
| **colonia** | VARCHAR(255) |  |  |Colonia o barrio.  |
| **municipio** | VARCHAR(100) |  |  |Municipio o alcaldía. |
| **estado** | VARCHAR(100) |  |  |Estado de la república. |
| **codigo_postal** | VARCHAR(10) |  |  |Código postal. |
| **latitud** | DECIMAL(9,6) | null |  |Coordenada geográfica. |
| **longitud** | DECIMAL(9,6) | null |  |Coordenada geográfica. |
| **telefono** | VARCHAR(20) | null |  |Teléfono de contacto. |
| **correo_electronico** | VARCHAR(100) | not null, unique |  |Correo de contacto oficial. |
| **nombre_director** | VARCHAR(255) | not null |  |Nombre del director o responsable. |
| **turno** | VARCHAR(20) | not null |  |Opciones: Matutino, Vespertino, Mixto. |
| **estatus** | VARCHAR(20) | not null |  |Opciones: activa, suspendida, cerrada. |


### estudiantes

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | VARCHAR(36) | 🔑 PK, not null, unique |  |Identificador único del estudiante. |
| **nombre** | VARCHAR(100) | not null |  |Nombre completo del estudiante. |
| **apellido_paterno** | VARCHAR(100) | not null |  |Apellido paterno del estudiante. |
| **apellido_materno** | VARCHAR(100) | not null |  |Apellido materno del estudiante. |
| **fecha_nacimiento** | DATE | not null |  |Fecha de nacimiento del estudiante. |
| **genero** | VARCHAR(20) | not null |  |Genero del estudiante. Opciones: femenino, masculino, otro. |
| **curp** | VARCHAR(18) | not null, unique |  |Identificación única en México. |
| **fecha_inscripcion** | DATE | not null |  |Fecha en que es inscribió el estudiante. |
| **grado_escolar** | VARCHAR(50) | not null |  |Grado escolar actual del estudiante. |
| **especialidad** | VARCHAR(255) | null |  |Especialidad del estudiante. |
| **promedio_general** | DECIMAL(4,2) | null |  |Promedio general del estudiante. |
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
| **monto_pagado** | DECIMAL(10,2) | not null, default 0.00 |  |Monto pagado de la factura. |
| **estatus** | VARCHAR(20) | not null, default "pendiente" |  |Estado de la factura. Opciones: pendiente, pagada, vencida. |
| **id_estudiante** | VARCHAR(36) | not null, unique | fk_facturas_id_estudiante_estudiantes |Clave foránea. Identificador único de un estudiante. |


### pagos

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | VARCHAR(36) | 🔑 PK, not null, unique |  |Identificador único de un pago parcial o completo para una factura. |
| **fecha_pago** | DATE | not null |  |Fecha en que se realizo el pago.  |
| **monto_pagado** | DECIMAL(10,2) | not null |  |Monto del pago abonado hacia la factura. |
| **metodo_pago** | VARCHAR(50) | not null |  |Método para realizar el pago. Opciones: efectivo, tarjeta, transferencia. |
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


<h2 id="notesER">Notas sobre el diseño del diagrama ER de la base de datos</h2>

[back to index](#indice)

- Se ha elegido utilizar un id del tipo UUID4 como primary key en lugar de un tipo INT autoincremental, con la finalidad de mitigar un posible ataque Insecure Direct Object Reference ([IDOR | CWE-639](https://cwe.mitre.org/data/definitions/639.html)) al momento de consultar los registros mediante la API.
- Se ha añadido una cuarta tabla (pagos) además de las principales, esto con la finalidad de permitir al estudiante los pagos parciales hacía sus facturas.
- Notese que los datos útilizados en la tabla pagos, son los minimos necesarios para emitir el Comprobante Electrónico de Pago en México (CEP).
![Rastreo banco de méxico.](img_docs/banco_mex_rastreo.png)
- Se ha obtado por añadir la tabla (pagos) para que con los datos, la persona interesada pueda obtener el CEP directamente en el Banco de México. Esto con la finalidad de evitar cargar
documentos y mitigar una posible vulnerabilidad: Local File Inclusion ([LFI | CWE-98](https://cwe.mitre.org/data/definitions/98.html))

<h1 id="endpoints">Consumir endpoints</h1>

[back to index](#indice)


El entorno consta de 3 CRUDS: Schools, Students, Invoices. Vamos a abordar primero Schools para ver
cómo consumir el servicio y qué podemos esperar en las respuestas.

Para probar en local:
**BASE_URL = localhost:8000**

Para probar online:
**BASE_URL = http://35.89.147.184**

<h2 id="health">Health Check Endpoint</h2>

### Método: GET

### URL: {{BASE_URL}}/health-check

### Query Params: N/A

### Body: N/A

### **Response - Status Code: 200**

```json
{
    "status": "Establish connection - OK"
}
```

### **Repsonse - Status Code: 400**
```json
{
    "status": "Bad response - Connection Fail"
}
```
---

<h2 id="school">Colegio</h2>

[back to index](#indice)

### Método: POST

### URL: {{BASE_URL}}/v1/schools

### Query Params: N/A

### Body

```json
{
    "clave_cct": "CCT1234567000",
    "nombre": "Instituto Educativo Test",
    "nivel_educativo": "Primaria",
    "calle": "Av. Viva 742",
    "colonia": "Centro",
    "municipio": "Cuernavaca",
    "estado": "Morelos",
    "codigo_postal": "62000",
    "latitud": 18.918972,
    "longitud": -99.234123,
    "telefono": "7771234567",
    "correo_electronico": "contacto@institutoTest.edu.mx",
    "nombre_director": "María LL",
    "turno": "Matutino",
    "estatus": "activa"
}
```

### **Response - Status Code: 201**
Registro creado de manera exitosa.

```json
{
    "status": "success",
    "pagination": {
        "next": null,
        "previous": null,
        "total_pages": 1,
        "current_page": 1
    },
    "body": [
        {
            "id": "8c20fe9c-7cd1-4768-a44a-74a022e6ec14",
            "clave_cct": "CCT1234567000",
            "nombre": "Instituto Educativo Test",
            "nivel_educativo": "Primaria",
            "calle": "Av. Viva 742",
            "colonia": "Centro",
            "municipio": "Cuernavaca",
            "estado": "Morelos",
            "codigo_postal": "62000",
            "latitud": 18.918972,
            "longitud": -99.234123,
            "telefono": "7771234567",
            "correo_electronico": "contacto@institutoTest.edu.mx",
            "nombre_director": "María LL",
            "turno": "Matutino",
            "estatus": "activa"
        }
    ]
}
```

### **Response - Status Code: 400**
Caso donde el registro ya se encuentra en la base de datos.

```json
{
    "status": "error",
    "error": "School 'CCT1234567890' already exist!"
}
```
---

[back to index](#indice)

### Método: GET

### URL: {{BASE_URL}}/v1/schools

### Query Params:
- id (str): 9ddae72d-a9f3-40bb-b2a4-3de86fa403cb [Ejemplo]
- clave_cct (str): CCT1234567890 [Ejemplo]
- nombre (str): Montesori [Ejemplo]
- nivel_educativo (str): Universidad [Ejemplo] - Opciones: Preescolar, Primaria, Secundaria, Universidad.
- turno (str): Matutino [Ejemplo] - Opciones: Matutino,Vespertino, Mixto.
- estatus (str): activa [Ejemplo] - Opciones: activa, suspendida, cerrada.
- correo_electronico (str): school@email.com [Ejemplo]


### Body: N/A

### **Response - Status Code: 200**


```json
{
    "status": "success",
    "pagination": {
        "total": 1,
        "next": null,
        "previous": null,
        "total_pages": 1,
        "current_page": 1
    },
    "body": [
        {
            "id": "8c20fe9c-7cd1-4768-a44a-74a022e6ec14",
            "clave_cct": "CCT1234567890",
            "nombre": "Instituto Educativo del Valle",
            "nivel_educativo": "Primaria",
            "calle": "Av. Siempre Viva 742",
            "colonia": "Centro",
            "municipio": "Cuernavaca",
            "estado": "Morelos",
            "codigo_postal": "62000",
            "latitud": 18.918972,
            "longitud": -99.234123,
            "telefono": "7771234567",
            "correo_electronico": "contacto@institutovalle.edu.mx",
            "nombre_director": "María López Hernández",
            "turno": "Matutino",
            "estatus": "activa"
        }
    ]
}
```

### **Response - Status Code: 400**
Caso donde se usa una opción no válida en uno de los filtros.

```json
{
    "status": "error",
    "error": "nivel_educativo 'Kinder' is not a valid option. Please select a value in: ['Preescolar', 'Primaria', 'Secundaria', 'Universidad']"
}
```

---

[back to index](#indice)

### Método: DELETE

### URL: {{BASE_URL}}/v1/schools/{{identificador}}

- identificador (str): Puede ser el uuid o la clave_cct de la escuela en cuestión.

### Query Params: N/A


### Body: N/A

### **Response - Status Code: 200**


```json
{
    "status": "success",
    "message": "School 'CCT1234567890' deleted OK!",
    "pagination": {
        "total": 1,
        "next": null,
        "previous": null,
        "total_pages": 1,
        "current_page": 1
    },
    "body": []
}
```

### **Response - Status Code: 400**
Caso donde el registro ya fue eliminado o no se encontró en la base de datos.

```json
{
    "status": "error",
    "error": "School 'CCT1234567890' was not deleted! Please check if the register exist."
}
```

---

[back to index](#indice)

### Método: PATCH

### URL: {{BASE_URL}}/v1/schools/{{identificador}}

- identificador (str): Puede ser el uuid o la clave_cct de la escuela en cuestión.

### Query Params: N/A

### Body:
```json
{
    "nombre": "Name", #Optional [str]
    "calle": "Street", # Optional [str]
    "colonia": "Neighboor", # Optional [str]
    "municipio": "Municipality", # Optional [str]
    "estado": "State", # Optional [str]
    "codigo_postal": "Postal Code", # Optional [str]
    "latitud": "Latitude", # Optional [float]
    "longitud": "Longitude", # Optional [float]
    "telefono": "Phone", # Optional [str]
    "correo_electronico": "Email", # Optional [str]
    "nombre_director": "Director Name", # Optional [str]
    "turno": "Mixto", # Optional [str] Valid Options: "Matutino", "Vespertino", "Mixto".
    "estatus": "cerrada", # Optional [str] Valid Options: "activa", "suspendida", "cerrada".

}

```

### **Response - Status Code: 200**


```json
{
    "status": "success",
    "pagination": {
        "total": 1,
        "next": null,
        "previous": null,
        "total_pages": 1,
        "current_page": 1
    },
    "body": [
        {
            "id": "620fd39c-fb19-420f-a9c6-c05a1f4247d7",
            "clave_cct": "CCT1234567890",
            "nombre": "Instituto Educativo Del Valle",
            "nivel_educativo": "Primaria",
            "calle": "Av. Siempre Viva 742",
            "colonia": "Centro",
            "municipio": "Cuernavaca",
            "estado": "Morelos",
            "codigo_postal": "62000",
            "latitud": 18.918972,
            "longitud": -99.234123,
            "telefono": "7771234567",
            "correo_electronico": "contacto@institutovalle.edu.mx",
            "nombre_director": "María López Hernández",
            "turno": "Mixto",
            "estatus": "cerrada"
        }
    ]
}
```

### **Response - Status Code: 400**
Caso donde el registro no fue encontrado en la base de datos.

```json
{
    "status": "error",
    "error": "School 'CCT12345678900' does not exist!"
}
```
---

<h2 id="students">Estudiantes</h2>

[back to index](#indice)

### Método: POST

### URL: {{BASE_URL}}/v1/schools/:identificador/student

- identificador (str): Se refiere a la clave_cct de la escuela en cuestión.

### Query Params: N/A

### Body

```json
{
    "nombre": "Luis",
    "apellido_paterno": "Martínez",
    "apellido_materno": "Gómez",
    "fecha_nacimiento": "2007-05-14",
    "genero": "Masculino",
    "curp": "MAGL070514HDFRMS09",
    "fecha_inscripcion": "2023-08-21",
    "grado_escolar": "3° de Secundaria",
    "especialidad": "Robótica",
    "promedio_general": 9.45,
    "carrera": "Ingeniería en Mecatrónica"
}
```

### **Response - Status Code: 201**
Registro creado de manera exitosa.

```json
{
    "status": "success",
    "pagination": {
        "total": 1,
        "next": null,
        "previous": null,
        "total_pages": 1,
        "current_page": 1
    },
    "body": [
        {
            "id": "2a353798-f153-4a08-9325-e98d4e138b42",
            "nombre": "Luis",
            "apellido_paterno": "Martínez",
            "apellido_materno": "Gómez",
            "fecha_nacimiento": "2007-05-14",
            "genero": "Masculino",
            "curp": "MAGL070514HDFRMS09",
            "fecha_inscripcion": "2023-08-21",
            "grado_escolar": "3° de Secundaria",
            "especialidad": "Robótica",
            "promedio_general": 9.45,
            "carrera": "Ingeniería en Mecatrónica",
            "id_escuela": "620fd39c-fb19-420f-a9c6-c05a1f4247d7"
        }
    ]
}
```

### **Response - Status Code: 400**
Caso donde el registro ya se encuentra en la base de datos.

```json
{
    "status": "error",
    "error": "Student 'MAGL070514HDFRMS09' already exist!"
}
```
---

[back to index](#indice)

### Método: GET

### URL: {{BASE_URL}}/v1/students

### Query Params:
- id (str): 9ddae72d-a9f3-40bb-b2a4-3de86fa403cb [Ejemplo]
- curp (str): MAGL070514HDFRMS09 [Ejemplo]
- genero (str): Masculino [Ejemplo] - Opciones: femenino, masculino, otro
- id_escuela (str): 9ddae72d-a9f3-40ds-b2a4-3de86fa403dsa [Ejemplo]


### Body: N/A

### **Response - Status Code: 200**


```json
{
    "status": "success",
    "pagination": {
        "total": 1,
        "next": null,
        "previous": null,
        "total_pages": 1,
        "current_page": 1
    },
    "body": [
        {
            "id": "2a353798-f153-4a08-9325-e98d4e138b42",
            "nombre": "Luis",
            "apellido_paterno": "Martínez",
            "apellido_materno": "Gómez",
            "fecha_nacimiento": "2007-05-14",
            "genero": "Masculino",
            "curp": "MAGL070514HDFRMS09",
            "fecha_inscripcion": "2023-08-21",
            "grado_escolar": "3° de Secundaria",
            "especialidad": "Robótica",
            "promedio_general": 9.45,
            "carrera": "Ingeniería en Mecatrónica",
            "id_escuela": "620fd39c-fb19-420f-a9c6-c05a1f4247d7"
        }
    ]
}
```

### **Response - Status Code: 400**
Caso donde no se encuentra el registro con los filtros útilizados.

```json
{
    "status": "success",
    "pagination": {
        "total": 0,
        "next": null,
        "previous": null,
        "total_pages": 1,
        "current_page": 1
    },
    "body": []
}
```

---

[back to index](#indice)

### Método: DELETE

### URL: {{BASE_URL}}/v1/students/{{identificador}}

- identificador (str): Puede ser el uuid o la curp del estudiante en cuestión.

### Query Params: N/A


### Body: N/A

### **Response - Status Code: 200**


```json
{
    "status": "success",
    "message": "Student '2a353798-f153-4a08-9325-e98d4e138b42' deleted OK!",
    "pagination": {
        "total": 1,
        "next": null,
        "previous": null,
        "total_pages": 1,
        "current_page": 1
    },
    "body": []
}
```

### **Response - Status Code: 400**
Caso donde el registro ya fue eliminado o no se encontró en la base de datos.

```json
{
    "status": "error",
    "error": "Student '2a353798-f153-4a08-9325-e98d4e138b42' was not deleted! Please check if the register exist."
}
```

---

[back to index](#indice)

### Método: PATCH

### URL: {{BASE_URL}}/v1/students/{{identificador}}

- identificador (str): Puede ser el uuid o la curp del estudiante en cuestión.

### Query Params: N/A

### Body:
```json

{
    "grado_escolar": "6to semestre", #Optional [str]
    "especialidad": "Ciencias", #Optional [str]
    "promedio_general": 8.9, #Optional [float]
    "carrera": "Ciencias de computación" #Optional [str]
    "id_escuela": "620fd39c-fb19-420f-a9c6-c05a1f4247d7" #Optional [str]
}

```

### **Response - Status Code: 200**


```json
{
    "status": "success",
    "pagination": {
        "total": 1,
        "next": null,
        "previous": null,
        "total_pages": 1,
        "current_page": 1
    },
    "body": [
        {
            "id": "14f8e910-2737-4bb6-872f-810a21eb6511",
            "nombre": "Luis",
            "apellido_paterno": "Martínez",
            "apellido_materno": "Gómez",
            "fecha_nacimiento": "2007-05-14",
            "genero": "masculino",
            "curp": "MAGL070514HDFRMS09",
            "fecha_inscripcion": "2023-08-21",
            "grado_escolar": "6to semestre",
            "especialidad": "Ciencias",
            "promedio_general": 8.9,
            "carrera": "Ciencias de computación",
            "id_escuela": "620fd39c-fb19-420f-a9c6-c05a1f4247d7"
        }
    ]
}
```

### **Response - Status Code: 400**
Caso donde el registro no fue encontrado en la base de datos.

```json
{
    "status": "error",
    "error": "Student 'MAGL070514HDFRMS01' does not exist!"
}
```

### **Response - Status Code: 400**
Caso donde el identificador del estudiante no es válido.

```json
{
    "status": "error",
    "error": "length student id 'MAGL070514HDFRMS011' is not valid!"
}
```
---

<h2 id="invoices">Facturas</h2>

[back to index](#indice)

### Método: POST

### URL: {{BASE_URL}}/v1/students/:identificador/invoice

- identificador (str): Se refiere a la CURP del estudiante en cuestión.

### Query Params: N/A

### Body

```json
{
  "fecha_emision": "2025-07-01",
  "fecha_vencimiento": "2025-07-31",
  "concepto": "Pago mensualidad julio",
  "monto": 1500.00
}
```

### **Response - Status Code: 201**
Registro creado de manera exitosa.

```json
{
    "status": "success",
    "pagination": {
        "total": 1,
        "next": null,
        "previous": null,
        "total_pages": 1,
        "current_page": 1
    },
    "body": [
        {
            "id": "67a6ba83-447e-45cd-b02f-d675446770c4",
            "fecha_emision": "2025-07-01",
            "fecha_vencimiento": "2025-07-31",
            "concepto": "Pago mensualidad julio",
            "monto": 1500.0,
            "monto_pagado": 0.0,
            "estatus": "pendiente",
            "id_estudiante": "14f8e910-2737-4bb6-872f-810a21eb6511"
        }
    ]
}
```

### NOTA

Dado que una factura como tal no se puede repetir, en el sentido de que no podemos tomar dos
facturas que sean iguales como las mismas porque ambas pueden significar dos prestamos
diferentes. En este caso lo que se debe de hacer es el uso del cache. Para evitar que al momento de crear, presionando dos veces el botón de "crear" en un intervalo de tiempo menor a un minuto, se creen dos facturas similares. En su lugar, el cache nos ayudará a evitar este tipo de casos.

NOTA: No he podido implementarlo por falta de tiempo.

---

[back to index](#indice)

### Método: GET

### URL: {{BASE_URL}}/v1/invoices

### Query Params:
- id (str): 9ddae72d-a9f3-40bb-b2a4-3de86fa403cb [Ejemplo]
- estatus (str): MAGL070514HDFRMS09 [Ejemplo] - Opciones: pendiente, pagada vencida
- id_estudiante (str): 9ddae72d-a9f3-40ds-b2a4-3de86fa403dsa [Ejemplo]


### Body: N/A

### **Response - Status Code: 200**


```json
{
    "status": "success",
    "pagination": {
        "total": 2,
        "next": null,
        "previous": null,
        "total_pages": 1,
        "current_page": 1
    },
    "body": [
        {
            "id": "2db48953-a1de-4768-ac5f-c2f4122583e0",
            "fecha_emision": "2025-07-01",
            "fecha_vencimiento": "2025-07-31",
            "concepto": "Pago mensualidad julio",
            "monto": 1500.0,
            "monto_pagado": 0.0,
            "estatus": "pendiente",
            "id_estudiante": "14f8e910-2737-4bb6-872f-810a21eb6511"
        },
        {
            "id": "8f5be063-65cb-4113-995a-acdb8c46ae71",
            "fecha_emision": "2025-07-02",
            "fecha_vencimiento": "2025-07-31",
            "concepto": "Pago mensualidad julio 2",
            "monto": 1500.0,
            "monto_pagado": 0.0,
            "estatus": "pendiente",
            "id_estudiante": "14f8e910-2737-4bb6-872f-810a21eb6511"
        }
    ]
}
```

### **Response - Status Code: 400**
Caso donde se usa una opción no válida para el filtro 'estatus'.

```json
{
    "status": "error",
    "error": "estatus 'pagados' is not a valid option. Please select a value in: ['pendiente', 'pagada', 'vencida']"
}
```

---

[back to index](#indice)

### Método: DELETE

### URL: {{BASE_URL}}/v1/invoices/{{identificador}}

- identificador (str): Es el uuid de la factura en cuestión.

### Query Params: N/A


### Body: N/A

### **Response - Status Code: 200**


```json
{
    "status": "success",
    "message": "Invoice '8f5be063-65cb-4113-995a-acdb8c46ae71' deleted OK!",
    "pagination": {
        "total": 1,
        "next": null,
        "previous": null,
        "total_pages": 1,
        "current_page": 1
    },
    "body": []
}
```

### **Response - Status Code: 400**
Caso donde el registro ya fue eliminado o no se encontró en la base de datos.

```json
{
    "status": "error",
    "error": "Invoice '8f5be063-65cb-4113-995a-acdb8c46ae71' was not deleted! Please check if the register exist."
}
```

---

[back to index](#indice)

### Método: PATCH

### URL: {{BASE_URL}}/v1/invoices/{{identificador}}

- identificador (str): Es el uuid de la factura en cuestión.

### Query Params: N/A

### Body:
```json

{
    "fecha_emision": "2025-07-10", # Optional [date] YYYY-MM-DD
    "estatus": "vencida", # Optional [str] - Options: pendiente, pagada, vencida
    "monto_pagado": 200, # Optional [float]
    "concepto": "pruebas" # Optional [str]
}

```

### **Response - Status Code: 200**


```json
{
    "status": "success",
    "pagination": {
        "total": 1,
        "next": null,
        "previous": null,
        "total_pages": 1,
        "current_page": 1
    },
    "body": [
        {
            "id": "2db48953-a1de-4768-ac5f-c2f4122583e0",
            "fecha_emision": "2025-07-10",
            "fecha_vencimiento": "2025-07-31",
            "concepto": "pruebas",
            "monto": 1500.0,
            "monto_pagado": 200.0,
            "estatus": "vencida",
            "id_estudiante": "14f8e910-2737-4bb6-872f-810a21eb6511"
        }
    ]
}
```

### **Response - Status Code: 400**
Caso donde el monto_pagado es mayor al monto de la factura.

```json
{
    "status": "error",
    "error": "monto_pagado [2000.0] is greater than monto_total [1500.00]"
}
```

### **Response - Status Code: 400**
Caso donde el identificador del estudiante no es válido.

```json
{
    "status": "error",
    "error": "Invoice '2db48953-a1de-4768-ac5f-c2f4122583e1' does not exist!"
}
```
---

<h1 id="anexo">Anexo</h1>

[back to index](#indice)

<h2 id="linting">Ejecución del linting</h2>

```bash
pre-commit run --all-files
```
![Linting.](img_docs/linting.png
)

<h2 id="test">Ejecución de test unitarios</h2>

```bash

poetry run pytest

# Para ejecutar test y coverage
poetry run pytest --cov=src
```

![Testing.](img_docs/testing.png
)

<h2 id="pending">Pendientes en el desarrollo y mejoras</h2>

[back to index](#indice)


- Implementación de CRUD para la tabla de pagos.
- Endpoint Estado de Cuenta Colegio: Utilizar una lógica similar al GET, pero filtrando a partir de la tabla facturas mediante un join. Apartir de las facturas, obtener los estudiantes de una escuela determinada.
- Endpoint Estado de Cuenta del Estudiante: Filtrado mediante ID del estudiante, sumar los montos de las facturas y restar la suma de los abonos de las facturas.
- Obtener más información haciendo uso de la tabla pagos, la tabla que fue añadida para llevar un control de los pagos parciales que realiza el estudiante.
- Más filtros en los endpoints GET.
- Añadir más test unitarios.
- Añadir pruebas de estres.
- Realizar pruebas de seguridad OWASP TOP 10 para API.
- Implementación de un gestor de errores como Sentry.
- Mejorar la documentación generada por Swagger.
- Archivo Make para automatizar el levantamiento del proyecto y reducir algunos pasos manuales.
- Mejorar la corrida de test para ejecutar mediante archivo MAKE.
- Mejorar el manejo de errores para estandarizar la respuesta de errores.
- Script para cargar datos de prueba en la BD.
- Implementar la paginación.
- Implementar uso de Caché.
- Subir el coverage al menos a un 85%.
