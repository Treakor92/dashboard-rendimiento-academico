#import "report-theme.typ": report-accent, report-theme
#import "@preview/glossarium:0.5.10": make-glossary, register-glossary, print-glossary, gls

#show: report-theme.with(
  title: "Dashboard de rendimiento académico",
  author: "Daniel Alfonso Rozo Briceño",
  rhythm: "report",
  running-header: true,
)

#show: make-glossary

#let terms = (
  (
    key: "mse",
    short: "MSE",
    long: "error cuadrático medio",
    description: "Promedio del cuadrado de las diferencias entre los valores observados y los valores predichos.",
  ),
  (
    key: "r2",
    short: "R²",
    long: "coeficiente de determinación",
    description: "Proporción de la variabilidad de la respuesta explicada por el modelo de regresión.",
  ),
  (
    key: "solver",
    short: "solver",
    long: "algoritmo de optimización",
    description: "Procedimiento numérico utilizado para estimar los coeficientes de la regresión logística.",
  ),
  (
    key: "callback",
    short: "callback",
    long: "función reactiva",
    description: "Función que recibe cambios en los controles del dashboard y actualiza automáticamente sus salidas.",
  ),
  (
    key: "binder",
    short: "Binder",
    long: "entorno Binder reproducible",
    description: "Servicio que construye un entorno ejecutable en la nube a partir de un repositorio público y sus archivos de configuración.",
  ),
)
#register-glossary(terms)

#let info-box(title, body) = block(
  width: 100%,
  fill: rgb("eef5f9"),
  stroke: 0.7pt + rgb("85a9ba"),
  inset: 12pt,
  radius: 2pt,
  breakable: true,
  [
    #text(fill: report-accent, weight: "bold")[#title]
    #v(4pt)
    #body
  ],
)

// ---------- Portada ----------
#page(margin: (top: 24%, x: 2.2cm), numbering: none, header: none)[
  #set par(first-line-indent: 0em)
  #align(center)[
    #text(size: 10pt, weight: "semibold", fill: luma(100))[BASES DE DATOS 2 · PROYECTO FINAL]
    #v(1.1em)
    #text(size: 27pt, weight: "bold", fill: report-accent)[Dashboard de rendimiento académico]
    #v(0.55em)
    #text(size: 14pt, fill: luma(75))[Evaluación, mejora de modelos y visualización interactiva]
    #v(2em)
    #line(length: 48%, stroke: 0.7pt + luma(145))
    #v(2em)
    #text(size: 12pt)[
      *Estudiante:* Daniel Alfonso Rozo Briceño \
      *Fecha:* #datetime.today().display("[day] de [month repr:long] de [year]")
    ]
    #v(3em)
    #text(size: 9pt, fill: luma(100))[Aplicación desarrollada con Python, Dash, Plotly, Pandas, SciPy y scikit-learn]
  ]
]

// ---------- Contenido ----------
#page(numbering: none, header: none)[
  #outline(title: [Contenido], indent: 1.4em)
]

#page(numbering: none, header: none)[
  #text(size: 18pt, weight: "bold", fill: report-accent)[Lista de figuras y tablas]
  #v(1.2em)
  *Figura 1.* Vista principal de la aplicación Dash con filtros, indicadores y distribuciones.

  *Tabla 1.* Variables y uso analítico.

  *Tabla 2.* Comparación de modelos de regresión.

  *Tabla 3.* Experimentos de regresión logística.

  *Tabla 4.* Archivos de reproducibilidad y publicación.
]

#counter(page).update(1)

= Introducción

El proyecto consolida el proceso desarrollado en las actividades anteriores sobre la relación entre las horas semanales de estudio y el puntaje obtenido en un examen. La muestra contiene 100 observaciones simuladas y fue construida con una semilla fija para conservar la reproducibilidad. El análisis preliminar mostró una asociación positiva fuerte entre ambas variables, lo cual justificó avanzar desde la exploración descriptiva hacia el contraste de hipótesis, la predicción continua y la clasificación de la condición de aprobación.

