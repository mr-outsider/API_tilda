# Mattilda API - Prueba Técnica

<h1 id="indice">Indice</h1>

- [Vista General](#vista_general)
- [¿Cómo correr este proyecto?](#run_project)


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
