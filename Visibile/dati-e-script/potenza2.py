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

figure('potenza_alla2').set_tight_layout(True)
clf()
figure('potenza_allab').set_tight_layout(True)
clf()
figure('potenza_alla2_esempio').set_tight_layout(True)
clf()
figure('potenza_allab_esempio').set_tight_layout(True)
clf()
figure('potenza_lineare').set_tight_layout(True)
clf()

power = zeros(len(Vpp))
for i in range(len(power)):
    for j in range(len(tpower)):
        if grad[i] == tgrad[j]:
            power[i] = tpower[j]
            break

dpower = power*0.03
    
dy = 0.68*0.5*dVpp 
dx = dpower

##estraggo indici misure a bassa potenza
a1_fit = []
da1_fit = []
a_fit = []
b_fit = []
da_fit = []
db_fit = []
p_max = []
p_i = 5
p_f = 41
step = 2
altezza = 6
larghezza = 3
j = 1
for pmax in range(p_i,p_f,step):
    indici_bassi = []
    for i in range(len(power)):
        if power[i] < pmax:
            indici_bassi.append(i)
    indici_bassi = array(indici_bassi)
    p_max.append(max(power[indici_bassi]))

##fit bassa potenza 
    def parabola(x, a):
        return a*x**2
    
    out = fit_curve(parabola, power[indici_bassi], Vpp[indici_bassi], dy=dy[indici_bassi], dx=dx[indici_bassi], p0=[1], absolute_sigma=True)
    par = out.par
    cov = out.cov
    err = sqrt(diag(cov))
    a1_fit.append(par[0])
    da1_fit.append(err[0])
    chisq = out.chisq
    chisq1 = '{0:.2f}'.format(out.chisq)
    p_value = '{0:.1f}'.format(out.chisq_pvalue*100)
    dof = out.chisq_dof
    chidof = '{0:.2f}'.format(chisq/dof)
    print('a = %s' %xe(par, err))
    print('chisq/dof = %d/%d = %.3f' %tuple((out.chisq, out.chisq_dof, out.chisq/out.chisq_dof)))
    print('p_value = %.3f\n' % out.chisq_pvalue)
    
    figure('potenza_alla2')
    subplot(altezza, larghezza, j)
    errorbar(power[indici_bassi], Vpp[indici_bassi], fmt='.k', yerr=dy[indici_bassi],xerr = dx[indici_bassi], markersize=4)
    xx = linspace(min(power[indici_bassi])-6, max(power[indici_bassi])+6, 2000)
    plot(xx, parabola(xx, *par), color='tab:red', label='{} = {} [mV/mW$^2$] \n {} = {}/{} = {} \n {} = {}%'.format('$a_{fit}$', xe(par[0], err[0]), '$\\frac{\chi^2}{dof}$', chisq1, dof, chidof, '$p_{value}$', p_value))
    xlim(min(power[indici_bassi])-0.5, 0.5+max(power[indici_bassi]))
    ylim(0, 0.5+max(Vpp[indici_bassi]))
    if j == 1:
        ylabel('intensità [mV]')
    if j == 4:
        ylabel('intensità [mV]')
    if j == 7:
        ylabel('intensità [mV]')
    if j == 10:
        ylabel('intensità [mV]')
    if j == 13:
        ylabel('intensità [mV]')
    if j == 16:
        ylabel('intensità [mV]')
    if j >= 16:
        xlabel('potenze [mW]')
    legend(fontsize='x-small', framealpha=0, loc=2)
    
    if j == 6:
        figure('potenza_alla2_esempio')
        errorbar(power[indici_bassi], Vpp[indici_bassi], fmt='.k', yerr=dy[indici_bassi],xerr = dx[indici_bassi], markersize=4)
        xx = linspace(min(power[indici_bassi])-6, max(power[indici_bassi])+6, 2000)
        plot(xx, parabola(xx, *par), color='tab:red', label='{} = {} [mV/mW$^2$] \t {} = {}% \n {} = {}/{} = {}'.format('$a_{fit}$', xe(par[0], err[0]), '$p_{value}$', p_value, '$\\frac{\chi^2}{dof}$', chisq1, dof, chidof))
        xlim(min(power[indici_bassi])-0.5, 0.5+max(power[indici_bassi]))
        ylim(0, 0.5+max(Vpp[indici_bassi]))
        ylabel('intensità [mV]')
        xlabel('potenze [mW]')
        legend(fontsize='large', framealpha=0, loc=2)
        