La solución final adopta un enfoque de producto analítico. Además de evaluar y mejorar los modelos, transforma los resultados en un dashboard interactivo completamente en español. La aplicación fue construida con Dash, framework de Python para aplicaciones de datos [1], e integra gráficos de Plotly, procesamiento con Pandas y estimación con SciPy y scikit-learn. Los controles permiten cambiar rangos y umbrales sin modificar el código, mientras que las #gls("callback") recalculan métricas y visualizaciones.

#info-box(
  "Pregunta de investigación",
  [¿En qué medida las horas semanales de estudio se relacionan con el puntaje del examen y qué tan útil es esta variable para predecir el desempeño académico y la condición de aprobación?],
)

== Justificación

Un reporte estático permite documentar resultados, pero limita la exploración de escenarios. El dashboard amplía el análisis al ofrecer filtros, comparación de modelos y modificación del umbral de clasificación. Esta característica es relevante porque métricas como sensibilidad y especificidad cambian según la decisión operativa. La interfaz hace visible dicho intercambio y evita presentar una única cifra como si fuera suficiente para evaluar el modelo.

= Objetivos

== Objetivo general

Desarrollar y documentar un dashboard interactivo que permita evaluar, comparar y comunicar modelos estadísticos aplicados al rendimiento académico, manteniendo un flujo reproducible desde los datos hasta la publicación en GitHub y Binder.

== Objetivos específicos

- Evaluar la relación entre las horas de estudio y el puntaje mediante correlación, contraste de hipótesis y regresión.
- Comparar una regresión lineal simple, una especificación polinómica de grado tres y una variante regularizada con Ridge.
- Entrenar modelos de regresión logística y experimentar de forma controlada con los valores de `C` y los solvers `liblinear` y `lbfgs`.
- Implementar filtros dinámicos, histogramas, dispersión con tendencia, diagnóstico de residuos, curva logística y matriz de confusión.
- Documentar las limitaciones de los datos simulados y proponer variables y validaciones para una etapa posterior.
- Preparar los archivos necesarios para ejecutar el proyecto en Anaconda, publicarlo en GitHub y abrirlo en Binder.

= Datos y preparación

La base contiene las variables originales `Horas_Estudio_Semana` y `Puntaje_Examen`. La variable binaria `Aprobado` se construyó con un umbral de 70 puntos. Para la comparación de regresiones se añadieron términos cuadrático y cúbico de las horas. Estos términos permiten representar curvatura, pero no deben interpretarse como nuevas mediciones independientes.

#table(
  columns: (1.3fr, 1fr, 2.3fr),
  inset: 7pt,
  stroke: 0.5pt + luma(190),
  table.header(
    [*Variable*], [*Tipo*], [*Uso en el proyecto*],
  ),
  [`Horas_Estudio_Semana`], [Continua], [Variable explicativa principal y base de los términos polinómicos.],
  [`Puntaje_Examen`], [Continua], [Variable objetivo de los modelos de regresión.],
  [`Aprobado`], [Binaria], [Objetivo de clasificación: 1 si el puntaje es mayor o igual a 70; 0 en caso contrario.],
  [`Horas²` y `Horas³`], [Derivadas], [Características usadas para explorar relaciones no lineales.],
)

El control de calidad verificó 100 filas, ausencia de valores perdidos y puntajes dentro del rango de 0 a 100. La semilla `42` se mantiene en la división de datos y en la validación cruzada para que los resultados puedan reproducirse.

```python
df = pd.read_csv("datos_estudiantes.csv")
df["Aprobado"] = (df["Puntaje_Examen"] >= 70).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)
```

= Procedimiento estadístico

== Contraste de hipótesis

Se plantea un contraste bilateral sobre la pendiente poblacional de la regresión lineal:

$ H_0: beta_1 = 0 quad "frente a" quad H_1: beta_1 != 0 $

