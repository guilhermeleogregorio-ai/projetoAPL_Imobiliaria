import json
import os
import re
from datetime import datetime


# ===========================
# CONFIGURAÇÃO
# ===========================
PASTA_RELATORIOS = "relatorios"
os.makedirs(PASTA_RELATORIOS, exist_ok=True)

# ===========================
# FUNÇÕES AUXILIARES
# ===========================

def carregar_dados(nome_arquivo):
    """Carrega os dados de um arquivo JSON, retorna lista vazia se não existir"""
    if not os.path.exists(nome_arquivo):
        return []
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_dados(nome_arquivo, dados):
    """Salva lista de dicionários em um arquivo JSON"""
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def salvar_relatorio_json(nome_arquivo, dados):
    """Salva relatório em JSON na pasta 'relatorios/'"""
    caminho = os.path.join(PASTA_RELATORIOS, nome_arquivo)
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f"Relatório salvo: {caminho}")


def ler_data(mensagem):
    """Lê uma data no formato dd/mm/yyyy"""
    while True:
        try:
            data = input(mensagem).strip()
            datetime.strptime(data, '%d/%m/%Y')
            return data
        except ValueError:
            print("Data inválida! Use dd/mm/yyyy.") 

def input_lista(mensagem):
    """Lê múltiplos valores até que o usuário aperte Enter sem digitar"""
    lista = []
    while True:
        valor = input(mensagem)
        if valor == '':
            break
        lista.append(valor)
    return lista


def validar_cpf():

    """
    Pede ao usuário um CPF e valida:
    - se tem 11 dígitos;
    - se não é uma sequência repetida (ex: 11111111111);
    - se os dígitos verificadores (10º e 11º) estão corretos.
    Retorna o CPF limpo (somente números).
    """


    # Função interna que remove qualquer coisa que não seja número (pontos, traços, espaços etc.)
    def limpar_cpf(cpf: str) -> str:
        return re.sub(r'[^0-9]', '', cpf)  # substitui tudo que não for número por vazio
    
    def calcular_digito(cpf_parcial: str) -> str:
         """
        Recebe os primeiros 9 ou 10 dígitos e retorna o próximo dígito verificador.
        Fórmula oficial do CPF:
          soma = (1º dígito * peso 10 ou 11) + (2º dígito * peso 9 ou 10) + ...
          resto = soma % 11
          dígito = 0 se resto < 2, senão 11 - resto
        """
         soma = 0
         peso = len(cpf_parcial) + 1 # começa em 10 para o 1º DV, ou 11 para o 2º
         for digito in cpf_parcial: 
             soma+= int(digito) * peso  # multiplica cada dígito pelo peso correspondente
             peso-= 1 # diminui o peso a cada iteração
         resto = soma % 11 # pega o resto da divisão por 11
        # Se o resto for menor que 2, o dígito é 0; senão, é 11 - resto
         return '0' if resto < 2 else str(11 - resto) 
    
    # Loop principal: continua até que o CPF seja válido
    while True:
        #solicita entrada de usuario
        cpf = input("CPF (somente números ou com . e -): ").strip()
        cpf = limpar_cpf(cpf)

        if len(cpf) != 11:
            print(" O CPF deve ter exatamente 11 dígitos.")
            continue

        if cpf == cpf[0] * 11:
            print(" CPF inválido (todos os dígitos iguais).")
            continue

        primeiro_dv = calcular_digito(cpf[:9])
        segundo_dv = calcular_digito(cpf[:9] + primeiro_dv)

        if cpf[-2:] == primeiro_dv + segundo_dv:
            return cpf  # CPF válido
        else:
            print(" CPF inválido! Digite novamente.")






# ===========================
# CLIENTES
# ===========================

def listar_clientes(clientes):
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return
    for c in clientes:
        print(f"CPF: {c['CPF']}\nNome: {c['Nome']}\nNascimento: {c['DataNascimento']}")
        print(f"Sexo: {c['Sexo']} | Salário: R${c['Salario']:.2f}")
        print(f"Telefones: {', '.join(c['Telefones']) if c['Telefones'] else 'Nenhum'}")
        print(f"Emails: {', '.join(c['Emails']) if c['Emails'] else 'Nenhum'}")
        print("-" * 50)

