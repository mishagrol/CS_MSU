import numpy as np
from POD.atom import Atom
from numba import jit


class CrystalStructure:
    def __init__(self, dim):
        self.dim = dim
        self.fcc = []

    def face_centred_cubic(self, _type):
        for i in range(self.dim):
            for j in range(self.dim):
                for k in range(self.dim):
                    self.fcc.append(Atom(_type, i, j, k))
                    self.fcc.append(Atom(_type, i, j + 0.5, k + 0.5))
                    self.fcc.append(Atom(_type, i + 0.5, j + 0.5, k))
                    self.fcc.append(Atom(_type, i + 0.5, j, k + 0.5))

    def calculate_energy(self, trans, a1, a0, ksi, p, q, r0, o=None):
        if o is None:
            o = []
        full_energy = 0.
        t = Atom().transform(trans)
        cutoff = 1.7 * max(t.x, max(t.y, t.z))
        for X1 in self.fcc:
            energy_r = 0.
            energy_b = 0.
            for X2 in self.fcc:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        for dz in range(-1, 2):
                            if X1 != X2 or dx != 0 or dy != 0 or dz != 0:
                                rij = ((X2 + Atom('', dx * self.dim, dy * self.dim, dz * self.dim)).transform(trans) -
                                       X1.transform(trans)).distance()
                            if rij < cutoff:
                                if X1.type == "Ag" and X2.type == "Ag":
                                    energy_r += ((a1 / r0) * (rij - r0) + a0) * np.exp(-1 * p * (rij / r0 - 1))
                                    energy_b += ksi * ksi * np.exp(-2 * q * (rij / r0 - 1))
                                elif X1.type == "Cr" and X2.type == "Ag" or X1.type == "Ag" and X2.type == "Cr":
                                    energy_r += ((o[0] / o[5]) * (rij - o[5]) + o[1]) *\
                                                np.exp(-1 * o[3] * (rij / o[5] - 1))
                                    energy_b += o[2] * o[2] * np.exp(-2 * o[4] * (rij / o[5] - 1))
            energy_b = -1 * np.sqrt(energy_b)
            full_energy += energy_r + energy_b
        return full_energy

    def get_size(self):
        return len(self.fcc)

    def change_atom(self, t):
        self.fcc[13].type = t
