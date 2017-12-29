"""script che analizza il segnale di trasmittivitĂ Â  di un Fabry-Perot letto da 
un fotodiodo"""

from pylab import *
from scipy.optimize import curve_fit
from lab import fit_curve, xe
from gvar import gvar
from scipy.special import erf
from scipy.integrate import quad

files = ['borcapasm01.txt',
         'borcapasm02.txt',
         'borcapasm03.txt',
         'borcapasme01.txt',
         'borcapasme02.txt',
         'borcapasme03.txt',
         'borcapasme04.txt',
         'borcapasme05.txt',
         'borcapasme06.txt',
         'borcapasme17.txt',
         'borcapasme18.txt',
         'borcapasv02.txt',
         'borcapasv03.txt',
         'borcapasv04.txt',
         'borcapasv05.txt',
         'borcapasv06.txt',
         'borcapasv07.txt',
         'borcapasv10.txt',
         'borcapasv11.txt',
         'borcapasv12.txt',
         'borcapasv13.txt',
         'borcapasv14.txt',
         'borcapasv15.txt',
         'borcapasv16.txt']

figure(2).set_tight_layout(True)
clf()
params = {'axes.labelsize': 'small',
         'xtick.labelsize':'x-small',
         'ytick.labelsize':'x-small'}
rcParams.update(params)
figure(1).set_tight_layout(True)
clf()
altezza = 8
larghezza = 3

##funzioncina che cerca gli indici dei massimi di un vettore
def massimi(array):
    """Se i massimi sono il primo e l'ultimo elemento non li prende.
       Se ci sono piĂš valori uguali prende l'indice del primo."""
    massimi = []
    for i in range(1, len(array)-1):
        if (array[i-1] < array[i]) & (array[i] >= array[i+1]):
            massimi.append(i)
    return massimi

##funzione di fit
def retta(x, a, b):
    return a*x + b

##funzione che calcola la media pesata (usa il pacchetto gvar e pylab)
def wmean(m, s):
    from gvar import gvar
    from pylab import sqrt, array
    m = array(m)
    s = array(s)
    media = (m*(1/s**2)).sum() / (1/s**2).sum()
    sigma = 1/sqrt((1/s**2).sum())
    return gvar(media, sigma)

