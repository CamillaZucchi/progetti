# -*- coding: utf-8 -*-
import nltk
import sys
import codecs 
import re #permette il trattamento delle espressioni regolari

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

#la funzione prende e restituisce le frasi del testo
def getPhrases(file):
    phrases = tokenizer.tokenize(file)
    return phrases

#la funzione calcola e restituisce il totale di tokens del testo
def getTokens(phrases):
    tokenList = []
    for phrase in phrases: #estraggo i token di tutte le frasi mediante la funzione di nltk; col cilo for, i token di frase vengono messi in una lista
        tokenSinglePhrase = nltk.word_tokenize(phrase)
        tokenList+=tokenSinglePhrase
    return tokenList

#la funzione prende e restituisce le Pos di ogni token
def getPosTokens(tokenList):
    posT = nltk.pos_tag(tokenList) #prende in input la lista dei token e restituisce un elenco di coppie (token,Pos)
    return posT

#la funzione prende e restituisce il testo rappresentato come un albero
def getTree (posToken):
    analisi = nltk.ne_chunk(posToken) #prende in input la lista di bigrammi token,Pos 
    return analisi

#la funzione estrae e restituisce la lista di entità "PERSON"
def getPerson(phrases):
    tokens = getTokens(phrases) #ho i token
    bigrams = getPosTokens(tokens) #ho i bigrammi(token,Pos)
    tree = getTree(bigrams) #ho l'albero
    personList = [] #lista vuota
    for node in tree: #analizzo l'albero nodo per nodo
        NE = ''
        if hasattr(node,'label'): #verifico se node è nodo intermedio o foglia
            if node.label() in ["PERSON"]: #estrae e verifica che l'etichetta sia PERSON
                for partNE in node.leaves(): #ciclo le foglie
                    if NE != '': #controllo i nomi formati da più parole
                        NE = NE + '' + partNE[0]
                    else:
                        NE = partNE[0]
                    personList.append(NE) #aggiungo all'elenco il nome proprio trovato
    return personList

#la funzione prende e restituisce i 10 nomi propri di persona più frequenti
def getFreqPerson(personList):
    freqList = nltk.FreqDist(personList) #la funzione permette di calcolare la distribuzione di frequenza degli elementi all'interno di una lista
    person10 = freqList.most_common(10)
    return person10

#la funzione prende e restituisce bigrammi formati dal nome proprio e dalle frasi che lo contengono
def getPhrasePerson (phrases,person):
    phraseList = []
    for phrase in phrases: #ciclo tutte le frasi dove controllo che sia presente la persona: se presente, la inserisco nella lista
        if person in phrase:
            phraseList.append(phrase)
    phraseList = tuple(phraseList) #creo una tupla
    bigram = [person,phraseList]
    return bigram

#la funzione prende e restituisce la frase più lunga
def getPhraseLonger(phrases):
    phraseLength = 0
    phraseMax = ""
    for phrase in phrases: #ciclo le frasi alla ricerca di quella più lunga
        token = nltk.word_tokenize(phrase)
        if len(token) > phraseLength: #verifico che la lunghezza della frase sia maggiore di quella della variabile, inizialmente uguale a 0
            phraseLength = len(token) #se maggiore, assegno la lunghezza della frase trovata alla variabile che mi indica la massima lunghezza
            phraseMax = phrase #metto la frase più lunga in una variabile
    return phraseMax

#la funzione prende e restituisce la frase più corta
def getPhraseShorter(phrases):
    phraseLength = 1000 #numero fittzio
    phraseMin = "" #stringa vuota
    for phrase in phrases: #il cilo for trova la frase di lunghezza minore
        token = nltk.word_tokenize(phrase)
        if len(token) < phraseLength: #verifico che la lunghezza della frase trovata sia minore di quella della variabile
            phraseLength = len(token) #se minore, assegno la lunghezza della frase alla variabile
            phraseMin = phrase #inserisco la frase minore in una variabile
    return phraseMin

