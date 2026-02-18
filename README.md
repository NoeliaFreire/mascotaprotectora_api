# API Protectora de Mascotas 🐾

API REST desarrollada con **FastAPI** para la gestión de mascotas en una protectora. Este proyecto implementa un flujo completo de CI/CD con **GitHub Actions**, incluyendo análisis estático de código, tests unitarios y tests end-to-end (E2E).

## 📋 1. Objetivo y Descripción del Servicio

El servicio permite gestionar el inventario de mascotas de una protectora mediante peticiones HTTP. Sus funcionalidades principales son:
- **POST `/mascotas`**: Registrar una nueva mascota (nombre, especie, edad, adopción).
- **GET especial `/mascotas/disponibles`**: Consultar mascotas aplicando filtros de negocio combinados (recupera mascotas NO adoptadas y menores de una edad límite).

Para cumplir con la simplicidad requerida, la persistencia de datos se realiza **en memoria** (listas de Python), prescindiendo de una base de datos externa. Los datos de entrada y salida se validan estrictamente mediante modelos de **Pydantic**.

## 🚀 2. Pipeline de GitHub Actions

El archivo `pipeline.yml` define un workflow que se ejecuta automáticamente en eventos de `push` y `pull_request` hacia la rama `main`.

**Fases del Pipeline:**

1. **Setup:** Prepara un entorno Ubuntu, instala Python 3.10 y las dependencias (`pip install -r requirements.txt`).
2. **Análisis Estático (Linting):** Se ejecuta `ruff check .`. *Justificación:* Se eligió Ruff por ser el linter más rápido del ecosistema Python actual, asegurando que el código no contenga imports sin usar o errores de sintaxis antes de gastar recursos en los tests.
3. **Tests Unitarios:** Ejecución de `python -m pytest tests/test_unit.py`. Valida la clase `PetService` de forma aislada.
4. **Arranque de la API en Background:** (Ver sección 4).
5. **Tests End-to-End:** Ejecución de `python -m pytest tests/test_e2e.py` utilizando `httpx` para simular un cliente web real.

## ⚙️ 3. Ejecución de la API y Tests E2E en el Pipeline

Uno de los mayores retos técnicos del proyecto fue coordinar el arranque de la API FastAPI y la ejecución de los tests E2E dentro de la misma máquina virtual de GitHub Actions.

**Estrategia adoptada:**

1. **Proceso en Segundo Plano:** En el pipeline se ejecuta el comando `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &`.
   * **Decisión Técnica:** El operador ampersand (`&`) es crítico aquí. Permite que el servidor web se ejecute como un proceso en background. Si no se incluyera, la terminal de GitHub Actions se quedaría bloqueada esperando peticiones HTTP infinitamente, y el pipeline jamás avanzaría al paso de los tests.
2. **Sincronización (Sleep):** Inmediatamente después del comando de arranque, se introduce un `sleep 5`.
   * **Decisión Técnica:** Uvicorn tarda unos instantes en inicializar la aplicación y abrir el puerto 8000. Si lanzáramos los tests de inmediato, fallarían por conexión rechazada. El `sleep` garantiza que el servidor esté "escuchando" antes de que `httpx` lance la primera petición POST.

---

## 🛠️ 4. Problemas Encontrados y Resoluciones

Durante el desarrollo iterativo del pipeline, se detectaron y solucionaron los siguientes impedimentos:

1. **Rechazo del Linter por código sucio:** * **Problema:** GitHub Actions cancelaba el pipeline en el paso 2 porque Ruff detectaba importaciones declaradas pero no utilizadas.
   * **Solución:** Se integró la limpieza de código en el flujo de desarrollo local ejecutando `ruff check . --fix`, garantizando que solo sube a la rama principal código que cumple con los estándares de calidad.

2. **Pérdida de Contexto de Módulos (`ModuleNotFoundError`):**
   * **Problema:** Al ejecutar `pytest` o `uvicorn` directamente en la máquina virtual de GitHub, estos comandos no encontraban el paquete `app`, provocando fallos en las importaciones relativas


## 🗂 5. Estructura del Proyecto

```text
protectora_api/
├── .github/workflows/
│   └── pipeline.yml     # Configuración del Pipeline de CI/CD en GitHub Actions
├── app/
│   ├── main.py          # Entrypoint de la API (Endpoints GET y POST)
│   ├── models.py        # Esquemas Pydantic para validación
│   └── service.py       # Lógica de negocio (PetService) totalmente desacoplada
├── tests/
│   ├── test_unit.py     # Tests unitarios con Pytest (prueban PetService aislando la API)
│   └── test_e2e.py      # Tests de integración (Peticiones HTTP reales con httpx)
└── requirements.txt     # Dependencias del proyecto
