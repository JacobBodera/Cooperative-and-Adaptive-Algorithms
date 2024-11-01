from random import uniform


# gene representation: [K_p, T_I, T_D]

W_ISE = 1
W_TR = 1
W_TS = 1
W_MP = 1

def rand_kp():
    return round(uniform(2, 18), 2)
def rand_ti():
    return round(uniform(1.05, 9.42), 2)
def rand_td():
    return round(uniform(0.26, 2.37), 2)
def random_gene():
    return [rand_kp(), rand_ti(), rand_td()]