#la funzione prende e restituisce la frase più lunga contenente il nome proprio di persona
def getPersonPhraseMax(phrasesPerson):
    PersonPhraseList = []
    for element in phrasesPerson: #il ciclo for analizza le frasi associate a nomi di persona
        phraseMax = getPhraseLonger(element[1]) #ho la frase più lunga riferita al nome proprio
        bigram = tuple([element[0],phraseMax]) #creazione di una tupla composta da un primo elemento, il nome proprio, e da un secondo elemento, la frase più lunga 
        PersonPhraseList.append(bigram) #inserisco nella lista il nome proprio con la frase più lunga associata
    return PersonPhraseList    

#la funzione prende e restituisce la frase più breve contenente il nome proprio di persona
def getPersonPhraseMin(phrasesPerson):
    PersonPhraseList = []
    for element in phrasesPerson: #il ciclo for analizza le frasi associate ai nomi di persona
        phraseMin = getPhraseShorter(element[1]) #ho la frase più breve associata al nome proprio
        bigram = tuple([element[0],phraseMin]) #creazione di una tupla composta da un primo elemento, il nome proprio, e da un secondo elemento, la frase più breve
        PersonPhraseList.append(bigram) #inserisce nella lista il nome proprio con la frase più breve associata
    return PersonPhraseList

#la funzione prende e restituisce la lista delle entità "GPE"
def getPlace(phrases):
    tokens = getTokens(phrases) #ho i token
    bigrams = getPosTokens(tokens) #ho i bigrammi token,Pos
    tree = getTree(bigrams) #ho l'albero
    placesList = []
    for node in tree: #analizzo l'albero nodo per nodo
        NE = ''
        if hasattr(node,'label'): #verifico se node è un nodo intermedio o una foglia
            if node.label() in ["GPE"]: #prende e verifica se l'etichetta è GPE
                for partNE in node.leaves(): #con il ciclo for analizzo le foglie del nodo
                     if NE != '': #controllo i luoghi formati da più parole
                         NE = NE + '' + partNE[0]
                     else:
                         NE = partNE[0]
                     placesList.append(NE) #inserisco nella lista il nome di luogo che ho trovato
    return placesList

#la funzione prende e restituisce i 10 luoghi più frequenti
def getPlace10 (places):
    freqList = nltk.FreqDist(places) #la funzione permette di calcolare la distribuzione di frequenza degli elementi in una lista
    places10 = freqList.most_common(10)
    return places10

#la funzione prende e restituisce i 10 luoghi più frequenti in riferimento alle frasi contenenti un nome proprio di persona
def getPersonPlace (phrasesPerson):
    dictPersPlace = {} #creazione di un dizionario vuoto
    for element in phrasesPerson: #con il ciclo for analizzo le frasi contenenti nomi propri di persona
        places = getPlace(element[1]) #prendo i luoghi dalla lista delle frasi
        places10 = getPlace10(places) #ho i 10 luoghi più frequenti
        dictPersPlace[element[0]] = places10 #creazione di un dizionario in cui associo al nome proprio i 10 luoghi più frequenti
    return dictPersPlace

#la funzione prende e restituisce le 10 persone più frequenti in riferimento alle frasi contenenti un nome proprio di persona
def getPersonInPhrases(phrasesPerson):
    dictPers = {} #creazione di un dizionario vuoto
    for element in phrasesPerson: #con ii ciclo for analizzo le frasi riferite a nomi propri di persona
        person = getPerson(element[1]) #estraggo il nome proprio di persona dalle frasi
        person10 = getFreqPerson(person) #prendo i 10 nomi propri più frequenti
        dictPers[element[0]] = person10 #creazione di un dizionario in cui vengono associati il nome proprio e le 10 persone più frequenti
    return dictPers

#la funzione prende e restituisce i sostantivi 
def getSost(phrase):
    sostList = []
    tokens = getTokens(phrase) #ho i token
    bigrams = getPosTokens(tokens) #ho i bigrammi (token, Pos)
    for pos in bigrams: #ciclo for controlla che la Pos sia equivalente a quella di un sostantivo
        if pos[1] in ['NN','NNS','NNP','NNPS']:
            sostList.append(pos[0]) #aggiungo alla lista il sostantivo
    return sostList

#la funzione prende e restituisce i 10 sostantivi più frequenti 
def getSost10(sostantiveList):
    freqList = nltk.FreqDist(sostantiveList)
    sostantive10 = freqList.most_common(10)
    return sostantive10

