# -*- coding: utf-8 -*-
"""TCC_ Análise da Arrecadação_Ciência de Dados_FURG.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BgFkgQDxcnsS0NmBuDzrA4tD0cbgDLwc

# **Tratamento, Visualização e Análise dos Dados da Arrecadação Federal nos anos de 2017 a 2021**
#Notebook do TCC da Pós-Graduação em Ciência de Dados - FURG
## Carlos Eduardo Fonseca Cardoso
## Fernando José Mostaert Locio
### Veruska Bersanetti Barbieri Sampaio

Base de dados obtida em **https**://www.gov.br/receitafederal/pt-br/acesso-a-informacao/dados-abertos/receitadata/arrecadacao/analise-gerencial-da-arrecadacao-angela-1 Acesso em janeiro de 2022.
"""

#Importando as bibliotecas
import pandas as pd
import numpy as np
import plotly.express as px

#Carregando os dados e visualizando as cinco primeiras linhas do data frame
df = pd.read_excel('/content/Angela - Arrecadação por mês - Cnae e Tributo.xlsx')
df.head()

#Vendo as cinco últimas linhas
df.tail()

"""# **Obtendo informações sobre a base de dados**"""

#identificando as colunas
df.columns

#Identificando os setores de arrecadação (coluna "Seção - Nome")
df['Seção - Nome'].unique()

#Outras informações
df.info()

#Identificando a quantitdade de dados faltantes em cada coluna
df.isnull().sum()

"""# Tratamento e preparação dos dados"""

#removendo a coluna sem interesse: " Seção - Sigla"
df2 = df.drop('Seção - Sigla', axis=1)
df2.head()

#Renomeando a coluna "Seção - Nome" para "Setor"
df2.rename(columns={'Seção - Nome': 'Setor'}, inplace = True)
df2. head()

#Estabelecendo-se a análise dos últimos 5 anos, vamos remover as informações do ano de 2016.
#Ficamos com 1440 linhas
df3 = df2.drop(df2[df2.Ano == 2016].index)
df3

#Preenchendo valores nulos (NaN) com zero
df4 = df3.fillna(value=0)
df4

#Organizando a formatação dos valores numéricos
#No Pandas, o separador de milhar é a vírgula e o das casas decimais é o ponto
pd.set_option('float_format','{:,.2f}'.format)
df4

#Criando a coluna "Total", que receberá a soma dos tributos em cada mês e ano por setor
df4['Total'] = (df4['II'] + df4['IE'] + df4['IPI'] + df4['IRPF'] + df4['IRPJ'] + df4['IRRF'] + df4['IOF'] + df4['ITR'] 
                + df4['Cofins'] + df4['Pis/Pasep'] + df4['CSLL'] + df4['Cide'] + df4['Contribuição Previdenciária'] + df4['CPSSS'] 
                + df4['Pagamento Unificado'] + df4['Outras Receitas Administradas'] + df4['Receitas Não Administradas'])
df4.head()

#Informações sobre o data frame após tratamento e preparação dos dados
df4.info()

"""# **Análise e visualização dos dados**
1. Utilizamos principalmente a função groupby() combinada com a função de agregação *agg*.  
2. Para os gráficos, utilizamos a biblioteca Plotly, especificamente Plotly Express.
"""

#Calculando o total da arrecadação por ano usando a função de agregação 'agg'
df4.groupby('Ano').agg({'Total':np.sum})

#Resetando os índices para fazer com que 'Ano' e 'Total' sejam colunas
df_agrupado_pelo_ano = df4.groupby('Ano', sort=False).agg({'Total':np.sum}).reset_index()
df_agrupado_pelo_ano

#Plotando gráfico de barras da arrecadação total por ano
fig = px.bar(df_agrupado_pelo_ano, x='Ano', y='Total', width=500, height=500,
       color_discrete_sequence=px.colors.qualitative.D3, template='plotly_white')
fig.show()

#Plotando gráfico de linha da arrecadação total por ano
fig = px.line(df_agrupado_pelo_ano, x='Ano', y='Total', width=500, height=500, 
        color_discrete_sequence=px.colors.qualitative.D3, template='plotly_white')
fig.show()

#Agrupando a arrecadação total por ano e Mês
df_agrupado_pelo_ano_e_mes = df4.groupby(['Ano', 'Mês'], sort=False).agg({'Total':np.sum}).reset_index()
df_agrupado_pelo_ano_e_mes

#Gráfico da evolução mensal da arrecadação por ano
px.line(df_agrupado_pelo_ano_e_mes, x='Mês', y='Total', color="Ano", width=1000, height=500,
        color_discrete_sequence=px.colors.qualitative.D3, template='plotly_white')

