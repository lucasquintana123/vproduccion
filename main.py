import streamlit as st

from demo import mostrar_demo
from app_streamlit2 import mostrar_completa


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Modelo exportación del cacao",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION STATE
# ============================================================

if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"

if "mostrar_graficas" not in st.session_state:
    st.session_state.mostrar_graficas = False

if "mostrar_analisis" not in st.session_state:
    st.session_state.mostrar_analisis = False


# ============================================================
# CSS GENERAL
# ============================================================

st.markdown("""
<style>

/* ============================================================
   FONDO GENERAL
   ============================================================ */

.stApp {
    background-color: #0f0f0f;
}


/* ============================================================
   CONTENEDOR PRINCIPAL
   ============================================================ */

[data-testid="stAppViewContainer"] > .main {
    width: 100%;
}

[data-testid="stMainBlockContainer"] {
    max-width: 100% !important;
    width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}


/* ============================================================
   OCULTAR ELEMENTOS DE STREAMLIT
   ============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* ============================================================
   TÍTULO PRINCIPAL
   ============================================================ */

.titulo-principal {
    text-align: center;
    padding-top: 20px;
    padding-bottom: 10px;
}

.titulo-principal h1 {
    color: white;
    font-size: 50px;
    font-weight: 800;
    margin-bottom: 10px;
}

.titulo-principal p {
    color: #d6d6d6;
    font-size: 20px;
}


/* ============================================================
   CARDS
   ============================================================ */

.card {
    background-color: #1e1e1e;
    padding: 35px;
    border-radius: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.35);
    border: 1px solid #2c2c2c;
    text-align: center;

    min-height: 320px;
    height: auto;

    display: flex;
    flex-direction: column;
    justify-content: space-between;

    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    border: 1px solid #6D4C41;
}


/* ============================================================
   SUBTÍTULOS DE LAS CARDS
   ============================================================ */

.card h2 {
    color: white;
    font-size: 30px;
    margin-bottom: 20px;
}


/* ============================================================
   TEXTO DE LAS CARDS
   ============================================================ */

.card p {
    color: #d0d0d0;
    font-size: 17px;
    line-height: 1.6;
}


/* ============================================================
   BOTONES
   ============================================================ */

.stButton > button {
    width: 100%;
    border-radius: 14px;
    min-height: 55px;
    font-size: 18px;
    font-weight: bold;
    border: none;

    background: linear-gradient(
        90deg,
        #6D4C41,
        #8D6E63
    );

    color: white;

    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.02);

    background: linear-gradient(
        90deg,
        #5D4037,
        #795548
    );
}


/* ============================================================
   LÍNEA DECORATIVA
   ============================================================ */

.linea {
    height: 4px;

    background: linear-gradient(
        to right,
        #6D4C41,
        #A1887F
    );

    border-radius: 10px;

    margin-top: 10px;
    margin-bottom: 40px;
}


/* ============================================================
   TEXTO GENERAL
   ============================================================ */

html,
body {
    color: white;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;
    color: #aaaaaa;
    font-size: 14px;
    padding-top: 30px;
}


/* ============================================================
   PLOTLY
   ============================================================ */

[data-testid="stPlotlyChart"] {
    width: 100% !important;
    max-width: 100% !important;
}


/* ============================================================
   DATAFRAMES
   ============================================================ */

[data-testid="stDataFrame"] {
    width: 100% !important;
    max-width: 100% !important;
}


/* ============================================================
   EVITAR DESBORDAMIENTO HORIZONTAL
   ============================================================ */

[data-testid="stAppViewContainer"] {
    overflow-x: hidden;
}


/* ============================================================
   RESPONSIVIDAD
   ============================================================ */

@media (max-width: 900px) {

    .titulo-principal h1 {
        font-size: 36px;
    }

    .titulo-principal p {
        font-size: 17px;
    }

    .card {
        padding: 25px;
        min-height: 280px;
    }

    .card h2 {
        font-size: 25px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCIÓN PARA VOLVER AL INICIO
# ============================================================

def volver_inicio():

    st.session_state.pagina = "inicio"

    st.session_state.mostrar_graficas = False
    st.session_state.mostrar_analisis = False

    st.rerun()


# ============================================================
# PANTALLA DE INICIO
# ============================================================

if st.session_state.pagina == "inicio":

    # --------------------------------------------------------
    # TÍTULO
    # --------------------------------------------------------

    st.markdown("""
    <div class="titulo-principal">

        <h1>
            🍫 Modelo Inteligente de Exportación del Cacao
        </h1>

        <p>
            Sistema basado en Machine Learning e Inteligencia Artificial
            para el análisis predictivo de exportaciones de cacao.
        </p>

    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # LÍNEA DECORATIVA
    # --------------------------------------------------------

    st.markdown(
        '<div class="linea"></div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # TEXTO INTRODUCTORIO
    # --------------------------------------------------------

    st.markdown("""
    <div style="
        text-align:center;
        font-size:20px;
        color:#d0d0d0;
        padding-bottom:30px;
    ">
        Seleccione la versión del sistema que desea utilizar.
    </div>
    """, unsafe_allow_html=True)


    # ========================================================
    # COLUMNAS
    # ========================================================

    col1, col2 = st.columns(
        2,
        gap="large"
    )


    # ========================================================
    # DEMO
    # ========================================================

    with col1:

        st.markdown("""
        <div class="card">

            <h2>Demo</h2>

            <p>
                Ejecuta el modelo con datos precargados.
            </p>

            <p>
                Incluye:
            </p>

            <p>
                ✔ Predicciones automáticas<br>
                ✔ Métricas del modelo<br>
                ✔ Visualizaciones<br>
                ✔ Análisis con IA
            </p>

        </div>
        """, unsafe_allow_html=True)


        st.write("")


        if st.button(
            "Ingresar a la Demo",
            key="demo",
            use_container_width=True
        ):

            st.session_state.pagina = "demo"
            st.rerun()


    # ========================================================
    # VERSIÓN COMPLETA
    # ========================================================

    with col2:

        st.markdown("""
        <div class="card">

            <h2>Versión Completa</h2>

            <p>
                Plataforma interactiva personalizada.
            </p>

            <p>
                Incluye:
            </p>

            <p>
                ✔ Carga de Excel<br>
                ✔ Filtros avanzados<br>
                ✔ Visualizaciones dinámicas<br>
                ✔ Descarga de resultados
            </p>

        </div>
        """, unsafe_allow_html=True)


        st.write("")


        if st.button(
            "Ingresar a la Versión Completa",
            key="completa",
            use_container_width=True
        ):

            st.session_state.pagina = "completa"
            st.rerun()


    # ========================================================
    # ESPACIO
    # ========================================================

    st.markdown(
        "<br><br>",
        unsafe_allow_html=True
    )


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown("""
    <div class="footer">
        Proyecto aplicado
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# PÁGINA DEMO
# ============================================================

elif st.session_state.pagina == "demo":

    # --------------------------------------------------------
    # BOTÓN VOLVER
    # --------------------------------------------------------

    col1, _ = st.columns([1, 8])

    with col1:

        if st.button(
            "⬅️ Volver",
            key="volver_demo"
        ):

            volver_inicio()


    # --------------------------------------------------------
    # EJECUTAR DEMO
    # --------------------------------------------------------

    mostrar_demo()


# ============================================================
# PÁGINA VERSIÓN COMPLETA
# ============================================================

elif st.session_state.pagina == "completa":

    # --------------------------------------------------------
    # BOTÓN VOLVER
    # --------------------------------------------------------

    col1, _ = st.columns([1, 8])

    with col1:

        if st.button(
            "⬅️ Volver",
            key="volver_completa"
        ):

            volver_inicio()


    # --------------------------------------------------------
    # EJECUTAR APLICACIÓN COMPLETA
    # --------------------------------------------------------

    mostrar_completa()
