"""fit legge quadratica della potenza"""

from pylab import *
from lab import fit_curve, xe

def correlazione(m):
    corr = m
    for i in range(len(m)):
        for j in range(len(m[0])):
            corr[i][j] = (m[i][j]) / sqrt(m[i][i] * m[j][j])
    return corr

grad, Vpp, dVpp = loadtxt('borcapDVTvsAng01.txt', unpack= True)
tgrad, tpower = loadtxt('borcapDVtaratura01.txt', unpack= True)

power = zeros(len(Vpp))
for i in range(len(power)):
    for j in range(len(tpower)):
        if grad[i] == tgrad[j]:
            power[i] = tpower[j]
            break
        
minerr = 0.8
dV = dVpp
for i in range(len(dVpp)):
    dV[i] = max(dVpp[i], minerr)

dpower = zeros(len(power))
for i in range(len(power)):
    if power[i] >= 100:
        dpower[i] = 1
    else:
        dpower[i] = 0.1

dpower = 0.03*power
    
dy = 0.68*0.5*dV
dx = dpower

def parabola(x, a):
    return a*x**2

out = fit_curve(parabola, power, Vpp, dy=dy, dx=dx, p0=[1], absolute_sigma=True)
par = out.par
cov = out.cov
err = sqrt(diag(cov))
print('a = %s' %xe(par, err))
print('chisq/dof = %d/%d = %.2f' %tuple((out.chisq, out.chisq_dof, out.chisq/out.chisq_dof)))
print('p_value = %.3f\n' % out.chisq_pvalue)

figure('potenza_alla2').set_tight_layout(True)
clf()
griglia = GridSpec(2, 1, height_ratios=[2,1])
subplot(griglia[0])
errorbar(power, Vpp, fmt='.k', yerr=dy, xerr=dx, markersize=4)
xx = linspace(min(power), max(power), 2000)
plot(xx, parabola(xx, *par), color='tab:green', label='\n$y = ax^2 \qquad a_{fit} = 0.4085(9) \; \\frac{V}{W^2}$\n$\\frac{\chi^2}{dof} = 1.27 \qquad p\_value = 8.2\%$ ')
xlim(0, 1.05*max(power))
ylabel('intensità seconda armonica [mV]')
xlabel('potenza [mW]')
legend(fontsize='large')
subplot(griglia[1])
indici = argsort(power)[::-1]
plot(power[indici], (Vpp[indici]-parabola(power[indici], *par))/dy, '.-k', markersize=4, linewidth=1)
ylabel('residui normalizzati')
xlabel('potenza [mW]')
xlim(0, 1.05*max(power))

def parabolab(x, a, b):
    return a*x**b

out = fit_curve(parabolab, power, Vpp, dy=dy, dx=dx, p0=[1,2], absolute_sigma=True)
par = out.par
cov = out.cov
err = sqrt(diag(cov))
print('[a b] = %s' %xe(par, err))
print('chisq/dof = %d/%d = %.2f' %tuple((out.chisq, out.chisq_dof, out.chisq/out.chisq_dof)))
print('p_value = %.3f' % out.chisq_pvalue)

figure('potenza_allab').set_tight_layout(True)
clf()
errorbar(power, Vpp, fmt='.k', yerr=dy, xerr=dx, markersize=4)
xx = linspace(min(power), max(power), 2000)
plot(xx, parabolab(xx, *par), color='tab:green', label='$y = ax^b$\n$a_{fit} = 0.466(12)$\n$b_{fit} = 1.979(4)$')
xlim(0, 1.05*max(power))
ylabel('intensità seconda armonica [mV]')
xlabel('potenza [mW]')
legend(fontsize='large')