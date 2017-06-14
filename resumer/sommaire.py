# -*- coding: utf-8 -*-

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

import sys

reload(sys)  
sys.setdefaultencoding('utf8')


class Resumeur:
    def resume(self, entree, nombre_phrase):
        liste_ponct = ['.', ',', '!', ';', '?']
        sommaire_phrases = []

	print 'Conversion des phrases en minuscule...'

        phrases = sent_tokenize(entree)
        phrases_minuscules = [phrase.lower() for phrase in phrases]

	print 'Conversion des mots en minuscules....'

        s = list(entree)
        ts = ''.join([o for o in s if not o in liste_ponct]).split()
        mots_minuscules = [mot.lower() for mot in ts]


	print 'Extractions des mots....'
        mots = [mot for mot in mots_minuscules if mot not in stopwords.words()]

	print 'Calcule de la fréquence des mots....'

        frequences_mots = FreqDist(mots)

	print 'Extractions des mots les plus fréquents....'
        mots_plus_frequents = [paire[0] for paire in frequences_mots.items()[:100]]

	print 'Nombre de mots les plus fréquents ', len(mots_plus_frequents)
        for mot in mots_plus_frequents:
            for i in range(0, len(phrases_minuscules)):
                if len(sommaire_phrases) >= nombre_phrase:
                    continue

                if phrases_minuscules[i] not in sommaire_phrases and mot in phrases_minuscules[i]:
                    sommaire_phrases.append(phrases[i])
                    break

        sommaire_phrases.sort(lambda s1, s2: entree.find(s1) - entree.find(s2))
        return ' '.join(sommaire_phrases)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Il manque un argument !")

    texte = ""

    with open(sys.argv[1], 'r') as fichier_entree:
        texte = fichier_entree.read()

    resumeur = Resumeur()
    print resumeur.resume(texte, 20)
