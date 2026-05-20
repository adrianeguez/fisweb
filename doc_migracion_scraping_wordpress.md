contin# Documento de base - Migracion de contenido Joomla a WordPress via scraping

## 1) Contexto y decision de enfoque
- Origen: sitio Joomla (contenido mayormente informativo).
- Destino: nuevo servidor con WordPress y nuevo template.
- No es prioridad: metadata editorial, fecha de publicacion, colores o vista movil.
- Si es prioridad: texto, jerarquia, puntuacion, negritas, enlaces, tablas, tabs, acordeones y estados JS visibles.
- Enfoque acordado: migracion basada en scraping-first.

## 2) Objetivo operativo
Construir un pipeline que recorra toda la web publica, extraiga contenido y estructura por URL, capture estados interactivos relevantes (tabs/acordeones/paginadores/botones), y deje evidencia visual completa por pagina para revision de un agente de IA.

## 3) Stack recomendado (2026)
### Base
- Python 3.12+
- Scrapy (crawler principal, descubrimiento de enlaces, cola y politicas de crawl)

### Renderizado JS y estados dinamicos
- Playwright (control de navegador headless para ejecutar JavaScript real)
- scrapy-playwright (integracion de Playwright dentro de spiders de Scrapy)

### Parseo y normalizacion
- Selectors de Scrapy (XPath/CSS)
- lxml/BeautifulSoup (opcional para limpieza adicional de HTML)

### Persistencia
- Archivos JSON por URL y por estado de la pagina
- Carpeta de screenshots full-page por URL y estado
- Archivo index global para trazabilidad de crawl

## 4) Por que Scrapy + Playwright (y no solo Scrapy)
- Scrapy solo no interactua con widgets JS complejos sin apoyo.
- Hay componentes Joomla que renderizan contenido al hacer click.
- Playwright permite:
  - esperar eventos JS,
  - abrir tabs/acordeones,
  - capturar estados,
  - sacar screenshot full-page real.
- Resultado: scraping robusto de paginas simples y tambien de paginas con interaccion.

## 5) Alcance funcional del crawler
### Descubrimiento de URLs
- Fuente 1: sitemap.xml y sitemaps anidados.
- Fuente 2: crawl navegacional desde homepage y menus.
- Fuente 3: enlaces internos encontrados en contenido.
- Regla: solo dominio objetivo (sin salir a externos).

### Extraccion por pagina
- URL final, titulo, breadcrumbs (si aplica).
- Contenido principal limpio (texto con semantica basica).
- Bloques estructurados detectados:
  - tablas,
  - listas,
  - enlaces,
  - imagenes,
  - tabs/acordeones,
  - embeds/iframes (si existen).

### Captura de estados
- Estado base (sin interaccion).
- Estado por cada tab/acordeon/boton principal detectable.
- Limite configurable para evitar explosion combinatoria.
- Registro de acciones ejecutadas para reproducibilidad.

### Evidencia visual
- Screenshot full-page por estado.
- Ancho fijo recomendado: 1920 px.
- Alto: full page automatico (sin recorte), o segmentado si la pagina es extremadamente larga.

## 6) Estructura de almacenamiento propuesta
```text
output/
  run_YYYYMMDD_HHMMSS/
    index.json
    urls/
      <url_hash>/
        meta.json
        state_000_base.json
        state_001_tab_admisiones.json
        state_002_tab_malla.json
        screenshot_000_base.png
        screenshot_001_tab_admisiones.png
        screenshot_002_tab_malla.png
        html_raw_000_base.html
        html_rendered_001_tab_admisiones.html
```

### Convenciones recomendadas
- Un directorio por URL (hash estable + slug humano opcional).
- Un JSON por estado con:
  - selector accionado,
  - tipo de accion,
  - texto visible extraido,
  - bloques detectados,
  - enlaces detectados.
- `index.json` global con:
  - estado de cada URL (ok/error/skipped),
  - numero de estados capturados,
  - metricas de cobertura.

