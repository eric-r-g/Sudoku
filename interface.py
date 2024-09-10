import tkinter as tk

# não tá sendo usado
matriz = [["1" for l in range(9)] for l in range(9)]

# https://tkdocs.com/shipman/tkinter.pdf documentação inteira em pdf
# https://tkdocs.com/shipman/index-2.html documentação no site

# Resumo: 
# crio três frames, insiro as celulas no do meio usando dois "for" e o resto é sintaxe do tkinter
# A parte mais importante do posicionamento é o .pack, ele insere o frame no frame pai na direção "contrária" a dada por "side"...
# Nesse caso todos os frames estão como "side='top'" então um é colocado abaixo do outro

# Problemas: 
# Talvez o tamanho das coisas seja pequeno demais, e feio, não sei como melhorar ainda pelos menos
# Separar os quadrantes talvez vá ser complicado, minha ideia é separar o grid em 9 partes e a cor de fundo é a separação, só teria que ver como posicionar isso com o tk

# Coisas pra dar uma olhada:
# O jeito que variaveis dentro da janela são definidos é diferente mas creio que não vá ser um problema: https://tkdocs.com/shipman/control-variables.html
# Em geral não seria difícil criar um controle de clique e teclado se a gente conseguir fazer a base da janela: https://tkdocs.com/shipman/events.html
# Tem como fazer os programas de forma bem mais organizada com classes, mas fica muito mais complicado do que a gente precisa(pelo menos eu achei): https://tkdocs.com/shipman/minimal-app.html 

# root é a janela do programa
root = tk.Tk() 
root.title("Sudoku")
root.configure(background='black')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

label_frame = tk.Frame(root, bg="blue")
label_frame.pack(side="top", fill="both")
tk.Label(label_frame, text="SUDOKU").pack(expand=True)

sudoku_frame = tk.Frame(root, bg="green")
sudoku_frame.pack(side="top", fill="both")
table_frame = tk.Frame(sudoku_frame)
table_frame.pack(expand=True)

entry_frame = tk.Frame(root, bg="red")
entry_frame.pack(side="top", fill="both")
tk.Entry(entry_frame).pack(expand=True)

for coluna in range(9):
    for linha in range(9):
        tk.Label(table_frame, text=str(coluna)+" "+str(linha), borderwidth=1, relief="solid", padx=2, pady=2).grid(column=coluna, row=linha+2, sticky=tk.N)
        
#Rodar o programa
root.mainloop()