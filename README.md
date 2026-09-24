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


## Referencias

[1] Plotly. (2026). *Dash Python User Guide*. https://dash.plotly.com/

[2] Binder Project. (2026). *Get started with Binder*. https://mybinder.readthedocs.io/en/latest/introduction.html

[3] The Turing Way Community. (2021). *Zero-to-Binder*. https://the-turing-way.netlify.app/communication/binder/zero-to-binder.html
