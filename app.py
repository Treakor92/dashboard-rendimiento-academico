import os
from pathlib import Path

import dash
from dash import Dash, Input, Output, callback, dash_table, dcc, html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import accuracy_score, confusion_matrix, mean_squared_error, r2_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "datos_estudiantes.csv"
UMBRAL_APROBACION = 70
RANDOM_STATE = 42

df = pd.read_csv(DATA_PATH)
df.insert(0, "ID", np.arange(1, len(df) + 1))
df["Aprobado"] = (df["Puntaje_Examen"] >= UMBRAL_APROBACION).astype(int)
df["Condicion"] = np.where(df["Aprobado"].eq(1), "Aprobado", "No aprobado")


def tema_figura(fig, titulo, alto=360):
    fig.update_layout(
        title={"text": titulo.upper(), "x": 0.02, "xanchor": "left"},
        height=alto,
        margin=dict(l=45, r=25, t=65, b=45),
        paper_bgcolor="rgba(7,40,75,0.72)",
        plot_bgcolor="rgba(7,40,75,0.20)",
        font=dict(family="Manrope, sans-serif", color="#eefaff", size=11),
        title_font=dict(family="IBM Plex Mono, monospace", color="#ffffff", size=14),
        hoverlabel=dict(bgcolor="#062546", bordercolor="#9ce7ff", font_color="white"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(gridcolor="rgba(198,235,255,.12)", linecolor="rgba(198,235,255,.35)")
    fig.update_yaxes(gridcolor="rgba(198,235,255,.12)", linecolor="rgba(198,235,255,.35)")
    return fig


def ajustar_lineal(datos):
    if len(datos) < 2 or datos["Horas_Estudio_Semana"].nunique() < 2:
        return {"pendiente": 0.0, "intercepto": 0.0, "r": 0.0, "r2": 0.0, "mse": 0.0}
    resultado = stats.linregress(datos["Horas_Estudio_Semana"], datos["Puntaje_Examen"])
    predicho = resultado.intercept + resultado.slope * datos["Horas_Estudio_Semana"]
    return {
        "pendiente": resultado.slope,
        "intercepto": resultado.intercept,
        "r": resultado.rvalue,
        "r2": resultado.rvalue**2,
        "mse": mean_squared_error(datos["Puntaje_Examen"], predicho),
        "p": resultado.pvalue,
    }


def comparar_regresiones(datos):
    X = datos[["Horas_Estudio_Semana"]]
    y = datos["Puntaje_Examen"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=RANDOM_STATE
    )
    modelos = {
        "Lineal simple": LinearRegression(),
        "Polinómico grado 3": Pipeline(
            [("polinomio", PolynomialFeatures(degree=3, include_bias=False)), ("modelo", LinearRegression())]
        ),
        "Ridge polinómico": Pipeline(
            [
                ("polinomio", PolynomialFeatures(degree=3, include_bias=False)),
                ("escala", StandardScaler()),
                ("modelo", Ridge(alpha=8.0)),
            ]
        ),
    }
    filas = []
    for nombre, modelo in modelos.items():
        modelo.fit(X_train, y_train)
        prediccion = modelo.predict(X_test)
        filas.append(
            {
                "Modelo": nombre,
                "MSE": round(mean_squared_error(y_test, prediccion), 3),
                "R2": round(r2_score(y_test, prediccion), 3),
            }
        )
    return pd.DataFrame(filas)


def experimentar_logistica(datos):
    X = datos[["Horas_Estudio_Semana"]]
    y = datos["Aprobado"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=RANDOM_STATE, stratify=y
    )
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    filas = []
    modelos = {}
    for c in (0.1, 1.0, 10.0):
        for solver in ("liblinear", "lbfgs"):
            modelo = LogisticRegression(
                C=c, solver=solver, max_iter=2000, random_state=RANDOM_STATE
            )
            modelo.fit(X_train, y_train)
            scores = cross_val_score(modelo, X_train, y_train, cv=cv, scoring="accuracy")
            prediccion = modelo.predict(X_test)
            vn, fp, fn, vp = confusion_matrix(y_test, prediccion, labels=[0, 1]).ravel()
            filas.append(
                {
                    "C": c,
                    "Solver": solver,
                    "Validacion": scores.mean(),
                    "Exactitud": accuracy_score(y_test, prediccion),
                    "Sensibilidad": vp / (vp + fn) if vp + fn else 0,
                    "Especificidad": vn / (vn + fp) if vn + fp else 0,
                }
            )
            modelos[(c, solver)] = modelo
    return pd.DataFrame(filas), modelos


comparacion_regresion = comparar_regresiones(df)
experimentos, modelos_logisticos = experimentar_logistica(df)
mejor_experimento = experimentos.sort_values("Validacion", ascending=False).iloc[0]


app = Dash(__name__, title="Plano analítico | Rendimiento académico", suppress_callback_exceptions=True)
server = app.server


def tarjeta_metrica(etiqueta, identificador, detalle):
    return html.Div(
        [
            html.Div(etiqueta, className="technical-label"),
            html.Div("—", id=identificador, className="metric-value"),
            html.P(detalle, className="metric-detail"),
        ],
        className="metric-card technical-panel",
    )


app.layout = html.Div(
    [
        html.Aside(
            [
                html.Div(
                    [
                        html.Div("△", className="brand-mark"),
                        html.Div(
                            [
                                html.Span("PLANO ANALÍTICO", className="technical-label"),
                                html.Strong("RENDIMIENTO 02"),
                            ],
                            className="brand-copy",
                        ),
                    ],
                    className="brand",
                ),
                html.Nav(
                    [
                        html.A("A–01  Panorama", href="#panorama"),
                        html.A("B–02  Relación", href="#relacion"),
                        html.A("C–03  Clasificación", href="#clasificacion"),
                        html.A("D–04  Modelos", href="#modelos"),
                        html.A("E–05  Metodología", href="#metodologia"),
                    ]
                ),
                html.Div(
                    [html.Span("ARCHIVO", className="technical-label"), html.Strong("PRJ–ACA–02"), html.Small("REV.03 / 2026")],
                    className="side-stamp",
                ),
            ],
            className="sidebar",
        ),
        html.Main(
            [
                html.Header(
                    [
                        html.Div(
                            [
                                html.Div([html.Span("MODELO VALIDADO"), html.Span("N = 100")], className="eyebrow-row"),
                                html.H1(["PLANO ANALÍTICO DEL ", html.Em("RENDIMIENTO ACADÉMICO")]),
                                html.P(
                                    "Exploración reproducible de la relación entre horas semanales de estudio y puntaje del examen, con contraste de hipótesis, regresión y clasificación binaria."
                                ),
                            ],
                            className="hero-copy",
                        ),
                        html.Div(
                            [
                                html.Div("PREGUNTA CENTRAL", className="dimension-label"),
                                html.P("¿Cómo cambia el desempeño académico cuando aumenta la dedicación semanal al estudio independiente?"),
                            ],
                            className="hero-question",
                        ),
                    ],
                    className="hero technical-panel",
                ),
                html.Section(
                    [
                        html.Div(
                            [
                                html.Div([html.Label("RANGO DE HORAS"), html.Span(id="etiqueta-horas")], className="filter-heading"),
                                dcc.RangeSlider(2, 19, 1, value=[2, 19], id="filtro-horas", tooltip={"placement": "bottom"}),
                            ],
                            className="filter-control",
                        ),
                        html.Div(
                            [
                                html.Div([html.Label("RANGO DE PUNTAJE"), html.Span(id="etiqueta-puntaje")], className="filter-heading"),
                                dcc.RangeSlider(45, 100, 1, value=[45, 100], id="filtro-puntaje", tooltip={"placement": "bottom"}),
                            ],
                            className="filter-control",
                        ),
                        html.Div(
                            [
                                html.Label("CONDICIÓN ACADÉMICA"),
                                dcc.Dropdown(
                                    options=[
                                        {"label": "Todos", "value": "Todos"},
                                        {"label": "Aprobado", "value": "Aprobado"},
                                        {"label": "No aprobado", "value": "No aprobado"},
                                    ],
                                    value="Todos",
                                    clearable=False,
                                    id="filtro-condicion",
                                ),
                            ],
                            className="filter-control",
                        ),
                    ],
                    className="filters technical-panel",
                ),
                html.Section(
                    [
                        html.Div([html.Div("A–01 / RESUMEN", className="technical-label"), html.H2("PANORAMA FILTRADO"), html.P("Los indicadores y gráficos responden a los filtros activos.")], className="section-heading"),
                        html.Div(
                            [
                                tarjeta_metrica("OBSERVACIONES", "kpi-total", "Registros dentro de la selección."),
                                tarjeta_metrica("HORAS PROMEDIO", "kpi-horas", "Dedicación semanal media."),
                                tarjeta_metrica("PUNTAJE PROMEDIO", "kpi-puntaje", "Media en escala de 0 a 100."),
                                tarjeta_metrica("TASA DE APROBACIÓN", "kpi-tasa", "Puntajes iguales o superiores a 70."),
                            ],
                            className="metric-grid",
                        ),
                        html.Div([dcc.Graph(id="grafico-horas"), dcc.Graph(id="grafico-puntajes")], className="chart-grid two"),
                    ],
                    id="panorama",
                    className="section",
                ),
                html.Section(
                    [
                        html.Div([html.Div("B–02 / INFERENCIA", className="technical-label"), html.H2("RELACIÓN Y DIAGNÓSTICO"), html.P("La pendiente y el ajuste se recalculan con la selección activa.")], className="section-heading"),
                        html.Div(
                            [
                                dcc.Graph(id="grafico-dispersion"),
                                html.Div(
                                    [
                                        tarjeta_metrica("CORRELACIÓN", "kpi-correlacion", "Coeficiente de Pearson."),
                                        tarjeta_metrica("R²", "kpi-r2", "Variabilidad explicada."),
                                        tarjeta_metrica("MSE", "kpi-mse", "Error cuadrático medio."),
                                    ],
                                    className="metric-stack",
                                ),
                            ],
                            className="relation-grid",
                        ),
                        dcc.Graph(id="grafico-residuos"),
                    ],
                    id="relacion",
                    className="section",
                ),
                html.Section(
                    [
                        html.Div([html.Div("C–03 / CLASIFICACIÓN", className="technical-label"), html.H2("PROBABILIDAD DE APROBACIÓN"), html.P("El umbral controla el intercambio entre sensibilidad y especificidad.")], className="section-heading"),
                        html.Div(
                            [html.Label("UMBRAL DE CLASIFICACIÓN"), dcc.Slider(0.2, 0.8, 0.05, value=0.5, marks={0.2: "0.20", 0.5: "0.50", 0.8: "0.80"}, id="umbral-clasificacion")],
                            className="threshold-control technical-panel",
                        ),
                        html.Div([dcc.Graph(id="grafico-logistica"), dcc.Graph(id="grafico-matriz")], className="chart-grid logistic"),
                        html.Div(
                            [
                                tarjeta_metrica("EXACTITUD", "kpi-exactitud", "Aciertos totales."),
                                tarjeta_metrica("SENSIBILIDAD", "kpi-sensibilidad", "Detección de aprobados."),
                                tarjeta_metrica("ESPECIFICIDAD", "kpi-especificidad", "Detección de no aprobados."),
                            ],
                            className="metric-grid three",
                        ),
                    ],
                    id="clasificacion",
                    className="section",
                ),
                html.Section(
                    [
                        html.Div([html.Div("D–04 / EXPERIMENTOS", className="technical-label"), html.H2("COMPARACIÓN CONTROLADA"), html.P("Todos los modelos usan una partición 70/30 y semilla fija.")], className="section-heading"),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Label("REGULARIZACIÓN C"),
                                        dcc.Dropdown([0.1, 1.0, 10.0], value=float(mejor_experimento["C"]), clearable=False, id="selector-c"),
                                        html.Label("SOLVER"),
                                        dcc.Dropdown(["liblinear", "lbfgs"], value=mejor_experimento["Solver"], clearable=False, id="selector-solver"),
                                        html.Div(id="resumen-experimento", className="experiment-summary"),
                                    ],
                                    className="experiment-controls technical-panel",
                                ),
                                dash_table.DataTable(
                                    data=comparacion_regresion.to_dict("records"),
                                    columns=[{"name": columna, "id": columna} for columna in comparacion_regresion.columns],
                                    style_table={"overflowX": "auto"},
                                    style_header={"backgroundColor": "#092f58", "color": "#bcecff", "fontFamily": "IBM Plex Mono", "border": "1px solid rgba(255,255,255,.25)"},
                                    style_cell={"backgroundColor": "rgba(8,45,84,.7)", "color": "white", "border": "1px solid rgba(255,255,255,.15)", "padding": "14px", "fontFamily": "Manrope"},
                                ),
                            ],
                            className="models-grid",
                        ),
                    ],
                    id="modelos",
                    className="section",
                ),
                html.Section(
                    [
                        html.Div([html.Div("E–05 / MEMORIA TÉCNICA", className="technical-label"), html.H2("NARRATIVA METODOLÓGICA"), html.P("Resultados, supuestos y próximos pasos se presentan por separado.")], className="section-heading"),
                        html.Div(
                            [
                                html.Article([html.Div("Σ", className="method-icon"), html.H3("HIPÓTESIS"), html.P("H₀: la pendiente poblacional es igual a cero. H₁: la pendiente es diferente de cero. El contraste bilateral del taller anterior obtuvo p < 0.05 y respaldó el rechazo de H₀.")], className="technical-panel"),
                                html.Article([html.Div("{}", className="method-icon"), html.H3("LIMITACIONES"), html.P("Los 100 registros fueron simulados y solo incluyen horas y puntaje. Los términos polinómicos son transformaciones, no mediciones independientes. El resultado no es causal ni generalizable.")], className="technical-panel"),
                                html.Article([html.Div("△", className="method-icon"), html.H3("PRÓXIMO CICLO"), html.P("Recolectar asistencia, promedio previo, sueño y técnicas de estudio; validar en una muestra externa; revisar residuos, calibración y equidad del umbral.")], className="technical-panel"),
                            ],
                            className="method-grid",
                        ),
                        html.Blockquote("Las horas de estudio aportan información predictiva relevante, pero no explican por sí solas el rendimiento. El tablero es un instrumento exploratorio y de comunicación, no un mecanismo automático de decisión individual.", className="technical-panel conclusion"),
                    ],
                    id="metodologia",
                    className="section",
                ),
                html.Footer([html.Span("DANIEL ALFONSO ROZO BRICEÑO · PROYECTO FINAL"), html.Span("DASH / PLOTLY / PANDAS · REV.03")]),
            ],
            className="main-content",
        ),
    ],
    className="app-shell",
)


