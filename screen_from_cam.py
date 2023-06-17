import os
import cv2
import time

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
            # Сохраняем кадр в папку dataset
            image_path = os.path.join("dataset", f"{i}.jpg")
            cv2.imwrite(image_path, frame)

            print(f"Сохранено фото {image_path}")

            # Увеличиваем порядковый номер
            i += 1

            # Сбрасываем время
            time_elapsed = 0

            # Удаляем снимок, сделанный минуту назад
            current_time = time.time()
            if current_time - last_deletion_time >= 60:
                last_deletion_time = current_time - 5  # Задержка перед удалением
                previous_image_path = os.path.join("dataset", f"{i - 2}.jpg")
                if os.path.exists(previous_image_path):
                    os.remove(previous_image_path)
                    print(f"Удален снимок {previous_image_path}")

    else:
        # Ошибка чтения кадра
        break

# Закрываем видеопоток и освобождаем ресурсы
cap.release()
cv2.destroyAllWindows()
