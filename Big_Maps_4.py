import requests
import pygame
from io import BytesIO


# Собираем параметры для запроса к StaticMapsAPI:
def maps_load(dlt, long, latt):
    map_params = {
        "ll": ",".join([long, latt]),
        "z": dlt,
        "l": layer
    }
    response = requests.get("http://static-maps.yandex.ru/1.x/", params=map_params)
    return response


# Обновить значения масштаба
def update_z(symbol):
    num = eval("{} {} {}".format(z, symbol, 1))
    return (str(num), True) if 0 <= num <= 17 else (z, False)


# Обновление долготы
def longitude_update(symbol):
    num = eval("{} {} {}".format(longitude, symbol, move_map[z]))
    return (str(num), True) if -180 < num < 180 else (longitude, False)


# Обновление широты
def lattitude_update(symbol):
    num = eval("{} {} {}".format(lattitude, symbol, move_map[z]))
    return (str(num), True) if -85 <= num <= 85 else (lattitude, False)


longitude, lattitude = tuple(map(str, input("Введите координаты через пробел\n>>> ").split(" ")))

z = "15"  # Измените, чтобы увеличить или уменьшить масщтаб карты
update_img = False  # Обновить карту если изменён размер карты

# Для каждого масштаба карты свои изменения координат
move_map = {"1": 10, "2": 5, "3": 3, "4": 2, "5": 1, "6": 0.7, "7": 0.4, "8": 0.2, "9": 0.09, "10": 0.07,
            "11": 0.05, "12": 0.03, "13": 0.01, "14": 0.007, "15": 0.005, "16": 0.003, "17": 0.0009}

# Слои
layer_num = 0
layer_list = ["map", "sat", "sat,skl"]
layer = layer_list[layer_num]

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(BytesIO(maps_load(z, longitude, lattitude).content)), (0, 0))
wind = True

pygame.display.flip()
while wind:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # Масштабирование карты
            if event.key == pygame.K_PAGEUP:
                z, update_img = update_z("+")

            if event.key == pygame.K_PAGEDOWN:
                z, update_img = update_z("-")

            # Перемещение карты
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                longitude, update_img = longitude_update("-")

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                longitude, update_img = longitude_update("+")

            if event.key == pygame.K_w or event.key == pygame.K_UP:
                lattitude, update_img = lattitude_update("+")

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                lattitude, update_img = lattitude_update("-")

            # Переключение слоев
            if event.key == pygame.K_f:
                if layer_num + 1 <= len(layer_list) - 1:
                    layer_num += 1
                else:
                    layer_num = 0
                layer = layer_list[layer_num]
                update_img = True

        if event.type == pygame.QUIT:
            wind = False

    if update_img:
        screen.blit(pygame.image.load(BytesIO(maps_load(z, longitude, lattitude).content)),
                    (0, 0))
        update_img = False
        pygame.display.flip()

pygame.quit()
