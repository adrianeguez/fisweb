# Mapa detallado de navegacion FIS EPN

Documento vivo para documentar la navegacion de segundo nivel del sitio FIS de la EPN.

Regla de lectura:
- `verificado` = revisado en la home con Playwright y/o en los lotes del crawler.
- `visible en menu` = enlace o nodo observado en la navegacion publica.
- `pendiente` = nodo visible pero sin revision profunda de su pagina hija en esta pasada.

## 1) Home y enlaces globales
**Pagina raiz:** [La Facultad de Ingenieria de Sistemas](https://fis.epn.edu.ec/index.php/es/you-will-love-our-school)

### Enlaces globales visibles
- `Estudiante`
- `Docente`
- `INICIO`
- `LA FACULTAD`
- `PREGRADO`
- `POSGRADO`
- `INVESTIGACION`
- `REVISTA LAJC`
- Controles de fuente: menor, defecto, mayor
- Logo a la portada
- Footer: `Facebook`, `Joomla Templates`

## 2) Rama LA FACULTAD
**Estado general:** verificado

### 2.1) Estructura organica
**Pagina:** [Estructura orgánica](https://fis.epn.edu.ec/index.php/es/la-facultad/estructura-organica)

**Bloques visibles:**
- `MISIÓN`
- `VISIÓN`
- `DEPARTAMENTO DE INFORMÁTICA Y CIENCIAS DE LA COMPUTACIÓN (DICC)`
- `AUTORIDADES`
  - Decana
  - Subdecano
  - Jefa del DICC

**Navegacion interna visible:**
- `Planta docente`
- `Departamento de Informática y Ciencias de la Computación`
- `Laboratorios de Docencia`
- `Laboratorios de investigación`
- `Gestión de Transferencia Tecnológica`

**Estado:** verificado

### 2.2) Planta docente
**Pagina:** [Planta docente](https://fis.epn.edu.ec/index.php/es/la-facultad/planta-docentes)

**Comportamiento:**
- Listado paginado de docentes.
- Cada tarjeta o fila abre una ficha individual.
- La pagina usa paginacion por `start`.

**Paginacion visible:**
- `start=10`
- `start=20`
- `start=30`
- `start=40`
- `start=50`

**Fichas individuales revisadas en esta sesion:**
- `Aguiar Pontes Josafa de Jesus`
- `Carrion Toro Mayra del Cisne`
- `Calle Jimenez Tania Elizabeth`
- `Barriga Andrade Jhonattan Javier`
- `Yoo Park Sang Guun`
- `Navarrete Rueda Rosa Del Carmen`
- `Carrera Izurieta Ivan Marcelo`
- `Mafla Gallegos Luis Enrique`
- `Recalde Cerda Lorena Katherine`
- `Martinez Mosquera Silvia Diana`
- `Peñafiel Aguilar Myriam Guadalupe`
- `Sanchez Gordon Sandra Patricia`
- `Perez Hernandez Maria Gabriela`
- `Flores Naranjo Pamela Catherine`
- `Ordóñez Calero Hernán David`

**Estructura de una ficha individual:**
- `Estudios`
- `Línea prioritaria de investigación`
- `Publicaciones`
- Contacto / correo / ORCID
- Tabla de datos del docente

**Estado:** verificado

### 2.3) Departamento de Informatica y Ciencias de la Computacion
**Pagina madre:** [Departamento de Informática y Ciencias de la Computación](https://fis.epn.edu.ec/index.php/es/la-facultad/departamento-de-informatica-y-ciencias-de-la-computacion)

**Hijos visibles desde el menu/home:**
- `Planta docente`
- `Líneas Prioritarias de Investigación`
- `Grupos de investigación`
- `Proyectos de investigación`
- `Proyectos de vinculación y proyección social`

**Estado:** visible en menu, pendiente de mapa propio si se quiere profundizar aun mas

### 2.4) Laboratorios de Docencia
**Pagina:** [Laboratorios de Docencia](https://fis.epn.edu.ec/index.php/es/la-facultad/laboratorios)

**Entradas visibles revisadas:**
- `Laboratorio del Programa de Doctorado en Informática - LAPDI`
- `Laboratorios de Docencia`

**Subenlaces visibles:**
- Enlaces a cada laboratorio individual
- Enlace a la ficha del laboratorio LAPDI

**Estado:** verificado

### 2.5) Laboratorios de investigacion
**Pagina:** [Laboratorios de investigación](https://fis.epn.edu.ec/index.php/es/la-facultad/laboratorios-de-investigacion)

**Estado:** visible en menu, pendiente de mapa propio

### 2.6) Gestion de Transferencia Tecnologica
**Pagina:** [Gestión de Transferencia Tecnológica](https://fis.epn.edu.ec/index.php/es/la-facultad/gestion-de-transferencia-tecnologica)

**Bloques visibles:**
- `Objetivo`
- `NOTICIAS Y EVENTOS`
- `FORTALEZAS INTERNAS`

**Subpaginas visibles:**
- [Centro de Medios](https://fis.epn.edu.ec/index.php/es/la-facultad/gestion-de-transferencia-tecnologica/centro-de-medios)
- `Eventos Organizados`
- `Fortalezas Internas`
- `Equipo`
- `Contacto GTTT`

**Estado:** verificado en home y en pagina madre; subpaginas visibles documentadas, algunas pendientes de revision profunda

## 3) Rama PREGRADO
**Estado general:** visible en menu

### 3.1) Software
**Pagina:** [Software](https://fis.epn.edu.ec/index.php/es/oferta-academicafis/software)

**Estado:** visible en menu, pendiente de revision profunda

### 3.2) Computacion
**Pagina:** [Computación](https://fis.epn.edu.ec/index.php/es/oferta-academicafis/computacion)

**Estado:** visible en menu, pendiente de revision profunda

### 3.3) Ciencia de Datos e Inteligencia Artificial
**Pagina:** [Ciencia de Datos e Inteligencia Artificial](https://fis.epn.edu.ec/index.php/es/oferta-academicafis/ciencia-de-datos-e-inteligencia-artificial)

**Estado:** visible en menu, pendiente de revision profunda

### 3.4) Sistemas de Informacion
**Pagina:** [Sistemas de Información](https://fis.epn.edu.ec/index.php/es/oferta-academicafis/sistemas-de-informacion)

**Estado:** visible en menu, pendiente de revision profunda

### 3.5) Ciberseguridad (En propuesta)
**Estado:** visible como texto en menu, sin pagina enlazada

## 4) Rama POSGRADO
**Estado general:** verificado en menu y en varias paginas

### 4.1) Maestria en Inteligencia Artificial
**Pagina:** [Maestría en Inteligencia Artificial](https://fis.epn.edu.ec/index.php/es/maestrias/maestria-en-inteligencia-artificial-art)

**Estado:** visible en menu, pendiente de revision profunda en esta pasada

### 4.2) Maestria en Ciberseguridad
**Pagina:** [Maestría en Ciberseguridad](https://fis.epn.edu.ec/index.php/es/maestrias/maestria-en-ciberseguridad)

**Estado:** visible en menu, pendiente de revision profunda en esta pasada

### 4.3) Maestria en Tecnologia e Innovacion Educativa
**Pagina:** [Maestría en Tecnología e Innovación Educativa](https://fis.epn.edu.ec/index.php/es/maestrias/maestria-en-tecnologia-e-innovacion-educativa)

**Bloques visibles:**
- Convocatoria / admision
- Perfil de ingreso
- Resultados de aprendizaje
- Perfil de egreso
- `POSTULA AQUÍ`

**Estado:** verificado

### 4.4) Doctorado en Informatica
**Pagina:** [Doctorado en Informática](https://fis.epn.edu.ec/index.php/es/maestrias/doctorado-en-informatica)

**Bloques visibles:**
- Descripcion institucional
- `CONTACTO`
- `UBICACIÓN`
- Sitio web externo del programa
- Facebook del programa

**Estado:** verificado

## 5) Rama INVESTIGACION
**Estado general:** visible en menu y con paginas ya validadas en lotes previos

### 5.1) Lineas Prioritarias de Investigacion
**Pagina:** [Líneas Prioritarias de Investigación](https://fis.epn.edu.ec/index.php/es/investigacion/lineas-de-investigacion)

**Estado:** visible en menu, pendiente de mapa propio

### 5.2) Grupos de investigacion
**Pagina:** [Grupos de investigación](https://fis.epn.edu.ec/index.php/es/la-facultad/departamento-de-informatica-y-ciencias-de-la-computacion/grupos-de-investigacion)

**Estado:** verificado en navegador / crawler

### 5.3) Proyectos de investigacion
**Pagina:** [Proyectos de investigación](https://fis.epn.edu.ec/index.php/es/la-facultad/departamento-de-informatica-y-ciencias-de-la-computacion/proyectos-de-investigacion)

**Estructura observada en lotes revisados:**
- Proyectos internos
- Proyectos internos sin financiamiento
- Secciones frecuentes:
  - `OBJETIVO GENERAL`
  - `OBJETIVOS ESPECÍFICOS`
  - `RESULTADOS`
  - `Publicaciones`
  - `Presentaciones en eventos internacionales`
  - `Proyectos de titulación`

**Estado:** verificado en varios lotes

### 5.4) Proyectos de vinculacion y proyeccion social
**Pagina:** [Proyectos de vinculación y proyección social](https://fis.epn.edu.ec/index.php/es/la-facultad/departamento-de-informatica-y-ciencias-de-la-computacion/proyectos-de-vinculacion-y-proyeccion-social)

**Estructura observada en lotes revisados:**
- Fichas de proyectos de vinculacion
- Objetivo general
- Publicaciones / resultados
- Proyectos derivados o asociados

**Estado:** verificado en varios lotes

## 6) Rama REVISTA LAJC
**Pagina madre:** `REVISTA LAJC`

**Pagina visible:**
- [LAJC](https://lajc.epn.edu.ec/index.php/LAJC)

**Estado:** visible en menu, pendiente de mapa propio

## 7) Observaciones de navegacion
- La home concentra la navegacion de primer nivel y funciona como indice general.
- `LA FACULTAD` y `POSGRADO` son las ramas con mas profundidad documental.
- `Planta docente` es la rama mas densa en cantidad de paginas hijas.
- `Gestion de Transferencia Tecnologica` tambien concentra varias subpaginas y merece mapa propio de segundo nivel.
- `INVESTIGACION` mezcla contenido conceptual con paginas de proyectos concretos.

## 8) Estado del documento
- Documento creado a partir de la navegacion ya verificada con Playwright y de los lotes del crawler revisados en esta sesion.
- Listo para seguir ampliandose con tercer nivel si quieres que documentemos cada subpagina de cada rama.

## 9) Indice final de paginas principales y enlaces disponibles
Este indice resume, para cada pagina principal ya documentada, que se muestra y que tipos de enlaces disponibles fueron observados.

### 9.1) Pagina raiz
**Pagina:** [La Facultad de Ingenieria de Sistemas](https://fis.epn.edu.ec/index.php/es/you-will-love-our-school)

**Resumen:** pagina de entrada del sitio. Presenta la mision institucional de la FIS y funciona como hub de navegacion a todas las ramas principales.

**Enlaces disponibles:**
- Enlaces internos de menu: `INICIO`, `LA FACULTAD`, `PREGRADO`, `POSGRADO`, `INVESTIGACION`, `REVISTA LAJC`
- Enlaces rapidos: `Estudiante`, `Docente`
- Controles de fuente
- Enlaces externos: `Facebook`, `Joomla Templates`

### 9.2) Estructura organica
**Pagina:** [Estructura orgánica](https://fis.epn.edu.ec/index.php/es/la-facultad/estructura-organica)

**Resumen:** presenta mision, vision y autoridades de la FIS, con foco en la organizacion interna.

**Enlaces disponibles:**
- Enlaces internos al resto de la Facultad
- Enlaces a perfiles de autoridades y docentes

### 9.3) Planta docente
**Pagina:** [Planta docente](https://fis.epn.edu.ec/index.php/es/la-facultad/planta-docentes)

**Resumen:** directorio paginado de docentes con acceso a fichas individuales.

**Enlaces disponibles:**
- Paginacion (`start=10`, `start=20`, `start=30`, `start=40`, `start=50`)
- Enlaces a fichas de docentes
- Enlaces de correo `mailto:`
- Enlaces `ORCID`
- Enlaces `Scopus` y `DOI` dentro de perfiles individuales

### 9.4) Departamento de Informatica y Ciencias de la Computacion
**Pagina:** [Departamento de Informática y Ciencias de la Computación](https://fis.epn.edu.ec/index.php/es/la-facultad/departamento-de-informatica-y-ciencias-de-la-computacion)

**Resumen:** pagina madre de la oferta academica y de investigacion del DICC.

**Enlaces disponibles:**
- `Planta docente`
- `Líneas Prioritarias de Investigación`
- `Grupos de investigación`
- `Proyectos de investigación`
- `Proyectos de vinculación y proyección social`

### 9.5) Laboratorios de Docencia
**Pagina:** [Laboratorios de Docencia](https://fis.epn.edu.ec/index.php/es/la-facultad/laboratorios)

**Resumen:** listado de laboratorios docentes con fichas y descripciones cortas.

**Enlaces disponibles:**
- Enlaces a cada laboratorio individual
- Enlace de regreso a la ficha del laboratorio madre

### 9.6) Laboratorios de investigacion
**Pagina:** [Laboratorios de investigación](https://fis.epn.edu.ec/index.php/es/la-facultad/laboratorios-de-investigacion)

**Resumen:** pagina madre de laboratorios de investigacion.

**Enlaces disponibles:**
- Navegacion interna hacia laboratorios y secciones de la Facultad

### 9.7) Gestion de Transferencia Tecnologica
**Pagina:** [Gestión de Transferencia Tecnológica](https://fis.epn.edu.ec/index.php/es/la-facultad/gestion-de-transferencia-tecnologica)

**Resumen:** portal de transferencia tecnologica con objetivo institucional, noticias y fortalezas.

**Enlaces disponibles:**
- `Centro de Medios`
- `Eventos Organizados`
- `Fortalezas Internas`
- `Equipo`
- `Contacto GTTT`
- Enlaces a notas y paginas internas de transferencia

### 9.8) Centro de Medios
**Pagina:** [Centro de Medios](https://fis.epn.edu.ec/index.php/es/la-facultad/gestion-de-transferencia-tecnologica/centro-de-medios)

**Resumen:** seccion multimedia con podcasts y contenido audiovisual.

**Enlaces disponibles:**
- Recurso multimedia embebido
- Contenido asociado a podcasts

### 9.9) Pregrado
**Pagina madre:** `PREGRADO`

**Resumen:** agrupacion de carreras/programas de pregrado.

**Hijos visibles:**
- [Software](https://fis.epn.edu.ec/index.php/es/oferta-academicafis/software)
- [Computación](https://fis.epn.edu.ec/index.php/es/oferta-academicafis/computacion)
- [Ciencia de Datos e Inteligencia Artificial](https://fis.epn.edu.ec/index.php/es/oferta-academicafis/ciencia-de-datos-e-inteligencia-artificial)
- [Sistemas de Información](https://fis.epn.edu.ec/index.php/es/oferta-academicafis/sistemas-de-informacion)
- `Ciberseguridad (En propuesta)`

**Enlaces disponibles:**
- Enlaces a cada oferta academica
- Enlaces de navegacion a paginas relacionadas de la Facultad

### 9.10) Posgrado
**Pagina madre:** `POSGRADO`

**Resumen:** agrupa los programas de maestria y doctorado.

**Hijos visibles:**
- [Maestría en Inteligencia Artificial](https://fis.epn.edu.ec/index.php/es/maestrias/maestria-en-inteligencia-artificial-art)
- [Maestría en Ciberseguridad](https://fis.epn.edu.ec/index.php/es/maestrias/maestria-en-ciberseguridad)
- [Maestría en Tecnología e Innovación Educativa](https://fis.epn.edu.ec/index.php/es/maestrias/maestria-en-tecnologia-e-innovacion-educativa)
- [Doctorado en Informática](https://fis.epn.edu.ec/index.php/es/maestrias/doctorado-en-informatica)

**Enlaces disponibles:**
- Enlaces a programas externos e internos
- Sitio web externo del doctorado
- Formularios o accesos de postulación donde aplique

### 9.11) Doctorado en Informatica
**Pagina:** [Doctorado en Informática](https://fis.epn.edu.ec/index.php/es/maestrias/doctorado-en-informatica)

**Resumen:** pagina institucional del doctorado, con descripcion, contacto y ubicacion.

**Enlaces disponibles:**
- `Visita el Sitio Web`
- `Sitio Web`
- `Facebook`
- `mailto:` de contacto

### 9.12) Maestria en Tecnologia e Innovacion Educativa
**Pagina:** [Maestría en Tecnología e Innovación Educativa](https://fis.epn.edu.ec/index.php/es/maestrias/maestria-en-tecnologia-e-innovacion-educativa)

**Resumen:** pagina del programa de maestria con convocatoria, admision, perfil de ingreso, resultados y egreso.

**Enlaces disponibles:**
- `POSTULA AQUÍ`
- Enlaces internos a planes de estudio y recursos asociados

### 9.13) Investigacion
**Pagina madre:** `INVESTIGACION`

**Resumen:** agrupa lineas, grupos, proyectos y vinculacion.

**Hijos visibles:**
- [Líneas Prioritarias de Investigación](https://fis.epn.edu.ec/index.php/es/investigacion/lineas-de-investigacion)
- [Grupos de investigación](https://fis.epn.edu.ec/index.php/es/la-facultad/departamento-de-informatica-y-ciencias-de-la-computacion/grupos-de-investigacion)
- [Proyectos de investigación](https://fis.epn.edu.ec/index.php/es/la-facultad/departamento-de-informatica-y-ciencias-de-la-computacion/proyectos-de-investigacion)
- [Proyectos de vinculación y proyección social](https://fis.epn.edu.ec/index.php/es/la-facultad/departamento-de-informatica-y-ciencias-de-la-computacion/proyectos-de-vinculacion-y-proyeccion-social)

### 9.14) Proyectos de investigacion
**Pagina:** [Proyectos de investigación](https://fis.epn.edu.ec/index.php/es/la-facultad/departamento-de-informatica-y-ciencias-de-la-computacion/proyectos-de-investigacion)

**Resumen:** fichas de proyectos con estructura semantica rica.

**Enlaces disponibles:**
- `OBJETIVO GENERAL`
- `OBJETIVOS ESPECÍFICOS`
- `RESULTADOS`
- `Publicaciones`
- `Presentaciones en eventos internacionales`
- `Proyectos de titulación`
- Enlaces externos a DOI, Springer, Scopus y revistas

### 9.15) Proyectos de vinculacion y proyeccion social
**Pagina:** [Proyectos de vinculación y proyección social](https://fis.epn.edu.ec/index.php/es/la-facultad/departamento-de-informatica-y-ciencias-de-la-computacion/proyectos-de-vinculacion-y-proyeccion-social)

**Resumen:** fichas de proyectos de vinculacion con informacion de objetivo y resultados.

**Enlaces disponibles:**
- Enlaces a proyectos asociados
- Enlaces externos de publicaciones cuando aplican

### 9.16) Revista LAJC
**Pagina:** [LAJC](https://lajc.epn.edu.ec/index.php/LAJC)

**Resumen:** portal de la revista institucional.

**Enlaces disponibles:**
- Navegacion propia de la revista
- Enlaces externos relacionados al portal editorial

## 10) Nota final
Este indice esta pensado como referencia rapida para migracion y QA. Si quieres, el siguiente paso es agregar un tercer nivel con una fila por cada subpagina concreta que ya revisamos, por ejemplo cada docente, cada proyecto y cada oferta academica.
