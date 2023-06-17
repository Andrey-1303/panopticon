import os
import cv2

# Создаем папку для сохранения фото
if not os.path.exists("_dataset"):
    os.makedirs("_dataset")

# Открываем видеофайл
video_path = "_video/video.mp4"
cap = cv2.VideoCapture(video_path)

# Переменная для хранения текущего порядкового номера фото
i = 1

# Переменная для отслеживания времени
time_elapsed = 0

# Читаем кадры из видео
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
            image_path = os.path.join("_dataset", f"{i}.jpg")
            cv2.imwrite(image_path, frame)

            # Увеличиваем порядковый номер
            i += 1

            # Сбрасываем время
            time_elapsed = 0

    else:
        # Конец видео
        break

# Закрываем видеофайл и освобождаем ресурсы
cap.release()
cv2.destroyAllWindows()