#la funzione prende e restituisce i 10 sostantivi più frequenti in riferimento alle frasi contenenti un nome proprio di persona
def getSostantiveInPhrases(phrasesPerson):
    dictSost = {}
    for element in phrasesPerson: #con il ciclo for analizzo le frasi riferite ai nomi propri di persona
        sostantive = getSost(element[1]) #ho i sostantivi dalla lista delle frasi
        sostantive10 = getSost10(sostantive) #ho i 10 sostantivi più frequenti
        dictSost[element[0]] = sostantive10 #creazione di un dizionario in cui associo al nome proprio di persona i 10 sostantivi più frequenti
    return dictSost

#la funzione prende e restituisce i verbi
def getVerbs(phrase):
    verbsList = []
    tokens = getTokens(phrase) #ho i token
    bigrams = getPosTokens(tokens) #ho i bigrammi (token, Pos)
    for pos in bigrams: #ciclo for verifica che la Pos sia equivalente a quella di un verbo
        if pos[1] in ['VB','VBD','VBG','VBN','VBP','VBZ']:
            verbsList.append(pos[0]) #aggiungo alla lista il verbo
    return verbsList

#la funzione prende e restituisce i 10 verbi più frequenti 
def getVerbs10(verbsList):
    freqList = nltk.FreqDist(verbsList)
    verbs10 = freqList.most_common(10)
    return verbs10

#la funzione prende e restituisce i 10 verbi più frequenti in riferimento alle frasi contenenti il nome proprio di persona
def getVerbsInPhrases(phrasesPerson):
    dictVerbs= {}
    for element in phrasesPerson: #il ciclo for analizza le frasi riferite ai nomi propri di persona
        verbs = getVerbs(element[1]) #ho i verbi dalla lista delle frasi
        verbs10 = getVerbs10(verbs) #ho i 10 verbi più frequenti
        dictVerbs[element[0]] = verbs10 #creazione di un dizionario in cui associo al nome proprio di persona di riferimento i 10 verbi più frequenti
    return dictVerbs

#la funzione prende e restituisce le date, i mesi e i giorni della settimana
def getDateMonthsDays(phrases):
    dateList = []
    for phrase in phrases: #il ciclo for analizza le frasi per trovare attraverso delle RE le date, i mesi e giorni
        dateList+=re.findall(r'[Jj]anuary|[Ff]ebruary|[Mm]arch|[Aa]pril|[Mm]ay|[Jj]une|[Jj]uly|[Aa]ugust|[Ss]eptember|[Oo]ctober|[Nn]ovember|[Dd]ecember',phrase)
        dateList+=re.findall(r'[Mm]onday|[Tt]uesday|[Ww]ednesday|[Tt]hursday|[Ff]riday|[Ss]aturday|[Ss]unday',phrase)
        dateList+=re.findall(r'[0-3]?\d[-/][01]?\d[-/][0-2]?\d?\d?\d',phrase) #la funzione restituisce la lista di tutte le sequenze di caratteri che soddisfano l'espressione regolare all'interno della frase
    dateFreqList = nltk.FreqDist(dateList) #la funzione permette di calcolare la distribuzione di frequenza degli elementi in una lista
    return dateFreqList

#la funzione prende e restituisce le date, i mesi e i giorni della settimana in riferimento alle frasi contenenti un nome proprio di persona
def getDateInPhrases(phrasesPerson):
    dictDate= {}
    for element in phrasesPerson: #il ciclo for analizza le frasi riferite ai nomi propri di persona
        date = getDateMonthsDays(element[1]) #ho le date, i mesi e i giorni dalla lista delle frasi
        dictDate[element[0]] = date #creazione di un dizionario in cui associo al nome proprio di persona di riferimenti le date, i mesi e i giorni
    return dictDate

#la funzione calcola e restituisce totale dei token
def getCountTokens(token):
    count = len(token)
    return count

