import numpy as np # For basic mathematical calculations
from scipy.integrate import solve_ivp # For solving differential equation of F = ma
from tqdm import tqdm # Gives a progress bar for loops
import os # for checking whether files exist

# For making pretty plots
import matplotlib.pyplot as plt
from matplotlib import rc, rcParams
rc_params = {'axes.labelsize': 18,
             'axes.titlesize': 15,
             'font.size': 15,
             'lines.linewidth' : 2,
             'legend.fontsize': 12,
             'xtick.labelsize': 14,
             'ytick.labelsize': 14
            }
rcParams.update(rc_params)

rc('text.latex', preamble='\\usepackage{txfonts}')
rc('text', usetex=True)
rc('font', family='serif')
rc('font', serif='times')
rc('mathtext', default='sf')
rc("lines", markeredgewidth=1)
rc("lines", linewidth=2)

Rc = 15.5 # mm
Rs = 20.5 # mm
Mc = 5.0 # g
Ms = 15.0 # g

def generate_Y0(delta, alpha, beta = None, V = 1000.0, idelta = 1.2 * Rs):
    if beta is None: beta = alpha
    alpha *= np.pi / 180.0
    beta *= np.pi / 180.0
    Xc = 1j * (delta + Rc)
    Vc = 0.0 + 1j * 0.0
    Xs = Xc + Rc * np.exp(1j * alpha) + idelta * np.exp(1j * beta)
    Vs = -V * np.exp(1j * beta)
    return [Xc, Vc, Xs, Vs]


'''
gap = 3.0
inc = 30.0
attack = 60.0
idelta = 1.2 * Rs
Y0 = generate_Y0(gap, inc, beta=attack, idelta=idelta, V = idelta)

fig,ax = plt.subplots(figsize=(7,7))
ax.plot([0],[0],alpha=0)
ax.add_patch(plt.Circle((Y0[0].real, Y0[0].imag), Rc, color='b'))
plt.text(Y0[0].real, Y0[0].imag-10, 'Coin', color='w', fontsize=20, weight='bold')
ax.add_patch(plt.Circle((Y0[2].real, Y0[2].imag), Rs, color='r'))
plt.text(Y0[2].real, Y0[2].imag-10, 'Striker', color='w', fontsize=20)
ax.set_aspect('equal')

plt.axhline(y=0, color='k', linestyle='-')
plt.text(1,70,'y-axis\n(imaginary)', color='k')
plt.axvline(x=0, color='k', linestyle='--')
plt.text(40,1,'Wall, x-axis\n(real)', color='k')
plt.xlim(right=60)
plt.ylim(top=75)

plt.axhline(y=0, xmin=0, xmax=0.6, color='g', linestyle=':')
plt.axhline(y=gap, xmin=0, xmax=0.6, color='g', linestyle=':')
plt.text(20, gap+1, r'$\delta$',color='g', fontsize=25)

plt.arrow(Y0[2].real, Y0[2].imag, Y0[3].real, Y0[3].imag, length_includes_head=True, width=0.5, head_width=3, color='yellow')
plt.arrow(Y0[0].real, Y0[0].imag,\
          (Rc * np.exp(1j * inc * np.pi / 180.0)).real, (Rc * np.exp(1j * inc * np.pi / 180.0)).imag,\
          length_includes_head=True, width=0.5, head_width=3, color='lawngreen')

plt.axhline(y=Y0[2].imag + Y0[3].imag, xmin=0.35, xmax=0.6, color='yellow', linestyle=':')
plt.axhline(y=Y0[0].imag, xmin=0.1, xmax=0.6, color='lawngreen', linestyle=':')
plt.text(Y0[2].real + Y0[3].real + 7, Y0[2].imag + Y0[3].imag + 3, r'$\beta$', color='yellow', fontsize=25)
plt.text(Y0[0].real + 5, Y0[0].imag + 1, r'$\alpha$', color='lawngreen', fontsize=25)

plt.arrow(Y0[0].real, Y0[0].imag, -8, 11, length_includes_head=True, width=0.5, head_width=3, color='c')
plt.text(Y0[0].real - 7, Y0[0].imag + 1, r'$\theta$', color='c', fontsize=25)

plt.axis('off')
#plt.savefig('./carrom_punch_coordinates.png')
plt.show()'''




gap = 1.0
inc = 65.0
attack = 60.0
idelta = 1.2 * Rs
Y0 = generate_Y0(gap, inc, beta=attack, idelta=idelta, V = idelta)

fig,ax = plt.subplots(figsize=(5,5))
ax.plot([0],[0],alpha=0)
ax.add_patch(plt.Circle((Y0[0].real, Y0[0].imag), Rc, color='b'))
plt.text(Y0[0].real-2, Y0[0].imag-10, 'Coin', color='w', fontsize=20, weight='bold')

plt.axhline(y=0, color='k')
plt.text(15,1,'Wall', color='k')

plt.axhline(y=0, xmin=0.3, xmax=0.7, color='g', linestyle=':')
plt.axhline(y=gap, xmin=0.3, xmax=0.7, color='g', linestyle=':')
plt.text(7, gap, r'gap',color='g', fontsize=20)

plt.arrow(Y0[0].real, Y0[0].imag,\
          (Rc * np.exp(1j * inc * np.pi / 180.0)).real, (Rc * np.exp(1j * inc * np.pi / 180.0)).imag,\
          length_includes_head=True, width=0.5, head_width=3, color='lawngreen')
plt.axhline(y=Y0[0].imag, xmin=0.2, xmax=0.8, color='lawngreen', linestyle=':')
plt.text(Y0[0].real + 3, Y0[0].imag + 1, r'$65^\circ$', color='lawngreen', fontsize=25)

plt.scatter([Y0[0].real + (Rc * np.exp(1j * inc * np.pi / 180.0)).real], [Y0[0].imag + (Rc * np.exp(1j * inc * np.pi / 180.0)).imag], marker='*', color='r', s=300)
plt.text(Y0[0].real + (Rc * np.exp(1j * inc * np.pi / 180.0)).real +1,\
         Y0[0].imag + (Rc * np.exp(1j * inc * np.pi / 180.0)).imag +1,\
         'HIT ME!', color='m', fontsize=30)

ax.set_aspect('equal')
plt.axis('off')
plt.savefig('./optimum_poi.png')
plt.show()