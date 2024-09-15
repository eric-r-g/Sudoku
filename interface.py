
import tkinter as tk
import Classe as sdk

# https://tkdocs.com/shipman/tkinter.pdf documentação inteira do tkinter em pdf
# https://tkdocs.com/shipman/index-2.html documentação no site

# Problemas: 
# Talvez o tamanho das coisas seja pequeno demais, e feio, não sei como melhorar ainda pelos menos
# Separar os quadrantes talvez vá ser complicado, minha ideia é separar o grid em 9 partes e a cor de fundo é a separação, só teria que ver como posicionar isso com o tk

# Classe herdada do programa principal
class Sudoku_interface(sdk.Sudoku):
    def __init__(self):
        super().__init__()
        self.grade = [[0 for _ in range(9)] for _ in range(9)]
        self.grade_str = [[tk.StringVar(value="   ") for _ in range(9)] for _ in range(9)]
        self.celulas_preenchidas = 0
    
    def inserir_numero(self, coluna, linha, numero):
        numero = int(numero)

        if self.pistas[linha][coluna]:
            exibir_erro(2)
        else:
            self.grade[linha][coluna] = numero
            self.grade_str[linha][coluna].set(" "+str(numero))
            self.celulas_preenchidas += 1

    def apagar_numero(self, coluna, linha):
        if self.grade[linha][coluna] == 0:
            exibir_erro(9)
        elif self.pistas[linha][coluna]:
            exibir_erro(2)
        else:
            self.grade[linha][coluna] = 0
            self.grade_str[linha][coluna].set("   ")
            self.celulas_preenchidas -= 1
    
    def obter_dica(self, coluna, linha):
        n_possiveis = self.verificar_possibilidades(coluna, linha)

        if len(n_possiveis) == 0:
            output("Não possui números possiveis para essa posição.")
        else:
            output("Número(s) possiveis: " + ', '.join(map(str, n_possiveis)))

def obter_arquivo(arquivo):
  with open(arquivo, 'r') as file:
    return file.readlines()

# Declarar a janela principal, em seguida algumas configurações para ela
root = tk.Tk() 
root.title("Sudoku")
root.configure(background='black')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.minsize(400, 310)

# Variáveis principais do programa
sudoku = Sudoku_interface()
qntd_outputs = tk.IntVar(value=0)
input_text = tk.StringVar()
file_text = tk.StringVar()
output_str = tk.StringVar(value="Insira o caminho de um arquivo na entrada inferior")


# ========= Criação e configuração dos frames e widgets do programa ========= #

title_frame = tk.Frame(root, bg="blue")
title_frame.pack(side="top", fill="both")
tk.Label(title_frame, text="SUDOKU").pack(expand=True)

# Alguns frames usados para posicionar a grade no centro da tela
sudoku_frame = tk.Frame(root, bg="green")
sudoku_frame.pack(side="top", fill="both")
table_frame = tk.Frame(sudoku_frame)
table_frame.pack(expand=True)

entry_frame = tk.Frame(root, bg="red", )
entry_frame.pack(side="top", fill="both")

input_entry = tk.Entry(entry_frame, textvariable=input_text)
tk.Label(entry_frame, text="Insira suas jogadas aqui").pack(side="top")
input_entry.pack(side="top",expand=True)

file_entry = tk.Entry(entry_frame, textvariable=file_text)
tk.Label(entry_frame, text="Insira o arquivo de pistas aqui").pack(side="top")
file_entry.pack(side="top",expand=True)

# Label que mostra os outputs do programa
tk.Label(entry_frame, textvariable=output_str).pack(side="bottom")


# ========= Funções principais do programa ========= #

def exibir_erro(codigo, entrada=None):

    if entrada != None:
        entrada = entrada.replace("\n", "").strip()

    erros = {
        1: "a linha ou a coluna está fora do alcance",
        2: "Você não pode interagir com uma pista.",
        3: "Você não pode ver as possibilidades de uma posição já preenchida",
        4: "msg 4",
        5: "O número precisa ser de 1 a 9",
        6: f"A jogada {entrada} não é possível",
        7: f"A jogada {entrada} eh invalida",
        8: "O número inserido é inválido.",
        9: "Não existe nada para ser apagado na posição solicitada."
    }
    
    if abs(codigo) in erros:
        output(erros[codigo])

