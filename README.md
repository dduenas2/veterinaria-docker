# 🐾 Sistema de Gestión Veterinaria con Docker

Sistema completo de gestión para veterinarias implementado con arquitectura de microservicios usando Docker.

## 🏗️ Arquitectura

El proyecto está compuesto por 3 contenedores Docker:

1. **Frontend** (React + Nginx) - Puerto 3000
2. **Backend** (Flask API) - Puerto 5000
3. **Base de Datos** (PostgreSQL) - Puerto 5432

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Docker Desktop instalado
- Git
- WSL2 (para Windows)

### Pasos para ejecutar

1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd veterinaria-docker
```

2. Construir y levantar los contenedores
```bash
docker-compose up --build
```

3. Acceder a la aplicación
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Base de Datos: localhost:5432

## 📁 Estructura del Proyecto
```
veterinaria-docker/
├── frontend/          # Aplicación React
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   └── nginx.conf
├── backend/           # API Flask
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── database/          # Scripts SQL
│   └── init.sql
├── docker-compose.yml
└── README.md
```

## 🔧 Comandos Útiles
```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Reconstruir imágenes
docker-compose build --no-cache

# Ver contenedores activos
docker ps
```

## 📊 Funcionalidades

- ✅ Gestión de clientes
- ✅ Registro de mascotas
- ✅ Agendamiento de citas
- ✅ Dashboard con estadísticas
- ✅ Historial médico
- ✅ Interfaz responsive

## 👨‍💻 Tecnologías Utilizadas

- **Frontend**: React 18, CSS3
- **Backend**: Python 3.11, Flask
- **Base de Datos**: PostgreSQL 15
- **Contenedores**: Docker, Docker Compose
- **Servidor Web**: Nginx

## 📝 Autor

Proyecto de Integración Continua - Semana 3
