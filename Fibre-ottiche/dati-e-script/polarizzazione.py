import pylab as py
from lab import fit_curve, xe
from scipy.optimize import curve_fit

files = ['cap16.txt',
         'cap13.txt',
         'cap10.txt']

py.figure(1).set_tight_layout(True)
py.clf()

m = []
dm = []
q = []
dq = []

altezza = 3
larghezza = 1

for i in range(len(files)):
    filename= files[i]
    n, l = py.loadtxt(filename, unpack=True)
    dl = py.ones(len(l))*0.1
    dn = 0

    ##faccio il grafico
    py.figure(1)
    py.subplot(altezza, larghezza, i+1)
    py.errorbar(n, l, dl, dn, '.', markersize='3')

    ##funzione di fit
    def retta(x, a, b):
        return a*x + b
    
    par, cov = curve_fit(retta, n, l, sigma = dl, p0 = [1,1], absolute_sigma=True)
    #par = out.par
    #cov = out.cov
    err = py.sqrt(py.diag(cov))
    m_fit = par[0]
    q_fit = par[1]
    dm_fit = err[0]
    dq_fit = err[1]
    dm_fit = py.sqrt(dm_fit**2+(0.01*m_fit)**2)
    m.append(m_fit)
    q.append(q_fit)
    dm.append(dm_fit)
    dq.append(dq_fit)
    print('m = %s  q = %s' %(xe(m_fit, dm_fit), xe(q_fit, dq_fit)))
    x = py.linspace(0, len(n)+1, 100)
    py.plot(x, retta(x, *par), linewidth=1, color ='tab:green' ,label='{} = {} [mm]'.format('$m_{fit}$', xe(m_fit, dm_fit)))
    py.legend(fontsize='large')
    py.ylabel('l [mm]')
    py.xlabel('N')

    
    
    
    
    

