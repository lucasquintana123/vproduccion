import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from sklearn.metrics import accuracy_score, mean_squared_error, confusion_matrix, precision_score
from io import BytesIO

# =============================
# IMPORTAR FUNCIONES
# =============================
from convertir_tipos import convertir_tipos
from preprocesamiento import *
from analisis_univariado import analisis_univariado
from dummy_creation import dummy_creation
from calificacion import calcular_calificacion
from analisis_ia import generar_analisis_ia


# =============================
# UI 
# =============================
st.markdown("""
<style>

.stApp {
    background-color: #0f0f0f;
}

h1, h2, h3, h4 {
    color: white !important;
}

/* KPI */
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

/* DOWNLOAD */
.stDownloadButton button {
    width: 100%;
    height: 55px;
    font-size: 18px;
    font-weight: bold;
    border-radius: 14px;
    background: linear-gradient(90deg, #6D4C41, #8D6E63);
    color: white;
}

.stDownloadButton button:hover {
    transform: scale(1.02);
}

</style>
""", unsafe_allow_html=True)

# =============================
# CONFIGURACIÓN GENERAL
# =============================
st.set_page_config(page_title="Modelo exportación cacao", layout="wide")
st.title("Modelo exportación del cacao y sus productos derivados")

# =============================
# SESSION STATE
# =============================
if "mostrar_graficas" not in st.session_state:
    st.session_state.mostrar_graficas = False

if "mostrar_analisis" not in st.session_state:
    st.session_state.mostrar_analisis = False

# =============================
# CARGAR MODELO
# =============================
model = joblib.load("modelo.pkl")
columnas_modelo = joblib.load("columnas_modelo.pkl")

# =============================
# FUNCIÓN PREPROCESAMIENTO
# =============================
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

    df['venta_fiable'] = df.apply(calcular_calificacion, axis=1)
    df['venta_fiable'] = df['venta_fiable'].fillna(0)

    from sklearn.preprocessing import MinMaxScaler
    scaler_extra = MinMaxScaler()

    columnas_extra = ['Peso_kilos_netos', 'Valor_FOB_USD']
    columnas_existentes = [c for c in columnas_extra if c in df.columns]

    if len(columnas_existentes) > 0:
        df[columnas_existentes] = scaler_extra.fit_transform(df[columnas_existentes])

    X = df.drop(['venta_fiable'], axis=1)
    y = df['venta_fiable'].round().astype(int)

    X = dummy_creation(X, X.select_dtypes(include=['object']).columns)
    X = X.reindex(columns=columnas_modelo, fill_value=0)

    return X, y, df

# =============================
# CARGA ARCHIVO
# =============================
st.header("Archivo Excel")
archivo = st.file_uploader("Cargar excel con las exportaciones", type=["xlsx"])

