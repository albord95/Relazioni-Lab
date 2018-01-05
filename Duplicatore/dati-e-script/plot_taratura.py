"""plot taratura duplicatore di frequenza"""

from pylab import *

grad, power = loadtxt('borcapDVtaratura01.txt', unpack= True)

#trovo e tolgo il 400
index400 = argmax(grad)
prettygrad = concatenate((grad[:index400], grad[index400+1:]))
prettypower = concatenate((power[:index400], power[index400+1:]))


figure('taratura').set_tight_layout(True)
clf()
errorbar(arange(len(prettygrad)), prettypower, fmt='.', yerr=prettypower*0.03, elinewidth=2, label='errore di calibrazione (3%)', markersize=7)
#errorbar(arange(len(prettygrad)), prettypower, fmt='.k', yerr=prettypower*0.01, elinewidth=3, markersize=7, label='errore statistico (1%)')
xlabel('angolo [grad]', fontsize='large')
ylabel('potenza [mW]', fontsize='large')
xticks(arange(len(prettygrad)), prettygrad.astype(int), rotation=60, fontsize='small')
legend(loc=3, fontsize='x-large')

derivataseconda = diff(diff(power))
figure(2).set_tight_layout(True)
clf()
plot(derivataseconda)
xlabel('angolo [grad]', fontsize='large')
ylabel('derivata discreta della potenza [mW]', fontsize='large')
ylim(-46, 25)
xticks(arange(len(prettygrad)), prettygrad.astype(int), rotation=60, fontsize='small')

indicibuoni = []
for i in range(len(derivataseconda)):
    if abs(derivataseconda[i]) < 50:
        indicibuoni.append(i)
indicubuoni = array(indicibuoni)

figure(4).set_tight_layout(True)
clf()
plot(derivataseconda[indicibuoni])
xticks(arange(len(prettygrad[indicibuoni])), prettygrad[indicibuoni].astype(int), rotation=60, fontsize='small')

buoni = derivataseconda[indicibuoni]
stdmobile = []
for i in range(len(buoni)-10):
    stdmobile.append(buoni[i:i+10].std())
    
figure(5)
clf()
plot(stdmobile)
    