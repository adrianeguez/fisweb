# Propuesta de redisenio de navegacion - FIS EPN

Documento de propuesta para reorganizar la informacion del sitio FIS de la EPN con una estructura mas clara, mas breve y mas facil de mantener.

## 1) Objetivo
Redisenar la navegacion publica para que el sitio responda rapido a tres necesidades:
- Entender que es la FIS.
- Encontrar la oferta academica y la investigacion.
- Acceder a recursos institucionales y de contacto.

## 2) Regla base de la nueva version
En la nueva pagina no existiran accesos publicos para `Estudiante`, `Docente` ni `staff`.

Alcance de usuarios:
- Solo visitantes publicos.
- Solo administradores de WordPress para edicion y mantenimiento.

Implicaciones:
- No debe haber menus publicos por rol.
- No debe haber areas privadas visibles para estudiantes o profesores.
- No debe existir navegacion basada en permisos de usuario para el frontend.

## 3) Principios de organizacion
- Organizar por intencion de busqueda, no por organigrama interno.
- Reducir el menu principal a pocos pilares estables.
- Evitar contenido repetido en varias paginas.
- Cada pagina debe tener un objetivo unico.
- Cada pagina debe cerrar con un bloque util de enlaces relacionados, descargas o contacto.
- El home debe funcionar como indice visual, no como lista extensa.

## 4) Arquitectura propuesta del sitio

### 4.1) Navegacion principal sugerida
1. Inicio
2. La Facultad
3. Oferta Academica
4. Investigacion e Innovacion
5. Transferencia y Vinculacion
6. Revista LAJC
7. Contacto

### 4.2) Estructura de segundo nivel

#### Inicio
- Resumen institucional
- Accesos rapidos por tema
- Noticias o destacados
- Bloque de eventos o avisos
- Bloque de enlaces utiles

#### La Facultad
- Estructura organica
- Autoridades
- Planta docente
- Departamento de Informatica y Ciencias de la Computacion
- Laboratorios de docencia
- Laboratorios de investigacion
- Historia o perfil institucional, si aplica

#### Oferta Academica
- Pregrado
  - Software
  - Computacion
  - Ciencia de Datos e Inteligencia Artificial
  - Sistemas de Informacion
  - Ciberseguridad, solo si ya existe como oferta oficial
- Posgrado
  - Maestria en Inteligencia Artificial
  - Maestria en Ciberseguridad
  - Maestria en Tecnologia e Innovacion Educativa
  - Doctorado en Informatica

#### Investigacion e Innovacion
- Lineas prioritarias de investigacion
- Grupos de investigacion
- Proyectos de investigacion
- Publicaciones y produccion academica
- Laboratorios de investigacion
- Centro de medios o contenidos multimedia

#### Transferencia y Vinculacion
- Gestion de transferencia tecnologica
- Eventos organizados
- Fortalezas internas
- Equipo de trabajo
- Contacto

#### Revista LAJC
- Portal de la revista
- Numeros o ediciones
- Normas para autores
- Envio de articulos
- Contacto editorial

#### Contacto
- Ubicacion
- Correo institucional
- Telefonos
- Redes sociales
- Mapa o ruta

## 5) Que conviene cambiar respecto al sitio actual

### 5.1) Quitar accesos por perfil publico
Los enlaces `Estudiante` y `Docente` deben desaparecer del encabezado publico.

Reemplazo recomendado:
- Un menu mas limpio con menos opciones.
- Accesos rapidos por tema, no por rol.

### 5.2) Mover Transferencia Tecnologica fuera de La Facultad
Hoy esta rama funciona como una subarea de la Facultad, pero por contenido y objetivo encaja mejor como una seccion transversal de innovacion y relacion externa.

### 5.3) Unificar paginas que repiten informacion
Hay varias paginas que se traslapan en contenido institucional, investigacion y oferta academica. Se recomienda:
- Una pagina madre por tema.
- Subpaginas solo para contenido realmente distinto.
- Evitar repetir mision, vision o enlaces en varias paginas.

