import random
import time
import streamlit as st

st.title("Projet le Compte est bon ")
st.sidebar.header("Les jeux disponibles ")
Married = st.sidebar.selectbox('les jeux', ('le compte est bon', 'le mot le plus long'))


# Définition des opérations possibles
OPERATIONS = ['+', '-', '*', '/']

# Définition des cartonnettes disponibles
CARTONNETTES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 25, 50, 75, 100]

# Définition de la durée d'une manche en secondes
DUREE_MANCHE = 45

# Définition du nombre de manches
NOMBRE_MANCHES = 4

# Définition du nombre de joueurs
NOMBRE_JOUEURS = 2

# Définition de la fonction pour générer un nombre aléatoire
def generer_nombre():
    return random.randint(1, 999)

# Définition de la fonction pour piocher des chiffres dans le sac
def piocher_chiffres():
    return random.sample(CARTONNETTES, 6)

# Définition de la fonction pour calculer toutes les combinaisons possibles
def calculer_combinaisons(chiffres):
    if len(chiffres) == 1:
        return [chiffres[0]]
    else:
        combinaisons = []
        for i in range(len(chiffres)):
            reste = chiffres[:i] + chiffres[i+1:]
            sous_combinaisons = calculer_combinaisons(reste)
            for sous_combinaison in sous_combinaisons:
                for operation in OPERATIONS:
                    expression = str(chiffres[i]) + operation + str(sous_combinaison)
                    try:
                        resultat = eval(expression)
                        if resultat > 0 and int(resultat) == resultat:
                            combinaisons.append(resultat)
                    except ZeroDivisionError:
                        pass
        return combinaisons

# Définition de la fonction pour trouver la combinaison la plus proche du nombre cible
def trouver_meilleure_combinaison(nombre_cible, combinaisons):
    combinaisons_triees = sorted(combinaisons, key=lambda x: abs(x - nombre_cible))
    return combinaisons_triees[0]
# Définition de la fonction pour jouer une manche
def jouer_manche():
    # Générer le nombre cible et les chiffres
    nombre_cible = generer_nombre()
    chiffres = piocher_chiffres()

    st.markdown("<h1 style='color: gold;'>Le nombre cible est : {}</h1>".format(nombre_cible), unsafe_allow_html=True)
    st.write("<h3 style='color: red;'>{}<h3>".format(chiffres), unsafe_allow_html=True)

    # Démarrer le chrono de la manche
    debut_manche = time.time()

    # Calculer les combinaisons possibles
    combinaisons = calculer_combinaisons(chiffres)

    # Boucle principale de la manche
    while True:
        # Vérifier si le temps de la manche est écoulé
        temps_ecoule = time.time() - debut_manche
        if temps_ecoule >= DUREE_MANCHE:
            st.write("Temps écoulé !")
            break

        # Demander les réponses des joueurs
        reponses = []
        for i in range(NOMBRE_JOUEURS):
            st.write("Joueur", i+1, ":", end=" ")
            #reponse = input()
            reponse = st.text_input("Réponse :", key=i, placeholder="Entrez votre réponse")

            # Vérifier que la réponse est valide
            try:
                resultat = int(eval(reponse))
                reponses.append(resultat)
            except:
                st.write("Erreur de saisie, réessayez")
                break
        else:
            # Trouver la meilleure combinaison pour chaque joueur
            meilleures_combinaisons = [trouver_meilleure_combinaison(nombre_cible, combinaisons) for _ in range(NOMBRE_JOUEURS)]

            # Calculer l'écart entre la réponse du joueur et la meilleure combinaison
            ecarts = [abs(reponse - combinaison) for reponse, combinaison in zip(reponses, meilleures_combinaisons)]

            # Déterminer le gagnant de la manche
            gagnant = ecarts.index(min(ecarts))
            if ecarts.count(min(ecarts)) > 1:
                st.write("Match nul !")
            else:
                st.write("Le joueur", gagnant+1, "remporte la manche !")

                # Retourner l'index du joueur gagnant
                return gagnant

# Définition de la fonction pour jouer une partie complète
def jouer_partie():
    # Initialiser les scores des joueurs
    scores = [0] * NOMBRE_JOUEURS

    # Boucle principale de la partie
    for manche in range(NOMBRE_MANCHES):
        st.write(f"<h1 style='color:green'>Manche {manche+1}</h2>", unsafe_allow_html=True)


        # Jouer la manche et récupérer l'index du joueur gagnant
        gagnant = jouer_manche()

        # Ajouter les points du joueur gagnant à son score
        scores[gagnant] += 6

        st.write("<span style='font-family: Arial; color: blue;'>Scores :</span>",
                 "<span style='font-family: Arial; color: red;'>{}</span>".format(scores),
                 unsafe_allow_html=True)

    # Déterminer le vainqueur de la partie
    vainqueur = scores.index(max(scores))
    st.write("Le joueur", vainqueur+1, "remporte la partie avec", max(scores), "points !")

# Lancer la partie
jouer_partie()

