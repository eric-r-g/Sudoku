import sys

# Classe principal que inicializa a matriz e os dados do jogo.
class Sudoku:
    def __init__(self):
        self.grade = [[0 for _ in range(9)] for _ in range(9)]
        self.pistas = [[False for _ in range(9)] for _ in range(9)]
        self.finalizado = False
        self.celulas_preenchidas = 0
    
    # Função para inserir um número dentro da grade.
    def inserir_numero(self, coluna, linha, numero):
        numero_atual = self.grade[linha][coluna]
        
        if self.pistas[linha][coluna]:
            exibir_erro(2)
        elif numero_atual != 0:
            substituir = input("Já existe um número nessa posição. Deseja substituir? (Digite 'sim' para prosseguir): ").strip().lower()
            if substituir == "sim":
                self.grade[linha][coluna] = numero
            # Caso o usuário digite outra coisa, o código irá prosseguir normalmente.
        else:
            self.grade[linha][coluna] = numero
            self.celulas_preenchidas += 1

    # Função responsável por apagar um número da grade.
    def apagar_numero(self, coluna, linha): 
        if self.grade[linha][coluna] == 0:
            exibir_erro(9)
        elif self.pistas[linha][coluna]:
            exibir_erro(2)
        else:
            self.grade[linha][coluna] = 0
            self.celulas_preenchidas -= 1

    def existe_numero_presente(self, local, i, numero):
        # Analisa em uma coluna ou linha.
        if local.lower() == "coluna":
            for linha in range(9):
                if self.grade[linha][i] == numero:
                    return True

            return False

        elif local.lower() == "quadrante":
            inicio_linha = (i // 3) * 3
            inicio_coluna = (i % 3) * 3

            for x in range(inicio_linha, inicio_linha + 3):
                for y in range(inicio_coluna, inicio_coluna + 3):
                    if (self.grade[x][y] == numero):
                        return True

            return False

        # Se não for um dos casos acima, assume que seja uma linha
        else:
            for coluna in range(9):
                if self.grade[i][coluna] == numero:
                    return True
            return False

    # Analisa as possíveis posições para uma posição específicas e retorna quais números são possíveis de inserir.
    def verificar_possibilidades(self, coluna, linha):
        numeros_possiveis = []
        quadrante = (coluna // 3) + 3 * (linha // 3)

        for i in range(1, 10):
            if not (self.existe_numero_presente("linha", linha, i) or
                    self.existe_numero_presente("coluna", coluna, i) or
                    self.existe_numero_presente("quadrante", quadrante, i)):
                     numeros_possiveis.append(i)
        
        return numeros_possiveis

    def obter_dica(self, coluna, linha):
        n_possiveis = self.verificar_possibilidades(coluna, linha)

        if len(n_possiveis) == 0:
            print("Não possui números possiveis para essa posição.")
        else:
            print("Número(s) possiveis: " + ', '.join(map(str, n_possiveis)))

    def exibir_grade(self):
        fil_padrao = [
            "    A   B   C    D   E   F    G   H   I",
            " ++---+---+---++---+---+---++---+---+---++",
            " ++===+===+===++===+===+===++===+===+===++"
        ]

        impres = [0, 1, 3, 1, 3, 1, 3, 2, 3, 1, 3, 1, 3, 2, 3, 1, 3, 1, 3, 1, 0]
        lin = 0

        for i in range(21):
            if impres[i] < 3:
                print(fil_padrao[impres[i]])
            else:
                # Formata o zero para uma string no formato " "
                linha_exibida = [str(self.grade[lin][col]) if self.grade[lin][col] != 0 else " " for col in range(9)]
                print("{}|| {} | {} |".format(lin + 1, linha_exibida[0], linha_exibida[1]), end="")
                print(" {} || {} | {} |".format(linha_exibida[2], linha_exibida[3], linha_exibida[4]), end="")
                print(" {} || {} | {} |".format(linha_exibida[5], linha_exibida[6], linha_exibida[7]), end="")
                print(" {} || {}".format(linha_exibida[8], lin + 1))
                lin += 1
