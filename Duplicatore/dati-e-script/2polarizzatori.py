"""fit legge di malus"""

from pylab import *
from lab import fit_curve, xe

angolo, Vpp, dVpp = loadtxt('borcapDVTvs2P01.txt', unpack= True) #gradi, mV, mV

dy = 1.5*ones(len(dVpp)) 
dx = 0.68*0.5*ones(len(dVpp))            

figure('2polarizzatori').set_tight_layout(True)
clf()
errorbar(angolo, Vpp, yerr=dy, fmt='.k')

def cos2(x, a, b):
    return a*(cos((x-b)*pi/180))**2

def cos2o(x, a, b, c):
    return a*(cos((x-b)*pi/180))**2 + c

out = fit_curve(cos2, angolo, Vpp, dy=dy, p0=[60, -90])
par = out.par
cov = out.cov
err = sqrt(diag(cov))
chi2norm = out.chisq/out.chisq_dof
pvalue = out.chisq_pvalue


out = fit_curve(cos2o, angolo, Vpp, dy=dy, p0=[60, -90, 1])
paro = out.par
covo = out.cov
erro = sqrt(diag(covo))
print(paro, erro)
chi2normo = out.chisq/out.chisq_dof
pvalueo = out.chisq_pvalue

plot(angolo, cos2(angolo, *par), '-', color='tab:orange', label='$y = a \cdot \cos^2(x-b)$\n$\\frac{\chi^2}{dof} = %.2f \qquad b_{fit} = %s$\n' %(chi2norm,xe(par[1],err[1])))
plot(angolo, cos2o(angolo, *paro), '-', color='tab:green', label='$y = a \cdot \cos^2(x-b) + c$\n$\\frac{\chi^2}{dof} = %.2f \qquad b_{fit} = %s$' %(chi2normo,xe(paro[1],erro[1])))
legend(fontsize='x-large', loc=0)
xlabel('$\\varphi$ [°]', fontsize='large')
ylabel('$V_{pp}$ [mV]', fontsize='large')