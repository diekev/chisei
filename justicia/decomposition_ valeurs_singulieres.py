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

import numpy as np

import matplotlib.pyplot as plt

la = np.linalg

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def calcule_matrice_correlation(mots, texte, indices_mots, taille_fenetre=5):
    nombre_mots = len(mots)
    longueur_texte = len(texte)
    matrice = np.zeros(shape=(nombre_mots, nombre_mots))

    for i in range(longueur_texte):
        indice_mot = indices_mots[texte[i]]

        for j in range(max(0, i - taille_fenetre), i):
            indice_mot_pre = indices_mots[texte[j]]
            matrice[indice_mot][indice_mot_pre] += 1

        for j in range(i + 1, min(i + taille_fenetre + 1, longueur_texte - taille_fenetre + 1)):
            indice_mot_post = indices_mots[texte[j]]
            matrice[indice_mot][indice_mot_post] += 1

    return matrice


from utilitaires import divise_texte
from utilitaires import liste_mots_uniques

#texte = "I like deep learning. I like NLP. I enjoy flying."

fichiers = [
#    'textes/droits_femme.txt',
#    'textes/droits_homme.txt',
    'textes/constitution.txt',
]

texte = ''

for f in fichiers:
    with open(f, 'r') as fichier:
        for ligne in fichier:
            if ligne.rstrip() == '':
                continue

            texte += ligne

texte_divise = divise_texte(texte)
mots_uniques = liste_mots_uniques(texte_divise)

#mots_uniques = ["i", "like", "enjoy", "deep", "learning", "nlp", "flying", "."]

indices_mots = {}
indice_mot = 0

for mot in mots_uniques:
    indices_mots[mot] = indice_mot
    indice_mot += 1

#print indices_mots

matrice = calcule_matrice_correlation(mots_uniques, texte_divise, indices_mots)

#print matrice

X = np.array([[0,2,1,0,0,0,0,2],
              [2,0,0,1,0,1,0,0],
              [1,0,0,0,0,0,1,0],
              [0,1,0,0,1,0,0,0],
              [0,0,0,1,0,0,0,1],
              [0,1,0,0,0,0,0,1],
              [0,0,1,0,0,0,0,1],
              [2,0,0,0,1,1,1,0]])

#print X

U, s, Vh = la.svd(matrice, full_matrices=False)

for i in xrange(len(mots_uniques)):
    plt.text(U[i, 0], U[i, 1], mots_uniques[i])

plt.show()
