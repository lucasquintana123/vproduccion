import pandas as pd

def analisis_univariado(df1):
    # Aplicamos la función a cada fila del DataFrame
    categorical_feat = list(df1.select_dtypes(include=['category','object']).columns)
    df1[categorical_feat] = df1[categorical_feat].astype(str)
    df1[categorical_feat].nunique().reset_index().sort_values(by=0, ascending=False)
    temp_razonimp = df1['Razon_social_importador'].value_counts()
    temp_razonexp = df1['Razon_social_exportador'].value_counts()
    temp_agentead = df1['Agente_aduanero'].value_counts()
    temp_nacmedtramp = df1['Nacionalidad_medio_transporte'].value_counts()
    temp_desparara = df1['Descripcion_partida_arancelaria'].value_counts()
    temp_depor=df1['Departamento_origen'].value_counts()
    temp_deppro=df1['Departmanento_procedencia'].value_counts()
    temp_aduana=df1['Aduana'].value_counts()
    temp_lugsal=df1['Lugar_salida'].value_counts()
    temp_modexp=df1['Modalidad_exportacion'].value_counts()
    razonimp_count = df1['Razon_social_importador'].apply(lambda x: temp_razonimp[x])
    razonexp_count = df1['Razon_social_exportador'].apply(lambda x: temp_razonexp[x])
    agentead_count = df1['Agente_aduanero'].apply(lambda x: temp_agentead[x])
    nacmedtramp_count = df1['Nacionalidad_medio_transporte'].apply(lambda x: temp_nacmedtramp[x])
    desparara_count =df1['Descripcion_partida_arancelaria'].apply(lambda x: temp_desparara[x])
    depor_count = df1['Departamento_origen'].apply(lambda x: temp_depor[x])
    deppro_count = df1['Departmanento_procedencia'].apply(lambda x: temp_deppro[x])
    aduana_count = df1['Aduana'].apply(lambda x: temp_aduana[x])
    lugsal_count = df1['Lugar_salida'].apply(lambda x: temp_lugsal[x])
    modexp_count = df1['Modalidad_exportacion'].apply(lambda x: temp_modexp[x])
    quantile_20 = razonimp_count.quantile(0.2)
    df1.loc[razonimp_count < quantile_20, 'Razon_social_importador'] = 'OTRO IMPORTADOR'
    quantile_20 = razonexp_count.quantile(0.3)
    df1.loc[razonexp_count < quantile_20, 'Razon_social_exportador'] = 'OTRO EXPORTADOR'
    quantile_20 = agentead_count.quantile(0.2)
    df1.loc[agentead_count < quantile_20, 'Agente_aduanero'] = 'OTRO AGENTE'
    quantile_10 = nacmedtramp_count.quantile(0.1)
    df1.loc[nacmedtramp_count < quantile_10, 'Nacionalidad_medio_transporte'] = 'OTRO NACIONALIDAD'
    quantile_20 = desparara_count.quantile(0.2)
    df1.loc[desparara_count < quantile_20, 'Descripcion_partida_arancelaria'] = 'OTRA DESCRIPCION'
    quantile_10 = depor_count.quantile(0.1)
    df1.loc[depor_count < quantile_10, 'Departamento_origen'] = 'OTRO DEPARTAMENTO'
    quantile_10 = deppro_count.quantile(0.1)
    df1.loc[deppro_count < quantile_10, 'Departmanento_procedencia'] = 'OTRO DEPARTAMENTO'
    quantile_10 = aduana_count.quantile(0.1)
    df1.loc[aduana_count < quantile_10, 'Aduana'] = 'OTRA ADUANA'
    quantile_10 = lugsal_count.quantile(0.1)
    df1.loc[lugsal_count < quantile_10, 'Lugar_salida'] = 'OTRO LUGAR'
    quantile_20 = modexp_count.quantile(0.2)
    df1.loc[modexp_count < quantile_20, 'Modalidad_exportacion'] = 'OTRA MODALIDAD'
    print(df1)
   
    return df1