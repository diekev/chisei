# -*- coding:utf-8 -*-

# ***** BEGIN GPL LICENSE BLOCK *****
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# The Original Code is Copyright (C) 2017 Kévin Dietrich.
# All rights reserved.
#
# ***** END GPL LICENSE BLOCK *****

import operator
import numpy

from utilitaires import calcule_matrice_correlation
from utilitaires import divise_texte
from utilitaires import genere_vecteur_mots
from utilitaires import liste_mots_uniques


def compte_occurences(mots, mots_uniques, top_mots=50):
    occurences = {}

    for mot in mots_uniques:
        occurences[mot] = 0

    for mot in mots:
        occurences[mot] += 1

    occurences_triees = []

    for k in occurences:
        occurences_triees.append((k, occurences[k]))

    occurences_triees = sorted(occurences_triees,
                               key=operator.itemgetter(1),
                               reverse=True)

    print ('Les {} mots les plus utilisés sont :'.format(top_mots))

    for i in range(top_mots):
        print occurences_triees[i][0], occurences_triees[i][1]


def calcule_correlations(matrice, nombre_articles):
    correlations = []

    for i in range(nombre_articles):
        for j in range(i + 1, nombre_articles):
            correlation = numpy.dot(matrice[i], matrice[j]) * 100
            correlations.append((i, j, correlation))

    correlations = sorted(correlations,
                          key=operator.itemgetter(2),
                          reverse=True)

    nombre_correlations = len(correlations)

    nombre_corr = 5
    print('Les {} articles les plus corrélés sont :'.format(nombre_corr))

    for i in range(nombre_corr):
        article_a = correlations[i][0]
        article_b = correlations[i][1]
        correlation = correlations[i][2]

        print('------------------------------------------------------------')
        print('Corrélation : ({:.5f}%)\n'.format(correlation))
        print('\t{} : {}'.format(article_a + 1, articles[article_a]))
        print('\t{} : {}'.format(article_b + 1, articles[article_b]))


def calcule_correlations_vecteur(matrice, nombre_articles, vecteur):
    correlations = []

    for i in range(nombre_articles):
        correlation = numpy.dot(matrice[i], vecteur_mots_cles[0])
        correlations.append((i, correlation))

    correlations = sorted(correlations,
                          key=operator.itemgetter(1),
                          reverse=True)

    nombre_correlations = len(correlations)

    nombre_corr = 5
    print('Les {} articles les plus corrélés sont :'.format(nombre_corr))

    for i in range(nombre_corr):
        article = correlations[i][0]
        correlation = correlations[i][1]

        print('------------------------------------------------------------')
        print('Corrélation : ({:.5f}%)\n'.format(correlation))
        print('\t{} : {}'.format(article + 1, articles[article]))


############################ Lecture des fichiers. ############################

fichiers = [
    'textes/charte_environnement.txt',
    'textes/constitution.txt',
    'textes/droits_femme.txt',
    'textes/droits_homme.txt',
]

articles = []
texte = ''

for fichier in fichiers:
    with open(fichier, 'r') as f:
        for ligne in f:
            if ligne.rstrip() == '':
                continue

            articles.append(ligne)

mots_uniques = []
nombre_mots = 0
texte_entier = []

for article in articles:
    mots = divise_texte(article)
    texte_entier += mots
    nombre_mots += len(mots)

    mots_uniques_article = liste_mots_uniques(mots)
    mots_uniques += mots_uniques_article

nombre_mots_unique = len(mots_uniques)
pourcentage_mots_uniques = (nombre_mots_unique * 100.0 / nombre_mots)

message = 'Il y a {} mots dans le texte, dont {} uniques ({}% du total).\n'
message = message.format(nombre_mots,
                         nombre_mots_unique,
                         pourcentage_mots_uniques)

print(message)

delta = 1.0 / nombre_mots

indice = 0
indices_mots = {}

for mot in mots_uniques:
    indices_mots[mot] = indice
    indice += 1

nombre_articles = len(articles)

######################## Génération matrice articles. #########################

matrice_article = numpy.zeros(shape=(nombre_articles, nombre_mots_unique))

indice_article = 0

for article in articles:
    mots = divise_texte(article)

    for mot in mots:
        indice_mot = indices_mots[mot]
        matrice_article[indice_article][indice_mot] += delta

    indice_article += 1

########################## Génération matrice mots. ###########################

matrice_mots = calcule_matrice_correlation(mots_uniques,
                                           texte_entier,
                                           indices_mots)

################################# Évaluation. #################################

while True:
    mots_cles = raw_input('Entrez des mots-clés : ')

    vecteur_mots_cles = genere_vecteur_mots(mots_cles,
                                            matrice_mots,
                                            indices_mots,
                                            nombre_mots_unique)

    calcule_correlations_vecteur(matrice_article,
                                 nombre_articles,
                                 vecteur_mots_cles)
