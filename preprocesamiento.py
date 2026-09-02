import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def asignar_trimestre(mes):
    if mes in [1,2,3]:
        return "Trimestre 1"
    elif mes in  [4,5,6]:
        return "Trimestre 2"
    elif mes in  [7,8,9]:
        return "Trimestre 3"
    else:
        return "Trimestre 4"

def categorizar_trimestre(df):
    df['trimestre'] = df['Mes'].apply(asignar_trimestre)
    return df

def asignar_cosecha(mes):
    if mes in [5,6,7,8]:
        return "cosecha principal"
    elif mes in  [11,12,1,2]:
        return "cosecha intermedia"
    else:
        return "No hay cosecha"

def categorizar_cosecha(df):
    df['Cosecha'] = df['Mes'].apply(asignar_cosecha)
    return df

def mapear_categoria(df):
    df['Categoria'] = df['Categoria'].str.strip()
    

    mapeo_cp ={
    'Cacao crudo en grano  entero para siembra':'Cacao crudo',
    'Cacao crudo en grano, entero para siembra.':'Cacao crudo',
    'Cacao en polvo':'Cacao en polvo',
    'Cacao en polvo con adicion de azucar u otro edulcorante':'Cacao en polvo',
    'Cacao en polvo sin adicion de azucar ni otro edulcorante':'Cacao en polvo',
    'Cacao en polvo sin adición de azúcar ni otro edulcorante.':'Cacao en polvo',
    'Cacao en polvo con adición de azúcar u otro edulcorante.':'Cacao en polvo',
    'Cacao tostado en grano  entero o partido':'Cacao tostado',
    'Cacao tostado en grano, entero o partido.':'Cacao tostado',
    'Cascara  peliculas y demas residuos de cacao':'Cascara de cacao',
    'Cáscara, películas y demás residuos de cacao.':'Cascara de cacao',
    'Las demas preparaciones alimenticias que contengan cacao  sin adicion de azucar  ni otros edulcorantes  en bloques o barras con peso superior a 2 kg  o en forma liquida  pastosa  en polvo  granulos o':'otras preparaciones',
    'Las demas preparciones alimenticias que contengan cacao  en bloques o barras con peso superior a 2 kg  o en forma liquida  pastosa  en polvo  granulos o en formas similares':'otras preparaciones',
    'Las demas preparciones alimenticias que contengan cacao  en bloques o barras con peso superior a 2 kg  o en forma liquida  pastosa  en polvo  granulos o en formas similares  en recipientes o envases i':'otras preparaciones',
    'Las demás preparciones alimenticias que contengan cacao, en bloques o barras con peso superior a 2 kg, o en forma líquida, pastosa, en polvo, gránulos o en formas similares, en recipientes o envases i':'otras preparaciones',
    'Las demás preparaciones alimenticias que contengan cacao, sin adición de azúcar, ni otros edulcorantes, en bloques o barras con peso superior a 2 kg, o en forma líquida, pastosa, en polvo, gránulos o':'otras preparaciones',
    'Los demas cacaos crudos en grano  entero o partido':'Cacao crudo',
    'Los demás cacaos crudos en grano, entero o partido.':'Cacao crudo',
    
    'Los demas chocolates y demas preparaciones alimenticas que contengan cacao  en bloques  tabletas o barras  sin rellenar':'Chocolates',
    'Los demas chocolates y demas preparaciones alimenticias que contengan cacao':'Chocolates',
    'Los demas chocolates y demas preparaciones alimenticias que contengan cacao  en bloques  tabletas o barras  rellenos':'Chocolates',
    'Los demas chocolates y demas preparaciones alimenticias que contengan cacao  en bloques  tabletas o barras  sin rellenar  sin adicion de azucar  ni otros edulcorantes':'Chocolates',
    'Los demas chocolates y demas preparaciones alimenticias que contengan cacao  sin adicion de azucar  ni otros edulcorantes':'Chocolates',
    'Los demás chocolates y demás preparaciones alimenticias que contengan cacao, en bloques, tabletas o barras, rellenos.':'Chocolates',
    'Los demás chocolates y demás preparaciones alimenticas que contengan cacao, en bloques, tabletas o barras, sin rellenar.':'Chocolates',
    'Los demás chocolates y demás preparaciones alimenticias que contengan cacao, sin adición de azúcar, ni otros edulcorantes.' :'Chocolates',
    'Los demás chocolates y demás preparaciones alimenticias que contengan cacao, en bloques, tabletas o barras, sin rellenar, sin adición de azúcar, ni otros edulcorantes.':'Chocolates',
    'Los demás chocolates y demás preparaciones alimenticias que contengan cacao.':'Chocolates',
    
    'Manteca de cacao  con un índice de acidez expresado en ácido oleico':'Manteca de cacao',
    'Manteca de cacao  con un Indice de acidez expresado en acido oleico inferior o igual a 1 porciento':'Manteca de cacao',
    'Manteca de cacao  con un indice de acidez expresado en acido oleico superior a 1 porciento pero inferior o igual a 165 porciento':'Manteca de cacao',
    'Manteca de cacao, con un índice de acidez expresado en ácido oleico superior a 1% pero inferior o igual a 1.65%.':'Manteca de cacao',
    'Manteca de cacao, con un índice de acidez expresado en ácido oleico inferior o igual a 1%.':'Manteca de cacao',
    'Grasa y aceite de cacao.':'Manteca de cacao',
    'Manteca de cacao, con un índice de acidez expresado en ácido oleico superior a 1.65%.':'Manteca de cacao',
    
    'NA':'otras preparaciones',
    'Pasta de cacao desgrasada total o parcialmente':'pasta de cacao',
    'Pasta de cacao sin desgrasar':'pasta de cacao',
    'Pasta de cacao sin desgrasar.':'pasta de cacao',
    'Pasta de cacao desgrasada total o parcialmente.':'pasta de cacao'
}

    df['Categoria'] = df['Categoria'].replace(mapeo_cp)
    print(df['Categoria'].value_counts())
    return df

