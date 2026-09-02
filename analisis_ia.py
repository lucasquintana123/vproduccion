import os
import time
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import streamlit as st

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

# Si no existe en local, usar Streamlit Secrets
if HF_TOKEN is None and "HF_TOKEN" in st.secrets:
    HF_TOKEN = st.secrets["HF_TOKEN"]

# Cliente
client = InferenceClient(
    api_key=HF_TOKEN,
)

# Lista de modelos en orden de preferencia (Serverless de alta disponibilidad)
MODELOS_DISPONIBLES = [
    "mistralai/Mistral-7B-Instruct-v0.3",
    "meta-llama/Llama-3.1-8B-Instruct",
    "Qwen/Qwen2.5-72B-Instruct"
]


def generar_analisis_ia(
    accuracy,
    precision,
    mse,
    cm,
    df_procesado,
    continente_lider,
    porcentaje_lider,
    pais_lider,
    cantidad_pais_lider,
    max_retries=3,
    delay_seconds=4
):
    total_registros = len(df_procesado)
    total_fiables = int((df_procesado["Prediccion"] == 1).sum())
    total_no_fiables = int((df_procesado["Prediccion"] == 0).sum())

    prompt = f"""
    Analiza los resultados de un modelo de clasificación de exportaciones de cacao y productos derivados desde Colombia.

    Métricas:
    - Exactitud: {round(accuracy, 3)}
    - Precisión: {round(precision, 3)}

    Matriz de Confusión:
    - Verdaderos Negativos: {cm[0][0]}
    - Falsos Positivos: {cm[0][1]}
    - Falsos Negativos: {cm[1][0]}
    - Verdaderos Positivos: {cm[1][1]}

    Total registros: {total_registros}
    Exportaciones fiables: {total_fiables}
    Exportaciones no fiables: {total_no_fiables}

    Continente líder: {continente_lider}
    Participación: {porcentaje_lider}%

    País líder: {pais_lider}
    Cantidad: {cantidad_pais_lider}

    Explica:
    1) Resultados de las métricas
    2) Qué muestran las gráficas
    3) Qué implica que ese continente y país lideren
    4) Recomendaciones estratégicas

    Responde en español, es importante que responda en español.
    """

    # Intentar con la lista de modelos y aplicar reintentos
    for model_name in MODELOS_DISPONIBLES:
        for intento in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": "Eres un analista experto en modelos predictivos y comercio internacional."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=2500,
                    temperature=0.7,
                )
                # Si la llamada es exitosa, retorna la respuesta de inmediato
                return response.choices[0].message.content

            except Exception as e:
                error_msg = str(e)
                # Si el modelo está ocupado o en error de servidor, esperar y reintentar
                if "busy" in error_msg.lower() or "503" in error_msg or "completion_error" in error_msg:
                    st.warning(f"El modelo `{model_name}` está ocupado. Reintentando ({intento + 1}/{max_retries})...")
                    time.sleep(delay_seconds * (intento + 1))  # Espera progresiva (4s, 8s, 12s)
                else:
                    # Otro tipo de error (ej. token inválido), rompe el bucle interno para probar el siguiente modelo
                    break

    # Si ningún modelo respondió tras los reintentos
    st.error("No se pudo generar el análisis en este momento porque los servidores de Hugging Face están saturados. Por favor, intenta de nuevo en un minuto.")
    return None