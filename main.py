import math
import random
import json
import csv
import os

init_pos_limit = 10.0
sheep_move_dist = 0.5
wolf_move_dist = 1.0
sheep_number = 15
turn_number = 50


class Wolf:
    def __init__(self, position_x, position_y):
        self.x = position_x
        self.y = position_y

    def find_nearest_ship(self, sheep_list):
        index = -1
        distance = math.inf
        for sheep in sheep_list:
            if sheep.alive:
                dist = math.sqrt(pow((self.x - sheep.x), 2) + pow((self.y - sheep.y), 2))
                if dist < distance:
                    distance = dist
                    index = sheep_list.index(sheep)
        return distance, index

    def move(self, sheep_list):
        distance, index = self.find_nearest_ship(sheep_list)
        message = ""
        if distance <= wolf_move_dist:
            self.x = sheep_list[index].x
            self.y = sheep_list[index].y
            sheep_list[index].alive = False
            message = "wilk pożarł owcę o indeksie: " + str(index)
        else:
            self.x += ((sheep_list[index].x - self.x) / distance) * wolf_move_dist
            self.y += ((sheep_list[index].y - self.y) / distance) * wolf_move_dist
            message = "wilk goni owcę o indeksie: " + str(index)
        return message


class Sheep:
    def __init__(self, position_x, position_y, alive=True):
        self.x = position_x
        self.y = position_y
        self.alive = alive

    def move(self, sheep_move_distance):
        direction = random.randrange(1, 4)
        if direction == 1:
            self.x += sheep_move_distance
        elif direction == 2:
            self.x -= sheep_move_distance
        elif direction == 3:
            self.y += sheep_move_distance
        else:
            self.y -= sheep_move_distance


def count_alive(sheep_list):
    alive_number = 0
    for sheep in sheep_list:
        if sheep.alive:
            alive_number += 1
    return alive_number


def create_dictionary(sheep_list, wolf, turn):
    sheep_position = []
    for sheep in sheep_list:
        if sheep.alive:
            sheep_position.append([sheep.x, sheep.y])
        else:
            sheep_position.append(None)
    dictionary = {
        "round_no": turn,
        "wolf_pos": [wolf.x, wolf.y],
        "sheep_pos": sheep_position
    }
    return dictionary


def write_to_json(dictionary):
    file = "pos.json"
    with open(file, "a") as json_file:
        json.dump(dictionary, json_file, indent=4)


def write_to_csv(prepare, sheep_list, turn_number=-1):
    file = "alive.csv"

    if prepare:
        with open(file, "w") as csv_file:
            writer = csv.writer(csv_file)
            row = ["Numer tury", " Liczba żywych owiec"]
            writer.writerow(row)
    else:
        alive = count_alive(sheep_list)
        with open(file, "a+", newline='') as  csv_file:
            writer = csv.writer(csv_file)
            row = [turn_number, alive]
            writer.writerow(row)


def initialize(sheep_list):
    for i in range(sheep_number):
        sheep_list.append(Sheep(random.uniform(-init_pos_limit, init_pos_limit),
                                random.uniform(-init_pos_limit, init_pos_limit)))


def simulate(wolf, sheep_list):
    if os.path.exists("pos.json"):
        os.remove("pos.json")
    flag = True
    write_to_csv(True, sheep_list)
    for i in range(1, turn_number + 1):
        if flag:
            if count_alive(sheep_list) == 0:
                print("Wilk pożarł wszystkie owce!")
                flag = False
            else:
                for sheep in sheep_list:
                    sheep.move(sheep_move_dist)
                print("Tura numer: " + str(i) + " pozycja wilka, x: " + str(round(wolf.x, 3)) + ", y: " + str(
                    round(wolf.y, 3)) + ", " + "liczba żywych owiec: " + str(count_alive(sheep_list)) + ", " + (
                          wolf.move(sheep_list)))
                write_to_csv(False, sheep_list, i)
                dict = create_dictionary(sheep_list, wolf, i)
                write_to_json(dict)


def main():
    wolf = Wolf(0.0, 0.0)
    sheep_list = []
    initialize(sheep_list)
    simulate(wolf, sheep_list)


if __name__ == '__main__':
    main()
