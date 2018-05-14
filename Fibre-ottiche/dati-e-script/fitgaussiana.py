
from pylab import *
from scipy.optimize import curve_fit
from lab import fit_curve

xdata, tem00, digit = loadtxt('borcapFOMLP1.txt', unpack=True)
yerr = sqrt((digit*0.5*0.68)**2 + (ones(len(tem00))*0.05)**2)
tem00 = tem00 - 0.002
                      
xerr = ones(len(xdata))*0.5*0.68

figure(1)
clf()
errorbar(xdata, tem00, yerr=yerr, xerr=xerr, fmt='.')

def gauss(x, mu, sigma, norma):
    return norma*exp(-(x-mu)**2/(2*sigma**2))

xlabel('gradi')
ylabel('P [$\mu$W]')

par0 = [194, 3, 50]
#out = fit_curve(gauss, xdata, tem00, dx=xerr/4, dy=yerr, p0=par0, method='leastsq')
out = fit_curve(gauss, xdata, tem00, dy=yerr, dx=xerr, p0=par0, method='odrpack')
par = out.par
cov = out.cov
err = sqrt(cov)
chi2 = out.chisq
dof = out.chisq_dof
chi2norm = chi2/dof
pvalue = out.chisq_pvalue
print('chi2 = ', chi2)
print('dof = ', dof)
print('chi2norm = ',chi2norm)
print('pvalue = ', pvalue)

plot(xx, gauss(xx,*par), color = 'tab:green',label='p$_0$ = 50.2(4) $\mu$W \n p$_1$ = 193.59(8) ° \n p$_2$ = 3.12(4) °')
legend()