"""script che fitta un picco di trasmittivitĂ  di un Fabry-Perot e calcola la finezza"""

from pylab import *
from lab import fit_curve, CurveModel, xe
import sympy
from statistics import mode

numbers = ['02a','02b','02c','03a','03b','03c','04a','04b','04c','05a','05b','05c','06a', '06b','06c','07a','07b','07c','08a','08b','08c','09a','09b','09c','10a','10b','11a', '11b','12a','13a','13b','14a','14b','15a','15b','16a','16b']
files = ['borcapasv00.txt']*len(numbers)
for j in range(len(files)):
    files[j] = 'borcapasv' + numbers[j] + '.txt'

def trasmittivita(x, A, B, C, D, F):
    """A è la scala e sarà negativa
       B è l'offset e sara circa nullo e puo essere fissato a mano
       C è il periodo (FSR)
       D è l'ordinata del picco
       F sarà circa la finezza"""
    return A / (1 + (F*2/pi*sympy.sin(pi*(x - D)/C))**2) + B

def trasmittivita_p(x, A, B, C, D, F):
    return A / (1 + (F*2/pi*sin(pi*(x - D)/C))**2) + B

figure('finezza_fit').set_tight_layout(True)
clf()
largh = 4
altez = 9
n_subplot = 1
finezza = []
for i in range(len(files)):
    filename = files[i]
    
    t, volt1, volt2, _, rampa1, rampa2 = loadtxt(filename, comments='"', unpack=True)
    t = t*1000 #ms
    volt1 = volt1*1000 #mV
    volt2 = volt2*1000 #mV
    dt = 0.68*0.5*(t[1] - t[0])
    dt = 10e-6
    dV = 10
    
    volt = (volt1 + volt2) / 2
    
    D = t[argmin(volt)]
    A = volt[argmin(volt)]
    B = -24
    p0 = [A, B, 36, D, 200]
    curva = CurveModel(trasmittivita, symb=True)
    out = fit_curve(curva, t, volt, dy=dV, dx=dt, p0=p0, pfix=[False,True,True,False,False],absolute_sigma=False, method='odrpack')
    par = out.par
    cov = out.cov
    err = sqrt(diag(cov))
    
    print(numbers[i], 'F = %s' %xe(par[4],err[4]), std(diff(volt)))
    if numbers[i] != '06c':
        subplot(altez, largh, n_subplot)
        ylim(-550,0)
        if len(files)-n_subplot <= largh:
            xlabel('t [ms]')
        if (n_subplot-1)%largh != 0: 
            yticks(array([]))
        else:
            ylabel('segn. [mV]')
        n_subplot += 1
        plot(t, volt, '.k', markersize=1, label='file: %s\n$F$ = %.0f' % tuple((numbers[i],par[4])))
        #plot(t, trasmittivita_p(t, *p0))
        plot(t, trasmittivita_p(t, *par), color='tab:red', alpha=0.7)
        if argmin(volt)<150:
            legend(loc=4, markerscale=0, fontsize='medium', framealpha=0)
        else:
            legend(loc=3, markerfirst=False, markerscale=0, fontsize='medium', framealpha=0)
    else:
        figure(numbers[i]).set_tight_layout(True)
        clf()
        ylim(-500,0)
        yticks(fontsize='medium')
        xticks(fontsize='large')
        ylabel('segnale [mV]', fontsize='large')
        xlabel('t [ms]', fontsize='large')
        plot(t, volt, '.k', markersize=3,label='file: %s\n$F$ = %.0f' % tuple((numbers[i],par[4])))
        plot(t, trasmittivita_p(t, *par), color='tab:red', linewidth=2, alpha=0.7)
        legend(loc=4, markerscale=0, fontsize='x-large', framealpha=0)
        figure('finezza_fit')
    
    finezza.append(par[4])

finezza = array(finezza)

#stimo l'errore sistematico con la std a terne corrispondenti
def primo_char_diverso(str1, str2):
    for a, b in zip(str1, str2):
        if a != b:
            return a
molt = []
start = -1
for i in range(len(finezza)-1):
    #idea: terne corrispondenti hanno quasi lo stesso nome
    if primo_char_diverso(numbers[i], numbers[i+1]).isalpha():
        buffo=0
    else:
        molt.append(i-start)
        start = i
molt.append(len(finezza)-array(molt).sum())
#finalmente calcolo l'errore sistemetico
deviazioni_standard = []
start = 0
for i in range(len(molt)):
    if molt[i] > 1:
        deviazioni_standard.append(std(finezza[start:start+molt[i]], ddof=1))
        start += molt[i]
    else:
        start += 1
        
def qmean(a):
    return sqrt(mean(array(a)**2))
err_statistico = std(finezza)/sqrt(len(finezza)-1)
err_sistematico = qmean(deviazioni_standard)
print(finezza.mean(), '+-', err_statistico, '+-', err_sistematico)
print('errore totale =', qmean([err_statistico, err_sistematico])*sqrt(2))