## 7) Esquema JSON minimo por estado
```json
{
  "url": "https://sitio/pagina-x",
  "state_id": "state_001_tab_admisiones",
  "actions": [
    {"type": "click", "selector": "#tabs .tab-admisiones"}
  ],
  "content": {
    "title": "...",
    "headings": ["..."],
    "paragraphs": ["..."],
    "links": [{"text": "...", "href": "..."}],
    "tables": [
      {
        "caption": "",
        "headers": ["..."],
        "rows": [["...", "..."]]
      }
    ],
    "tabs": [
      {"label": "Admisiones", "active": true}
    ]
  },
  "assets": {
    "screenshot": "screenshot_001_tab_admisiones.png",
    "html_rendered": "html_rendered_001_tab_admisiones.html"
  }
}
```

## 8) Buenas practicas 2026 para este proyecto
- Crawl incremental por lotes (no intentar toda la web en primera corrida).
- Cadencia operativa recomendada: lotes fijos de 5 URLs (5x5) con compuerta de QA entre lotes.
- Politicas de respeto al servidor: concurrencia moderada, retry con backoff, timeout claro.
- Deteccion y deduplicacion de URLs canonicas.
- Trazabilidad completa de errores por URL y selector.
- Versionar el schema JSON desde el inicio (`schema_version`).
- Registrar metricas por corrida:
  - URLs descubiertas,
  - URLs procesadas,
  - errores,
  - paginas con JS,
  - numero de estados por pagina.
- Mantener una lista de paginas complejas para segunda fase.

## 9) Riesgos esperados y mitigacion
- Riesgo: no capturar todos los enlaces por JS tardio.
  - Mitigacion: esperar eventos, scroll controlado y rutas desde sitemap.
- Riesgo: explosion de estados combinatorios.
  - Mitigacion: maximo de acciones por pagina y priorizacion por componentes.
- Riesgo: contenido duplicado por URLs equivalentes.
  - Mitigacion: normalizacion/canonicalizacion de URLs.
- Riesgo: capturas truncadas en paginas muy largas.
  - Mitigacion: full-page + opcion de capturas segmentadas.

## 10) Estrategia por fases
### Fase A - Cobertura rapida
- Capturar estado base de todas las URLs.
- Detectar paginas complejas automaticamente.

### Fase B - Estados interactivos
- Ejecutar clicks sobre tabs/acordeones/controles comunes.
- Guardar estados adicionales y evidencia visual.

### Fase C - QA y priorizacion
- Revisar cobertura y errores.
- Separar paginas simples (migracion directa) de complejas (analisis manual guiado).

## 10.1) Cadencia de ejecucion 5x5 con MCP Playwright
Para reducir riesgo y acelerar ajustes, la ejecucion se hace por micro-lotes:

1. Ejecutar lote N de 5 URLs.
2. Validar evidencia por URL con MCP Playwright (live vs `state_*.json` + screenshots).
3. Registrar gaps detectados (texto faltante, acordeones/tabs no capturados, enlaces rotos).
4. Ajustar selectores/extractores.
5. Re-ejecutar el mismo lote hasta pasar QA.
6. Avanzar al lote N+1 (siguiente bloque de 5 URLs).

### Criterio de paso por lote
- 100% de las 5 URLs con `meta.json` y `state_000_base.json`.
- Al menos 1 screenshot por URL.
- Componentes interactivos visibles en live con evidencia equivalente en artifacts.
- Sin errores bloqueantes en logs del run.

## 11) Definiciones de listo (DoD)
Una URL se considera lista cuando:
- Tiene `meta.json` valido.
- Tiene al menos 1 estado capturado.
- Tiene screenshot full-page del estado base.
- Tiene contenido estructurado (texto + enlaces + bloques detectados).
- No tiene errores bloqueantes en el log.

## 12) Proximos pasos para iniciar investigacion
1. Definir dominio exacto, subdominios permitidos y exclusiones.
2. Definir limite de profundidad y politicas de crawl.
3. Implementar PoC en modo 5x5 (primeros 5, luego siguientes 5, etc.) hasta completar 30-50 URLs.
4. Ajustar detectores de tabs/tablas/acordeones.
5. Escalar al sitio completo por lotes.

## 13) Decision de trabajo
- Se acepta iniciar con scraping-first.
- Se prioriza capturar la informacion visible y su estructura util para migracion.
- Las paginas complejas se procesan en una segunda pasada con reglas especificas.
