from pylab import *

##cambio virgole in punti del file che voglio importare
filename = 'borcapMM06.txt'
f = open(filename,'r')
filedata = f.read()
f.close()
newdata = filedata.replace(",",".")
f = open(filename,'w')
f.write(newdata)
f.close()

t, frange = loadtxt(filename, unpack = True)

def trigger(sin, time, cut1=0, cut2=-1, start='basso'):
    """applico un algoritmo per trovare i tempi dei picchi di una sinusoide"""
    l = len(sin)
    cutindex1 = 0
    cutindex2 = l-1
    for i in range(l-1):
        if time[i] < cut1:
            cutindex1 += 1
        if time[i] < cut2:
            cutindex2 = i
    
    N = 5
    sin = convolve(sin, ones((N,))/N, mode='same')
    picco = []
    level = start
    h = sin.mean()
    for i in range(cutindex1,cutindex2):
        if level == 'basso':
            if (sin[i] <= h) & (sin[i+1] > h):
                picco1 = time[i]
                level = 'alto'
                picco.append(picco1)
        if level == 'alto':
            if (sin[i] >= h) & (sin[i+1] < h):
                picco2 = time[i]
                level = 'basso'
                picco.append(picco2)
    for i in range(len(picco)-1):
        picco[i] = (picco[i] + picco[i+1]) / 2
    picco = picco[:-1]
                
    """ora stimo la lunghezza di un periodo e liscio la sinusoide convolvendola
       con una funzione caratteristica larga meno di 1/4 di periodo"""
    differenze = diff(picco)
    T = 2*differenze.mean()
    Totaltime = time[len(time)-1]
    periodi = Totaltime/T
    puntiperperiodo = len(time)/periodi
    N = int(ceil(puntiperperiodo)/6)
    sin2 = convolve(sin, ones((N,))/N, mode='same')
    
    "riapplico l'algoritmo alla sinusoide ripulita"
    picco = []
    for i in range(cutindex1,cutindex2):
        if level == 'basso':
            if (sin[i] <= h) & (sin[i+1] > h):
                picco1 = time[i]
                level = 'alto'
                picco.append(picco1)
        if level == 'alto':
            if (sin[i] >= h) & (sin[i+1] < h):
                picco2 = time[i]
                level = 'basso'
                picco.append(picco2)
    for i in range(len(picco)-1):
        picco[i] = (picco[i] + picco[i+1]) / 2
    picco = picco[:-1]
    
    figure(0)
    clf()
    subplot(211)
    xlim(-1,time[len(time)-1]+1)
    plot(time, sin) #sinusoide
    plot(time,h*ones(len(time))) #media mobile
    plot(time[cutindex1:cutindex2], sin2[cutindex1:cutindex2]) #sinusoide ripulita
    subplot(212)
    xlim(-1,time[-1]+1)
    #pylab.plot(picco[:-1], numpy.diff(picco)) #lunghezza periodi
    plot(picco[:-1], diff(picco))

    return picco

picco = trigger(frange, t)