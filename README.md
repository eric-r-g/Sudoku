# JOGO_SUDOKU

Um jogo sudoku, com modos tanto interativo quanto batch, além de possui uma interface própria

## Estrutura do projeto
- **SUDOKU básico**: modelo padrão do sudoku, cumprindo os requisitos básicos do que foi pedido
- **INTERFACE**: arquivo extra utilizando a biblioteca tkinter para a construção de uma interface

## SUDOKU básico

o projeto foi seperado em 3 arquivos sendo eles o main, a classe e a validação:
- main: contêm o escopo principal do código, desde a inicialização, a seleção de modos, etc
- classe: contêm a classe da grade, alé de definir funções que interagem diretamente com ela
- validação: contêm as funções relacionadas diretamente ao sistema de erro do Sudoku

## INTERFACE

a interface foi construida em cima da base, adaptando as funções para o modelo que o Tkinter
segue, não sendo separado em sub-arquivos. 

## Como executar o projeto

## Sudoku

#### opção 1 (interativo):
1. inicialize o arquivo já na pasta devida
```bash
python main.py pistas.txt
```
obs: fornecemos um modelo de pistas já padrão, porém pode ser substituido de acordo com sua escolha 

2. a partir dai, você estará no modo interativo

