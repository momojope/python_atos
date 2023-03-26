import random
import itertools
import threading
import time
import streamlit as st

# Dictionnaire des mots valides
dictionnaire = set()
with open("Liste.txt", "r") as f:
    for ligne in f:
        dictionnaire.add(ligne.strip())


# Fonction pour jouer à "Le Mot le plus Long"
def jouer_mot_plus_long():
    voyelles = "AEIOU"
    consonnes = "BCDFGHJKLMNPQRSTVWXYZ"
    sac_voyelles = list(voyelles * 15)
    sac_consonnes = list(consonnes * 7)
    random.shuffle(sac_voyelles)
    random.shuffle(sac_consonnes)
    tirage = []
    for i in range(2):
        tirage.append(random.choice(voyelles))
    for i in range(4):
        tirage.append(random.choice(consonnes))
    for i in range(2):
        tirage.append(random.choice(sac_voyelles))
    for i in range(2):
        tirage.append(random.choice(sac_consonnes))
    random.shuffle(tirage)
    st.write("<h3 style='color: red;'>{}<h3>".format(tirage), unsafe_allow_html=True)
    reponse = []

    def input_with_timeout():
        nonlocal reponse
        timer = threading.Timer(30.0, thread_timeout)
        timer.start()
        reponse = st.text_input("Votre mot : ")
        timer.cancel()

    def thread_timeout():
        nonlocal reponse
        st.write("\nLe temps est écoulé !\n")
        reponse = "TEMPS ÉCOULÉ"

    input_thread = threading.Thread(target=input_with_timeout)
    input_thread.start()
    input_thread.join()

    if reponse == "TEMPS ÉCOULÉ":
        return 0

    for lettre in reponse:
        if lettre.upper() not in tirage:
            st.write("Le mot n'est pas valide.")
            return 0

    if reponse.lower() not in dictionnaire:
        st.write("Le mot n'est pas valide.")
        return 0

    return len(reponse)

def jouer_compte_est_bon():
    chiffres = [1, 2, 3, 4, 5, 6, 7, 8, 9, 25, 50, 75, 100]
    random.shuffle(chiffres)
    cible = random.randint(1, 999)
    st.write("<h3 style='color: gold;'>{}<h3>".format(cible), unsafe_allow_html=True)
    st.write("<h3 style='color: red;'>{}<h3>".format(chiffres), unsafe_allow_html=True)

    # Définir la fonction pour le compte à rebours
    def countdown():
        for i in range(30, 0, -1):
            st.write("Temps restant :", i)
            time.sleep(1)

    # Démarrer le compte à rebours en tant que thread
    timer_thread = threading.Thread(target=countdown)
    timer_thread.start()

    reponse = st.text_input("Votre solution : ")

    # Arrêter le compte à rebours si le joueur répond avant la fin du temps imparti
    timer_thread.join(0)

    try:
        # Vérifier que l'expression arithmétique est valide
        eval(reponse.replace("^", "**"))
        # Calculer le score
        score = abs(eval(reponse.replace("^", "**")) - cible)
        if score < 10:
            st.write("Bravo, vous avez trouvé une solution proche de la cible !")
        else:
            st.write("Dommage, votre solution est trop éloignée de la cible.")
    except:
        st.write("L'expression que vous avez saisie n'est pas valide.")
        return 0

# Lancer le jeu
if st.button("Jouer au Mot le plus Long"):
    jouer_mot_plus_long()

if st.button("Jouer au Compte est bon"):
    jouer_compte_est_bon()