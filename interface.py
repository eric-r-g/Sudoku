
import tkinter as tk
import Sudoku as sdk


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
    
def exibir_erro(codigo):
    erros = {
        -1: "msg 1",
        -2: "msg 2",
        -3: "msg 3",
        -4: "msg 4",
        -5: "msg 5",
        -6: "msg 6",
        -7: "msg 7"
    }
    
    if codigo in erros:
        avisar(erros[codigo])

# root é a janela do programa
root = tk.Tk() 
root.title("Sudoku")
root.configure(background='black')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

num_pres_linha = [[False for l in range(9)] for l in range(9)]
num_pres_coluna = [[False for l in range(9)] for l in range(9)]
num_pres_quadrante = [[False for l in range(9)] for l in range(9)]
eh_pista = [[False for l in range(9)] for l in range(9)]
str_matriz = [[tk.StringVar(value="   ") for l in range(9)] for l in range(9)]
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
        label_matriz[linha][coluna] = tk.Label(table_frame, textvariable=str_matriz[linha][coluna], borderwidth=1, relief="solid", padx=2, pady=2).grid(column=coluna, row=linha+2, sticky=tk.N)

def get_matriz(matriz):
    matriz_retorno = [[None for l in range(9)] for l in range(9)]
    for coluna in range(9):
        for linha in range(9):
            matriz_retorno[linha][coluna] = matriz[linha][coluna].get()

def avisar(aviso):
    if aviso_str.get() != aviso and aviso_str.get() != aviso+f'[{qntd_avisos.get()}]':
        aviso_str.set(aviso)
        qntd_avisos.set(0)
    else:
        qntd_avisos.set(qntd_avisos.get() + 1)
        aviso_str.set(aviso+f'[{qntd_avisos.get()}]')

def registrar_pistas(evento = None):
    try:
        pistas = obter_arquivo(file_text.get())
        qntd_pistas = len(pistas)
        if qntd_pistas >= 1 and qntd_pistas <= 80:
            file_text.set("")
            for pista in pistas:
                pista_form = sdk.form_e_verif_entrada(pista, get_matriz(str_matriz), eh_pista, num_pres_linha, num_pres_coluna, num_pres_quadrante)
                if pista_form[0] >= 0:
                    inserir(pista_form)
                    eh_pista[pista_form[1]][pista_form[0]] = True
                else:
                    avisar("Configuração inválida")
        else:
            avisar("Quantidade inválida de pistas: "+str(qntd_pistas))
    except FileNotFoundError as erro:
        avisar(erro.strerror)

def inserir(entrada):
    coluna, linha, numero = entrada
    numero = int(numero)
    quadrante = coluna // 3 + 3 * (linha // 3)

    num_anterior = str_matriz[linha][coluna].get().strip()
    if num_anterior != "":
        num_anterior = int(num_anterior) - 1
        num_pres_linha[linha][num_anterior] = False
        num_pres_coluna[coluna][num_anterior] = False
        num_pres_quadrante[quadrante][num_anterior] = False

    num_pres_linha[linha][numero - 1] = True
    num_pres_coluna[coluna][numero - 1] = True
    num_pres_quadrante[quadrante][numero - 1] = True

    str_matriz[linha][coluna].set(" "+str(numero))

def inserir_teclado(evento = None):
    jogada = sdk.form_e_verif_entrada(input_text.get(), get_matriz(str_matriz), eh_pista, num_pres_linha, num_pres_coluna, num_pres_quadrante)
    if jogada[0] >= 0:
        inserir(jogada) 
        input_text.set("")
    else:
        exibir_erro(jogada[0])

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