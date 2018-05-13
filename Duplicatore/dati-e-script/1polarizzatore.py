"""fit legge cos alla 4"""

from pylab import *
from lab import fit_curve, xe

angolo, Vpp, dVpp = loadtxt('borcapDVTvs1P01.txt', unpack= True) #gradi, mV, mV

figure('1polarizzatore').set_tight_layout(True)
clf()
#errorbar(angolo, Vpp, yerr=dVpp, fmt='.-k')

Wmax = 284.5
Wmin = 154.5
ratio = 154.5 / 284.5
b2sua2 = (1 / ratio)**2
angolo0 = 29

V = Vpp / ((cos((angolo + angolo0)*pi/180)**2 + ratio*sin((angolo + angolo0)*pi/180)**2)**2)
dV = dVpp / ((cos((angolo + angolo0)*pi/180)**2 + ratio*sin((angolo + angolo0)*pi/180)**2)**2)
dy = 1.5*ones(len(angolo)) / ((cos((angolo + angolo0)*pi/180)**2 + ratio*sin((angolo + angolo0)*pi/180)**2)**2)
dx = ones(len(angolo))

errorbar(angolo, V, yerr=dy, xerr=dx, fmt='.k')

V2 = Vpp*(cos((angolo + angolo0)*pi/180)**2 + b2sua2*sin((angolo + angolo0)*pi/180)**2)
dV2 = dVpp*(cos((angolo + angolo0)*pi/180)**2 + b2sua2*sin((angolo + angolo0)*pi/180)**2)
dy2 = 1.5*ones(len(angolo))*(cos((angolo + angolo0)*pi/180)**2 + b2sua2*sin((angolo + angolo0)*pi/180)**2)

#errorbar(angolo, V2, yerr=dV2, xerr=dx, fmt='.k')

def cos4(x, a, b):
    return a*(cos((x-b)*pi/180))**4

out = fit_curve(cos4, angolo, Vpp, dy=dVpp, dx=dx, p0=[60, -10])
par0 = out.par
cov0 = out.cov

out = fit_curve(cos4, angolo, V, dy=dy, dx=dx, p0=[120, -10])
par1 = out.par
cov1 = out.cov
err1 = sqrt(diag(cov1))
chi2norm1 = out.chisq / out.chisq_dof
print('chi2norm = ', chi2norm1)
print('p-value = ', out.chisq_pvalue)
print('parameters = ', par1)
print('errors     = ', err1)


out = fit_curve(cos4, angolo, V2, dy=dy2, dx=dx, p0=[80, -10])
par2 = out.par
cov2 = out.cov
err2 = sqrt(diag(cov2))
chi2norm2 = out.chisq / out.chisq_dof
print('chi2norm = ', chi2norm)
print('p-value = ', out.chisq_pvalue)
print('parameters = ', par2)
print('errors     = ', err2)

#plot(angolo, cos4(angolo, *par0), '-k')
plot(angolo, cos4(angolo, *par1), '-g', label='$y = a \cdot \cos^4(x-b)$\n$\\frac{\chi^2}{dof} = %.2f$\n$b_{fit} = %s °$' %(chi2norm1,xe(par1[1],err1[1])))
#plot(angolo, cos4(angolo, *par2), '-g', label='$y = a \cdot \cos^4(x-b)$\n$\\frac{\chi^2}{dof} = %.2f$\n$b_{fit} = %s$' %(chi2norm2,xe(par2[1],err2[1])))
legend(fontsize='x-large')
xlabel('$\\varphi$ [°]', fontsize='large')
ylabel('intensità della seconda armonica [u.a.]', fontsize='large')