nu_sinistra = []
dnu_sinistra = []
nu_destra = []
dnu_destra = []
indici_salita = []
indici_discesa = []
numero_ordini = []
for i in range(len(files)):
    filename= files[i]
    t, volt, _, __, rampa, ___ = loadtxt(filename, comments='"', unpack=True)
    t = t*1000 #millisecondi
    volt = volt*1000 #millivolt
    rampa = rampa*1000 #millivolt
    
    ##stimo il fattore di scala tra rampa e segnale
    hvolt = abs(max(volt) - min(volt))
    hrampa = abs(max(rampa) - min(rampa))
    scale = hvolt/hrampa
    offset = max(scale*rampa)-max(volt)
    
    ##plot di controllo
    figure(1)
    subplot(altezza, larghezza, i+1)
    plot(t, volt)
    plot(t, scale*rampa - 1.2*offset*ones(len(rampa))) #riscalo la rampa
    if i%larghezza == 0:
        ylabel('segnale [mV]')
    if i >= len(files)-larghezza:
        xlabel('t [ms]')
    
    maxindex = argmax(rampa)
    minindex = argmin(rampa)
    print()
    if maxindex > minindex:
        print(filename, ': rampa in SALITA')
        indici_salita.append(i)
    else:
        print(filename, ': rampa in DISCESA')
        indici_discesa.append(i)
    print('Vpp = %.0f mV' % (rampa[maxindex]-rampa[minindex]))
        
    ##cerco i minimi
    minimi = massimi(-volt)
    
    voltmean = volt.mean()
    voltstd = volt.std()
    triggerlevel = voltmean - 0.5*voltstd
    
    ##prendo solo i minimi sotto il triggerlevel (e dentro la rampa)
    picchi = []
    for j in range(len(minimi)):
        if (min(minindex, maxindex) < minimi[j]) & (minimi[j] < max(minindex, maxindex)+3):
            if (volt[minimi[j]] < triggerlevel):
                picchi.append(minimi[j]) 
    
    ##tolgo i picchi di ordini incompleti 
    ##(solo il primo e l'ultimo ordine possono essere incompleti)
    p = len(picchi)
    if (p < 6) | (p > 27):
        print('ATTENZIONE: picchi molto sospetti')
        print('numero picchi = %d' %p)
    else:
        diffpicchi = diff(picchi)
        meandiffpicchi = diffpicchi.mean()
        if diffpicchi[0] > meandiffpicchi:
            picchi = picchi[1:]
        elif diffpicchi[1] > meandiffpicchi:
            picchi = picchi[2:]
        if diffpicchi[-1] > meandiffpicchi:
            picchi = picchi[:-1]
        elif diffpicchi[-2] > meandiffpicchi:
            picchi = picchi[:-2]
        p = len(picchi)
        if p%3 != 0:
            print('ATTENZIONE: picchi sospetti')
        else:
            print('numero ordini =', p//3 - 1)        
        
        figure(1)
        plot(t[picchi], volt[picchi], 'o', color='tab:red', markersize=4)
        
        ##trovo i deltanu con un fit    
        figure(2)
        subplot(altezza, larghezza, i+1)
        n_ordini = int(len(picchi)/3)
        numero_ordini.append(n_ordini)
        ordini = linspace(1, n_ordini, n_ordini)
        ordini_fit = ordini - (n_ordini+1)/2
        """con questo trucco fitto una retta simmetrica rispetto all'asse y per
        avere un miglior q e per non doverne propagare l'errore"""
        m = []
        dm = []
        q = []
        dq = []
        nomipicchi = ['sinistra', 'centro  ', 'destra  ']
        for k in range(3):
            piccoinquestione = picchi[k::3]
            plot(ordini, t[piccoinquestione], 'o', color='tab:red', markersize='4')
            """come errore metto (1/2)*sensibilità*0.68,
            scelta discutibile ma giustificata a spanne dal confidence level"""
            out = fit_curve(retta, ordini_fit, t[piccoinquestione], dy=0.5*0.68*(t[1]-t[0]), p0=[1,1], absolute_sigma=True)
            par = out.par
            cov = out.cov
            m_fit = par[0]
            q_fit = par[1]
            dm_fit, dq_fit = sqrt(diag(cov))
            print('picco %s: m = %s  q = %s' %(nomipicchi[k], xe(m_fit, dm_fit), xe(q_fit, dq_fit)))
            m.append(m_fit)
            q.append(q_fit)
            dm.append(dm_fit)
            dq.append(dq_fit)
            plot(ordini, retta(ordini_fit, *par), linewidth=1)
        
        if i%larghezza == 0:
            ylabel('t [ms]')
        if i >= len(files)-larghezza:
            xlabel('ordini')
        #xlabel('numero ordine interferenza')
        #ylabel('t [ms]')
        xticks(arange(1, n_ordini+1, 1))
        ylim(ylim(min(t)-0.2*(max(t)-min(t)),max(t)))
        xlim(0.5, n_ordini+0.5)
        
        ##calcolo i deltanu
        m = array(m)
        dm = array(dm)
        q = array(q)
        dq = array(dq)
        uFSR = gvar(m.mean(), dm.mean()/sqrt(3))
        diffq = diff(q)
        udeltaq_sinistra = gvar(diffq[0], dq.mean()*sqrt(2))
        udeltaq_destra = gvar(diffq[1], dq.mean()*sqrt(2))
        udeltanu_sinistra = 1500*udeltaq_sinistra/uFSR
        udeltanu_destra = 1500*udeltaq_destra/uFSR
        if maxindex > minindex:
            print('deltanu_12 =', xe(udeltanu_sinistra.mean, udeltanu_sinistra.sdev))
            print('deltanu_23 =', xe(udeltanu_destra.mean, udeltanu_destra.sdev))
        else:
            print('deltanu_23 =', xe(udeltanu_sinistra.mean, udeltanu_sinistra.sdev))
            print('deltanu_12 =', xe(udeltanu_destra.mean, udeltanu_destra.sdev))
        nu_sinistra.append(udeltanu_sinistra.mean)
        dnu_sinistra.append(udeltanu_sinistra.sdev)
        nu_destra.append(udeltanu_destra.mean)
        dnu_destra.append(udeltanu_destra.sdev)
        if maxindex > minindex: #cioe se la rampa è in salita
            plot(ordini, t[picchi[1::3]], 'o', color='tab:red', markersize='0', label='{} = {} Hz \n{} = {} Hz'.format('$\Delta\\nu_{12}$', xe(udeltanu_sinistra.mean, udeltanu_sinistra.sdev), '$\Delta\\nu_{23}$', xe(udeltanu_destra.mean, udeltanu_destra.sdev)))
        else:
            plot(ordini, t[picchi[1::3]], 'o', color='tab:red', markersize='0', label='{} = {} Hz \n{} = {} Hz'.format('$\Delta\\nu_{23}$', xe(udeltanu_sinistra.mean, udeltanu_sinistra.sdev), '$\Delta\\nu_{12}$', xe(udeltanu_destra.mean, udeltanu_destra.sdev)))
        legend(fontsize='x-small', framealpha=0, loc=4)

nu_sinistra = array(nu_sinistra)
dnu_sinistra = array(dnu_sinistra)
nu_destra = array(nu_destra)
dnu_destra = array(dnu_destra)
numero_ordini = array(numero_ordini)

nu_medio = (nu_sinistra + nu_destra) / 2
dnu_medio = (dnu_sinistra + dnu_destra) / 2 / sqrt(2)

##medio distinguendo destra e sinistra e salita e discesa
media_nu_sinistra_salita = wmean(nu_sinistra[indici_salita], dnu_sinistra[indici_salita])
media_nu_sinistra_discesa = wmean(nu_sinistra[indici_discesa], dnu_sinistra[indici_discesa])
media_nu_destra_salita = wmean(nu_destra[indici_salita], dnu_destra[indici_salita])
media_nu_destra_discesa = wmean(nu_destra[indici_discesa], dnu_destra[indici_discesa])
media_nu_sinistra = wmean([media_nu_sinistra_salita.mean, media_nu_sinistra_discesa.mean], [media_nu_sinistra_salita.sdev, media_nu_sinistra_discesa.sdev])
media_nu_destra = wmean([media_nu_destra_salita.mean, media_nu_destra_discesa.mean], [media_nu_destra_salita.sdev, media_nu_destra_discesa.sdev])
media_nu_basso = wmean([media_nu_sinistra_salita.mean, media_nu_destra_discesa.mean], [media_nu_sinistra_salita.sdev, media_nu_destra_discesa.sdev])
media_nu_alto = wmean([media_nu_destra_salita.mean, media_nu_sinistra_discesa.mean], [media_nu_destra_salita.sdev, media_nu_sinistra_discesa.sdev])
media_sinistra_destra = wmean([media_nu_sinistra.mean, media_nu_destra.mean], [media_nu_sinistra.sdev, media_nu_destra.sdev])
media_alto_basso = wmean([media_nu_alto.mean, media_nu_basso.mean], [media_nu_alto.sdev, media_nu_basso.sdev])

print('\nMEDIA')
print('media_nu_sinistra_salita  =', media_nu_sinistra_salita)
print('media_nu_sinistra_discesa =', media_nu_sinistra_discesa)
print('media_nu_destra_salita    =', media_nu_destra_salita)
print('media_nu_destra_discesa   =', media_nu_destra_discesa)
#print('media_nu_sinistra         =', media_nu_sinistra)
#print('media_nu_destra           =', media_nu_destra)
print('media_nu_12               =', media_nu_basso)
print('media_nu_23               =', media_nu_alto)
#print('media_sinistra_destra     =', media_sinistra_destra)
print('nu_medio                  =', media_alto_basso)

##calcolo un po' di deviazioni standard
def sigma_m(x):
    return std(x)/(sqrt(len(x)-1))

def exp_sigma(a):
    return std(a) * len(a) / (len(a)-1)

sigma_sinistra_salita = sigma_m(nu_sinistra[indici_salita])
sigma_sinistra_discesa = sigma_m(nu_sinistra[indici_discesa])
sigma_destra_salita = sigma_m(nu_destra[indici_salita])
sigma_destra_discesa = sigma_m(nu_destra[indici_discesa])
sigma_sinistra = sigma_m(nu_sinistra)
sigma_destra = sigma_m(nu_destra)

tutto = concatenate((nu_sinistra, nu_destra))
sigma_tutto = sigma_m(tutto)

#print('\nStimo le deviazioni standard sulle medie direttamente dai dati:')
#print('sigma_sinistra_salita  =', sigma_sinistra_salita)
#print('sigma_sinistra_discesa =', sigma_sinistra_discesa)
#print('sigma_destra_salita    =', sigma_destra_salita)
#print('sigma_destra_discesa   =', sigma_destra_discesa)
#print('sigma_sinistra =', sigma_sinistra)
#print('sigma_destra   =', sigma_destra)
#print('sigma_tutto    =', sigma_tutto)

##test compatibilità
def p_value(start, s):
    return 2*quad(lambda x: exp(-x**2/(2*s**2))/(sqrt(2*pi)*s), start, inf)[0]

print('\ntest compatibilità')
#print('sinistra-destra:', media_nu_sinistra-media_nu_destra, '   p_value = %.2g%%' %(100*p_value((media_nu_sinistra-media_nu_destra).mean, (media_nu_sinistra-media_nu_destra).sdev)))
print('alto-basso     :', media_nu_basso-media_nu_alto, '   p_value = %.2g%%' %(100*p_value((media_nu_basso-media_nu_alto).mean, (media_nu_basso-media_nu_alto).sdev)))

params = {'axes.labelsize': 'large',
         'xtick.labelsize':'small',
         'ytick.labelsize':'medium'}
rcParams.update(params)

basso = concatenate((nu_sinistra[indici_salita], nu_destra[indici_discesa]))
sigma_basso = exp_sigma(basso)
alto = concatenate((nu_destra[indici_salita], nu_sinistra[indici_discesa]))
sigma_alto = exp_sigma(alto)

figure('deltanu12 e deltanu23').set_tight_layout(True)
clf()
subplot(211)
errorbar(array(indici_salita)+1, nu_sinistra[indici_salita], yerr=dnu_sinistra[indici_salita], color='tab:blue', fmt='o')
errorbar(array(indici_discesa)+1, nu_destra[indici_discesa], yerr=dnu_destra[indici_discesa], color='tab:blue', fmt='o')
plot(arange(0,len(nu_sinistra)+2), ones(len(nu_sinistra)+2)*media_nu_basso.mean, '--', color='tab:red', label='{}'.format('$\Delta\\nu_{12}$ = 435.96'))
x = arange(0,len(basso)+2)
y = ones(len(basso)+2)*media_nu_basso.mean
dy = sigma_basso
fill_between(x, y-dy, y+dy, color='tab:red', alpha=0.3)
legend(loc=8,fontsize='large')
ylabel('{}'.format('$\Delta\\nu_{12}$ [Hz]'))
xlim(0.1,24.9)
xticks( arange(1,25) )
subplot(212)
errorbar(array(indici_salita)+1, nu_destra[indici_salita], yerr=dnu_destra[indici_salita], color='tab:blue', fmt='o')
errorbar(array(indici_discesa)+1, nu_sinistra[indici_discesa], yerr=dnu_sinistra[indici_discesa], color='tab:blue', fmt='o')
x = arange(0,len(nu_destra)+2)
y = ones(len(nu_destra)+2)*media_nu_alto.mean
dy = sigma_alto
plot(x, y, '--', color='tab:red', label='{}'.format('$\Delta\\nu_{23}$ = 433.01'))
fill_between(x, y-dy, y+dy, color='tab:red', alpha=0.3)
legend(loc=9,fontsize='large')
ylabel('{}'.format('$\Delta\\nu_{23}$ [Hz]'))
xlim(0.1,24.9)
xticks( arange(1,25) )
xlabel('numero presa dati')

#figure('deltanu23(alto)')
#clf()
#errorbar(indici_salita, nu_destra[indici_salita], yerr=dnu_destra[indici_salita], fmt='o')
#errorbar(indici_discesa, nu_sinistra[indici_discesa], yerr=dnu_sinistra[indici_discesa], fmt='o')
#
#figure('deltanu sinistra')
#clf()
#errorbar(indici_salita, nu_sinistra[indici_salita], yerr=dnu_sinistra[indici_salita], fmt='o')
#errorbar(indici_discesa, nu_sinistra[indici_discesa], yerr=dnu_sinistra[indici_discesa], fmt='o')
#
#figure('deltanu destra')
#clf()
#errorbar(indici_salita, nu_destra[indici_salita], yerr=dnu_destra[indici_salita], fmt='o')
#errorbar(indici_discesa, nu_destra[indici_discesa], yerr=dnu_destra[indici_discesa], fmt='o')

figure('deltanu_medio').set_tight_layout(True)
clf()
errorbar(array(indici_salita)+1, nu_medio[indici_salita], yerr=dnu_medio[indici_salita], fmt='o', label='{}'.format('$\Delta\\nu$ rampa in salita'))
errorbar(array(indici_discesa)+1, nu_medio[indici_discesa], yerr=dnu_medio[indici_discesa], fmt='o', label='{}'.format('$\Delta\\nu$ rampa in discesa'))
plot(arange(0,len(nu_medio)+2), ones(len(nu_medio)+2)*media_alto_basso.mean, '--', color='tab:red', label='{}'.format('$\Delta\\nu_{medio}$ = 434.5(7)'))
xlim(0.1,24.9)
ylim(426.1, 447.9)
ylabel('{}'.format('$\Delta\\nu$ [Hz]'))
xlabel('numero presa dati')
xticks( arange(1,25) )
legend(fontsize='large')

show()