import json
import os
from datetime import datetime

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

def ler_data(mensagem):
    """Lê uma data no formato dd/mm/yyyy"""
    while True:
        try:
            return datetime.strptime(input(mensagem), '%d/%m/%Y')
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

# ===========================
# CLIENTES
# ===========================

def listar_clientes(clientes):
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return
    for c in clientes:
        print(f"CPF: {c['CPF']}\nNome: {c['Nome']}\nNascimento: {c['DataNascimento']}")
        print(f"Sexo: {c['Sexo']} | Salário: {c['Salario']}")
        print(f"Telefones: {', '.join(c['Telefones'])}")
        print(f"Emails: {', '.join(c['Emails'])}")
        print("-"*40)

def buscar_cliente(clientes, cpf):
    return next((c for c in clientes if c['CPF'] == cpf), None)

def incluir_cliente(clientes):
    cpf = input("CPF: ")
    if buscar_cliente(clientes, cpf):
        print("Cliente com este CPF já existe!")
        return clientes
    nome = input("Nome: ")
    data_nasc = ler_data("Data de Nascimento (dd/mm/yyyy): ").strftime('%d/%m/%Y')
    sexo = input("Sexo (M/F): ")
    salario = float(input("Salário: "))
    telefones = input_lista("Telefone (Enter para parar): ")
    emails = input_lista("Email (Enter para parar): ")
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
    if data_nasc: cliente['DataNascimento'] = data_nasc
    sexo = input(f"Sexo ({cliente['Sexo']}): ")
    if sexo: cliente['Sexo'] = sexo
    salario = input(f"Salário ({cliente['Salario']}): ")
    if salario: cliente['Salario'] = float(salario)
    if input("Alterar telefones? (S/N) ").upper()=='S':
        cliente['Telefones'] = input_lista("Novo telefone (Enter para parar): ")
    if input("Alterar emails? (S/N) ").upper()=='S':
        cliente['Emails'] = input_lista("Novo email (Enter para parar): ")
    print("Cliente alterado com sucesso!")
    return clientes

def excluir_cliente(clientes):
    cpf = input("CPF do cliente: ")
    cliente = buscar_cliente(clientes, cpf)
    if not cliente:
        print("Cliente não encontrado!")
        return clientes
    if input(f"Confirma exclusão de {cliente['Nome']}? (S/N) ").upper()=='S':
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
        print(f"Código: {i['Codigo']} | Tipo: {i['Tipo']} | Valor: {i['ValorAluguel']}")
        print(f"Descrição: {i['Descricao']}\nEndereço: {i['Endereco']}, {i['Cidade']}-{i['Estado']} | CEP: {i['CEP']}")
        print("-"*40)

def buscar_imovel(imoveis, codigo):
    return next((i for i in imoveis if i['Codigo'] == codigo), None)

def incluir_imovel(imoveis):
    codigo = input("Código do imóvel: ")
    if buscar_imovel(imoveis, codigo):
        print("Imóvel com este código já existe!")
        return imoveis
    descricao = input("Descrição: ")
    endereco = input("Endereço: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    cep = input("CEP: ")
    tipo = input("Tipo (residencial/comercial): ")
    valor = float(input("Valor do aluguel: "))
    imoveis.append({
        "Codigo": codigo, "Descricao": descricao, "Endereco": endereco,
        "Cidade": cidade, "Estado": estado, "CEP": cep, "Tipo": tipo, "ValorAluguel": valor
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
    if input(f"Confirma exclusão do imóvel {codigo}? (S/N)").upper()=='S':
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
        print(f"Data Entrada: {a['DataEntrada']} | Data Saída: {a['DataSaida']} | Valor Mensal: {a['ValorMensal']}")
        print("-"*40)

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
    data_entrada = ler_data("Data de entrada (dd/mm/yyyy): ").strftime('%d/%m/%Y')
    data_saida = ler_data("Data de saída (dd/mm/yyyy): ").strftime('%d/%m/%Y')
    valor_mensal = float(input("Valor mensal: "))
    alugueis.append({
        "CPFCliente": cpf_cliente, "CodigoImovel": codigo_imovel,
        "CPFFiador": cpf_fiador, "NomeFiador": nome_fiador,
        "DataEntrada": data_entrada, "DataSaida": data_saida,
        "ValorMensal": valor_mensal
    })
    print("Aluguel incluído com sucesso!")
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

def relatorio_clientes_por_telefones(clientes):
    x = int(input("Mostrar clientes com mais de X telefones. X = "))
    filtrados = [c for c in clientes if len(c['Telefones']) > x]
    listar_clientes(filtrados)

def relatorio_imoveis_por_tipo(imoveis):
    tipo = input("Tipo do imóvel (residencial/comercial): ").lower()
    filtrados = [i for i in imoveis if i['Tipo'].lower() == tipo]
    listar_imoveis(filtrados)

def relatorio_alugueis_por_periodo(alugueis):
    data_inicio = ler_data("Data início (dd/mm/yyyy): ")
    data_fim = ler_data("Data fim (dd/mm/yyyy): ")
    for a in alugueis:
        data_ent = datetime.strptime(a['DataEntrada'], '%d/%m/%Y')
        if data_inicio <= data_ent <= data_fim:
            print(a)
            print("-"*40)

# ===========================
# MENUS
# ===========================

def menu_clientes():
    clientes = carregar_dados("clientes.json")
    while True:
        print("\n--- Clientes ---")
        print("1. Listar todos\n2. Buscar\n3. Incluir\n4. Alterar\n5. Excluir\n6. Voltar")
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
        print("1. Listar todos\n2. Buscar\n3. Incluir\n4. Alterar\n5. Excluir\n6. Voltar")
        opc = input("Opção: ")
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
        print("1. Listar todos\n2. Buscar\n3. Incluir\n4. Excluir\n5. Voltar")
        opc = input("Opção: ")
        if opc=='1': listar_alugueis(alugueis)
        elif opc=='2':
            cpf=input("CPF do cliente: ")
            codigo=input("Código do imóvel: ")
            print(buscar_aluguel(alugueis, cpf, codigo) or "Não encontrado")
        elif opc=='3': alugueis = incluir_aluguel(alugueis, clientes, imoveis)
        elif opc=='4': alugueis = excluir_aluguel(alugueis)
        elif opc=='5': salvar_dados("alugueis.json", alugueis); break

def menu_relatorios():
    clientes = carregar_dados("clientes.json")
    imoveis = carregar_dados("imoveis.json")
    alugueis = carregar_dados("alugueis.json")
    while True:
        print("\n--- Relatórios ---")
        print("1. Clientes com mais de X telefones")
        print("2. Imóveis por tipo")
        print("3. Aluguéis entre datas")
        print("4. Voltar")
        opc = input("Opção: ")
        if opc=='1': relatorio_clientes_por_telefones(clientes)
        elif opc=='2': relatorio_imoveis_por_tipo(imoveis)
        elif opc=='3': relatorio_alugueis_por_periodo(alugueis)
        elif opc=='4': break

def main():
    while True:
        print("\n=== Sistema Imobiliária ===")
        print("1. Clientes\n2. Imóveis\n3. Aluguéis\n4. Relatórios\n5. Sair")
        opc = input("Opção: ")
        if opc=='1': menu_clientes()
        elif opc=='2': menu_imoveis()
        elif opc=='3': menu_alugueis()
        elif opc=='4': menu_relatorios()
        elif opc=='5': break
        else: print("Opção inválida!")

if __name__ == "__main__":
    main()
