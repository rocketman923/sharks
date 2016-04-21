#!/usr/bin/env python3

from genlsp import genlsp;
from genpbs import genpbs;
from pys import test,sd;
import re;
import os;
import shutil as sh;
lsp_d=dict(
    w=2.2e-6,
    T=40e-15,
    l=780e-9,
    I=3e18,
    fp=(0,0,0),
    lim= (-30, 5, -20,20, -20,20),
    res=( 35*10, 40*10, 40*10),
    tlim=(-27.5,0,-15,15,-15,15),
    timestep=4e-17,
    totaltime=500e-15,
    dumpinterval=5e-16,
    targetdat="watercolumn.dat",
    description="hotwater in 3d",
    domains=780,
    region_split=('z',5),
);

def mkdir(dir):
    os.makedirs(dir, exist_ok=True);

def mksim(pbsbase,**d):
    print("making {}".format(pbsbase));
    myd = sd(lsp_d, **d);
    lsp=genlsp(**myd);

    #making for different servers
    pbses=dict(
        oakley=genpbs(
            pbsbase=pbsbase,
            domains=myd['domains'],
            cluster='oakley'),
        garnet_debug=genpbs(
            pbsbase=pbsbase,
            domains=myd['domains'],
            cluster='garnet',
            queue='debug'),
        garnet=genpbs(
            pbsbase=pbsbase,
            domains=myd['domains'],
            cluster='garnet',
            queue='standard_lw'));
    mkdir(pbsbase);    
    auxs = [
        "sine700points.dat", myd['targetdat'],
        "autozipper"
    ];
    for aux in auxs:
        sh.copy(aux, pbsbase);
    pbsbase = "{0}/{0}".format(pbsbase);
    with open(pbsbase+".lsp","w") as f:
        f.write(lsp);
    for pbsk in pbses:
        fname = "{}_{}.pbs".format(
            pbsbase,pbsk);
        with open(fname,"w") as f:
            f.write(pbses[pbsk]);


Is= [5.4e17, 1e18, 1.5e18, 3e18, 1e19];

#vanillas
for I in Is:
    mksim("hotwater3d_{}".format(I),I=I);