### 5.4) Separar contenido editorial de contenido institucional
LAJC no deberia competir visualmente con la oferta academica o la Facultad. Debe quedar como seccion secundaria o independiente.

## 6) Reglas de contenido para cada tipo de pagina

### 6.1) Paginas institucionales
Debe incluir:
- Resumen corto inicial.
- Datos clave.
- Bloque de autoridades si aplica.
- Enlaces internos relacionados.
- Imagen o grafico solo si aporta claridad.

### 6.2) Paginas de programas academicos
Debe incluir:
- Que es el programa.
- A quien va dirigido.
- Perfil de ingreso.
- Perfil de egreso.
- Malla, plan o documentos de respaldo.
- Proceso de admision o postulacion.
- Contacto.
- Descargas en PDF si existen.

### 6.3) Paginas de docentes
Debe incluir:
- Resumen profesional.
- Areas de interes.
- Linea de investigacion.
- Publicaciones.
- Contacto.
- Identificadores externos como ORCID o Scopus si existen.

### 6.4) Paginas de proyectos
Debe incluir:
- Objetivo.
- Alcance.
- Equipo o responsables.
- Resultados.
- Productos.
- Enlaces externos o documentos asociados.

### 6.5) Paginas de laboratorios
Debe incluir:
- Descripcion.
- Equipamiento o capacidades.
- Ubicacion.
- Responsable.
- Imagenes o galeria, si existen.

### 6.6) Paginas de vinculacion y transferencia
Debe incluir:
- Proposito.
- Servicios o actividades.
- Equipo.
- Eventos.
- Noticias.
- Formas de contacto.

## 7) Reglas de navegacion
- Menu superior con 6 o 7 opciones maximo.
- Submenus cortos y agrupados por tema.
- Breadcrumb obligatorio en paginas internas.
- Bloque de enlaces relacionados al final.
- No usar listas interminables en el menu principal.
- No ocultar contenido clave dentro de rutas profundas sin acceso directo.
- Mantener enlaces cruzados entre areas relacionadas.

## 8) Reglas visuales de home
El inicio deberia tener esta secuencia:
1. Encabezado claro con propuesta institucional.
2. Hero principal con CTA a oferta academica e investigacion.
3. Tarjetas de acceso rapido por area.
4. Noticias o destacados.
5. Bloques de programas, investigacion y vinculo.
6. Pie con contacto y enlaces externos.

## 9) Mejoras concretas que se recomiendan
- Reducir el numero de entradas visibles en el encabezado.
- Eliminar accesos por perfil de usuario publico.
- Crear una jerarquia mas clara entre Facultad, Oferta Academica e Investigacion.
- Llevar Transferencia Tecnologica a una categoria propia.
- Dar a cada programa una plantilla uniforme.
- Crear un patron comun para docentes, proyectos y laboratorios.
- Agregar indice interno en paginas largas.
- Mostrar recursos descargables y enlaces externos en un bloque final estandar.
- Unificar estilo de titulos, botones y secciones.

## 10) Prioridades de implementacion
### Fase 1
- Eliminar accesos publicos por rol.
- Definir nuevo menu principal.
- Ajustar home con nueva jerarquia.

### Fase 2
- Reordenar paginas de La Facultad.
- Unificar plantillas de programas academicos.
- Mejorar paginas de docentes, proyectos y laboratorios.

### Fase 3
- Reubicar Transferencia Tecnologica.
- Separar mejor LAJC.
- Ajustar enlaces secundarios y contenidos repetidos.

## 11) Criterio editorial final
Cada pagina debe responder una sola funcion dominante. Si una pagina intenta explicar demasiado, vender un programa, mostrar noticias y listar documentos al mismo tiempo, debe dividirse.

La meta es que cualquier visitante pueda entender el sitio en menos de tres clics desde la home.
