#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:15:29 2020

@author: kantundpeterpan
"""

from gooey import Gooey, GooeyParser

import argparse
import pandas as pd
import numpy as np
import os

from IsoSpecPy import IsoSpecPy
from tools import peak_shaper

folder = os.path.dirname(os.path.abspath(__file__))
icon_folder = os.path.join(folder,'icon')
data_folder = os.path.join(folder,'data')
print(folder)

m_proton = 1.007825032239 - 0.0005488 #H - electron (amu)
m_electron = 0.0005488

@Gooey(program_name='IsoTool',
       image_dir=icon_folder
      )
def main():
    global m_proton
    parser = GooeyParser(prog='IsoTool')
    #parser = argparse.ArgumentParser()

    parser.add_argument('Molecule', type=str, widget='FileChooser')
    
    g = parser.add_argument_group()
    isos = g.add_mutually_exclusive_group(
        required=True
        )
    
    isos.add_argument('--terrestrial',
                      metavar = 'Terrestrial abundances',
                      default = os.path.join(data_folder, 'isotopes_terrestrial.csv'),
                      dest='isotopes'
                      )
    
    isos.add_argument(
        '--custom',
        metavar='Custom isotope definitons',
        dest='isotopes',
        widget='FileChooser'
        )
    
    #parser.add_argument('-i', '--isotopes', metavar='Isotopes',
     #                   help='Isotope masses and abundances', type=str, widget='FileChooser',
      #                  default = os.path.join(folder,'isotopes_terrestrial.csv'))
    
    parser.add_argument('-o', '--output_folder', metavar='Output Folder', type=str, widget='DirChooser',
                        default = folder)    
    parser.add_argument('-z', '--charge', metavar='Charge',
                        help='z, adds protons and recalculates m/z accordingly',
                        default=1, dest='z', type=int)
    
    parser.add_argument('-r', '--resolution', metavar='Resolution',
                        help='m/z*1/FWHM, determines Gaussian peak width',
                        type=int, default=40000)
    parser.add_argument('-bs', '--binsize',
                        help='for summing Gaussian peaks of isotopologues',
                        type=float, default=0.002)
    parser.add_argument('-ps', '--points', help='no. of points for Gaussian peak',
                        type=int, default=250)
    parser.add_argument('-dmz', '--delta_mz', metavar = 'Delta m/z',
                        help='two sided mass offset for Gaussian peaks',
                        type=float, default=0.05)
    parser.add_argument('-p', '--proba', metavar = 'Probability Cutoff',
                        help='Cumulative probability threshold for isotopologue calculations',
                        type=float, default=0.9999)

    args = parser.parse_args()    

    isotopes = pd.read_csv(args.isotopes,
                       index_col='element_symbol').dropna()
    
    mol = pd.read_csv(args.Molecule).set_index('element')
    
    mol.loc['H','n'] += args.z
    
    elements =  [e for e in mol.reset_index().element.values if mol.loc[e].n>0]

    atoms = [n for n in mol.n.values if n>0]
    masses = []        
    probs = []
    
    for e in elements:
        try:
            assert e in isotopes.index
            temp_masses = tuple(isotopes.loc[e].atomic_mass.values)
            masses.append(temp_masses)
            temp_probs = tuple(isotopes.loc[e].abundance.values)
            probs.append(temp_probs)
        except:
            raise ValueError('Element %s has no defined isotopes' % e)
            pass
    
    i = IsoSpecPy.IsoSpec(atoms,
                      masses,
                      probs,
                      args.proba)
    
    confs = i.getConfs()
    
    confs = pd.DataFrame(confs).transpose()
    confs.columns = ['mz', 'p', 'isotopologue']
    confs.p = confs.p.astype(np.float64).apply(np.exp)

    confs.mz = (confs.mz-m_electron)/args.z
    confs = confs.sort_values('mz')

    f = isotopes.loc[elements]
    iso_cols = [''.join([str(y),str(x)]) for (x,y) in zip(f.index, f.mass_number)]
    temp_df = pd.DataFrame.from_records(confs.isotopologue, columns=iso_cols)
    confs = pd.concat([confs[['mz', 'p']].reset_index(drop=True),
                       temp_df.reset_index(drop=True)],
                      axis=1,
                      )
    
    print(confs.head().to_string())
    
        
    spectrum = peak_shaper(confs[['mz', 'p']].values,
                           args.resolution,
                           delta_mz = args.delta_mz,
                           binsize = args.binsize,
                           no_points = args.points,
                           normalize = True,
                           process_binning = True)
    
    spectrum = pd.DataFrame(spectrum, columns=['mz', 'int'])
    
    confs.to_csv(os.path.join(args.output_folder,'centroids.csv'), index=False)
    spectrum.to_csv(os.path.join(args.output_folder,'spectrum.csv'), index=False)
    
if __name__=='__main__':
    main()
