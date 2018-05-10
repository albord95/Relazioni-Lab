"""fit angolo phase matching"""

from pylab import *
from lab import fit_curve, xe

def PM(theta, a, b, theta_m):
    arg = b*(theta-theta_m)
    return a*((sin(arg)/arg)**2)
def gaussiana(theta, a, b, theta_m):
    return a*exp(-1/2*((theta-theta_m)/b)**2)

primi, Vpp, dVpp = loadtxt('borcapDVTvsPM01.txt', unpack= True) #primi, mV, mV

minerr = 0.8
dV = dVpp
for i in range(len(dVpp)):
    dV[i] = max(dVpp[i], minerr)
    
#fit onesto
dy = 0.68*0.5*dVpp
dx = 0.68*0.5*ones(len(primi))
out = fit_curve(PM, primi, Vpp, dy=dy, dx=dx, p0=[500,0.02,150])
par = out.par
cov = out.cov

#fit senza code
cutlevel = 100 #mV
cutindex1 = 0
cutindex2 = len(Vpp)
for i in range(len(Vpp)-1):
    if (cutlevel < Vpp[i+1]) & (cutlevel >= Vpp[i]):
        cutindex1 = i
    if (cutlevel < Vpp[i]) & (cutlevel >= Vpp[i+1]):
        cutindex2 = i+1
out = fit_curve(PM, primi[cutindex1:cutindex2], Vpp[cutindex1:cutindex2], dy=dy[cutindex1:cutindex2], dx=dx[cutindex1:cutindex2], p0=[500,0.02,150])
parc = out.par
covc = out.cov
errc = sqrt(diag(covc))
print(out.par)
print('FIT SENZA CODE')
print('sinc: chisq/dof = %d/%d = %.2f' %tuple((out.chisq, out.chisq_dof, out.chisq/out.chisq_dof)))
out = fit_curve(gaussiana, primi[cutindex1:cutindex2], Vpp[cutindex1:cutindex2], dy=dy[cutindex1:cutindex2], p0=[500,50,150])
parg = out.par
covg = out.cov
print('gauss: chisq/dof = %d/%d = %.2f\n' %tuple((out.chisq, out.chisq_dof, out.chisq/out.chisq_dof)))



figure('phase_matching').set_tight_layout(True)
clf()
errorbar(primi, Vpp, yerr=dy, xerr=dx, fmt='.')
xx = linspace(min(primi), max(primi), 2000)
plot(xx, PM(xx, *par), label='fit con tutte le misure')
#$y = \\alpha \\frac{\sin^2(\\beta (\\theta - \\theta_m))}{[\\beta (\\theta - \\theta_m)]^2}$
xxx = linspace(min(primi[cutindex1:cutindex2]), max(primi[cutindex1:cutindex2]), 2000)
plot(xxx, PM(xxx, *parc), label='fit senza le code')
plot(xx, PM(xx, *parc), '--', color='tab:green', label='estrapolazione')
#plot(xxx, gaussiana(xxx, *parg))
bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.5)
text(313, 505, '$y = \\alpha \\frac{\sin^2(\\beta (\\theta - \\theta_m))}{[\\beta (\\theta - \\theta_m)]^2}$ \n $\\beta_{fit} = 1.377(2)\;gradi^{-1}$' %xe(parc[1]*60, errc[1]*60), fontsize='large', verticalalignment='top', horizontalalignment='right', bbox=bbox_props)
xlabel('angolo [\']')
ylabel('intensità seconda armonica [V]')
legend(fontsize='large', loc=2)

figure('sinc_gaussiana').set_tight_layout(True)
clf()
errorbar(primi, Vpp, yerr=dy, xerr=dx, fmt='.')
xx = linspace(min(primi), max(primi), 2000)
xxx = linspace(min(primi[cutindex1:cutindex2]), max(primi[cutindex1:cutindex2]), 2000)
plot(xxx, PM(xxx, *parc), color='tab:green', label='fit con $y = \\alpha \\frac{\sin^2(\\beta (\\theta - \\theta_m))}{[\\beta (\\theta - \\theta_m)]^2}$')
plot(xx, PM(xx, *parc), '--', color='tab:green')
plot(xxx, gaussiana(xxx, *parg), color='tab:red', label='fit con una gaussiana')
plot(xx, gaussiana(xx, *parg), '--', color='tab:red')
xlabel('angolo [\']')
ylabel('intensità seconda armonica [V]')
legend(fontsize='large', loc=2)

quanti = 10
for k in range(quanti):
    cutlevel = 0 + (250-0)/quanti*(k+1) #mV
    cutindex1 = 0
    cutindex2 = len(Vpp)
    for i in range(len(Vpp)-1):
        if (cutlevel < Vpp[i+1]) & (cutlevel >= Vpp[i]):
            cutindex1 = i
        if (cutlevel < Vpp[i]) & (cutlevel >= Vpp[i+1]):
            cutindex2 = i+1
    out = fit_curve(PM, primi[cutindex1:cutindex2], Vpp[cutindex1:cutindex2], dy=dy[cutindex1:cutindex2], p0=[500,0.1,150])
    parc = out.par
    covc = out.cov
    #print('FIT SENZA CODE')
    print('cut level =', cutlevel)
    print('sinc: chisq/dof = %d/%d = %.2f' %tuple((out.chisq, out.chisq_dof, out.chisq/out.chisq_dof)))
    out = fit_curve(gaussiana, primi[cutindex1:cutindex2], Vpp[cutindex1:cutindex2], dy=dy[cutindex1:cutindex2], p0=[500,10,150])
    parg = out.par
    covg = out.cov
    print('gauss: chisq/dof = %d/%d = %.2f' %tuple((out.chisq, out.chisq_dof, out.chisq/out.chisq_dof)))

