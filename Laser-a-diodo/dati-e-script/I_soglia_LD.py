

import pylab as py
from lab import fit_curve, xe

files = ['borcapLDG12PvsI.txt',
         'borcapLDG25PvsI.txt',
         'borcapLDG43PvsI.txt']

py.figure(1).set_tight_layout(True)
py.clf()
##[I]=mA e [P]=muA
I12, P12 = py.loadtxt('borcapLDG12PvsI.txt', unpack=True)
'''I25, P25 = py.loadtxt('borcapLDG25PvsI.txt', unpack=True)
I43, P43 = py.loadtxt('borcapLDG43PvsI.txt', unpack=True)'''

    
##faccio il grafico P-I
py.figure(1)
py.plot(I12, P12, '.', color='tab:red', markersize='3')  
'''py.plot(I25, P25, '.', color='tab:blue', markersize='3')
py.plot(I43, P43, '.', color='tab:green', markersize='3')'''

##estraggo i dati da fittare
i=0
while P12[i]>100:
    i=i+1

'''j=0
while P25[j]>100:
    j=j+1
         
k=0
while P43[k]>100:
    k=k+1'''
    
##funzione di fit
def retta(x, a, b):
    return a*x + b

##trovo I_th con un fit    
m = []
dm = []
q = []
dq = []
out = fit_curve(retta, I12[0:i-1], P12[0:i-1], dy=1, p0=[1,1], absolute_sigma=True)
par = out.par
cov = out.cov
m_fit = par[0]
q_fit = par[1]
dm_fit, dq_fit = py.sqrt(py.diag(cov))
print('m = %s  q = %s' %(xe(m_fit, dm_fit), xe(q_fit, dq_fit)))
print('I_th = %s' %(-q_fit/m_fit))
m.append(m_fit)
q.append(q_fit)
dm.append(dm_fit)
dq.append(dq_fit)
py.plot(I12[0:i-1], retta(I12[0:i-1], *par), linewidth=1)

py.ylabel('P [\muW]')
py.xlabel('I [mA]')
        