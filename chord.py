import os
from datetime import datetime

def create_markdown_with_image(url, height=58000, markdown_dir="D:/9. NAS drive/Smartnotes/Smartnotes2024/30.interets/31. Guitare", image_dir="D:/9. NAS drive/Smartnotes/Smartnotes2024/30.interets/31. Guitare/img"):
    """
    Capture une page web, stocke l'image dans un répertoire, et génère un fichier Markdown avec l'image.

    Paramètres :
    - url (str) : L'URL de la page web à capturer.
    - height (int, optionnel) : Hauteur maximale de la capture (par défaut : 58000 pixels).
    - markdown_dir (str, optionnel) : Répertoire où le fichier Markdown sera stocké (par défaut : "D:/9. NAS drive/Smartnotes/Smartnotes2024/30.interets/31. Guitare").
    - image_dir (str, optionnel) : Répertoire où l'image sera stockée (par défaut : "D:/9. NAS drive/Smartnotes/Smartnotes2024/30.interets/31. Guitare/img").

    Sortie :
    - Le fichier Markdown est créé avec l'image référencée.
    """
    # Étape 1 : Extraire le titre (partie après le dernier "/")
    title = url.split("/")[-1]

    # Étape 2 : Formater le nom de la chanson (supprimer les suffixes et remplacer les tirets par des espaces)
    song_name = "-".join(title.split("-")[:-2]).replace("-", " ")

    # Étape 3 : Extraire le nom de l'artiste
    artist = url.split("/")[-2]

    # Étape 4 : Construire le nom du fichier image et Markdown
    output_filename = f"{artist} - {song_name}.png"
    markdown_title = f"{artist} - {song_name}"
    markdown_filename = f"{artist} - {song_name}.md"

    # Étape 5 : Vérifier et créer les répertoires "img" et "markdown" s'ils n'existent pas
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # Étape 6 : Construire le chemin de sortie pour l'image et le fichier Markdown
    image_path = os.path.join(image_dir, output_filename)
    markdown_path = os.path.join(markdown_dir, markdown_filename)

    # Étape 7 : Exécuter la commande shot-scraper avec le sélecteur fixe
    command = f'shot-scraper {url} -s .P8ReX --height {height} -o "{image_path}"'
    print(f"Exécution de la commande : {command}")
    os.system(command)

    # Étape 8 : Obtenir la date d'aujourd'hui
    current_date = datetime.today().strftime('%Y-%m-%d')

    # Étape 9 : Créer le contenu du fichier Markdown avec le nom de fichier image relatif
    markdown_content = f"""---
title: {song_name}
artiste: "[[{artist}]]"
date: {current_date}
---
![[{output_filename}]]
"""

    # Étape 10 : Écrire le fichier Markdown
    with open(markdown_path, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)

    print(f"Fichier Markdown créé : {markdown_path}")
    return markdown_path

# Boucle
while True:
    url = input("Veuillez entrer l'URL de la page web (ou tapez 'q' pour quitter) : ")
    if url.lower() == 'q':
        print("Fermeture du programme.")
        break

    markdown_file = create_markdown_with_image(url)
    print(f"Fichier Markdown généré : {markdown_file}")
    print("------------------------------------------------------")