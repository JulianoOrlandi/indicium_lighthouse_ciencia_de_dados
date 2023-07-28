# Desafio Lighthouse Ciência de Dados
#### **Autor:** Juliano Orlandi
#### **Descrição:**
O objetivo deste desafio é analisar dois conjuntos de dados disponíveis nos arquivos *cars_train.csv* e *cars_test.csv* para responder às perguntas de negócios feitas pelo cliente e criar um modelo preditivo que precifique os carros de forma que eles fiquem o mais próximos dos valores de mercado.

#### **Tecnologias:**
- Python 3.11.4
- Pandas 2.0.3
- Numpy 1.25.0
- Scikit-learn 1.3.0
- Xgboost 1.7.6

#### **Instalação:**
Para rodar este programa, é preciso instalar as tecnologias acima listadas. Além disso, é preciso possuir os arquivos com os conjuntos de dados supramencionados.

#### **Execução:**
Uma vez que todos os pacotes estejam instalados e os arquivos se encontrem no mesmo diretório do arquivo *modelagem.py*, o programa pode ser executado. Ao final, ele gerará um arquivo chamado *predicted.csv* com os resultados das previsões de preço para os veículos do arquivo *cars_test.csv*.

#### **Documentação:**
A função *main()* se divide em seis etapas. A primeira delas é a leitura e concatenação das duas bases de dados. Os arquivos *.csv* são lidos, as linhas duplicadas são removidas de ambos e, por fim, eles são concatenados. A segunda etapa é a preparação do conjunto unificado de dados. Ela é feita pela função *preparar_para_modelagem()*, que recebe um DataFrame como argumento e realiza uma série de procedimentos. Basicamente, eles removem colunas que não são relevantes ou podem atrapalhar o algoritmo de aprendizado de máquina, preenchem informações faltantes, criam e preenchem novas colunas a partir de informações que estão reunidas no conjunto original, resumem variáveis categóricas que possuem muitos níveis. A função *preparar_para_modelagem()* retorna o conjunto de dados limpo e organizado para o aprendizado de máquina. A terceira etapa consiste na reseparação do conjunto de dados em DataFrames análogos aos que foram criados a partir dos arquivos *.csv* originais. A quarta etapa padroniza o conjunto de dados para a implementação do modelo. A quinta etapa consiste na criação e preenchimento do modelo e é seguida pelo seu uso para a previsão de valores. Por fim, a última etapa cria um novo DataFrame com as 'id's e os preços previstos para os veículos do arquivo *cars_test.csv*. Deste DataFrame se gera um novo arquivo *.csv* intitulado *predicted.csv*.