if archivo is not None:

    try:
        df = pd.read_excel(archivo)
        X, y, df_procesado = preprocesar_datos(df)

        y_pred = model.predict(X)
        df_procesado = df_procesado.copy()
        df_procesado["Prediccion"] = y_pred

        # =============================
        # MÉTRICAS
        # =============================
        accuracy = accuracy_score(y, y_pred)
        mse = mean_squared_error(y, y_pred)
        precision = precision_score(y, y_pred, zero_division=0)
        cm = confusion_matrix(y, y_pred)

        st.header("Resultados")

        col1, col2, col3 = st.columns(3)
        col1.metric("Exactitud", round(accuracy, 3))
        col2.metric("Precisión", round(precision, 3))
        col3.metric("MSE", round(mse, 3))

        # =============================
        # MATRIZ CONFUSIÓN
        # =============================
        st.subheader("Matriz de Confusión")

        cm_df = pd.DataFrame(
            cm,
            index=["Real 0", "Real 1"],
            columns=["Pred 0", "Pred 1"]
        )

        fig_cm = px.imshow(cm_df, text_auto=True,
                           color_continuous_scale="Blues",
                           aspect="equal")

        fig_cm.update_layout(title="Matriz de Confusión",title_x=0.5)
        st.plotly_chart(fig_cm, use_container_width=True)

        # =============================
        # VS REAL
        # =============================
        st.subheader("Valor real vs valor predicho")

        tn, fp, fn, tp = cm.ravel()

        df_vs = pd.DataFrame({
            "Clase Real": ["No Fiable (0)", "No Fiable (0)", "Fiable (1)", "Fiable (1)"],
            "Tipo Resultado": ["Correcto", "Incorrecto", "Incorrecto", "Correcto"],
            "Cantidad": [tn, fp, fn, tp]
        })

        fig_vs = px.bar(
            df_vs,
            x="Clase Real",
            y="Cantidad",
            color="Tipo Resultado",
            barmode="stack",
            text="Cantidad"
        )

        fig_vs.update_layout(title="Distribución por Clase Real", title_x=0.5)
        st.plotly_chart(fig_vs, use_container_width=True)

        # =============================
        # GRÁFICAS GENERALES
        # =============================
        st.header("Gráficas")

        productos_disponibles = sorted(
            df_procesado["Categoria"].dropna().unique().tolist()
        )

        tipos_productos = ["Todos"] + productos_disponibles
        producto = st.selectbox("Tipo producto", tipos_productos)

        if st.button("📊 Generar gráficas"):
            st.session_state.mostrar_graficas = True

        if st.session_state.mostrar_graficas:

            if producto != "Todos":
                df_graf = df_procesado[df_procesado["Categoria"] == producto]
            else:
                df_graf = df_procesado

            if not df_graf.empty:

                col1, col2 = st.columns(2)

                # =============================
                # BARRAS PREDICCIÓN
                # =============================
                with col1:
                    conteo = df_graf["Prediccion"].value_counts().reset_index()
                    conteo.columns = ["Clase", "Cantidad"]

                    fig1 = px.bar(conteo, x="Clase", y="Cantidad",
                                  color="Clase", text="Cantidad")
                    fig1.update_layout(title="Distribución de predicciones", title_x=0.5)
                    st.plotly_chart(fig1, use_container_width=True)

                # =============================
                # BARRAS CONTINENTE
                # =============================
                with col2:
                    fiables = df_graf[df_graf["Prediccion"] == 1]
                    if not fiables.empty:
                        conteo_cont = fiables["Continente_destino"].value_counts().reset_index()
                        conteo_cont.columns = ["Continente", "Cantidad"]

                        fig2 = px.bar(conteo_cont,
                                      x="Continente",
                                      y="Cantidad",
                                      text="Cantidad")
                        fig2.update_layout(title="Exportaciones fiables por continente", title_x=0.5)
                        st.plotly_chart(fig2, use_container_width=True)

                # =============================
                # PIE CHARTS
                # =============================
                st.subheader("Proporción de exportaciones por continente")

                col_pie1, col_pie2 = st.columns(2)

                with col_pie1:
                    fig_pie = px.pie(
                        conteo_cont,
                        names="Continente",
                        values="Cantidad",
                        title="Exportaciones fiables",
                        hole=0.4
                    )
                    fig_pie.update_traces(textposition="inside",
                                          textinfo="percent+label")
                    fig_pie.update_layout(title_x=0.5)
                    st.plotly_chart(fig_pie, use_container_width=True)

                with col_pie2:
                    no_fiables = df_graf[df_graf["Prediccion"] == 0]
                    if not no_fiables.empty:
                        conteo_no = no_fiables["Continente_destino"].value_counts().reset_index()
                        conteo_no.columns = ["Continente", "Cantidad"]

                        fig_pie_no = px.pie(
                            conteo_no,
                            names="Continente",
                            values="Cantidad",
                            title="Exportaciones no fiables",
                            hole=0.4
                        )
                        fig_pie_no.update_traces(textposition="inside",
                                                 textinfo="percent+label")
                        fig_pie_no.update_layout(title_x=0.5)
                        st.plotly_chart(fig_pie_no, use_container_width=True)

                # =============================
                # TENDENCIA
                # =============================
                st.subheader("Tendencia del Valor FOB (USD)")

                if "Año" in df_graf.columns:
                    df_tendencia = df_graf.groupby("Año")["Valor_FOB_USD"].sum().reset_index()

                    fig_tendencia = px.line(
                        df_tendencia,
                        x="Año",
                        y="Valor_FOB_USD",
                        markers=True,
                        title=f"Evolución anual del Valor FOB (USD) - {producto}"
                    )

                    fig_tendencia.update_layout(title_x=0.5)
                    st.plotly_chart(fig_tendencia, use_container_width=True)

        # =============================
        # ANÁLISIS ESPECÍFICO
        # =============================
        st.subheader("Análisis específico por producto y continente")

        fiables_total = df_procesado[df_procesado["Prediccion"] == 1]

        producto_filtro = st.selectbox(
            "Seleccione producto",
            sorted(fiables_total["Categoria"].dropna().unique())
        )

        continente_filtro = st.selectbox(
            "Seleccione continente",
            sorted(fiables_total["Continente_destino"].dropna().unique())
        )

        if st.button("Generar análisis específico"):
            st.session_state.mostrar_analisis = True

        if st.session_state.mostrar_analisis:

            df_filtrado = fiables_total[
                (fiables_total["Categoria"] == producto_filtro) &
                (fiables_total["Continente_destino"] == continente_filtro)
            ]

            if not df_filtrado.empty:
                df_paises = (
                    df_filtrado.groupby("Pais_destino")
                    .size()
                    .reset_index(name="Cantidad Exportaciones Fiables")
                    .sort_values(by="Cantidad Exportaciones Fiables", ascending=False)
                )

                fig3 = px.bar(
                    df_paises,
                    x="Pais_destino",
                    y="Cantidad Exportaciones Fiables",
                    text="Cantidad Exportaciones Fiables",
                    category_orders={
                    "Pais_destino": df_paises["Pais_destino"].tolist()
                    }
                )

                fig3.update_layout(
                title=f"Exportaciones fiables de {producto_filtro} en {continente_filtro}",
                title_x=0.5,
                xaxis_tickangle=-45
                )

                st.plotly_chart(fig3, use_container_width=True)

                #  RESUMEN GRÁFICA PAÍS 
                df_paises = (
                    df_filtrado
                    .groupby("Pais_destino")
                    .size()
                    .reset_index(name="Cantidad")
                    .sort_values(by="Cantidad", ascending=False)
                )

                pais_lider = df_paises.iloc[0]["Pais_destino"]
                cantidad_pais_lider = int(df_paises.iloc[0]["Cantidad"])


        # RESUMEN GRÁFICA CONTINENTE 
        conteo_cont = (
            df_procesado[df_procesado["Prediccion"] == 1]
            .groupby("Continente_destino")
            .size()
            .reset_index(name="Cantidad")
            .sort_values(by="Cantidad", ascending=False)
        )

        continente_lider = conteo_cont.iloc[0]["Continente_destino"]
        porcentaje_lider = round(
            (conteo_cont.iloc[0]["Cantidad"] / conteo_cont["Cantidad"].sum()) * 100,
            2
        )

       
        
        # =============================
        # ANÁLISIS INTELIGENTE
        # =============================
        st.header("Análisis Inteligente con IA")

        if st.button("🧠 Explicar resultados con IA"):


            

            with st.spinner("Generando análisis inteligente..."):

                try:
                    analisis = generar_analisis_ia(
                        accuracy,
                        precision,
                        mse,
                        cm,
                        df_procesado,
                        continente_lider,
                        porcentaje_lider,
                        pais_lider,
                        cantidad_pais_lider
                    )

                    st.success("Análisis generado correctamente")
                    st.markdown("### 📊 Informe generado por IA")
                    st.markdown(analisis)

                except Exception as e:
                    st.error(f"Error generando análisis: {e}")        

        # =============================
        # TABLA FINAL
        # =============================
        st.header("Datos con Predicción")
        st.dataframe(df_procesado)

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

