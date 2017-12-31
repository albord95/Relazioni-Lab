from pylab import *
from lab import fit_curve, xe
from uncertainties import ufloat
from uncertainties import umath as um
from uncertainties import unumpy

def qmean(a):
    return sqrt(mean(array(a)**2))



pin633_1 = ufloat(1630, 0.03*1630)
pin633_2 = ufloat(2440, 0.03*2440)
pout633_1 = ufloat(598, 0.03*598)
pout633_2 = ufloat(832, 0.03*832)

pin532_1 = ufloat(1470, 0.03*1470)
pin532_2 = ufloat(2800, 0.03*2800)
pout532_1 = ufloat(156, 0.03*156)
pout532_2 = ufloat(320, 0.03*320)

pin633_1 = ufloat(1630,20)
pin633_2 = ufloat(2440,30)
pout633_1 = ufloat(598,2)
pout633_2 = ufloat(832,2)

pin532_1 = ufloat(1470,20)
pin532_2 = ufloat(2800,30)
pout532_1 = ufloat(156,2)
pout532_2 = ufloat(320,2)

l633_1 = ufloat(293.5,0.5)
l633_2 = ufloat(289.2,0.5)
l532_1 = ufloat(291.3,0.5)
l532_2 = ufloat(287.1,0.5)

lamb = [633, 532]
lamb_n = [850, 1300]
atten_n = [ufloat(4,0.1), ufloat(1.5, 0.1)]
atten_1 = array([um.log10(pin633_1/pout633_1)/l633_1, um.log10(pin532_1/pout532_1)/l532_1])*10000
atten_2 = array([um.log10(pin633_2/pout633_2)/l633_2, um.log10(pin532_2/pout532_2)/l532_2])*10000
print('attenuazione1 532 = %s' %xe(atten_1[1].n, atten_1[1].s))
print('attenuazione2 532 = %s' %xe(atten_2[1].n, atten_2[1].s))
print('attenuazione1 633 = %s' %xe(atten_1[0].n, atten_1[0].s))
print('attenuazione2 633 = %s' %xe(atten_2[0].n, atten_2[0].s))

sigma633 = std(array([atten_1[0].n, atten_2[0].n,]), ddof=1)
sigma532 = std(array([atten_1[1].n, atten_2[1].n,]), ddof=1)
print('sigma 532  = %.2f' % sigma532)
print('sigma 633  = %.2f' % sigma633)
print('mean sigma = %.2f' % qmean([sigma532, sigma633]))

#fit
tuttilamb = array(lamb + lamb + lamb_n)
mieilamb = array(lamb + lamb)
tuttiatten = array(list(atten_1) + list(atten_2) + atten_n)
tuttiatten = unumpy.nominal_values(tuttiatten)
mieiatten = array(list(atten_1) + list(atten_2))
mieiatten = unumpy.nominal_values(mieiatten)
dy = [0.93,0.45,0.93,0.45]

def xalla4(x, a):
    return a*x**(-4)
def xallab(x, a, b):
    return a*x**b
out = fit_curve(xalla4, mieilamb.astype(float), mieiatten, dy=dy, p0=[2e13], absolute_sigma=True)
par4 = out.par
cov4 = out.cov
chi2norm = out.chisq / out.chisq_dof
print('punti misurati: chi2/dof = %.2f/%d = %.2f' % (out.chisq, out.chisq_dof, chi2norm))
std4 = sqrt(diag(cov4))
out = fit_curve(xallab, mieilamb.astype(float), mieiatten, dy=dy, p0=[2e12, -4], absolute_sigma=True)
parb = out.par
covb = out.cov
stdb = sqrt(diag(covb))

out = fit_curve(xalla4, array(lamb_n).astype(float), unumpy.nominal_values(atten_n), dy=unumpy.std_devs(atten_n), p0=[2e13], absolute_sigma=True)
par4d = out.par
cov4d = out.cov
chi2normd = out.chisq / out.chisq_dof
print('punti datasheet: chi2/dof = %.2f/%d = %.2f' % (out.chisq, out.chisq_dof, chi2normd))
std4d = sqrt(diag(cov4d))
out = fit_curve(xallab, array(lamb_n).astype(float), unumpy.nominal_values(atten_n), dy=unumpy.std_devs(atten_n), p0=[2e13, -4], absolute_sigma=True)
parbd = out.par
covbd = out.cov
stdbd = sqrt(diag(covbd))

out = fit_curve(xalla4, array(tuttilamb).astype(float), tuttiatten, dy=dy + list(unumpy.std_devs(atten_n)), p0=[2e13], absolute_sigma=True)
par4t = out.par
cov4t = out.cov
chi2normt = out.chisq / out.chisq_dof
print('tutti i punti: chi2/dof = %.2f/%d = %.2f' % (out.chisq, out.chisq_dof, chi2normt))
std4t = sqrt(diag(cov4d))
out = fit_curve(xallab, array(tuttilamb).astype(float), tuttiatten, dy=dy + list(unumpy.std_devs(atten_n)), p0=[2e13, -4], absolute_sigma=True)
parbt = out.par
covbt = out.cov
stdbt = sqrt(diag(covbd))

