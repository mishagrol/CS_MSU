import numpy as np
from POD.crystal_structure import CrystalStructure

CONST = 0.8018993929636421
ALPHA = 10e-4
a0_true = 4.085
e_coh_true = -2.960
b_true = 1.08
c11_true = 1.32
c12_true = 0.97
c44_true = 0.51
b_pos = np.array([1 + ALPHA, 0, 0, 0, 1 + ALPHA, 0, 0, 0, 1 + ALPHA])
b_neg = np.array([1 - ALPHA, 0, 0, 0, 1 - ALPHA, 0, 0, 0, 1 - ALPHA])
c11_pos = np.array([1 + ALPHA, 0, 0, 0, 1 + ALPHA, 0, 0, 0, 1])
c11_neg = np.array([1 - ALPHA, 0, 0, 0, 1 - ALPHA, 0, 0, 0, 1])
c12_pos = np.array([1 + ALPHA, 0, 0, 0, 1 - ALPHA, 0, 0, 0, 1])
c12_neg = np.array([1 - ALPHA, 0, 0, 0, 1 + ALPHA, 0, 0, 0, 1])
c44_pos = np.array([1, ALPHA, 0, ALPHA, 1, 0, 0, 0, 1 / (1 - ALPHA * ALPHA)])
c44_neg = np.array([1, -ALPHA, 0, -ALPHA, 1, 0, 0, 0, 1 / (1 - ALPHA * ALPHA)])
identity_matrix = np.array([1., 0, 0, 0, 1., 0, 0, 0, 1.])


def get_derivative(dim, positive, negative, energy, a1, a0, ksi, p, q, r0):
    cs = CrystalStructure(dim)
    cs.face_centred_cubic("Ag")
    coh_energy = (
                         cs.calculate_energy(positive, a1, a0, ksi, p, q, r0)
                         + cs.calculate_energy(negative, a1, a0, ksi, p, q, r0)
                 ) / cs.get_size()
    return (coh_energy - 2. * energy) / (ALPHA * ALPHA)


def calculate_characteristics(m0, dim, energy, a1, a0, ksi, p, q, r0):
    v0 = m0 * m0 * m0 / 4

    sq_derivative_energy_b = get_derivative(dim, m0 * b_pos, m0 * b_neg, energy, a1, a0, ksi, p, q, r0)
    sq_derivative_energy_c11 = get_derivative(dim, m0 * c11_pos, m0 * c11_neg, energy, a1, a0, ksi, p, q, r0)
    sq_derivative_energy_c12 = get_derivative(dim, m0 * c12_pos, m0 * c12_neg, energy, a1, a0, ksi, p, q, r0)
    sq_derivative_energy_c44 = get_derivative(dim, m0 * c44_pos, m0 * c44_neg, energy, a1, a0, ksi, p, q, r0)

    b = 2. * sq_derivative_energy_b * CONST / (9. * v0)
    c11 = (sq_derivative_energy_c11 * CONST + sq_derivative_energy_c12 * CONST) / (2. * v0)
    c12 = (sq_derivative_energy_c11 * CONST - sq_derivative_energy_c12 * CONST) / (2. * v0)
    c44 = (sq_derivative_energy_c44 * CONST) / (2. * v0)

    return b, c11, c12, c44


def calculate_energy_sol(e_coh_a, e_coh_b, e_b, e_ab):
    return e_ab - e_b - e_coh_a + e_coh_b


def error_bb(w, dim, a0, e_coh):
    b, c11, c12, c44 = calculate_characteristics(a0, dim, e_coh, w[0], w[1], w[2], w[3], w[4], w[5])
    err = (a0 - a0_true) * (a0 - a0_true) / (a0_true * a0_true) + \
          (e_coh - e_coh_true) * (e_coh - e_coh_true) / (e_coh_true * e_coh_true) + \
          (b - b_true) * (b - b_true) / (b_true * b_true) + \
          (c11 - c11_true) * (c11 - c11_true) / (c11_true * c11_true) + \
          (c12 - c12_true) * (c12 - c12_true) / (c12_true * c12_true) + \
          (c44 - c44_true) * (c44 - c44_true) / (c44_true * c44_true)
    err = np.sqrt(err / 6)
    return err


def error_ab(w, dim, m0, A1, A0, KSI, P, Q, R0, e_coh_b, e_b):
    e_coh_a = 4.10
    e_true = 0.881
    A_B = CrystalStructure(dim)
    A_B.face_centred_cubic("Ag")
    A_B.change_atom("Cr")
    e_ab = A_B.calculate_energy(m0 * identity_matrix, A1, A0, KSI, P, Q, R0, w)
    e_sol = calculate_energy_sol(e_coh_a, e_coh_b, e_b, e_ab)
    err = (e_sol - e_true) * (e_sol - e_true) / (e_true * e_true)
    return err


def nrg(rij, o):
    energy_r = ((o[0] / o[5]) * (rij - o[5]) + o[1]) * np.exp(-1 * o[3] * (rij / o[5] - 1))
    energy_b = o[2] * o[2] * np.exp(-2 * o[4] * (rij / o[5] - 1))
    energy_b = -1 * np.sqrt(energy_b)
    return energy_r + energy_b
