# Requerimientos iniciales - AI-driven development para Joomla FIS

## Objetivo principal
Implementar un proceso de desarrollo basado en IA para el sitio Joomla de la Escuela Politécnica Nacional (FIS), donde cada nueva página o función se construye a partir de componentes reutilizables en un "pool".

## Alcance
1. Auditar la instalación actual de Joomla 3.10 (actualmente 3.10.12 según el help screen).
2. Identificar APIs disponibles (Joomla com_admin, com_content, API REST, etc.) para creación/edición de páginas y componentes.
3. Listar y documentar componentes actuales en uso (módulos, plugins, templates, componentes personalizados).
4. Diseñar un flujo de trabajo de nuevas páginas:
   - Input: requerimiento/descripción/diseño UI (imagen o Figma).
   - Matching: mapa de componentes existentes (pool) + gaps detectados.
   - Output: propuesta de construcción (combinación de componentes, nuevo componente, ajustes).
5. Definir un proceso automatizado/machine-assisted para:
   - Generar borradores de contenido y estructura usando un modelo de lenguaje (p.e. ChatGPT).
   - Generar o ajustar archivos de template y layout (overrides) según diseño.
   - Crear tickets/PRs y pruebas de regresión.

## Preguntas iniciales (para el cliente)
- ¿Tenemos acceso directo a los archivos del template actual y a la base de datos del sitio? 
- ¿Existe un control de versiones para extendidos (componentes personalizados) en github? 
- ¿Quieren usar la API Joomla 3.10 (sin API de contenido nativa) o migrar a Joomla 4 con API REST nativa? 
- ¿Cuál es el proceso de QA/Deploy actual (local/staging/prod)?

## Restricciones conocidas
- Joomla 3.10 no trae REST nativo completo; puede requerir plugin joomla-api o com_api.
- Seguridad: tokens CSRF (form token) y ACL deben respetarse.
- Deploy en servidor `fis.epn.edu.ec` posiblemente con PHP 7.x/8.x y permisos restringidos.

## Hitos iniciales
1. Inventario de componentes y módulos activos.
2. Definición de esquema JSON para el pool de componentes.
3. API de descubrimiento: endpoint interno para consultar `pool` y compatibilidad de diseño.
4. PoC: crear una página de ejemplo usando pool y un diseño simple.
