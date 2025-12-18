# Curso de Geoestadística

Curso de geoestadística con sciData - Análisis espacial de datos criminológicos en México

## Descripción del Proyecto

Este proyecto implementa análisis geoestadístico de datos de criminalidad en México, específicamente enfocado en homicidios dolosos. Utiliza herramientas de Python para el procesamiento, análisis y visualización de datos geoespaciales.

## Estructura del Proyecto

```
geostatistic-course/
├── src/
│   ├── config.py          # Configuración de rutas y archivos
│   ├── main.py            # Archivo principal de ejecución
│   ├── session_2.py       # Análisis de homicidios dolosos por entidad
│   └── session_3.py       # Análisis avanzados (en desarrollo)
├── notebooks/
│   ├── session_2.ipynb    # Notebook interactivo sesión 2
│   └── session_3.ipynb    # Notebook interactivo sesión 3
├── data/
│   ├── IDFC_oct2025.csv   # Datos de incidencia delictiva
│   └── maps/
│       └── mexico/
│           └── 00ent.shp  # Shapefile de entidades federativas
└── README.md
```

## Funcionalidades

### Sesión 2 - Análisis de Homicidios Dolosos
- **Carga y procesamiento** de datos de incidencia delictiva del fuero común (IDFC)
- **Filtrado** de datos por tipo de delito (homicidio doloso)
- **Agregación** de datos por año, entidad federativa
- **Visualización geoespacial** mediante mapas coropletas
- **Merge de datos** geográficos con estadísticas criminales

### Características Técnicas
- Manejo de encodings específicos (`cp1252`) para datos mexicanos
- Resolución automática de incompatibilidades de tipos de datos en merges
- Agregación temporal por meses del año
- Compatibilidad con shapefiles del INEGI

## Instalación y Configuración

### Requisitos
- Python 3.8+
- Bibliotecas principales:
  - `pandas` - Manipulación de datos
  - `geopandas` - Análisis geoespacial
  - `matplotlib` - Visualización
  - `jupyter` - Notebooks interactivos

### Instalación
```bash
# Clonar el repositorio
git clone <repository-url>
cd geostatistic-course

# Instalar dependencias (si usas uv)
uv sync

# O con pip tradicional
pip install pandas geopandas matplotlib jupyter
```

### Estructura de Datos Requerida
1. **IDFC_oct2025.csv**: Archivo de incidencia delictiva con columnas:
   - `Subtipo de delito`
   - `Año`
   - `Clave_Ent`
   - `Entidad`
   - Columnas mensuales (Enero, Febrero, ..., Diciembre)

2. **00ent.shp**: Shapefile de entidades federativas con:
   - `CVE_ENT`: Clave de entidad
   - `NOMGEO`: Nombre geográfico

## Uso

### Ejecución de Scripts
```bash
# Análisis básico de homicidios dolosos
python src/session_2.py

# Script principal (en desarrollo)
python src/main.py
```

### Notebooks Interactivos
```bash
# Iniciar Jupyter
jupyter notebook

# Abrir notebooks específicos
notebooks/session_2.ipynb
notebooks/session_3.ipynb
```

## Solución de Problemas Comunes

### Error de Merge de Tipos de Datos
**Problema**: "You are trying to merge on object and int64 columns"

**Solución Implementada**: Conversión automática de tipos de datos antes del merge:
```python
# Convertir ambas columnas a string para compatibilidad
map_["CVE_ENT"] = map_["CVE_ENT"].astype(str)
data_total_hom[Columns.CLAVE_ENT] = data_total_hom[Columns.CLAVE_ENT].astype(str)
```

### Problemas de Encoding
**Problema**: Caracteres especiales no se muestran correctamente

**Solución**: Usar encoding `cp1252` para archivos CSV mexicanos:
```python
data = pd.read_csv(Config.IDFC, encoding="cp1252")
```

## Mejoras Recientes

### Versión Actual
- ✅ **Corregido**: Error de tipos de datos en merge de mapas
- ✅ **Corregido**: Asignación faltante en operación groupby
- ✅ **Mejorado**: Organización del código y legibilidad
- ✅ **Añadido**: Documentación completa del proyecto

### Próximas Mejoras
- [ ] Análisis temporal de tendencias
- [ ] Mapas de calor interactivos
- [ ] Análisis de autocorrelación espacial
- [ ] Indicadores estadísticos avanzados

## Contribución

Para contribuir al proyecto:
1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto es parte del curso de geoestadística con sciData.

## Contacto

Para preguntas sobre el curso o el proyecto, contactar con sciData.
