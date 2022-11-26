from instance_generator import generate_tsp_instance
from branch_and_bound import branch_and_bound_tsp
from twice_around_the_tree import twice_around_the_tree
from christofides import christofides
import utils

import argparse

parser = argparse.ArgumentParser(description="nao sei oq por na descirçao")
parser.add_argument("--dist", dest = "dist", type = str, help = "Tipo de distância utilizado entre os pontos da instância gerada")
parser.add_argument("--size", dest = "size", type = int, help = "Tamanho da instância que deve ser gerada")
parser.add_argument("--alg", dest = "alg", type = str, help = "Qual algoritmos deve ser utilizado para o cálculo")

ARGUMENTS = parser.parse_args()

def main():
    print("oi")

if __name__ == "__main__":
    main()