#Plotando gráfico de barras da arrecadação total por ano e mês
px.bar(df_agrupado_pelo_ano_e_mes, x='Ano', y='Total', color = 'Mês', barmode = 'group', width=1100,
       height=500, color_discrete_sequence=px.colors.qualitative.Set3, template='plotly_white')

#Agrupando total da arrecadaçao por ano e setor
df_agrupado_pelo_ano_e_setor = df4.groupby(['Ano', 'Setor'], sort=False).agg({'Total':np.sum}).reset_index()
df_agrupado_pelo_ano_e_setor

#Gráfico de barras do total da arrecadaçao por ano e setor
px.bar(df_agrupado_pelo_ano_e_setor, x='Ano', y='Total', color = 'Setor', barmode = 'group',
       color_discrete_sequence=px.colors.qualitative.Set3, template='plotly_white')

#Setores que tiveram arrecadação acima de 50 bilhões -2017 a 2021
df_mask_50bi=df_agrupado_pelo_ano_e_setor['Total']>=50000000000
filtro_df_50bi = df_agrupado_pelo_ano_e_setor[df_mask_50bi]
filtro_df_50bi

#Visualização gráfica dos setores com arrecadação acima de 50 bilhões - 2017 a 2021
px.bar(filtro_df_50bi, x='Ano', y='Total', color = 'Setor', barmode = 'group',
       color_discrete_sequence=px.colors.qualitative.Set3, template='plotly_white', width=1100,
       height=500)

#Filtrando o ano de 2017 por Setor
df_mask = df_agrupado_pelo_ano_e_setor['Ano']==2017
filtro_df_2017 = df_agrupado_pelo_ano_e_setor[df_mask]
#Ordenando o data frame filtrado, de forma decrescente por total
filtro_df_2017 = filtro_df_2017.sort_values(by=['Total'],ignore_index=True, ascending=False)
filtro_df_2017

#Filtrando o ano de 2018 por Setor
df_mask = df_agrupado_pelo_ano_e_setor['Ano']==2018
filtro_df_2018 = df_agrupado_pelo_ano_e_setor[df_mask]
#Ordenando o data frame filtrado, de forma decrescente por total
filtro_df_2018 = filtro_df_2018.sort_values(by=['Total'],ignore_index=True, ascending=False)
filtro_df_2018

#Filtrando o ano de 2019 por Setor
df_mask = df_agrupado_pelo_ano_e_setor['Ano']==2019
filtro_df_2019 = df_agrupado_pelo_ano_e_setor[df_mask]
#Ordenando o data frame filtrado, de forma decrescente por total
filtro_df_2019 = filtro_df_2019.sort_values(by=['Total'],ignore_index=True, ascending=False)
filtro_df_2019

#Filtrando o ano de 2020 por Setor
df_mask = df_agrupado_pelo_ano_e_setor['Ano']==2020
filtro_df_2020 = df_agrupado_pelo_ano_e_setor[df_mask]
#Ordenando o data frame filtrado, de forma decrescente por total
filtro_df_2020 = filtro_df_2020.sort_values(by=['Total'],ignore_index=True, ascending=False)
filtro_df_2020

#Filtrando o ano de 2021 por Setor
df_mask = df_agrupado_pelo_ano_e_setor['Ano']==2021
filtro_df_2021 = df_agrupado_pelo_ano_e_setor[df_mask]
#Ordenando o data frame filtrado, de forma decrescente por total
filtro_df_2021 = filtro_df_2021.sort_values(by=['Total'],ignore_index=True, ascending=False)
filtro_df_2021

#Gráfico de barras da arrecadação por setor - 2017 a 2021
fig1 = px.bar(filtro_df_2017, x='Ano', y='Total', color = 'Setor', barmode = 'group', orientation = 'v', width=1000, height=500)
fig1.show()
fig2 = px.bar(filtro_df_2018, x='Ano', y='Total', color = 'Setor', barmode = 'group', orientation = 'v', width=1000, height=500)
fig2.show()
fig3 = px.bar(filtro_df_2019, x='Ano', y='Total', color = 'Setor', barmode = 'group', orientation = 'v', width=1000, height=500)
fig3.show()
fig4 = px.bar(filtro_df_2020, x='Ano', y='Total', color = 'Setor', barmode = 'group', orientation = 'v', width=1000, height=500)
fig4.show()
fig5 = px.bar(filtro_df_2021, x='Ano', y='Total', color = 'Setor', barmode = 'group', orientation = 'v', width=1000, height=500)
fig5.show()