def llenar_na_continente_destino(df):
    df['Continente Destino'].fillna('no determinado', inplace=True)
    return df

def escalar_variables(df):
    scaler = MinMaxScaler()
    variables_a_escalar = ['Cantidad(es)', 'Peso en kilos brutos', 'Número de artículos',
                           'Valor FOB (COP)', 'Valor Agregado Nacional (VAN)', 'Valor Flete',
                           'Valor seguro', 'Valor otros', 'Precio Unitario FOB (COP) Peso Neto',
                           'Precio Unitario FOB (COP) Peso Bruto', 'Precio Unitario FOB (USD) Peso Neto',
                           'Precio Unitario FOB (USD) Peso Bruto', 'Precio Unitario FOB (USD) Cantidad',
                           'Precio Unitario FOB (COP) Cantidad']
    df[variables_a_escalar] = scaler.fit_transform(df[variables_a_escalar])
    return df



def renombrar_columnas(df):
    # Renombrar columnas
    df = df.rename(columns={'Tipo de declaración': 'Tipo_de_declaracion',
        'Agente aduanero(s)': 'Agente_aduanero',
        'Razón social actual Exportador': 'Razon_social_exportador',
        'Razón social del importador': 'Razon_social_importador',
        'Código Partida': 'Codigo_partida',
        'Descripción de la partida arancelaria': 'Descripcion_partida_arancelaria',
        'Cantidad(es)': 'Cantidades',
        'Peso en kilos netos': 'Peso_kilos_netos',
        'Peso en kilos brutos': 'Peso_Kilos_brutos',
        'Número de artículos': 'Numero_articulos',
        'País de Destino': 'Pais_destino',
        'Departamento Origen': 'Departamento_origen',
        'Departamento De Procedencia': 'Departmanento_procedencia',
        'Lugar de salida': 'Lugar_salida',
        'Vía de transporte': 'Via_transporte',
        'Nacionalidad del medio de transporte': 'Nacionalidad_medio_transporte',
        'Regimen Exportacion': 'Regimen_exportacion',
        'Modalidad de exportación': 'Modalidad_exportacion',
        'Certificado de Origen': 'Certificado_origen',
        'Sistemas Especiales': 'Sistemas_especiales',
        'Forma de pago': 'Forma_pago',
        'Valor FOB (USD)': 'Valor_FOB_USD',
        'Valor FOB (COP)': 'Valor_FOB_COP',
        'Valor Agregado Nacional (VAN)': 'Valor_agregado_nacional',
        'Valor Flete': 'Valor_flete',
        'Valor seguro': 'Valor_seguro',
        'Valor otros': 'Valor_otros',
        'Precio Unitario FOB (COP) Peso Neto': 'Precio_unitario_FOB_COP_Peso_Neto',
        'Precio Unitario FOB (COP) Peso Bruto': 'Precio_unitario_FOB_COP_Peso_Bruto',
        'Precio Unitario FOB (USD) Peso Neto': 'Precio_unitario_FOB_USD_peso_Neto',
        'Precio Unitario FOB (USD) Peso Bruto': 'Precio_unitario_FOB_USD_Peso_Bruto',
        'Precio Unitario FOB (USD) Cantidad': 'Precio_Unitario_FOB_USD_Cantidad',
        'Precio Unitario FOB (COP) Cantidad': 'Precio_unitario_FOB_COP_Cantidad',
        'Continente Destino': 'Continente_destino'
                            
                           })
    return df



def filtrar_paises(df):
    temp_co = df['Pais_destino'].value_counts()
    pais_count = df['Pais_destino'].apply(lambda x: temp_co[x])
    for i in range(0, len(df)):
        if pais_count[i] < pais_count.quantile(0.05):
            df.loc[i, 'Pais_destino'] = 'OTROS PAISES'
    df = df[~df['Pais_destino'].isin(['COLOMBIA', 'ZONA FRANCA  DE  BOGOTA', 'OTROS PAISES'])]
    return df


