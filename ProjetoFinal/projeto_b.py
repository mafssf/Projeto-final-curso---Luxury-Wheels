from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3
#from sqlalchemy import Values
import datetime
from openpyxl import Workbook

# Ligação à base de dados — disponível para todas as classes
db = sqlite3.connect("database/luxury_wheels.db")
cursor = db.cursor()

def formatar_data(var):
    valor = var.get() # vai buscar o valor

    digitos = [c for c in valor if c.isdigit()] # percorre cada caracter e filtra apenas os dígitos
    digitos = "".join(digitos)  # junta os dígitos numa única string

    # Adiciona o / após 2 e 4 digitos inseridos
    if len(digitos) <= 2:
        data = digitos
    elif len(digitos) == 3:
        data = digitos[:2] + "/"+ digitos [2]
    elif len(digitos) >= 4:
        data = digitos[:2] + "/" + digitos[2:4] + "/" + digitos[4:]

    var.set(data) # atualiza o campo com a data formatada

    if len(digitos) ==8: # Só valida depois da data estar completa
        try:
            datetime.datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            messagebox.showwarning("Erro", "Data inválida! Verifique se o dia e o mês estão corretos.")
    elif 0 < len(digitos) < 8:
        messagebox.showwarning("Erro", "Data incompleta! Verifique se escreveu o dia, mês e ano na totalidade.")


def formatar_data_entry(entry):
    valor = entry.get()  # vai buscar o valor

    digitos = [c for c in valor if c.isdigit()]  # percorre cada caracter e filtra apenas os dígitos
    digitos = "".join(digitos)  # junta os dígitos numa única string

    # Adiciona o / após 2 e 4 digitos inseridos
    if len(digitos) <= 2:
        data = digitos
    elif len(digitos) == 3:
        data = digitos[:2] + "/" + digitos[2]
    elif len(digitos) >= 4:
        data = digitos[:2] + "/" + digitos[2:4] + "/" + digitos[4:]

    entry.delete(0, END) # apaga todo o conteúdo do campo, da posição 0 até ao fim
    entry.insert(0, data) # insere a data formatada na posição 0

    if len(digitos) == 8:  # Só valida depois da data estar completa
        try:
            datetime.datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            messagebox.showwarning("Erro", "Data inválida! Verifique se o dia e o mês estão corretos.")
    elif 0 < len(digitos) < 8:
        messagebox.showwarning("Erro", "Data incompleta! Verifique se escreveu o dia, mês e ano na totalidade.")


