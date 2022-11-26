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


