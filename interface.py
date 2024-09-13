
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

# root é a janela do programa
root = tk.Tk() 
root.title("Sudoku")
root.configure(background='black')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

str_matriz = [[tk.StringVar(value="   ") for l in range(9)] for l in range(9)]
label_matriz = [[None for l in range(9)] for l in range(9)]

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
input_entry.pack(side="top",expand=True)
file_entry = tk.Entry(entry_frame, textvariable=file_text)
file_entry.pack(side="top",expand=True)

for coluna in range(9):
    for linha in range(9):
        label_matriz[coluna][linha] = tk.Label(table_frame, textvariable=str_matriz[coluna][linha], borderwidth=1, relief="solid", padx=2, pady=2).grid(column=coluna, row=linha+2, sticky=tk.N)

def registrar_pistas(evento = None):
    pistas = obter_arquivo(file_text.get())
    file_text.set("")
    for pista in pistas:
        inserir(pista)

def inserir(entrada):
    coluna, linha, conteudo = sdk.formatacao(entrada)
    str_matriz[coluna][linha].set(" "+str(conteudo))

def inserir_teclado(evento = None):
    coluna, linha, conteudo = sdk.formatacao(input_text.get())
    input_text.set("")
    str_matriz[coluna][linha].set(" "+str(conteudo))

def foco_entrada(evento = None):
    print("foco") 
    root.unbind_all('<Return>')
    root.bind('<Return>', inserir_teclado)
def blur_entrada(evento = None):
    print("blur") 
    root.unbind_all('<Return>')
    root.bind('<Return>', registrar_pistas)
input_entry.bind("<FocusIn>", foco_entrada)
input_entry.bind("<FocusOut>", blur_entrada)
root.bind('<Return>', inserir_teclado)

#Rodar o programa
root.mainloop()