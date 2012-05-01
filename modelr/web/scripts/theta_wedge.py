'''
Created on Apr 30, 2012

@author: sean
'''
from argparse import ArgumentParser
from modelr.reflectivity import create_theta
import matplotlib
import matplotlib.pyplot as plt
import tempfile
from os import unlink
from modelr.rock_properties import RockProperties, zoeppritz
import numpy as np

short_description = 'Create an ...'

def add_arguments(parser):
    
    parser.add_argument('title', default='Plot', type=str, help='The title of the plot')
    parser.add_argument('xlim', type=float, action='list')
    parser.add_argument('pad', default=50, type=int, help='The time in mili seconds aboe and below the wedge')
    parser.add_argument('thickness', default=50, type=int, help='The maximum thickness of the wedge')
    
    parser.add_argument('rho0', type=float, default=.3, help='lower', required=True)
    parser.add_argument('rho1', type=float, default=.3, help='upper', required=True)

    parser.add_argument('vp0', type=float, default=.3, help='lower', required=True)
    parser.add_argument('vp1', type=float, default=.3, help='upper', required=True)

    parser.add_argument('vs0', type=float, help='lower')
    parser.add_argument('vs1', type=float, help='upper')
    
    parser.add_argument('theta', type=float, action='list', help='Angle of incidence')
    
    parser.add_argument('f', type=float, help='frequency', default=25)
    parser.add_argument('points', type=int, help='choose ... ', default=100)
    parser.add_argument('reflectivity_method', type=str, help='choose ... ', default='zoeppritz')
    return parser

methods = {'zoeppritz': zoeppritz,
           'const': lambda r1, r2, theta: 0.3}

def run_script(args):
    
    matplotlib.interactive(False)
    
    Rprop0 = RockProperties(args.vp0, args.vs0, args.rho0) 
    Rprop1 = RockProperties(args.vp1, args.vs1, args.rho1)
    
    theta = np.arange(args.theta[0], args.theta[1], args.theta[2])
    
    reflectivity_method = methods[args.reflectivity_method]
    
    warray_amp = create_theta(args.pad, args.thickness,
                              Rprop0, Rprop1, theta, args.f, args.points, reflectivity_method)
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    plt.gray()
    aspect = float(warray_amp.shape[1]) / warray_amp.shape[0]
    ax1.imshow(warray_amp, aspect=aspect)
    
    plt.title(args.title % locals())
    plt.ylabel('time (ms)')
    plt.xlabel('trace')
    
    fig_path = tempfile.mktemp('.jpeg')
    plt.savefig(fig_path)
    
    with open(fig_path, 'rb') as fd:
        data = fd.read()
        
    unlink(fig_path)
        
    return data
    
    
def main():
    parser = ArgumentParser(usage=short_description, description=__doc__)
    add_arguments(parser)
    args = parser.parse_args()
    run_script(args)
    
if __name__ == '__main__':
    main()