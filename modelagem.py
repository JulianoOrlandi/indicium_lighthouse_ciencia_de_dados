# Importação de bibliotecas
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

def main():
    
    # Leitura do conjunto de dados
    df_cars_train = pd.read_csv('cars_train.csv', sep='\t', encoding='utf_16_le')
    df_cars_test = pd.read_csv('cars_test.csv', sep='\t', encoding='utf_16_le')
    
    # Remoção das linhas duplicadas
    df_cars_train.drop_duplicates()
    df_cars_test.drop_duplicates()

    # Informações para separar o dataframe mais tarde
    size_train = len(df_cars_train)

    # Concatenando os dois dataframes
    df_cars_test.insert((df_cars_test.shape[1]), 'preco', np.NaN)
    df = pd.concat([df_cars_train, df_cars_test],ignore_index=True)

    # Preparando os conjuntos de dados para a modelagem
    df_preparado = preparar_para_modelagem(df)

    # Separando o dataframe em treino e teste
    df_train_ML = df_preparado[0:size_train]
    df_test_ML = df_preparado[size_train:len(df)]
    df_test_ML.reset_index(drop=True, inplace=True)

    # Separando as features do target no conjunto de treinamento e transformando em numpy array:
    X_train = df_train_ML.drop(['preco'], axis=1).values
    y_train = df_train_ML['preco'].values
        
    # Transformando as features do conjunto de teste em numpy array:
    X_test = df_test_ML.drop(['preco'], axis=1).values

    # Padronizando os conjuntos de dados
    X_train = padronizar(X_train)
    X_test = padronizar(X_test)

    # Implementando modelo XGBoost
    xgboost_modelo = XGBRegressor(max_depth=5, learning_rate=0.1, n_estimators=100, objective='reg:linear', booster='gbtree')
    xgboost_modelo_fit = xgboost_modelo.fit(X_train, y_train)

    # Fazendo predições para cars_test.csv    
    predicoes = xgboost_modelo_fit.predict(X_test)
    
    # Criando novo dataframe com 'id' do arquivo 'cars_test.csv' e adicionando as predições
    new_df = pd.DataFrame(df_cars_test['id'])
    new_df.insert((new_df.shape[1]), 'preco', predicoes)
    
    # Gerando arquivo .csv com as predições
    new_df.to_csv('predicted.csv', sep='\t', encoding='utf_16_le')
    
def padronizar(X):
    scaler = StandardScaler()
    scaler_fit = scaler.fit(X)
    X = scaler_fit.transform(X)
    
    return X

