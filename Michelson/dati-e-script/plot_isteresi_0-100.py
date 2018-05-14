from pylab import *
from trova_tempi_frange import t_semifrange
from lab import fit_curve, xe


files_frange = ['borcapMMfrangeisteresi03.txt', 'borcapMMfrangeisteresi04.txt']
files_volt = ['borcapMMvoltisteresisalita03.txt', 'borcapMMvoltisteresidiscesa04.txt']
cuts = [[10, 302], [0, 310]]
d_start = 0
verso = 1 # 1 = salita, -1 = discesa

figure('isteresi_0-100').set_tight_layout(True)
clf()
xlabel('alimentazione piezoelettrico [V]')
ylabel('$d$ [$\mu$m]')

def retta(x, a, b):
    return a*x + b

for i in range(len(files_frange)):
    t, frange = loadtxt(files_frange[i], unpack = True)
    tempi_semifrange = t_semifrange(frange, t, cuts[i][0], cuts[i][1], figname=files_frange[i])
    volt = loadtxt(files_volt[i], usecols=(3),unpack = True)
    V = zeros(len(tempi_semifrange))
    T = zeros(len(tempi_semifrange))
    
    for i in range(len(tempi_semifrange)):
        T[i] = floor(tempi_semifrange[i])
        DeltaT = tempi_semifrange[i] - T[i]
        DeltaV = volt[int(T[i]+1)] - volt[int(T[i])]
        V[i] = volt[int(T[i])] + DeltaV * DeltaT
    
    d = d_start*ones(len(T)) + verso*0.633*(arange(len(tempi_semifrange)))/2
    d_start = d[-1]
    verso = -verso
    dV = 0.2*ones(len(V)) #errore della fluttuazione a occhio delle cifre del voltmetro
    dd = 2*((max(d) - min(d))/len(d))*ones(len(d)) #errore = 1 frangia
    
    figure('isteresi_0-100')
    errorbar(V, d, yerr=dd, xerr=dV, fmt='.')
    
    cut1 = 0
    j = 0
    while abs(V[0]-V[j]) < 51:
        cut2 = j
        j += 1
    
    m = []
    for k in range(2):
        out = fit_curve(retta, V[cut1:cut2], d[cut1:cut2], dy=dd[cut1:cut2], dx=dV[cut1:cut2], p0=[1,1], absolute_sigma=True)
        par = out.par
        cov = out.cov
        dpar = sqrt(diag(cov))
        plot(V[cut1:cut2], retta(V[cut1:cut2], *par), label='coeff. angolare = {} $\mu$m/V'.format(xe(par[0], dpar[0])))
        m.append(par[0])
        cut1 = cut2
        cut2 = len(V)
    print('differenza relativa = ', abs(m[0]-m[1])/ ((m[0] + m[1]) / 2) )

legend(fontsize='large')