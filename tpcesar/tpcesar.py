# http://veron.univ-tln.fr/ENSEIGNEMENT/M2/TP/CESAR/tpcesar.pdf

alphabet = "abcdefghijklmnopqrstuvwxyz"

def cesar_chiffre(inp, out, k):
    global alphabet
    inFile = open(inp, "r")
    outFile = open(out, "w")
    content = list(inFile.readline().lower())
    while(content != []):
        i = 0
        content = suppr_accent(content)
        while(i < len(content)):
            if(content[i] in alphabet):
                numLettre = alphabet.index(content[i])
                nvlLettre = (numLettre + k)%26
                content[i] = alphabet[nvlLettre]
            i += 1
        chaine = ''.join(content)
        outFile.write(chaine)
        content = list(inFile.readline().lower())
    outFile.close()
    inFile.close()

def cesar_dechiffre(inp, out, k):
    global alphabet
    inFile = open(inp, "r")
    outFile = open(out, "w")
    content = list(inFile.readline().lower())
    while(content != []):
        i = 0
        content = suppr_accent(content)
        while(i < len(content)):
            if(content[i] in alphabet):
                numLettre = alphabet.index(content[i])
                nvlLettre = (numLettre - k)%26
                content[i] = alphabet[nvlLettre]
            i += 1
        chaine = ''.join(content)
        outFile.write(chaine)
        content = list(inFile.readline().lower())
    outFile.close()
    inFile.close()

def suppr_accent(content):
    n = len(content)
    i = 0
    while(i < n):
        if content[i] == "é" or content[i] == "è" or content[i] == "ê":
            content[i] = "e"
        elif content[i] == "à":
            content[i] = "a"
        elif content[i] == "ù":
            content[i] = "u"
        i += 1
    return content


def cesar_cryptanalyse(inp):
    global alphabet
    inFile = open(inp, "r")
    dico = {}
    for i in alphabet:
        dico[i] = 0
    content = list(inFile.readline().lower())
    while(content != []):
        content = suppr_accent(content)
        for i in content:
            if i in alphabet:
                dico[i] += 1
        content = list(inFile.readline().lower())
    nbOccur = 0
    maxOccur = ''
    for i in dico.items():
        if i[1] > nbOccur:
            maxOccur = i[0]
            nbOccur = i[1]
    E_crypte = alphabet.index(maxOccur)
    # print(maxOccur)
    clePossible = (E_crypte - 4)%26
    inFile.close()
    return clePossible, dico


def vigenere_chiffre(inp, out, cle):
    global alphabet
    inFile = open(inp, "r")
    outFile = open(out, "w")
    content = list(inFile.readline().lower())
    while(content != []):
        i = 0
        content = suppr_accent(content)
        while(i < len(content)):
            if(content[i] in alphabet):
                numLettre = alphabet.index(content[i])
                nvlLettre = (numLettre + alphabet.index(cle[i%len(cle)]))%26
                content[i] = alphabet[nvlLettre]
            i += 1
        chaine = ''.join(content)
        outFile.write(chaine)
        content = list(inFile.readline().lower())
    outFile.close()
    inFile.close()


def vigenere_dechiffre(inp, out, cle):
        global alphabet
        inFile = open(inp, "r")
        outFile = open(out, "w")
        content = list(inFile.readline().lower())
        while(content != []):
            i = 0
            content = suppr_accent(content)
            while(i < len(content)):
                if(content[i] in alphabet):
                    numLettre = alphabet.index(content[i])
                    nvlLettre = (numLettre - alphabet.index(cle[i%len(cle)]))%26
                    content[i] = alphabet[nvlLettre]
                i += 1
            chaine = ''.join(content)
            outFile.write(chaine)
            content = list(inFile.readline().lower())
        outFile.close()
        inFile.close()


def longueur_vigenere(inp):
    inFile = open(inp, "r")
    content = inFile.readlines()
    ch = ""
    for string in content:
        ch += string.replace('\n', '')
    dico = {}
    trigrammes = []
    i = 0
    while(i < len(ch)):
        trigrammes += [ch[i:i+3]]
        i += 1
    print(ch)
    for n in trigrammes:
        if(len(n) == 3):
            if n in dico.keys():
                dico[n] += 1
            else:
                dico[n] = 1
    maxOccur = ''
    nbOccur = 0
    for i in dico.items():
        if i[1] > nbOccur:
            maxOccur = i[0]
            nbOccur = i[1]
    inFile.close()
    return maxOccur


if __name__ == '__main__':
    cesar_chiffre("entree.txt", "sortie.txt", 4)
    cesar_dechiffre("sortie.txt", "sortieTest.txt", 4)
    d = cesar_cryptanalyse("sortie.txt")
    print(d)
    # vigenere_chiffre("entree.txt", "sortie.txt", "cle")
    # vigenere_dechiffre("sortie.txt", "sortieTest.txt", "cle")
    # print(longueur_vigenere("cryptogrammeFourni"))
