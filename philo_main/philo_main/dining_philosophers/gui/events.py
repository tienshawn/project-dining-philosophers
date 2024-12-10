import tkinter as tk
import time
from multiprocessing import Process

from .gui import GUI, rel
from ..solutions import *
from ..table import Table
from .._states import PhilosopherState

class EventHandler:
    TABLES = [ArbitratorTable, CMTable, HierachyTable, LimitTable]
    STATE_IMG = {
        # PhilosopherState.THINKING: tk.PhotoImage(file=rel("philosopher_thinking.png")),
        # PhilosopherState.EATING: tk.PhotoImage(file=rel("philosopher_eating.png")),
        # PhilosopherState.HUNGRY: tk.PhotoImage(file=rel("philosopher_hungry.png")),
        # "default": tk.PhotoImage(file=rel("philosopher.png"))
          0: {  # Triết gia 0
        PhilosopherState.THINKING: tk.PhotoImage(file=rel("anya1_thinking.png")),
        PhilosopherState.EATING: tk.PhotoImage(file=rel("anya1_eating.png")),
        PhilosopherState.HUNGRY: tk.PhotoImage(file=rel("anya1_hungry.png")),
        "default": tk.PhotoImage(file=rel("anya1.png")),
        },
        1: {  # Triết gia 1
        PhilosopherState.THINKING: tk.PhotoImage(file=rel("anya2_thinking.png")),
        PhilosopherState.EATING: tk.PhotoImage(file=rel("anya2_eating.png")),
        PhilosopherState.HUNGRY: tk.PhotoImage(file=rel("anya2_hungry.png")),
        "default": tk.PhotoImage(file=rel("anya2.png")),
        },
        2: {  # Triết gia 2
        PhilosopherState.THINKING: tk.PhotoImage(file=rel("anya3_thinking.png")),
        PhilosopherState.EATING: tk.PhotoImage(file=rel("anya3_eating.png")),
        PhilosopherState.HUNGRY: tk.PhotoImage(file=rel("anya3_hungry.png")),
        "default": tk.PhotoImage(file=rel("anya3.png")),
        },
        3: {  # Triết gia 3
        PhilosopherState.THINKING: tk.PhotoImage(file=rel("anya4_thinking.png")),
        PhilosopherState.EATING: tk.PhotoImage(file=rel("anya4_eating.png")),
        PhilosopherState.HUNGRY: tk.PhotoImage(file=rel("anya4_hungry.png")),
        "default": tk.PhotoImage(file=rel("anya4.png")),
        },
        4: {  # Triết gia 4
        PhilosopherState.THINKING: tk.PhotoImage(file=rel("anya5_thinking.png")),
        PhilosopherState.EATING: tk.PhotoImage(file=rel("anya5_eating.png")),
        PhilosopherState.HUNGRY: tk.PhotoImage(file=rel("anya5_hungry.png")),
        "default": tk.PhotoImage(file=rel("anya5.png")),
        },
    }

    def __init__(self, gui: GUI):
        self.gui = gui
        self.kernel: Table = ArbitratorTable(self)

    def btn_select_method(self):
        for i in range(len(self.TABLES)):
            self.gui._btns[i].bind("<Button-1>", lambda e: self._reset_kernel(self.TABLES[i]))
    
    def btn_start(self):
        self.gui._btn_start.bind("<Button-1>", lambda e: self._start_dining())

    def _reset_kernel(self, table: Table):
        self.gui._canvas.delete("All")
        self.kernel = table(self)
        self.gui.default_build()

    def _start_dining(self):
        self.kernel.start_dining()

    def _animate_dining(self, dining_table: Table):
        # phil_coors = [(560, 540), (570, 200), (200, 100), (70, 390), (270, 655)]
        # for id_, philosopher in enumerate(dining_table._philosophers):
        #     philosopher.x, philosopher.y = phil_coors[id_]

        stop = False
        while not stop:
            all_alive = False
            for philosopher in dining_table._philosophers:
                cur_state = philosopher.is_alive()
                if cur_state:
                    self.gui._canvas.itemconfig(
                        self.gui._philosophers[philosopher.id_],
                        image=self.STATE_IMG[philosopher.id_][philosopher.state.value]
                    )
                
                    if philosopher.state == PhilosopherState.HUNGRY:
                    # Di chuyển kiếm tới triết gia
                        self.gui._swords[philosopher.id_].move_to(
                            philosopher.x, philosopher.y
                        )
                    elif philosopher.state == PhilosopherState.THINKING:
                    # Trả kiếm về vị trí trên bàn
                        self.gui._swords[philosopher.id_].move_to(
                            self.gui._swords[philosopher.id_].x, self.gui._swords[philosopher.id_].y
                        )
                else:
                    self.gui._canvas.itemconfig(
                        self.gui._philosophers[philosopher.id_],
                        image=self.STATE_IMG[philosopher.id_]["default"]
                    )

                self.gui.window.update()
                all_alive = all_alive or cur_state

        # Cập nhật vị trí cho tất cả các thanh kiếm
            for sword in self.gui._swords:
                sword.update_position()
            
            stop = stop or not all_alive
            time.sleep(0.05)

                
                
                    


