import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
def convertir_tipos(df):

    df['Peso en kilos netos'] = df['Peso en kilos netos'].astype(float)
    df['Peso en kilos brutos'] = df['Peso en kilos brutos'].astype(float)
    df['Número de artículos'] = df['Número de artículos'].astype(float)
    df['Valor FOB (USD)'] = df['Valor FOB (USD)'].astype(float)
    df['Valor FOB (COP)'] = df['Peso en kilos netos'].astype(float)  # Corregido: había un error aquí
    df['Valor Agregado Nacional (VAN)'] = df['Valor Agregado Nacional (VAN)'].astype(float)
    df['Valor Flete'] = df['Valor Flete'].astype(float)
    df['Valor seguro'] = df['Valor seguro'].astype(float)
    df['Precio Unitario FOB (COP) Peso Neto'] = df['Precio Unitario FOB (COP) Peso Neto'].astype(float)
    df['Precio Unitario FOB (COP) Peso Bruto'] = df['Precio Unitario FOB (COP) Peso Bruto'].astype(float)
    df['Precio Unitario FOB (USD) Peso Neto'] = df['Precio Unitario FOB (USD) Peso Neto'].astype(float)
    df['Precio Unitario FOB (USD) Peso Bruto'] = df['Precio Unitario FOB (USD) Peso Bruto'].astype(float)
    df['Precio Unitario FOB (USD) Cantidad'] = df['Precio Unitario FOB (USD) Cantidad'].astype(float)
    df['Precio Unitario FOB (COP) Cantidad'] = df['Precio Unitario FOB (COP) Cantidad'].astype(float)
    df['Cantidad(es)'] = df['Cantidad(es)'].astype(float)
    
    return df