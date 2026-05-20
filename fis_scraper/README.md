# FIS Scraper (Piloto)

Crawler de validacion tecnica para migracion de contenido de `fis.epn.edu.ec`.

## Estado actual
- Entorno Python 3.12 validado.
- Proyecto Scrapy inicializado.
- Integracion `scrapy-playwright` configurada.
- Piloto de 5 URLs ejecutado con salida `finished`.
- Flujo incremental 5x5 habilitado (lote, validacion visual, ajuste, continuar).

## Estructura clave
- `fis_scraper/settings.py`: configuracion Scrapy + Playwright.
- `fis_scraper/playwright_utils.py`: filtro de requests externos.
- `fis_scraper/spiders/fis_pilot_spider.py`: spider piloto con salida por URL/estado.
- `output/run_*/`: artefactos de cada corrida.

## Dependencias
Instaladas en entorno virtual `.venv` del workspace.

Archivo de versiones: `requirements.txt`.

## Ejecucion
Desde `d:/github/epn/fisweb/fis_scraper`:

```powershell
..\.venv\Scripts\python.exe -m scrapy crawl fis_pilot
```

Corrida de smoke test (1 URL, sin interacciones):

```powershell
..\.venv\Scripts\python.exe -m scrapy crawl fis_pilot -a pilot_limit=1 -a max_interactions=0
```

## Parametros del spider
- `pilot_limit`: cantidad de URLs semilla a procesar (default: 5).
- `max_interactions`: maximo de clicks por pagina para estados JS (default: 3).
- `seed_file`: archivo con listado de URLs semilla (una por linea).
- `batch_start`: indice inicial del lote dentro de `seed_file` (default: 0).
- `batch_size`: tamano del lote (default: 5).
- `scope_limit`: alcance acumulado desde el inicio del seed (ej: 5, 10, 15...).
- `review_from`: desde que indice se consideran "URLs nuevas" para QA en `index.json`.

Ejemplo:

```powershell
..\.venv\Scripts\python.exe -m scrapy crawl fis_pilot -a pilot_limit=5 -a max_interactions=2
```

## Flujo recomendado 5x5
1. Ejecutar un lote de 5 URLs.
2. Validar con MCP Playwright (comparar live vs artifacts).
3. Ajustar reglas del spider si hay gaps.
4. Repetir con el siguiente lote (`batch_start + 5`).

## Flujo acumulativo recomendado (5 -> 10 -> 15 -> 20 ...)
Este modo aumenta el alcance total y marca en `index.json` solo las URLs nuevas de cada incremento.

Paso 1 (alcance 5, nuevas 0-4):

```powershell
..\.venv\Scripts\python.exe -m scrapy crawl fis_pilot -a seed_file=input/urls_master.txt -a scope_limit=5 -a review_from=0 -a max_interactions=5
```

Paso 2 (alcance 10, nuevas 5-9):

```powershell
..\.venv\Scripts\python.exe -m scrapy crawl fis_pilot -a seed_file=input/urls_master.txt -a scope_limit=10 -a review_from=5 -a max_interactions=5
```

Paso 3 (alcance 15, nuevas 10-14):

```powershell
..\.venv\Scripts\python.exe -m scrapy crawl fis_pilot -a seed_file=input/urls_master.txt -a scope_limit=15 -a review_from=10 -a max_interactions=5
```

Repite el mismo patron para 20, 25, 30, etc.

## Descubrimiento automatico de URLs
Si no tienes lista completa, genera un `urls_master.txt` automaticamente con el spider de discovery:

```powershell
..\.venv\Scripts\python.exe -m scrapy crawl fis_discovery -a max_urls=1200 -a output_file=input/urls_master.txt
```

El spider:
- recorre solo `fis.epn.edu.ec`,
- filtra assets/adjuntos no HTML,
- normaliza URLs Joomla (limpiando parametros de tracking),
- guarda la lista en `input/urls_master.txt`.

Luego ejecuta el flujo acumulativo con esa lista.

Archivo de semillas sugerido: `input/urls_master.txt`.

Ejemplo lote 1 (URLs 0-4):

```powershell
..\.venv\Scripts\python.exe -m scrapy crawl fis_pilot -a seed_file=input/urls_master.txt -a batch_start=0 -a batch_size=5 -a max_interactions=5
```

Ejemplo lote 2 (URLs 5-9):

```powershell
..\.venv\Scripts\python.exe -m scrapy crawl fis_pilot -a seed_file=input/urls_master.txt -a batch_start=5 -a batch_size=5 -a max_interactions=5
```

## Artefactos generados
Cada corrida crea:
- `output/run_YYYYMMDD_HHMMSS/index.json`
- `output/run_*/urls/<url_hash>/meta.json`
- `output/run_*/urls/<url_hash>/state_*.json`
- `output/run_*/urls/<url_hash>/html_rendered_*.html`
- `output/run_*/urls/<url_hash>/screenshot_*.png`
