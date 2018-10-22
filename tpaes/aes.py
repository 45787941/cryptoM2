# -*- coding: utf-8 -*-
# http://veron.univ-tln.fr/ENSEIGNEMENT/M2/TP/AES/tpaes.pdf
def transforme(W):
# tranforme le tableau des cl'es interm'ediaires
# repr'esent'e par 44 colonnes de taille 4 par une liste L
# compos'e de 4 sous-listes de taille 44.
	L=[0]*4
	for i in range(4):
		L[i] = [0]*44
		for j in range(44):
			L[i][j] = W[j][i]
	return L

def tohex(n):
# retourne la repr'esentation hexad'ecimale
# sur 2 chiffres d'un entier < 256
	if n < 16:
		return '0'+hex(n)[-1]
	else:
		return hex(n)[2:]

def affiche(L):
# pour afficher les Ã©tats
	print(list(map(tohex,L[0])))
	print(list(map(tohex,L[1])))
	print(list(map(tohex,L[2])))
	print(list(map(tohex,L[3])))
	print()

def convert_to_state(message):
    # renvoie un message ou une cl'e sous forme d''etat
	state = [0]*4
	for i in range(0,4):
		state[i] = []
	i = 0
	j = 0
	while(i < len(message)):
		state[j].append(ord(message[i]))
		i += 1
		j += 1
		if(i%4 == 0):
			j = 0
	return state

def multbyalpha(x):
	# A COMPLETER, RENVOIE y = alpha * x dans le corps F_2^8
    y = x << 1
    if(y & ( 1 << 8 )):
        y = y ^ polynome
    return y

def multbygen(x):
# pour l'AES alpha+1 est un gÃ©nÃ©rateur
# cette fonction renvoie y = x * (alpha+1)
    y = multbyalpha(x)
    y ^= x
    return y

def mult(a,b):
# renvoie l'Ã©lÃ©ment y = a*b dans F_2^8
# en se servant de la table des log en base g
# o'u g est le g'en'erateur de F_2^8
    if (a == 0) or (b == 0):
        return 0
	# A COMPLETER
    y = gen[(log_gen[a] + log_gen[b])%255]
    return y

def construit_F_2_8():
# le corps est construit en
# en utilisant le fait que alpha+1
# est un generateur
	table = [1]
	log_t = [0]*256
	log_t[1] = 0
	for i in range(1,256):
		aux = multbygen(table[i-1])
		table = table + [aux]
		log_t[aux] = i
	return table, log_t

def inv(x):
# renvoie y = x^(-1) dans F_2^8
# en se servant de la table des log en base g
    y = gen[255 - (log_gen[x])]
    return y

def S(x):
# code de la boite S
	if x == 0:
		y = 0
	else:
		y = inv(x)
	result = 0
	# A COMPLETER (multiplication matricielle dans F_2)
	yb = list(bin(y)[2:].zfill(8))
	for i in range(0,8):
		yb[i] = int(yb[i])
	yb.reverse()
	g = []
	g.append(yb[0] ^ yb[4] ^ yb[5] ^ yb[6] ^ yb[7] ^ 1)
	g.append(yb[0] ^ yb[1] ^ yb[5] ^ yb[6] ^ yb[7] ^ 1)
	g.append(yb[0] ^ yb[1] ^ yb[2] ^ yb[6] ^ yb[7] ^ 0)
	g.append(yb[0] ^ yb[1] ^ yb[2] ^ yb[3] ^ yb[7] ^ 0)
	g.append(yb[0] ^ yb[1] ^ yb[2] ^ yb[3] ^ yb[4] ^ 0)
	g.append(yb[1] ^ yb[2] ^ yb[3] ^ yb[4] ^ yb[5] ^ 1)
	g.append(yb[2] ^ yb[3] ^ yb[4] ^ yb[5] ^ yb[6] ^ 1)
	g.append(yb[3] ^ yb[4] ^ yb[5] ^ yb[6] ^ yb[7] ^ 0)

	for i in range(0,8):
		result += g[i]*pow(2,i)
	return result

