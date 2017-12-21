from pylab import *
from lab import fit_curve, xe
from gvar import gvar

name = 'borcapasme03.txt'

t, volt, _, __, rampa, ___ = loadtxt(name, comments='"', unpack=True)
t = t*1000 #mV
volt = volt*1000 #mV
rampa = rampa*1000 #mV

def massimi(array):
    """Se i massimi sono il primo e l'ultimo elemento non li prende.
       Se ci sono piĂš valori uguali prende l'indice del primo."""
    massimi = []
    for i in range(1, len(array)-1):
        if (array[i-1] < array[i]) & (array[i] >= array[i+1]):
            massimi.append(i)
    return massimi

def retta(x, a, b):
    return a*x + b

##stimo il fattore di scala tra rampa e segnale
hvolt = abs(max(volt) - min(volt))
hrampa = abs(max(rampa) - min(rampa))
scale = hvolt/hrampa
offset = max(scale*rampa)-max(volt)

##plot di controllo
figure(0).set_tight_layout(True)
clf()
subplot(211)
plot(t, volt)
plot(t, scale*rampa - 1.21*offset*ones(len(rampa))) #riscalo la rampa
ylim(-485,85)
ylabel('segnale [mV]')
xlabel('t [ms]')

maxindex = argmax(rampa)
minindex = argmin(rampa)
print()
if maxindex > minindex:
    print(name, ': rampa in SALITA')
else:
    print(name, ': rampa in DISCESA')
    
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

plot(t[picchi], volt[picchi], 'o', color='tab:red', label='picchi selezionati')
legend(loc=4)

##trovo i deltanu con un fit    
subplot(212)
n_ordini = int(len(picchi)/3)
ordini = linspace(0, n_ordini-1, n_ordini)
ordini_fit = ordini - (n_ordini)/2
"""con questo trucco fitto una retta simmetrica rispetto all'asse y per
avere un miglior q e per non doverne propagare l'errore"""

m = []
dm = []
q = []
dq = []
nomipicchi = ['sinistra', 'centro  ', 'destra  ']
for k in range(3):
    piccoinquestione = picchi[k::3]
    plot(ordini, t[piccoinquestione], 'o', color='tab:red')
    """come errore metto (1/2)*sensibilità*0.68,
    scelta discutibile ma giustificata a spanne dal confidence level"""
    out = fit_curve(retta, ordini_fit, t[piccoinquestione], dy=0.5*0.68*(t[1]-t[0]), p0=[1,1], absolute_sigma=True)
    par = out.par
    cov = out.cov
    m_fit = par[0]
    q_fit = par[1]
    dm_fit, dq_fit = sqrt(diag(cov))
    m.append(m_fit)
    q.append(q_fit)
    dm.append(dm_fit)
    dq.append(dq_fit)
    print('picco %s: m = %s  q = %s' %(nomipicchi[k], xe(m_fit, dm_fit), xe(q_fit, dq_fit)))
    plot(ordini, retta(ordini_fit, *par))

xticks(arange(0, n_ordini, 1))
xlim(-0.3, n_ordini-1+0.3)
ylim(min(t),max(t))
ylabel('t [ms]')
xlabel('ordine')

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
print('deltanu_sinistra =', xe(udeltanu_sinistra.mean, udeltanu_sinistra.sdev))
print('deltanu_destra   =', xe(udeltanu_destra.mean, udeltanu_destra.sdev))
scritte = ['$\Delta\\nu_{12}$', xe(udeltanu_sinistra.mean, udeltanu_sinistra.sdev)]
plot(ordini, t[picchi[0::3]], 'o', color='tab:red', markersize=0,
     label='{} = {} Hz \n{} = {} Hz'.format('$\Delta\\nu_{12}$', xe(udeltanu_sinistra.mean, udeltanu_sinistra.sdev), '$\Delta\\nu_{23}$', xe(udeltanu_destra.mean, udeltanu_destra.sdev)))
legend(fontsize='large', loc=4, framealpha=0)