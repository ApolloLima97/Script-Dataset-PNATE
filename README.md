📊 Script-Dataset-PNATE
Análise Exploratória dos Repasses do PNATE com Python
<p align="left"> <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" /> <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-yellow?logo=pandas&logoColor=white" /> <img src="https://img.shields.io/badge/Matplotlib-Visualization-orange?logo=matplotlib&logoColor=white" /> <img src="https://img.shields.io/badge/Seaborn-Statistical%20Plots-teal?logo=seaborn&logoColor=white" /> <img src="https://img.shields.io/badge/PNATE-Dataset-red" /> </p>
📌 Sobre o Projeto

Este repositório contém um script em Python desenvolvido para realizar uma análise detalhada dos repasses do PNATE (Programa Nacional de Apoio ao Transporte Escolar).

O código faz limpeza do dataset, cálculo de estatísticas e geração de diversas visualizações para compreender como os valores são distribuídos entre Infantil, Fundamental e Médio, permitindo análise por:

Brasil (todos os estados e municípios)

Estado (UF)

Município específico

Ele foi criado como base para estudos, TCC, projetos acadêmicos e análises em Data Science.

🚀 Principais Funcionalidades

✔ Leitura automática do arquivo CSV

✔ Limpeza de dados e padronização (UF, municípios, valores monetários)

✔ Conversão do formato BRL → float

✔ Cálculo de estatísticas:

média

mediana

moda

mínimo e máximo

soma total dos repasses

análises com zeros e sem zeros

✔ Visualizações dinâmicas:

Gráfico de barras (Infantil × Fundamental × Médio)

Gráfico de pizza por região (nível Brasil)

Boxplot comparativo por estado

Gráficos de dispersão entre etapas

✔ Agrupamentos por estado ou região

✔ Identificação automática do nível analisado (Brasil / Estado / Município)

📚 Bibliotecas Utilizadas
🐍 Python

Linguagem principal para análise e visualização de dados.

📊 Pandas

Usado para manipulação, limpeza e análise do dataset.

Permite:

carregar o CSV

organizar dados em DataFrames

padronizar campos

converter valores monetários

filtrar por Brasil, estado ou município

calcular estatísticas

agrupar dados por Estado/Região

📈 Matplotlib

Base da renderização dos gráficos:

criação das figuras

títulos e eixos

exibição final

ajustes de layout

🎨 Seaborn

Usado para gráficos estatísticos mais avançados:

scatter plots

boxplots

paletas de cores

estética aprimorada

📁 Estrutura do Projeto
/
├── trabalho-dataset.py     # Script completo da análise
├── PNATE - REPASSES.csv    # Dataset utilizado (se incluído)
└── README.md               # Esta documentação

🖼️ Exemplo de Gráfico (opcional)

Você pode adicionar depois, basta salvar uma imagem no repositório:

## 📊 Exemplo de Gráfico
![Gráfico Exemplo](./exemplo-grafico.png)

🚀 Como Executar

Instale as dependências:

pip install pandas matplotlib seaborn


Execute o script:

python trabalho-dataset.py


Siga o menu interativo para escolher:

Brasil

Um estado

Um município

🎯 Objetivo

O objetivo deste projeto é facilitar a exploração dos repasses do PNATE, permitindo que estudantes, pesquisadores e analistas entendam melhor como os recursos são distribuídos.
O código pode ser adaptado para outras bases públicas e para projetos acadêmicos de Data Science.

📄 Licença

Este projeto pode ser utilizado livremente para estudo, análise e extensão.
Para uso comercial, recomenda-se criar uma licença apropriada (MIT, GPL etc.).

🤝 Contribuições

Contribuições são bem-vindas!
Sugestões de melhoria, novos gráficos e novas funcionalidades podem ser enviadas via Pull Request.
