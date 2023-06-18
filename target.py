import os
import cv2
from deepface import DeepFace

# Путь к фото target.jpg
target_image_path = "target.jpg"

# Путь к папке с фотографиями лиц
faces_folder = "_faces"

# Загружаем фото target.jpg
target_image = cv2.imread(target_image_path)

# Функция для сравнения лиц на двух изображениях
def face_verify(img_1, img_2):
    try:
        result_dict = DeepFace.verify(img1_path=img_1, img2_path=img_2)
        if result_dict.get('verified'):
            return True
        return False
    except Exception as _ex:
        return False

# Проверяем каждую фотографию из папки faces
for face_file in os.listdir(faces_folder):
    face_path = os.path.join(faces_folder, face_file)
    if face_verify(face_path, target_image_path):
        print(f"На фото {target_image_path} есть лицо, такое же как на фото {face_path}")
        # Действия, которые нужно выполнить, если найдено совпадение
        break
else:
    print(f"На фото {target_image_path} нет лиц, таких же как на фотографиях в папке {faces_folder}")
