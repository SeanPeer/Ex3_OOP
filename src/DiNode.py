import random


class DiNode:

    def __init__(self, id_: int, pos: tuple):
        self.pos = pos
        self.id = id_
        self.score = float('inf')

        self.ins = {}
        self.outs = {}

    def update_position(self, v_size):
        if self.pos is None:
            x, y, z = random.randint(0, v_size+5), random.uniform(0, v_size+5), 0
            self.pos = (x, y, z)

    def add_into(self, id2: int, w: float) -> bool:
        if not self.check_edge_in(id2):

            self.ins[id2] = w

            return True
        return False

    def add_outo(self, id2: int, w: float) -> bool:
        if not self.check_edge_out(id2):

            self.outs[id2] = w

            return True
        return False

    def disconnect_in(self, id2: int):
        del self.ins[id2]

    def disconnect_out(self, id2: int):
        del self.outs[id2]

    def check_edge_in(self, ni_id: int) -> bool:
        return ni_id in self.ins

    def check_edge_out(self, ni_id: int) -> bool:
        return ni_id in self.outs

    def __repr__(self):
        return f"{self.id}: |edges out| {len(self.outs)} |edges in| {len(self.ins)}"

    def __str__(self):
        return f"{self.id}: |edges out| {len(self.outs)} |edges in| {len(self.ins)}"