##fit bassa potenza esponente 
    def parabolab(x, a, b):
        return a*x**b
    
    out = fit_curve(parabolab, power[indici_bassi], Vpp[indici_bassi], dy=dy[indici_bassi], dx=dx[indici_bassi], p0=[1,2], absolute_sigma=True)
    par = out.par
    cov = out.cov
    err = sqrt(diag(cov))
    a_fit.append(par[0])
    b_fit.append(par[1])
    da_fit.append(err[0])
    db_fit.append(err[1])
    print('[a b] = %s' %xe(par, err))
    print('chisq/dof = %d/%d = %.2f' %tuple((out.chisq, out.chisq_dof, out.chisq/out.chisq_dof)))
    print('p_value = %.2f' % out.chisq_pvalue)
    
    figure('potenza_allab')
    subplot(altezza, larghezza, j)
    errorbar(power[indici_bassi], Vpp[indici_bassi], fmt='.k', yerr=dy[indici_bassi],xerr = dx[indici_bassi], markersize=4)
    xx = linspace(min(power[indici_bassi])-6, max(power[indici_bassi])+6, 2000)
    plot(xx, parabolab(xx, *par), color='tab:red', label='{} = {} [mV/mW$^2$]\n{} = {} '.format('$a_{fit}$', xe(par[0], err[0]), '$b_{fit}$', xe(par[1], err[1])))
    xlim(min(power[indici_bassi])-0.5, 0.5+max(power[indici_bassi]))
    ylim(0, 0.5+max(Vpp[indici_bassi]))
    if j == 1:
        ylabel('intensità [mV]')
    if j == 4:
        ylabel('intensità [mV]')
    if j == 7:
        ylabel('intensità [mV]')
    if j == 10:
        ylabel('intensità [mV]')
    if j == 13:
        ylabel('intensità [mV]')
    if j == 16:
        ylabel('intensità [mV]')
    if j >= 16:
        xlabel('potenze [mW]')
    legend(fontsize='x-small', framealpha=0, loc=2)
    j = j + 1
    
    if j == 6:
        figure('potenza_allab_esempio')
        errorbar(power[indici_bassi], Vpp[indici_bassi], fmt='.k', yerr=dy[indici_bassi],xerr = dx[indici_bassi], markersize=4)
        xx = linspace(min(power[indici_bassi])-6, max(power[indici_bassi])+6, 2000)
        plot(xx, parabolab(xx, *par), color='tab:red', label='{} = {} [mV/mW$^2$]\n{} = {} '.format('$a_{fit}$', xe(par[0], err[0]), '$b_{fit}$', xe(par[1], err[1])))
        xlim(min(power[indici_bassi])-0.5, 0.5+max(power[indici_bassi]))
        ylim(0, 0.5+max(Vpp[indici_bassi]))
        ylabel('intensità [mV]')
        xlabel('potenze [mW]')
        legend(fontsize='large', framealpha=0, loc=2)

a1_fit = array(a1_fit)
da1_fit = array(da1_fit)

##andamento di b in funzione del cut
figure(5).set_tight_layout(True)
clf()  
a_fit = array(a_fit)
b_fit = array(b_fit)
da_fit = array(da_fit)
db_fit = array(db_fit)
p_max = array(p_max)
errorbar(p_max, b_fit, fmt='.k', yerr=db_fit, markersize=4)
plot(arange(p_i-1,p_f+1), ones(p_f-p_i+2)*2, '--', color='tab:red', label='$b_{atteso}$ = 2')
xlabel('potenza [mW]')
ylabel('$b_{fit}$')
legend(fontsize='large', framealpha=0)

##fluttuazioni relative di b_fit rispetto a b_atteso in funzione del cut
figure(6).set_tight_layout(True)
clf()
res = (b_fit-2)/db_fit
plot(p_max, res, '.', color = 'black', markersize=4)
plot(arange(p_i-1,p_f+1), zeros(p_f-p_i+2), '--', color='tab:red')
fill_between(arange(p_i-1,p_f+1), zeros(p_f-p_i+2)-2, zeros(p_f-p_i+2)+2, color='tab:red', alpha=0.3)
xlabel('potenza [mW]')
ylabel('residui normalizzati')
xlim(p_i-1, p_f)


##estraggo indici misure ad alta potenza
m_fit = []
dm_fit = []
q_fit = []
dq_fit = []
p_min = []
p_i = 40
p_f = 480
step = 40
altezza = 4
larghezza = 2
j = 1

for pmin in range(p_i,p_f,step):
    indici_alti = []
    for i in range(len(power)):
        if power[i] > pmin:
            indici_alti.append(i)
    indici_alti = array(indici_alti)
    p_min.append(min(power[indici_alti]))
    
    ##fit alta potenza
    def retta(x, a, b):
        return a*x + b
    
    out = fit_curve(retta,power[indici_alti], Vpp[indici_alti], dy=dy[indici_alti], dx=dx[indici_alti], p0=[1,1], absolute_sigma=True)
    par = out.par
    cov = out.cov
    err = sqrt(diag(cov))
    m_fit.append(par[0])
    dm_fit.append(err[0])
    q_fit.append(par[1])
    dq_fit.append(err[1])
    chisq = out.chisq
    chisq1 = '{0:.2f}'.format(out.chisq)
    p_value = '{0:.1f}'.format(out.chisq_pvalue*100)
    dof = out.chisq_dof
    chidof = '{0:.2f}'.format(chisq/dof)
    print('[m q] = %s' %xe(par, err))
    print('chisq/dof = %d/%d = %.3f' %tuple((out.chisq, out.chisq_dof, out.chisq/out.chisq_dof)))
    print('p_value = %.3f\n' % out.chisq_pvalue)
    
    figure('potenza_lineare')
    subplot(altezza, larghezza, j)
    errorbar(power[indici_alti], Vpp[indici_alti], fmt='.k', yerr=dy[indici_alti], xerr=dx[indici_alti], markersize=4)
    x = linspace(min(power[indici_alti]), max(power[indici_alti]), 2000)
    plot(x, retta(x, *par), color='tab:red', label='{} = {} \t {} = {} \n {} = {}% \n {} = {}/{} = {}'.format('$m_{fit}$', xe(par[0], err[0]), '$q_{fit}$', xe(par[1], err[1]), '$p_{value}$', p_value, '$\\frac{\chi^2}{dof}$', chisq1, dof, chidof))
    legend(fontsize='x-small', framealpha=0, loc=2)
    if j == 1:
        ylabel('intensità [mV]')
    if j == 3:
        ylabel('intensità [mV]')
    if j == 5:
        ylabel('intensità [mV]')
    if j == 7:
        ylabel('intensità [mV]')
    if j >= 7:
        xlabel('potenze [mW]')
    j = j + 1
    
    if j > 8:
        break

