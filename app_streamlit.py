import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, mean_squared_error, confusion_matrix, precision_score
from io import BytesIO

# =============================
# IMPORTAR  FUNCIONES
# =============================
from convertir_tipos import convertir_tipos
from preprocesamiento import *
from analisis_univariado import analisis_univariado
from dummy_creation import dummy_creation
from calificacion import calcular_calificacion

# =============================
# CONFIGURACIÓN GENERAL
# =============================
st.set_page_config(page_title="Modelo exportación cacao", layout="wide")
st.title("Modelo exportación del cacao y sus productos derivados")

# =============================
# CARGAR MODELO ENTRENADO
# =============================
model = joblib.load("modelo.pkl")
columnas_modelo = joblib.load("columnas_modelo.pkl")

# =============================
# FUNCIÓN DE PREPROCESAMIENTO
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

    # =============================
    # CREAR VARIABLE OBJETIVO
    # =============================
    df['venta_fiable'] = df.apply(calcular_calificacion, axis=1)
    df['venta_fiable'] = df['venta_fiable'].fillna(0)

    # =============================
    # ESCALAR VARIABLES EXTRA
    # =============================
    from sklearn.preprocessing import MinMaxScaler
    scaler_extra = MinMaxScaler()

    columnas_extra = ['Peso_kilos_netos', 'Valor_FOB_USD']
    columnas_existentes = [c for c in columnas_extra if c in df.columns]

    if len(columnas_existentes) > 0:
        df[columnas_existentes] = scaler_extra.fit_transform(df[columnas_existentes])

    # =============================
    # SEPARAR X y y
    # =============================
    X = df.drop(['venta_fiable'], axis=1)
    y = df['venta_fiable'].round().astype(int)

    # =============================
    # DUMMIES
    # =============================
    X = dummy_creation(X, X.select_dtypes(include=['object']).columns)

    # =============================
    # ALINEAR CON MODELO
    # =============================
    X = X.reindex(columns=columnas_modelo, fill_value=0)

    return X, y, df


# =============================
# CARGA DE ARCHIVO
# =============================
st.header("Archivo Excel")
archivo = st.file_uploader("Cargar excel con las exportaciones", type=["xlsx"])

if archivo is not None:

    try:
        df = pd.read_excel(archivo)

        # =============================
        # PREPROCESAMIENTO
        # =============================
        X, y, df_procesado = preprocesar_datos(df)

        # =============================
        # PREDICCIÓN
        # =============================
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
        # MATRIZ DE CONFUSIÓN
        # =============================
        st.subheader("Matriz de Confusión")

        fig_cm, ax = plt.subplots(figsize=(2, 2))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            cbar=False,
            square=True,
            linewidths=0.5,
            ax=ax
        )
        ax.set_xlabel("Pred")
        ax.set_ylabel("Real")
        plt.tight_layout()
        st.pyplot(fig_cm, use_container_width=False)

        # =============================
        # GRÁFICAS
        # =============================
        st.header("Gráficas")

        if "Categoria" in df_procesado.columns:

            productos_disponibles = sorted(
                df_procesado["Categoria"].dropna().unique().tolist()
            )

            tipos_productos = ["Todos"] + productos_disponibles

            if len(productos_disponibles) == 0:
                st.warning("No hay categorías disponibles en el dataset.")
            else:

                producto = st.selectbox("Tipo producto", tipos_productos)

                if st.button("Generar gráfica"):

                    if producto != "Todos":
                        df_graf = df_procesado[df_procesado["Categoria"] == producto]
                    else:
                        df_graf = df_procesado

                    # =============================
                    # VALIDAR DATAFRAME VACÍO
                    # =============================
                    if df_graf.empty:
                        st.warning("No hay datos para este producto.")
                    else:

                        col1, col2 = st.columns(2)

                        # =============================
                        # GRÁFICA 1
                        # =============================
                        with col1:
                            st.subheader("Cantidad exp fiable y no fiables")

                            conteo = df_graf["Prediccion"].value_counts()

                            if conteo.empty:
                                st.warning("No hay predicciones disponibles.")
                            else:
                                fig1, ax1 = plt.subplots(figsize=(4, 3))
                                conteo.plot(kind="bar", ax=ax1)
                                ax1.set_xlabel("Clase (0 = No fiable, 1 = Fiable)")
                                ax1.set_ylabel("Cantidad")
                                st.pyplot(fig1)

                        # =============================
                        # GRÁFICA 2
                        # =============================
                        with col2:
                            st.subheader("Exportaciones fiables por continente")

                            fiables = df_graf[df_graf["Prediccion"] == 1]

                            if fiables.empty:
                                st.warning("No hay exportaciones clasificadas como fiables para este producto.")
                            elif "Continente_destino" not in fiables.columns:
                                st.warning("No existe la columna Continente_destino.")
                            else:
                                conteo_cont = fiables["Continente_destino"].value_counts()

                                if conteo_cont.empty:
                                    st.warning("No hay datos por continente para este producto.")
                                else:
                                    fig2, ax2 = plt.subplots(figsize=(4, 3))
                                    conteo_cont.plot(kind="bar", ax=ax2)
                                    ax2.set_xlabel("Continente")
                                    ax2.set_ylabel("Cantidad")
                                    st.pyplot(fig2)

        # =============================
        # TABLA FINAL
        # =============================
        st.header("Datos con Predicción")
        st.dataframe(df_procesado)

        # =============================
        # DESCARGAR EXCEL
        # =============================
        def convertir_a_excel(df):
            output = BytesIO()
            df.to_excel(output, index=False)
            return output.getvalue()

        excel_data = convertir_a_excel(df_procesado)

        st.download_button(
            label="Descargar Excel con Predicciones",
            data=excel_data,
            file_name="exportaciones_con_predicciones.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Ocurrió un error procesando el archivo: {e}")