La estimación de la pendiente fue $hat(beta)_1 = 2.9923$, con un valor p de $2.45739 times 10^(-36)$ y un intervalo de confianza del 95 % entre 2.6951 y 3.2895. Como el valor p es menor que $alpha = 0.05$, se rechaza la hipótesis nula. En la muestra, una hora semanal adicional se asocia con un aumento promedio cercano a tres puntos en el examen.

La correlación de Pearson fue $r = 0.8961$, lo que indica una asociación lineal positiva fuerte. Sin embargo, el diseño simulado y observacional impide concluir que aumentar las horas sea la causa directa del cambio en el puntaje.

== Regresión y regularización

Se compararon tres especificaciones con la misma división de entrenamiento y prueba del 70/30. La regresión lineal simple sirve como referencia interpretable. La variante polinómica incorpora $x$, $x^2$ y $x^3$. El modelo Ridge utiliza las mismas características y añade una penalización cuadrática:

$ min_beta sum_(i=1)^n (y_i - hat(y)_i)^2 + lambda sum_(j=1)^p beta_j^2 $

La penalización reduce la magnitud de los coeficientes y ayuda a controlar la variabilidad de modelos con características correlacionadas. Se evaluó cada alternativa mediante #gls("mse") y #gls("r2") sobre el conjunto de prueba.

== Regresión logística

La probabilidad de aprobación se modeló con la función logística:

$ P(Y=1 | x) = 1 / (1 + e^(-(beta_0 + beta_1 x))) $

Se probaron `C = 0.1`, `1.0` y `10.0` con los #gls("solver") `liblinear` y `lbfgs`. En scikit-learn, valores pequeños de `C` implican mayor regularización. Cada configuración se comparó con validación cruzada estratificada de cinco particiones y luego se evaluó en el conjunto de prueba.

```python
for c in (0.1, 1.0, 10.0):
    for solver in ("liblinear", "lbfgs"):
        modelo = LogisticRegression(
            C=c, solver=solver, max_iter=2000, random_state=42
        )
        scores = cross_val_score(modelo, X_train, y_train, cv=cv)
```

= Resultados y experimentos

== Comparación de regresiones

#table(
  columns: (1.8fr, 1fr, 1fr, 2.2fr),
  inset: 7pt,
  stroke: 0.5pt + luma(190),
  table.header([*Modelo*], [*MSE*], [*R²*], [*Interpretación*]),
  [Lineal simple], [21.330], [0.749], [Referencia de baja complejidad e interpretación directa.],
  [Polinómico grado 3], [19.930], [0.766], [Mejora el error al representar una curvatura moderada.],
  [Ridge polinómico], [19.597], [0.770], [Obtiene el mejor resultado y controla los coeficientes mediante penalización.],
)

La regularización Ridge ofrece la mejor combinación de #gls("mse") y #gls("r2") en la partición utilizada. La mejora frente al modelo polinómico sin penalización es pequeña, por lo cual la conclusión prudente es que la regularización estabiliza la especificación más compleja, no que garantiza una superioridad general. La comparación debe repetirse con nuevas particiones y datos externos.

== Experimentos de clasificación

#table(
  columns: (0.65fr, 1fr, 1.1fr, 1fr, 1fr, 1fr),
  inset: 5.5pt,
  table.header([*C*], [*Solver*], [*Validación*], [*Accuracy*], [*Sens.*], [*Espec.*]),
  [0.1], [liblinear], [60.0 %], [63.3 %], [100.0 %], [15.4 %],
  [0.1], [lbfgs], [87.1 %], [76.7 %], [76.5 %], [76.9 %],
  [1.0], [liblinear], [81.4 %], [73.3 %], [94.1 %], [46.2 %],
  [1.0], [lbfgs], [85.7 %], [76.7 %], [76.5 %], [76.9 %],
  [10.0], [liblinear], [88.6 %], [80.0 %], [88.2 %], [69.2 %],
  [10.0], [lbfgs], [85.7 %], [76.7 %], [76.5 %], [76.9 %],
)

