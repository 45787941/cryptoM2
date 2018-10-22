# -*- coding: utf-8 -*-
import aes
matrix_mix_columnsInv = [[0xe,0xb,0xd,0x9],[0x9,0xe,0xb,0xd],[0xd,0x9,0xe,0xb],[0xb,0xd,0x9,0xe]]

def ShiftRowsInv(etat):
# renvoie dans state le tableau etat
# aprÃ¨s application de la transformation ShiftRows
	state = [0]*4
	for i in range(0,4):
		state[i] = []
	for i in range(0,4):
		for j in range(0,4):
			state[i].append(etat[i][(j-i)%4])
	return state

def MixColumnsInv(etat):
	state = [0]*4
	for i in range(0, 4):
		state[i] = []
	for i in range(0,4):
		for j in range(0,4):
			val = 0
			for k in range(0,4):
				val ^= aes.mult(matrix_mix_columnsInv[i][k], etat[k][j])
			state[i].append(val)
	return state

def Sinv():
    invS = [0]* 256
    for i in range(0, 256):
        var = aes.S(i)
        invS[var] = i
    return invS

def SubBytesInv(etat):
	# renvoie dans state le tableau etat
	# aprÃ¨s application de la transformation S
	state = [0]*4
	for i in range(0,4):
		state[i] = []
	for i in range(0, 4):
		for j in range(0, 4):
			state[i].append(inverseS[etat[i][j]])
	return state

def convert_to_clair(state):
    clair = ''
    for i in range(0,4):
        for j in range(0,4):
            clair += chr(state[j][i])
    return clair

if __name__ == '__main__':
    # TESTS FCT
    # test = aes.MixColumns(matrix_mix_columnsInv)
    # aes.affiche(test)
    inverseS = Sinv()
    # print(inverseS)

    print("Matrice cryptee")
    etat = [[41, 87, 64, 26], [195, 20, 34, 2], [80, 32, 153, 215], [95, 246, 179, 58]]
    aes.affiche(etat)
    # aes.affiche(etat)
	# Deroulement de l'AES
    etat=aes.AddRoundKey(etat,10)
    etat = ShiftRowsInv(etat)
    etat = SubBytesInv(etat)
    # affiche(etat)
    for i in range(1,10):
        etat = aes.AddRoundKey(etat,10-i)
        etat = MixColumnsInv(etat)
        etat = SubBytesInv(etat)
        etat = ShiftRowsInv(etat)
    etat = aes.AddRoundKey(etat,0)
	# affichage du cryptogramme
    print("matrice decryptee")
    aes.affiche(etat)
    print(convert_to_clair(etat))
