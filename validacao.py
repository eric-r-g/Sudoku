def validar_entrada(sudoku, entrada):
    if formatar(entrada) == None:
        exibir_erro(7, entrada)
        return None
    else:
        return verificar_jogada(sudoku, formatar(entrada))
      

def formatar(entrada):
    try:
        entrada = entrada.replace(" ","").strip().upper()

        if "?" in entrada:
            coluna, linha = entrada.replace("?","").split(",")
            conteudo = "?"
        elif "!" in entrada:
            coluna, linha = entrada.replace("!","").split(",")
            conteudo = "!"
        else:
            entrada, conteudo = entrada.split(":")
            coluna, linha = entrada.split(",")
            conteudo = int(conteudo)
        
        # permite a ordem da linha e coluna de qualquer forma 
        if not linha.isnumeric():
            linha, coluna = coluna, linha
        linha = int(linha) - 1
        coluna = ord(coluna) - 65
        
        if coluna < 0 or coluna > 25:
            return None
    except ValueError:
        return None
    
    return [coluna, linha, conteudo]


def verificar_jogada(sudoku, entrada_formatada):
    coluna, linha, conteudo = entrada_formatada

    jogada_dados = [coluna, linha, conteudo]
    
    if linha < 0 or linha > 8 or coluna < 0 or coluna > 8:
        jogada_dados = [1]
    elif sudoku.pistas[linha][coluna]:
        jogada_dados = [2]
    elif conteudo == '?' and sudoku.grade[linha][coluna] != 0:
        jogada_dados = [3]
    elif conteudo == '!' and sudoku.grade[linha][coluna] == 0:
        jogada_dados = [9]
    elif conteudo == "?" or conteudo == "!":
        return jogada_dados
    else:
        conteudo = int(conteudo)

        quadrante = coluna // 3 + 3 * (linha // 3)

        if conteudo < 0 or conteudo > 9:
            jogada_dados = [5]
        elif sudoku.existe_numero_presente("linha", linha, conteudo) or sudoku.existe_numero_presente("coluna", coluna, conteudo) or sudoku.existe_numero_presente("quadrante", quadrante, conteudo):
            jogada_dados = [6]
        
    return jogada_dados

# Registra as mensagens de erro baseado em um número correspondente.
# Alguns eventos envolvem a jogada/ação do usuário e podem ser passadas como parâmetro da função.
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
        print(erros[codigo])