#la funzione calcola e restituisce la probabiità con un modello di Markov di ordine 0
def getProbabMarkov0(corpus,freqDist,tokens):
    probability = 1.0 #la variabile indica la probabilità della frase, inizializzata a 1.0
    for tok in tokens:
        probToken = freqDist[tok]*1.0 / corpus*1.0 #calcolo la probabilità di ogni token secondo la definizione frequentista
        probability = probability*probToken #calcolo la probabilità della frase con il modello di markov di ordine 0 P(w1,w2,...,wn)= P(w1)*P(w2)*...*P(wn)
    return probability

#la funzione prende e restituisce i token della singola frase
def getSinglePhraseTokens(phrase):
    tokens = nltk.word_tokenize(phrase)
    return tokens

#la funzione prende e restituisce le frasi di minimo 8 token e massimo 12 token con probabilità massima riferite ai nomi propri di persona
def getPhraseProbabMax(phrasesPerson,lenCorpus,freqDist):
    dictMarkov= {}
    for element in phrasesPerson: #ciclo le frasi riferite ai nomi propri di persona
        maxProb = 0
        maxPhrase = ""
        for phrase in element[1]: #ciclo le frasi in modo che per ognuna calcolo il numero di token
            tokens = getSinglePhraseTokens(phrase)
            countToken = getCountTokens(tokens)
            if countToken > 7 and countToken < 13: #controllo che rispettino la lunghezza 
                mark0 = getProbabMarkov0(lenCorpus,freqDist,tokens) #calcolo la probabilità con un modello di Markov di ordine 0
                if mark0 > maxProb: #controllo che si tratti di una probabilità più alta di quella presente nella mia variabile
                    maxProb = mark0 
                    maxPhrase = phrase
        tupla = [] #creazione di una tupla formata dalla frase con relativa probabilità massima
        tupla.append(maxPhrase)
        tupla.append(maxProb)
        dictMarkov[element[0]] = tuple(tupla) #creazione di un dizionario a cui al nome proprio della persona associo la tupla
    return dictMarkov        