@callback(
    Output("etiqueta-horas", "children"),
    Output("etiqueta-puntaje", "children"),
    Output("kpi-total", "children"),
    Output("kpi-horas", "children"),
    Output("kpi-puntaje", "children"),
    Output("kpi-tasa", "children"),
    Output("kpi-correlacion", "children"),
    Output("kpi-r2", "children"),
    Output("kpi-mse", "children"),
    Output("grafico-horas", "figure"),
    Output("grafico-puntajes", "figure"),
    Output("grafico-dispersion", "figure"),
    Output("grafico-residuos", "figure"),
    Input("filtro-horas", "value"),
    Input("filtro-puntaje", "value"),
    Input("filtro-condicion", "value"),
)
def actualizar_exploracion(rango_horas, rango_puntaje, condicion):
    datos = df[
        df["Horas_Estudio_Semana"].between(rango_horas[0], rango_horas[1])
        & df["Puntaje_Examen"].between(rango_puntaje[0], rango_puntaje[1])
    ].copy()
    if condicion != "Todos":
        datos = datos[datos["Condicion"].eq(condicion)].copy()

    total = len(datos)
    horas_promedio = datos["Horas_Estudio_Semana"].mean() if total else 0
    puntaje_promedio = datos["Puntaje_Examen"].mean() if total else 0
    tasa = datos["Aprobado"].mean() if total else 0
    modelo = ajustar_lineal(datos)

    fig_horas = go.Figure(go.Histogram(x=datos["Horas_Estudio_Semana"], nbinsx=9, marker_color="#9ce7ff"))
    tema_figura(fig_horas, "Distribución de horas")
    fig_horas.update_xaxes(title="Horas semanales")
    fig_horas.update_yaxes(title="Frecuencia")

    fig_puntaje = go.Figure(go.Histogram(x=datos["Puntaje_Examen"], nbinsx=9, marker_color="#ffd166"))
    tema_figura(fig_puntaje, "Distribución de puntajes")
    fig_puntaje.update_xaxes(title="Puntaje")
    fig_puntaje.update_yaxes(title="Frecuencia")

    fig_dispersion = go.Figure()
    fig_dispersion.add_trace(go.Scatter(x=datos["Horas_Estudio_Semana"], y=datos["Puntaje_Examen"], mode="markers", name="Observado", marker=dict(color="#9ce7ff", size=8, line=dict(color="#ffffff", width=0.5))))
    if total >= 2:
        x_linea = np.linspace(datos["Horas_Estudio_Semana"].min(), datos["Horas_Estudio_Semana"].max(), 100)
        fig_dispersion.add_trace(go.Scatter(x=x_linea, y=modelo["intercepto"] + modelo["pendiente"] * x_linea, mode="lines", name="Tendencia", line=dict(color="#ff8f7a", width=3)))
    tema_figura(fig_dispersion, f"Puntaje frente a horas · ŷ = {modelo['pendiente']:.2f}x + {modelo['intercepto']:.2f}", 420)
    fig_dispersion.update_xaxes(title="Horas de estudio")
    fig_dispersion.update_yaxes(title="Puntaje")

    predicho = modelo["intercepto"] + modelo["pendiente"] * datos["Horas_Estudio_Semana"] if total else pd.Series(dtype=float)
    residuos = datos["Puntaje_Examen"] - predicho if total else pd.Series(dtype=float)
    fig_residuos = go.Figure(go.Scatter(x=predicho, y=residuos, mode="markers", marker=dict(color="#7ee0b8", size=8)))
    fig_residuos.add_hline(y=0, line_dash="dash", line_color="#ff8f7a")
    tema_figura(fig_residuos, "Diagnóstico: residuos frente a predicción", 340)
    fig_residuos.update_xaxes(title="Puntaje predicho")
    fig_residuos.update_yaxes(title="Residuo")

    return (
        f"{rango_horas[0]}–{rango_horas[1]} h",
        f"{rango_puntaje[0]}–{rango_puntaje[1]}",
        str(total),
        f"{horas_promedio:.1f} h",
        f"{puntaje_promedio:.1f}",
        f"{tasa:.1%}",
        f"{modelo['r']:.3f}",
        f"{modelo['r2']:.3f}",
        f"{modelo['mse']:.2f}",
        fig_horas,
        fig_puntaje,
        fig_dispersion,
        fig_residuos,
    )


