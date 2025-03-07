# Implémentation d'un processeur dans Logisim

Ce projet implémente un processeur virtuel dans **Logisim**, incluant plusieurs composants essentiels tels que les registres, l'ALU, le décodeur d'instructions, et une pile.

## Description des composants

### 1. Registres
**Entrées :**
- `Write` (1 bit) : Active l'écriture dans les registres.
- `IN` (16 bits) : Information à stocker lorsque `Write` est activé.
- `SR1`, `SR2`, `DR` (3 bits chacun) : Adresses des registres sources et destination.
- `Load` (1 bit) : Charge les 16 bits de poids faible de `MemOUT`.
- `MemOUT` (32 bits) : Information à stocker en cas d'instruction `Load`.
- `Clock`, `Reset`.

**Sorties :**
- Contenu des registres sources (`16 bits` chacun).
- Contenu du registre destination (`16 bits`).

---

### 2. ALU (Unité Arithmétique et Logique)
**Entrées :**
- `SR1`, `SR2` (3 bits chacun) : Adresses des registres contenant les opérandes.
- `Cst` (16 bits) : Valeur d'une constante en cas d'opération immédiate.
- `Imm` (1 bit) : Indique si l'opération utilise une constante.
- `GetOp` (3 bits) : Code de l'opération arithmétique.

**Sortie :**
- `Output` (16 bits) : Résultat de l'opération.

---

### 3. Décodeur d'Instructions (Decode IR)
**Entrée :**
- `RegIR` (32 bits) : Contenu de l'instruction binaire.

**Sorties :**
- `GetOp` (3 bits) : Code de l'opération.
- `Load`, `Store`, `CTRL`, `RET`, `CALL` (1 bit chacun) : Indiquent le type d'instruction.
- `JMPAdress` (16 bits) : Adresse de saut pour les instructions de contrôle.

---

### 4. Gestion des opérations de contrôle
- **CondChecker** : Compare les valeurs et active `Cond` si la condition est remplie.
- **GetAddr** : Gère l'adresse mémoire selon la phase (`Fetch`, `Exec`, `Store`).
- **RegPC** : Incrémente le `PC` ou le modifie en fonction d'un saut (`CALL`, `RET`).
- **Pile** : Gère l'empilement et le dépilement des adresses pour les instructions `CALL` et `RET`.

---

## Assemblage et Simulation
Un script Python a été utilisé pour convertir un code assembleur en binaire compatible avec Logisim. Ce programme permet de tester l'exécution du processeur en simulant différentes instructions.

---

## Exécution dans Logisim
1. Ouvrir Logisim.
2. Charger le fichier du circuit (`.circ`).
3. Exécuter le programme en activant `Clock`.
4. Observer les résultats dans les registres et la mémoire.

---

## Auteurs
- **Abir Hanned **
- **Ashley PADAYODI**
- **Chafae QALLOUJ**
- **Nawal EL KHAL **

Projet réalisé dans le cadre de l'étude des architectures de processeurs.

