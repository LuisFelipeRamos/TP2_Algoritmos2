# Diretrizes

Este arquivo tem o propósito de explicar a organização do projeto.

# Estrutura de Arquivos

O projeto é dividido em cinco arquivos principais, osquais contêm as implementações dos algoritmos propostos no enunciado do trabalho, assim como algumas funções auxiliares úteis para as análises e documentações.

Além disso, existem três diretórios principais, `docs`, `data` e `spec`. `docs` contém este arquivo de diretrizes e uma pasta com um relatório em LaTeX (com um subdiretório para imagens), `data` contêm os conjuntos de dados coletados na internet para a reaização de testes assim como o local de onde foram adquiridos e `spec` contêm a especificação do trabalho.

# Práticas de Código

Na medida do possível, o projeto é fortemente tipado. No mais, valem as seguintes práticas:

- Nomes de módulos devem ser em *snake_case* 
- Nomes de classes devem ser em *PascalCase*
- Nomes de funções devem ser em *snake_case*
- Nomes de variáveis devem ser em *snake_case*

# Dependências

O trabalho faz uso de algumas bibliotecas auxiliares para a implementação dos algoritmos propostos, e para utilizá-los é necessário fazer a instalação desses pacotes em sua máquina. O arquivo `requirements` contêm o nome de todos eles e, para realizar a instalação, use o comando:

`pip install -r requirements`

# Execução

Para executar o código, deve-se estar no diretório raiz do projeto, e utilizar o comando:

`python main.py`

seguido dos parâmetros d elinha de comando, descritos a seguir.

- --dist : Tipo de distância utilizado no cálculo entre os pontos da instância gerada
    - Opções: `euclidean` ou `manhattan`
- --size : Tamanho da instância que deve ser gerada (potência de 2 utilizada)
    - Opções: qualquer valor pode ser passado, mas o trabalho foi feito pensando em valores de 4 a 10
- --alg : Qual algoritmos deve ser utilizado para o cálculo
    - Opções: `branch-and-bound`, `twice-around-the-tree` ou `christofides`

Exemplo de execução:

`python main.py --dist euclidean --size 6 --alg christofides`

## Observações:

O algoritmo de branch-and-bound é exaustivo e provavelmentenão será interessante utilizá-lo com instâncias maiores do que 2⁴. Tente rodar essas instâncias por sua própria cnta e risco.

