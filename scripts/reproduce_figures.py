from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.integrate import solve_ivp
from scipy.signal import find_peaks

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
FIG = ROOT / 'figures'
FIG.mkdir(exist_ok=True)

plt.rcParams.update({
    'font.size': 8.5,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.dpi': 150,
    'savefig.dpi': 300,
})

# ----------------------------
# Representative limit cycles
# ----------------------------
def fhn(t, s, I=0.972, tau=12.5):
    v, w = s
    return [v - v**3/3 - w + I, (v + 0.7 - 0.8*w)/tau]

def ml_rhs(t, s, I, gCa, type1=False):
    V, w = s
    C, gK, gL = 20.0, 8.0, 2.0
    VCa, VK, VL = 120.0, -84.0, -60.0
    V1, V2 = -1.2, 18.0
    if type1:
        V3, V4, phi = 12.0, 17.4, 0.0667
    else:
        V3, V4, phi = 2.0, 30.0, 0.04
    minf = 0.5*(1+np.tanh((V-V1)/V2))
    winf = 0.5*(1+np.tanh((V-V3)/V4))
    tauw = 1/np.cosh((V-V3)/(2*V4))
    dV = (I - gCa*minf*(V-VCa) - gK*w*(V-VK) - gL*(V-VL))/C
    dw = phi*(winf-w)/tauw
    return [dV, dw]

def hr_fast(t, s, I=2.4, zbar=2.0):
    x, y = s
    return [y - x**3 + 3*x**2 - zbar + I, 1 - 5*x**2 - y]