#Vendo os setores de maior arrecadação por percentual - 2017 a 2021 
fig1 = px.pie(filtro_df_2017, names='Setor', values = 'Total', width=900, height=500, title = 2017)
fig1.show()
fig2 = px.pie(filtro_df_2018, names='Setor', values = 'Total', width=1000, height=500, title = 2018) 
fig2.show()
fig3 = px.pie(filtro_df_2019, names='Setor', values = 'Total', width=1000, height=500, title = 2019) 
fig3.show()
fig4 = px.pie(filtro_df_2020, names='Setor', values = 'Total', width=1000, height=500, title = 2020) 
fig4.show()
fig5 = px.pie(filtro_df_2021, names='Setor', values = 'Total', width=1000, height=500, title = 2021) 
fig5.show()

#Melhorando a visualização com apenas os setores que tiveram mais de 10 bilhões de arrecadação - 2017 a 2021. 
#Os setores com arrecadação menor que 10 bi, foram renomeados para "Outros Serotres"
filtro_df_2017.loc[filtro_df_2017['Total'] <= 10000000000, 'Setor'] = 'Outros Setores'
fig1 = px.pie(filtro_df_2017, values='Total', names='Setor', title = 2017, width=900, height=500)
fig1.show()

filtro_df_2018.loc[filtro_df_2018['Total'] <= 10000000000, 'Setor'] = 'Outros Setores'
fig2 = px.pie(filtro_df_2018, values='Total', names='Setor', title = 2018, width=900, height=500)
fig2.show()

filtro_df_2019.loc[filtro_df_2019['Total'] <= 10000000000, 'Setor'] = 'Outros Setores'
fig3 = px.pie(filtro_df_2019, values='Total', names='Setor', title = 2019, width=900, height=500)
fig3.show()

filtro_df_2020.loc[filtro_df_2020['Total'] <= 10000000000, 'Setor'] = 'Outros Setores'
fig4 = px.pie(filtro_df_2020, values='Total', names='Setor', title = 2020, width=900, height=500)
fig4.show()

filtro_df_2021.loc[filtro_df_2021['Total'] <= 10000000000, 'Setor'] = 'Outros Setores'
fig5 = px.pie(filtro_df_2021, values='Total', names='Setor', title = 2021, width=900, height=500)
fig5.show()

"""# **Analisando o IRPF**"""

#Agrupando a arrecadação de 2017 a 2021 pelo IRPF (anos e meses). 
df_agrupado_pelo_ano_mes_e_IRPF = df4.groupby(['Ano', 'Mês'], sort=False).agg({'IRPF':np.sum}).reset_index()
df_agrupado_pelo_ano_mes_e_IRPF

#Agrupando a arrecadação de 2017 a 2021 pelo IRPF (apenas anos). 
df_agrupado_pelo_ano_e_IRPF = df4.groupby(['Ano'], sort=False).agg({'IRPF':np.sum}).reset_index()
df_agrupado_pelo_ano_e_IRPF

#Visualizando arrecadação do IRPF de 2017 a 2021
px.bar(df_agrupado_pelo_ano_e_IRPF, x='Ano', y='IRPF', width=500, height=500,
       color_discrete_sequence=px.colors.qualitative.D3, template='plotly_white')

#Verificando o comportamento da arrecadação do IRPF
px.line(df_agrupado_pelo_ano_e_IRPF, x='Ano', y='IRPF', width=700, height=600, 
        color_discrete_sequence=px.colors.qualitative.D3, template='plotly_white')

#Vendo que nos anos de 2020 e 2021 o IRPF teve comportamento diferente
px.line(df_agrupado_pelo_ano_mes_e_IRPF, x='Mês', y='IRPF', color="Ano", width=1000, height=500,
         color_discrete_sequence=px.colors.qualitative.D3, template='plotly_white')

"""# **Manipulação e análise dos dados (continuação)**
 Foi realizada a inversão do data frame
  
"""

#Inicialmente, agrupou-se a arrecadação de 2017 a 2021 apenas pelo ano e pela soma de cada tributo 
df_agrupado_pelo_ano_e_tributos = df4.groupby(['Ano'], sort=False).agg({'II':np.sum, 'IE':np.sum, 'IPI':np.sum,'IRPF':np.sum,'IRPJ':np.sum,'IRRF':np.sum,'IOF':np.sum,'ITR':np.sum,'Cofins':np.sum,'Pis/Pasep':np.sum,'CSLL':np.sum,'Cide':np.sum, 'Contribuição Previdenciária':np.sum, 'CPSSS':np.sum, 'Pagamento Unificado':np.sum, 'Outras Receitas Administradas':np.sum, 'Receitas Não Administradas':np.sum}).reset_index()
df_agrupado_pelo_ano_e_tributos

