# -*- coding: utf-8 -*-
import nltk
import sys
import codecs #permette la gestione di file codificati diversamente
import operator #lascia fare operazioni matematiche
import math #contiene funzione matematiche non supportate da Python

#viene caricato il modello statistico
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

#la funzione prende e restituisce le frasi del testo
def getPhrases(file):
    phrases = tokenizer.tokenize(file)
    return phrases

#la funzione calcola e restituisce il totale della frasi del testo
def getCountPhrases(phrases):
    count = len(phrases)
    return count

#la funzione calcola e restituisce il totale dei tokens
def getTokens(phrases):
    tokenList = []
    for phrase in phrases: #estraggo i token di ogni singola frase grazie a nltk. Con il ciclo for li metto in una lista
        tokenSinglePhrase = nltk.word_tokenize(phrase)
        tokenList+=tokenSinglePhrase
    return tokenList

#la funzione calcola e restituisce il totale dei token
def getCountTokens(token):
    count = len(token)
    return count

#la funzione restituisce la lunghezza media delle frasi in termini di token
def getAverageLenTokens(phrases,token):
    averageTok = token / phrases #totale di token viene diviso con il totale delle frasi
    return averageTok

#la funzione calcola e restituisce il totale dei caratteri
def getCharacters(tokens):
    charactersTot= 0
    for token in tokens: #for calcola il totale di carattere per token e lo aggiunge in una variabile
        characterSingleToken = len(token)
        charactersTot+=characterSingleToken
    return charactersTot

#la funzione calcola e restituisce la lunghezza media delle parole in caratteri
def getAverageLenCharacters(token,caratteri):
    averageChar= caratteri/token #totale di caratteri diviso il totale dei token
    return averageChar

#la funzione calcola e restituisce il totale delle parole tipo all'aumento del corpus per porzioni incrementali di 1000 token
def getVocabulary(tokens,index):
    tokensTot = []
    for tok in range (0,index):
        if tok < index:  #il ciclo for controlla che il totale dei token sia minore di quello dell'index e lo aggiunge ad un elenco
            tokensTot.append(tokens[tok])
    typeWords = set(tokensTot) #la funzione set consente di avere un elenco di elementi diversi che sono in tokensTot
    lenTypeWords = len(typeWords)
    return lenTypeWords

#la funzione prende e restituisce il numero di hapax
def getHapax (tokens):
    hapaxTot = 0
    for tok in tokens: #for considera solo token con frequenza uguale a 1
        freqT = tokens.count(tok)
        if freqT == 1:
            hap = freqT
            hapaxTot += hap
    return hapaxTot

#la funzione calcola e restituisce la distribuzione degli hapax all'aumento del corpus per porzioni incrementali di 1000 token
def getHapaxDistrib(tokens,index):
    v1 = getHapax(tokens) / index
    return v1

#la funzione prende e restituisce la Pos di ciascun token
def getPosTokens(tokenList):
    posT = nltk.pos_tag(tokenList) #la funzione prende la elenco dei token come paramentro e restituisce una lista di bigrammi token, pos
    return posT

#la funzione prende e restituisce il totale dei sostantivi a partire dalla lista di bigrammi token,pos
def getNouns(bigrams):
    nounsList = []
    for pos in bigrams: #for guarda la Pos dei bigrammi e, se coincide con la Pos di un sostantivo, la inserisce nella lista
        if pos[1] in ['NN','NNS','NNP','NNPS']:
            nounsList.append(pos)
    countNouns = len (nounsList)
    return countNouns

#la funzione prende e restituisce il totale dei verbi partendo dalla lista di bigrammi token,pos
def getVerb(bigrams):
    verbs = []
    for pos in bigrams: #for guarda la pos dei bigrammi e, se uguale alla pos di un verbo, la aggiunge alla lista
        if pos[1] in ['VB','VBD','VBG','VBN','VBP','VBZ']:
            verbs.append(pos)
    countVerbs = len(verbs)
    return countVerbs

#la funzione calcola e restituisce il rapporto tra sostantivi e verbi
def getDivision (nouns,verbs):
    divisionNv = nouns / verbs
    return divisionNv

#la funzione prende e restituisce le Pos
def getPosList (bigrams):
    posB = []
    for pos in bigrams: #aggiunge le Pos ad una lista per ciascun bigramma
        posB.append(pos[1])
    return posB

#la funzione calcola e restituisce le 10 Pos maggiormente frequenti
def getFreqPos (pos):
    freqPos = nltk.FreqDist(pos) #distribuzione di frequenza delle Pos
    posFreq = freqPos.most_common(10) #prende le 10 Pos maggiormente comuni
    return posFreq

