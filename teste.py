import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

print('Executando...')
opcoes = Options()
opcoes.add_argument("--disable-blink-features=AutomationControlled")
opcoes.add_argument("start-maximized")
opcoes.add_argument("user-agent=Mozilla/5.0)(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opcoes)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """
})

arquivo_dados = 'dados.csv'
try:
    pd.read_csv(arquivo_dados)
    print(f"'{arquivo_dados}' encontrado.")
except FileNotFoundError:
    print(f"'{arquivo_dados}' não encontrado. Criando um novo.")
    df_vazio = pd.DataFrame(columns=['ID', 'Data', 'Hora', 'Tempo'])
    df_vazio.to_csv(arquivo_dados, index=False, header=True, encoding='utf-8')

try:
    driver.get("https://www.google.com")
    busca = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
    for letra in "amazon":
        busca.send_keys(letra)
        time.sleep(random.uniform(0.1, 0.3))
    time.sleep(random.uniform(0.5, 1.0))
    busca.send_keys(Keys.RETURN)

    link_amazon = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'https://www.amazon.com.br/')]")))
    inicio_tempo = time.time()
    link_amazon.click()
    time.sleep(random.uniform(3, 5))

finally:
    tempo_final = time.time() - inicio_tempo
    agora = time.localtime()
    id_gerado = int(np.round(random.randrange(10000000), 0))

    data_formatada = f"{agora.tm_mday:02d}/{agora.tm_mon:02d}/{agora.tm_year}"
    hora_formatada = f"{agora.tm_hour:02d}:{agora.tm_min:02d}"

    print('---------------------------------')
    print(f"Data : {data_formatada}")
    print(f"Hora : {hora_formatada}")
    print(f"Tempo: {tempo_final:.2f} segundos")
    print(f"ID : {id_gerado}")
    print('---------------------------------')

    novo_registro = pd.DataFrame({
        'ID': [id_gerado],
        'Data': [data_formatada],
        'Hora': [hora_formatada],
        'Tempo': [round(tempo_final, 2)]
    })
    novo_registro.to_csv(arquivo_dados, mode='a', index=False, header=False, encoding='utf-8')

    df_atual = pd.read_csv(arquivo_dados, header=0, encoding='utf-8')
    print("Conteúdo de dados.csv:")
    print(df_atual.to_string(index=False))

    driver.quit()


# Gerando os Gráficos (Linhas Coloridas por Local com Data/Hora em Todos os Pontos)

locais_arquivos = {
    'Local': 'dados.csv',
    'Senai': 'dados_senai.csv',
    'Isaque': 'dados_isaque.csv',
    'Felipe L': 'dados_felipel.csv',
    'Dudu': 'dados_dudu.csv',
    'Vinicius C': 'dados_vinic.csv',
    'Felipe S': 'dados_felipes.csv',
    'Estevão': 'dados_estevao.csv',
}

num_locais = len(locais_arquivos)
cols_grafico = 3
linhas_grafico = (num_locais + cols_grafico - 1) // cols_grafico

fig, eixos = plt.subplots(linhas_grafico, cols_grafico, figsize=(cols_grafico * 7, linhas_grafico * 4.5))
eixos = eixos.flatten()

# Paleta de cores vibrantes e distintas para cada local
cores_locais = [
    '#1f77b4',  # Azul (Local)
    '#ff7f0e',  # Laranja (Senai)
    '#2ca02c',  # Verde (Isaque)
    '#d62728',  # Vermelho (Felipe L)
    '#9467bd',  # Roxo (Dudu)
    '#8c564b',  # Marrom (Vinicius C)
    '#e377c2',  # Rosa (Felipe S)
    '#7f7f7f',  # Cinza (Estevão)
]

# Cores para mínimo e máximo de cada linha
cor_min_ponto = '#32CD32' # Verde Lima
cor_max_ponto = '#FF0000' # Vermelho Puro

