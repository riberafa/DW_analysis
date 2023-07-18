import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("================================")
print("Trabalho Final")
print("================================\n")

# Função para carregar os dados de todos os arquivos .csv em uma pasta e subpastas
def carregar_dados_pasta(pasta, tabela):
    dados = []
    for root, dirs, files in os.walk(pasta):
        for file in files:
            if file.endswith('.csv'):
                arquivo = os.path.join(root, file)
                dados.append(pd.read_csv(arquivo))
    return pd.concat(dados, ignore_index=True)

# Pasta raiz contendo os dados
pasta_raiz = 'Dados_DW'

# Carregar dados do Cadastro Único
bpc_pasta = os.path.join(pasta_raiz, 'Dados', 'Por_Beneficiario')
bpc_data = carregar_dados_pasta(bpc_pasta, 'bpc')

# Carregar dados do Bolsa Família
bolsa_familia_pasta = os.path.join(pasta_raiz, 'Dados', 'Por_Beneficiario', 'Bolsa_Familia')
bolsa_familia_data = carregar_dados_pasta(bolsa_familia_pasta, 'bolsa_familia')

# Carregar dados do Auxílio Brasil
auxilio_brasil_pasta = os.path.join(pasta_raiz, 'Dados', 'Por_Beneficiario', 'Auxilio_Brasil')
auxilio_brasil_data = carregar_dados_pasta(auxilio_brasil_pasta, 'Auxilio_Brasil')

# Carregar dados do Auxílio Emergencial
auxilio_emergencial_pasta = os.path.join(pasta_raiz, 'Dados', 'Por_Beneficiario', 'Auxilio_Emergencial')
auxilio_emergencial_data = carregar_dados_pasta(auxilio_emergencial_pasta, 'Auxilio_Emergencial')

# Criação da base de dados com NIS do responsável, número de pessoas da família e renda da família
base_dados = bpc_data[['NIS Beneficiário', 'Quantidade Dependentes', 'Valor']]
base_dados.columns = ['NIS Responsável', 'Número de Pessoas', 'Renda Familiar']
base_dados = base_dados.replace({0.0: np.nan})  # Substituir 0.0 por Null
base_dados.to_csv('base_dados.csv', index=False)    # Salvar a base de dados em um novo arquivo .csv