def main(file1,file2):

    print ("\nStudente: Camilla Zucchi, matricola: 490366\n")
    print ("\nPrimo libro: The Canterville Ghost by Oscar Wilde\n")
    print ("\nSecondo libro: The Happy Prince and Other Tales by Oscar Wilde\n")

    #apro i file ricevuti in input dal programma
    fileInput1 = codecs.open(file1,"r","utf-8")
    fileInput2 = codecs.open(file2,"r","utf-8")

    #lettura dei due file di testo
    fileRead1 = fileInput1.read()
    fileRead2 = fileInput2.read()

    phrasesFile1 = getPhrases(fileRead1) #funzione per avere le frasi del primo libro
    phrasesFile2 = getPhrases(fileRead2) #funzione per avere le frasi del secondo libro

    personListFile1 = getPerson(phrasesFile1) #funzione per avere le entità Person del primo libro
    personListFile2 = getPerson(phrasesFile2) #funzione per avere le entità Person del secondo libro

    #1: i dieci nomi propri di persona più frequenti e la lista delle frasi che li contengono
    personFreqFile1 = getFreqPerson(personListFile1) #funzione per aver i 10 nomi propri più frequenti nel primo libro
    print ("\n\n-I 10 nomi propri di persona più frequenti nel primo libro sono: ")
    for element in personFreqFile1: #il ciclo for stampa la persona insieme alla sua frequenza
        print ("\nPersona: ", element[0], "con frequenza: ", element[1])

    personPhrasesFile1 = []
    for person in personFreqFile1: #col ciclo for associo ad ogni frase un nome proprio di persona
         bigram = getPhrasePerson(phrasesFile1,person[0])
         personPhrasesFile1.append(bigram)

    personFreqFile2 = getFreqPerson(personListFile2) #funzione per avere i 10 nomi propri più frequenti nel secondo libro
    print ("\n\n-I 10 nomi di persona più frequenti del secondo libro sono: ")
    for element in personFreqFile2: #ciclo for stampa la persona e la sua frequenza
        print("\nPersona: ", element[0], " con frequenza: ", element[1])

    personPhrasesFile2 = []
    for person in personFreqFile2: #col ciclo for associo ad ogni frase un nome proprio di persona
        bigram = getPhrasePerson(phrasesFile2,person[0])
        personPhrasesFile2.append(bigram)

    #2: la frase più lunga e più breve che contengono un nome proprio di persona
    phrasesMaxFile1 = getPersonPhraseMax(personPhrasesFile1) #funzione per avere la frase più lunga del primo libro in riferimento al nome proprio di persona
    print ( "\n\n-La frase più lunga riferita ai singoli nomi propri di persona più frequenti del primo libro ")
    for element in phrasesMaxFile1:
        print("\nPersona: ", element[0])
        print("\nFrase più lunga:", element[1]) 
    
    phrasesMinFile1 = getPersonPhraseMin(personPhrasesFile1) #funzione per avere la frase più breve del primo libro in riferimento al nome proprio di persona
    print ("\n\n-La frase più breve riferita ai singoli nomi propri di persona più frequenti del primo libro è:")
    for element in phrasesMinFile1:
        print("\nPersona: ", element[0])
        print("\nFrase più breve: ", element[1])
    
    phrasesMaxFile2 = getPersonPhraseMax(personPhrasesFile2) #funzione per avere la frase più lunga del secondo libro in riferimento al nome proprio di persona
    print ( "\n\n-La frase più lunga riferita ai singoli nomi propri di persona più frequenti del secondo libro è:")
    for element in phrasesMaxFile2:
        print("\nPersona: ", element[0])
        print("\nFrase più lunga: ", element[1])
    
    phrasesMinFile2 = getPersonPhraseMin(personPhrasesFile2) #funzione per avere la frase più breve del secondo libro in riferimento al nome proprio di persona
    print ("\n\n-La frase più breve riferita ai singoli nomi propri di persona più frequenti del secondo libro è:")
    for element in phrasesMinFile2:
        print("\nPersona: ", element[0])
        print("\nFrase più breve: ", element[1]) 


    #3a: i dieci luoghi più frequenti
    personPlaceFile1 = getPersonPlace(personPhrasesFile1) #funzione per avere i 10 luoghi più frequenti nelle frasi che contengono il nome proprio di persona
    print ("\n\n-I 10 luoghi più frequenti nelle frasi associate ai 10 nomi propri del primo libro sono:")
    for element in personPlaceFile1:
        print("\nPersona: ", element)
        if len(personPlaceFile1[element]) == 0: #verifico se la lista è vuota
            print("\nNon ci sono luoghi nelle frasi associate alla persona sopracitata\n")
        else:
            for place in personPlaceFile1[element]: #considero tutti gli elementi del dizionario dei luoghi
                print("\nLuogo: ", place[0], " con frequenza: ", place[1], "\n") 

    personPlaceFile2 = getPersonPlace(personPhrasesFile2) #funzione per avere i 10 luoghi più frequenti nel secondo libro
    print ("\n\n-I 10 luoghi più frequenti nelle frasi associate ai 10 nomi propri del secondo libro sono:")
    for element in personPlaceFile2:
        print("\nPersona: ", element)
        if len(personPlaceFile2[element]) == 0: #verifico se la lista è vuota
            print("\nNon ci sono luoghi nelle frasi associate alla persona sopracitata\n")
        else:
            for place in personPlaceFile2[element]: #considero ogni elemento del dizionario dei luoghi
                print("\nLuogo: ", place[0], " con frequenza: ", place[1], "\n")


    #3b: le dieci persone più frequenti 
    personPhraseFile1 = getPersonInPhrases(personPhrasesFile1) #funzione per avere le 10 persone più frequenti nelle frasi contenenti i nomi propri di persona nel primo libro
    print("\n\n-Le 10 persone più frequenti nelle frasi associate ai 10 nomi propri nel primo libro sono:")
    for element in personPhraseFile1:
        print("\nNome proprio: ", element)
        if len(personPhraseFile1[element]) == 0: #verifico se la lista è vuota
            print("\nNon ci sono nomi di persona nelle frasi associate alla persona sopracitata\n")
        else:
            for pson in personPhraseFile1[element]: #considero tutti gli elementi del dizionario contenente le persone
                print("\nPersona: ", pson[0], " con frequenza: ", pson[1])

    personPhraseFile2 = getPersonInPhrases(personPhrasesFile2)#richiamo la funzione per ottenere le 10 persone più frequenti nelle frasi associate ai nomi propri di persona del secondo libro
    print("\n\n\n---Le 10 persone più frequenti nelle frasi associate ai 10 nomi propri nel secondo libro sono:")
    for element in personPhraseFile2:
        print("\n\nNome proprio: ", element)
        if len(personPhraseFile2[element]) == 0: #verifico se la lista è vuota
            print("\nNon ci sono nomi di persona nelle frasi associate alla persona sopracitata\n")
        else:
            for pson in personPhraseFile2[element]: #considero ogni elemento del dizionario contenente le persone
                print("\nPersona: ", pson[0], " con frequenza: ", pson[1])


    #3c: i dieci sostantivi più frequenti
    sostantivePhraseFile1 = getSostantiveInPhrases(personPhrasesFile1) #funzione per avere i 10 sostantivi più frequenti nelle frasi associate ai nomi proprio di persona del primo libro
    print ("\n\n-I 10 sostantivi più frequenti nelle frasi associate ai 10 nomi propri del primo libro sono:")
    for element in sostantivePhraseFile1:
        print("\nPersona: ", element)
        if len(sostantivePhraseFile1[element]) == 0: #controllo se la lista è vuota
            print("\nNon ci sono sostantivi nelle frasi associate alla persona sopracitata\n")
        else:
            for sost in sostantivePhraseFile1[element]: #considero ogni elemento del dizionario dei sostantivi
                print("\nSostantivo: ", sost[0], " con frequenza: ", sost[1])

    sostantivePhraseFile2 = getSostantiveInPhrases(personPhrasesFile2) #funzione per avere i 10 sostantivi più frequenti nelle frasi associate ai nomi propri di persona del secondo libro
    print ("\n\n-I 10 sostantivi più frequenti nelle frasi associate ai 10 nomi propri del secondo libro sono:")
    for element in sostantivePhraseFile2:
        print("\nPersona: ", element)
        if len(sostantivePhraseFile2[element]) == 0: #controllo se la lista è vuota
            print("\nNon ci sono sostantivi nelle frasi associate alla persona sopracitata\n")
        else:
            for sost in sostantivePhraseFile2[element]: #considero ogni elemento del dizionario delle persone
                print("\nSostantivo: ", sost[0], " con frequenza: ", sost[1])


    #3d: i dieci verbi più frequenti
    verbsPhraseFile1 = getVerbsInPhrases(personPhrasesFile1)#funzione per avere i 10 verbi più frequenti nelle frasi associate ai nomi propri di persona del primo libro
    print ("\n\n-I 10 verbi più frequenti nelle frasi associate ai nomi propri del primo libro sono:")
    for element in verbsPhraseFile1:
        print("\nPersona: ", element)
        if len(verbsPhraseFile1[element]) == 0: #verifico se la lista è vuota
            print("\nNon ci sono verbi nelle frasi associate alla persona sopracitata\n")
        else:
            for vb in verbsPhraseFile1[element]: #considero ogni elemento del dizionario dei verbi
                print("\nVerbi: ", vb[0], " con frequenza: ", vb[1])

    verbsPhraseFile2 = getVerbsInPhrases(personPhrasesFile2) #funzione per avere i 10 verbi più frequenti nelle frasi associate ai nomi propri di persona del secondo libro
    print ("\n\n-I 10 verbi più frequenti nelle frasi associate ai nomi propri del secondo libro sono:")
    for element in verbsPhraseFile2:
        print("\nPersona: ", element)
        if len(verbsPhraseFile2[element]) == 0: #verifico se la lista è vuota
            print("\nNon ci sono verbi nelle frasi associate alla persona sopracitata\n")
        else:
            for vb in verbsPhraseFile2[element]: #considero ogni elemento del dizionario in verbi
                print("\nVerbi: ", vb[0], " con frequenza: ", vb[1])


    #3e: date, mesi e giorni della settimana
    datePhraseFile1 = getDateInPhrases(personPhrasesFile1) #funzione per avere le date, i mesi e i giorni nelle frasi associate ai nomi propri di persona nel primo libro
    print ("\n\n-Le date, i mesi e i giorni nelle frasi associate ai nomi propri nel primo libro sono:")
    for element in datePhraseFile1:
        print("\nPersona: ", element)
        if len(datePhraseFile1[element]) == 0: #verifico se la lista è vuota
            print("\nNon ci sono date, mesi o giorni nelle frasi associate alla persona sopracitata\n")
        else:
            for dt in datePhraseFile1[element]: #considero ogni elemento del dizionario delle date
                print("\nLe date, i mesi o i giorni: ", dt, " con frequenza: ", datePhraseFile1[element][dt]) #stampo il suo valore(dt) e il valore associato nel dizionario a (dt)

    datePhraseFile2 = getDateInPhrases(personPhrasesFile2) #funzione per avere le date, i mesi e i giorni nelle frasi associate ai nomi propri di persona nel secondo libro
    print ("\n\n-Le date, i mesi e i giorni nelle frasi associate ai nomi propri nel secondo libro sono:")
    for element in datePhraseFile2: 
        print("\nPersona: ", element)
        if len(datePhraseFile2[element]) == 0: #verifico se la lista è vuota
            print("\nNon ci sono date, mesi o giorni nelle frasi associate alla persona sopracitata\n")
        else:
            for dt in datePhraseFile2[element]: #considero ogni elemento del dizionario delle date
                print("\nLe date, i mesi o i giorni: ", dt, " con frequenza: ", datePhraseFile2[element][dt]) #stampo il suo valore(dt) e il valore associato nel dizionario a (dt)


    #3f:la frase lunga minimo 8 token e massimo 12 con probabilità più alta. Modello di Markov di ordine 0
    tokenFile1 = getTokens(phrasesFile1) #funzione per avere i token del primo libro
    CorpusFile1 = len(tokenFile1) #funzione per avere la lunghezza del corpus
    FreqDistFile1 = nltk.FreqDist(tokenFile1) #ottengo la distribuzione di frequenza
    markov0File1 = getPhraseProbabMax(personPhrasesFile1,CorpusFile1,FreqDistFile1)
    print ("\n\n-La frase lunga minimo 8 token e massimo 12 con probabilità più alta associata ai nomi proprio nel primo libro:")
    for element in markov0File1: #col ciclo for analizzo gli elementi del dizionario
        print("\n\nPersona: ", element) #stampo il nome della persona
        if markov0File1[element][1] == 0: #se il secondo elemento della tupla è 0, vuol dire che non ci sono frasi
            print("\nNon ci sono frasi con numero di token tra 8 e 12 associate alla persona sopracitata\n")
        else:
            for mv in markov0File1[element]: #col cilo for analizzo gli elementi della tupla
                if (markov0File1[element].index(mv) == 1): #se l'indice dell'elemento considerato è in seconda posizione, rappresenta la probabilità
                    print("Con probabilità", mv)
                else:
                    print("\nFrase: ", mv)

    tokenFile2 = getTokens(phrasesFile2) #funzione per avere i token del secondo libro
    CorpusFile2 = len(tokenFile2) #funzione per avere la lunghezza del corpus
    FreqDistFile2 = nltk.FreqDist(tokenFile2) #ottengo la distribuzione di frequenza
    markov0File2 = getPhraseProbabMax(personPhrasesFile2,CorpusFile2,FreqDistFile2)
    print ("\n\n-La frase lunga minimo 8 token e massimo 12 con probabilità più alta associata ai nomi proprio del secondo libro:")
    for element in markov0File2: #col ciclo for analizzo gli elementi del dizionario
        print("\nPersona: ", element) #stampo il nome della persona
        if markov0File2[element][1] == 0: #verifico se il secondo elemento della tupla è 0
            print("\nNon ci sono frasi con numero di token tra 8 e 12 associate alla persona sopracitata\n")
        else:
            for mv in markov0File2[element]: #col ciclo for analizzo gli elementi della tupla
                if (markov0File2[element].index(mv) == 1): #se l'indice dell'elemento preso in considerazione è in seconda posizione, rappresenta la probabilità
                    print("Con probabilità", mv)
                else:
                    print("\nFrase: ", mv)

main(sys.argv[1],sys.argv[2])
                                    
