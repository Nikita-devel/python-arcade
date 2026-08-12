import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import pandas as pd
from tkinter import ttk

def analyse_donnees_gps(chemin_fichier, vitesse_moyenne):
    try:
        # Read the CSV file
        df = pd.read_csv(chemin_fichier, delimiter=';')

        # Compute the total distance traveled
        distance_totale = df['Distance (m)'].sum()

        # Compute the elevation gain and loss
        denivele_positif = max(0, df['Altitude (m)'].diff().clip(lower=0).sum())
        denivele_negatif = max(0, -df['Altitude (m)'].diff().clip(upper=0).sum())

        # Find the maximum altitude
        altitude_maximale = df['Altitude (m)'].max()

        # Compute travel time from the average speed
        temps_de_parcours = round(distance_totale / vitesse_moyenne, 2)

        # Compute the approximate calories burned
        df['Calories Brûlées'] = df['Distance (m)'] * 0.05  # Utilisez votre propre coefficient
        calories_brulees = round(df['Calories Brûlées'].sum(), 2)

        # Show the results
        texte_resultat = f"Distance totale parcourue : {distance_totale} m\n"
        texte_resultat += f"Dénivelé positif : {denivele_positif} m\n"
        texte_resultat += f"Dénivelé négatif : {denivele_negatif} m\n"
        texte_resultat += f"Altitude maximale : {altitude_maximale} m\n"
        texte_resultat += f"Temps de parcours à {vitesse_moyenne} m/s : {temps_de_parcours} s\n"
        texte_resultat += f"Dépense de calories : {calories_brulees} cal"

        # Clear and show the results in the text box
        champ_texte.delete(1.0, tk.END)
        champ_texte.insert(tk.END, texte_resultat)

    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'analyse des données : {str(e)}")

# Function called when the "Start" button is clicked
def demarrer_clic():
    chemin_fichier = filedialog.askopenfilename(title="Choisir un fichier CSV", filetypes=[("Fichiers CSV", "*.csv")])
    if chemin_fichier:
        # Pick the speed
        fenetre_vitesse = tk.Toplevel(root)
        fenetre_vitesse.title("Entrez la vitesse moyenne")

        etiquette_vitesse = tk.Label(fenetre_vitesse, text="Entrez la vitesse moyenne (m/s) :")
        etiquette_vitesse.pack(pady=10)

        entree_vitesse = ttk.Entry(fenetre_vitesse)
        entree_vitesse.pack(pady=10)

        def analyser_avec_vitesse():
            vitesse = float(entree_vitesse.get())
            analyse_donnees_gps(chemin_fichier, vitesse)
            fenetre_vitesse.destroy()

        bouton_vitesse = tk.Button(fenetre_vitesse, text="Analyser avec la vitesse donnée", command=analyser_avec_vitesse)
        bouton_vitesse.pack(pady=10)

# Create the main window
root = tk.Tk()
root.title("Analyse des données GPS")

# Create the "Start" button
bouton_demarrer = tk.Button(root, text="Démarrer", command=demarrer_clic)
bouton_demarrer.pack(pady=20)

# Create the text box that shows the results
champ_texte = scrolledtext.ScrolledText(root, width=40, height=15)
champ_texte.pack(padx=20, pady=20)

# Create the exit button
bouton_sortie = tk.Button(root, text="Quitter", command=root.destroy)
bouton_sortie.pack(pady=20)

# Start the GUI's main loop
root.mainloop()
