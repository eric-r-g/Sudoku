
import tkinter as tk
from Classe import Sudoku
from validacao import validar_entrada

# https://tkdocs.com/shipman/tkinter.pdf documentação inteira do tkinter em pdf
# https://tkdocs.com/shipman/index-2.html documentação no site

# Classe herdada do programa principal
class Sudoku_interface(Sudoku):
    def __init__(self):
        super().__init__()
        self.grade_str = [[tk.StringVar(value="    ") for _ in range(9)] for _ in range(9)]
        self.grade_label = [[None for _ in range(9)] for _ in range(9)]

    # Função para atualizar a vizualização da grade
    def atualizar_visualizacao(self, coluna, linha, numero = "  "):
        self.grade_str[linha][coluna].set(" "+str(numero)+" ")

    # Adaptação da função inserção para o tkinter
    def inserir_numero(self, coluna, linha, numero):
        numero = int(numero)

        if self.pistas[linha][coluna]:
            exibir_erro(2)
        else:
            self.grade[linha][coluna] = numero
            self.celulas_preenchidas += 1
            if self.celulas_preenchidas == 81 or self.finalizado:
                self.finalizado = True

    # Adaptação da função de remoção para o tkinter
    def apagar_numero(self, coluna, linha):
        if self.grade[linha][coluna] == 0:
            exibir_erro(9)
        elif self.pistas[linha][coluna]:
            exibir_erro(2)
        else:
            self.grade[linha][coluna] = 0
            self.celulas_preenchidas -= 1
        if self.celulas_preenchidas < 81:
            self.finalizado = False

    # Adaptação da função de dica para o tkinter
    def obter_dica(self, coluna, linha):
        n_possiveis = self.verificar_possibilidades(coluna, linha)

        if len(n_possiveis) == 0:
            output("Não possui números possiveis para essa posição.")
        else:
            output("Número(s) possiveis: " + ', '.join(map(str, n_possiveis)))

    # Função para resetar o jogo
    def clear(self):
        for coluna in range(9):
            for linha in range(9):
                self.grade[linha][coluna] = 0
                self.pistas[linha][coluna] = False
                self.grade_str[linha][coluna].set("    ")
                sudoku.grade_label[linha][coluna].configure(fg="black")
        self.celulas_preenchidas = 0
        self.finalizado = False
        output("Jogo resetado")

# Função para obtenção de arquivo 
def obter_arquivo(arquivo):
  with open(arquivo, 'r') as file:
    return file.readlines()

# Declarar a janela principal, em seguida algumas configurações para ela
root = tk.Tk() 
root.title("Sudoku")
root.configure(background='black')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.minsize(600, 310)

# Variáveis principais do programa
sudoku = Sudoku_interface()
qntd_outputs = tk.IntVar(value=0)
input_text = tk.StringVar()
file_text = tk.StringVar()
batch_text = tk.StringVar()
output_str = tk.StringVar(value="Insira o caminho de um arquivo na entrada inferior")
batch = tk.BooleanVar(value=False)
batch_anim = tk.BooleanVar(value=True)

# ========= Funções principais do programa ========= #

# Adaptação para a função de erro
def exibir_erro(codigo, entrada=None):

    if entrada != None:
        entrada = entrada.replace("\n", "").strip()

    erros = {
        1: "a linha ou a coluna esta fora do alcance",
        2: "Voce nao pode interagir com uma pista.",
        3: "Voce nao pode ver as possibilidades de uma posicao ja preenchida",
        4: "msg 4",
        5: "O numero precisa ser de 1 a 9",
        6: f"A jogada {entrada} nao eh possivel",
        7: f"A jogada {entrada} eh invalida",
        8: "O numero inserido eh invalido.",
        9: "Nao existe nada para ser apagado na posicao solicitada."
    }
    
    if abs(codigo) in erros:
        output(erros[codigo])

# Mostrar mensagem (Uma função print() mas na tela)
def output(output):
    # Sisteminha pra mostrar repetições de output no formato "repetição[1]"
    output = str(output)
    if output_str.get() != output and output_str.get() != output+f'[{qntd_outputs.get()}]':
        output_str.set(output)
        qntd_outputs.set(0)
    else:
        qntd_outputs.set(qntd_outputs.get() + 1)
        output_str.set(output+f'[{qntd_outputs.get()}]')