class JanelaLogin:
    def __init__(self, root):
        self.janela = root # Guarda a referência da janela para usar nos restantes métodos
        self.janela.title("Luxury Wheels") # Titulo da janela login
        self.janela.resizable(False, False) # fixamos o tamanho da jánela
        self.janela.wm_iconbitmap('recursos/car.ico') # icon de carro


        # Criação de frame de login
        frame = LabelFrame(self.janela, text="Login")
        frame.place(relx=0.5, rely=0.5, anchor="center") # centra o frame e fixar


        # Lable utilizador
        self.etiqueta_utilizador = Label(frame, text="Utilizador: ") # Cria o lable
        self.etiqueta_utilizador.grid(column=0, row=1) # posiciona o lable
        self.utilizador = Entry(frame) # Input de texto
        self.utilizador.grid(column=1, row=1)
        self.utilizador.focus() # direciona o rato para o 1ro campo a preencher

        # Lable Password
        self.etiqueta_password = Label(frame, text="Password: ")
        self.etiqueta_password.grid(column=0, row=2)
        self.password = Entry(frame, show='*') # Mostrar password como **
        self.password.grid(column=1, row=2)
        self.mostrar_password = IntVar() # Variável que guarda se a checkbox está marcada (1) ou não (0)
        self.check_password = ttk.Checkbutton(frame, text="Mostrar password", variable=self.mostrar_password, command=self.toggle_password) # Checkbox para mostrar/esconder password
        self.check_password.grid(column=1, row=3, sticky=W)

        # Botão Entrar
        self.botao_entrar = ttk.Button(frame, text="Entrar", command=self.verificar_login)
        self.botao_entrar.grid(column=1, row=4, sticky= W)
        self.janela.bind("<Return>", lambda event: self.verificar_login()) # permite o utilizador entrar com tecla enter

        # centrar janela de login
        largura_janela = 400
        altura_janela = 300

        largura_ecra = self.janela.winfo_screenwidth()  # largura do ecrã
        altura_ecra = self.janela.winfo_screenheight()  # altura do ecrã

        x = (largura_ecra // 2) - (largura_janela // 2)
        y = (altura_ecra // 2) - (altura_janela // 2)

        self.janela.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

        self.janela.deiconify()  # Mostra a janela já configurada

    def toggle_password(self):
        # Função que mostra ou esconde a password consoante o estado da checkbox
        if self.mostrar_password.get():
            self.password.config(show='') # mostra a password em texto normal
        else:
            self.password.config(show='*') # esconde a password com asteriscos


    def verificar_login(self):
        username = self.utilizador.get()
        password = self.password.get()
        cursor.execute("SELECT * FROM utilizadores WHERE username = ? AND password = ?",(username, password))
        resultado = cursor.fetchone()

        # janela informativa resultado de login
        if resultado:
            self.janela.unbind("<Return>") # desliga o bind de enter do login para não voltar a disparar depois de autenticado
            messagebox.showinfo("Sucesso", "Login efetuado com sucesso!") # janela popup acesso concedido
            self.janela.withdraw()  # fecha a janela de login
            nova_janela = Toplevel(self.janela)  # cria nova janela
            nova_janela.withdraw()  # Esconde até estar configurada
            app = JanelaPrincipal(nova_janela, resultado[0])  # abre janela principal e guarda o utilizador que fez o acesso
            nova_janela.protocol("WM_DELETE_WINDOW", self.janela.destroy) # Fecha o programa ao fechar a janela principal

        else:
            messagebox.showerror("Erro", "Username ou password incorrectos!") # janela de acesso negado

class JanelaPrincipal:
    def __init__(self, root, id_utilizador):
        self.janela = root # Guarda a referência da janela para usar nos restantes métodos
        self.id_utilizador = id_utilizador
        self.janela.title('Luxury Wheels')
        self.janela.resizable(False, False)
        self.janela.wm_iconbitmap('recursos/car.ico')


        # alerta de revisão de veículo a expirar
        self.alerta_revisao()

        # centrar janela principal
        largura_janela = 900
        altura_janela = 600

        largura_ecra = self.janela.winfo_screenwidth()  # largura do ecrã
        altura_ecra = self.janela.winfo_screenheight()  # altura do ecrã

        x = (largura_ecra // 2) - (largura_janela // 2)
        y = (altura_ecra // 2) - (altura_janela // 2)

        self.janela.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

        # Limpa conteudo aberto (impede janelas sobrepostas)
        self.frame_conteudo_atual = None #

        # Frame lateral com menu
        frame_lateral = LabelFrame(self.janela, text="Menu Principal", width=200)
        frame_lateral.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        self.janela.columnconfigure(0, weight=0)  # coluna do menu — tamanho fixo
        self.janela.columnconfigure(1, weight=1)  # coluna do conteúdo — expande
        self.janela.rowconfigure(0, weight=1)  # linha principal — expande na vertical

        # botões laterais com opção do menu como labels clicáveis
        frame_lateral_dashboard = Label(frame_lateral, text="📊 Dashboard", cursor="hand2")
        frame_lateral_dashboard.grid(row=0, column=0, pady=5, padx=10, sticky="w")
        frame_lateral_dashboard.bind("<Button-1>", lambda e: self.abrir_dashboard())
        frame_lateral_veiculos = Label(frame_lateral, text="🚗 Veículos", cursor="hand2")
        frame_lateral_veiculos.grid(row=1, column=0, pady=5, padx=10, sticky="w")
        frame_lateral_veiculos.bind("<Button-1>", lambda e: self.abrir_veiculos())
        frame_lateral_clientes = Label(frame_lateral, text="👤 Clientes", cursor="hand2")
        frame_lateral_clientes.grid(row=2, column=0, pady=5, padx=10, sticky="w")
        frame_lateral_clientes.bind("<Button-1>", lambda e: self.abrir_clientes())
        frame_lateral_reservas = Label(frame_lateral, text="📅 Reservas", cursor="hand2")
        frame_lateral_reservas.grid(row=3, column=0, pady=5, padx=10, sticky="w")
        frame_lateral_reservas.bind("<Button-1>", lambda e: self.abrir_reservas())
        frame_lateral_utilizadores = Label(frame_lateral, text="💳  Formas de Pagamento", cursor="hand2")
        frame_lateral_utilizadores.grid(row=4, column=0, pady=5, padx=10, sticky="w")
        frame_lateral_utilizadores.bind("<Button-1>", lambda e: self.abrir_formas_pagamento())

        self.janela.deiconify()  # Mostra a janela já configurada

    def alerta_revisao(self):
        # Vai buscar a matrícula e data da próxima revisão de todos os veículos
        cursor.execute("SELECT matricula, data_proxima_revisao FROM veiculos")
        resultado = cursor.fetchall()

        veiculos_para_revisao = [] # Lista para guardar matrículas com revisão a expirar

        for revisao in resultado:
            # Calcula a diferença entre a data de revisão e hoje
            self.data_inspecao = datetime.datetime.strptime(revisao [1], "%d/%m/%Y").date() - datetime.date.today()

            # Se a revisão expirar em 5 dias ou menos, adiciona à lista
            if self.data_inspecao.days <= 5:
                veiculos_para_revisao.append(revisao[0])

        # Mostra popup de aviso se existirem veículos com revisão a expirar
        if veiculos_para_revisao:
                messagebox.showwarning("Aviso", "Veículos com revisão a expirar em 5 dias:\n" + "\n".join(veiculos_para_revisao))

    def abrir_dashboard(self):
        # Fecha janela (se já aberta)
        if self.frame_conteudo_atual != None:
            self.frame_conteudo_atual.destroy()

        # Criar frame para o conteúdo
        frame_conteudo = LabelFrame(self.janela, text="Indicadores de Gestão")
        frame_conteudo.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame_conteudo_atual = frame_conteudo

        # Distribuir o espaço disponível igualmente pelas colunas e linhas
        frame_conteudo.columnconfigure(0, weight=1)
        frame_conteudo.columnconfigure(1, weight=1)
        frame_conteudo.rowconfigure(0, weight=1)
        frame_conteudo.rowconfigure(1, weight=1)
        frame_conteudo.rowconfigure(2, weight=1)

        # Labels para painel visual com informações resumidas
        frame_alugados = LabelFrame(frame_conteudo, text="Veículos Alugados")
        frame_alugados.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        frame_clientes = LabelFrame(frame_conteudo, text="Últimos Clientes")
        frame_clientes.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        frame_disponiveis = LabelFrame(frame_conteudo, text="Veículos Disponíveis")
        frame_disponiveis.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        frame_reservas_mes = LabelFrame(frame_conteudo, text="Reservas do Mês")
        frame_reservas_mes.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        frame_alertas = LabelFrame(frame_conteudo, text="Alertas de Veículos")
        frame_alertas.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")


        # Vai buscar matrícula, datas e nome do cliente de todas as reservas
        cursor.execute("""SELECT matricula, data_inicio, data_fim, clientes.nome FROM reservas 
        JOIN clientes ON reservas.id_clientes = clientes.id""")
        todas_reservas = cursor.fetchall()

        hoje = datetime.datetime.now() # Guarda a data de hoje
        reservas_ativas = []  # Lista para guardar as reservas que estão ativas hoje

        # Procura as datas e converte de string para data
        for reserva in todas_reservas:
            data_inicio = datetime.datetime.strptime(reserva[1], "%d/%m/%Y")
            data_fim = datetime.datetime.strptime(reserva[2], "%d/%m/%Y")
            if data_inicio <= hoje <= data_fim:  # Verifica se a reserva está ativa hoje
                reservas_ativas.append(reserva)

        # procura as datas das reservas ativas e converte de string para data
        for i, reserva in enumerate(reservas_ativas):
            data_fim = datetime.datetime.strptime(reserva[2], "%d/%m/%Y")
            dias_restantes = (data_fim.date() - hoje.date()).days # Efetua o calculo
            Label(frame_alugados, text=f"{reserva[0]} - {reserva[3]} - {dias_restantes} dias restantes").grid( row=i, column=0, padx=10, pady=10) # Informa quantos dias falta pelo calculo inserido

        # Na lista de clientes vai buscar por ordem de id os últimos 5 clientes criados
        cursor.execute("SELECT nome FROM clientes ORDER BY id DESC LIMIT 5 ")
        ultimos_clientes = cursor.fetchall()

        # procura os últimos clientes
        for i, cliente in enumerate (ultimos_clientes):
            nome = cliente[0]
            label_nome = Label(frame_clientes, text=nome) # mostra o nome do cliente criado
            label_nome.grid(row=i, column=0, padx=10, pady=10)

        # vai buscar os veiculos que não se encontram em manutenção agrupando por categoria e tipo de veiculo
        cursor.execute("SELECT tipo_veiculo, categoria, COUNT(*) FROM veiculos WHERE em_manutencao = 'Não' GROUP BY tipo_veiculo, categoria")
        veiculos_disponiveis = cursor.fetchall()

        # Procura os veiculos
        for i, veiculo in enumerate(veiculos_disponiveis):
            label_veiculo = Label(frame_disponiveis, text= f"{veiculo[0]} - {veiculo[1]}:{veiculo[2]} disponíveis") # mostra os veiculos disponiveis por categoria e tipo de veiculo
            label_veiculo.grid(row=i, column=0, padx=10, pady=10)

        # Vai buscar as datas de reserva na lista das reservas
        cursor.execute("SELECT data_inicio, data_fim, valor_total FROM reservas ")
        reservas_mes = cursor.fetchall()

        hoje = datetime.datetime.now() # Variavel com a data de hoje
        reservas_totais = []

        # Procura as datas e converte de string para data na lista de reservas
        for reserva in reservas_mes:
            data_inicio = datetime.datetime.strptime(reserva[0], "%d/%m/%Y")
            if data_inicio.month == hoje.month and data_inicio.year == hoje.year:
                reservas_totais.append(reserva)

        total = sum(reserva[2] for reserva in reservas_totais) # Somo o valor total de todas as reservas do mês em reservas[2]
        Label(frame_reservas_mes, text=f"Reservas este mês: {len(reservas_totais)}").grid(row=0, column=0, padx=10, pady=10) # Mostra quantas reservas houve nesse mês
        Label(frame_reservas_mes, text=f"Total: {total} €").grid(row=1, column=0, padx=10, pady=10) # Mostra o total faturado nesse mês

        # Vai buscar as datas de controlo dos veiculos na lista de veiculos
        cursor.execute("SELECT matricula, data_proxima_revisao, data_seguro, data_inspecao FROM veiculos ")
        alerta_revisao = cursor.fetchall()

        # Contador de linhas para os alertas, evita sobreposição de Labels
        row_alerta = 0
        # Procura as datas e converte de string para data
        for i, alerta in enumerate (alerta_revisao):
            data_proxima_revisao= datetime.datetime.strptime(alerta[1], "%d/%m/%Y")
            data_seguro = datetime.datetime.strptime(alerta[2], "%d/%m/%Y")
            data_inspecao = datetime.datetime.strptime(alerta[3], "%d/%m/%Y")

            dias_revisao = (data_proxima_revisao.date() - hoje.date()).days # Variável que calcula os dias até à proxima revisão
            if 0<= dias_revisao <= 15: # condição para datas inferiores a 15 dias
                Label(frame_alertas, text=f"{alerta[0]} - Revisão expira em {dias_revisao} dias").grid(row=row_alerta % 4, column=row_alerta // 4, padx=10, pady=10) # Mostra quanto tempo falta para a revisão
                row_alerta += 1  # Incrementa a linha para o próximo alerta

            dias_seguro = (data_seguro.date() - hoje.date()).days # Variável que calcula os dias até renovar o seguro
            if 0 <= dias_seguro <= 15: # condição para datas inferiores a 15 dias
                Label(frame_alertas, text=f"{alerta[0]} - Seguro expira em {dias_seguro} dias").grid(row=row_alerta % 4, column= row_alerta // 4, padx=10, pady=10) # Mostra quanto tempo falta para o seguro
                row_alerta += 1  # Incrementa a linha para o próximo alerta

            dias_inspecao = (data_inspecao.date() - hoje.date()).days # Variável que calcula os dias até à inspeção
            if 0 <= dias_inspecao <= 15: # condição para datas inferiores a 15 dias
                Label(frame_alertas, text=f"{alerta[0]} - Inspeção expira em {dias_inspecao} dias").grid(row=row_alerta % 4 , column= row_alerta // 4, padx=10, pady=10) # Mostra quanto tempo falta para a inspeção
                row_alerta += 1  # Incrementa a linha para o próximo alerta


    def abrir_veiculos(self):
        # Fecha janela (se já aberta)
        if self.frame_conteudo_atual != None:
            self.frame_conteudo_atual.destroy()

        # Criar frame para o conteúdo
        frame_conteudo = LabelFrame(self.janela, text="Lista de Veículos")
        frame_conteudo.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame_conteudo_atual = frame_conteudo

        # Criar tabela
        tabela = ttk.Treeview(frame_conteudo)
        self.tabela = tabela
        tabela.grid(row=0, column=0)
        frame_detalhe = LabelFrame(frame_conteudo, text="Detalhes do Veículo")
        frame_detalhe.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.entries = []
        for i, campo in enumerate(["tipo_veiculo", "combustivel", "num_lugares", "cor", "imagem",
                      "data_seguro", "data_inspecao", "data_ultima_revisao", "data_proxima_revisao"]):
            label = Label(frame_detalhe, text=campo.replace("_", " ").title()) # legendas com maiusculas e espaços
            label.grid(row=i // 5 * 2, column=i % 5, sticky="nsew") # linha: divisão inteira i = 0 0//5 linha 0, coluna: resto da divisão i = 0 0%5 coluna 0 (temos 5 colunas e duas linhas)
            entry = Entry(frame_detalhe, state="readonly") # entrada de conteudo apenas para visualização
            entry.grid(row=i // 5 * 2 + 1, column=i % 5, padx=5, pady=5)
            self.entries.append(entry)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(frame_conteudo, orient="vertical", command=tabela.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        tabela.configure(yscrollcommand=scrollbar.set)

        # Definir colunas
        tabela["columns"] = ("matricula", "marca", "modelo", "categoria", "valor_diaria", "em_manutencao" )
        tabela.column("#0", width=0, stretch=NO)  # esconde coluna padrão
        tabela.column("matricula", width=100)
        tabela.column("marca", width=100)
        tabela.column("modelo", width=100)
        tabela.column("categoria", width=100)
        tabela.column("valor_diaria", width=100)
        tabela.column("em_manutencao", width=100)

        # Cabeçalhos
        tabela.heading("matricula", text="Matrícula")
        tabela.heading("marca", text="Marca")
        tabela.heading("modelo", text="Modelo")
        tabela.heading("categoria", text="Categoria")
        tabela.heading("valor_diaria", text="Valor diária")
        tabela.heading("em_manutencao", text="Em Manutenção")

        # Ocupação do frame
        self.janela.columnconfigure(1, weight=1)
        self.janela.rowconfigure(0, weight=1)
        frame_conteudo.columnconfigure(0, weight=1)
        frame_conteudo.rowconfigure(0, weight=1)
        tabela.grid(row=0, column=0, sticky="nsew")

        # carregar dados
        self.carregar_veiculos()

        # Verificar mais informação ao clicar numa linha
        tabela.bind("<<TreeviewSelect>>", lambda event: self.mostrar_detalhes_veiculo())

        # Botões adicionar, editar e eliminar veiculo
        # Frame de botões adicionar, editar, eliminar
        frame_botoes = Frame(frame_conteudo)
        frame_botoes.grid(row=3, column=0, sticky="nsew")

        #Botão adicionar
        self.botao_adicionar = ttk.Button(frame_botoes, text="Adicionar", command=self.adicionar_veiculo)
        self.botao_adicionar.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        # Botão eliminar
        self.botao_eliminar = ttk.Button(frame_botoes, text="Eliminar", command=self.eliminar_veiculo)
        self.botao_eliminar.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        # Botão editar
        self.botao_editar = ttk.Button(frame_botoes, text="Editar", command=self.editar_veiculo)
        self.botao_editar.grid(row=0, column=2, sticky="n", padx=10, pady=10)

        # Botão em manutenção
        self.botao_manutencao = ttk.Button(frame_botoes, text="Manutenção", command=self.marcar_manutencao)
        self.botao_manutencao.grid(row=0, column=3, sticky="n", padx=10, pady=10)

        # Botão reservar
        self.botao_reservar = ttk.Button(frame_botoes, text="Reservar Veiculo", command=self.reservar_veiculo)
        self.botao_reservar.grid(row=0, column=4, sticky="n", padx=10, pady=10)

        # Botão exportar
        self.botao_exportar = ttk.Button(frame_botoes, text="Exportar Excel", command=self.exportar_veiculos)
        self.botao_exportar.grid(row=0, column=5, sticky="n", padx=10, pady=10)

    def carregar_veiculos(self):
        # Apaga os dados, evita dados duplicados
        self.tabela.delete(*self.tabela.get_children())

        # Carregar dados
        cursor.execute("SELECT matricula, marca, modelo, categoria, valor_diaria, em_manutencao, data_proxima_revisao FROM veiculos")
        veiculos = cursor.fetchall()

        # Inserir dados na tabela
        for veiculo in veiculos:
            # Calcula a diferença entre a data de revisão e hoje
            self.data_revisao = datetime.datetime.strptime(veiculo [6], "%d/%m/%Y").date() - datetime.date.today()

            if(self.data_revisao.days <=5): # Verifica qual ou quais os veiculos que têm data de proxima revisão inferior a 5 dias
                self.tabela.insert("", END, values=veiculo, tags=("revisao_urgente",))
            elif veiculo[5] == "Sim": # verifica qual o veículo que está em manutenção
                self.tabela.insert("", END, values=veiculo, tags=("em_manutencao",))
            else:
                self.tabela.insert("", END, values=veiculo)

        self.tabela.tag_configure("revisao_urgente", background="red") # Define a cor de fundo para vermelho quando a revisão é urgente
        self.tabela.tag_configure("em_manutencao", background="orange") # Define a cor de fundo para laranja quando está em manutenção

    def mostrar_detalhes_veiculo(self):
        valores = self.tabela.focus()  # devolve o id da linha
        dados = self.tabela.item(valores, "values") # usa o id para obter os dados
        if not dados: # Sai da função se não houver linha selecionada
            return

        # Carregar detalhes de veiculos
        cursor.execute("""SELECT tipo_veiculo, combustivel, num_lugares, cor, imagem, data_seguro, 
        data_inspecao, data_ultima_revisao, data_proxima_revisao FROM veiculos WHERE matricula = ?""", (dados[0],)) # Usa a matrícula (id) para carregar os dados do veículo selecionado
        veiculos = cursor.fetchall()
        if not veiculos:
            return

        # Visualizar detalhes
        for entry, dado in zip(self.entries, veiculos[0]):
            entry.config(state="normal")
            entry.delete(0, END)
            entry.insert(0, str(dado) if dado is not None else "") # Torna o Null em string, permite leitura de dados
            entry.config(state="readonly")

    def adicionar_veiculo(self):
        self.janela_form = Toplevel(self.janela)
        self.janela_form.grab_set() # bloqueia a janela principal enquanto o formulário está aberto, impede abrir formulários repetidos
        self.janela_form.title("Adicionar Veículo")
        self.janela_form.resizable(False, False)
        self.a_guardar = False  # inicia a flag para permitir guardar

        # Centrar janela toplevel
        largura_janela = 350
        altura_janela = 500

        largura_ecra = self.janela_form.winfo_screenwidth()  # largura do ecrã
        altura_ecra = self.janela_form.winfo_screenheight()  # altura do ecrã

        x = (largura_ecra // 2) - (largura_janela // 2)
        y = (altura_ecra // 2) - (altura_janela // 2)

        self.janela_form.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

        # Limpa conteudo aberto (impede janelas sobrepostas)
        self.frame_conteudo_atual = None

        # Estrutura da janela Toplevel
        frame_form = Frame(self.janela_form)
        frame_form.grid(row=0, column=0, sticky="nsew")
        self.entries_form = [] # Lista para guardar os campos do formulário

        # Lista de dados
        campos_preencher = [("matricula", "entry"), ("marca", "entry"), ("modelo", "entry"), ("tipo_veiculo", "combobox"),
                            ("categoria", "combobox"), ("combustivel", "combobox"), ("num_lugares", "entry"),
                            ("cor", "entry"), ("valor_diaria", "entry"), ("imagem", "entry"), ("data_seguro", "entry"),
                            ("data_inspecao", "entry"), ("data_ultima_revisao", "entry"), ("data_proxima_revisao", "entry"),
                            ("em_manutencao", "combobox")]

        # Dicionário de dados fixos
        opcoes = {
            "tipo_veiculo": ["Mota", "Ligeiro de passageiros", "SUV", "Comercial", "Pesado de passageiros"],
            "categoria": ["Económico", "Familiar", "Premium", "Ecológico", "Desportivo", "Monovolume"],
            "combustivel": ["Gasolina", "Disel", "Elétrico", "Híbrido"],
            "em_manutencao": ["Sim", "Não"]
            }

        # Loop para criar campos do formulário
        for i, (nome,tipo) in enumerate(campos_preencher):
            lable_veiculos = Label(frame_form, text=nome, anchor="w")
            lable_veiculos.grid(row=i, column=0, padx=5, pady=5)

            # criar Entry
            if tipo == "entry":
                entry_veiculos = Entry(frame_form, width=20)
            # criar Combobox
            elif tipo == "combobox":
                entry_veiculos = ttk.Combobox(frame_form, values=opcoes[nome], state="readonly", width=17)

            if nome.startswith("data"):
                entry_veiculos.bind("<FocusOut>", lambda e, en=entry_veiculos: formatar_data_entry(en))  # Obriga o utilizador a manter o mesmo formato de datas
                entry_veiculos.bind("<Return>", lambda e, en=entry_veiculos: formatar_data_entry(en))  # formata a data ao pressionar Enter


            entry_veiculos.grid(row=i, column=1, padx=5, pady=5)
            self.entries_form.append(entry_veiculos) # Adiciona o campo à lista para posterior leitura dos valore

        # coloca o foco no primeiro campo do formulário, para o utilizador poder escrever de imediato
        self.entries_form[0].focus()

        # Botão guardar
        self.botao_guardar = ttk.Button(frame_form, text="Guardar", command=self.guardar_veiculo)
        self.botao_guardar.grid(row=16, columnspan=2, padx=5, pady=5)

        # Enter aciona o botão guardar
        self.janela_form.bind("<Return>", lambda e: self.guardar_veiculo())

    def guardar_veiculo(self):
        #Impede erro quando carregamos mais vezes no enter por engano
        if self.a_guardar:
            return
        self.a_guardar = True

        valores = [entry.get() for entry in self.entries_form] # Ler valores dos campos do formulário

        # Verificação de entrada de valores
        for i, valor in enumerate(valores):
            if i != 9 and valores[i] == "":
                messagebox.showinfo("Erro", "Todos os campos devem ser preenchidos") # janela popup com mensagem de erro
                self.a_guardar = False  # reinicia a flag para que o utilizador acabe o preenchimento dos dados
                return

        cursor.execute("""INSERT INTO veiculos (matricula, marca, modelo, tipo_veiculo, categoria, combustivel, num_lugares,
        cor, valor_diaria, imagem, data_seguro, data_inspecao, data_ultima_revisao, data_proxima_revisao,
        em_manutencao) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", valores) #insere os valores novos na tabela sql na sequência certa
        db.commit() # guardar alterações na base de dados
        self.carregar_veiculos()
        messagebox.showinfo("Sucesso", "Veiculo guardo com sucesso!") #janela popup com mensagem de guardado
        self.janela_form.destroy() # fecha a janela após dados guardados

    def eliminar_veiculo(self):
        valores = self.tabela.focus()  # devolve o id da linha
        if not valores:
            messagebox.showinfo("Erro", "Selecione um Veículo para eliminar")
            return
        dados = self.tabela.item(valores, "values") # usa o id para obter os dados

        cursor.execute("SELECT COUNT(*) FROM reservas WHERE matricula = ?", (dados[0],))
        reservas = cursor.fetchone()[0]

        # Impede eliminar um veículo com registos associados em reservas
        if reservas > 0:
            messagebox.showerror("Erro","Este Veículo tem reservas associadas e não pode ser eliminado")
            return

        # Confirmar para eliminar
        confirmacao = messagebox.askyesno(message= "Tens a certeza?", icon="question", title="Eliminar")
        if confirmacao:
            cursor.execute("DELETE FROM veiculos WHERE matricula = ?", (dados[0],)) # Consulta SQL e elimina
            db.commit() # Confirma e guarda
            self.carregar_veiculos()  # Atualizar a tabela de veiculos
            messagebox.showinfo("Sucesso", f"Veiculo {dados[0]} eliminado!") # Dá a confirmação ao utilizador

    def editar_veiculo(self):
        valores = self.tabela.focus()  # devolve o id da linha
        if not valores:
            messagebox.showinfo("Erro", "Selecione um Veículo para editar")
            return
        dados = self.tabela.item(valores, "values") # usa o id para obter os dados
        self.editar_matricula = dados[0]  # guarda a matricula


        self.janela_form = Toplevel(self.janela)
        self.janela_form.grab_set() # bloqueia a janela principal enquanto o formulário está aberto, impede abrir formulários repetidos
        self.janela_form.title("Editar Veículo")
        self.janela_form.resizable(False, False)
        self.a_guardar = False  # inicia a flag para permitir guardar

        # Centrar janela toplevel
        largura_janela = 350
        altura_janela = 500

        largura_ecra = self.janela_form.winfo_screenwidth()  # largura do ecrã
        altura_ecra = self.janela_form.winfo_screenheight()  # altura do ecrã

        x = (largura_ecra // 2) - (largura_janela // 2)
        y = (altura_ecra // 2) - (altura_janela // 2)

        self.janela_form.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

        # Limpa conteudo aberto (impede janelas sobrepostas)
        self.frame_conteudo_atual = None

        # Estrutura da janela Toplevel
        frame_form = Frame(self.janela_form)
        frame_form.grid(row=0, column=0, sticky="nsew")
        self.entries_form = []

        # Lista de dados
        campos_preencher = [("matricula", "entry"), ("marca", "entry"), ("modelo", "entry"), ("tipo_veiculo", "combobox"),
                            ("categoria", "combobox"), ("combustivel", "combobox"), ("num_lugares", "entry"),
                            ("cor", "entry"), ("valor_diaria", "entry"), ("imagem", "entry"), ("data_seguro", "entry"),
                            ("data_inspecao", "entry"), ("data_ultima_revisao", "entry"), ("data_proxima_revisao", "entry"),
                            ("em_manutencao", "combobox")]

        # Dicionário de dados fixos
        opcoes = {
            "tipo_veiculo": ["Mota", "Ligeiro de passageiros", "SUV", "Comercial", "Pesado de passageiros"],
            "categoria": ["Económico", "Familiar", "Premium", "Ecológico"],
            "combustivel": ["Gasolina", "Disel", "Elétrico", "Híbrido"],
            "em_manutencao": ["Sim", "Não"]
            }

        #Loop de carregar dados
        cursor.execute("""SELECT matricula, marca, modelo, tipo_veiculo, categoria, combustivel, num_lugares,
        cor, valor_diaria, imagem, data_seguro, data_inspecao, data_ultima_revisao, data_proxima_revisao,
        em_manutencao FROM veiculos WHERE matricula = ?""", (dados[0],))
        editar_dados = cursor.fetchall()

        # Loop para visualizar os campos do veiculo
        for i, (nome,tipo) in enumerate(campos_preencher):
            label_veiculos = Label(frame_form, text=nome, anchor="w")
            label_veiculos.grid(row=i, column=0, padx=5, pady=5)

            # criar Entry
            if tipo == "entry":
                entry_veiculos = Entry(frame_form, width=20)
                entry_veiculos.insert(0, str(editar_dados[0][i]))

            # criar Combobox
            elif tipo == "combobox":
                entry_veiculos = ttk.Combobox(frame_form, values=opcoes[nome], state="readonly", width=17)
                entry_veiculos.set(editar_dados[0][i])

            if nome.startswith("data"):
                entry_veiculos.bind("<FocusOut>", lambda e, en=entry_veiculos: formatar_data_entry(en))  # Obriga o utilizador a manter o mesmo formato de datas
                entry_veiculos.bind("<Return>", lambda e, en=entry_veiculos: formatar_data_entry(en))  # formata a data ao pressionar Enter

            entry_veiculos.grid(row=i, column=1, padx=5, pady=5)
            self.entries_form.append(entry_veiculos) # Adiciona o campo à lista para posterior leitura dos valore

        # coloca o foco no primeiro campo do formulário, para o utilizador poder escrever de imediato
        self.entries_form[0].focus()

        # Botão guardar alterações
        self.botao_guardar = ttk.Button(frame_form, text="Guardar", command=self.atualizar_veiculo)
        self.botao_guardar.grid(row=16, columnspan=2, padx=5, pady=5)

        # Enter aciona o botão guardar
        self.janela_form.bind("<Return>", lambda e: self.atualizar_veiculo())

    def atualizar_veiculo(self):
        #Impede erro quando carregamos mais vezes no enter por engano
        if self.a_guardar:
            return
        self.a_guardar = True

        valores = [entry.get() for entry in self.entries_form] # Ler valores dos campos do formulário

        cursor.execute("""UPDATE veiculos SET matricula = ?, marca = ?, modelo = ?, tipo_veiculo = ?, categoria = ?, combustivel = ?, num_lugares = ?,
        cor = ?, valor_diaria = ?, imagem = ?, data_seguro = ?, data_inspecao = ?, data_ultima_revisao = ?, data_proxima_revisao = ?,
        em_manutencao = ? WHERE matricula = ?""", valores + [self.editar_matricula])
        db.commit()  # guardar alterações na base de dados
        self.carregar_veiculos()
        messagebox.showinfo("Sucesso", "Veiculo alterado com sucesso!")  # janela popup com mensagem de guardado
        self.janela_form.destroy()  # fecha a janela após dados guardados

    def marcar_manutencao(self):
        valores = self.tabela.focus()  # devolve o id da linha
        if not valores:
            messagebox.showinfo("Erro", "Selecione o Veículo em Manutenção")
            return
        dados = self.tabela.item(valores, "values")  # usa o id para obter os dados

        # Consulta SQL as reservas associadas a este veículo, para verificar se alguma ainda está ativa ou é futura
        cursor.execute("SELECT data_inicio, data_fim FROM reservas WHERE matricula = ?", (dados[0],))
        ver_manutencao = cursor.fetchall()

        # data de hoje, para comparar com a data de fim de cada reserva
        hoje = datetime.datetime.now().date()

        # Impede marcar o veículo em manutenção se tiver alguma reserva a decorrer ou agendada para o futuro
        for manutencao in ver_manutencao:
            fim = datetime.datetime.strptime(manutencao[1], "%d/%m/%Y").date()
            if fim >= hoje:
                messagebox.showerror("Erro", "Este veiculo ainda tem datas de reserva válidas!")
                return

        # Confirmar para colocar em Manutenção
        confirmacao = messagebox.askyesno(
            message="Tens a certeza?",
            icon="question", title="Manutenção")
        if confirmacao:
            cursor.execute("UPDATE veiculos SET em_manutencao = ? WHERE matricula = ?", ("Sim",dados[0],))  # Consulta SQL e coloca em Manutenção
            db.commit()  # Confirma e guarda
            self.carregar_veiculos()  # Atualizar a tabela de veiculos
            messagebox.showinfo("Sucesso", f"Veiculo {dados[0]} em Manutenção!")  # Dá a confirmação ao utilizador

    def reservar_veiculo(self):
        valores = self.tabela.focus()  # devolve o id da linha
        if not valores:
            messagebox.showinfo("Erro", "Selecione um Veículo para reservar")
            return
        dados = self.tabela.item(valores, "values") # usa o id para obter os dados
        if dados[5] == "Sim":
            messagebox.showinfo("Erro", "Veiculo em Manutenção, Selecione outro veiculo")
            return
        self.editar_matricula = dados[0]  # guarda a matricula


        self.janela_form = Toplevel(self.janela)
        self.janela_form.grab_set() # bloqueia a janela principal enquanto o formulário está aberto, impede abrir formulários repetidos
        self.janela_form.title("Reservar Veículo")
        self.janela_form.resizable(False, False)
        self.a_guardar = False  # inicia a flag para permitir guardar

        # Centrar janela toplevel
        largura_janela = 350
        altura_janela = 500

        largura_ecra = self.janela_form.winfo_screenwidth()  # largura do ecrã
        altura_ecra = self.janela_form.winfo_screenheight()  # altura do ecrã

        x = (largura_ecra // 2) - (largura_janela // 2)
        y = (altura_ecra // 2) - (altura_janela // 2)

        self.janela_form.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

        # Limpa conteudo aberto (impede janelas sobrepostas)
        self.frame_conteudo_atual = None

        # Estrutura da janela Toplevel
        frame_form = Frame(self.janela_form)
        frame_form.grid(row=0, column=0, sticky="nsew")

        self.entries_form = []
        self.vars_form = []

        # Lista de dados
        campos_preencher = [("data_inicio", "entry"), ("data_fim", "entry"), ("valor_total", "entry"), ("cliente", "combobox"),
                            ("formas_pagamento", "combobox")]

        cursor.execute("SELECT nome FROM clientes" ) # Consulta SQL o nome do cliente a partir do id do cliente
        lista_clientes = cursor.fetchall()

        cursor.execute("SELECT tipo_pagamento FROM formas_pagamento") # Consulta SQL inicial (sem filtro) só para popular a combobox ao abrir o formulário; a lista é depois filtrada por cliente em atualizar_formas_pagamento()
        lista_pagamentos = cursor.fetchall()

        # Loop para visualizar os campos da reserva
        for i, (nome,tipo) in enumerate(campos_preencher):
            label_reservar = Label(frame_form, text=nome, anchor="w")
            label_reservar.grid(row=i, column=0, padx=5, pady=5)

            # criar Entry
            if tipo == "entry":

                # Cria uma StringVar para os campos de data e detetar as alterações
                if i == 0 or i == 1:
                    var = StringVar()
                    entry_nova_reserva = Entry(frame_form, textvariable=var)
                    self.vars_form.append(var)
                    var.trace("w", lambda *args: self.calcular_valor_nova_reserva())  # Deteta alterações nas datas e chama o calcular valor nova reserva
                    entry_nova_reserva.bind("<FocusOut>", lambda e, v=var: formatar_data(v)) # Obriga o utilizador a manter o mesmo formato de datas
                    entry_nova_reserva.bind("<Return>", lambda e, v=var: formatar_data(v)) # formata a data ao pressionar Enter
                elif i == 2:
                    entry_nova_reserva = Entry(frame_form, width=20)
                    entry_nova_reserva.config(state="readonly")  # valor_total deve ser um parametro de leitura

            # criar Combobox
            elif tipo == "combobox":
                if nome == "cliente":
                    entry_nova_reserva = ttk.Combobox(frame_form, values=[cliente[0] for cliente in lista_clientes], state="readonly", width=17)
                    self.combo_cliente = entry_nova_reserva # guarda referência à combobox do cliente para usar depois
                    entry_nova_reserva.bind("<<ComboboxSelected>>", lambda e: self.formas_pagamento_cliente()) # ao escolher cliente, atualiza as formas de pagamento

                elif nome == "formas_pagamento":
                    entry_nova_reserva = ttk.Combobox(frame_form, values=[formas_pagamento[0] for formas_pagamento in lista_pagamentos], state="readonly", width=17)
                    self.combo_formas_pagamento = entry_nova_reserva # guarda referência à combobox de formas de pagamento para atualizar depois

            entry_nova_reserva.grid(row=i, column=1, padx=5, pady=5)
            self.entries_form.append(entry_nova_reserva) # Adiciona o campo à lista para posterior leitura dos valore

        # coloca o foco no primeiro campo do formulário, para o utilizador poder escrever de imediato
        self.entries_form[0].focus()

        # Botão guardar alterações
        self.botao_guardar = ttk.Button(frame_form, text="Guardar", command=self.guardar_nova_reserva)
        self.botao_guardar.grid(row=6, columnspan=2, padx=5, pady=5)

        # Enter aciona o botão guardar
        self.janela_form.bind("<Return>", lambda e: self.guardar_nova_reserva())

    def formas_pagamento_cliente(self):
        # Atualiza a combobox de formas de pagamento consoante o cliente selecionado
        nome_cliente = self.combo_cliente.get() # nome do cliente selecionado na combobox

        # Consulta SQL o id do cliente a partir do nome selecionado
        cursor.execute("SELECT id, nome FROM clientes WHERE nome = ?", (nome_cliente,))
        lista_clientes = cursor.fetchone() # só existe um id por cliente

        # Consulta SQL as formas de pagamento associadas a esse cliente
        cursor.execute("SELECT tipo_pagamento FROM formas_pagamento WHERE id_cliente = ?", (lista_clientes[0],))
        lista_pagamentos = cursor.fetchall() # um cliente pode ter várias formas de pagamento

        # Converte a lista de tuplos numa lista simples de strings
        values=[mais_formas_pagamento[0] for mais_formas_pagamento in lista_pagamentos]

        self.combo_formas_pagamento["values"] = values # atualiza as opções visíveis na combobox

    def calcular_valor_nova_reserva(self):
        nova_data_inicio = self.vars_form[0].get()
        nova_data_fim = self.vars_form[1].get()

        # Loop de carregar dados
        cursor.execute("SELECT valor_diaria FROM veiculos WHERE matricula = ?", (self.editar_matricula, ))
        reservas = cursor.fetchall()

        # Calcula a diferença entre a nova data de início e fim
        try:
            self.novo_valor_reserva= datetime.datetime.strptime(nova_data_fim, "%d/%m/%Y").date() - datetime.datetime.strptime(nova_data_inicio, "%d/%m/%Y").date()
            self.novo_valor_total = self.novo_valor_reserva.days * reservas[0][0]

            # Visualizar valores
            self.entries_form[2].config(state="normal")
            self.entries_form[2].delete(0, END)
            self.entries_form[2].insert(0, str(self.novo_valor_total))
            self.entries_form[2].config(state="readonly")

            return self.novo_valor_total # Retorna o calculo efetuado

        except ValueError:
            return

    def guardar_nova_reserva(self):
        #Impede erro quando carregamos mais vezes no enter por engano
        if self.a_guardar:
            return
        self.a_guardar = True

        valores = [entry.get() for entry in self.entries_form] # Ler valores dos campos do formulário

        # Verificação de entrada de valores
        for i, valor in enumerate(valores):
            if valores[i] == "":
                messagebox.showinfo("Erro", "Todos os campos devem ser preenchidos") # janela popup com mensagem de erro
                self.a_guardar = False # reinicia a flag para que o utilizador acabe o preenchimento dos dados
                return

        cursor.execute("SELECT id FROM clientes WHERE nome = ?", (self.entries_form[3].get(),))
        id_cliente = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM formas_pagamento WHERE tipo_pagamento = ?", (self.entries_form[4].get(),))
        id_formas_pagamento = cursor.fetchone()[0]

        cursor.execute("SELECT data_inicio, data_fim FROM reservas WHERE matricula = ?", (self.editar_matricula, ))
        reservas_existentes = cursor.fetchall()

        # Verificar datas sobreppostas
        novo_inicio = datetime.datetime.strptime(valores[0], "%d/%m/%Y")
        novo_fim = datetime.datetime.strptime(valores[1], "%d/%m/%Y")
        hoje = datetime.datetime.now().date()

        if novo_inicio.date() < hoje:
            messagebox.showerror("Erro", "A data de início não pode ser anterior à data de hoje!")
            self.a_guardar = False # reinicia a flag para que o utilizador possa corrigir a
            return

        if novo_fim.date() < novo_inicio.date():
            messagebox.showerror("Erro", "A data de fim não pode ser anterior à data de início!")
            self.a_guardar = False  # reinicia a flag para que o utilizador possa corrigir a
            return

        # Procura as datas e converte de string para data
        for reserva in reservas_existentes:
            inicio = datetime.datetime.strptime(reserva[0], "%d/%m/%Y")
            fim = datetime.datetime.strptime(reserva[1], "%d/%m/%Y")
            if novo_inicio <= fim and novo_fim >= inicio: # Verifica se as novas datas se sobrepõem a uma reserva existente
                messagebox.showinfo("Erro", "Veículo já reservado nessas datas!")
                self.a_guardar = False  # inicia a flag para permitir guardar
                return

        cursor.execute("INSERT INTO reservas (id_clientes, matricula, id_utilizadores, id_formas_pagamento, data_inicio, data_fim, valor_total) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (id_cliente, self.editar_matricula, self.id_utilizador, id_formas_pagamento, valores[0], valores[1], valores[2]))
        db.commit()  # guardar alterações na base de dados
        self.carregar_veiculos()
        messagebox.showinfo("Sucesso", "Reserva efetuada com sucesso!")  # janela popup com mensagem de guardado
        self.janela_form.destroy()  # fecha a janela após dados guardados

    def exportar_veiculos(self):
        wb = Workbook() # Cria um novo ficheiro Excel
        ws = wb.active # Seleciona a folha ativa
        ws.title = "Lista de Veículos"

        # Consulta SQL e carrega os dados a exportar
        cursor.execute("""SELECT matricula, marca, modelo, tipo_veiculo, categoria, combustivel, num_lugares,
        cor, valor_diaria, data_seguro, data_inspecao, data_ultima_revisao, data_proxima_revisao,
        em_manutencao FROM veiculos""")
        exportar_dados = cursor.fetchall()

        ws.append(["Matricula", "Marca", "Modelo", "Tipo de Veículo", "Categoria", "Combustivel", "Número de lugares",
        "Cor", "Valor da diária", "Data do seguro", "Data de Inspeção", "Data da última Revisão", "Data da proxima Revisão",
        "Em Manutenção"]) # Insere a linha de cabeçalhos no Excel

        #Loop de carregar dados
        for veiculo in exportar_dados:
            ws.append(list(veiculo))

        wb.save("Lista de Veiculos.xlsx")
        messagebox.showinfo("Sucesso", "Lista de Veículos exportada com sucesso!")

    def abrir_clientes(self):
        # Fecha janela se já aberta
        if self.frame_conteudo_atual != None:
            self.frame_conteudo_atual.destroy()

        # Criar frame para o conteúdo
        frame_conteudo = LabelFrame(self.janela, text="Lista de Clientes")
        frame_conteudo.grid(row=0, column=1, sticky="NSEW", padx=10, pady=10)
        self.frame_conteudo_atual = frame_conteudo

        # Criar tabela
        tabela = ttk.Treeview(frame_conteudo)
        self.tabela = tabela
        tabela.grid(row=0, column=0)
        frame_detalhe = LabelFrame(frame_conteudo, text="Detalhes do Cliente")
        frame_detalhe.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.entries = []

        # loop para visualizar os campos de cliente
        for i, campo in enumerate(["data_nascimento", "cartao_cidadao", "morada"]):
            label = Label(frame_detalhe, text=campo.replace("_", " ").title())  # legendas com maiusculas e espaços
            label.grid(row=i // 3 * 2, column=i % 3, sticky="nsew")
            if i == 2:
                entry = Entry(frame_detalhe, state="readonly", width=60)
            else:
                entry = Entry(frame_detalhe, state="readonly")
            entry.grid(row=i // 3 * 2 + 1, column=i % 3, padx=10, pady=10) # linha: divisão inteira i = 0 0//3 linha 0, coluna: resto da divisão i = 0 0%3 coluna 0 (temos 3 colunas e duas linhas)
            self.entries.append(entry)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(frame_conteudo, orient="vertical", command=tabela.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        tabela.configure(yscrollcommand=scrollbar.set)

        # Definir colunas
        tabela["columns"] = ("nome", "nif", "carta_conducao", "num_tlm" )
        tabela.column("#0", width=0, stretch=NO)  # esconde coluna padrão
        tabela.column("nome", width=100)
        tabela.column("nif", width=100)
        tabela.column("carta_conducao", width=100)
        tabela.column("num_tlm", width=100)

        # Cabeçalhos
        tabela.heading("nome", text="Nome")
        tabela.heading("nif", text="NIF")
        tabela.heading("carta_conducao", text="Carta de condução")
        tabela.heading("num_tlm", text="Número de Telemóvel")

        # Ocupação do frame
        self.janela.columnconfigure(1, weight=1)
        self.janela.rowconfigure(0, weight=1)
        frame_conteudo.columnconfigure(0, weight=1)
        frame_conteudo.rowconfigure(0, weight=1)
        tabela.grid(row=0, column=0, sticky="nsew")

        # Carregar dados
        self.carregar_clientes()

        # Verificar mais informação ao clicar numa linha
        tabela.bind("<<TreeviewSelect>>", lambda event: self.mostrar_detalhes_cliente())

        # Botões adicionar, editar e eliminar cliente
        # Frame de botões adicionar, editar, eliminar
        frame_botoes = Frame(frame_conteudo)
        frame_botoes.grid(row=3, column=0, sticky="nsew")

        #Botão adicionar
        self.botao_adicionar = ttk.Button(frame_botoes, text="Adicionar", command=self.adicionar_cliente)
        self.botao_adicionar.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        # Botão eliminar
        self.botao_eliminar = ttk.Button(frame_botoes, text="Eliminar", command=self.eliminar_cliente)
        self.botao_eliminar.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        # Botão editar
        self.botao_editar = ttk.Button(frame_botoes, text="Editar", command=self.editar_clientes)
        self.botao_editar.grid(row=0, column=2, sticky="n", padx=10, pady=10)

        # Botão exportar
        self.botao_exportar = ttk.Button(frame_botoes, text="Exportar Excel", command=self.exportar_clientes)
        self.botao_exportar.grid(row=0, column=5, sticky="n", padx=10, pady=10)

    def carregar_clientes(self):
        # Apaga os dados, evita dados duplicados
        self.tabela.delete(*self.tabela.get_children())


        cursor.execute("SELECT id, nome, nif, carta_conducao, num_tlm FROM clientes")
        clientes = cursor.fetchall()

        # Inserir dados na tabela
        for cliente in clientes:
            self.tabela.insert("", END, values=cliente[1:], iid=cliente[0])
            # cliente[1:] exclui o id dos valores visíveis na Treeview e o iid=cliente[0] usa o id da base de dados como identificador da linha na Treeview

    def mostrar_detalhes_cliente(self):
        id_cliente = self.tabela.focus() # Obtém o id da linha selecionada na Treeview

        # Consulta SQL para detalhes de clientes
        cursor.execute("SELECT data_nascimento, cartao_cidadao, morada FROM clientes WHERE id = ?", (id_cliente,))
        clientes = cursor.fetchall()
        if not clientes: # Sai da função se não houver linha selecionada
            return

        # Visualizar detalhes
        for entry, dado in zip(self.entries, clientes[0]):
            entry.config(state="normal")
            entry.delete(0, END)
            entry.insert(0, str(dado))
            entry.config(state="readonly")

    def adicionar_cliente(self):
        self.janela_form = Toplevel(self.janela)
        self.janela_form.grab_set() # bloqueia a janela principal enquanto o formulário está aberto, impede abrir formulários repetidos
        self.janela_form.title("Adicionar Novo Cliente")
        self.janela_form.resizable(False, False)
        self.a_guardar = False # inicia a flag para permitir guardar

        # Centrar janela toplevel
        largura_janela = 300
        altura_janela = 250

        largura_ecra = self.janela_form.winfo_screenwidth()  # largura do ecrã
        altura_ecra = self.janela_form.winfo_screenheight()  # altura do ecrã

        x = (largura_ecra // 2) - (largura_janela // 2)
        y = (altura_ecra // 2) - (altura_janela // 2)

        self.janela_form.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

        # Limpa conteudo aberto (impede janelas sobrepostas)
        self.frame_conteudo_atual = None

        # Estrutura da janela Toplevel
        frame_form = Frame(self.janela_form)
        frame_form.grid(row=0, column=0, sticky="nsew")
        self.entries_form = [] # Lista para guardar os campos do formulário

        for i, campo in enumerate(["nome", "data_nascimento", "nif", "cartao_cidadao", "carta_conducao", "morada", "num_tlm"]):
            label_clientes = Label(frame_form, text=campo, anchor="w")
            label_clientes.grid(row=i, column=0, padx=5, pady=5)
            entry_clientes = Entry(frame_form, width=20)
            entry_clientes.grid(row=i, column=1, padx=5, pady=5)
            self.entries_form.append(entry_clientes)

            if campo.startswith("data"):
                entry_clientes.bind("<FocusOut>", lambda e, en=entry_clientes: formatar_data_entry(en))  # Obriga o utilizador a manter o mesmo formato de datas
                entry_clientes.bind("<Return>", lambda e, en=entry_clientes: formatar_data_entry(en))  # formata a data ao pressionar Enter

        # coloca o foco no primeiro campo do formulário, para o utilizador poder escrever de imediato
        self.entries_form[0].focus()

        # Botão guardar
        self.botao_guardar = ttk.Button(frame_form, text="Guardar", command=self.guardar_clientes)
        self.botao_guardar.grid(row=16, columnspan=2, padx=5, pady=5)

        # Enter aciona o botão guardar
        self.janela_form.bind("<Return>", lambda e: self.guardar_clientes())

    def guardar_clientes(self):
        #Impede erro quando carregamos mais vezes no enter por engano
        if self.a_guardar:
            return
        self.a_guardar = True

        valores = [entry.get() for entry in self.entries_form]  # Ler valores dos campos do formulário

        # Verificação de entrada de valores
        for i, valor in enumerate(valores):
            if valores[i] == "":
                messagebox.showinfo("Erro", "Todos os campos devem ser preenchidos") # janela popup com mensagem de erro
                self.a_guardar = False # reinicia a flag para que o utilizador acabe o preenchimento dos dados
                return

        cursor.execute("""INSERT INTO clientes (nome, data_nascimento, nif, cartao_cidadao, carta_conducao, morada, num_tlm)
         VALUES (?, ?, ?, ?, ?, ?, ?)""", valores) #insere os valores novos na tabela sql
        db.commit() # guardar alterações na base de dados
        self.carregar_clientes()
        messagebox.showinfo("Sucesso", "Cliente guardo com sucesso!") #janela popup com mensagem de guardado
        self.janela_form.destroy() # fecha a janela após dados guardados

    def eliminar_cliente(self):
        self.id_cliente = self.tabela.focus()  # devolve o id da linha
        if not self.id_cliente:
            messagebox.showinfo("Erro", "Selecione um Cliente para eliminar")
            return

        cursor.execute("SELECT COUNT(*) FROM formas_pagamento WHERE id_cliente = ?", (self.id_cliente,))
        pagamento = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM reservas WHERE id_clientes = ?", (self.id_cliente,))
        reservas = cursor.fetchone()[0]

        # Impede eliminar cliente com registos associados em reservas ou formas de pagamento
        if pagamento > 0 or reservas > 0:
            messagebox.showerror("Erro", "Este cliente tem reservas e/ou formas de pagamento associadas e não pode ser eliminado")
            return

        # Confirmar para eliminar
        confirmacao = messagebox.askyesno(message= "Tens a certeza?", icon="question", title="Eliminar")


        cursor.execute("SELECT nome FROM clientes WHERE id = ?", (self.id_cliente,)) # Obtém o nome do cliente
        nome = cursor.fetchone()[0] # Guarda o nome para usar na mensagem de confirmação
        if confirmacao:
            cursor.execute("DELETE FROM clientes WHERE id = ?", (self.id_cliente,)) # Consulta SQL e elimina
            db.commit() # Confirma e guarda
            self.carregar_clientes()  # Atualizar a tabela de clientes
            messagebox.showinfo("Sucesso", f"{nome} eliminado!") # Dá a confirmação ao utilizador

    def editar_clientes(self):
        self.id_cliente = self.tabela.focus()  # devolve o id da linha
        if not self.id_cliente:
            messagebox.showinfo("Erro", "Selecione um Cliente para editar")
            return
        self.janela_form = Toplevel(self.janela)
        self.janela_form.grab_set() # bloqueia a janela principal enquanto o formulário está aberto, impede abrir formulários repetidos
        self.janela_form.title("Editar Cliente")
        self.janela_form.resizable(False, False)
        self.a_guardar = False  # inicia a flag para permitir guardar

        # Centrar janela toplevel
        largura_janela = 300
        altura_janela = 250

        largura_ecra = self.janela_form.winfo_screenwidth()  # largura do ecrã
        altura_ecra = self.janela_form.winfo_screenheight()  # altura do ecrã

        x = (largura_ecra // 2) - (largura_janela // 2)
        y = (altura_ecra // 2) - (altura_janela // 2)

        self.janela_form.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

        # Limpa conteudo aberto (impede janelas sobrepostas)
        self.frame_conteudo_atual = None

        # Estrutura da janela Toplevel
        frame_form = Frame(self.janela_form)
        frame_form.grid(row=0, column=0, sticky="nsew")
        self.entries_form = []


        cursor.execute("""SELECT nome, data_nascimento, nif, cartao_cidadao, carta_conducao, morada, num_tlm 
        FROM clientes WHERE id = ?""", (self.id_cliente,))
        editar_cliente = cursor.fetchall()

        # Loop para visualizar os campos de cliente
        for i, campo in enumerate(["nome", "data_nascimento", "nif", "cartao_cidadao", "carta_conducao", "morada", "num_tlm"]):
            label_clientes = Label(frame_form, text=campo, anchor="w")
            label_clientes.grid(row=i, column=0, padx=5, pady=5)
            entry_clientes = Entry(frame_form, width=20)
            entry_clientes.insert(0, editar_cliente[0][i]) # Preenche o campo com o valor correspondente do cliente selecionado
            entry_clientes.grid(row=i, column=1, padx=5, pady=5)
            self.entries_form.append(entry_clientes) # Adiciona o campo à lista para posterior leitura dos valore

            if campo.startswith("data"):
                entry_clientes.bind("<FocusOut>", lambda e, en=entry_clientes: formatar_data_entry(en))  # Obriga o utilizador a manter o mesmo formato de datas
                entry_clientes.bind("<Return>", lambda e, en=entry_clientes: formatar_data_entry(en))  # formata a data ao pressionar Enter

        # coloca o foco no primeiro campo do formulário, para o utilizador poder escrever de imediato
        self.entries_form[0].focus()

        # Botão guardar alterações
        self.botao_guardar = ttk.Button(frame_form, text="Guardar", command=self.atualizar_clientes)
        self.botao_guardar.grid(row=16, columnspan=2, padx=5, pady=5)

        # Enter aciona o botão guardar
        self.janela_form.bind("<Return>", lambda e: self.atualizar_clientes())

    def atualizar_clientes(self):
        #Impede erro quando carregamos mais vezes no enter por engano
        if self.a_guardar:
            return
        self.a_guardar = True

        valores = [entry.get() for entry in self.entries_form] # Ler valores dos campos do formulário

        cursor.execute("""UPDATE clientes SET nome = ?, data_nascimento = ?, nif = ?, cartao_cidadao = ?, carta_conducao = ?, 
        morada = ?, num_tlm = ? WHERE id = ?""", valores + [self.id_cliente])
        db.commit()  # guardar alterações na base de dados
        self.carregar_clientes()
        messagebox.showinfo("Sucesso", "Cliente alterado com sucesso!")  # janela popup com mensagem de guardado
        self.janela_form.destroy()  # fecha a janela após dados guardados

    def exportar_clientes(self):
        wb = Workbook() # Cria um novo ficheiro Excel
        ws = wb.active # Seleciona a folha ativa
        ws.title = "Lista de Clientes"

        # Consulta SQL e carrega os dados a exportar
        cursor.execute("SELECT nome, data_nascimento, nif, cartao_cidadao, carta_conducao, morada, num_tlm FROM clientes")
        exportar_dados = cursor.fetchall()

        ws.append(["Nome", "Data de Nascimento", "NIF", "Cartão do Cidadão", "Carta de Condução", "Morada", "N.º Telemovel"]) # Insere a linha de cabeçalhos no Excel

        for cliente in exportar_dados:
            ws.append(list(cliente))

        wb.save("Lista de Clientes.xlsx")
        messagebox.showinfo("Sucesso", "Lista de Clientes exportada com sucesso!")

    def abrir_reservas(self):
        # Fecha janela se já aberta
        if self.frame_conteudo_atual != None:
            self.frame_conteudo_atual.destroy()

        # Criar frame para o conteúdo
        frame_conteudo = LabelFrame(self.janela, text="Lista de Reservas")
        frame_conteudo.grid(row=0, column=1, sticky="NSEW", padx=10, pady=10)
        self.frame_conteudo_atual = frame_conteudo

        # Criar tabela
        tabela = ttk.Treeview(frame_conteudo)
        self.tabela = tabela
        tabela.grid(row=0, column=0)
        frame_detalhe = LabelFrame(frame_conteudo, text="Detalhes da reserva")
        frame_detalhe.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.entries = []
        for i, campo in enumerate(["Utilizador", "Tipo de pagamento"]):
            Label_detalhes = Label(frame_detalhe, text=campo, anchor="w")
            Label_detalhes.grid(row=i // 2 * 2, column=i % 2, padx=5, pady=5)
            entry = Entry(frame_detalhe, state="readonly")
            entry.grid(row=i // 2 * 2 + 1, column=i % 2, padx=5, pady=5) # linha: divisão inteira i = 0 0//2 linha 0, coluna: resto da divisão i = 0 0%2 coluna 0 (temos 2 colunas e duas linhas)
            self.entries.append(entry)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(frame_conteudo, orient="vertical", command=tabela.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        tabela.configure(yscrollcommand=scrollbar.set)

        # Definir colunas
        tabela["columns"] = ("nome_cliente", "matricula", "data_inicio", "data_fim", "valor_total" )
        tabela.column("#0", width=0, stretch=NO)  # esconde coluna padrão
        tabela.column("nome_cliente", width=100)
        tabela.column("matricula", width=100)
        tabela.column("data_inicio", width=100)
        tabela.column("data_fim", width=100)
        tabela.column("valor_total", width=100)

        # Cabeçalhos
        tabela.heading("nome_cliente", text="Cliente")
        tabela.heading("matricula", text="Matrícula")
        tabela.heading("data_inicio", text="Inicio a:")
        tabela.heading("data_fim", text="Termina a:")
        tabela.heading("valor_total", text="Valor total")

        # Ocupação do frame
        self.janela.columnconfigure(1, weight=1)
        self.janela.rowconfigure(0, weight=1)
        frame_conteudo.columnconfigure(0, weight=1)
        frame_conteudo.rowconfigure(0, weight=1)
        tabela.grid(row=0, column=0, sticky="nsew")

        # Consulta SQL
        cursor.execute("""SELECT reservas.id, clientes.nome, reservas.matricula, reservas.data_inicio, reservas.data_fim, reservas.valor_total 
        FROM reservas JOIN clientes ON reservas.id_clientes = clientes.id""") # O join permite o acesso ao nome do cliente a partir do id de cliente
        reservas = cursor.fetchall()

        # Inserir dados na tabela
        for reserva in reservas:
            tabela.insert("", END, values=reserva [1:], iid=reserva[0])

        # Verificar mais informação ao clicar numa linha
        tabela.bind("<<TreeviewSelect>>", lambda event: self.mostrar_detalhes_reserva())

        # Botões editar e eliminar reservas
        # Frame de botões editar, eliminar
        frame_botoes = Frame(frame_conteudo)
        frame_botoes.grid(row=3, column=0, sticky="nsew")

        # Botão eliminar
        self.botao_eliminar = ttk.Button(frame_botoes, text="Eliminar", command=self.eliminar_reservas)
        self.botao_eliminar.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        # Botão editar
        self.botao_editar = ttk.Button(frame_botoes, text="Editar", command=self.editar_reservas)
        self.botao_editar.grid(row=0, column=2, sticky="n", padx=10, pady=10)

        # Botão exportar
        self.botao_exportar = ttk.Button(frame_botoes, text="Exportar Excel", command=self.exportar_reservas)
        self.botao_exportar.grid(row=0, column=5, sticky="n", padx=10, pady=10)

    def carregar_reservas(self):
        # Apaga os dados, evita dados duplicados
        self.tabela.delete(*self.tabela.get_children())


        cursor.execute("""SELECT reservas.id, clientes.nome, reservas.matricula, reservas.data_inicio, reservas.data_fim, reservas.valor_total
                       FROM reservas JOIN clientes ON reservas.id_clientes = clientes.id""")
        reservas = cursor.fetchall()

        # Inserir dados na tabela
        for reserva in reservas:
            self.tabela.insert("", END, values=reserva[1:], iid=reserva[0])
            # reservas[1:] exclui o id dos valores visíveis na Treeview e o iid=reservas[0] usa o id da base de dados como identificador da linha na Treeview

    def mostrar_detalhes_reserva(self):
        id_reserva = self.tabela.focus()
        if not id_reserva:
            return

        # Consulta SQL para detalhes das reservas
        cursor.execute("""SELECT utilizadores.nome, formas_pagamento.tipo_pagamento FROM reservas 
        JOIN formas_pagamento ON reservas.id_formas_pagamento = formas_pagamento.id 
        JOIN utilizadores ON reservas.id_utilizadores = utilizadores.id 
        WHERE reservas.id = ?""", (id_reserva, ))
        reservas = cursor.fetchall()

        # Visualizar detalhes
        for entry, dado in zip(self.entries, reservas[0]):
            entry.config(state="normal")
            entry.delete(0, END)
            entry.insert(0, str(dado))
            entry.config(state="readonly")

    def eliminar_reservas(self):
        self.id_reservas = self.tabela.focus()  # devolve o id da linha
        if not self.id_reservas:
            messagebox.showinfo("Erro", "Selecione uma Reserva para eliminar")
            return

        # Confirmar para eliminar
        confirmacao = messagebox.askyesno(
            message= "Tens a certeza?",
            icon="question", title="Eliminar")

        if confirmacao:
            cursor.execute("DELETE FROM reservas WHERE reservas.id = ?", (self.id_reservas,)) # Consulta SQL e elimina
            db.commit() # Confirma e guarda
            self.carregar_reservas()  # Atualizar a tabela de reservas
            messagebox.showinfo("Sucesso", f"Reserva n.º{self.id_reservas} eliminada!") # Dá a confirmação ao utilizador

    def editar_reservas(self):
        self.id_reservas = self.tabela.focus()  # devolve o id da linha
        if not self.id_reservas:
            messagebox.showinfo("Erro", "Selecione uma Reserva para editar")
            return
        self.janela_form = Toplevel(self.janela)
        self.janela_form.grab_set() # bloqueia a janela principal enquanto o formulário está aberto, impede abrir formulários repetidos
        self.janela_form.title("Editar Reservas")
        self.janela_form.resizable(False, False)
        self.a_guardar = False  # inicia a flag para permitir guardar

        # Centrar janela toplevel
        largura_janela = 300
        altura_janela = 250

        largura_ecra = self.janela_form.winfo_screenwidth()  # largura do ecrã
        altura_ecra = self.janela_form.winfo_screenheight()  # altura do ecrã

        x = (largura_ecra // 2) - (largura_janela // 2)
        y = (altura_ecra // 2) - (altura_janela // 2)

        self.janela_form.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

        # Limpa conteudo aberto (impede janelas sobrepostas)
        self.frame_conteudo_atual = None

        # Estrutura da janela Toplevel
        frame_form = Frame(self.janela_form)
        frame_form.grid(row=0, column=0, sticky="nsew")
        self.entries_form = []

        # Loop de carregar dados
        cursor.execute("SELECT data_inicio, data_fim, valor_total FROM reservas WHERE reservas.id = ?", (self.id_reservas, ))
        editar_reservas= cursor.fetchall()

        # Lista para guardar as variáveis das datas
        self.vars_form = []

        # Loop para visualizar os campos das
        for i, campo in enumerate(["data_inicio", "data_fim", "valor_total"]):
            label_reservas = Label(frame_form, text=campo, anchor="w")
            label_reservas.grid(row=i, column=0, padx=5, pady=5)

            # Cria uma StringVar para os campos de data e detetar as alterações
            if i ==0 or i == 1:
                var = StringVar()
                entry_reservas = Entry(frame_form, textvariable=var)
                var.set(editar_reservas[0][i])
                self.vars_form.append(var)
                var.trace("w", lambda *args: self.recalcular_total()) # Deteta alterações nas datas e chama o recalcular_total
                entry_reservas.bind("<FocusOut>", lambda e,v=var: formatar_data(v)) # Obriga o utilizador a manter o mesmo formato de datas
                entry_reservas.bind("<Return>",  lambda e,v=var: formatar_data(v)) # formata a data ao pressionar Enter

            # Calculo automático
            elif i == 2:
                entry_reservas = Entry(frame_form, width=20)
                entry_reservas.insert(0, editar_reservas[0][i])  # Preenche o campo com o valor correspondente da reserva selecionada
                entry_reservas.config(state="readonly") # valor_total deve ser um parametro de leitura, o calculo é feito em calcular_valor_total

            entry_reservas.grid(row=i, column=1, padx=5, pady=5)
            self.entries_form.append(entry_reservas)  # Adiciona o campo à lista para posterior leitura dos valore

        # coloca o foco no primeiro campo do formulário, para o utilizador poder escrever de imediato
        self.entries_form[0].focus()

        # Botão guardar alterações
        self.botao_guardar = ttk.Button(frame_form, text="Guardar", command=self.atualizar_reservas)
        self.botao_guardar.grid(row=3, columnspan=2, padx=5, pady=5)

        # Enter aciona o botão guardar
        self.janela_form.bind("<Return>", lambda e: self.atualizar_reservas())


    def recalcular_total(self):
        nova_data_inicio = self.vars_form[0].get()
        nova_data_fim = self.vars_form[1].get()


        cursor.execute("""SELECT veiculos.valor_diaria FROM reservas JOIN veiculos ON reservas.matricula = veiculos.matricula 
        WHERE reservas.id = ?""", (self.id_reservas, ))
        reservas = cursor.fetchall()

        try:
            # Calcula a diferença entre a nova data de início e fim
            self.valor_reserva_recalc= datetime.datetime.strptime(nova_data_fim, "%d/%m/%Y").date() - datetime.datetime.strptime(nova_data_inicio, "%d/%m/%Y").date()
            self.novo_valor_total = self.valor_reserva_recalc.days * reservas[0][0]

            # Visualizar valores
            self.entries_form[2].config(state="normal")
            self.entries_form[2].delete(0, END)
            self.entries_form[2].insert(0, str(self.novo_valor_total))
            self.entries_form[2].config(state="readonly")

            return self.novo_valor_total # Retorna o calculo efetuado
        except ValueError:
            return

    def atualizar_reservas(self):
        #Impede erro quando carregamos mais vezes no enter por engano
        if self.a_guardar:
            return
        self.a_guardar = True

        valores = [entry.get() for entry in self.entries_form] # Ler valores dos campos do formulário

        # Converter datas para validação
        novo_inicio = datetime.datetime.strptime(valores[0], "%d/%m/%Y")
        novo_fim = datetime.datetime.strptime(valores[1], "%d/%m/%Y")
        hoje = datetime.datetime.now().date()

        if novo_inicio.date() < hoje:
            messagebox.showerror("Erro", "A data de início não pode ser anterior à data de hoje!")
            self.a_guardar = False # reinicia a flag para que o utilizador possa corrigir a
            return

        if novo_fim.date() < novo_inicio.date():
            messagebox.showerror("Erro", "A data de fim não pode ser anterior à data de início!")
            self.a_guardar = False  # reinicia a flag para que o utilizador possa corrigir a
            return

        cursor.execute("""UPDATE reservas SET data_inicio = ?, data_fim = ?, valor_total = ? WHERE reservas.id = ?""", valores + [self.id_reservas])
        db.commit()  # guardar alterações na base de dados
        self.carregar_reservas()
        messagebox.showinfo("Sucesso", "Reserva alterada com sucesso!")  # janela popup com mensagem de guardado
        self.janela_form.destroy()  # fecha a janela após dados guardados

    def exportar_reservas(self):
        wb = Workbook() # Cria um novo ficheiro Excel
        ws = wb.active # Seleciona a folha ativa
        ws.title = "Lista de Reservas"

        # Consulta SQL e carrega os dados a exportar
        cursor.execute("""SELECT clientes.nome, matricula, utilizadores.nome, formas_pagamento.tipo_pagamento, data_inicio, data_fim, 
        valor_total FROM reservas JOIN clientes ON reservas.id_clientes = clientes.id 
        JOIN formas_pagamento ON reservas.id_formas_pagamento = formas_pagamento.id
        JOIN utilizadores ON reservas.id_utilizadores = utilizadores.id""")
        exportar_dados = cursor.fetchall()

        ws.append([ "Nome Cliente", "Matricula", "Utilizador", "Tipo de Pagamento", "Data Inicio", "Data Fim", "Valor Total"]) # Insere a linha de cabeçalhos no Excel

        for reserva in exportar_dados:
            ws.append(list(reserva))

        wb.save("Lista de Reservas.xlsx")
        messagebox.showinfo("Sucesso", "Lista de Reservas exportada com sucesso!")

    def abrir_formas_pagamento(self):
        # Fecha janela se já aberta
        if self.frame_conteudo_atual != None:
            self.frame_conteudo_atual.destroy()

        # Criar frame para o conteúdo
        frame_conteudo = LabelFrame(self.janela, text="Lista de Formas de Pagamento")
        frame_conteudo.grid(row=0, column=1, sticky="NSEW", padx=10, pady=10)
        self.frame_conteudo_atual = frame_conteudo

        # Combobox para selecionar cliente
        cursor.execute("SELECT id, nome FROM clientes")
        lista_clientes = cursor.fetchall()

        Label(frame_conteudo, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_clientes = ttk.Combobox(frame_conteudo, values=[c[1] for c in lista_clientes], state="readonly", width=100)
        self.combo_clientes.grid(row=0, column=0, columnspan=2, sticky="e", padx=5, pady=5)
        self.combo_clientes.bind("<<ComboboxSelected>>", lambda e: self.carregar_formas_pagamento())

        # Criar tabela
        tabela = ttk.Treeview(frame_conteudo)
        self.tabela = tabela
        tabela.grid(row=1, column=0)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(frame_conteudo, orient="vertical", command=tabela.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        tabela.configure(yscrollcommand=scrollbar.set)

        # Definir colunas
        tabela["columns"] = ("tipo_pagamento", "numero_cartao", "validade", "num_tlm")
        tabela.column("#0", width=0, stretch=NO)  # esconde coluna padrão
        tabela.column("tipo_pagamento", width=100)
        tabela.column("numero_cartao", width=100)
        tabela.column("validade", width=100)
        tabela.column("num_tlm", width=100)

        # Cabeçalho
        tabela.heading("tipo_pagamento", text="Formas de Pagamento")
        tabela.heading("numero_cartao", text="Número de Cartão")
        tabela.heading("validade", text="Validade")
        tabela.heading("num_tlm", text="Número de Telemóvel")

        # Ocupação do frame
        self.janela.columnconfigure(1, weight=1)
        self.janela.rowconfigure(0, weight=1)
        frame_conteudo.columnconfigure(0, weight=1)
        frame_conteudo.rowconfigure(1, weight=1)
        tabela.grid(row=1, column=0, sticky="nsew")

        # Carregar dados
        self.carregar_formas_pagamento()

        # Botões adicionar, editar e eliminar Formas de Pagamento
        # Frame de botões adicionar, editar, eliminar
        frame_botoes = Frame(frame_conteudo)
        frame_botoes.grid(row=3, column=0, sticky="nsew")

        #Botão adicionar
        self.botao_adicionar = ttk.Button(frame_botoes, text="Adicionar", command=self.adicionar_formas_pagamento)
        self.botao_adicionar.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        # Botão eliminar
        self.botao_eliminar = ttk.Button(frame_botoes, text="Eliminar", command=self.eliminar_formas_pagamento)
        self.botao_eliminar.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        # Botão editar
        self.botao_editar = ttk.Button(frame_botoes, text="Editar", command=self.editar_formas_pagamento)
        self.botao_editar.grid(row=0, column=2, sticky="n", padx=10, pady=10)

        # Botão exportar
        self.botao_exportar = ttk.Button(frame_botoes, text="Exportar Excel", command=self.exportar_formas_pagamento)
        self.botao_exportar.grid(row=0, column=5, sticky="n", padx=10, pady=10)

    def carregar_formas_pagamento(self):
        # Apaga os dados, evita dados duplicados
        self.tabela.delete(*self.tabela.get_children())

        # Verifica se o Combobox tem valor antes de continuar
        nome_cliente = self.combo_clientes.get()
        if not nome_cliente:
            return

        # Consulta SQL e vai buscar o id da tabela de clientes para aceder ao nome
        nome_cliente = self.combo_clientes.get()
        cursor.execute("SELECT id FROM clientes WHERE nome = ?", (nome_cliente,))
        id_cliente = cursor.fetchone()[0]

        #Consulta SQL e carrega os dados através do nome do cliente
        cursor.execute("SELECT id, tipo_pagamento, numero_cartao, validade, num_tlm FROM formas_pagamento WHERE id_cliente = ?", (id_cliente,))
        formas_pagamento = cursor.fetchall()

        # Inserir dados na tabela
        for forma in formas_pagamento:
            # Mater o numero de cartão protegido
            numero_mascarado = "**** **** **** " + forma[2][-4:] if forma[2] else "N/A"
            self.tabela.insert("", END, values=(forma[1], numero_mascarado, forma[3], forma[4]), iid=forma[0] ) # forma[1:] exclui o id dos valores visíveis na Treeview e o iid=forma[0] usa o id da base de dados como identificador da linha na Treeview

    def adicionar_formas_pagamento(self):
        if not self.combo_clientes.get():
            messagebox.showinfo("Erro", "Selecione um Cliente para adicionar uma forma de pagamento")
            return
        self.janela_form = Toplevel(self.janela)
        self.janela_form.grab_set() # bloqueia a janela principal enquanto o formulário está aberto, impede abrir formulários repetidos
        self.janela_form.title("Adicionar Formas de Pagamento")
        self.janela_form.resizable(False, False)
        self.a_guardar = False  # inicia a flag para permitir guardar

        # Centrar janela toplevel
        largura_janela = 300
        altura_janela = 250

        largura_ecra = self.janela_form.winfo_screenwidth()  # largura do ecrã
        altura_ecra = self.janela_form.winfo_screenheight()  # altura do ecrã

        x = (largura_ecra // 2) - (largura_janela // 2)
        y = (altura_ecra // 2) - (altura_janela // 2)

        self.janela_form.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

        # Limpa conteudo aberto (impede janelas sobrepostas)
        self.frame_conteudo_atual = None

        # Estrutura da janela Toplevel
        frame_form = Frame(self.janela_form)
        frame_form.grid(row=0, column=0, sticky="nsew")
        self.entries_form = []


        # Loop para criar os campos de formulário para as formas de pagamento
        for i, campo in enumerate(["tipo_pagamento", "numero_cartao", "validade", "num_tlm"]):
            label_formas_pagamento = Label(frame_form, text=campo, anchor="w") # Mostra os campos
            label_formas_pagamento.grid(row=i, column=0, padx=5, pady=5)
            if campo == "tipo_pagamento":
                entry_formas_pagamento = ttk.Combobox(frame_form, values=["Monetário", "Debito", "Credito", "American Express", "MBWay"], state="readonly", width=20) # cria uma caixa com campos pré-preechidos
            else:
                entry_formas_pagamento = Entry(frame_form, width=20) # Cria um campo de texto livre para os restantes campos
            entry_formas_pagamento.grid(row=i, column=1, padx=5, pady=5)
            self.entries_form.append(entry_formas_pagamento) # Adiciona o campo à lista para depois ler os valores

        # Pré-preencher num_tlm com o número do cliente
        nome_cliente = self.combo_clientes.get()
        cursor.execute("SELECT num_tlm FROM clientes WHERE nome = ?", (nome_cliente,))
        num_tlm = cursor.fetchone()
        if num_tlm and num_tlm[0]:
            self.entries_form[3].insert(0, str(num_tlm[0]))

        # coloca o foco no primeiro campo do formulário, para o utilizador poder escrever de imediato
        self.entries_form[0].focus()

        # Botão guardar
        self.botao_guardar = ttk.Button(frame_form, text="Guardar", command=self.guardar_formas_pagamento)
        self.botao_guardar.grid(row=16, columnspan=2, padx=5, pady=5)

        # Enter aciona o botão guardar
        self.janela_form.bind("<Return>", lambda e: self.guardar_formas_pagamento())

    def guardar_formas_pagamento(self):
        #Impede erro quando carregamos mais vezes no enter por engano
        if self.a_guardar:
            return
        self.a_guardar = True

        valores = [entry.get() for entry in self.entries_form] # Ler valores dos campos do formulário

        # Verificação de entrada de valores
        tipo = valores[0].lower()

        # Preenchimento obrigatório para MBay
        if "mbway" in tipo:
            if valores[3] == "":
                messagebox.showinfo("Erro", "Preenche o número de telemóvel!")
                self.a_guardar = False  # inicia a flag para permitir guardar
                return

        # Consulta SQL e vai buscar o id da tabela de clientes para aceder ao nome
        nome_cliente = self.combo_clientes.get()
        cursor.execute("SELECT id FROM clientes WHERE nome = ?", (nome_cliente,))
        id_cliente = cursor.fetchone()[0]

        dados = [id_cliente] + valores # Junta o id_cliente aos valores do formulário para o INSERT

        cursor.execute("""INSERT INTO formas_pagamento (id_cliente, tipo_pagamento, numero_cartao, validade, num_tlm)
         VALUES (?, ?, ?, ?, ?)""", dados) #insere os valores novos na tabela sql
        db.commit() # guardar alterações na base de dados
        self.carregar_formas_pagamento()
        messagebox.showinfo("Sucesso", "Formas de Pagamento guardas com sucesso!") #janela popup com mensagem de guardado
        self.janela_form.destroy() # fecha a janela após dados guardados

    def editar_formas_pagamento(self):
        self.id_formas_pagamento = self.tabela.focus()  # devolve o id da linha
        if not self.id_formas_pagamento:
            messagebox.showinfo("Erro", "Selecione um Cliente para editar a forma de pagamento")
            return

        self.janela_form = Toplevel(self.janela)
        self.janela_form.grab_set() # bloqueia a janela principal enquanto o formulário está aberto, impede abrir formulários repetidos
        self.janela_form.title("Editar Formas de Pagamento")
        self.janela_form.resizable(False, False)
        self.a_guardar = False  # inicia a flag para permitir guardar

        # Centrar janela toplevel
        largura_janela = 300
        altura_janela = 250

        largura_ecra = self.janela_form.winfo_screenwidth()  # largura do ecrã
        altura_ecra = self.janela_form.winfo_screenheight()  # altura do ecrã

        x = (largura_ecra // 2) - (largura_janela // 2)
        y = (altura_ecra // 2) - (altura_janela // 2)

        self.janela_form.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

        # Limpa conteudo aberto (impede janelas sobrepostas)
        self.frame_conteudo_atual = None

        # Estrutura da janela Toplevel
        frame_form = Frame(self.janela_form)
        frame_form.grid(row=0, column=0, sticky="nsew")
        self.entries_form = []

        # Vai buscar os dados atuais da forma de pagamento selecionada
        cursor.execute("SELECT tipo_pagamento, numero_cartao, validade, num_tlm FROM formas_pagamento WHERE id = ?", (self.id_formas_pagamento, ))
        editar_formas_pagamento = cursor.fetchall()

        # Lista para guardar as variáveis das datas
        self.vars_form = []

        # Loop para visualizar os campos das
        for i, campo in enumerate(["tipo_pagamento", "numero_cartao", "validade", "num_tlm"]):
            label_formas_pagamento = Label(frame_form, text=campo, anchor="w")
            label_formas_pagamento.grid(row=i, column=0, padx=5, pady=5)
            entry_formas_pagamento = Entry(frame_form, width=20)
            entry_formas_pagamento.insert(0, str(editar_formas_pagamento[0][i]) if editar_formas_pagamento[0][i] else "") # Preenche o campo com o valor correspondente


            entry_formas_pagamento.grid(row=i, column=1, padx=5, pady=5)
            self.entries_form.append(entry_formas_pagamento) # Adiciona o campo à lista para posterior leitura dos valore

        # coloca o foco no primeiro campo do formulário, para o utilizador poder escrever de imediato
        self.entries_form[0].focus()

        # Botão guardar alterações
        self.botao_guardar = ttk.Button(frame_form, text="Guardar", command=self.atualizar_formas_pagamento)
        self.botao_guardar.grid(row=4, columnspan=2, padx=5, pady=5)

        # Enter aciona o botão guardar
        self.janela_form.bind("<Return>", lambda e: self.atualizar_formas_pagamento())

    def atualizar_formas_pagamento(self):
        #Impede erro quando carregamos mais vezes no enter por engano
        if self.a_guardar:
            return
        self.a_guardar = True

        valores = [entry.get() for entry in self.entries_form]  # Ler valores dos campos do formulário

        cursor.execute("UPDATE formas_pagamento SET tipo_pagamento = ?, numero_cartao = ?, validade = ?, num_tlm = ? WHERE formas_pagamento.id = ?",
                       valores + [self.id_formas_pagamento])
        db.commit()  # guardar alterações na base de dados
        self.carregar_formas_pagamento()
        messagebox.showinfo("Sucesso", "Forma de Pagamento alterada com sucesso!")# janela popup com mensagem de guardado
        self.janela_form.destroy()  # fecha a janela após dados guardados

    def eliminar_formas_pagamento(self):
        self.id_formas_pagamento = self.tabela.focus()  # devolve o id da linha
        if not self.id_formas_pagamento:
            messagebox.showinfo("Erro", "Selecione um Tipo de pagamento a eliminar")
            return

        # Confirmar para eliminar
        confirmacao = messagebox.askyesno(
            message="Tens a certeza?",
            icon="question", title="Eliminar")

        if confirmacao:
            cursor.execute("DELETE FROM formas_pagamento WHERE id = ?", (self.id_formas_pagamento,))# Consulta SQL e elimina
            db.commit()  # Confirma e guarda
            self.carregar_formas_pagamento()  # Atualizar a tabela de formas de pagamento
            messagebox.showinfo("Sucesso","Tipo de pagamento eliminado!") # Dá a confirmação ao utilizador

    def exportar_formas_pagamento(self):
        wb = Workbook() # Cria um novo ficheiro Excel
        ws = wb.active # Seleciona a folha ativa
        ws.title = "Lista de Formas de Pagamentos"

        # Consulta SQL e carrega os dados a exportar
        cursor.execute("""SELECT clientes.nome, tipo_pagamento, numero_cartao, validade, formas_pagamento.num_tlm FROM formas_pagamento 
        JOIN clientes ON formas_pagamento.id_cliente = clientes.id""")
        exportar_dados = cursor.fetchall()

        ws.append(["Nome do Cliente", "Tipo de Pagamento", "N.º do Cartão", "Validade do Cartão", "N.º Telemóvel"]) # Insere a linha de cabeçalhos no Excel

        for formas_pagamento in exportar_dados:
            # Mater o número de cartão protegido
            numero_mascarado = "**** **** **** " + formas_pagamento[2][-4:] if formas_pagamento[2] else "N/A"
            ws.append([formas_pagamento[0], formas_pagamento[1], numero_mascarado, formas_pagamento[3], formas_pagamento[4]])

        wb.save("Lista de Formas de Pagamento.xlsx")
        messagebox.showinfo("Sucesso", "Lista de Formas de pagamento exportada com sucesso!")




if __name__ == '__main__':
    root = Tk() # Instância da janela principal (cria a tabela)
    root.withdraw() # Esconde a janela até estar configurada
    app = JanelaLogin(root) # configura a tabela
    root.mainloop() # Começamos o ciclo de aplicação, é como um while True (mostra a tabela e mantem)