#la funzione restituisce i bigrammi di Pos
def getPosBigrams (pos):
    posBigrams = nltk.bigrams(pos)
    return list(posBigrams) #la funzione list() rende l'oggetto bigrams un elenco

#la funzione trasforma e restituisce l'elenco dei bigrammi Pos senza ripetizioni
def getSetPosBigrams(pos):
    setPos = set(pos)
    return setPos

#la funzione calcola e restituisce i 10 bigrammi Pos con probabilità condizionata massima
def getProbCondMax(posBigrams,setPos,pos):
    posProb = []
    for posBigr in setPos:
        freqFirstEl = pos.count(posBigr[0]) #calcolo della frequenza del primo elemento della coppia Pos
        freqBigrams = posBigrams.count(posBigr) #calcolo della frequenza del bigramma Pos dall'elenco dei bigrammi senza ripetizioni
        probMax = freqBigrams*1.0/freqFirstEl*1.0 #frequenza del bigramma divisa per la frequenza del primo elemento, entrambi moltiplicati per 1.0 per avere un risultato con la virgola
        tupla = [] #creazione di una lista vuota in cui vengono aggiunti il bigramma Pos e la sua probabilità condizionata
        tupla.append(posBigr)
        tupla.append(probMax)
        tupla = tuple(tupla) #creazione di una tupla
        posProb.append(tupla) #la tupla viene aggiunta alla lista posProb
    posProb.sort(key=operator.itemgetter(1), reverse = True) #la lista viene ordinata per frequenza decrescente
    return posProb[:10] #restituisce la probabilità condizionata massima di 10 bigrammi Pos

#la funzione calcola e restituisce la probabilità di un singolo elemento
def getProbSingleElement (pos,posList):
    freqAss = posList.count(pos) #conta la frequenza assoluta di ciascun Pos
    freqRelativa = (freqAss*1.0) / (len(posList)*1.0) #divido la frequenza assoluta per il corpus e calcolo la probabilità
    return freqRelativa

#la funzione calcola e restituisce la probabilità congiunta
def getProbabilityCong(bigram,posListBigrams,tokens):
    freqAssBigram = posListBigrams.count(bigram) #calcolo della frequenza assoluta del bigramma
    freqRelBigram = (freqAssBigram*1.0) / (len(tokens)*1.0) #calcolo della probabilità del bigramma
    return freqRelBigram

#la funzione calcola e restituisce i 10 Pos con Local Mutual Information massima
def getLMI(posListBigrams,posList,posSetBigrams):
    posLMI = []
    for posBigr in posSetBigrams:
        freqAssBigram = posListBigrams.count(posBigr) #calcolo della frequenza assoluta del bigramma Pos
        probFirstElem = getProbSingleElement(posBigr[0],posList) #calcolo della probabilità del primo elemento del bigramma
        probSecondElem = getProbSingleElement(posBigr[1],posList) #calcolo della probabilità del secondo elemento del bigramma
        probCong = getProbabilityCong(posBigr,posListBigrams,posList) #calcolo della probabilità congiunta del bigramma
        MI = math.log(probCong/(probFirstElem*probSecondElem)) #calcolo la Mutual Information
        LMI = (freqAssBigram) * (MI) #calcolo della Local Mutual Information
        tupla = []
        tupla.append(posBigr)
        tupla.append(LMI)
        tupla = tuple(tupla)
        posLMI.append(tupla) #creazione di una tipla di bigramma Pos e LMI
    posLMI.sort(key=operator.itemgetter(1), reverse = True) #la lista viene ordinata in frequenza decrescente
    return posLMI[:10] #restituisce i 10 Pos con LMI massima