# Funcao para registrar as pistas, adaptada
def registrar_pistas(evento):
    try:
        pistas = obter_arquivo(file_text.get())
        qntd_pistas = len(pistas)
        if qntd_pistas >= 1 and qntd_pistas <= 80:
            invalida = False
            for pista in pistas:
                pista_form = validar_entrada(sudoku, pista)
                coluna, linha, numero = pista_form
                if pista_form != None and len(pista_form) == 3 and not invalida:
                    registrar_acao(pista_form)
                    sudoku.pistas[linha][coluna] = True
                else:
                    invalida = True
                sudoku.grade_label[linha][coluna].configure(fg="red")
            if invalida:
                output("Configuração inválida")
            else:    
                output('Use a entrada superior ou clique em um espaço')
        else:
            output("Quantidade invalida de pistas: "+str(qntd_pistas))
    except FileNotFoundError as erro:
        output(erro.strerror)
    file_text.set("")

# Função para registrar as jogadas do batch, adaptada
def registrar_batch(evento):
    if batch.get():
        entradas = obter_arquivo(batch_text.get())
        tempo = 0
        erros = 'nenhuma\n'
        for entrada in entradas:
            tempo+=1
            jogada = validar_entrada(sudoku, entrada)
            if jogada != None and len(jogada) == 3:
                registrar_acao (jogada, tempo*batch_anim.get())
            else:
                if erros == 'nenhuma': erros = ''
                erros = erros + entrada
    saida = f'Jogadas invalidas: {erros}' + ("Parabens! Você completou o sudoku" if sudoku.finalizado else "Voce nao completou o sudoku")
    if batch_anim.get(): entry_frame.after(100*len(entradas) ,output, saida)
    else: output(saida)
    batch_text.set('')

# Função para registrar as ações, adaptadas
def registrar_acao(acao, tempo = 0):
    coluna, linha, conteudo = acao

    acoes = {
        "!": sudoku.apagar_numero,
        "?": sudoku.obter_dica
    }

    try:
        # Checa se é um número de 1-9
        if 1 <= int(conteudo) <= 9:
            sudoku.inserir_numero(coluna, linha, int(conteudo))
            if tempo <= 0:
                sudoku.atualizar_visualizacao(coluna, linha, int(conteudo))
            else:
                sudoku.grade_label[linha][coluna].after(100*tempo, sudoku.atualizar_visualizacao, coluna, linha, int(conteudo))
    # Se não for um número, vai tentar procurar uma ação com o conteudo da variável
    except ValueError:
        if conteudo in acoes:
            acoes[conteudo](coluna, linha)
            if tempo <= 0 and conteudo != "?":
                sudoku.atualizar_visualizacao(coluna, linha)
            elif conteudo != "?":
                sudoku.grade_label[linha][coluna].after(100*tempo, sudoku.atualizar_visualizacao, coluna, linha)


# Função intermediária de inserção para o teclado
def inserir_teclado(evento):
    entrada = input_text.get()
    jogada = validar_entrada(sudoku, entrada)
    if jogada != None and len(jogada) == 3 and not sudoku.finalizado:
        registrar_acao(jogada)
        input_text.set("")
    elif jogada == None:
        exibir_erro(7, entrada)
    else:
        exibir_erro(jogada[0], entrada)
    if sudoku.finalizado:
        output('Parabéns! Você completou o sudoku')

# Função intermediária de controle dos eventos de mouse
def handle_click(evento):
    widget = evento.widget
    widget.focus_set()

    # Função intermediária de inserção para o mouse
    def inserir_click(evento):
        def processo_insercao(entrada):
            jogada = validar_entrada(sudoku, entrada)
            if jogada != None and len(jogada) == 3:
                registrar_acao(jogada)
                input_text.set("")
            else:
                exibir_erro(jogada[0], entrada)
            if sudoku.finalizado:
                output('Parabéns! Você completou o sudoku')
        digito = evento.keysym
        if digito != "0" and digito.isnumeric():
            entrada = f'{chr(widget.coluna+65)},{widget.linha+1}:{digito}'
            processo_insercao(entrada)
        elif digito == "0":
            entrada = f'?{chr(widget.coluna+65)},{widget.linha+1}'
            processo_insercao(entrada)
        elif digito == "BackSpace":
            entrada = f'!{chr(widget.coluna+65)},{widget.linha+1}'
            processo_insercao(entrada)
        elif digito == "Escape":
            output("Jogada cancelada")
        root.focus()
        

    output('Insira um digito no seu teclado, Backspace para apagar,\n0 para verificar possibilidades ou Escape para cancelar')
    widget.bind('<KeyPress>', inserir_click)