def preparar_para_modelagem(df):
    # Excluindo coluna 'id':
    df.drop(['id'], axis=1, inplace=True)
        
    # Preenchendo valores NaN em 'num_fotos'
    df['num_fotos'].fillna(value=round(df['num_fotos'].mean()), inplace=True)
        
    # Reduzindo o número de categorias na variável 'marca'
    marca_frequencia = df['marca'].value_counts() / len(df)
    marcas_menos_frequentes = marca_frequencia[marca_frequencia<0.01]
    df.loc[df['marca'].isin(marcas_menos_frequentes.index.tolist()), 'marca'] = 'OUTRA'
        
    # Excluindo coluna 'modelo':
    df.drop(['modelo'], axis=1, inplace=True)

    # Dividindo a coluna 'versao' em duas novas variáveis: 'cilindrada' e 'tipo_combustivel'
        # Criando as novas colunas
    df.insert(3, 'cilindrada', np.NaN)
    df.insert(4, 'tipo_combustivel', np.NaN)

        # Preenchendo as novas colunas a partir da coluna 'versao'
    tipos = ['flex', 'gasolina', 'diesel', 'híbrido', 'hybrid']
    for i in range(len(df)):
        if 'elétrico' in df.loc[i, 'versao'].lower() or 'electric' in df.loc[i, 'versao'].lower():
            df.loc[i, 'tipo_combustivel'] = 'eletrico'
            df.loc[i, 'cilindrada'] = 2.0
        else:
            df.loc[i, 'cilindrada'] = float(df['versao'][i][0:3])
            for tipo in tipos:
                if tipo in df.loc[i, 'versao'].lower():                
                    if tipo == 'híbrido' or tipo == 'hybrid':
                        df.loc[i, 'tipo_combustivel'] = 'hibrido'
                    else:
                        df.loc[i, 'tipo_combustivel'] = tipo
                        
        # Preenchendo o 'tipo_combustivel' com a moda para as entradas que não continham essa informação
    df['tipo_combustivel'].fillna(value=(df['tipo_combustivel'].mode()[0]), inplace=True)
        
        # Excluindo coluna 'versao':
    df.drop(['versao'], axis=1, inplace=True)
            
        # Reduzindo o número de categorias na variável 'cilindrada'
    for i in range(len(df['cilindrada'])):
        if 0.5<=df.loc[i, 'cilindrada']<=1.4:
            df.loc[i, 'cilindrada'] = '0.5 - 1.4'
        elif 1.5<=df.loc[i, 'cilindrada']<=2.4:
            df.loc[i, 'cilindrada'] = '1.5 - 2.4'
        elif 2.5<=df.loc[i, 'cilindrada']<=3.4:
            df.loc[i, 'cilindrada'] = '2.5 - 3.4'
        elif 3.5<=df.loc[i, 'cilindrada']<=4.4:
            df.loc[i, 'cilindrada'] = '3.5 - 4.4'
        elif 4.5<=df.loc[i, 'cilindrada']<=5.4:
            df.loc[i, 'cilindrada'] = '4.5 - 5.4'
        else:
            df.loc[i, 'cilindrada'] = '5.5 - 6.7'
        
    # Excluindo coluna 'ano_de_fabricacao':
    df.drop(['ano_de_fabricacao'], axis=1, inplace=True)
    
    # Substituindo valores em 'blindado':
    df['blindado'].replace('N', 'Não', inplace=True)
    df['blindado'].replace('S', 'Sim', inplace=True)

    # Excluindo a coluna ['cidade_vendedor']
    df.drop('cidade_vendedor', axis=1, inplace=True)

    # Substituindo valores em 'entrega_delivery':
    df['entrega_delivery'] = df['entrega_delivery'].map({True: 'Entrega', False: 'Não entrega'})

    # Substituindo valores em 'troca':
    df['troca'] = df['troca'].map({True: 'Trocado', False: 'Não foi trocado'})
    
    # Excluindo a coluna ['elegivel_revisao']
    df.drop('elegivel_revisao', axis=1, inplace=True)
    
    # Substituindo valores em 'dono_aceita_troca':
    df['dono_aceita_troca'].fillna(value='Não aceita', inplace=True)
    
    # Substituindo valores em 'veiculo_único_dono':
    df['veiculo_único_dono'].fillna(value='Não', inplace=True)
    
    # Substituindo valores em 'revisoes_concessionaria':
    df['revisoes_concessionaria'].fillna(value='Não', inplace=True)
    df['revisoes_concessionaria'].replace('Todas as revisões feitas pela concessionária', 'Sim', inplace=True)
    
    # Excluindo a coluna 'ipva_pago':
    df.drop('ipva_pago', axis=1, inplace=True)
    
    # Substituindo valores em 'veiculo_licenciado':
    df['veiculo_licenciado'].fillna(value='Não', inplace=True)
    
    # Substituindo valores em 'garantia_de_fábrica':
    df['garantia_de_fábrica'].fillna(value='Não', inplace=True)
    df['garantia_de_fábrica'].replace('Garantia de fábrica', 'Sim', inplace=True)
    
    # Substituindo valores em 'revisoes_dentro_agenda':
    df['revisoes_dentro_agenda'].fillna(value='Não', inplace=True)
    df['revisoes_dentro_agenda'].replace('Todas as revisões feitas pela agenda do carro', 'Sim', inplace=True)
    
    # Excluindo a coluna ['veiculo_alienado']
    df.drop('veiculo_alienado', axis=1, inplace=True)
    
    # Tranformando o tipo de variáveis categóricas numéricas para strings
    df = df.astype({'num_fotos': 'str', 'ano_modelo': 'str', 'num_portas': 'str'})
    
    # Convertendo as variáveis categóricas para o aprendizado de máquina
    df = pd.get_dummies(df)
    
    return df

if __name__ == "__main__":
    main()