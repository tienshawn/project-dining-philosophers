import multiprocessing
import logging
from random import uniform
import time
from typing import List, Dict, Tuple, Any

from .utils import logger

from ._states import PhilosopherState
from .forks import Fork
class Sword:
    def __init__(self, canvas, x, y, image, id_):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image = image
        self.id_ = id_
        self.object = canvas.create_image(x, y, image=image)
        self.target_x = x
        self.target_y = y

    def move_to(self, target_x, target_y):
        """Đặt mục tiêu di chuyển thanh kiếm."""
        self.target_x = target_x
        self.target_y = target_y

    def update_position(self, step=5):
        """Cập nhật vị trí thanh kiếm từng bước để di chuyển về mục tiêu."""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = (dx**2 + dy**2)**0.5

        if distance > step:
            dx = dx / distance * step
            dy = dy / distance * step
            self.canvas.move(self.object, dx, dy)
            self.x += dx
            self.y += dy
        else:
            # Nếu kiếm đã đạt mục tiêu, đặt đúng vị trí cuối cùng
            self.canvas.coords(self.object, self.target_x, self.target_y)
            self.x = self.target_x
            self.y = self.target_y
class Philosopher(multiprocessing.Process):
    EAT_TIMES_UNTIL_FULL = 3

    def __init__(
        self, 
        id_: int,
        state,
        forks: Tuple[Fork, Fork],
        x: int = 0,  # Tọa độ x mặc định
        y: int = 0,  # Tọa độ y mặc định
        ):
        multiprocessing.Process.__init__(self)
        
        self.id_ = id_
        self.state = state
        self.forks = forks
        self._full = 0
    
    def run(self):
        while self._full < self.EAT_TIMES_UNTIL_FULL:
            self.think()
            self.eat()
        logger.info("{:<13}".format(str(self)) + f" full")
        return

    def eat(self):
        # Set hungry state here
        # PROCESS SYNCH HERE
        
        self.state.value = PhilosopherState.EATING
        self._full += 1
        logger.info("{:<13}".format(str(self)) + f" {self.state.value.value}" + f" ({self._full})")
        time.sleep(uniform(1.2, 5.0))

    def think(self):
        self.state.value = PhilosopherState.THINKING
        logger.info("{:<13}".format(str(self)) + f" {self.state.value.value}")
        time.sleep(uniform(1.2, 5.0))

    def __repr__(self) -> str:
        return f'[PHILOSOPHER {self.id_:02}]'