def gen_cles(k):
	RC = [0,1]
	for i in range(2,11):
		RC = RC + [multbyalpha(RC[i-1])]
	W_ = [0]*44
	for i in range(44):
		W_[i] = [0]*4
	cle_convert = convert_to_state(k)
	for j in range(4):
		for i in range(4):
			W_[i][j] = cle_convert[j][i]
	for i in range(4,44):
		temp = W_[i-1]
		if (i % 4) == 0 :
			temp = list(map(S,temp[1:]+[temp[0]]))
			temp[0] ^= RC[i//4]
		for j in range(4):
			W_[i][j] = W_[i-4][j] ^ temp[j]
	return transforme(W_)


def SubBytes(etat):
	# renvoie dans state le tableau etat
	# aprÃ¨s application de la transformation S
	state = [0]*4
	for i in range(0,4):
		state[i] = []
	for i in range(0, 4):
		for j in range(0, 4):
			state[i].append(S(etat[i][j]))
	return state

def ShiftRows(etat):
# renvoie dans state le tableau etat
# aprÃ¨s application de la transformation ShiftRows
	state = [0]*4
	for i in range(0,4):
		state[i] = []
	for i in range(0,4):
		for j in range(0,4):
			state[i].append(etat[i][(j+i)%4])
	return state

def MixColumns(etat):
# renvoie dans state le tableau etat
# apr'es application de la transformation MixColumns
# cette tranformation revient 'a multiplier chaque colonne
# de etat par la matrice mix_column
# attention il s'agit d'une multiplication dans F_2^8.
# Chaque 'el'ement de la matrice est un 'el'ement de F_2^8
# et chaque colonne de etat est consid'er'e comme un vecteur
# de F_2^8, voir section 4.2.3 page 12 de aes-standard.pdf
# et le transparent 7 de aes-exemple.pdf
	state = [0]*4
	for i in range(0, 4):
		state[i] = []
	for i in range(0,4):
		for j in range(0,4):
			val = 0
			for k in range(0,4):
				val ^= mult(matrix_mix_columns[i][k], etat[k][j])
			state[i].append(val)
	return state

def AddRoundKey(etat,tour):
	state = []
	K = [0,0,0,0]
	for i in range(4):
		K[i] = W[i][4*tour:4*(tour+1)]
	for i in range(4):
		aux = []
		for j in range(4):
			aux = aux + [etat[i][j] ^ K[i][j]]
		state = state + [aux]
	return state

polynome = 0b100011011
# polynome x^8+x^4+x^3+x+1 pour generer F_2^8
# il n'est pas primitif
# donc alpha sa racine n'est pas un generateur
# par contre on peut montrer que alpha+1 esr un generateur
c = 0b01100011 # constante pour la cr'eation des cl'es de tour
# l'op'eration mixcolumns coorespond 'a une multiplication matricielle
# attention la matrice ci-dessous est constitu'ee d''elements de F_2^8
# elle correspond a la matrice :
# |alpha		alpha+1		1			1		|
# |1			alpha		alpha+1		1		|
# |1			1			alpha		alpha+1	|
# |alpha+1		1			1			alpha	|

matrix_mix_columns = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
gen, log_gen = construit_F_2_8()

#clair = "Ceci est un texte"
#cle =   "Ceci est une clef"

cle = "Thats my Kung Fu"
clair = "Two One Nine Two"

W = gen_cles(cle)
etat=convert_to_state(clair)

if __name__ == "__main__":
	affiche(etat)

	print(multbyalpha(2))
	print(multbyalpha(128))
	print(multbyalpha(253))

	print("\n")

	print(multbygen(2))
	print(multbygen(128))
	print(multbygen(253))

	print("\n")

	print(mult(2, 64))
	print(mult(128, 2))
	print(mult(253, 4))

	# print(gen)
	# print(log_gen)

	print("\n")

	print(inv(2))
	print(inv(128))
	print(inv(253))

	print(S(0))
	print("\n")

	# Deroulement de l'AES
	etat=AddRoundKey(etat,0)
	# affiche(etat)
	for i in range(1,10):
		etat = SubBytes(etat)
		etat = ShiftRows(etat)
		etat = MixColumns(etat)
		etat = AddRoundKey(etat,i)
	etat = SubBytes(etat)
	etat = ShiftRows(etat)
	etat = AddRoundKey(etat,10)
	# affichage du cryptogramme
	affiche(etat)
