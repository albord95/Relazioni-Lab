#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 10:45:28 2018
s
@author: Giulio
"""

from pylab import *
from scipy.optimize import curve_fit
from lab import fit_curve, xe
from gvar import gvar
from scipy.special import erf
from scipy.integrate import quad

files = ['borcapLDG12PvsI.txt',
         'borcapLDG25PvsI.txt',
         'borcapLDG43PvsI.txt']

'''figure(2).set_tight_layout(True)
clf()
params = {'axes.labelsize': 'small',
         'xtick.labelsize':'x-small',
         'ytick.labelsize':'x-small'}
rcParams.update(params)
figure(1).set_tight_layout(True)
clf()'''

for i in range(len(files)):
    filename= files[i]
    I, P = loadtxt(filename, comments='"', unpack=True)
    ##[I]=mA e [P]=muA
    
    ##faccio il grafico P-I
    figure(1)
    subplot(3, 1, 1)
    plot(I, P, '.', color='', markersize='')       

    '''##funzione di fit
    def retta(x, a, b):
        return a*x + b

    ##trovo I_th con un fit    
        m = []
        dm = []
        q = []
        dq = []
        T = ['12°C ', '25°C ', '45°C ']
        for k in range(3):
            plot(I, P, '.', color='', markersize='')
            """come errore metto (1/2)*sensibilità*0.68,
            scelta discutibile ma giustificata a spanne dal confidence level"""
            out = fit_curve(retta, I, P, dy=, p0=[1,1], absolute_sigma=True)
            par = out.par
            cov = out.cov
            m_fit = par[0]
            q_fit = par[1]
            dm_fit, dq_fit = sqrt(diag(cov))
            print('I$_{th}$ (%s): m = %s  q = %s' %(T[k], xe(m_fit, dm_fit), xe(q_fit, dq_fit)))
            m.append(m_fit)
            q.append(q_fit)
            dm.append(dm_fit)
            dq.append(dq_fit)
            plot(I, retta(I, *par), linewidth=1)
        
            ylabel('P [\mus]')
            xlabel('I ˆ[mA]')
        
        xticks(arange(1, n_ordini+1, 1))
        ylim(ylim(min(t)-0.2*(max(t)-min(t)),max(t)))
        xlim(0.5, n_ordini+0.5)'''
        