import discord
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Criando os intents
intents = discord.Intents.default()
intents.message_content = True  # Ativa a leitura do conteúdo das mensagens

# Inicializando o cliente Discord com os intents
client = discord.Client(intents=intents)

# ID do canal onde os resultados serão enviados
CHANNEL_ID = 1309193189743398913  # Substitua com o ID do seu canal do Discord

# Função para enviar a mensagem ao Discord
async def enviar_resultado(resultados):
    channel = client.get_channel(CHANNEL_ID)  # Pega o canal usando o ID
    if channel:
        await channel.send(resultados)  # Envia os resultados no canal

# Inicializar o driver do navegador (Chrome)
driver = webdriver.Chrome()

# Abrir o site
driver.get('https://m.betpix365.com/ptb/games/livecasino/detail/18280/evol_BacBo00000000001_BRL')

# Espera até o primeiro iframe estar carregado
while True:
    try:
        iframe_1_elements = driver.find_elements(By.XPATH, '/html/body/app-root/app-out-component/div[1]/main/app-games/app-live-casino-details/div/div/div/div/div[2]/iframe')
        if iframe_1_elements:
            iframe_1 = iframe_1_elements[0]
            driver.switch_to.frame(iframe_1)
            print("Iframe 1 carregado e trocado com sucesso.")
            break
        else:
            print("Aguardando iframe 1 carregar...")
            time.sleep(2)  # Aguarda por 2 segundos antes de tentar novamente
    except Exception as e:
        print(f"Erro ao tentar trocar para o iframe 1: {e}")
        time.sleep(2)

# Espera até o segundo iframe estar carregado
while True:
    try:
        iframe_2_elements = driver.find_elements(By.XPATH, '/html/body/div[5]/div[2]/iframe')
        if iframe_2_elements:
            iframe_2 = iframe_2_elements[0]
            driver.switch_to.frame(iframe_2)
            print("Iframe 2 carregado e trocado com sucesso.")
            break
        else:
            print("Aguardando iframe 2 carregar...")
            time.sleep(2)  # Aguarda por 2 segundos antes de tentar novamente
    except Exception as e:
        print(f"Erro ao tentar trocar para o iframe 2: {e}")
        time.sleep(2)

# Variáveis para armazenar os resultados e sequências
resultados_anteriores = []  # Armazenar resultados anteriores
sequencia_atual = []  # Para detectar sequências de resultados

# Função para calcular probabilidades de P e B
def calcular_probabilidade(resultados_anteriores):
    """
    Calcula a probabilidade de cada cor (P e B) com base nos resultados anteriores.
    """
    total = len(resultados_anteriores)
    if total == 0:
        return {'P': 0.5, 'B': 0.5, 'T': 0.0}  # Se não houver resultados, retorna 50% para P e B, e 0 para T

    p_prob = resultados_anteriores.count('P') / total
    b_prob = resultados_anteriores.count('B') / total
    t_prob = resultados_anteriores.count('T') / total  # Empates não são considerados na aposta
    
    return {'P': p_prob, 'B': b_prob, 'T': t_prob}

# Função para sugerir qual cor apostar (de acordo com a sua estratégia)
def sugerir_aposta(resultados_anteriores):
    """
    Sugerir qual cor apostar com base nos resultados anteriores.
    Segue a lógica:
    - Se o resultado for B, aposta em P
    - Se for P, aposta em B
    - Se for T, aposta em B
    """
    if len(resultados_anteriores) > 0:
        ultimo_resultado = resultados_anteriores[-1]  # Pega o último resultado
        
        if ultimo_resultado == 'B':
            return "Aposte em P (Player) - AZUL"
        elif ultimo_resultado == 'P':
            return "Aposte em B (Banker) - VERMELHO"
        elif ultimo_resultado == 'T':
            return "Aposte em B (Banker) - VERMELHO"
    return "Aguardando o primeiro resultado..."

# Espera até os resultados estarem disponíveis e atualiza continuamente
print("Aguardando e atualizando resultados dinamicamente...")

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

    # Loop para capturar os resultados do site
    while True:
        try:
            # Tenta encontrar os resultados na página
            resultados_elements = driver.find_elements(By.XPATH, '/html/body/div[4]/div/div/div[2]/div[6]/div/div[1]/div/div/div')
            if resultados_elements:
                resultados = resultados_elements[0]
                resultados_text = resultados.text

                # Se os resultados mudaram, atualize a lista
                if resultados_text not in resultados_anteriores:
                    # Armazenando o novo resultado
                    resultados_anteriores.append(resultados_text)
                    sequencia_atual.append(resultados_text)  # Adiciona à sequência

                    # Exibir os resultados
                    resultados_split = resultados_text.split("\n")
                    result_line = " | ".join(resultados_split)
                    print(f"Resultados: {result_line}")

                    # Calcular probabilidades de P, B e T
                    probabilidades = calcular_probabilidade(resultados_anteriores)
                    print(f"Probabilidades - P: {probabilidades['P']:.2f}, B: {probabilidades['B']:.2f}, T: {probabilidades['T']:.2f}")
                    
                    # Sugerir qual cor apostar com base no último resultado
                    estrategia = sugerir_aposta(resultados_anteriores)
                    print(f"Estratégia sugerida: {estrategia}")

                    # Enviar os resultados ao Discord
                    await enviar_resultado(result_line)
                    
            else:
                print("Aguardando resultados...")

            # Aguardar um tempo antes de tentar capturar novamente
            time.sleep(5)  # A cada 5 segundos tenta capturar os resultados novamente

        except Exception as e:
            print(f"Erro ao tentar capturar os resultados: {e}")
            time.sleep(2)  # Aguarda por 2 segundos antes de tentar novamente

# Rodando o bot
client.run('MTMwOTE3ODc3NTkyNTI5NzIxMg.GMb2G0.8bDxnoPEt0EqLPI1Qjsyo6CiqEZkJRjr_u1fI4')  # Substitua pelo seu token do bot
