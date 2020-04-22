#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:12:46 2020

@author: kantundpeterpan
"""
import numpy as np
from scipy.stats import norm

def binning(mzs,
            binsize,
           ):

    min_mz = np.min(mzs[:,0])
    max_mz = np.max(mzs[:,0])
    
    delta = max_mz-min_mz
    
    bins = np.linspace(min_mz, max_mz, num = int(delta//binsize))
    
    spectrum = np.empty((len(bins),2))
    spectrum[:,0] = bins+binsize/2
    spectrum[:,1] = np.zeros(len(bins))
    
    chunked = np.array_split(mzs, indices_or_sections=1)
    
    for div in chunked:
        
        mz_s = div[:,0]
        counts = div[:,1]

        ind_mz_indices = np.digitize(mz_s, bins)
        
        populated_bins = np.unique(ind_mz_indices)
        
        ind_mz_indices-=1
        populated_bins-=1
        
        temp_spectrum = np.empty((len(bins),2))
        temp_spectrum[:,0] = bins
        temp_spectrum[:,1] = np.zeros(len(bins))
        
        for bin_no in populated_bins:

            mz = bins[bin_no]+binsize/2
            ind = (ind_mz_indices == bin_no)

            temp_sum_counts = np.sum(counts[ind])
            temp_spectrum[bin_no][1] = temp_sum_counts
            
            temp_spectrum[:,0] = bins+binsize/2
        
        spectrum[:,1]+=temp_spectrum[:,1]

    return spectrum

def peak_shaper(centroid_spectrum, resolution,
                delta_mz = 0.05, no_points = 250,
                normalize = False,
                process_binning=False, binsize = 0.005):
    
    centroids = centroid_spectrum[:,0]
    probs = centroid_spectrum[:,1]
    
    new_mzs = []
    new_probs = []
    
    for c,p in zip(centroids, probs):
        #setting peakwidth
        sigma = c/(resolution*2.355)
        #range for gaussian curve
        temp_new_mzs = np.arange(c-delta_mz, c+delta_mz, delta_mz/(0.5*no_points))
        #getting gaussian curve with mean=m/z-centroid and sigma as calculated from fwhm, scaled by centroid prob
        temp_new_probs = norm(c,sigma).pdf(temp_new_mzs)*p

        #appending new data to respective lists
        new_mzs.append(temp_new_mzs)
        new_probs.append(temp_new_probs)
        
    #casting numpy arrays from lists
    new_mzs = np.hstack(new_mzs)
    new_probs = np.hstack(new_probs)
    
    #indices for sorting by m/z
    ind = np.argsort(new_mzs)
    
    #resorting numpy arrays
    new_mzs = new_mzs[ind]
    new_probs = new_probs[ind]
    
    #merging m/z and intensities to one array
    new_spectrum = np.array([new_mzs, new_probs]).transpose()
        
    if process_binning:
        new_spectrum = binning(new_spectrum, binsize) #uses non compiled version => probably slow?!
        new_spectrum = new_spectrum[np.nonzero(new_spectrum[:,1])]
        
    if normalize:
        new_spectrum[:,1] = new_spectrum[:,1]/np.max(new_spectrum[:,1])
        
    return new_spectrum
