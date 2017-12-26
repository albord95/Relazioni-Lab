"""script che calcola la finezza di un Fabry-Perot con F = FSR/FWHM"""

from pylab import *
from lab import fit_curve

numeri = ['02a','02b','02c','03a','03b','03c','04a','04b','04c','05a','05b','05c','06a', '06b','06c','07a','07b','07c','08a','08b','08c','09a','09b','09c','10a','10b','11a', '11b','12a','13a','13b','14a','14b','15a','15b','16a','16b']

files = ['borcapasv00.txt']*len(numeri)
for j in range(len(files)):
    files[j] = 'borcapasv' + numeri[j] + '.txt'
FSR = 36

figure('finezza_FWHM').set_tight_layout(True)
clf()
params = {'axes.labelsize': 'small',
         'xtick.labelsize':'small',
         'ytick.labelsize':'small'}
rcParams.update(params)

largh = 4
altez = 9

n_subplot = 1
finezza = []
for i in range(len(files)):
    filename= files[i]
    #cambio virgole in punti nel file .txt
    f = open(filename,'r')
    filedata = f.read()
    f.close()
    newdata = filedata.replace(",",".")
    f = open(filename,'w')
    f.write(newdata)
    f.close()
    
    t, volt1, volt2, _, rampa1, rampa2 = loadtxt(filename, comments='"', unpack=True)
    t = t*1000 #ms
    volt1 = volt1*1000 #mV
    volt2 = volt2*1000 #mV
    dt = 0.68*0.5*(t[1] - t[0])
    #dV = min(diff(volt1)) #risoluzione
    dV = 5
    
    volt = (volt1 + volt2) / 2
    volt=volt2
    
    altezza = max(volt) - min(volt)
    level = altezza/5
    HM = (min(volt) + max(volt)) / 2 #volt a metà altezza
        
    #prendo un po' di punti attorno alla metà altezza               
    indici_prima = []
    indici_dopo = []
    zona = 'prima'
    
    for k in range(len(volt)):
        if (zona == 'prima') & (volt[k] > HM - level) & (volt[k] < HM + level):
            indici_prima.append(k)
        if volt[k] == min(volt):
            zona = 'dopo'
        if (zona == 'dopo') & (volt[k] > HM - level) & (volt[k] < HM + level):
            indici_dopo.append(k)
    if min(len(indici_prima), len(indici_dopo)) < 10:
        print('ATTENZIONE: pochi punti per interpolare')
    
    
    
    def parabola(y, a, b, c):
        return a + b*y + c
    #uso una parabola per interpolare (attenzione uso x = ay^2 + by + c)
    out = fit_curve(parabola, volt[indici_prima], t[indici_prima], p0=[1,1,1], absolute_sigma=False)
    par1 = out.par
    t_prima = parabola(HM, *par1)
    #print('parametri parabola sinistra: ', par)
    out = fit_curve(parabola, volt[indici_dopo], t[indici_dopo], p0=[1,1,1], absolute_sigma=False)
    par2 = out.par
    t_dopo = parabola(HM, *par2)
    FWHM = t_dopo - t_prima
    #print('parametri parabola destra:   ', par)
    
    if numeri[i] != '06c':
        subplot(altez, largh, n_subplot)
        ylim(-550,0)
        if len(files)-n_subplot <= largh:
            xlabel('t [ms]')
        if (n_subplot-1)%largh != 0: 
            yticks(array([]))
        else:
            ylabel('segn. [mV]')
        n_subplot += 1
        plot(parabola(sort(volt[indici_prima]), *par1), sort(volt[indici_prima]), '-c', linewidth=3)
        plot(parabola(sort(volt[indici_dopo]), *par2), sort(volt[indici_dopo]), '-c', linewidth=3)
        plot(t, volt, '.k', markersize=1, label='file: %s\n$F$ = %.0f' % tuple((numeri[i],FSR/FWHM)))
        plot([t_prima, t_dopo], [HM, HM], '-', linewidth=3,color='tab:red')
        if argmin(volt)<150:
            legend(loc=4, markerscale=0, fontsize='medium', framealpha=0)
        else:
            legend(loc=3, markerfirst=False, markerscale=0, fontsize='medium', framealpha=0)
    else:
        figure(numeri[i]).set_tight_layout(True)
        clf()
        ylim(-500,0)
        yticks(fontsize='medium')
        xticks(fontsize='large')
        ylabel('segnale [mV]', fontsize='large')
        xlabel('t [ms]', fontsize='large')
        plot(parabola(sort(volt[indici_prima]), *par1), sort(volt[indici_prima]), '-c', linewidth=5)
        plot(parabola(sort(volt[indici_dopo]), *par2), sort(volt[indici_dopo]), '-c', linewidth=5)
        plot(t, volt, '.k', markersize=3, label='file: %s\n$F$ = %.0f' % tuple((numeri[i],FSR/FWHM)))
        plot([t_prima, t_dopo], [HM, HM], '-', linewidth=5, color='tab:red')
        legend(loc=4, markerscale=0, fontsize='x-large', framealpha=0)
        figure('finezza_FWHM')
    
    finezza.append(FSR/FWHM)
    print('finezza = ', FSR/FWHM)

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
    if primo_char_diverso(numeri[i], numeri[i+1]).isalpha():
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
print('errore =', qmean([err_statistico, err_sistematico])*sqrt(2))