# Mostrar mensagem (Uma função print() mas na tela)
def output(output):
    # Sisteminha pra mostrar repetições de output no formato "repetição[1]"
    if output_str.get() != output and output_str.get() != output+f'[{qntd_outputs.get()}]':
        output_str.set(output)
        qntd_outputs.set(0)
    else:
        qntd_outputs.set(qntd_outputs.get() + 1)
        output_str.set(output+f'[{qntd_outputs.get()}]')

# Exatamente igual a do programa principal, copiada para usar o exibir_erro() daqui
def validar_entrada(sudoku, entrada):
    if sdk.formatar(entrada) == None:
        exibir_erro(7, entrada)
        return None
    else:
        return sdk.verificar_jogada(sudoku, sdk.formatar(entrada))

def registrar_pistas(evento):
    try:
        pistas = obter_arquivo(file_text.get())
        qntd_pistas = len(pistas)
        if qntd_pistas >= 1 and qntd_pistas <= 80:
            file_text.set("")
            invalida = False
            for pista in pistas:
                pista_form = validar_entrada(sudoku, pista)
                if pista_form != None and len(pista_form) == 3 and not invalida:
                    coluna, linha, numero = pista_form
                    sudoku.inserir_numero(coluna, linha, numero)
                    sudoku.pistas[pista_form[1]][pista_form[0]] = True
                else:
                    invalida = True
            if invalida:
                output("Configuração inválida")
            else:    
                output('Use a entrada superior ou clique em um espaço')
        else:
            output("Quantidade inválida de pistas: "+str(qntd_pistas))
    except FileNotFoundError as erro:
        output(erro.strerror)

# Função intermediária de inserção para o teclado
def inserir_teclado(evento):
    entrada = input_text.get()
    jogada = validar_entrada(sudoku, entrada)
    if jogada != None and len(jogada) == 3 and not sudoku.finalizado:
        sdk.registrar_acao(sudoku, jogada)
        input_text.set("")
    elif sudoku.celulas_preenchidas == 81 or sudoku.finalizado:
        sudoku.finalizado = True
        output('Parabéns! Você completou o sudoku')
    else:
        exibir_erro(jogada[0], entrada)

# Função intermediária de controle dos eventos de mouse
def handle_click(evento):
    widget = evento.widget
    widget.focus_set()

    # Função intermediária de inserção para o mouse
    def inserir_click(evento):
        def processo_insercao(entrada):
            jogada = validar_entrada(sudoku, entrada)
            if jogada != None and len(jogada) == 3:
                sdk.registrar_acao(sudoku, jogada)
                input_text.set("")
                print(sudoku.celulas_preenchidas)
            elif sudoku.celulas_preenchidas == 81 or sudoku.finalizado:
                sudoku.finalizado = True
                output('Parabéns! Você completou o sudoku')
            else:
                exibir_erro(jogada[0], entrada)
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

# Funções intermediárias de controle dos eventos de teclado
def foco_entrada(evento):
    root.unbind_all('<Return>')
    root.bind('<Return>', inserir_teclado)
def foco_file(evento):
    root.unbind_all('<Return>')
    root.bind('<Return>', registrar_pistas)


# ========= Inicialização do programa ========= #

# Criação da grade do sudoku na janela
for coluna in range(9):
    for linha in range(9):
        cell = tk.Label(table_frame, textvariable=sudoku.grade_str[linha][coluna], borderwidth=1, relief="solid", padx=2, pady=2)
        cell.grid(column=coluna, row=linha+2, sticky=tk.N)
        cell.linha = linha
        cell.coluna = coluna
        cell.conteudo = sudoku.grade_str[linha][coluna]
        cell.bind('<Button-1>',handle_click)

# Eventos de teclado do programa
input_entry.bind('<FocusIn>', foco_entrada)
file_entry.bind('<FocusIn>', foco_file)
root.bind('<Return>', inserir_teclado)

# Iniciar o programa
root.mainloop()