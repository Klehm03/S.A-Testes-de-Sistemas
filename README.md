# S.A Testes de Sistemas
Atividade Avaliativa de Testes de Sistemas do SENAI

Resumo do Projeto: Monitoramento de Tempo de Resposta da Amazon
Este projeto utiliza Python e a biblioteca Selenium para automatizar a navegação na web e medir o tempo que leva para o site da Amazon carregar.
#--

Como Funciona:
Automação de Navegação: O script abre o Google Chrome, pesquisa por "amazon" no Google e clica no link oficial da Amazon Brasil.

Medição de Desempenho: Ele calcula exatamente quanto tempo leva desde o clique no link da Amazon até a página carregar por completo.

Registro de Dados: Cada execução gera um ID único, registra a data, a hora e o tempo de resposta em segundos. Esses dados são armazenados de forma organizada em um arquivo CSV chamado dados.csv, sem apagar informações anteriores.

Análise Visual: Além de registrar, o projeto gera gráficos de linha interativos usando matplotlib. Esses gráficos mostram a variação do tempo de resposta ao longo do tempo, e o mais interessante é que ele consegue comparar os dados de várias fontes (outros arquivos CSV, 
como dados_senai.csv, dados_isaque.csv, etc.), simulando resultados de diferentes locais ou usuários. Os pontos de tempo mínimo e máximo em cada gráfico são destacados para facilitar a análise.

#--
Para que Serve:
O objetivo principal é monitorar e visualizar a performance de carregamento da Amazon de diferentes pontos, ajudando a identificar variações ou problemas de latência ao longo do tempo e em diversas localidades.
