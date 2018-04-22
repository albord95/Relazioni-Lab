
import pylab as py
from scipy.optimize import curve_fit
from lab import fit_curve, xe
from gvar import gvar
from scipy.special import erf
from scipy.integrate import quad

files = ['borcapLDG12PvsI.txt',
         'borcapLDG25PvsI.txt',
         'borcapLDG43PvsI.txt']

py.figure(1).set_tight_layout(True)
py.clf()

##[I]=mA e [P]=muA

for i in range(len(files)):
    filename= files[i]
    I, P = py.loadtxt(filename, unpack=True)
    dI = py.ones(len(I))*0.1
    
    
    ##faccio il grafico P-I
    py.figure(1)
    py.plot(I, P, '.', color='tab:red', markersize='3')  
    
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
    I_th = -q_fit/m_fit
    dI = I_th*(dm_fit/m_fit + dq_fit/q_fit)
    print('m = %s  q = %s' %(xe(m_fit, dm_fit), xe(q_fit, dq_fit)))
    print('I_th = %s' %(xe(I_th, dI)))
    m.append(m_fit)
    q.append(q_fit)
    dm.append(dm_fit)
    dq.append(dq_fit)
    
    py.plot(I12[0:i-1], retta(I12[0:i-1], *par), linewidth=1, label='$I_{th} (T = 12°C) = 53.4(2) mA$')
    py.legend(fontsize='large')
    py.ylabel('P [$\mu$W]')
    py.xlabel('I [mA]')


        