figure(1).set_tight_layout(True)
clf()
subplot(211)
cap = 5
errorbar(lamb, unumpy.nominal_values(atten_1), yerr=[sigma633, sigma532], fmt='.', capsize=cap)
errorbar(lamb, unumpy.nominal_values(atten_2), yerr=[sigma633, sigma532], fmt='.', capsize=cap)
errorbar(lamb_n, unumpy.nominal_values(atten_n), yerr=unumpy.std_devs(atten_n), fmt='.', capsize=cap)
xx = linspace(min(mieilamb), max(mieilamb), 2000)
plot(xx, xalla4(xx, *par4), label='$y = a \cdot x^4 \quad \quad \\frac{\chi^2}{dof} = %.2f$' %(chi2norm))
plot(xx, xallab(xx, *parb), label='$y = a \cdot x^b \quad \quad b = %.2f$' %parb[1])
xx = linspace(min(lamb_n), max(lamb_n), 2000)
plot(xx, xalla4(xx, *par4d), label='$y = a \cdot x^4 \quad \quad \\frac{\chi^2}{dof} = %.0f$' %(chi2normd))
plot(xx, xallab(xx, *parbd), label='$y = a \cdot x^b \quad \quad b = %.2f$' %parbd[1])
ylabel('attenuazione [dB/km]')
xlabel('$\lambda$ [nm]')
legend(fontsize='large')

subplot(212)
errorbar(lamb, unumpy.nominal_values(atten_1), yerr=unumpy.std_devs(atten_1), fmt='.', capsize=cap)
errorbar(lamb, unumpy.nominal_values(atten_2), yerr=unumpy.std_devs(atten_2), fmt='.', capsize=cap)
errorbar(lamb_n, unumpy.nominal_values(atten_n), yerr=unumpy.std_devs(atten_n), fmt='.', capsize=cap)
xx = linspace(min(mieilamb), max(mieilamb), 2000)
plot(xx, xalla4(xx, *par4), label='$y = a \cdot x^4 \quad \quad \\frac{\chi^2}{dof} = %.2f$' %(chi2norm))
plot(xx, xallab(xx, *parb), label='$y = a \cdot x^b \quad \quad b = %.2f$' %parb[1])
xx = linspace(min(lamb_n), max(lamb_n), 2000)
plot(xx, xalla4(xx, *par4d), label='$y = a \cdot x^4 \quad \quad \\frac{\chi^2}{dof} = %.0f$' %(chi2normd))
plot(xx, xallab(xx, *parbd), label='$y = a \cdot x^b \quad \quad b = %.2f$' %parbd[1])
ylabel('attenuazione [dB/km]')
xlabel('$\lambda$ [nm]')
xscale('log')
yscale('log')

figure(2).set_tight_layout(True)
clf()
subplot(211)
cap = 5
errorbar(lamb, unumpy.nominal_values(atten_1), yerr=[sigma633, sigma532], fmt='.', capsize=cap)
errorbar(lamb, unumpy.nominal_values(atten_2), yerr=[sigma633, sigma532], fmt='.', capsize=cap)
errorbar(lamb_n, unumpy.nominal_values(atten_n), yerr=unumpy.std_devs(atten_n), fmt='.', capsize=cap)
xx = linspace(min(tuttilamb), max(tuttilamb), 2000)
plot(xx, xalla4(xx, *par4t), label='$y = a \cdot x^4 \quad \quad \\frac{\chi^2}{dof} = %.0f$' %(chi2normt))
plot(xx, xallab(xx, *parbt), label='$y = a \cdot x^b \quad \quad b = %.2f$' %parbt[1])
ylabel('attenuazione [dB/km]')
xlabel('$\lambda$ [nm]')
legend(fontsize='large')

subplot(212)
errorbar(lamb, unumpy.nominal_values(atten_1), yerr=unumpy.std_devs(atten_1), fmt='.', capsize=cap)
errorbar(lamb, unumpy.nominal_values(atten_2), yerr=unumpy.std_devs(atten_2), fmt='.', capsize=cap)
errorbar(lamb_n, unumpy.nominal_values(atten_n), yerr=unumpy.std_devs(atten_n), fmt='.', capsize=cap)
xx = linspace(min(tuttilamb), max(tuttilamb), 2000)
plot(xx, xalla4(xx, *par4t), label='$y = a \cdot x^4 \quad \quad \\frac{\chi^2}{dof} = %.0f$' %(chi2normt))
plot(xx, xallab(xx, *parbt), label='$y = a \cdot x^b \quad \quad b = %.2f$' %parbt[1])
ylabel('attenuazione [dB/km]')
xlabel('$\lambda$ [nm]')
xscale('log')
yscale('log')