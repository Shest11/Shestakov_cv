import cv2
import numpy as np
import random

cv2.namedWindow("Game", cv2.WINDOW_GUI_NORMAL)
cap = cv2.VideoCapture(0)

click_pos = None
colors_hsv = []
random_order = random.sample([0, 1, 2, 3], 4)

def on_click(event, x, y, flags, param):
    global click_pos
    if event == cv2.EVENT_LBUTTONDOWN:
        click_pos = (x, y)

cv2.setMouseCallback("Game", on_click)

# Функция поиска одного шара по его HSV цвету
def find_ball(hsv_img, color):
    lower = np.clip(color * 0.9, 0, 255).astype("u1")
    upper = np.clip(color * 1.1, 0, 255).astype("u1")
    upper[1:] = 255  # Сразу выставляем S и V в максимум

    mask = cv2.inRange(hsv_img, lower, upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        (x, y), r = cv2.minEnclosingCircle(c)
        if r > 10:
            return int(x), int(y), int(r)
    return None

while True:
    ret, frame = cap.read()
    if not ret or cv2.waitKey(30) & 0xFF == ord('q'):
        break

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Обработка клика во время калибровки
    if click_pos and len(colors_hsv) < 4:
        colors_hsv.append(hsv[click_pos[1], click_pos[0]])
        click_pos = None

    # Поиск всех откалиброванных шаров
    ball_centers = []
    for i, color in enumerate(colors_hsv):
        ball_data = find_ball(hsv, color)
        if ball_data:
            x, y, r = ball_data
            ball_centers.append((x, y, i))

            # Визуализация зеленый цвет кружков при калибровке, желтый при готовности
            is_ready = len(colors_hsv) == 4
            cv2.circle(frame, (x, y), r, (0, 255, 255) if is_ready else (0, 255, 0), 2)
            cv2.putText(frame, str(i + 1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Проверка на победу
    if len(ball_centers) == 4:
        # Сортируем по Y
        ball_centers.sort(key=lambda ball: ball[1])

        top_balls = ball_centers[:2]
        bottom_balls = ball_centers[2:]

        # Сортируем верхние по X
        top_balls.sort(key=lambda ball: ball[0])
        # Сортируем нижние по X
        bottom_balls.sort(key=lambda ball: ball[0])

        current_order = []

        # Добавляем номера верхних шаров
        for ball in top_balls:
            ball_number = ball[2]
            current_order.append(ball_number)

        # Добавляем номера нижних шаров
        for ball in bottom_balls:
            ball_number = ball[2]
            current_order.append(ball_number)

        # Проверяем, совпадает ли порядок с загаданным
        if current_order == random_order:
            cv2.putText(frame, "OTGADAL!", (frame.shape[1] // 2 - 200, frame.shape[0] // 2),
                        cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 255, 0), 4)

    cv2.imshow("Game", frame)

cap.release()
cv2.destroyAllWindows()
