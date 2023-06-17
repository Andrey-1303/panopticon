import os
import cv2
import time
from deepface import DeepFace

# Создаем папку для сохранения фото
if not os.path.exists("dataset"):
    os.makedirs("dataset")

# Инициализируем видеопоток с камеры
cap = cv2.VideoCapture(0)

# Проверяем успешное открытие видеопотока
if not cap.isOpened():
    print("Не удалось открыть видеопоток с камеры.")
    exit()

# Переменная для хранения текущего порядкового номера фото
i = 1

# Переменная для отслеживания времени
time_elapsed = 0

# Переменная для хранения времени последнего удаления
last_deletion_time = time.time()

# Переменная для хранения текущей папки
current_folder = "dataset"

# Функция для сравнения лиц на двух изображениях
def face_verify(img_1, img_2):
    try:
        result_dict = DeepFace.verify(img1_path=img_1, img2_path=img_2)
        if result_dict.get('verified'):
            return 'лица одинаковые'
        return 'лица разные'
    except Exception as _ex:
        return _ex

# Читаем кадры из видеопотока
while cap.isOpened():
    # Читаем следующий кадр
    ret, frame = cap.read()

    # Если удалось прочитать кадр
    if ret:
        # Увеличиваем время
        time_elapsed += 1

        # Если прошло 5 секунд (примерно 150 кадров при 30 кадрах в секунду)
        if time_elapsed == 150:
            # Сохраняем кадр в текущую папку
            image_path = os.path.join(current_folder, f"{i}.jpg")
            cv2.imwrite(image_path, frame)
            print(f"Сохранено фото {image_path}")

            # Проверяем сохраненный кадр с предыдущими фотографиями
            similar_face_found = False
            for j in range(1, i):
                previous_image_path = os.path.join(current_folder, f"{j}.jpg")
                result = face_verify(previous_image_path, image_path)
                print(f"Сравнение {previous_image_path} и {image_path}: {result}")
                if result == 'лица одинаковые':
                    similar_face_found = True
                    # Сохраняем фотографию в папку с похожим лицом
                    current_folder = os.path.dirname(previous_image_path)
                    i = int(os.path.splitext(os.path.basename(previous_image_path))[0]) + 1
                    break

            if not similar_face_found:
                # Создаем новую папку
                new_folder_index = len(os.listdir("dataset")) + 1
                current_folder = os.path.join("dataset", str(new_folder_index))
                os.makedirs(current_folder)
                print(f"Создана новая папка {current_folder}")
                i = 1

            # Сохраняем фотографию в текущую папку
            new_image_path = os.path.join(current_folder, f"{i}.jpg")
            cv2.imwrite(new_image_path, frame)
            print(f"Сохранено фото в текущую папку: {new_image_path}")

            # Увеличиваем порядковый номер
            i += 1

            # Сбрасываем время
            time_elapsed = 0

            # Удаляем снимок, сделанный минуту назад
            current_time = time.time()
            if current_time - last_deletion_time >= 60:
                last_deletion_time = current_time - 5  # Задержка перед удалением
                previous_image_path = os.path.join(current_folder, f"{i - 2}.jpg")
                if os.path.exists(previous_image_path):
                    os.remove(previous_image_path)
                    print(f"Удален снимок {previous_image_path}")

    else:
        # Ошибка чтения кадра
        break

# Закрываем видеопоток и освобождаем ресурсы
cap.release()
cv2.destroyAllWindows()
