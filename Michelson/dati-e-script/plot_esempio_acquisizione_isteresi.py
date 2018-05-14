from pylab import *
from trova_tempi_frange import t_semifrange

t, frange = loadtxt('borcapMMfrangeisteresi07.txt', unpack = True)
Tempi_salita = t_semifrange(frange, t, 10, 165)
Volt_salita = loadtxt('borcapMMvoltisteresisalita07.txt', usecols=(3),unpack = True)
V_s = zeros(len(Tempi_salita))
T_s = zeros(len(Tempi_salita))

for i in range(len(Tempi_salita)):
    T_s[i] = floor(Tempi_salita[i])
    DeltaT = Tempi_salita[i] - T_s[i]
    DeltaV = Volt_salita[int(T_s[i]+1)] - Volt_salita[int(T_s[i])]
    V_s[i] = Volt_salita[int(T_s[i])] + DeltaV * DeltaT

figure(1).set_tight_layout(True)
clf()
subplot(311)
plot(Volt_salita)
ylabel('$V(t)$ [V]')
xlabel('$t$ [s]')
#xlim(-5, 172)
subplot(312)
plot(t, frange, linewidth=1)
h = frange.mean()
plot(t,h*ones(len(t))) #media
plot(Tempi_salita, h*(ones(len(Tempi_salita))), '|', color='r', markersize=15)
ylabel('intensità frange [V]')
xlabel('$t$ [s]')
#xlim(-5, 172)
subplot(313)
d_s = 0.633*(arange(len(Tempi_salita)))/2
plot(V_s, d_s, '.')
ylabel('d [$\mu$m]')
xlabel('V piezoelettrico [V]')
#xlim(29, 71)