for i, (nome, caminho_arq) in enumerate(locais_arquivos.items()):
    eixo_atual = eixos[i]
    cor_da_linha = cores_locais[i % len(cores_locais)] # Atribui uma cor da lista, repetindo se necessário

    try:
        df_local = pd.read_csv(caminho_arq, header=0, encoding='utf-8')

        if not df_local.empty and 'Tempo' in df_local.columns and 'Hora' in df_local.columns:
            
            # Calcula min e max para o dataset atual (por local)
            min_tempo_local = df_local['Tempo'].min()
            max_tempo_local = df_local['Tempo'].max()

            # Plota a linha principal com a cor específica do local
            eixo_atual.plot(df_local.index, df_local['Tempo'], color=cor_da_linha, 
                            marker='o', linestyle='-', linewidth=2, markersize=6, 
                            label=f'Tempo de Resposta ({nome})')

            # Adiciona os pontos com cores de destaque e labels de data/hora
            for idx, row in df_local.iterrows():
                tempo_atual = row['Tempo']
                data_hora_label = f"{row['Data']}\n{row['Hora']}"

                # Define a cor do marcador e do texto
                marker_color = cor_da_linha # Cor padrão do marcador é a da linha do local
                text_color = 'black'        # Cor padrão para o texto da data/hora
                va_position = 'bottom'      # Posição vertical padrão do texto
                y_offset = (df_local['Tempo'].max() * 0.05)

                if tempo_atual == min_tempo_local:
                    marker_color = cor_min_ponto
                    text_color = cor_min_ponto
                    va_position = 'top' # Posiciona o texto abaixo para mínimos
                    y_offset = -(df_local['Tempo'].max() * 0.08) # Offset negativo para mínimos
                elif tempo_atual == max_tempo_local:
                    marker_color = cor_max_ponto
                    text_color = cor_max_ponto
                    va_position = 'bottom' # Posiciona o texto acima para máximos
                    y_offset = (df_local['Tempo'].max() * 0.08) # Offset positivo para máximos
                
                # Plota o marcador para cada ponto
                eixo_atual.plot(idx, tempo_atual, marker='o', markersize=6, color=marker_color, zorder=5)
                
                # Adiciona o texto da data/hora (e o valor do tempo)
                eixo_atual.text(idx, tempo_atual + y_offset,
                                f"{tempo_atual:.2f}s\n{data_hora_label}",
                                ha='center', va=va_position, fontsize=7, color=text_color,
                                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))


            eixo_atual.set_xlabel('Execução (Ordem Cronológica)', fontweight='bold', fontsize=9)
            eixo_atual.set_ylabel('Tempo (segundos)', fontweight='bold', fontsize=9)
            eixo_atual.set_title(f'{nome}', fontsize=12)

            # Os ticks X serão os índices para manter a linha contínua
            eixo_atual.set_xticks(df_local.index)
            # Remove os labels dos ticks X, pois já temos nos pontos.
            eixo_atual.set_xticklabels([]) 
            eixo_atual.tick_params(axis='x', which='major', pad=5)

            # Legenda para as cores dos pontos
            legenda_elementos = [
                plt.Line2D([0], [0], color=cor_da_linha, lw=2, marker='o', markersize=6, label=f'Tempo de Resposta ({nome})'),
                plt.Line2D([0], [0], color=cor_min_ponto, lw=0, marker='o', markersize=8, label='Mínimo do Local'),
                plt.Line2D([0], [0], color=cor_max_ponto, lw=0, marker='o', markersize=8, label='Máximo do Local')
            ]
            
            eixo_atual.legend(handles=legenda_elementos, loc='upper left', fontsize=7)

            eixo_atual.grid(axis='y', linestyle='--', alpha=0.7)
        else:
            eixo_atual.set_visible(False)
            print(f"Aviso: Arquivo '{caminho_arq}' vazio, sem 'Tempo' ou sem 'Hora'. Gráfico para {nome} não aparece.")
    except FileNotFoundError:
        eixo_atual.set_visible(False)
        print(f"Erro: Arquivo '{caminho_arq}' não encontrado. Gráfico para {nome} não aparece.")

# Remove subplots vazios no final
for i in range(num_locais, len(eixos)):
    fig.delaxes(eixos[i])

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.suptitle('Variação do Tempo de Resposta da Amazon por Local', fontsize=18, fontweight='bold')
plt.show()

print('Acabou')