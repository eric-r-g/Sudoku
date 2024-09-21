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
Para o modo interativo, é necessário inicializar o arquivo com um parâmetro extra, sendo o nome do arquivo que contém as pistas
```bash
python main.py pistas.txt
```
obs: já fornecemos um modelo pistas, embora o programa não seja restrio a ele

#### opção 2 ( batch):
Para o modo batch, é necessário inicializar o arquivo com dois parâmetros extra sendo eles respectivamente o nome do arquivo que contém as pistas e o nome do arquivo com as ações do modo batch
```bash
python main.py pistas.txt inputbatch.txt
```

#### opção 3 (interface):
Para o modo interface, é necessário inicializar o arquivo com um parâmetro extra escrito "interface"
```bash
python main.py interface
```
obs: o modo interface possui tanto o modo interativo como o batch, porém essa escolha já é feita dentro da interface.