# Função do botão de batch
def set_batch():
    if batch.get():
        batch_entry = tk.Entry(batch_frame, textvariable=batch_text, name="entry")
        batch_label = tk.Label(batch_frame, text="Insira o arquivo de entrada aqui", name="label")
        batch_label.pack(side="top")
        batch_entry.pack(side="top",expand=True)
        batch_entry.bind('<FocusIn>', foco_batch)
    else:
        batch_frame.children['entry'].destroy()
        batch_frame.children['label'].destroy()
    batch_text.set('') 

# Funções intermediárias de controle dos eventos de teclado
def foco_entrada(evento):
    root.unbind_all('<Return>')
    root.bind('<Return>', inserir_teclado)
def foco_file(evento):
    root.unbind_all('<Return>')
    root.bind('<Return>', registrar_pistas)
def foco_batch(evento):
    root.unbind_all('<Return>')
    root.bind('<Return>', registrar_batch)

# ========= Criação e configuração dos frames e widgets do programa ========= #
title_frame = tk.Frame(root, bg="#5432a8")
title_frame.pack(side="top", fill="both")
tk.Label(title_frame, text="SUDOKU").pack(expand=True)

# Alguns frames usados para posicionar a grade no centro da tela
sudoku_frame = tk.Frame(root, bg="#7e42f5")
sudoku_frame.pack(side="top", fill="both")
table_frame = tk.Frame(sudoku_frame, bg="black")
table_frame.pack()

entry_frame = tk.Frame(root, bg="#3f2580")
entry_frame.pack(side="top", fill="both")

options_frame = tk.Frame(sudoku_frame, bg="yellow")
options_frame.place(relx=0.75, rely=0.05)

tk.Label(options_frame, text="Opções").pack(side="top")
tk.Checkbutton(options_frame, variable=batch, command=set_batch, text="Modo batch").pack(side="top")
tk.Checkbutton(options_frame, variable=batch_anim, text="Animação do batch").pack(side="top")
tk.Button(options_frame, command=sudoku.clear, text="Resetar jogo", fg="red").pack(side="top")
tk.Button(options_frame, command=root.quit, text="Sair", fg="red").pack(side="top")

input_entry = tk.Entry(entry_frame, textvariable=input_text)
tk.Label(entry_frame, text="Insira suas jogadas aqui").pack(side="top")
input_entry.pack(side="top",expand=True)

file_entry = tk.Entry(entry_frame, textvariable=file_text)
tk.Label(entry_frame, text="Insira o arquivo de pistas aqui").pack(side="top")
file_entry.pack(side="top",expand=True)

batch_frame = tk.Frame(entry_frame, bg="#3f2580")
batch_frame.pack(side="top")

# Label que mostra os outputs do programa
tk.Label(entry_frame, textvariable=output_str).pack(side="bottom")

# ========= Inicialização do programa ========= #

# Criação da grade do sudoku na janela
def iniciar_matriz():
    for coluna in range(9):
        for linha in range(9):
            cell = tk.Label(table_frame, textvariable=sudoku.grade_str[linha][coluna], borderwidth=1, relief="solid", padx=2, pady=2, font="Bold")
            cell.grid(column=coluna, row=linha)
            cell.linha = linha
            cell.coluna = coluna
            cell.conteudo = sudoku.grade_str[linha][coluna]
            cell.bind('<Button-1>',handle_click)
            sudoku.grade_label[linha][coluna] = cell

# Eventos de teclado do programa
input_entry.bind('<FocusIn>', foco_entrada)
file_entry.bind('<FocusIn>', foco_file)
root.bind('<Return>', inserir_teclado)

# Iniciar o programa
def iniciar_interface():
    print('Iniciando interface')
    iniciar_matriz()
    root.mainloop()