---

---

Creación de un Entorno Local de Desarrollo

- Introducción

  Este documento proporciona una guía detallada para configurar un entorno de desarrollo local para el proyecto "reto_final_python". El objetivo es facilitar la integración y contribución eficiente de nuevos miembros al equipo, permitiendo la validación de nuevas características y la ejecución de pruebas unitarias en un entorno local.
- Configuración del Entorno Local

  Antes de comenzar, asegúrese de tener instalado lo siguiente:

  - Docker: [Guía de Instalación](https://docs.docker.com/get-docker/)
  - Docker Compose: [Guía de Instalación](https://docs.docker.com/compose/install/)
  - Docker Desktop (para usuarios de Windows y Mac): [Guía de Instalación](https://docs.docker.com/desktop/)
  - Git: [Guía de Instalación](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
  - PostgreSQL: [Guía de Instalación](https://www.postgresql.org/download/)

  PARA DESARROLLADORES

  1. Clonación del Repositorio

     · Utilice el siguiente comando para clonar el repositorio Git que contiene el proyecto:
     git clone https://github.com/IgnacioCantero/reto_final_python

  · Acceda al proyecto:
  cd reto_final_python

  2. Inicie el servicio de PostgreSQL:
     brew services start postgresql

     Nota: Asegúrese de que el servicio PostgreSQL esté en ejecución antes de intentar crear la base de datos y el usuario.
  3. Establezca la variable de entorno 'DATABASE_URI' para apuntar a su base de datos local:
     export DATABASE_URI=postgresql://myuser:mypassword@localhost:5432/mydatabase

     Nota: Esta variable será necesario configurarla cada vez que se inicie una nueva sesión de terminal.
  4. Configuración del Entorno Virtual

     · Para crear y activar un entorno virtual navegue al directorio del proyecto y ejecute:

     - [En Linux/Mac]:
     python3 -m venv venv
     source venv/bin/activate

     - [En Windows (cmd.exe)]:
     python -m venv venv
     venv\Scripts\activate.bat

     - [En Windows (PowerShell)]:
     python -m venv venv
     venv\Scripts\Activate.ps1

     · Instale las dependencias necesarias ejecutando:
     pip install -r requirements.txt

     · Ejecute 'manage.py' para crear las tablas en la DB:
     python3 manage.py

     · Inicie el servicio Flask ejecutando:
     python3 run.py

     · La aplicación ahora estará accesible en 'http://localhost:5001'
  5. Abra una nueva Terminal para interactuar con la DB:

     · Para leer datos existentes (GET) ejecute:
     curl http://localhost:5001/data

     · Para crear nuevos datos (POST) ejecute:
     curl -X POST http://localhost:5001/data -H "Content-Type: application/json" -d '{"name": "Nombre de Prueba"}'

     · Para eliminar datos existentes (DELETE) ejecute:
     curl -X DELETE http://localhost:5001/data/{id}

     Nota: Reemplace {id} con el ID real del registro que deseas eliminar.
  6. Ejecución de Pruebas Unitarias:

     · Ejecute pytest para validar las nuevas características:
     pytest

     · Verifique la cobertura de las pruebas ejecutando:
     coverage run -m pytest

     - Para un reporte de la cobertura de pruebas ejecute:
     coverage report

     - Para un reporte detallado genere uno en HTML que le permitirá ver la cobertura en su navegador ejecutando:
     coverage html
     open htmlcov/index.html
  7. Detenga la aplicación y los servicios una vez finalizado el trabajo ejecutando:
     CTRL + C
  8. Desactive el entorno virtual ejecutando:
     deactivate
- Documentación y Colaboración

  · Arquitectura del Software:
  La aplicación utiliza Flask como framework web, SQLAlchemy para la interacción con la base de datos y estructura MVC para organizar el código.

  · Normas de Colaboración:
  Se sigue un modelo de ramas tipo Trunk-Based Development, donde los cambios se desarrollan en ramas cortas y se integran frecuentemente en la rama principal. Las nuevas características se trabajan en ramas separadas que luego se fusionan a la rama principal mediante Pull Requests.
- Conclusión

  Este entorno de desarrollo local está diseñado para maximizar la eficiencia y facilitar la colaboración dentro del equipo de desarrollo, asegurando que todas las contribuciones mantengan la calidad y coherencia del proyecto.

---

---

Creación de Pipeline de CI

- Introducción

  Este segmento ofrece una guía para configurar un Pipeline de Integración Continua (CI) usando Jenkins, integrado con ngrok y GitHub, para automatizar las pruebas y despliegues de código.
- Configuración de Jenkins

  Antes de comenzar, asegúrese de tener Jenkins instalado y accesible, potencialmente usando ngrok para exponer Jenkins de manera segura desde una red local:

  - Jenkins: [Guía de Instalación](https://www.jenkins.io/doc/book/installing/)
  - Ngrok: [Guía de Instalación](https://ngrok.com/docs/getting-started/)

  PARA DESARROLLADORES

  1. Jenkins:

     · Cree un nuevo Pipeline.

     · En la sección "Build Triggers" marque la casilla "GitHub hook trigger for GITScm polling"

     · En la sección "Pipeline":

     - Elija "Pipeline script from SCM" y seleccione "Git" como SCM.
     - Ingrese la URL del repositorio (https://github.com/IgnacioCantero/reto_final_python) y configure las credenciales.
     - En "Branches to build" escriba "*/main"
     - En "Script Path" escriba "Jenkinsfile"

     · Guarde la configuración.
  2. Ngrok:

     · Para la primera vez:

     - Inicie sesión en ngrok (https://dashboard.ngrok.com/login) y copie su "Authtoken"
     - Done permisos de ejecución al ejecutable:
       chmod +x ngrok
     - Instale su "Authtoken" copiado:
       ./ngrok authtoken Authtoken
     - Para permitir ejecutar ngrok desde cualquier directorio en la terminal sin especificar la ruta completa, mueva el ejecutable de ngrok a una ubicación en su PATH:
       mv ngrok /usr/local/bin

     · Ejecute ngrok con el puerto del servidor de Jenkins (por defecto 8080):
     ngrok http 8080

     · Copie la URL pública generada.
  3. GitHub

     · Cree un nuevo Webhook en el repositorio de GitHub

     · Pegue la URL de ngrok en "Payload URL" seguido de "github-webhook/":

     Ejemplo: https://c187-85-48-125-14.ngrok-free.app/github-webhook/

     · En "Content type" seleccione la opción "aplication/json"

     · En "Which events would you like to trigger this webhook?" seleccione "Just the push event"

     · Guarde el Webhook.

     Nota: Actualice el Webhook en GitHub cada vez que reinicie ngrok, ya que su URL pública cambiará (plan gratuito). Se ofrecen planes de pago que permiten usar URLs personalizadas y reservadas que no cambian cada vez que se reinicia ngrok.
- Comprobación:

  1. Haga cambios en el proyecto, guárdelos y haga commit y push a GitHub para activar el pipeline:
     git add .
     git commit -m "Update repository"
     git push

     Nota: Podrá comprobar desde la terminal de Jenkins cómo se ejecuta un nuevo job del Pipeline creado.
  2. Descargue la imagen Docker actualizada desde DockerHub ejecutando:
     docker pull ignaciocantero/reto_final_python:0.0.1
  3. Inicie la aplicación con Docker Compose ejecutando:
     docker-compose up
  4. Acceda a la base de datos ejecutando:
     docker exec -it reto_final_python-db-1 psql -U myuser -d mydatabase
  5. Interactúe con la DB usando comandos de psql:

     · Liste todas las tablas:
     \dt

     · Consulte un registro:
     SELECT * FROM personas;

     · Consulte un registro por ID:
     SELECT * FROM personas WHERE id = 1;

     · Actualice un registro:
     UPDATE personas SET nombre = 'Ana', apellido = 'López', telefono = '987654321' WHERE id = 1;

     · Elimine un registro por ID:
     DELETE FROM personas WHERE id = 1;

     · Elimine una tabla:
     DROP TABLE personas;

     · Salga:
     exit
- Conclusión

  Con esta configuración, cada vez que se produzca un cambio (push) en el repositorio de GitHub, se ejecutará un job del pipeline de Jenkins.
