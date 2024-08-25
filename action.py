from enum import Enum
from typing import Tuple
import pyautogui
from config.v1 import config


class Pixel:
    def __init__(self, px: Tuple[int, ...]):
        self.px = px

    def __str__(self):
        return f'({self.px[0]}, {self.px[1]}, {self.px[2]})'

    @staticmethod
    def in_deviation(a: int, b: int, deviation: int) -> bool:
        if a > b:
            return b + deviation > a
        return a + deviation >= b

    def like(self, px: 'Pixel', deviation=20) -> bool:
        if len(self.px) != len(px.px):
            return False
        for i in range(len(px.px)):
            if not self.in_deviation(self.px[i], px.px[i], deviation):
                return False
        return True


def get_color(x: int, y: int) -> Pixel:
    im = pyautogui.screenshot()
    return Pixel(im.getpixel((x, y)))


class Page:
    def __str__(self) -> str:
        money = ''
        if self.need_gold:
            money += 'gold'
        if self.need_diamond:
            money += 'diamond'
        return (
            f'money={money} white={self.white_card} blue={self.blue_card} '
            f'purple={self.purple_card} yellow={self.yellow_card} red={self.red_card}')

    def __init__(self):
        self.need_diamond = False
        self.need_gold = False
        self.white_card = 0
        self.blue_card = 0
        self.purple_card = 0
        self.yellow_card = 0
        self.red_card = 0

        self.im = pyautogui.screenshot()

        self.update_state()

        self.update_card_num(*config["pixel"]["range"]["card_1"])
        self.update_card_num(*config["pixel"]["range"]["card_2"])
        self.update_card_num(*config["pixel"]["range"]["card_3"])
        self.total_card_num = self.white_card + self.blue_card + self.purple_card + self.yellow_card + self.red_card

    def update_state(self):
        start, end = config["pixel"]["range"]["gold"]
        if self.find_color_in_range(start, end, Pixel(config["pixel"]["color"]["gold"])):
            self.need_diamond = True

        start, end = config["pixel"]["range"]["diamond"]
        if self.find_color_in_range(start, end, Pixel(config["pixel"]["color"]["diamond"])):
            self.need_gold = True

    def find_color_in_range(self, start: tuple, end: tuple, color: Pixel) -> bool:
        def compare_color(x: int, y: int) -> bool:
            px = Pixel(self.im.getpixel((x, y)))
            return px.like(color)

        if compare_color((start[0] + end[0]) / 2, (start[1] + end[1]) / 2):
            return True  # find color in center
        x, y = start[0], start[1]
        while x < end[0] and y < end[1]:
            if compare_color(x, y):
                return True
            x, y = x + 1, y + 1
        x, y = end[0], end[1]
        while x > start[0] and y > start[1]:
            if compare_color(x, y):
                return True
            x, y = x - 1, y - 1
        return False

    def update_card_num(self, start: tuple, end: tuple) -> bool:
        if self.find_color_in_range(start, end, Pixel(config["pixel"]["color"]["white"])):
            self.white_card += 1
            return True
        if self.find_color_in_range(start, end, Pixel(config["pixel"]["color"]["blue"])):
            self.blue_card += 1
            return True
        if self.find_color_in_range(start, end, Pixel(config["pixel"]["color"]["purple"])):
            self.purple_card += 1
            return True
        if self.find_color_in_range(start, end, Pixel(config["pixel"]["color"]["yellow"])):
            self.yellow_card += 1
            return True
        if self.find_color_in_range(start, end, Pixel(config["pixel"]["color"]["red"])):
            self.red_card += 1
            return True
        return False

    def is_unknown_status(self):
        return (not self.need_diamond and not self.need_gold) or self.total_card_num != 3

    def need_confirm(self) -> bool:
        px1 = Pixel(self.im.getpixel(config["pixel"]["pos"]["confirm_no"]))
        px2 = Pixel(self.im.getpixel(config["pixel"]["pos"]["confirm_yes"]))
        px3 = Pixel(self.im.getpixel(config["pixel"]["pos"]["confirm_bottom"]))
        return (px1.like(Pixel(config["pixel"]["color"]["confirm_no"])) and
                px2.like(Pixel(config["pixel"]["color"]["confirm_yes"])) and
                px3.like(Pixel(config["pixel"]["color"]["confirm_bottom"])))

    def is_correct_bottom(self) -> bool:
        px = Pixel(self.im.getpixel(config["pixel"]["pos"]["bottom_bar"]))
        print(px)
        return px.like(Pixel(config["pixel"]["color"]["bottom_bar"]))


class Action:
    # 招募
    @staticmethod
    def enlist():
        # 像素点位置不等同于鼠标坐标系位置
        pyautogui.moveTo(*config["click"]["enlist"])
        pyautogui.click()

    # 加注
    @staticmethod
    def increase_bet():
        pyautogui.moveTo(*config["click"]["increase_bet"])
        pyautogui.click()
        pyautogui.moveRel(0, -20)
        pyautogui.click()

    # 放弃
    @staticmethod
    def give_up():
        pyautogui.moveTo(*config["click"]["give_up"])
        pyautogui.click()

    # 确认放弃招募剩下的高品质角色
    @staticmethod
    def confirm_give_up():
        pyautogui.moveTo(*config["click"]["confirm_give_up"])
        pyautogui.click()

    # 鼠标离开游戏窗口
    @staticmethod
    def mouse_leaved() -> bool:
        px = pyautogui.position()
        return px.x > config["click"]["border"][0] or px.y > config["click"]["border"][1]

    # 鼠标复位，避免干扰像素判定
    @staticmethod
    def move_title(click=False):
        pyautogui.moveTo(*config["click"]["title_bar"])
        if click:
            pyautogui.click()

    @staticmethod
    def move_bottom(click=False):
        pyautogui.moveTo(*config["click"]["bottom_bar"])
        if click:
            pyautogui.click()
