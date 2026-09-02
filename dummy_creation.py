import pandas as pd

def dummy_creation(df, cols):
    # Verificar qué columnas están presentes en el DataFrame
    present_cols = [col for col in cols if col in df.columns]
    
    if not present_cols:
        print("Ninguna de las columnas especificadas está presente en el DataFrame.")
        return df
    
    # Obtener variables dummy solo para las columnas presentes
    df_dummies = pd.get_dummies(df[present_cols], prefix_sep=':')
    df_dummies = df_dummies.astype(int) # convertir a valores enteros
    
    # Eliminar las columnas originales del DataFrame
    df = df.drop(columns=present_cols)
    
    # Concatenar las nuevas columnas dummy con el DataFrame original
    df = pd.concat([df, df_dummies], axis=1)
    
    return df