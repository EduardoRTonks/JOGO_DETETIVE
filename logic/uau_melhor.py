import random
import time

PERSONAGENS = {
    'Silas Stone': 'Corporativo, frio, tinha uma cópia ilegal da Chave Ômega. A corporação ganha com o seguro da estação.',
    'Engenheira Jade Jenkins': 'Prodígio técnica. Ignorada pela Comandante após avisar sobre "anomalias" de energia.',
    'Piloto Paxton Price': 'Piloto de transporte. Furiosa por sua suspensão. Estava confinado na Ponte de Comando.',
    'Cmandante Victoria Volkova': 'A Comandante. Única (com Stone) com acesso à Chave Ômega. Suspendeu a Piloto Price recentemente.',
    'Dr. Alistair Armstrong': 'Biólogo-Chefe. Arrogante. Sua pesquisa vital foi cortada por Stone.',
    'Dr. Elias Erwin': 'Médico/Psicólogo. Reportou o roubo de um sedativo forte de seus estoques na Ala Médica.',
    'Chefe Kaelen Knight': 'Chefe de Segurança. Metódico. Foi encontrado sedado perto do Compartimento de Carga.',
    'A.T.H.E.N.A.': 'a IA que gerencia a nave. ela Foi danificada e está "cega" para o ataque, mas ainda fornece outros dados (logs de portas, inventário) que servem como pistas que podem ser acessadas.'
}

SUSPEITOS = list(PERSONAGENS.keys())[:-1]

AREAS = [
    'Engenharia (Suporte de Vida)',
    'Compartimento de Carga',
    'Ala Médica (MedBay)',
    'Laboratório de Biociência',
    'Ponte de Comando',
    'Dutos de Ventilação'
]

LOCAIS = list(AREAS[:-1])

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


def apresentar_contexto():
    print("=" * 60)
    print("       SABOTAGEM NA ARES-7: AR E SILÊNCIO")
    print("=" * 60 + "\n")
    print("A ARES-7, uma estação de pesquisa em órbita de Marte, mergulha no caos.")
    print(f"O Sistema de Suporte de Vida foi sabotado. A tripulação tem {HORAS}h de oxigênio.")
    print("Para piorar, o único transmissor de longo alcance foi roubado do Compartimento de Carga, cortando toda a comunicação com a Terra.")
    print("O sabotador usou um vírus que corrompeu os logs de câmera da IA (A.R.E.S.) nos locais-chave.")
    print("\nSua única esperança é usar a lógica para conectar os fatos restantes e descobrir o culpado antes que o tempo se esgote!")
    input("\n\nPressione ENTER para conhecer os tripulantes...\n\n")

def apresentar_personagens():
    print("\n" + "=" * 60)
    print("                   TRIPULANTES")
    print("=" * 60 + "\n")
    for nome, descricao in PERSONAGENS.items():
        print(f" - {nome}: {descricao}")
    input("\n\nPressione ENTER para ver as Regras de Dedução...\n\n")

def apresentar_regras():
    print("\n" + "=" * 60)
    print("                         REGRAS")
    print("=" * 60)
    print(f"Objetivo: Descobrir o sabotador antes que o tempo ({HORAS}h traduzidas em {TEMPO_MAX_SEGUNDOS // 60} minutos) se esgote.")
    print("Consultar Pistas: Esta ação gasta tempo, mas fornece um fato chave para ajudar a encontrar o culpado.")
    print("Arriscar o Culpado: Faça sua acusação final. Acertar salva a tripulação, errar significa fracasso imediato.")
    print("\nO destino da ARES-7 está em suas mãos. Use a lógica!")
    input("\n\nPressione ENTER para INICIAR A PARTIDA...\n\n")


def configurar_partida():
    

    culpado_real = random.choice(list(SUSPEITOS))
    
    inocentes = [S for S in list(SUSPEITOS) if S != culpado_real]
    

    item_crime = random.choice(ITENS)
    local_crime = random.choice(LOCAIS)

    pistas_inocentes_fixas = {
        'Cmandante Victoria Volkova': f'não precisaria de sedativo, poderia ter prendido o Chefe Knight sem a Seringa para acessar o {local_crime}).', 
        'Piloto Paxton Price': 'estava confinado na Ponte de Comando, sem acesso aos Dutos de Ventilação necessários para o ataque.',
        'Engenheira Jade Jenkins': f'estava no Observatório, sem acesso à Ala Médica ou aos Dutos para levar o {item_crime} até o local.',
        'Chefe Kaelen Knight': f'estava sedado e não poderia ter usado os Dutos de Ventilação, deixando o {item_crime} intacto.',
        'Silas Stone': f'ficou monitorando a falha de energia, sem acesso aos Dutos de Ventilação e ao {local_crime}.',
        'Dr. Alistair Armstrong': f'não tinha motivo para ir à Ala Médica (roubar sedativo), nem acesso ao {item_crime} para cometer a sabotagem.',
        'Dr. Elias Erwin': f'não tinha acesso ao item "{item_crime}", nem ao item "{random.choice([i for i in ITENS if i != item_crime])}"'
    }
    
    pistas_dinamicas = []
    for inocente in inocentes:
        pista = f"A investigação provou que {inocente} {pistas_inocentes_fixas[inocente]}"
        pistas_dinamicas.append(pista)
        

    pistas_dinamicas.append(f"Os logs da A.R.E.S. mostram que a desativação do Suporte de Vida exigiu o item {item_crime} ou o item {random.choice([i for i in ITENS if i != item_crime])}.")
    pistas_dinamicas.append(f"Os logs da A.R.E.S. mostram que o item {random.choice([i for i in ITENS if i != item_crime])} não foi usado.")
    pistas_dinamicas.append(f"Apenas {culpado_real} ou {random.choice([i for i in inocentes])} teriam acesso ao item {item_crime}.")
    pistas_dinamicas.append(f"O culpado teria que ter acesso ao {local_crime} e aos dutos de ventilação.")
        
    return culpado_real, local_crime, pistas_dinamicas

