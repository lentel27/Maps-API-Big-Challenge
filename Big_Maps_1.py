import requests
import pygame
from io import BytesIO

# 65.534328 57.153033
longitude, lattitude = tuple(map(str, input("Введите координаты через пробел\n>>> ").split(" ")))
delta = "0.005"  # Измените, чтобы увеличить или уменьшить масщтаб карты

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([longitude, lattitude]),
    "spn": ",".join([delta, delta]),
    "l": "map"
}
response = requests.get("http://static-maps.yandex.ru/1.x/", params=map_params)

# Инициализируем pygame
pygame.init()

screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(BytesIO(response.content)), (0, 0))

pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass

pygame.quit()