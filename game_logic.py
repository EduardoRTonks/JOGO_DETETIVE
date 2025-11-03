import random
import time
import json

PERSONAGENS = {
    'Silas Stone': 'Corporativo, frio, tinha uma cópia ilegal da Chave Ômega. A corporação ganha com o seguro da estação.',
    'Engenheira Jade Jenkins': 'Prodígio técnica. Ignorada pela Comandante após avisar sobre "anomalias" de energia.',
    'Piloto Paxton Price': 'Piloto de transporte. Furiosa por sua suspensão. Estava confinado na Ponte de Comando.',
    'Comandante Victoria Volkova': 'A Comandante. Única (com Stone) com acesso à Chave Ômega. Suspendeu a Piloto Price recentemente.',
    'Dr. Alistair Armstrong': 'Biólogo-Chefe. Arrogante. Sua pesquisa vital foi cortada por Stone.',
    'Dr. Elias Erwin': 'Médico/Psicológo. Reportou o roubo de um sedativo forte de seus estoques na Ala Médica.',
    'Chefe Kaelen Knight': 'Chefe de Segurança. Metódico. Foi encontrado sedado perto do Compartimento de Carga.',
    'A.T.H.E.N.A.': 'a IA que gerencia a nave. ela Foi danificada e está "cega" para o ataque, mas ainda fornece outros dados (logs de portas, inventário) que servem como pistas que podem ser acessadas.'
}
SUSPEITOS = list(PERSONAGENS.keys())[:-1]
LOCAIS = [
    'Engenharia',
    'Compartimento de Carga',
    'Ala Médica',
    'Laboratório de Biociência',
    'Ponte de Comando'
]
ITENS = [
    'Seringa Sedativa',
    'Cortador a Plasma',
    'Unidade de Transmissão LR',
    'Chave de Acesso Ômega',
    'Vírus de Corrupção'
]
DIAS = 2
DURACAO_DIA = 120 
TEMPO_MAX_SEGUNDOS = DIAS * DURACAO_DIA
HORAS = DIAS * 24

ITEM_LOCAIS = {
    'Seringa Sedativa': 'Ala Médica',
    'Cortador a Plasma': 'Engenharia',
    'Unidade de Transmissão LR': 'Compartimento de Carga',
    'Chave de Acesso Ômega': 'Ponte de Comando',
    'Vírus de Corrupção': 'Laboratório de Biociência'
}
LOCAL_ACESSO = {
    'Engenharia': ['Engenheira Jade Jenkins', 'Comandante Victoria Volkova'],
    'Compartimento de Carga': ['Chefe Kaelen Knight', 'Piloto Paxton Price'],
    'Ala Médica': ['Dr. Elias Erwin', 'Dr. Alistair Armstrong'],
    'Laboratório de Biociência': ['Dr. Alistair Armstrong', 'Engenheira Jade Jenkins'],
    'Ponte de Comando': ['Comandante Victoria Volkova', 'Piloto Paxton Price', 'Silas Stone']
}
ALIBIS_FIXOS = {
    'Silas Stone': 'estava em uma chamada corporativa na Ponte de Comando, monitorado por logs externos.',
    'Engenheira Jade Jenkins': 'estava recalibrando sensores no Observatório, longe de todos os locais de itens.',
    'Piloto Paxton Price': 'estava confinado em seus aposentos (perto da Ponte) após sua suspensão.',
    'Comandante Victoria Volkova': 'estava na Engenharia oposta ao seu acesso à Ponte, verificando os danos da IA.',
    'Dr. Alistair Armstrong': 'estava trancado no Laboratório de Biociência analisando amostras contaminadas.',
    'Dr. Elias Erwin': 'estava na Ala Médica tratando o Chefe de Segurança sedado.',
    'Chefe Kaelen Knight': 'foi encontrado sedado e incapacitado perto do Compartimento de Carga.'
}
ARQUIVO_PONTUACOES = 'pontuacoes.json' 



