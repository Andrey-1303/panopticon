import os
import cv2
import json
from deepface import DeepFace
import shutil

# Создаем папку для сохранения фото
if not os.path.exists("_dataset"):
    os.makedirs("_dataset")

# Создаем папку для лиц
if not os.path.exists("_faces"):
    os.makedirs("_faces")

# Создаем папку для базы данных
if not os.path.exists("_database"):
    os.makedirs("_database")

# Создаем папку для архива фото
if not os.path.exists("_datasetarchive"):
    os.makedirs("_datasetarchive")

# Файлы для хранения текущего состояния
face_index_file = "_faces/index.json"
database_index_file = "_database/index.json"

# Инициализируем переменные
i = 1
face_paths = []

# Загрузка текущего состояния лиц
if os.path.exists(face_index_file):
    with open(face_index_file, "r") as f:
        face_paths = json.load(f)

# Загрузка текущего состояния базы данных
if os.path.exists(database_index_file):
    with open(database_index_file, "r") as f:
        i = json.load(f)["counter"]

# Получаем список файлов с фотографиями из папки "_dataset"
dataset_files = os.listdir("_dataset")
dataset_paths = [os.path.join("_dataset", f) for f in dataset_files]

# Функция для сравнения лиц на двух изображениях
def face_verify(img_1, img_2):
    try:
        result_dict = DeepFace.verify(img1_path=img_1, img2_path=img_2)
        if result_dict.get('verified'):
            return 'лица одинаковые'
        return 'лица разные'
    except Exception as _ex:
        return _ex

# Проверяем каждую фотографию из базы данных
for image_path in dataset_paths:
    found_match = False

    # Проверяем сохраненную фотографию с фотографиями лиц из папки "faces"
    for face_path in face_paths:
        result = face_verify(face_path, image_path)
        if result == "лица одинаковые":
            # Получаем номер img_1
            img_1_number = int(os.path.basename(face_path).split(".")[0])

            # Создаем папку с именем n внутри папки "database"
            database_folder = os.path.join("_database", str(img_1_number))
            if not os.path.exists(database_folder):
                os.makedirs(database_folder)

            # Копируем img_2 в папку "database/n"
            img_2_filename = str(len(os.listdir(database_folder))) + ".jpg"
            img_2_destination = os.path.join(database_folder, img_2_filename)
            cv2.imwrite(img_2_destination, cv2.imread(image_path))
            found_match = True
            break

    if not found_match:
        # Если нет совпадения, добавляем фото в папку "faces"
        new_face_path = os.path.join("_faces", f"{i}.jpg")
        cv2.imwrite(new_face_path, cv2.imread(image_path))
        face_paths.append(new_face_path)

        # Создаем папку с именем n внутри папки "database"
        new_database_folder = os.path.join("_database", str(i))
        os.makedirs(new_database_folder)

        # Копируем img_1 в папку "database/n"
        img_1_index = int(os.path.basename(image_path).split(".")[0])
        img_1_filename = f"{i}_q{img_1_index * 5}.jpg"
        img_1_destination = os.path.join(new_database_folder, img_1_filename)
        cv2.imwrite(img_1_destination, cv2.imread(new_face_path))

        i += 1

    # Перемещаем проверенную фотографию в папку архива
    shutil.move(image_path, os.path.join("_datasetarchive", os.path.basename(image_path)))

# Сохранение текущего состояния лиц
with open(face_index_file, "w") as f:
    json.dump(face_paths, f)

# Сохранение текущего состояния базы данных
with open(database_index_file, "w") as f:
    json.dump({"counter": i}, f)

print("Фотографии разных лиц успешно сохранены в папку '_faces'.")
