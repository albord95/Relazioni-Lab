"""riassunto comandi utili per le figure"""

from pylab import *

x = arange(10)
y = arange(10)

figure('nome').set_tight_layout(True) #tight_layout serve ad aggiustare bene i margini
clf()

plot(x, y, '*--', color='tab:red', label='retta', markersize=10, linewidth=2) #color='tab:colore' usa i colori di default, che sono carini
errorbar(x, y+2, yerr=1, xerr=0.5, fmt='o') #color, label, markersize come in plot

xlabel('x [$\mu$.a.]', fontsize='medium')
ylim(0,12)

legend(loc=0, fontsize='x-large') #loc=0, che si può omettere, mette la legend dove gli pare, loc=1-4 per metterla agli angoli, loc=5-9 per metterla in giro