def buscar_cliente(clientes, cpf):
    return next((c for c in clientes if c['CPF'] == cpf), None)

def incluir_cliente(clientes):
    cpf = validar_cpf()
    if buscar_cliente(clientes, cpf):
        print("Cliente com este CPF já existe!")
        return clientes
    nome = input("Nome: ")
    data_nasc = ler_data("Data de Nascimento (dd/mm/yyyy): ")
    sexo = input("Sexo (M/F): ").upper()
    salario = float(input("Salário: "))
    telefones = input_lista("Digite os telefones:")
    emails = input_lista("Digite os e-mails:")
    clientes.append({
        "CPF": cpf, "Nome": nome, "DataNascimento": data_nasc,
        "Sexo": sexo, "Salario": salario, "Telefones": telefones, "Emails": emails
    })
    print("Cliente incluído com sucesso!")
    return clientes

def alterar_cliente(clientes):
    cpf = input("CPF do cliente: ")
    cliente = buscar_cliente(clientes, cpf)
    if not cliente:
        print("Cliente não encontrado!")
        return clientes
    print("Deixe em branco para não alterar.")
    nome = input(f"Nome ({cliente['Nome']}): ")
    if nome: cliente['Nome'] = nome
    data_nasc = input(f"Data Nascimento ({cliente['DataNascimento']}): ")
    if data_nasc: cliente['DataNascimento'] = ler_data("Nova data: ")
    sexo = input(f"Sexo ({cliente['Sexo']}): ")
    if sexo: cliente['Sexo'] = sexo.upper()
    salario = input(f"Salário ({cliente['Salario']}): ")
    if salario: cliente['Salario'] = float(salario)
    if input("Alterar telefones? (S/N) ").upper() == 'S':
        cliente['Telefones'] = input_lista("Novos telefones:")
    if input("Alterar emails? (S/N) ").upper() == 'S':
        cliente['Emails'] = input_lista("Novos e-mails:")
    print("Cliente alterado com sucesso!")
    return clientes

def excluir_cliente(clientes):
    cpf = input("CPF do cliente: ")
    cliente = buscar_cliente(clientes, cpf)
    if not cliente:
        print("Cliente não encontrado!")
        return clientes
    if input(f"Confirma exclusão de {cliente['Nome']}? (S/N) ").upper() == 'S':
        clientes.remove(cliente)
        print("Cliente excluído!")
    return clientes


# ===========================
# IMÓVEIS
# ===========================


def listar_imoveis(imoveis):
    if not imoveis:
        print("Nenhum imóvel cadastrado.")
        return
    for i in imoveis:
        print(f"Código: {i['Codigo']} | Tipo: {i['Tipo']} | R${i['ValorAluguel']:.2f}")
        print(f"Descrição: {i['Descricao']}")
        print(f"Endereço: {i['Endereco']}, {i['Cidade']}-{i['Estado']} | CEP: {i['CEP']}")
        print("-" * 50)

def buscar_imovel(imoveis, codigo):
    return next((i for i in imoveis if i['Codigo'] == codigo), None)

