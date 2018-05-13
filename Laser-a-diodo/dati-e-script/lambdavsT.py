'''fit lineare andamento lambda vs T del diodo laser'''

import pylab as py
from lab import fit_curve, xe

T, L = py.loadtxt('borcapLDVtlambda.txt', unpack=True)
dL = py.ones(len(L))
dT = 0

py.figure(1).set_tight_layout(True)
py.clf()
 
##faccio il grafico
py.figure(1)
py.errorbar(T, L, dL, dT, '.', markersize='3')

##funzione di fit
def retta(x, a, b):
    return a*x + b
    
##trovo I_th con un fit    
m = []
dm = []
q = []
dq = []
out = fit_curve(retta, T, L, dy=1, p0=[1,1], absolute_sigma=True)
par = out.par
cov = out.cov
err = py.sqrt(py.diag(cov))
m_fit = par[0]
q_fit = par[1]
dm_fit = err[0]
dq_fit = err[1]
print('m = %s  q = %s' %(xe(m_fit, dm_fit), xe(q_fit, dq_fit)))
x = py.linspace(T[0]-1, T[len(T)-1]+1, 100)
py.plot(x, retta(x, *par), linewidth=1, label='m = 0.22(2) nm/°C \n q = 775.4(5) nm')
py.legend(fontsize='large')
py.ylabel('$\lambda$ [nm]')
py.xlabel('T [°C]')


        