La configuración seleccionada fue `C = 10.0` con `liblinear`, debido a que obtuvo la mayor exactitud media de validación cruzada, 88.6 %. En el conjunto de prueba alcanzó 80.0 % de exactitud, 88.2 % de sensibilidad y 69.2 % de especificidad. La matriz de confusión fue $[[9, 4], [2, 15]]$, siguiendo el orden verdadero negativo, falso positivo, falso negativo y verdadero positivo.

#info-box(
  "Lectura del umbral",
  [El dashboard incluye un control entre 0.20 y 0.80. Disminuir el umbral suele aumentar la sensibilidad y también los falsos positivos; aumentarlo suele mejorar la especificidad, pero puede dejar más aprobados sin detectar. La elección final depende del costo de cada tipo de error.],
)

== Interfaz desarrollada

La aplicación distribuye el análisis en cinco módulos: panorama, relación, clasificación, modelos y memoria técnica. Su estética de plano arquitectónico utiliza fondo azul real, cuadrícula técnica, marcos rectangulares, líneas de dimensión, tipografía sans serif de alto contraste y etiquetas monoespaciadas. Esta dirección visual diferencia el proyecto de un tablero genérico y refuerza la idea de instrumento de medición.

#figure(
  image("dashboard_portada.webp", width: 100%),
  caption: [Vista principal de la aplicación Dash con filtros, indicadores y distribuciones.],
) <fig-dashboard>

Los filtros de horas, puntaje y condición actualizan las tarjetas, histogramas, dispersión, pendiente y residuos. Un control independiente modifica el umbral de clasificación. Finalmente, dos selectores permiten revisar de manera controlada las seis combinaciones de `C` y #gls("solver").

```python
@callback(
    Output("kpi-total", "children"),
    Output("grafico-dispersion", "figure"),
    Input("filtro-horas", "value"),
    Input("filtro-puntaje", "value"),
    Input("filtro-condicion", "value"),
)
def actualizar_exploracion(rango_horas, rango_puntaje, condicion):
    # Filtrado y reconstrucción de las salidas
    ...
```

= Reproducibilidad, GitHub y Binder

El repositorio incorpora el código, los datos y los archivos de configuración requeridos para reconstruir el entorno. La documentación oficial indica que un repositorio listo para #gls("binder") debe contener el material ejecutable y la descripción de sus dependencias [2]. La guía Zero-to-Binder recomienda utilizar un repositorio público, fijar las dependencias y compartir el enlace generado por `mybinder.org` [3].

#table(
  columns: (1.35fr, 2.8fr),
  inset: 7pt,
  stroke: 0.5pt + luma(190),
  table.header([*Archivo*], [*Función*]),
  [`app.py`], [Aplicación, callbacks, modelos y servidor WSGI.],
  [`datos_estudiantes.csv`], [Muestra reproducible utilizada en el taller anterior.],
  [`requirements.txt`], [Versiones de Dash, Plotly, Pandas, SciPy, scikit-learn, Gunicorn y el proxy de Jupyter.],
  [`assets/style.css`], [Estilos de plano arquitectónico y adaptación a distintos tamaños.],
  [`start` y `postBuild`], [Permisos e inicio de Dash en el puerto 8050 para Binder.],
  [`enlaces.txt`], [URLs del repositorio y del dashboard público.],
)

== Ejecución con Anaconda

```bash
conda create -n dashboard-academico python=3.11 -y
conda activate dashboard-academico
pip install -r requirements.txt
python app.py
```

La aplicación se abre en `http://127.0.0.1:8050`. La prueba local confirmó respuesta HTTP 200 para la página principal y la hoja de estilos. También se ejecutaron cinco pruebas automatizadas sobre la muestra, la comparación de modelos y las salidas de los callbacks.

== Publicación requerida

