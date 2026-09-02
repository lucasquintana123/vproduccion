from sklearn.model_selection import train_test_split
from scipy.stats import chi2_contingency
from scipy.stats import f_oneway
from sklearn.feature_selection import f_classif
import pandas as pd
import numpy as np

def feature_selection(X,y):
   # df1['venta_fiable'] = df1['venta_fiable'].fillna(0)
    

    # Dividir X y usando Train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=1727, stratify=y)
    X_train_num = X_train.select_dtypes(include='number').copy()

    # Obtener forma del train y datos de prueba
    print("train data size:", X_train.shape)
    print("test data size:", X_test.shape)
    print("test data size:", y_test.shape)
    X_train_cat = X_train.select_dtypes(include=['object', 'category']).copy()

    # Definir un diccionario vacío para almacenar los resultados de la prueba chi-cuadrado
    chi2_check = {}

    # Recorrer cada columna en el conjunto de entrenamiento para calcular la estadística chi con la variable objetivo
    for column in X_train_cat:
        chi, p, dof, ex = chi2_contingency(pd.crosstab(y_train, X_train_cat[column]))
        chi2_check.setdefault('Feature', []).append(column)
        chi2_check.setdefault('p-value', []).append(round(p, 10))

    # Convertir diccionario a DataFrame
    chi2_result = pd.DataFrame(data=chi2_check)

    data_merge = chi2_result.merge(X_train_cat.describe().T.reset_index(),
                                    left_on='Feature',
                                    right_on='index').sort_values(by=['p-value', 'unique'])

    p_data = data_merge[(data_merge['p-value'] < 0.05)].sort_values(by='p-value')
    p_data
    data_merge[(data_merge['p-value'] > 0.05)].sort_values(by='p-value')
    X_train[list(p_data['Feature'])].sample(5)

    # ANOVA
    f_statistics, p_values = f_classif(X_train_num.fillna(X_train_num.median()), y_train)
    anova_f_table = pd.DataFrame(data={'Feature': X_train_num.columns.values,
                                       'F-Score': f_statistics,
                                       'p-value': p_values.round(decimals=10)})
    anova_merge = anova_f_table.merge(X_train_num.describe().T.reset_index(),
                                      left_on='Feature',
                                      right_on='index').sort_values(['F-Score', 'count'], ascending=False).head(
        50)

    p_anova = anova_merge[(anova_merge['p-value'] < 0.05)].sort_values(by='p-value')
    p_anova

    list(p_anova['Feature'])
    X_train[list(p_anova['Feature'])].sample(5)

    # Correlación
    corr_matrix = X_train[list(p_anova['Feature'])].corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    c = X_train[list(p_anova['Feature'])].corr().abs()
    s = c.unstack()
    so = s.sort_values(kind="quicksort", ascending=False)
    so = pd.DataFrame(so, columns=['Pearson Correlation'])

    so[so['Pearson Correlation'] < 1].head()

    so_cond = so[(so['Pearson Correlation'] < 1) | (so['Pearson Correlation'] == 1)]
    so[so['Pearson Correlation'] < 1].describe().T
    to_drop = [column for column in upper.columns if any(upper[column] > 0.8)]
    to_drop
    num_consider = [x for x in list(p_anova['Feature']) if x not in to_drop]
    num_consider
    selected_cols = num_consider + list(p_data['Feature'])
    selected_cols
    X_train = X_train[selected_cols]
    X_test = X_test[selected_cols]
    columnas_a_eliminar = ['Agente_aduanero', 'Razon_social_exportador', 'Razon_social_importador',
                           'Nacionalidad_medio_transporte']
    X_train = X_train.drop(columns=columnas_a_eliminar)
    X_train
    X_test = X_test.drop(columns=columnas_a_eliminar)
    return X_train, X_test, y_train, y_test,p_data