"""plot taratura duplicatore di frequenza"""

from pylab import *

grad, Vpp, dVpp = loadtxt('borcapVLTvsAng01.txt', unpack= True)
tgrad, tpower = loadtxt('borcapVLtaratura01.txt', unpack= True)


power = zeros(len(Vpp))
for i in range(len(power)):
    for j in range(len(tpower)):
        if grad[i] == tgrad[j]:
            power[i] = tpower[j]
            break

dpower = power*0.03
    
dy = 0.68*0.5*dVpp 
dx = dpower

figure(1).set_tight_layout(True)
clf()
errorbar(power, Vpp, fmt='.', yerr=dVpp, xerr=power*0.03, markersize=4)
xlim(0, 1.05*max(power))
ylabel('intensità [mV]', fontsize='large')
xlabel('potenza [mW]', fontsize='large')

figure(2).set_tight_layout(True)
clf()
errorbar(arange(len(tgrad)), tpower, fmt='.', yerr=tpower*0.03, elinewidth=2, label='errore di calibrazione (3%)', markersize=3)
#errorbar(arange(len(prettygrad)), prettypower, fmt='.k', yerr=prettypower*0.01, elinewidth=3, markersize=7, label='errore statistico (1%)')
xlabel('angolo [grad]', fontsize='large')
ylabel('potenza [mW]', fontsize='large')
xticks(arange(len(tgrad)), tgrad.astype(int), rotation=70, fontsize='xx-small')
legend(fontsize='x-large')

'''derivataseconda = diff(diff(tpower))
figure(3).set_tight_layout(True)
clf()
plot(derivataseconda)
xlabel('angolo [grad]', fontsize='large')
ylabel('derivata discreta della potenza [mW]', fontsize='large')
ylim(-46, 25)
xticks(arange(len(tgrad)), grad.astype(int), rotation=60, fontsize='small')

indicibuoni = []
for i in range(len(derivataseconda)):
    if abs(derivataseconda[i]) < 50:
        indicibuoni.append(i)
indicubuoni = array(indicibuoni)

figure(4).set_tight_layout(True)
clf()
plot(derivataseconda[indicibuoni])
xticks(arange(len(tgrad[indicibuoni])), tgrad[indicibuoni].astype(int), rotation=60, fontsize='small')

buoni = derivataseconda[indicibuoni]
stdmobile = []
for i in range(len(buoni)-10):
    stdmobile.append(buoni[i:i+10].std())
    
figure(5)
clf()
plot(stdmobile)'''
    