La entrega incorpora el usuario de GitHub `Treakor92`. Después de subir la carpeta a un repositorio público llamado `dashboard-rendimiento-academico`, los enlaces definitivos son:

```text
GitHub: https://github.com/Treakor92/dashboard-rendimiento-academico
Binder: https://mybinder.org/v2/gh/Treakor92/dashboard-rendimiento-academico/HEAD?urlpath=proxy/8050/
```

El primer inicio puede tardar mientras Binder construye la imagen y descarga las dependencias. El repositorio no debe contener contraseñas, tokens ni archivos privados [2].

= Limitaciones y recomendaciones

La principal limitación es el origen simulado de la información. Una correlación fuerte dentro de una muestra generada no garantiza el mismo comportamiento en un grupo real. Además, la base original solo contiene una variable explicativa observada. Los términos cuadrático y cúbico dependen de la misma medición y, por ello, no sustituyen variables como asistencia, desempeño previo, sueño, carga laboral, conectividad o estrategias de aprendizaje.

El tamaño de 100 observaciones también restringe la estabilidad de una clasificación. Las métricas cambian según la partición, el hiperparámetro y el umbral. En un uso institucional sería necesario realizar validación externa, revisar la calibración de probabilidades, estudiar el desempeño por subgrupos y documentar el costo de falsos positivos y falsos negativos.

Para una siguiente fase se recomienda recopilar datos reales con consentimiento y reglas de protección, ampliar las variables explicativas, comparar técnicas adicionales y conservar una línea base interpretable. El dashboard debería continuar como herramienta de apoyo analítico, nunca como única fuente para decisiones sobre estudiantes.

= Conclusiones

El contraste de hipótesis confirmó una asociación estadísticamente significativa entre las horas de estudio y el puntaje del examen. La pendiente estimada indica un incremento promedio cercano a tres puntos por hora semanal adicional, y la correlación de 0.8961 respalda una relación positiva fuerte dentro de la muestra.

La comparación de regresiones mostró que el modelo Ridge polinómico obtuvo el menor error de prueba y el mayor #gls("r2"), aunque la mejora frente a la regresión polinómica sin penalización fue moderada. Este resultado justifica conservar la regularización como mecanismo de control, sin afirmar una ventaja universal.

En clasificación, `C = 10.0` y `liblinear` ofrecieron el mejor promedio de validación cruzada. El desempeño de prueba fue razonable, con mayor sensibilidad que especificidad. El control interactivo del umbral permite comunicar que estas métricas dependen de una decisión y no son propiedades invariables del modelo.

El producto final cumple el propósito académico al unir código, resultados, narrativa y reproducibilidad. La estructura incluye los componentes exigidos para ejecución local, publicación en GitHub y apertura en Binder. No obstante, los hallazgos deben entenderse como demostración del procedimiento analítico basada en datos simulados.

= Glosario

#print-glossary(terms, show-all: true, disable-back-references: true)

= Referencias

[1] Plotly. (2026). _Dash Python User Guide_. #link("https://dash.plotly.com/")[https://dash.plotly.com/]

[2] Binder Project. (2026). _Get started with Binder_. #link("https://mybinder.readthedocs.io/en/latest/introduction.html")[https://mybinder.readthedocs.io/en/latest/introduction.html]

[3] The Turing Way Community. (2021). _Zero-to-Binder_. #link("https://the-turing-way.netlify.app/communication/binder/zero-to-binder.html")[https://the-turing-way.netlify.app/communication/binder/zero-to-binder.html]

[4] SciPy Community. (2026). _scipy.stats.linregress_. #link("https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html")[Documentación oficial de SciPy]

[5] scikit-learn developers. (2026). _LinearRegression_. #link("https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html")[Documentación oficial]

[6] scikit-learn developers. (2026). _LogisticRegression_. #link("https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html")[Documentación oficial]

[7] McKinney, W. (2022). _Python for Data Analysis_ (3.ª ed.). O'Reilly Media.
