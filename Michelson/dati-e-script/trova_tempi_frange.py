from pylab import *

def t_semifrange(sinusoide, time, cut1=0, cut2=-1, figname='0'):
    """applico un algoritmo per trovare i tempi dei picchi di una sinusoide"""
    l = len(sinusoide)
    cutindex1 = 0
    cutindex2 = l-1
    for i in range(l-1):
        if time[i] < cut1:
            cutindex1 += 1
        if time[i] < cut2:
            cutindex2 = i
    
    N = 5
    sinusoide = convolve(sinusoide, ones((N,))/N, mode='same')
    picco = []
    h = sinusoide.mean()
    if sinusoide[0] < h:
        level = 'basso'
    else:
        level = 'alto'
    for i in range(cutindex1,cutindex2):
        if level == 'basso':
            if (sinusoide[i] <= h) & (sinusoide[i+1] > h):
                picco1 = time[i]
                level = 'alto'
                picco.append(picco1)
        if level == 'alto':
            if (sinusoide[i] >= h) & (sinusoide[i+1] < h):
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
    N = int(ceil(puntiperperiodo)/8)
    sinusoide2 = convolve(sinusoide, ones((N,))/N, mode='same')
    
    "riapplico l'algoritmo alla sinusoideusoide ripulita"
    if sinusoide[cutindex1] < h:
        level = 'basso'
    else:
        level = 'alto'
    picco = []
    for i in range(cutindex1,cutindex2):
        if level == 'basso':
            if (sinusoide2[i] <= h) & (sinusoide2[i+1] > h):
                picco1 = time[i]
                level = 'alto'
                picco.append(picco1)
        if level == 'alto':
            if (sinusoide2[i] >= h) & (sinusoide2[i+1] < h):
                picco2 = time[i]
                level = 'basso'
                picco.append(picco2)
    for i in range(len(picco)-1):
        picco[i] = (picco[i] + picco[i+1]) / 2
    picco = picco[:-1]
    
    figure(figname)
    clf()
    subplot(211)
    xlim(-1,time[len(time)-1]+1)
    plot(time, sinusoide) #sinusoideusoide
    plot(time,h*ones(len(time))) #media
    plot(time[cutindex1:cutindex2], sinusoide2[cutindex1:cutindex2]) #sinusoideusoide ripulita
    plot(picco, h*(ones(len(picco))), '|')
    subplot(212)
    xlim(-1,time[-1]+1)
    #pylab.plot(picco[:-1], numpy.diff(picco)) #lunghezza periodi
    plot(picco[:-1], diff(picco))
    return picco