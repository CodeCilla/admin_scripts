#!/bin/bash

# Chemin du dossier à surveiller
# folder="/volume1/sauvegarde_ftp_le_mans/Camera"
# folder="/volume1/sauvegarde_ftp_rouen/Camera"
# folder="/volume1/sauvegarde_NASRENNES/Camera"
# folder="/volume1/sauvegarde_nantes/Camera"

# Chemin du dossier à surveiller
folder="/volume1/sauvegarde_ftp_le_mans/Camera"

# Emplacement du fichier de log
log_file="/volume1/sauvegarde_ftp_le_mans/Program/log/suppression_camera.log"

# Espace disque total (en Mo)
total_space=$(df -BM "$folder" | awk 'NR==2{print $2}' | sed 's/[^0-9]*//g')

# Définir la limite d'espace disque à 90% de l'espace total
limit=$((total_space * 90 / 100))

# Espace disque disponible (en Mo)
disk_space=$(df -BM "$folder" | awk 'NR==2{print $4}' | sed 's/[^0-9]*//g')

# Espace en %
used_space=$(df "$folder" | awk 'NR==2{print $5}' | sed 's/%//g')

# Ajouter des informations de débogage au fichier de log
echo "===== Exécution du script le $(date '+%Y-%m-%d %H:%M:%S') =====" | tee -a "$log_file"
echo "Espace disque total: $total_space Mo" | tee -a "$log_file"
echo "Limite d'espace disque: $limit Mo" | tee -a "$log_file"
echo "Espace disque disponible: $disk_space Mo" | tee -a "$log_file"

# Si l'espace disponible est inférieur à la limite
if [ "$used_space" -ge 90 ]; then
    echo "Début du nettoyage..." | tee -a "$log_file"

    # Compter et logger le nombre de fichiers avant suppression
    nb_fichiers_avant=$(find "$folder" -type f | wc -l)
    echo "Nombre de fichiers avant nettoyage : $nb_fichiers_avant" | tee -a "$log_file"

    # Supprimer les fichiers plus anciens que 3 semaines
    find "$folder" -type f -mtime +21 -delete

    # Compter et logger le nombre de fichiers après suppression
    nb_fichiers_apres=$(find "$folder" -type f | wc -l)
    echo "Nombre de fichiers après nettoyage : $nb_fichiers_apres" | tee -a "$log_file"
    echo "Nombre de fichiers supprimés : $((nb_fichiers_avant - nb_fichiers_apres))" | tee -a "$log_file"

    # Supprimer tous les dossiers non essentiels ou anciens (vides)
    find "$folder" -mindepth 1 -type d -empty -delete
    echo "Nettoyage terminé." | tee -a "$log_file"
else
    echo "Espace disque suffisant." | tee -a "$log_file"
fi

echo "=== Fin de l'exécution ===" | tee -a "$log_file"
echo "" | tee -a "$log_file"

# test experimental

