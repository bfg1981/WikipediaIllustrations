# This source code is public domain

import numpy, getopt, sys
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from localize_py import Translator

def usage():
    print ("""Usage is:\n\t %s [options] <filename>

Opions:
    -l, --lang Language code
    -h, --help This usage
""" % (sys.argv[0]))

try:
    opts, args = getopt.getopt(sys.argv[1:], "hl:", ["help", "lang="])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
lang = 'de'
for o, a in opts:
    if o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("-l", "--lang"):
        lang = a
        print(a)
    else:
        assert False, "unhandled option"

fName=args[0]


Translator.load_translations(de='localization/de.json',no='localization/no.json')
_ = Translator(lang)

G=1
k=1
f0=0.5

x = numpy.linspace(-8,8,16)[1:-1]
numpy.random.seed(50)
y =numpy.random.normal(G/(1+numpy.exp(-k*G*x)*(G/f0-1)),0.1)

err=1E8
err=numpy.mean(numpy.square(y-G/(1+numpy.exp(-k*G*x)*(G/f0-1))))
print(err,G,k,f0)
numpy.random.seed(2)
for i in range(5000):
    faktor=1+0.01*(numpy.random.rand()-.5)
    for ivar in 1,2,3:
        backup=[err,G,k,f0]
        var=backup[:]
        var[ivar]=var[ivar]*faktor
        err,G,k,f0=var

        err_neu = numpy.mean(numpy.square(y-G/(1+numpy.exp(-k*G*x)*(G/f0-1))))
        if err_neu<err:
            err=err_neu
        else:
            var[ivar]=backup[ivar]
            err,G,k,f0=var
print(err,G,k,f0,"(%s)" % (_('Fehlerquadrat minimiert')))
    
xneu = numpy.linspace(-8,8,50)
yneu = G/(1+numpy.exp(-k*G*xneu)*(G/f0-1))

xr = x
yr = G/(1+numpy.exp(-k*G*xr)*(G/f0-1))
residuen = []
for i in range(len(x)): residuen +=[ [x[i]+8, x[i]+8],[y[i]*10, yr[i]*10], 'g-']

fig = plt.figure(figsize=(4.2, 3.2))
y0 = plt.plot(*residuen[:-3], color='#60c060', linewidth=1.5)
y0, = plt.plot(*residuen[-3:],label=_('Residuum'), color='#60c060', linewidth=1.5)
y2, = plt.plot(xneu+8,yneu*10,'r-',label=_('Modelfunktion'))
plt.setp(y2, linewidth=1.5)
y1, = plt.plot(x+8,y*10,'o',label=_('Messpunkte'))
plt.xlabel('x')
plt.ylabel('y')
order = y1,y2,y0
plt.legend(order,[p.get_label() for p in order],frameon=True, loc='lower right')
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(2))
plt.grid(True, alpha=0.7)
plt.tight_layout()
plt.savefig(fName)