option = ''
while option != '0':
    print("\n--------------------------------")
    print("\nGráficos")
    print("1 - Interferência em Beneficiários: Transição Bolsa Família para Auxílio Brasil")
    print("2 - Pessoas que recebem Bolsa Família e BPC")
    print("3 - Número de beneficiários de cada programa")
    print("4 - Número de Pessoas que Aderiram a cada Benefício nos Últimos 5 Anos")
    option = input("Selecione uma opção (1, 2, 3, 4) ou digite '0' para sair: ")
    
    if option == "1":
        # Interferência em Famílias do Bolsa Família
        beneficiarios_bf = bolsa_familia_data['NIS Beneficiário'].unique()
        beneficiarios_ab = auxilio_brasil_data['NIS Beneficiário'].unique()
        beneficiarios_perdidos = set(beneficiarios_bf) - set(beneficiarios_ab)
        interferencia = len(beneficiarios_perdidos) / len(beneficiarios_bf)

        beneficiarios_sofreram_interferencia = len(beneficiarios_perdidos)
        beneficiarios_sem_interferencia = len(beneficiarios_bf) - beneficiarios_sofreram_interferencia

        labels = ["Sofreram interferência", "Sem interferência"]
        sizes = [beneficiarios_sofreram_interferencia, beneficiarios_sem_interferencia]
        colors = ["lightcoral", "lightskyblue"]

        print(f"1) A mudança do programa pode ter causado interferência em {interferencia * 100:.2f}% dos beneficiários cadastrados no Bolsa Família.")

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.title("Interferência em Beneficiários do Bolsa Família", fontsize=16)
        plt.axis('equal')
        plt.show()
    
    elif option == "2":
        # Pessoas que recebem Bolsa Família e BPC
        bpc_pasta = os.path.join(pasta_raiz, 'Dados', 'Por_Beneficiario', 'bpc')
        bpc_data = carregar_dados_pasta(bpc_pasta, 'bpc')
        pessoas_bf_bpc = set(bolsa_familia_data['NIS Beneficiário']).intersection(set(bpc_data['NIS Beneficiário']))
        people_bf = len(bolsa_familia_data)
        people_bpc = len(bpc_data)
        people_both = len(pessoas_bf_bpc)

        print(f"3 Existem {len(pessoas_bf_bpc)} pessoas que recebem tanto o Bolsa Família quanto o Benefício de Prestação Continuada.")

        labels = ["Bolsa Família", "BPC", "Ambos"]
        sizes = [people_bf, people_bpc, people_both]
        colors = ['blue', 'orange', 'green']
        explode = (0.1, 0.1, 0.1)

        total_people = sum(sizes)
        percentages = [100 * (size / total_people) for size in sizes]
        people_counts = [f"{label}: {size} ({percentage:.1f}%)" for label, size, percentage in zip(labels, sizes, percentages)]

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=people_counts, colors=colors, explode=explode, autopct='%1.1f%%', shadow=True)
        plt.title("Beneficiários: Bolsa Família vs. BPC", fontsize=16)
        plt.axis('equal')
        plt.show()

    elif option == "3":
        # Contar o número de beneficiários de cada programa
        num_bolsa_familia = len(bolsa_familia_data['NIS Beneficiário'])
        num_auxilio_brasil = len(auxilio_brasil_data['NIS Beneficiário'])
        num_auxilio_emergencial = len(auxilio_emergencial_data['NIS Beneficiário'])
        num_bpc = len(bpc_data['NIS Beneficiário'])

        # Plotar gráfico de barras empilhadas
        programs = ['Bolsa Família', 'Auxílio Brasil', 'Auxílio Emergencial', 'BPC']
        num_beneficiarios = [num_bolsa_familia, num_auxilio_brasil, num_auxilio_emergencial, num_bpc]
        colors = ['lightcoral', 'lightskyblue', 'lightgreen', 'mediumturquoise']

        plt.figure(figsize=(8, 6))
        plt.bar(programs, num_beneficiarios, color=colors)
        plt.xlabel('Programa')
        plt.ylabel('Número de Beneficiários')
        plt.title('Comparação do Número de Beneficiários por Programa')
        plt.show()
    
    elif option == '4':

        # Lista dos benefícios para análise
        beneficios = ['Auxilio_Brasil', 'Auxilio_Emergencial', 'Bolsa_Familia', 'bpc']

        # Dicionário para armazenar o número de pessoas por ano de cada benefício
        dados_beneficios = {}

        # Iterar sobre os benefícios
        for beneficio in beneficios:
            dados_beneficio = []
            pasta_beneficio = os.path.join(pasta_raiz, 'Dados', 'Por_Beneficiario', beneficio)
            
            # Iterar sobre os anos dos últimos 5 anos
            for ano in range(2019, 2024):
                pasta_ano = os.path.join(pasta_beneficio, str(ano))
                if os.path.exists(pasta_ano):
                    dados_ano = carregar_dados_pasta(pasta_ano, beneficio)
                    numero_pessoas = len(dados_ano)
                    dados_beneficio.append(numero_pessoas)
                else:
                    dados_beneficio.append(None)
            
            dados_beneficios[beneficio] = dados_beneficio

        # Plotar o gráfico
        anos = range(2019, 2024)
        cores = ['blue', 'orange', 'green', 'red']
        labels = ['Auxilio Brasil', 'Auxilio Emergencial', 'Bolsa Família', 'BPC']

        plt.figure(figsize=(10, 6))
        for i, beneficio in enumerate(beneficios):
            valores = dados_beneficios[beneficio]
            if all(valor is None for valor in valores):
                # Se todos os valores forem None, exibir o nome do benefício na legenda com a informação "sem dados"
                plt.plot([], [], color=cores[i], label=labels[i] + ' (sem dados)')
            else:
                # Caso contrário, plotar os dados normalmente
                plt.plot(anos, valores, marker='o', color=cores[i], label=labels[i])

        plt.xticks(anos)  # Definir os ticks do eixo x como os anos
        plt.xlabel('Ano')
        plt.ylabel('Número de Pessoas')
        plt.title('Número de Pessoas que Aderiram a Cada Benefício nos Últimos 5 Anos')
        plt.legend()
        plt.show()
    
    elif option == '0':
        print("Encerrando...")
    
    else:
        print("Opção inválida. Tente novamente.\n")

