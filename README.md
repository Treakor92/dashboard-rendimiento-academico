# Dashboard de rendimiento académico

Este proyecto presenta un **dashboard interactivo en español** para explorar la relación entre las horas semanales de estudio y el puntaje de un examen. La aplicación continúa el análisis estadístico de las actividades anteriores e integra filtros, contraste de hipótesis, regresión, diagnóstico, clasificación logística y experimentación controlada con hiperparámetros.

> La muestra contiene 100 registros simulados y se utiliza con fines académicos y demostrativos. Los resultados describen asociación estadística, no causalidad ni evidencia generalizable sobre estudiantes reales.

## Contenido del repositorio

| Archivo o carpeta | Propósito |
|---|---|
| `app.py` | Aplicación Dash, modelos, gráficos y callbacks. |
| `datos_estudiantes.csv` | Muestra reproducible procedente del taller anterior. |
| `assets/style.css` | Estética de plano arquitectónico y diseño adaptable. |
| `requirements.txt` | Dependencias de Python para instalación local y Binder. |
| `runtime.txt` | Versión de Python solicitada para el entorno reproducible. |
| `start` y `postBuild` | Inicio automático de la aplicación dentro de Binder. |
| `Procfile` | Comando de ejecución con Gunicorn para servicios compatibles. |
| `enlaces.txt` | URLs de GitHub y Binder exigidas por la actividad. |
| `Informe_proyecto_final.pdf` | Informe académico con evaluación, experimentos y conclusiones. |
| `notebooks/` | Taller anterior y análisis estadístico ejecutado. |
| `test_app.py` | Pruebas automáticas de datos, modelos y callbacks. |

## Ejecución local con Anaconda

Abre **Anaconda Prompt** y ejecuta los siguientes comandos desde la carpeta del proyecto:

```bash
conda create -n dashboard-academico python=3.11 -y
conda activate dashboard-academico
pip install -r requirements.txt
python app.py
```

Después abre `http://127.0.0.1:8050` en el navegador. Para detener el servidor, vuelve a la terminal y presiona `Ctrl + C`.

Para verificar los cálculos antes de ejecutar el dashboard, utiliza:

```bash
python test_app.py
```

## Uso desde JupyterLab o Anaconda Navigator

Desde **Anaconda Navigator**, inicia JupyterLab y navega hasta la carpeta del proyecto. En el panel izquierdo puedes abrir `notebooks/taller_anterior.ipynb` y `notebooks/analisis_estadistico_ejecutado.ipynb`; después selecciona **Kernel → Restart Kernel and Run All Cells** para ejecutar el proceso completo.

Para abrir el dashboard sin salir de JupyterLab, crea una terminal desde **File → New → Terminal** y ejecuta:

```bash
conda activate dashboard-academico
python app.py
```

Mantén esa terminal abierta y visita `http://127.0.0.1:8050` en otra pestaña del navegador. Se recomienda iniciar Dash desde la terminal de JupyterLab y no desde una celda, porque el servidor debe permanecer activo mientras se utiliza la interfaz.

## Publicación en GitHub

1. Crea un repositorio público llamado `dashboard-rendimiento-academico`.
2. Sube todos los archivos de esta carpeta sin modificar su estructura.
3. Confirma que `app.py`, `requirements.txt`, `start`, `postBuild` y `datos_estudiantes.csv` estén en la raíz.
4. Confirma que `enlaces.txt` conserve el usuario `Treakor92` y comprueba los dos enlaces.

## Visualización en Binder

Binder necesita un repositorio público, el código y archivos que describan el entorno. Este proyecto incluye esos componentes [2]. Cuando el repositorio esté publicado, utiliza la dirección:

```text
https://mybinder.org/v2/gh/Treakor92/dashboard-rendimiento-academico/HEAD?urlpath=proxy/8050/
```

La primera construcción puede tardar varios minutos. Binder instalará las dependencias, ejecutará el archivo `start`, iniciará Dash en el puerto 8050 y mantendrá activo Jupyter en el puerto 8888. El script `start` debe conservar `exec "$@"`, porque esa instrucción permite que Binder complete el lanzamiento de la sesión.

## Interacciones disponibles

El dashboard filtra en tiempo real por rango de horas, rango de puntaje y condición académica. La selección actualiza las tarjetas de resumen, histogramas, dispersión, tendencia y diagnóstico de residuos. El umbral de clasificación modifica la matriz de confusión y las métricas. Los selectores de `C` y `solver` muestran los resultados de los experimentos de regresión logística.

## Referencias

[1] Plotly. (2026). *Dash Python User Guide*. https://dash.plotly.com/

[2] Binder Project. (2026). *Get started with Binder*. https://mybinder.readthedocs.io/en/latest/introduction.html

[3] The Turing Way Community. (2021). *Zero-to-Binder*. https://the-turing-way.netlify.app/communication/binder/zero-to-binder.html