def mostrar_tempo_restante(tempo_restante_segundos):
    """Exibe o tempo restante no formato Minutos:Segundos."""
    minutos = int(tempo_restante_segundos // 60)
    segundos = int(tempo_restante_segundos % 60)

    if tempo_restante_segundos <= 30:
        print(f"\n[AVISO CRÍTICO] TEMPO CRÍTICO: Menos de 30 segundos restantes! ({minutos:02}:{segundos:02})")
    elif tempo_restante_segundos <= 60:
        print(f"\n[AVISO] Restam {minutos} minuto(s) e {segundos} segundos.️")
    else:
        print(f"\n[LOG] Tempo Restante: {minutos} minuto(s) e {segundos} segundos.")
    time.sleep(1) 


PISTAS_DA_PARTIDA = []

def consultar_pistas():
    global PISTAS_DA_PARTIDA
    
    if not PISTAS_DA_PARTIDA:
        print("\n --- Todas as pistas disponíveis para esta partida já foram reveladas!")
        return 5
        
    dica = random.choice(PISTAS_DA_PARTIDA)
    PISTAS_DA_PARTIDA.remove(dica) 
    
    tempo = random.randint(5,10)
    print(f"\n{dica}\n--- {tempo}s gastos ---\n")
    return tempo

def arriscar_culpado(culpado_escolhido, culpado_real):
    print(f"\n--- ACUSAÇÃO FINAL: {culpado_escolhido} ---")
    time.sleep(2)

    if culpado_escolhido == culpado_real:
        print("\n" + "=" * 60)
        print(f"       SUCESSO! O CULPADO É {culpado_real}!")
        print("Você usou a lógica e salvou a tripulação da ARES-7. O sistema de suporte de vida foi reativado.")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print(f"       FRACASSO. {culpado_escolhido} ERA INOCENTE.")
        print("Você errou. O oxigênio acaba antes que o verdadeiro sabotador possa ser detido.")
        print(f"O culpado real era {culpado_real}.")
        print("=" * 60)
        return True

def iniciar_jogo():
    global PISTAS_DA_PARTIDA
    global TEMPO_MAX_SEGUNDOS 

    apresentar_contexto()
    apresentar_personagens()
    apresentar_regras()

    culpado_real, local_crime_principal, pistas_dinamicas = configurar_partida()
    PISTAS_DA_PARTIDA = pistas_dinamicas 
    jogo_acabou = False
    
    tempo_inicio = time.time()
    tempo_limite = tempo_inicio + TEMPO_MAX_SEGUNDOS
    
    print(f"\nO Compartimento de Carga e a Ala Médica foram violados. O crime principal está ligado a {local_crime_principal}.")
    print(f"Restam {len(PISTAS_DA_PARTIDA)} pistas para analisar.**")

    while not jogo_acabou:
        
        tempo_atual = time.time()
        tempo_restante = tempo_limite - tempo_atual
        
        if tempo_restante <= 0:
            break
            
        mostrar_tempo_restante(tempo_restante)
        
        print("\n\n--- Ações:")
        print("1. Consultar Pistas")
        print("2. Arriscar o Culpado\n")
        
        escolha = input("Sua escolha (1 ou 2): ")
        
        if escolha == '1':
            tempo_gasto = consultar_pistas()
            tempo_limite -= tempo_gasto 
            
        elif escolha == '2':
            print("\nQuem você acredita ser o sabotador? (Selecione o número):")
            suspeitos_lista = sorted(list(SUSPEITOS)) 
            for i, p in enumerate(suspeitos_lista):
                    print(f"{i+1}. {p}")

            try:
                indice_culpado = int(input("Número do Suspeito: ")) - 1
                culpado_escolhido = suspeitos_lista[indice_culpado]
                jogo_acabou = arriscar_culpado(culpado_escolhido, culpado_real)
            except (ValueError, IndexError):
                print("Escolha inválida. Tente novamente.")
            
        else:
            print("Opção inválida. Tente novamente.")
            

        if time.time() >= tempo_limite and not jogo_acabou:
            break

    if not jogo_acabou:
        print("\n" + "=" * 60)
        print("       TEMPO ESGOTADO - FRACASSO NA MISSÃO! ")
        print("O oxigênio esgotou. A tripulação perece no caos da ARES-7. ")
        print(f"O culpado era {culpado_real}.")
        print("=" * 60)

if __name__ == "__main__":
    iniciar_jogo()