import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
def cargar_datos(ruta):
   
    df = pd.read_excel(ruta)
    return df