def integrate_cycle(fun, y0, t_end, n=40000, min_sep=100):
    t_eval = np.linspace(0, t_end, n)
    sol = solve_ivp(fun, (0,t_end), y0, method='DOP853', t_eval=t_eval,
                    rtol=1e-9, atol=1e-11)
    x = sol.y[0]
    start = int(0.55*n)
    peaks, _ = find_peaks(x[start:], distance=min_sep, prominence=max(1e-7,0.05*np.std(x[start:])))
    peaks = peaks + start
    if len(peaks) >= 2:
        a,b = peaks[-2], peaks[-1]
        cyc = sol.y[:,a:b+1].T
    else:
        cyc = sol.y[:,-max(1000,n//20):].T
    return cyc

def whiten(cyc):
    mu = cyc.mean(axis=0)
    C = np.cov(cyc.T, bias=True)
    vals, vecs = np.linalg.eigh(C)
    vals = np.maximum(vals, 1e-12)
    W = vecs @ np.diag(vals**-0.5) @ vecs.T
    return (cyc-mu) @ W.T

cycles = []
cycles.append(('FHN', integrate_cycle(lambda t,s:fhn(t,s), [-1.0,-0.2], 1600, 36000, 250)))
cycles.append(('ML-II', integrate_cycle(lambda t,s:ml_rhs(t,s,110,4.4,False), [-50.0,0.05], 5000, 50000, 250)))
cycles.append(('ML-I', integrate_cycle(lambda t,s:ml_rhs(t,s,55,4.0,True), [-55.0,0.05], 5000, 50000, 250)))
cycles.append(('HR-fast', integrate_cycle(lambda t,s:hr_fast(t,s), [-1.0,-5.0], 1000, 40000, 180)))
th = np.linspace(0, 2*np.pi, 900, endpoint=False)
r = np.sqrt(1.1)
sl = np.c_[r*np.cos(th), r*np.sin(th)]
cycles.append(('Stuart--Landau', sl))

fig = plt.figure(figsize=(7.6, 3.5))
gs = fig.add_gridspec(2,5, height_ratios=[1.0, 0.4], hspace=0.2, wspace=0.15)
for i,(name, cyc) in enumerate(cycles):
    ax=fig.add_subplot(gs[0,i])
    Y=whiten(cyc)
    ax.plot(Y[:,0],Y[:,1],lw=1.25)
    idx=np.linspace(0,len(Y)-1,16,endpoint=False,dtype=int)
    ax.scatter(Y[idx,0],Y[idx,1],s=10,facecolors='white',edgecolors='black',linewidths=0.45,zorder=3)
    ax.set_title(name,fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect('equal', adjustable='datalim')
    for s in ('top','right','left','bottom'):
        ax.spines[s].set_visible(True)
        ax.spines[s].set_linewidth(0.5)

ax=fig.add_subplot(gs[1,:]); ax.axis('off')
boxes=[
    (0.125, 0.50, '16 time-uniform\nphase nodes'),
    (0.375, 0.50, 'Local fit\n16 directions\n$\\times$ 2 radii'),
    (0.625, 0.50, 'Estimate gradient\nand Hessian'),
    (0.875, 0.50, 'Held-out test\n12 directions\n$\\times$ 6 amplitudes'),
]

box_w = 0.17
box_h = 0.55
pad = 0.02

for x, y, txt in boxes:
    rect = patches.FancyBboxPatch(
        (x - box_w/2, y - box_h/2), box_w, box_h,
        boxstyle=f'round,pad={pad}', ec='0.35', fc='white', lw=1.0, transform=ax.transAxes, clip_on=False
    )
    ax.add_patch(rect)
    ax.text(x, y, txt, ha='center', va='center', transform=ax.transAxes, fontsize=8.5)

for i in range(3):
    x1 = boxes[i][0] + box_w/2 + pad + 0.005
    x2 = boxes[i+1][0] - box_w/2 - pad - 0.005
    ax.annotate('', xy=(x2, 0.50), xytext=(x1, 0.50), xycoords=ax.transAxes,
                arrowprops=dict(arrowstyle='->', lw=1.2))

for ext in ('pdf','png'):
    fig.savefig(FIG/f'fig1_design.{ext}',bbox_inches='tight')
plt.close(fig)

# ----------------------------
# Figure 2: aggregate errors
# ----------------------------
agg=pd.read_csv(DATA/'aggregate_error.csv')
eps=agg.epsilon.to_numpy(); e1=agg.first_order_error.to_numpy(); e2=agg.second_order_error.to_numpy()
fig,ax=plt.subplots(figsize=(5.5,3.9))
c_first = '#1f77b4'
c_sec = '#ff7f0e'
ax.loglog(eps,e1,'o-', color=c_first, label='first order')
ax.loglog(eps,e2,'s-', color=c_sec, label='Hessian-corrected')
# guides anchored at epsilon=.05
anchor=1
c2=e1[anchor]/eps[anchor]**2
c3=e2[anchor]/eps[anchor]**3
ax.loglog(eps,c2*eps**2,'--', color=c_first, lw=1.2, alpha=0.7, label=r'$\epsilon^2$ guide')
ax.loglog(eps,c3*eps**3,':', color=c_sec, lw=1.5, alpha=0.7, label=r'$\epsilon^3$ guide')
ax.set_xlabel(r'whitened perturbation amplitude $\epsilon$')
ax.set_ylabel('median absolute phase error (cycles)')
ax.legend(frameon=False, fontsize=9, loc='lower right')
for ext in ('pdf','png'):
    fig.savefig(FIG/f'fig2_error_scaling.{ext}',bbox_inches='tight')
plt.close(fig)

# ----------------------------
# Figure 3: setting gains + residual fidelity
# ----------------------------
g=pd.read_csv(DATA/'setting_gains.csv')
order=np.argsort(g.gain_eps_010.to_numpy())
gx=np.arange(len(g))
fig,axs=plt.subplots(1,2,figsize=(7.6, 3.8),gridspec_kw={'width_ratios':[1.4,1], 'wspace':0.3})
ax=axs[0]
for fam,sub in g.iloc[order].groupby('family',sort=False):
    pos=[np.where(order==i)[0][0] for i in sub.index]
    ax.scatter(pos,sub.gain_eps_010,s=25,label=fam)
    ax.scatter(pos,sub.gain_eps_025,s=30,facecolors='none',edgecolors=ax.collections[-1].get_facecolor(),linewidths=1.0)
ax.axhline(0,lw=1.0,ls='--',color='0.5')
ax.set_xlabel(r'setting (sorted by $\epsilon=0.10$ gain)')
ax.set_ylabel('reduction in median phase error (%)')
ax.set_ylim(20,105)
ax.legend(frameon=False,fontsize=8,ncol=2, loc='lower right')
ax.text(0.03,0.97,r'filled: $\epsilon=0.10$'+'\n'+r'open: $\epsilon=0.25$',transform=ax.transAxes,va='top',fontsize=8.5,
        bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='none', alpha=0.8))

ax=axs[1]
labels=['slope','R$^2$']
med=[0.9980,0.9834]; lo=[0.9974,0.9687]; hi=[1.0000,0.9920]
x=np.arange(2)
ax.errorbar(x,med,yerr=[np.array(med)-np.array(lo),np.array(hi)-np.array(med)],fmt='o',capsize=3,markersize=4,label='median [95% interval]')
ax.scatter(x,[0.785,0.581],marker='D',s=25,label='near-SNIC ML-I $I=40$',zorder=3)
ax.set_xticks(x, labels)
ax.set_ylim(0.5,1.05)
ax.set_ylabel(r'predictive statistic at $\epsilon=0.10$', fontsize=9)
ax.legend(frameon=False,fontsize=8,loc='lower left')
for ext in ('pdf','png'):
    fig.savefig(FIG/f'fig3_setting_results.{ext}',bbox_inches='tight')
plt.close(fig)

# ----------------------------
# Figure 4: affine stress test
# ----------------------------
a=pd.read_csv(DATA/'affine_summary.csv')
fig, ax = plt.subplots(figsize=(6.0, 3.6))
labels=['native\ngradient','native\nHessian','unit-box\ngradient','unit-box\nHessian']
vals=[a.loc[0,'native_gradient_spread'],a.loc[0,'native_hessian_spread'],a.loc[0,'unitbox_gradient_spread'],a.loc[0,'unitbox_hessian_spread']]
bars = ax.bar(np.arange(4),np.log10(vals), color='#4c72b0', alpha=0.85)
ax.set_xticks(np.arange(4))
ax.set_xticklabels(labels, fontsize=9)
ax.set_ylabel(r'$\log_{10}$ maximum descriptor spread', fontsize=10)
for i,v in enumerate(vals):
    ax.text(i,np.log10(v)+0.15,f'{v:.2e}',ha='center',va='bottom',fontsize=7)
ax.set_ylim(0,14.0)

# Integrate the text inside the right side of the main plot
text_str = (
    '$\\mathbf{Whitened\\ coordinates}$\n\n'
    'Worst relative discrepancy\n'
    '$\\mathbf{4.919\\times10^{-5}}$\n\n'
    'Largest condition number\n'
    '$\\mathbf{4.838\\times10^{3}}$'
)
ax.text(1.05, 0.5, text_str, transform=ax.transAxes, ha='left', va='center',
        fontsize=10.5, linespacing=1.5,
        bbox=dict(boxstyle='round,pad=0.8', fc='#f8f9fa', ec='#ced4da', lw=1.2))
for ext in ('pdf','png'):
    fig.savefig(FIG/f'fig4_affine_stress.{ext}',bbox_inches='tight')
plt.close(fig)

print('Generated figures in', FIG)