def incluir_imovel(imoveis):
    codigo = input("Código do imóvel: ").strip()
    if buscar_imovel(imoveis, codigo):
        print("Imóvel com este código já existe!")
        return imoveis
    descricao = input("Descrição: ")
    endereco = input("Endereço: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    cep = input("CEP: ")
    tipo = input("Tipo (residencial/comercial): ").strip().lower()
    valor = float(input("Valor do aluguel: "))
    imoveis.append({
        "Codigo": codigo, "Descricao": descricao, "Endereco": endereco,
        "Cidade": cidade, "Estado": estado, "CEP": cep, "Tipo": tipo.capitalize(),
        "ValorAluguel": valor
    })
    print("Imóvel incluído com sucesso!")
    return imoveis

def alterar_imovel(imoveis):
    codigo = input("Código do imóvel: ")
    imovel = buscar_imovel(imoveis, codigo)
    if not imovel:
        print("Imóvel não encontrado!")
        return imoveis
    print("Deixe em branco para não alterar.")
    for campo in ["Descricao","Endereco","Cidade","Estado","CEP","Tipo"]:
        valor = input(f"{campo} ({imovel[campo]}): ")
        if valor: imovel[campo] = valor
    valor_aluguel = input(f"Valor Aluguel ({imovel['ValorAluguel']}): ")
    if valor_aluguel: imovel['ValorAluguel'] = float(valor_aluguel)
    print("Imóvel alterado!")
    return imoveis

def excluir_imovel(imoveis):
    codigo = input("Código do imóvel: ")
    imovel = buscar_imovel(imoveis, codigo)
    if not imovel:
        print("Imóvel não encontrado!")
        return imoveis
    if input(f"Confirma exclusão do imóvel {codigo}? (S/N)").upper() == 'S':
        imoveis.remove(imovel)
        print("Imóvel excluído!")
    return imoveis

# ===========================
# ALUGUÉIS
# ===========================

def listar_alugueis(alugueis):
    if not alugueis:
        print("Nenhum aluguel cadastrado.")
        return
    for a in alugueis:
        print(f"Cliente CPF: {a['CPFCliente']} | Imóvel Código: {a['CodigoImovel']}")
        print(f"Fiador: {a['CPFFiador']} - {a['NomeFiador']}")
        print(f"Data Entrada: {a['DataEntrada']} | Data Saída: {a['DataSaida']} | Valor Mensal: {a['ValorMensal']:.2f}")
        print("-"*50)

def buscar_aluguel(alugueis, cpf_cliente, codigo_imovel):
    return next((a for a in alugueis if a['CPFCliente']==cpf_cliente and a['CodigoImovel']==codigo_imovel), None)

def incluir_aluguel(alugueis, clientes, imoveis):
    cpf_cliente = input("CPF do cliente: ")
    if not buscar_cliente(clientes, cpf_cliente):
        print("Cliente não cadastrado!")
        return alugueis
    codigo_imovel = input("Código do imóvel: ")
    if not buscar_imovel(imoveis, codigo_imovel):
        print("Imóvel não cadastrado!")
        return alugueis
    if buscar_aluguel(alugueis, cpf_cliente, codigo_imovel):
        print("Aluguel já cadastrado para este cliente e imóvel!")
        return alugueis
    cpf_fiador = input("CPF do fiador: ")
    nome_fiador = input("Nome do fiador: ")
    data_entrada = ler_data("Data de entrada (dd/mm/yyyy): ")
    data_saida = ler_data("Data de saída (dd/mm/yyyy): ")
    valor_mensal = float(input("Valor mensal: "))
    alugueis.append({
        "CPFCliente": cpf_cliente, "CodigoImovel": codigo_imovel,
        "CPFFiador": cpf_fiador, "NomeFiador": nome_fiador,
        "DataEntrada": data_entrada, "DataSaida": data_saida,
        "ValorMensal": valor_mensal
    })
    print("Aluguel incluído com sucesso!")
    return alugueis


def alterar_aluguel(alugueis):
    cpf_cliente = input("CPF do cliente: ")
    codigo_imovel = input("Código do imóvel: ")
    aluguel = buscar_aluguel(alugueis, cpf_cliente, codigo_imovel)
    if not aluguel:
        print("Aluguel não encontrado!")
        return alugueis
    print("Deixe em branco para não alterar.")
    cpf_fiador = input(f"CPF do fiador ({aluguel['CPFFiador']}): ")
    if cpf_fiador: aluguel['CPFFiador'] = cpf_fiador
    nome_fiador = input(f"Nome do fiador ({aluguel['NomeFiador']}): ")
    if nome_fiador: aluguel['NomeFiador'] = nome_fiador
    data_entrada = input(f"Data de entrada ({aluguel['DataEntrada']}): ")
    if data_entrada: aluguel['DataEntrada'] = ler_data("Nova data de entrada: ")
    data_saida = input(f"Data de saída ({aluguel['DataSaida']}): ")
    if data_saida: aluguel['DataSaida'] = ler_data("Nova data de saída: ")
    valor_mensal = input(f"Valor mensal ({aluguel['ValorMensal']}): ")
    if valor_mensal: aluguel['ValorMensal'] = float(valor_mensal)
    print("Aluguel alterado!")
    return alugueis


def excluir_aluguel(alugueis):
    cpf_cliente = input("CPF do cliente: ")
    codigo_imovel = input("Código do imóvel: ")
    aluguel = buscar_aluguel(alugueis, cpf_cliente, codigo_imovel)
    if not aluguel:
        print("Aluguel não encontrado!")
        return alugueis
    if input("Confirma exclusão do aluguel? (S/N)").upper()=='S':
        alugueis.remove(aluguel)
        print("Aluguel excluído!")
    return alugueis

# ===========================
# RELATÓRIOS
# ===========================


def rel_a_clientes_mais_telefones(clientes):
    while True:
        try:
            x = int(input("Mostrar clientes com mais de quantos telefones? "))
            break
        except ValueError:
            print("Digite um número válido.")
    
    filtrados = [c for c in clientes if len(c['Telefones']) > x]
    if not filtrados:
        print(f"Nenhum cliente com mais de {x} telefone(s).")
        return
    
    relatorio = {
        "tipo": "clientes_mais_telefones",
        "parametro_x": x,
        "gerado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "total": len(filtrados),
        "clientes": filtrados
    }
    
    nome_arq = f"rel_clientes_mais_{x}_telefones.json"
    salvar_relatorio_json(nome_arq, relatorio)
    
    print(f"\n--- {len(filtrados)} cliente(s) com mais de {x} telefone(s) ---")
    listar_clientes(filtrados)


def rel_b_imoveis_por_tipo(imoveis):
    tipo = input("Tipo do imóvel (residencial/comercial): ").strip().lower()
    filtrados = [i for i in imoveis if i['Tipo'].lower() == tipo]
    if not filtrados:
        print(f"Nenhum imóvel {tipo} encontrado.")
        return
    
    relatorio = {
        "tipo": "imoveis_por_tipo",
        "parametro_tipo": tipo,
        "gerado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "total": len(filtrados),
        "imoveis": filtrados
    }
    
    nome_arq = f"rel_imoveis_{tipo}.json"
    salvar_relatorio_json(nome_arq, relatorio)
    
    print(f"\n--- {len(filtrados)} imóvel(is) do tipo '{tipo}' ---")
    listar_imoveis(filtrados)

def rel_c_alugueis_por_periodo(alugueis, clientes, imoveis):
    data_inicio = ler_data("Data início (dd/mm/yyyy): ")
    data_fim = ler_data("Data fim (dd/mm/yyyy): ")
    
    dt_inicio = datetime.strptime(data_inicio, "%d/%m/%Y")
    dt_fim = datetime.strptime(data_fim, "%d/%m/%Y")
    
    resultados = []
    for a in alugueis:
        dt_entrada = datetime.strptime(a['DataEntrada'], "%d/%m/%Y")
        if dt_inicio <= dt_entrada <= dt_fim:
            cliente = buscar_cliente(clientes, a['CPFCliente'])
            imovel = buscar_imovel(imoveis, a['CodigoImovel'])
            if cliente and imovel:
                resultados.append({
                    "cpf_cliente": a['CPFCliente'],
                    "nome_cliente": cliente['Nome'],
                    "codigo_imovel": a['CodigoImovel'],
                    "descricao_imovel": imovel['Descricao'],
                    "endereco_completo": f"{imovel['Endereco']}, {imovel['Cidade']}-{imovel['Estado']} CEP {imovel['CEP']}",
                    "tipo_imovel": imovel['Tipo'],
                    "valor_aluguel_imovel": imovel['ValorAluguel'],
                    "data_entrada": a['DataEntrada'],
                    "data_saida": a['DataSaida'],
                    "valor_mensal": a['ValorMensal'],
                    "fiador": {"cpf": a['CPFFiador'], "nome": a['NomeFiador']}
                })
    
    if not resultados:
        print("Nenhum aluguel encontrado no período.")
        return
    relatorio = {
        "tipo": "alugueis_por_periodo",
        "periodo": {"inicio": data_inicio, "fim": data_fim},
        "gerado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "total": len(resultados),
        "alugueis": resultados
    }
    
    nome_arq = f"rel_alugueis_{data_inicio.replace('/', '')}_a_{data_fim.replace('/', '')}.json"
    salvar_relatorio_json(nome_arq, relatorio)
    
    print(f"\n--- {len(resultados)} aluguel(is) entre {data_inicio} e {data_fim} ---")
    for r in resultados:
        print(f"{r['nome_cliente']} → Imóvel {r['codigo_imovel']} | Entrada: {r['data_entrada']}")


# ===========================
# MENUS
# ===========================

def menu_clientes():
    clientes = carregar_dados("clientes.json")
    while True:
        print("\n--- Clientes ---")
        print("1. Listar todos\n2. Buscar\n3. Incluir\n4. Alterar\n5. Excluir\n6. Voltar/Salvar")
        opc = input("Opção: ")
        if opc=='1': listar_clientes(clientes)
        elif opc=='2': cpf=input("CPF: "); print(buscar_cliente(clientes, cpf) or "Não encontrado")
        elif opc=='3': clientes = incluir_cliente(clientes)
        elif opc=='4': clientes = alterar_cliente(clientes)
        elif opc=='5': clientes = excluir_cliente(clientes)
        elif opc=='6': salvar_dados("clientes.json", clientes); break

def menu_imoveis():
    imoveis = carregar_dados("imoveis.json")
    while True:
        print("\n--- Imóveis ---")
        print("1. Listar todos\n2. Buscar\n3. Incluir\n4. Alterar\n5. Excluir\n6. Voltar/Salvar")
        opc = input("Opção: ").strip()
        if opc=='1': listar_imoveis(imoveis)
        elif opc=='2': codigo=input("Código: "); print(buscar_imovel(imoveis, codigo) or "Não encontrado")
        elif opc=='3': imoveis = incluir_imovel(imoveis)
        elif opc=='4': imoveis = alterar_imovel(imoveis)
        elif opc=='5': imoveis = excluir_imovel(imoveis)
        elif opc=='6': salvar_dados("imoveis.json", imoveis); break

def menu_alugueis():
    alugueis = carregar_dados("alugueis.json")
    clientes = carregar_dados("clientes.json")
    imoveis = carregar_dados("imoveis.json")
    while True:
        print("\n--- Aluguéis ---")
        print("1. Listar todos\n2. Buscar\n3. Incluir\n4. Alterar\n5. Excluir \n6. Voltar/Salvar")
        opc = input("Opção: ").strip()

        if opc == '1': listar_alugueis(alugueis)
        elif opc == '2':
            cpf = input("CPF do cliente: ")
            codigo = input("Código do imóvel: ")
            a = buscar_aluguel(alugueis, cpf, codigo)
            print(a if a else "Não encontrado")
        elif opc == '3': alugueis = incluir_aluguel(alugueis, clientes, imoveis)
        elif opc == '4': alugueis = alterar_aluguel(alugueis)
        elif opc == '5': alugueis = excluir_aluguel(alugueis)
        elif opc == '6':
            salvar_dados("alugueis.json", alugueis)
            break

def menu_relatorios():
    clientes = carregar_dados("clientes.json")
    imoveis = carregar_dados("imoveis.json")
    alugueis = carregar_dados("alugueis.json")
    
    while True:
        print("\n" + "="*50)
        print("       SUBMENU RELATÓRIOS")
        print("="*50)
        print("1. Clientes com mais de X telefones")
        print("2. Imóveis por tipo")
        print("3. Aluguéis entre datas")
        print("4. Voltar")
        print("-"*50)
        opc = input("Escolha uma opção: ").strip()
        
        if opc == '1':
            rel_a_clientes_mais_telefones(clientes)
        elif opc == '2':
            rel_b_imoveis_por_tipo(imoveis)
        elif opc == '3':
            rel_c_alugueis_por_periodo(alugueis, clientes, imoveis)
        elif opc == '4': break
        else:
            print("Opção inválida!")

def main():
    while True:
        print("\n=== Sistema Imobiliária ===")
        print("1. Clientes\n2. Imóveis\n3. Aluguéis\n4. Relatórios\n5. Sair")
        opc = input("Opção: ")
        if opc=='1': menu_clientes()
        elif opc=='2': menu_imoveis()
        elif opc=='3': menu_alugueis()
        elif opc=='4': menu_relatorios()
        elif opc=='5': print("Saindo..."); break
        else: print("Opção inválida!")

if __name__ == "__main__":
    main()