#Inveretendo o data frame agrupado por ano e tributos
df_invertido_agrupado_pelo_ano_e_tributos = df_agrupado_pelo_ano_e_tributos.transpose().reset_index()
df_invertido_agrupado_pelo_ano_e_tributos

#Retirando a primeira linha do data frame acima
df2_invertido_agrupado_pelo_ano_e_tributos = df_invertido_agrupado_pelo_ano_e_tributos.drop(0)
df2_invertido_agrupado_pelo_ano_e_tributos

#Alterando o nome das colunas
df2_invertido_agrupado_pelo_ano_e_tributos.rename(columns={'index': 'Tributo', 0: '2017', 1 : '2018', 2 : '2019', 3 : '2020', 4 : '2021'}, inplace = True)
df2_invertido_agrupado_pelo_ano_e_tributos

#Filtrando cada ano e ordenando de forma decrescente (do tributo de maior arrecadação para o de menor)
#2017
df2_invertido_agrupado_pelo_ano_e_tributos[['Tributo','2017']].sort_values(by=['2017'], ascending=False)

#2018
df2_invertido_agrupado_pelo_ano_e_tributos[['Tributo','2018']].sort_values(by=['2018'],ascending=False)

#2019
df2_invertido_agrupado_pelo_ano_e_tributos[['Tributo','2019']].sort_values(by=['2019'], ascending=False)

#2020
df2_invertido_agrupado_pelo_ano_e_tributos[['Tributo','2020']].sort_values(by=['2020'], ascending=False)

#2021
df2_invertido_agrupado_pelo_ano_e_tributos[['Tributo','2021']].sort_values(by=['2021'], ascending=False)

#Vendo no gráfico o valor da arrecadação por tributo em cada ano do período.
fig1 = px.bar(df2_invertido_agrupado_pelo_ano_e_tributos[['Tributo','2017']].sort_values(by=['2017'],ascending=True), x='2017', y= 'Tributo', width=550, height=450, color_discrete_sequence=px.colors.qualitative.D3, template='plotly_white') 
fig1.show()

fig2 = px.bar(df2_invertido_agrupado_pelo_ano_e_tributos[['Tributo','2018']].sort_values(by=['2018'],ascending=True), x='2018', y= 'Tributo', width=550, height=450, color_discrete_sequence=px.colors.qualitative.D3, template='plotly_white') 
fig2.show()

fig3 = px.bar(df2_invertido_agrupado_pelo_ano_e_tributos[['Tributo','2019']].sort_values(by=['2019'],ascending=True), x='2019', y= 'Tributo', width=550, height=450, color_discrete_sequence=px.colors.qualitative.D3, template='plotly_white') 
fig3.show()

fig4 = px.bar(df2_invertido_agrupado_pelo_ano_e_tributos[['Tributo','2020']].sort_values(by=['2020'],ascending=True), x='2020', y= 'Tributo', width=550, height=450, color_discrete_sequence=px.colors.qualitative.D3, template='plotly_white') 
fig4.show()

fig5 = px.bar(df2_invertido_agrupado_pelo_ano_e_tributos[['Tributo','2021']].sort_values(by=['2021'],ascending=True), x='2021', y= 'Tributo', width=550, height=450, color_discrete_sequence=px.colors.qualitative.D3, template='plotly_white') 
fig5.show()

#Mostrando arrecadação do período - Percentual por tributo.
fig1 = px.pie(df2_invertido_agrupado_pelo_ano_e_tributos, names= 'Tributo', values ='2017', width=850, height=520, title = 2017)
fig1.update_traces(textposition='inside', textinfo='percent+label') 
fig1.show()

fig2 = px.pie(df2_invertido_agrupado_pelo_ano_e_tributos, names= 'Tributo', values ='2018', width=850, height=520, title = 2018)
fig2.update_traces(textposition='inside', textinfo='percent+label') 
fig2.show()

fig3 = px.pie(df2_invertido_agrupado_pelo_ano_e_tributos, names= 'Tributo', values ='2019', width=850, height=520, title = 2019)
fig3.update_traces(textposition='inside', textinfo='percent+label') 
fig3.show()

fig4 = px.pie(df2_invertido_agrupado_pelo_ano_e_tributos, names= 'Tributo', values ='2020', width=850, height=520, title = 2020)
fig4.update_traces(textposition='inside', textinfo='percent+label') 
fig4.show()

fig5 = px.pie(df2_invertido_agrupado_pelo_ano_e_tributos, names= 'Tributo', values ='2021', width=850, height=520, title = 2021)
fig5.update_traces(textposition='inside', textinfo='percent+label') 
fig5.show()