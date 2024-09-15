
import tkinter as tk
import Classe as sdk

class Sudoku_interface(sdk.Sudoku):
    def __init__(self):
        super().__init__()
        self.grade = [[0 for _ in range(9)] for _ in range(9)]
        self.grade_str = [[tk.StringVar(value="   ") for _ in range(9)] for _ in range(9)]
    
    def inserir_numero(self, coluna, linha, numero):
        numero = int(numero)

        if self.pistas[linha][coluna]:
            exibir_erro(2)
        else:
            self.grade[linha][coluna] = numero
            self.grade_str[linha][coluna].set(" "+str(numero))

    def apagar_numero(self, coluna, linha):
        if self.grade[linha][coluna] == 0:
            exibir_erro(9)
        elif self.pistas[linha][coluna]:
            exibir_erro(2)
        else:
            self.grade[linha][coluna] = 0
            self.grade_str[linha][coluna].set("   ")
    
    def obter_dica(self, coluna, linha):
        n_possiveis = self.verificar_possibilidades(coluna, linha)

        if len(n_possiveis) == 0:
            output("Não possui números possiveis para essa posição.")
        else:
            output("Número(s) possiveis: " + ', '.join(map(str, n_possiveis)))

# https://tkdocs.com/shipman/tkinter.pdf documentação inteira em pdf
# https://tkdocs.com/shipman/index-2.html documentação no site

# Problemas: 
# Talvez o tamanho das coisas seja pequeno demais, e feio, não sei como melhorar ainda pelos menos
# Separar os quadrantes talvez vá ser complicado, minha ideia é separar o grid em 9 partes e a cor de fundo é a separação, só teria que ver como posicionar isso com o tk

# Coisas pra dar uma olhada:
# Em geral não seria difícil criar um controle de clique e teclado se a gente conseguir fazer a base da janela: https://tkdocs.com/shipman/events.html

def obter_arquivo(arquivo):
  with open(arquivo, 'r') as file:
    return file.readlines()
def obter_arquivo_str(arquivo):
    with open(arquivo, 'r') as file:
        return file.read()
    
def exibir_erro(codigo, entrada=None):

    if entrada != None:
        entrada = entrada.replace("\n", "").strip()

    erros = {
        1: "msg 1",
        2: "Você não pode interagir com uma pista.",
        3: "msg 3",
        4: "msg 4",
        5: "msg 5",
        6: f"A jogada {entrada} não é possível",
        7: "A jogada " + entrada + " eh invalida",
        8: "O número inserido é inválido.",
        9: "Não existe nada para ser apagado na posição solicitada."
    }
    
    if abs(codigo) in erros:
        output(erros[codigo])

# root é a janela do programa
root = tk.Tk() 
root.title("Sudoku")
root.configure(background='black')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

sudoku = Sudoku_interface()
#num_pres_linha = [[False for l in range(9)] for l in range(9)]
#num_pres_coluna = [[False for l in range(9)] for l in range(9)]
#num_pres_quadrante = [[False for l in range(9)] for l in range(9)]
#eh_pista = [[False for l in range(9)] for l in range(9)]
label_matriz = [[None for l in range(9)] for l in range(9)]

qntd_avisos = tk.IntVar(value=0)

label_frame = tk.Frame(root, bg="blue")
label_frame.pack(side="top", fill="both")
tk.Label(label_frame, text="SUDOKU").pack(expand=True)

sudoku_frame = tk.Frame(root, bg="green")
sudoku_frame.pack(side="top", fill="both")
table_frame = tk.Frame(sudoku_frame)
table_frame.pack(expand=True)

input_text = tk.StringVar()
file_text = tk.StringVar()
entry_frame = tk.Frame(root, bg="red")
entry_frame.pack(side="top", fill="both")

input_entry = tk.Entry(entry_frame, textvariable=input_text)
label_entry = tk.Label(entry_frame, text="Insira suas jogadas aqui").pack(side="top")
input_entry.pack(side="top",expand=True)

file_entry = tk.Entry(entry_frame, textvariable=file_text)
label_file = tk.Label(entry_frame, text="Insira o arquivo de pistas aqui").pack(side="top")
file_entry.pack(side="top",expand=True)

aviso_str = tk.StringVar()
label_aviso = tk.Label(entry_frame, textvariable=aviso_str).pack(side="bottom")

for coluna in range(9):
    for linha in range(9):
        label_matriz[linha][coluna] = tk.Label(table_frame, textvariable=sudoku.grade_str[linha][coluna], borderwidth=1, relief="solid", padx=2, pady=2).grid(column=coluna, row=linha+2, sticky=tk.N)
# retorna uma matriz de strings normais a partir da matriz de StringVar do tkinter
#def get_matriz(matriz):
#    matriz_retorno = [[None for l in range(9)] for l in range(9)]
#    for coluna in range(9):
#        for linha in range(9):
#            matriz_retorno[linha][coluna] = matriz[linha][coluna].get()

# mostrar mensagem
def output(aviso):
    if aviso_str.get() != aviso and aviso_str.get() != aviso+f'[{qntd_avisos.get()}]':
        aviso_str.set(aviso)
        qntd_avisos.set(0)
    else:
        qntd_avisos.set(qntd_avisos.get() + 1)
        aviso_str.set(aviso+f'[{qntd_avisos.get()}]')

def validar_entrada(sudoku, entrada):
    if sdk.formatar(entrada) == None:
        exibir_erro(7, entrada)
        return None
    else:
        return sdk.verificar_jogada(sudoku, sdk.formatar(entrada))

def registrar_pistas(evento = None):
    try:
        pistas = obter_arquivo(file_text.get())
        qntd_pistas = len(pistas)
        if qntd_pistas >= 1 and qntd_pistas <= 80:
            file_text.set("")
            for pista in pistas:
                pista_form = validar_entrada(sudoku, pista)
                if pista_form != None and len(pista_form) == 3:
                    coluna, linha, numero = pista_form
                    sudoku.inserir_numero(coluna, linha, numero)
                    sudoku.pistas[pista_form[1]][pista_form[0]] = True
                else:
                    output("Configuração inválida")
        else:
            output("Quantidade inválida de pistas: "+str(qntd_pistas))
    except FileNotFoundError as erro:
        output(erro.strerror)

# Função intermediária de inserção
def inserir_teclado(evento = None):
    entrada = input_text.get()
    jogada = validar_entrada(sudoku, entrada)
    if jogada != None and len(jogada) == 3:
        sdk.registrar_acao(sudoku, jogada)
        input_text.set("")
    else:
        exibir_erro(jogada[0], entrada)

def foco_entrada(evento = None):
    root.unbind_all('<Return>')
    root.bind('<Return>', inserir_teclado)
def foco_file(evento = None):
    root.unbind_all('<Return>')
    root.bind('<Return>', registrar_pistas)

input_entry.bind("<FocusIn>", foco_entrada)
file_entry.bind("<FocusIn>", foco_file)
root.bind('<Return>', inserir_teclado)

#Rodar o programa
root.mainloop()