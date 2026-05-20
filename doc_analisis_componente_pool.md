# Análisis de enfoque: Pool de componentes para Joomla

## 1. Requisitos funcionales
- Extraer datos de la instancia Joomla actual: listados de:
  - Componentes (`com_...` activos)
  - Módulos y módulos asignados a menús
  - Plugins habilitados
  - Templates y overrides existentes
  - Ítems de menú y rutas actuales
- Estandarizar componente: nombre, tipo, parámetros, puntos de anclaje (positions), dependencias.
- Exponer un endpoint de consulta (API interna) que devuelva el pool en formato estructurado.
- Para cada nuevo diseño:
  - Extraer requerimientos visuales/textuales.
  - Mapear a componentes pool (ej: hero, lista de cards, formulario, tabla de datos).
  - Generar propuesta automática y/o sugerir componente faltante.

## 2. Análisis técnico
- Joomla 3.10: no API CRUD de contenido. Opciones:
  - Usar el helper `JTable` + servicios `JModelLegacy` para manipular `#__content`, `#__modules`, `#__menus`, etc.
  - Instalar `com_api` (https://github.com/techjoomla/com_api) para endpoints RESTable de terceros.
  - Acceso directo a BD si no se permite API.
- Enfoque sin tocar núcleo:
  - Crear un componente propio `com_componentpool` que registre y exponga el pool.
  - La UI de administración en backend + una API JSON para consumo con IA.
- Integración de IA:
  - Motor local/externo para entender texto/diseño -> componente mapping.
  - Guardado de análisis en `#__component_pool_analysis` y versión de diseño.

## 3. Estructura sugerida del documento de pool
- `id`: UUID / componente
- `slug`: hero-banner, card-grid, contact-form
- `tipo`: module, component, template-override, custom
- `posiciones`: [top, left, right, footer]
- `parametros`: (ancho, color, data-source, fields)
- `dependencias`: [com_content, mod_menu]
- `estatus`: activo, legacy, deprecated

## 4. Validación de viabilidad (PoC)
1. Listar y exportar pool actual (script PHP/SQL simple).
2. Crear script de mapeo de diseño -> componentes existentes.
3. Crear página de prueba en frontend que arme un layout con los componentes mapeados.
4. Revisar impacto de cambios en SEO y caché.

## 5. Siguientes pasos
1. Hacer inventario real con acceso al sitio.
2. Definir API de “requerimiento a componentes” (uso de LLM en pipeline).
3. Implementar componente backend para gestión del pool.
4. Iterar con 1-2 casos reales de páginas nuevas.