def carregar_pontuacoes():
    """Carrega as pontuações do arquivo JSON."""
    try:
        with open(ARQUIVO_PONTUACOES, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Retorna lista vazia se o arquivo não existir ou estiver corrompido
        return []

def salvar_pontuacoes(nome, pontos):
    """Salva a nova pontuação no arquivo JSON."""
    if pontos <= 0: # Não salva pontuações de derrota
        return f"Pontuação de 0 não registrada no placar."

    pontuacoes = carregar_pontuacoes()
    pontuacoes.append({'nome': nome, 'pontos': pontos})
    
    try:
        with open(ARQUIVO_PONTUACOES, 'w') as f:
            json.dump(pontuacoes, f, indent=4)
        return f"Pontuação de {pontos} registrada para {nome}!"
    except IOError as e:
        return f"Erro ao salvar pontuação: {e}"

def mostrar_pontuacoes():
    """Exibe o placar dos 10 melhores jogadores."""
    pontuacoes = carregar_pontuacoes()
    
    if not pontuacoes:
        return "Nenhuma pontuação registrada ainda."

    # Ordena as pontuações da maior para a menor
    pontuacoes_ordenadas = sorted(pontuacoes, key=lambda p: p['pontos'], reverse=True)
    
    result = "=" * 30 + "\n"
    result += "       PLACAR DE LÍDERES\n"
    result += "=" * 30 + "\n"
    
    # Mostra apenas os 10 primeiros
    for i, score in enumerate(pontuacoes_ordenadas[:10]):
        result += f"{i+1: >2}. {score['nome']: <20} - {score['pontos']} pontos\n"
    result += "=" * 30
    
    return result

def apresentar_contexto():
    """Retorna o texto do contexto em vez de imprimir"""
    context = "=" * 60 + "\n"
    context += "       SABOTAGEM NA ARES-7\n"
    context += "     O PROBLEMA: AR E SILÊNCIO\n"
    context += "=" * 60 + "\n\n"
    context += "A ARES-7, uma estação de pesquisa em órbita de Marte, mergulha no caos.\n"
    context += "O Sistema de Suporte de Vida foi sabotado.\n"
    context += "A tripulação tem menos de 48 horas de oxigênio.\n\n"
    context += "Para piorar, o único transmissor de longo alcance foi roubado\n"
    context += "do Compartimento de Carga, cortando toda a comunicação com a Terra.\n\n"
    context += "O sabotador usou um vírus que corrompeu os logs de câmera da\n"
    context += "IA (A.T.H.E.N.A.) nos locais-chave.\n\n"
    context += "A única esperança da tripulação é usar a lógica para conectar os fatos\n"
    context += "restantes e descobrir o culpado antes que o tempo se esgote."
    
    return context

def apresentar_personagens():
    """Retorna o texto dos personagens em vez de imprimir"""
    result = "=" * 60 + "\n"
    result += "                   TRIPULANTES\n"
    result += "=" * 60 + "\n\n"
    for nome, descricao in PERSONAGENS.items():
        result += f" - {nome}: {descricao}\n"
    return result

def apresentar_regras():
    """Retorna o texto das regras em vez de imprimir"""
    result = "=" * 60 + "\n"
    result += "                         REGRAS\n"
    result += "=" * 60 + "\n"
    result += f"Objetivo: Descobrir o sabotador antes que o tempo ({TEMPO_MAX_SEGUNDOS // 60} minutos) se esgote.\n"
    result += "Pontuação: Você começa com 1000 pontos. Pedir pistas custa tempo E pontos.\n"
    result += "Consultar Pistas: Esta ação gasta tempo, mas fornece um fato chave para ajudar a encontrar o culpado.\n"
    result += "Arriscar o Culpado: Faça sua acusação final. Acertar salva a tripulação, errar significa fracasso imediato.\n\n"
    result += "Use a lógica! Sua pontuação final dependerá de sua eficiência."
    return result


def configurar_partida():
    """Configura a cadeia lógica (Culpado -> Local -> Item) e gera as pistas."""
    culpado_real = random.choice(SUSPEITOS)
    locais_possiveis = [local for local, acesso in LOCAL_ACESSO.items() if culpado_real in acesso]
    local_crime = random.choice(locais_possiveis)
    itens_possiveis = [item for item, local in ITEM_LOCAIS.items() if local == local_crime]
    item_crime = random.choice(itens_possiveis)
    
    pistas_dinamicas = []
    itens_falsos = [i for i in ITENS if i != item_crime]
    item_falso_pista1 = random.choice(itens_falsos)
    
    pistas_dinamicas.append(f"Pista Lógica (Item): A sabotagem exigiu o item '{item_crime}' OU o item '{item_falso_pista1}'.")
    pistas_dinamicas.append(f"Pista Lógica (Item): A investigação confirmou que o item '{item_falso_pista1}' NÃO foi usado.")
    pistas_dinamicas.append(f"Pista de Localização: Os registros de inventário mostram que o item '{item_crime}' pertence à '{local_crime}'.")

    lista_suspeitos_local = LOCAL_ACESSO[local_crime][:]
    random.shuffle(lista_suspeitos_local)
    
    if len(lista_suspeitos_local) == 2:
        texto_suspeitos = f"{lista_suspeitos_local[0]} ou {lista_suspeitos_local[1]}"
    else:
        texto_suspeitos = f"{lista_suspeitos_local[0]}, {lista_suspeitos_local[1]} ou {lista_suspeitos_local[2]}"
            
    pistas_dinamicas.append(f"Pista de Acesso: Os logs da IA mostram que apenas {texto_suspeitos} acessaram a '{local_crime}' recentemente.")

    inocentes_com_acesso = [s for s in lista_suspeitos_local if s != culpado_real]
    for inocente in inocentes_com_acesso:
        pistas_dinamicas.append(f"Pista de Álibi: {inocente} {ALIBIS_FIXOS[inocente]}")

    todos_inocentes = [s for s in SUSPEITOS if s != culpado_real]
    inocentes_sem_acesso = [s for s in todos_inocentes if s not in inocentes_com_acesso]
    
    for i in range(random.randint(1, 2)):
        if inocentes_sem_acesso:
            inocente_random = inocentes_sem_acesso.pop()
            pistas_dinamicas.append(f"Pista (Irrelevante): A investigação provou que {inocente_random} {ALIBIS_FIXOS[inocente_random]}")
    
    random.shuffle(pistas_dinamicas)
    return culpado_real, local_crime, item_crime, pistas_dinamicas

def mostrar_tempo_restante(tempo_restante_segundos, pontuacao_atual):
    minutos = int(tempo_restante_segundos // 60)
    segundos = int(tempo_restante_segundos % 60)
    result = f"[STATUS] Pontuação: {pontuacao_atual} | Tempo Restante: {minutos:02}:{segundos:02}"
    if tempo_restante_segundos <= 30:
        result += f"\n[AVISO CRÍTICO] NÍVEIS DE OXIGÊNIO CRÍTICOS! ({minutos:02}:{segundos:02})"
    return result

def consultar_pistas(pistas_da_partida):
    if not pistas_da_partida:
        return 0, 0, pistas_da_partida, "Todas as pistas disponíveis para esta partida já foram reveladas!"
    
    dica = pistas_da_partida.pop() 
    tempo_gasto = random.randint(5, 10)
    custo_pontos = tempo_gasto * 10 
    
    clue_text = f"{dica}"
    
    return tempo_gasto, custo_pontos, pistas_da_partida, clue_text

def arriscar_culpado(culpado_escolhido, culpado_real, pontuacao_final, tempo_restante):
    if culpado_escolhido == culpado_real:
        bonus_tempo = int(tempo_restante)
        pontuacao_total = pontuacao_final + bonus_tempo
        
        result = "=" * 60 + "\n"
        result += f"       SUCESSO! O CULPADO É {culpado_real}!\n"
        result += "Você usou a lógica e salvou a tripulação da ARES-7.\n"
        result += "-" * 60 + "\n"
        result += f"Pontuação Base: {pontuacao_final}\n"
        result += f"Bônus de Tempo: {bonus_tempo}\n"
        result += f"PONTUAÇÃO FINAL: {pontuacao_total}\n"
        result += "=" * 60
        
        return True, pontuacao_total, result
    else:
        result = "=" * 60 + "\n"
        result += f"       FRACASSO. {culpado_escolhido} ERA INOCENTE.\n"
        result += "Você errou. O oxigênio acaba antes que o verdadeiro sabotador possa ser detido.\n"
        result += f"O culpado real era {culpado_real}.\n"
        result += "-" * 60 + "\n"
        result += "PONTUAÇÃO FINAL: 0\n"
        result += "=" * 60
        
        return True, 0, result


def iniciar_jogo(nome_jogador): 
    PONTUACAO_INICIAL = 1000
    pontuacao_atual = PONTUACAO_INICIAL
    
    apresentar_contexto()
    apresentar_personagens()
    apresentar_regras()

    culpado_real, local_crime_real, item_crime_real, pistas_da_partida = configurar_partida()
    
    jogo_acabou = False
    pontuacao_final_da_partida = 0
    
    tempo_inicio = time.time()
    tempo_limite = tempo_inicio + TEMPO_MAX_SEGUNDOS
    
    print(f"\nBoa sorte, Detetive {nome_jogador}!")
    print(f"Iniciando investigação... O crime principal está ligado à área '{local_crime_real}' e ao item '{item_crime_real}'.")
    print(f"Restam {len(pistas_da_partida)} pistas para analisar.")

    while not jogo_acabou:
        tempo_atual = time.time()
        tempo_restante = tempo_limite - tempo_atual
        
        if tempo_restante <= 0:
            break
            
        mostrar_tempo_restante(tempo_restante, pontuacao_atual) 
        
        print("\n\n--- Ações:")
        print("1. Consultar Pistas")
        print("2. Arriscar o Culpado\n")
        
        escolha = input("Sua escolha (1 ou 2): ")
        
        if escolha == '1':
            tempo_gasto, custo_pontos, pistas_da_partida, clue_text = consultar_pistas(pistas_da_partida)
            print(f"\n[PISTA RECEBIDA] {clue_text}")
            print(f"--- {tempo_gasto}s gastos | {custo_pontos} pontos perdidos ---")
            tempo_limite -= tempo_gasto 
            pontuacao_atual -= custo_pontos
            if pontuacao_atual < 0:
                pontuacao_atual = 0
            
        elif escolha == '2':
            print("\nQuem você acredita ser o sabotador? (Selecione o número):")
            suspeitos_lista = sorted(list(SUSPEITOS)) 
            for i, p in enumerate(suspeitos_lista):
                    print(f"{i+1}. {p}")

            try:
                indice_culpado = int(input("Número do Suspeito: ")) - 1
                culpado_escolhido = suspeitos_lista[indice_culpado]
                
                tempo_restante_final = tempo_limite - time.time()
                jogo_acabou, pontuacao_final_da_partida, result_text = arriscar_culpado(culpado_escolhido, culpado_real, pontuacao_atual, tempo_restante_final)
                print(f"\n--- ACUSAÇÃO FINAL: {culpado_escolhido} ---")
                time.sleep(2)
                print(result_text)
                
            except (ValueError, IndexError):
                print("Escolha inválida. Tente novamente.")
            
        else:
            print("Opção inválida. Tente novamente.")
            
        if time.time() >= tempo_limite and not jogo_acabou:
            jogo_acabou = True
            
    if not pontuacao_final_da_partida and tempo_restante <= 0:
        print("\n" + "=" * 60)
        print("       TEMPO ESGOTADO - FRACASSO NA MISSÃO! ")
        print("O oxigênio esgotou. A tripulação perece no caos da ARES-7. ")
        print(f"O culpado era {culpado_real}.")
        print("-" * 60)
        print("PONTUAÇÃO FINAL: 0")
        print("=" * 60)
        pontuacao_final_da_partida = 0
    
    return pontuacao_final_da_partida

# --- Menu Principal e Execução ---

if __name__ == "__main__":
    
    while True:
        print("\n" + "=" * 40)
        print("   SABOTAGEM NA ARES-7: AR E SILÊNCIO")
        print("=" * 40)
        print("1. Iniciar Jogo")
        print("2. Ver Pontuações (Leaderboard)")
        print("3. Sair")
        
        escolha_menu = input("Escolha uma opção (1-3): ")
        
        if escolha_menu == '1':
            nome_jogador = input("\nDigite seu nome de Detetive: ")
            if not nome_jogador:
                nome_jogador = "Detetive Anônimo"
                
            pontuacao_final = iniciar_jogo(nome_jogador)
            
            salvar_pontuacoes(nome_jogador, pontuacao_final)
            
            input("\n\nPressione ENTER para voltar ao Menu Principal...")
            
        elif escolha_menu == '2':
            print(mostrar_pontuacoes())
            input("\n\nPressione ENTER para voltar ao Menu Principal...")
            
        elif escolha_menu == '3':
            print("\nSaindo da ARES-7... Obrigado por jogar!")
            break
            
        else:
            print("\nOpção inválida. Por favor, escolha 1, 2 ou 3.")