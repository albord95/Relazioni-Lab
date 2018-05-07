"""fit in regimi di alta (lineare) e bassa (quadratico) potenza"""

from pylab import *
from lab import fit_curve, xe

def correlazione(m):
    corr = m
    for i in range(len(m)):
        for j in range(len(m[0])):
            corr[i][j] = (m[i][j]) / sqrt(m[i][i] * m[j][j])
    return corr

grad, Vpp, dVpp = loadtxt('borcapVLTvsAng01.txt', unpack= True)
tgrad, tpower = loadtxt('borcapVLtaratura01.txt', unpack= True)

figure('potenza_allab').set_tight_layout(True)
clf()
figure('potenza_alla2').set_tight_layout(True)
clf()

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
    
dy = sqrt((0.68*0.5*dV)**2 + (0.68*0.5*dpower)**2)

##estraggo indici misure a bassa potenza
altezza = 5
larghezza = 3
a_fit = []
b_fit = []
da_fit = []
db_fit = []
p_max = []
for pmax in range(5,20):
    indici_bassi = []
    for i in range(len(power)):
        if power[i] < pmax:
            indici_bassi.append(i)
    indici_bassi = array(indici_bassi)
    p_max.append(max(power[indici_bassi]))

##fit bassa potenza 
    def parabola(x, a):
        return a*x**2
    
    out = fit_curve(parabola, power[indici_bassi], Vpp[indici_bassi], dy=dy[indici_bassi], p0=[1], absolute_sigma=True)
    par = out.par
    cov = out.cov
    err = sqrt(diag(cov))
    a_fit.append(par[0])
    da_fit.append(err[0])
    chisq = out.chisq
    p_value = out.chisq_pvalue
    dof = out.chisq_dof
    print('a = %s' %xe(par, err))
    print('chisq/dof = %d/%d = %.2f' %tuple((out.chisq, out.chisq_dof, out.chisq/out.chisq_dof)))
    print('p_value = %.3f\n' % out.chisq_pvalue)
    
    figure('potenza_alla2')
    subplot(altezza, larghezza, pmax-4)
    errorbar(power[indici_bassi], Vpp[indici_bassi], fmt='.k', yerr=dy[indici_bassi], markersize=4)
    xx = linspace(min(power[indici_bassi]), max(power[indici_bassi]), 2000)
    plot(xx, parabola(xx, *par), color='tab:green', label='{} = {} \n {} = {}/{} \qquad p_value = {} '.format('$a_{fit}$', xe(par[0], err[0]), '$\\frac{\chi^2}{dof}$', chisq, dof, p_value))
    '''legend(fontsize='large')
    subplot(griglia[1])
    indici = argsort(power[indici_bassi])[::-1]
    plot(power[indici_bassi], (Vpp[indici_bassi]-parabola(power[indici_bassi], *par))/dy[indici_bassi], '.-k', markersize=4, linewidth=1)
    ylabel('residui normalizzati')
    xlabel('potenza [mW]')'''
    xlim(min(power[indici_bassi])-0.5, 0.5+max(power[indici_bassi]))
    ylim(0, 0.5+max(Vpp[indici_bassi]))
    if pmax == 5:
        ylabel('intensità [mV]')
    if pmax == 8:
        ylabel('intensità [mV]')
    if pmax == 11:
        ylabel('intensità [mV]')
    if pmax == 14:
        ylabel('intensità [mV]')
    if pmax == 17:
        ylabel('intensità [mV]')
    if (pmax-4) >= 13:
        xlabel('potenze [mW]')
    legend(fontsize='x-small', framealpha=0, loc=0)
    
##fit bassa potenza esponente 
    def parabolab(x, a, b):
        return a*x**b
    
    out = fit_curve(parabolab, power[indici_bassi], Vpp[indici_bassi], dy=dy[indici_bassi], p0=[1,2], absolute_sigma=True)
    par = out.par
    cov = out.cov
    err = sqrt(diag(cov))
    a_fit.append(par[0])
    b_fit.append(par[1])
    da_fit.append(err[0])
    db_fit.append(err[1])
    print('[a b] = %s' %xe(par, err))
    print('chisq/dof = %d/%d = %.2f' %tuple((out.chisq, out.chisq_dof, out.chisq/out.chisq_dof)))
    print('p_value = %.3f' % out.chisq_pvalue)
    
    figure('potenza_allab')
    subplot(altezza, larghezza, pmax-4)
    errorbar(power[indici_bassi], Vpp[indici_bassi], fmt='.k', yerr=dy[indici_bassi], markersize=4)
    xx = linspace(min(power[indici_bassi]), max(power[indici_bassi]), 2000)
    plot(xx, parabolab(xx, *par), color='tab:red', label='{} = {} \n{} = {} '.format('$a_{fit}$', xe(par[0], err[0]), '$b_{fit}$', xe(par[1], err[1])))
    xlim(min(power[indici_bassi])-0.5, 0.5+max(power[indici_bassi]))
    ylim(0, 0.5+max(Vpp[indici_bassi]))
    if pmax == 5:
        ylabel('intensità [mV]')
    if pmax == 8:
        ylabel('intensità [mV]')
    if pmax == 11:
        ylabel('intensità [mV]')
    if pmax == 14:
        ylabel('intensità [mV]')
    if pmax == 17:
        ylabel('intensità [mV]')
    if (pmax-4) >= 13:
        xlabel('potenze [mW]')
    legend(fontsize='x-small', framealpha=0, loc=0)

##andamento di b in funzione del cut
figure(3).set_tight_layout(True)
clf()  
a_fit = array(a_fit)
b_fit = array(b_fit)
da_fit = array(da_fit)
db_fit = array(db_fit)
p_max = array(p_max)
errorbar(p_max, b_fit, fmt='.k', yerr=db_fit, markersize=4)
plot(arange(4,21), ones(17)*2, '--', color='tab:red', label='{}'.format('$b_{atteso}$ = 2'))
xlabel('potenza [mW]')
ylabel('$b_{fit}$')
legend(fontsize='large', framealpha=0)

##estraggo indici misure ad alta potenza
indici_alti = []
for i in range(len(power)):
    if power[i] > 80 and power[i] < 300:
        indici_alti.append(i)
indici_alti = array(indici_alti)
    
##fit alta potenza
def retta(x, a, b):
    return a*x + b
        
figure('potenza_lineare').set_tight_layout(True)
clf()
m = []
dm = []
q = []
dq = []
out = fit_curve(retta,power[indici_alti], Vpp[indici_alti], dy=dy[indici_alti], p0=[1,1], absolute_sigma=True)
par = out.par
cov = out.cov
m_fit = par[0]
q_fit = par[1]
dm_fit, dq_fit = sqrt(diag(cov))
print('m = %s  q = %s' %(xe(m_fit, dm_fit), xe(q_fit, dq_fit)))
errorbar(power[indici_alti], Vpp[indici_alti], fmt='.k', yerr=dy[indici_alti], markersize=4)
x = linspace(min(power[indici_alti]), max(power[indici_alti]), 2000)
plot(x, retta(x, *par), color='tab:red', label='m = {} \n q = {}'.format(xe(m_fit, dm_fit), xe(q_fit, dq_fit)))
legend(fontsize='large')
ylabel('intensità [mV]')
xlabel('potenze [mW]')

