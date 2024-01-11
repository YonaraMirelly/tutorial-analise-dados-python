# Primeiro você deve criar um arquivo .ipynb, pois ele é usado para trabalhar com análises
# tive que usar o .py por conta de problemas técnicos no github, mas use o .ipynb

# Depois instalar as bibliotecas:
# pip install pandas
# pip install plotly
# pip install nbformat -> esse é opcional (em caso de erro)

# ALGORITMO
# 1 - importar a base de dados
# 2 - visualizar a base de dados
# 3 - corrigir os problemas da base de dados
# 4 - análise inicial
# 5 - análise das causas...(como que as colunas da base impactam em algo)

# Importar a base de dados
import pandas as pd
# lê a base de dados
tabela = pd.read_csv("cancelamentos_sample.csv")
# removendo a coluna inútil : CustomerID
tabela = tabela.drop("CustomerID", axis=1)
# printa a tabela de forma organizada -> display(tabela) : só funciona no arquivo .ipynb
print(tabela)

# identificando valores vazios
print(tabela.info())

# removendo valores vazios
tabela = tabela.dropna()
print(tabela.info())

# saber quantas pessoas cancelaram
print(tabela["cancelou"].value_counts())
# Em forma de porcentagem
print(tabela["cancelou"].value_counts(normalize=True).map("{:.1%}".format))

# analise as colunas que devem impactar mais no cancelamento... intuitivamente
# 1 - dias_atraso
# 2 - duracao_contrato
# 3 - ligacoes_callcenter
# para analisar, você precisa criar gráficos/dashboards
import plotly.express as px
# para cada coluna nas colunas da tabela, o for vai criar um gráfico no formato de histograma
for coluna in tabela.columns:
    grafico = px.histogram(tabela, x=coluna, color = "cancelou")
    grafico.show()

# analisando os gráficos, descobre-se muita coisa:
# clientes do contrato mensal: TODOS cancelam:
    # oferecer desconto nos planos anuais e trimestrais
# se eu tirar os contratos mensais, já reduz a taxa de cancelamento!
tabela = tabela[tabela["duracao_contrato"]!="Monthly"]
# clientes que ligam mais de 4 vezes para o callcenter, cancelam:
    # criar um processo para resolver o problema do cliente em no máx 3 ligações
tabela = tabela[tabela["ligacoes_callcenter"]<=4]
# clientes que atrasam em mais de 20 dias, cancelam:
    # política de resolver atrasos em até 20 dias (equipe de finanças)
tabela = tabela[tabela["dias_atraso"]<=20]
# ele vai mostrar como seria a situação se eu retirasse os contratos mensais, as ligações maiores que 4 e dos dias de atraso maisores que 20
print(tabela["cancelou"].value_counts())
print(tabela["cancelou"].value_counts(normalize = True).map("{:.1%}".format))

# Por fim:
# A remoção dos contratos mensais, ligações maiores que 4 e atrasos de pagamentos maiores que 20 dias alteraram significativamente a distribuição dos cancelamentos.
# A proporção de não cancelamentos (0.0) aumentou de 43.2% para 81.6%, indicando que muitos desses casos foram removidos.
# A proporção de cancelamentos (1.0) diminuiu de 56.8% para 18.4% após as remoções.
