Pour ce module
script scrapping_urls.py pour scrapper les urls que j'ai lancé en externe qui me renvoie un fichier urls.csv
le script main.py
lit le fichier urls.csv qui a été généré
Supprime les fichiers statiques .jpg, .pdf, ... qui ne sont pas traqués par google
Supprime le domaine de l'url
Normalise les URLs en ajoutant / devant si besoin
Création d'une collection pour supprimer les doublons éventuels
Redirection en 301
