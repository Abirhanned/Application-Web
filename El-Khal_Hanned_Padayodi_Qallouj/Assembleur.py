"""
Nom du programme : assembleur.py

Description      : Programme permettant de traduire un code assembleur en un code
                   machine (compréhensible par la mémoire d'un processeur virtuel)

Date             : 08/12/2024
"""


# Table de correspondance entre instructions assembleur et codes binaires
instruction_table = {
    "ADD": "000", "ADDi": "000", "SUB": "001", "SUBi": "001", "AND": "010",
    "ANDi": "010", "OR": "011", "ORi": "011", "XOR": "100", "XORi": "100",
    "SL": "101", "SLi": "101", "SR": "110", "SRi": "110", "MUL": "111",
    "MUL": "111", "LD": "000", "STR": "001", "JMP": "000", "JEQU": "001",
    "JNEQ": "010", "JSUP": "011", "JINF": "100", "RET": "101", "CALL": "110",
    "HALT": "111", "ADDi": "000", "SUBi": "001", "ANDi": "010", "ORi": "011",
    "XORi": "100", "SLi": "101", "SRi": "110", "MULi": "111"
}


# Dictionnaire des registres

registers = {
    "R0": "000", "R1": "001", "R2": "010", "R3": "011",
    "R4": "100", "R5": "101", "R6": "110", "R7": "111"
}


# Labels pour les sauts

labels = {}



# ------------------------------ FONCTIONS ----------------------------------- #


# Fonction pour convertir un entier en binaire sur 16 bits

def int_to_bin16(value):
    return format(value if value >= 0 else (1 << 16) + value, "016b")


# Fonction pour traduire une instruction assembleur en binaire

def parse_instruction(instruction):

    parts = instruction.split()

    if len(parts) == 0:
        return ""  # Retourner une chaîne vide pour les lignes vides ou les commentaires

    op = parts[0]
    binary = ""

    # -Opérations arithmétiques-

        # -Immédiates-

    if op in ["ADDi", "SUBi", "ANDi", "ORi", "XORi", "SLi", "SRi", "MULi"]:
        dr = registers[parts[1].strip(',')]  # Enlève la virgule
        r = registers[parts[2].strip(',')]
        immediate = int_to_bin16(int(parts[3]))

        binary_for_ram = immediate + "0000" + r + dr + "1" + instruction_table[op] + "00"

        # -Non immédiates-

    elif op in ["ADD", "SUB", "AND", "OR", "XOR", "SL", "SR", "MUL"]:
        dr = registers[parts[1].strip(',')]
        r1 = registers[parts[2].strip(',')]
        r2 = registers[parts[3].strip(',')]

        binary_for_ram = "0"*17 + r2 + r1 + dr + "0" + instruction_table[op] + "00"

    # -Opérations de mémoire-

    elif op in ["LD", "STR"]:
        r = registers[parts[1].strip(',')]
        adress = registers[parts[2].strip(',')]
        binary_for_ram = 20*"0" + adress + r + "0" + instruction_table[op] + "01"

    # -Opérations de contrôle-

    elif op == "JMP" or op == "CALL":
        label = parts[1]

        binary_for_ram = str(int_to_bin16(labels[label])) + 11*"0" + instruction_table[op] + "11"

    elif op in ["JEQU", "JNEQ", "JSUP", "JINF"]:
        r1 = registers[parts[1].strip(',')]
        r2 = registers[parts[2].strip(',')]
        label = parts[3]

        binary_for_ram = str(int_to_bin16(labels[label])) + "0" + r2 + r1 + "0000" + instruction_table[op] + "11"

    elif op == "RET":
        binary_for_ram = 27*"0" + instruction_table[op] + "11"

    elif op == "HALT":  # Gérer l'instruction HALT
        binary_for_ram = 32*"0" + instruction_table[op] + "00"

    else:
        raise ValueError(f"Instruction inconnue : {instruction}")

    return binary_for_ram



# Fonction pour lire le fichier, gérer les labels et convertir les instructions

def assemble_to_binary(input_file, output_file):

    # Étape 1 : Lire toutes les lignes et enregistrer les labels

    with open(input_file, "r") as infile:
        lines = infile.readlines()

    current_line = 0

    for line in lines:
        line = line.strip()

        if not line or line.startswith(";"):  # Gérer les commentaires
            continue

        if ":" in line:  # Si un label est trouvé
            label = (line.split(":")[0]).strip()
            labels[label] = current_line  # Ajout du label avec la valeur de son adresse dans le dictionnaire 'labels'

        else:
            current_line += 1

    # Étape 2 : Traduire chaque ligne en binaire

    with open(output_file, "w") as outfile:

        outfile.write("v2.0 raw\n")  # Avoir un format compréhensible pour la RAM

        current_line = 0

        for line in lines:

            if not line or line.startswith(";"):
                continue

            if ":" in line:  # Si un label est trouvé
                parts = line.split(":")
                # Si une instruction suit le label, la traiter
                if len(parts) > 1:
                    line = parts[1].strip()

            else:
                line = line.strip()

            try:
                binary = parse_instruction(line)
                hex_code = "".join([f"{int(binary[i:i+8], 2):02X}" for i in range(0, len(binary), 8)])  # Convertion d'une chaîne binaire en une chaîne hexadécimale
                outfile.write(hex_code + "\n")
                current_line += 1

            except ValueError as e:
                print(f"Erreur à la ligne {current_line + 1} : {e}")

    print("Programme exécuté avec succès ! Le fichier de sortie 'binaryLogisim.txt' a bien été généré.")


# --------------------------- PROGRAMME PRINCIPAL ---------------------------- #

assemble_to_binary("assembly.txt", "binaryLogisim.txt")
