# Mini mattilda (Carlos Silva)

## Descripción

Mini Mattilda es una app web que te qyudará a gestionar escuelas, alumnos y sus cuentas pendientes

Esta construida usando:

- Docker y Docker compose
- Python 3.11
- FastAPI como framework REST para el manejo de peticiones HTTP
- SQLModel como ORM
- Poetry para el manejo de dependencias y ambientes virtuales
- PostgreSQL como base de datos
- Redis para el almacenamiento de cache
- y Next.js para el frontend

## Los modelos

Estos son los modelos implementados

### Schools

Representan las instituciones educativas

```python
class SchoolBase(SQLModel):
  id: int
  address: Optional[str]
  city: Optional[str]
  email: Optional[str]
  name: str
  phone: Optional[str]
  sid: str # School ID for internal recognition purposes
  state: Optional[str]
  zip_code: Optional[str]
  website: Optional[str]
  created_at: datetime.datetime
  updated_at: datetime.datetime
```

### Students

Representan los estudiantes de las escuelas

```python
class StudentBase(SQLModel):
  id: int
  email: Optional[str]
  first_name: str
  last_name: Optional[str]
  phone: Optional[str]
  sid: str
  created_at: datetime.datetime
  updated_at: datetime.datetime
```

### Invoices

Representan las facturas de los estudiantes, cada una está relacionada con un estudiante y una escuela

```python
class InvoiceBase(SQLModel):
  amount: int
  date: datetime.datetime
  due_date: datetime.datetime
  description: Optional[str]
  school_id: int
  student_id: int
  status: InvoiceStatus # "unpaid", "paid" o "cancelled"
```

### Inscriptions

Representa la relación que tiene una escuela con el estudiante
De esta manera es posible relacionar fácilmente a un estudiante con varias escuelas a la vez

```python
class InscriptionBase(SQLModel):
  id: int
  status: InvoiceStatus # "active" o "inactive"
  student_id: int = Field(foreign_key="student.id")
  school_id: int = Field(foreign_key="school.id")
  created_at: datetime.datetime
  updated_at: datetime.datetime
```

### sid

Las entidades School y Student cuenta con un campo "sid" este campo esta pensado para que sea usado como un identificador interno, podría compararlo con la forma en que los RFCs trabajan en México pero mas legibles
Esto con el objetivo de tener un identificador mas amigable para los agentes humanos, según mi experiencia este identificador puede agilizar varios procesos, quedaría pendiente ver como escala

## Como se inicia?

El proyecto cuenta con un docker compose que levanta todos los servicios necesrios, por lo que solo es necesario contar con `docker` instalado

Se puede iniciar el proyecto con el siguiente comando

```bash
docker compose up
```

Si se desea hacer modificaciones se puede usar en modo "watch" para ver los cambios reflejados al guardar usando el siguiente comando

```bash
docker compose watch
```

Esto levantará los servicios necesarios (PostgreSQL, Redis, Guvicorn para FastAPI y Next)

Una vez desplegado, se podra acceder atravez de localhost a cada componente del proyecto

- `localhost:8000`: API
- `localhost:8000/docs`: API docs
- `localhost:8000/redoc`: API docs alternativos
- `localhost:3000`: Next front-end

## Cómo correr las pruebas del API?

La forma mas fácil de correr los test es usando docker también.

Se puede usar el siguiente comando para correr las pruebas dentro del contenedor (el contenedor debe encontrase activo para poder ejecutar las pruebas en el)

```bash
docker exec mini_mattilda_api pytest
```

También se puede correr fuera del docker si se desea, pero es necesario tener el docker corriendo o un servidor de redis local en el puerto 6379

para correrlo fuera del docker se necesita posicionarse en la carpeta `backend` y seguir estos pasos

1. Instalar las dependencias con poetry

```bash
poetry install
```

2. Activar el environment

```bash
poetry shell
```

3. Correr los test usando pytest

```bash
pytest
```

## Que casos de uso implementa?

### CRUD de Colegios

```
GET     /schools
GET     /schools/{school_id}
POST    /schools
PUT     /schools/{school_id}
DELETE  /schools
GET     /{school_id}/account-statement # Estado de cuenta del colegio
```

### CRUD de estudiantes

```
GET     /students
GET     /students/{student_id}
POST    /students
PUT     /students/{student_id}
DELETE  /students
GET     /{student_id}/account-statement # Estado de cuenta del estudiante
```

### CRUD de Facturas

```
GET     /invoices
GET     /invoices/{invoice_id}
GET     /invoices/student/{student_id}
GET     /invoices/school/{school_id}
POST    /invoices
PUT     /invoices/{invoice_id}
DELETE  /invoices/{invoice_id}
```

### EP Estado de cuenta de colegio

```
GET     /{school_id}/account-statement
```

### EP Estado de Cuenta del Estudiante

```
GET     /{student_id}/account-statement
```

### CRUD Inscripciones

```
GET     /inscriptions
GET     /inscriptions/{inscription_id}
GET     /inscriptions/student/{student_id}
GET     /inscriptions/school/{school_id}
POST    /inscriptions
PUT     /inscriptions/{inscription_id}
DELETE  /inscriptions/{inscription_id}
```