def main(file1,file2):

    print ("\nStudente: Camilla Zucchi, Matricola: 490366\n")
    print ("\nPrimo libro: The Canterville Ghost by Oscar Wilde\n")
    print ("\nSecondo libro: The Happy Prince and Other Tales by Oscar Wilde\n")       
    #I file ricevuti in input dal programma vengono aperti
    fileInput1= codecs.open(file1,"r","utf-8")
    fileInput2= codecs.open(file2,"r","utf-8")

    #I due file vengono letti
    fileRead1 = fileInput1.read()
    fileRead2 = fileInput2.read()

    #1: Numero totale di frasi e token per ogni libro
    phrasesFile1 = getPhrases(fileRead1) #funzione per avere le frasi del primo libro
    phrasesFile2 = getPhrases(fileRead2) #funzione per avere le frasi del secondo libro
    countPhrasesFile1 = getCountPhrases(phrasesFile1) #funzione per avere il totale delle frasi del primo libro
    countPhrasesFile2 = getCountPhrases(phrasesFile2) #funzione per avere il totale delle frasi del secondo libro
    print ("\n\n-Il totale di frasi:")
    print ("\nPrimo libro: ", countPhrasesFile1)
    print ("\nSecondo libro: ", countPhrasesFile2)

    tokensFile1 = getTokens(phrasesFile1) #funzione per avere i token del primo libro
    tokensFile2 = getTokens(phrasesFile2) #funzione per avere i token del secondo libro
    countTokensFile1 = getCountTokens(tokensFile1) #funzione per avere i token del primo libro
    countTokensFile2 = getCountTokens(tokensFile2) #funzione per avere i token del secondo libro
    print("\n\n-Il totale di token: ")
    print("\nPrimo libro: ", countTokensFile1)
    print("\nSecondo libro: ", countTokensFile2)

    #2: Lunghezza media delle frasi in termini di token e lunghezza media delle parole in termini di caratteri
    AverageLenTokensFile1 = getAverageLenTokens(countPhrasesFile1,countTokensFile1) #funzione per avere la lunghezza media delle frasi del primo libro in termini di token
    AverageLenTokensFile2 = getAverageLenTokens(countPhrasesFile2, countTokensFile2) #funzione per avere la lunghezza media delle frasi del secondo libro in termini di token
    print("\n\n-La lunghezza media delle frasi in termini di token: ")
    print("\nPrimo libro: ", AverageLenTokensFile1)
    print("\nSecondo libro: ", AverageLenTokensFile2)

    characters1 = getCharacters(tokensFile1) #funzione per avere il numero dei caratteri del primo libro
    characters2 = getCharacters(tokensFile2) #funzione per avere il numero dei caratteri del secondo libro
    averageLenChar1 = getAverageLenCharacters(countTokensFile1, characters1) #funzione per avere la lunghezza media dei token del primo libro in termini di caratteri
    averageLenChar2 = getAverageLenCharacters(countTokensFile2, characters2) #funzione per avere la lunghezza media dei token del secondo libro in termini di caratteri
    print ("\n\n-La lunghezza media delle parole in termini di caratteri: ")
    print ("\nPrimo libro: ", averageLenChar1)
    print ("\nSecondo libro: ", averageLenChar2)


    #3a: la grandezza del vocabolario all'aumentare del corpus per porzioni incrementale di 1000 token
    print ("\n\n-La grandezza del vocabolario: ")
    for tok in range (1000,13552,1000): #intervalli di token considerati
        lenVocabularyFile1 = getVocabulary(tokensFile1,tok) #funzione per avere la lunghezza del vocabolario del primo libro
        print ("\nNumero di parole tipo del primo libro in ", tok, "tokens: ", lenVocabularyFile1)
        lenVocabularyFile2 = getVocabulary(tokensFile2,tok) #funzione per avere la lunghezza del vocabolario del secondo libro
        print ("\nNumero di parole tipo del secondo libro in ", tok, "tokens: ", lenVocabularyFile2)

    #3b: la distribuzione degli hapax all'aumentare del corpus per porzioni incrementali di 1000 token
    print("\n\n-La distribuzione degli hapax: ")
    for hapax in range(1000,13552,1000): #intervalli di token considerati
        hapaxDistrFile1 = getHapaxDistrib(tokensFile1,hapax) #funzione per avere la distribuzione degli hapax nel primo libro
        print ("\nPrimo libro in ", hapax, "tokens: ",hapaxDistrFile1)
        hapaxDistrFile2 = getHapaxDistrib(tokensFile2,hapax) #funzione per avere la distribuzione degli hapax nel secondo libro
        print ("\nSecondo libro in ", hapax, "tokens: ", hapaxDistrFile2)
        
    #4: rapporto tra sostantivi e verbi
    posTokenFile1 = getPosTokens(tokensFile1) #funzione per avere la Pos dei token del primo libro
    nounFile1 = getNouns(posTokenFile1) #funzione per avere il numero delle Pos equivalente ai sostantivi
    verbsFile1 = getVerb(posTokenFile1) #funzione per avere il numero delle Pos equivalente ai verbi
    divisionSv1 = getDivision(nounFile1,verbsFile1)
    print ("\n\n-Il rapporto tra sostantivi e verbi: ")
    print("\nPrimo libro: ", divisionSv1)
    posTokenFile2 = getPosTokens(tokensFile2) #funzione per avere la Pos dei token del secondo libro
    nounFile2 = getNouns(posTokenFile2) #funzione per avere il numero delle Pos equivalente ai sostantivi
    verbsFile2 = getVerb(posTokenFile2) #funzione per avere il numero delle pos equivalente ai verbi
    divisionSv2 = getDivision(nounFile2,verbsFile2)
    print("\nSecondo libro: ",divisionSv2)

    #5: le 10 PoS più frequenti
    posListFile1 = getPosList(posTokenFile1) #funzione per avere la lista delle Pos del primo libro
    freqPosFile1 = getFreqPos(posListFile1) #funzione per avere le 10 Pos più frequenti nel primo libro
    print ("\n\n-Le 10 Pos più frequenti nel primo libro sono: ")
    for element in freqPosFile1: #prendo in considerazione ogni elemento del bigramma
        print("\nPos: ", element[0], "con frequenza: ", element[1]) #stampo la Pos e la loro frequenza

    posListFile2 = getPosList(posTokenFile2) #funzione per avere la lista delle Pos nel secondo libro
    freqPosFile2 = getFreqPos(posListFile2) #funzione per avere la le 10 Pos più frequenti nel secondo libro
    print("\n\n-Le 10 Pos più frequenti del secondo libro sono: ")
    for element in freqPosFile2: #prendo in considerazione ogni elemento del bigramma
        print("\nPos: ", element[0], " con frequenza: ", element[1]) #stampo la Pos e la sua frequenza

    #6a: Estrazione e ordinamento dei 10 bigrammi di Pos con probabilità condizionata massima
    posBigramsFile1 = getPosBigrams (posListFile1) #funzione per avere la lista dei bigrammi Pos del primo libro
    posSetBigramsFile1 = getSetPosBigrams (posBigramsFile1) #funzione per avere la lista dei bigrammi Pos senza ripetizioni del primo libro
    posProbCondMaxFile1 = getProbCondMax (posBigramsFile1,posSetBigramsFile1,posListFile1) #funzione per il calcolo della probabilità condizionata massima
    print ("\n\n-I 10 bigrammi di Pos del primo libro con probabilità condizionata massima sono: ")
    for element in posProbCondMaxFile1: #prendo in considerazione ogni elemento del bigramma
        print("\nBigramma Pos: ", element[0], "con probabilità condizionata: ", element[1]) #stampo la Pos e la sua frequenza

    posBigramsFile2 = getPosBigrams (posListFile2) #funzione per avere la lista dei bigrammi Pos del secondo libro
    posSetBigramsFile2 = getSetPosBigrams (posBigramsFile2) #funzione per avere la lista dei bigrammi Pos senza ripetizioni del secondo libro
    posProbCondMaxFile2 = getProbCondMax (posBigramsFile2, posSetBigramsFile2, posListFile2) #funzione per calcolare la probabilità condizionata massima
    print ("\n\n-I 10 bigrammi di Pos del secondo libro con probabilità condizionata massima sono: ")
    for element in posProbCondMaxFile2: #prendo in considerazione ogni elemento del bigramma
        print("\nBigramma Pos: ", element[0], "con probabilità condizionata: ", element[1]) #stampo i bigrammi Pos e la loro probabilità condizionata


    #6b: Estrazione e ordinamento dei 10 bigrammi di Pos con forza associativa massima
    LMIFile1 = getLMI(posBigramsFile1,posListFile1,posSetBigramsFile1) #funzione per ottenere la LMI massima dei 10 bigrammi di Pos del primo libro
    print ("\n\n-I 10 bigrammi di Pos del primo libro con LMI massima sono: ")
    for element in LMIFile1: #prendo in considerazione ogni elemento del bigramma
        print("\nBigramma Pos: ", element[0]," con LMI: ", element[1]) #stampo i bigrammi Pos e la loro LMI massima

    LMIFile2 = getLMI(posBigramsFile2,posListFile2,posSetBigramsFile2) #funzione per avere la LMI massima dei 10 bigrammi di Pos del secondo libro
    print("\n\n-I 10 bigrammi di Pos del secondo libro con LMI massima sono: ")
    for element in LMIFile2: #prendo in considerazione ogni elemento del bigramma
        print("\nBigramma Pos: ", element[0], "con LMI: ", element[1]) #stampo i bigrammi Pos e la loro LMI massima

main(sys.argv[1],sys.argv[2])        
