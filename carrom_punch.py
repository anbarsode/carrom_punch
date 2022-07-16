import numpy as np
from scipy.integrate import solve_ivp
import sys

Rc = 15.5 # mm
Rs = 20.5 # mm
Mc = 5.0 # g
Ms = 15.0 # g

E_cs = 3.7e9 # Pa
E_cw = 6.0e9 # Pa
E_sw = 3.7e9 # Pa
L = 8.0 # mm, thickness of the coin

# precalculate quantities for optimization

F_coef_cs = np.pi / 4.0 * E_cs * L * 1e-6
Rcs = Rc + Rs
F_coef_cw = np.pi / 4.0 * E_cw * L * 1e-6
F_coef_sw = np.pi / 4.0 * E_sw * L * 1e-6

def Force_cs(r):
    if Rc + Rs > r:
        return F_coef_cs * (Rcs - r)
    else:
        return 0.0

def Force_cw(r):
    if Rc > r:
        return F_coef_cw * (Rc - r)
    else:
        return 0.0

def Force_sw(r):
    if Rs > r:
        return F_coef_sw * (Rs - r)
    else:
        return 0.0
    
def dYdt(t, Y):
    Xc, Vc, Xs, Vs = Y
    r_cs = np.abs(Xs-Xc)
    F_cs = Force_cs(r_cs)
    F_cw = Force_cw(Xc.imag) # wall at y=0
    F_sw = Force_sw(Xs.imag) # wall at y=0
    
    dXcdt = Vc
    dVcdt = (F_cs * (Xc - Xs) / r_cs + 1j * F_cw) * 1000.0 / Mc
    dXsdt = Vs
    dVsdt = (F_cs * (Xs - Xc) / r_cs + 1j * F_cs) * 1000.0 / Ms
    return [dXcdt, dVcdt, dXsdt, dVsdt]

def calculate_theta(Y0, t_max, t_more = 0.0):
    sol = solve_ivp(dYdt, [0 + t_more, t_max + t_more], Y0, method = 'DOP853', rtol = 1e-6)
    theta = 180.0 - np.angle(sol.y[1][-1]) * 180.0 / np.pi
    if theta < 180.0:
        return theta
    else: # sometimes, for large deltas, the coin might be moving downwards for a short amount of time, so simulate some more
        Y0 = [y[-1] for y in sol.y]
        return calculate_theta(Y0, t_max, t_more = t_max)

def generate_Y0(delta, alpha, beta = None, V = 1000.0, idelta = 1.2 * Rs):
    if beta is None: beta = alpha
    alpha *= np.pi / 180.0
    beta *= np.pi / 180.0
    Xc = 1j * (delta + Rc)
    Vc = 0.0 + 1j * 0.0
    Xs = Xc + Rc * np.exp(1j * alpha) + idelta * np.exp(1j * beta)
    Vs = -V * np.exp(1j * beta)
    if np.abs(Xs - Xc) > 1 + (Rc + Rs):
        return [Xc, Vc, Xs, Vs]
    else: # if you end up having the coin and striker intersecting each other, recalculate with a higher initial separation
        return generate_Y0(delta, alpha * 180 / np.pi, beta = beta * 180 / np.pi, V = V, idelta = idelta + 0.1 * Rs)

def unpack_input(s):
    d = s.split(':')
    if len(d) == 3:
        return np.linspace(float(d[0]), float(d[1]), int(d[2]))
    else:
        d = s.split('_')
        if len(d) == 3:
            return np.logspace(float(d[0]), float(d[1]), int(d[2]))
        else:
            d = s.split(',')
            d = np.array([float(x) for x in d])
            return d

deltas = unpack_input(sys.argv[1])
alphas = unpack_input(sys.argv[2])
betas = unpack_input(sys.argv[3])
Vs = unpack_input(sys.argv[4])

if len(sys.argv) != 5 or deltas.any() < 0 or alphas.any() < 0 or betas.any() < 0 or Vs.any() < 0 or alphas.any() > 90 or betas.any() > 90:
    print('Usage:\nGive 4 command line inputs corresponding to delta, alpha, beta, V\n\
    These should be 4 strings separated by spaces\n\
    For any variable, you can give single numbers like 0.5\n\
    or sequences like 0.5,0.6,0.7\n\
    or linspaces like 0.5:0.7:3\n\
    or logspaces like -1_2_100\n\
    For ex. This is a valid input: $ python carrom_punch.py -1_1_50 65 15:75:5 100,1000\n')
    raise ValueError('Invalid input')

print('# delta(mm) alpha(deg) beta(deg) V(mm/s) theta(deg)')
for delta in deltas:
    for alpha in alphas:
        for beta in betas:
            for V in Vs:
                Y0 = generate_Y0(delta, alpha, beta = beta, V = V)
                if Y0[2].imag < Rs:
                    print(delta, '%.2f' % alpha, '%.2f' % beta, V, 'Impossible configuration')
                else:
                    print(delta, '%.2f' % alpha, '%.2f' % beta, V, '%.2f' % calculate_theta(Y0, t_max = 100.0 / V))
