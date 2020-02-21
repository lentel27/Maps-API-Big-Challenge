import requests
import pygame
from io import BytesIO


# Собираем параметры для запроса к StaticMapsAPI:
def maps_load(dlt):
    map_params = {
        "ll": ",".join([longitude, lattitude]),
        "z": dlt,
        "l": "map"
    }
    response = requests.get("http://static-maps.yandex.ru/1.x/", params=map_params)
    return response


# Обновить значения масштаба
def update_z(symbol):
    return (str(eval("{} {} {}".format(z, symbol, 1))), True) if 0 <= eval("{} {} {}".format(z, symbol, 1)) <= 17 else\
        (z, False)


longitude, lattitude = tuple(map(str, input("Введите координаты через пробел\n>>> ").split(" ")))

z = "15"  # Измените, чтобы увеличить или уменьшить масщтаб карты
update_img = False  # Обновить карту если изменён размер карты

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(BytesIO(maps_load(z).content)), (0, 0))
wind = True

pygame.display.flip()
while wind:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # Приблизить
            if event.key == pygame.K_PAGEUP:
                z, update_img = update_z("+")

            # Уменьшить
            if event.key == pygame.K_PAGEDOWN:
                z, update_img = update_z("-")

        if event.type == pygame.QUIT:
            wind = False

    if update_img:
        screen.blit(pygame.image.load(BytesIO(maps_load(z).content)), (0, 0))
        update_img = False
        pygame.display.flip()

pygame.quit()
