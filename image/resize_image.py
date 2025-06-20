import os
from PIL import Image

# Dossier contenant les images à redimensionner
input_folder = "images_a_redimensionner"
output_folder = "images_redimensionnees"
os.makedirs(output_folder, exist_ok=True)

size = (130, 130)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path).convert("RGBA")

        # Créer une image blanche carrée
        new_img = Image.new("RGBA", size, (255, 255, 255, 0))
        # Redimensionner l’image en gardant le ratio
        img.thumbnail(size, Image.LANCZOS)
        # Centrer l’image sur le carré
        x = (size[0] - img.width) // 2
        y = (size[1] - img.height) // 2
        new_img.paste(img, (x, y), img)
        # Sauvegarder
        output_path = os.path.join(output_folder, filename)
        new_img.convert("RGB").save(output_path)
        print(f"{filename} redimensionnée.")

print("Terminé !")