@callback(
    Output("grafico-logistica", "figure"),
    Output("grafico-matriz", "figure"),
    Output("kpi-exactitud", "children"),
    Output("kpi-sensibilidad", "children"),
    Output("kpi-especificidad", "children"),
    Input("umbral-clasificacion", "value"),
)
def actualizar_clasificacion(umbral):
    c = float(mejor_experimento["C"])
    solver = mejor_experimento["Solver"]
    modelo = modelos_logisticos[(c, solver)]
    horas_grid = np.linspace(df["Horas_Estudio_Semana"].min(), df["Horas_Estudio_Semana"].max(), 250)
    prob_grid = modelo.predict_proba(pd.DataFrame({"Horas_Estudio_Semana": horas_grid}))[:, 1]
    prob = modelo.predict_proba(df[["Horas_Estudio_Semana"]])[:, 1]
    pred = (prob >= umbral).astype(int)
    vn, fp, fn, vp = confusion_matrix(df["Aprobado"], pred, labels=[0, 1]).ravel()
    exactitud = (vn + vp) / len(df)
    sensibilidad = vp / (vp + fn) if vp + fn else 0
    especificidad = vn / (vn + fp) if vn + fp else 0

    fig_logistica = go.Figure()
    fig_logistica.add_trace(go.Scatter(x=horas_grid, y=prob_grid, mode="lines", name="Probabilidad", line=dict(color="#9ce7ff", width=4)))
    fig_logistica.add_hline(y=umbral, line_dash="dash", line_color="#ffd166", annotation_text=f"Umbral {umbral:.2f}")
    tema_figura(fig_logistica, "Curva logística", 390)
    fig_logistica.update_xaxes(title="Horas de estudio")
    fig_logistica.update_yaxes(title="Probabilidad", tickformat=".0%", range=[0, 1])

    matriz = np.array([[vn, fp], [fn, vp]])
    fig_matriz = go.Figure(go.Heatmap(z=matriz, x=["Pred. no aprobado", "Pred. aprobado"], y=["Real no aprobado", "Real aprobado"], text=matriz, texttemplate="%{text}", colorscale=[[0, "#0c3f74"], [1, "#9ce7ff"]], showscale=False))
    tema_figura(fig_matriz, "Matriz de confusión", 390)

    return fig_logistica, fig_matriz, f"{exactitud:.1%}", f"{sensibilidad:.1%}", f"{especificidad:.1%}"


@callback(
    Output("resumen-experimento", "children"),
    Input("selector-c", "value"),
    Input("selector-solver", "value"),
)
def actualizar_experimento(c, solver):
    fila = experimentos[(experimentos["C"].eq(float(c))) & (experimentos["Solver"].eq(solver))].iloc[0]
    return [
        html.Div("VALIDACIÓN CRUZADA", className="technical-label"),
        html.Strong(f"{fila['Validacion']:.1%}"),
        html.P(f"Accuracy {fila['Exactitud']:.1%} · Sensibilidad {fila['Sensibilidad']:.1%} · Especificidad {fila['Especificidad']:.1%}"),
    ]


if __name__ == "__main__":
    os.environ["PORT"] = os.getenv("DASH_PORT", "8050")
    app.run(debug=False, host="0.0.0.0", port=8050)
