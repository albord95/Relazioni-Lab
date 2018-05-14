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

def trova_t_picchi(sin, time, cut1=0, cut2=-1):
    """applico un algoritmo per trovare i tempi dei picchi di una sinusoide"""
    """i cut in argomento sono tempi"""
    l = len(sin)
    cutindex1 = 0
    cutindex2 = l-1
    for i in range(l-1):
        if time[i] < cut1:
            cutindex1 += 1
        if time[i] < cut2:
            cutindex2 = i
    
    """media mobile su +-5 punti per smussare un po'"""
    N = 5
    sin = numpy.convolve(sin, numpy.ones((N,))/N, mode='same')
    picco = []
    level = 'basso'
    h = sin.mean() #livello di trigger
    for i in range(cutindex1,cutindex2):
        if level == 'basso':
            if (sin[i] <= h) & (sin[i+1] > h):
                picco1 = time[i]
                level = 'alto'
        if level == 'alto':
            if (sin[i] >= h) & (sin[i+1] < h):
                picco2 = time[i]
                level = 'basso'
                picco.append((picco1 + picco2)/2)
    lenrun1 = len(picco)
                
    """ora stimo la lunghezza di un periodo e liscio la sinusoide convolvendola
       con una funzione caratteristica larga meno di 1/4 di periodo"""
    diff = numpy.diff(picco)
    T = diff.mean()
    Totaltime = time[-1]
    periodi = Totaltime/T
    puntiperperiodo = len(time)/periodi
    N = int(pylab.ceil(puntiperperiodo)/6)
    sin2 = numpy.convolve(sin, numpy.ones((N,))/N, mode='same')
    
    "riapplico l'algoritmo alla sinusoide ripulita"
    nuovopicco = []
    level = 'basso'
    N = 30*int(pylab.ceil(puntiperperiodo))
    vh = numpy.convolve(sin, numpy.ones((N,))/N, mode='same')
    for i in range(cutindex1,cutindex2):
        if level == 'basso':
            if (sin2[i] <= h) & (sin2[i+1] > h):
                picco1 = time[i]
                level = 'alto'
        if level == 'alto':
            if (sin2[i] >= h) & (sin2[i+1] < h):
                picco2 = time[i]
                level = 'basso'
                nuovopicco.append((picco1 + picco2)/2)
                
    lenrun2 = len(nuovopicco)
    
    pylab.figure(1)
    pylab.clf()
    pylab.subplot(311)
    pylab.xlim(-1,time[-1]+1)
    pylab.plot(time, sin) #sinusoide
    pylab.plot(time,h*ones(len(time))) #media mobile
    pylab.plot(time[cutindex1:cutindex2], sin2[cutindex1:cutindex2]) #sinusoide ripulita
    pylab.subplot(312)
    pylab.xlim(-1,time[-1]+1)
    #pylab.plot(picco[:-1], numpy.diff(picco)) #lunghezza periodi
    pylab.plot(nuovopicco[:-1], numpy.diff(nuovopicco))

    sin2 = -sin2
    h = -h            
    nuovopicco2 = []
    level = 'basso'
    N = 30*int(pylab.ceil(puntiperperiodo))
    vh = numpy.convolve(sin, numpy.ones((N,))/N, mode='same')
    for i in range(cutindex1,cutindex2):
        if level == 'basso':
            if (sin2[i] <= h) & (sin2[i+1] > h):
                picco1 = time[i]
                level = 'alto'
        if level == 'alto':
            if (sin2[i] >= h) & (sin2[i+1] < h):
                picco2 = time[i]
                level = 'basso'
                nuovopicco2.append((picco1 + picco2)/2)
                
    subplot(313)
    pylab.xlim(-1,time[-1]+1)
    pylab.plot(nuovopicco2[:-1], numpy.diff(nuovopicco2))
    
    print('periodi = (', len(picco), '+', len(nuovopicco2), ')/2 = ', (len(nuovopicco)+len(nuovopicco2))/2) 
    return nuovopicco