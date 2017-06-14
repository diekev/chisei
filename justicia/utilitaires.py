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

import numpy


def est_nombre(a, b, c):
    return (a == '-' or a == ',' or a == ' ') and b.isdigit() and c.isdigit()


def divise_texte(texte):
    liste_mots = []
    mot_courrant = ''
    debut = 0
    fin = len(texte)

    for i in range(fin):
        lettre = texte[i].lower()

        if lettre in [' ', '\n', '\t']:
            if (i > 0 and i < fin - 1) \
               and est_nombre(lettre, texte[i - 1], texte[i + 1]):
                mot_courrant += lettre
                continue

            if mot_courrant != '':
                liste_mots.append(mot_courrant)
                mot_courrant = ''

            continue

        if lettre in [',', ';', ':', '(', ')', '?', '!', '.', '\'', '-']:
            if (i > 0 and i < fin - 1) \
               and est_nombre(lettre, texte[i - 1], texte[i + 1]):
                mot_courrant += lettre
                continue

            if mot_courrant != '':
                liste_mots.append(mot_courrant)
                mot_courrant = ''

            liste_mots.append(lettre)
            continue

        mot_courrant += lettre

    if mot_courrant != '':
        liste_mots.append(mot_courrant)

    return liste_mots


def liste_mots_uniques(mots):
    mots_uniques = []

    for mot in mots:
        if mot not in mots_uniques:
            mots_uniques.append(mot)

    return mots_uniques


# Génère un vecteur à partir des mots passés en paramètre. Le vecteur est le
# résultat de la multiplication des vecteurs des mots passés en paramètre entre
# eux issus de la matrice passée en paramètre.
def genere_vecteur_mots(mots, matrice, indices_mots, taille_vecteur):
    liste_mots_cles = divise_texte(mots)
    vecteur_mots_cles = numpy.ones(shape=(1, taille_vecteur))

    for mot in liste_mots_cles:
        if mot not in indices_mots:
            continue

	indice_mot = indices_mots[mot]

	print(numpy.linalg.norm(matrice[indice_mot]))
        vecteur_mots_cles *= matrice[indice_mot]

    return vecteur_mots_cles


# Génère la matrice qui représente la corrélation entre les mots passés en
# paramètre, corrélation prenant en compte un nombre de mots dans le voisinage
# du mot centré égale au paramètre 'taille_fenetre'.
def calcule_matrice_correlation(mots, texte, indices_mots, taille_fenetre=5):
    nombre_mots = len(mots)
    longueur_texte = len(texte)
    matrice = numpy.zeros(shape=(nombre_mots, nombre_mots))

    for i in range(longueur_texte):
        indice_mot = indices_mots[texte[i]]

        for j in range(max(0, i - taille_fenetre), i):
            indice_mot_pre = indices_mots[texte[j]]
            matrice[indice_mot][indice_mot_pre] += 1

        for j in range(i + 1, min(i + taille_fenetre + 1, longueur_texte - taille_fenetre + 1)):
            indice_mot_post = indices_mots[texte[j]]
            matrice[indice_mot][indice_mot_post] += 1

    return matrice
