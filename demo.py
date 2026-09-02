import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

from sklearn.metrics import (
    accuracy_score,
    mean_squared_error,
    confusion_matrix,
    precision_score
)

from io import BytesIO

from convertir_tipos import convertir_tipos
from preprocesamiento import *
from analisis_univariado import analisis_univariado
from dummy_creation import dummy_creation
from calificacion import calcular_calificacion
from analisis_ia import generar_analisis_ia


# ============================================================
# FUNCIÓN PRINCIPAL DE LA DEMO
# ============================================================

def mostrar_demo():

    # ========================================================
    # CSS ESPECÍFICO
    # ========================================================

    st.markdown("""
    <style>

    h1, h2, h3, h4 {
        color: white !important;
    }

    .kpi-card {
        background: #1e1e1e;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #2c2c2c;
        text-align: center;
    }

    .kpi-title {
        font-size: 13px;
        color: #aaa;
    }

    .kpi-value {
        font-size: 26px;
        font-weight: bold;
        color: white;
    }

    .stDownloadButton button {
        width: 100%;
        min-height: 55px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 14px;
        background: linear-gradient(
            90deg,
            #6D4C41,
            #8D6E63
        );
        color: white;
    }

    </style>
    """, unsafe_allow_html=True)


    # ========================================================
    # HEADER
    # ========================================================

    st.title("🍫 Modelo exportación del cacao y sus productos derivados")

    st.success("DEMO AUTOMÁTICA DEL MODELO PREDICTIVO")

    st.markdown("""
    ### ¿Qué hace esta demo?

    Esta aplicación utiliza técnicas de inteligencia artificial y
    aprendizaje automático para analizar exportaciones de cacao
    y sus derivados, identificando qué operaciones tienen mayor
    probabilidad de ser consideradas exportaciones fiables.

    ### Funcionalidades incluidas en esta demo

    La demo ejecuta automáticamente:

    - Predicciones del modelo
    - Métricas de rendimiento
    - Visualizaciones analíticas
    - Análisis inteligente generado con IA
    - Filtros automáticos para Chocolate y América

    ### Versión completa del sistema

    En la versión completa, el usuario podrá:

    - Cargar archivos Excel
    - Seleccionar diferentes tipos de productos
    - Elegir continentes específicos
    - Descargar resultados procesados automáticamente

    Esta demo presenta únicamente una ejecución automática del
    sistema utilizando un conjunto de datos precargado.
    """)


    # ========================================================
    # INFORMACIÓN
    # ========================================================

    with st.expander("ℹ️ Información sobre la demo"):

        st.markdown("""
        ### Objetivo del sistema

        Este sistema utiliza Machine Learning para analizar
        exportaciones de cacao y estimar qué operaciones comerciales
        presentan mayores probabilidades de éxito y confiabilidad.

        ### Tecnologías utilizadas

        - Streamlit
        - Scikit-learn
        - Plotly
        - Inteligencia Artificial Generativa
        - Modelos predictivos supervisados

        ### Dataset

        La demo utiliza un conjunto de datos precargado automáticamente.
        """)


    # ========================================================
    # CARGAR MODELO
    # ========================================================

    model = joblib.load("modelo.pkl")
    columnas_modelo = joblib.load("columnas_modelo.pkl")


    # ========================================================
    # PREPROCESAMIENTO
    # ========================================================

    def preprocesar_datos(df):

        df = convertir_tipos(df)
        df = categorizar_trimestre(df)
        df = categorizar_cosecha(df)
        df = mapear_categoria(df)
        df = llenar_na_continente_destino(df)
        df = escalar_variables(df)
        df = renombrar_columnas(df)
        df = filtrar_paises(df)
        df = analisis_univariado(df)

        df["venta_fiable"] = df.apply(calcular_calificacion, axis=1)
        df["venta_fiable"] = df["venta_fiable"].fillna(0)

        from sklearn.preprocessing import MinMaxScaler

        scaler_extra = MinMaxScaler()
        columnas_extra = ["Peso_kilos_netos", "Valor_FOB_USD"]
        columnas_existentes = [c for c in columnas_extra if c in df.columns]

        if len(columnas_existentes) > 0:
            df[columnas_existentes] = scaler_extra.fit_transform(df[columnas_existentes])

        X = df.drop(["venta_fiable"], axis=1)
        y = df["venta_fiable"].round().astype(int)

        X = dummy_creation(
            X,
            X.select_dtypes(include=["object"]).columns
        )

        X = X.reindex(
            columns=columnas_modelo,
            fill_value=0
        )

        return X, y, df


    # ========================================================
    # DATASET
    # ========================================================

    try:

        df = pd.read_excel("demo.xlsx")
        X, y, df_procesado = preprocesar_datos(df)

        y_pred = model.predict(X)

        df_procesado = df_procesado.copy()
        df_procesado["Prediccion"] = y_pred


        # ====================================================
        # MÉTRICAS
        # ====================================================

        accuracy = accuracy_score(y, y_pred)
        mse = mean_squared_error(y, y_pred)
        precision = precision_score(y, y_pred, zero_division=0)
        cm = confusion_matrix(y, y_pred)


        # ====================================================
        # KPI
        # ====================================================

        st.markdown("## 📊 Métricas del modelo")

        col1, col2, col3 = st.columns(3)

        col1.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Exactitud</div>
            <div class="kpi-value">{round(accuracy, 3)}</div>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Precisión</div>
            <div class="kpi-value">{round(precision, 3)}</div>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">MSE</div>
            <div class="kpi-value">{round(mse, 3)}</div>
        </div>
        """, unsafe_allow_html=True)


        # ====================================================
        # MATRIZ DE CONFUSIÓN
        # ====================================================

        st.markdown("## 📊 Matriz de Confusión")

        st.markdown("""
        La matriz de confusión permite visualizar cuántas
        predicciones fueron correctas e incorrectas comparando
        los valores reales frente a los predichos por el modelo.
        """)

        cm_df = pd.DataFrame(
            cm,
            index=["Real 0", "Real 1"],
            columns=["Pred 0", "Pred 1"]
        )

        fig_cm = px.imshow(
            cm_df,
            text_auto=True,
            color_continuous_scale="Blues"
        )

        fig_cm.update_layout(
            title="Matriz de Confusión",
            title_x=0.5,
            autosize=True,
            margin=dict(l=40, r=40, t=70, b=40)
        )

        st.plotly_chart(fig_cm, use_container_width=True)


        # ====================================================
        # VISUALIZACIONES
        # ====================================================

        st.markdown("## 📊 Visualizaciones")

        st.markdown("""
        Las siguientes visualizaciones muestran patrones
        encontrados por el modelo sobre exportaciones de
        chocolate hacia diferentes continentes.
        """)

        producto = "CHOCOLATE"

        df_procesado["Categoria"] = (
            df_procesado["Categoria"]
            .astype(str)
            .str.upper()
            .str.strip()
        )

        df_graf = df_procesado[
            df_procesado["Categoria"].str.contains(producto, na=False)
        ]

        if df_graf.empty:
            st.warning("No existen datos para generar gráficas con el filtro aplicado.")
        else:
            col1, col2 = st.columns(2)

            # =================================================
            # GRÁFICA 1
            # =================================================

            with col1:
                st.markdown("#### Distribución de predicciones")

                conteo = (
                    df_graf["Prediccion"]
                    .value_counts()
                    .reset_index()
                )
                conteo.columns = ["Clase", "Cantidad"]
                conteo = conteo.sort_values("Clase")

                fig1 = px.bar(
                    conteo,
                    x="Clase",
                    y="Cantidad",
                    text="Cantidad"
                )

                fig1.update_layout(
                    xaxis_title="Clase",
                    yaxis_title="Cantidad",
                    autosize=True,
                    margin=dict(l=40, r=40, t=50, b=40)
                )

                st.plotly_chart(fig1, use_container_width=True)

            # =================================================
            # GRÁFICA 2
            # =================================================

            with col2:
                fiables = df_graf[df_graf["Prediccion"] == 1]

                if fiables.empty:
                    st.warning("No hay exportaciones fiables para este filtro.")
                else:
                    st.markdown("#### Exportaciones fiables por continente")

                    conteo_cont = (
                        fiables["Continente_destino"]
                        .value_counts()
                        .reset_index()
                    )
                    conteo_cont.columns = ["Continente", "Cantidad"]

                    fig2 = px.bar(
                        conteo_cont,
                        x="Continente",
                        y="Cantidad",
                        text="Cantidad"
                    )

                    fig2.update_layout(
                        xaxis_title="Continente",
                        yaxis_title="Cantidad",
                        autosize=True,
                        margin=dict(l=40, r=40, t=50, b=40)
                    )

                    st.plotly_chart(fig2, use_container_width=True)


        # ====================================================
        # IA
        # ====================================================

        st.markdown("## 🧠 Análisis Inteligente con IA")

        st.markdown("""
        La inteligencia artificial genera automáticamente
        una interpretación de los resultados obtenidos por
        el modelo, facilitando la toma de decisiones.
        """)

        with st.spinner("Generando análisis inteligente..."):
            try:
                analisis = generar_analisis_ia(
                    accuracy,
                    precision,
                    mse,
                    cm,
                    df_procesado,
                    "GLOBAL",
                    0,
                    "N/A",
                    0
                )
                st.markdown(analisis)
            except Exception as e:
                st.error(f"Error generando análisis: {e}")


        # ====================================================
        # DATASET
        # ====================================================

        st.markdown("## 📋 Datos con Predicción")

        st.markdown("""
        La tabla final contiene los datos procesados junto
        con la predicción generada automáticamente por el
        modelo.
        """)

        st.dataframe(df_procesado.head(20), use_container_width=True)


        # ====================================================
        # DESCARGA
        # ====================================================

        st.markdown("## 📥 Descarga de resultados")

        output = BytesIO()
        df_procesado.to_excel(output, index=False)

        st.download_button(
            "⬇️ Descargar Excel con Predicciones",
            data=output.getvalue(),
            file_name="exportaciones_con_predicciones.xlsx",
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Ocurrió un error procesando el archivo: {e}")
