import cv2
import numpy as np
import time
import pyautogui
from mss import MSS

pyautogui.PAUSE = 0

sct = MSS()
print("Открой игру")
time.sleep(5)

# стартовый прыжок
pyautogui.press('space')

# область захвата экрана
monitor = {
    "top": 240,
    "left": 350,
    "width": 600,
    "height": 150
}

while True:
    # скрин
    img = np.array(sct.grab(monitor))

    # бинаризация
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # зоны проверки препятствий
    ground_zone = thresh[85:120, 100:200]
    air_zone = thresh[30:85, 100:200]

    # считаем белые пиксели
    ground_pixels = cv2.countNonZero(ground_zone)
    air_pixels = cv2.countNonZero(air_zone)


    # если найден объект
    if ground_pixels > 80:
        pyautogui.keyDown('space')
        # Ждём нужное количество миллисекунд (чем дольше, тем выше прыжок)
        time.sleep(0.1)
        # Отпускаем клавишу
        pyautogui.keyUp('space')

    if air_pixels > 50:
        pyautogui.keyDown('down')
        # Ждём нужное количество миллисекунд (чем дольше, тем дольше сидит)
        time.sleep(0.3)
        # Отпускаем клавишу
        pyautogui.keyUp('down')

    # рисуем зеленый прямоугольник
    cv2.rectangle(img, (120, 85), (200, 120), (0, 255, 0), 2)
    cv2.rectangle(img, (120, 30), (200, 84), (255, 0, 0), 2)
    cv2.imshow("Dino", img)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
