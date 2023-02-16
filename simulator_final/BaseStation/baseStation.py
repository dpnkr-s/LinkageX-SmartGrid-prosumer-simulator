#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import scipy.io as scio
import numpy as np
import matplotlib.pyplot as plt

def main(args):
	plt.plot(strategy(com))
	plt.plot(strategy(res))
	plt.plot(strategy(com_end))
	plt.plot(strategy(res_end))
	plt.show()
	return 0
	
def strategy(period):
	no_Macro=1
	Ntrx_Macro=6 
	Ntrx_Micro=2
	P0_Macro=20 
	P0_Micro=6.3
	Pmax_Macro=84
	Pmax_Micro=56
	deltaP_Macro=4.7
	deltaP_Micro=2.6
	energy = np.empty(np.shape(period))
	power = np.empty(np.shape(period))
	for i in range(len(period)) :
		if 0.8<com[i]<1.0 :
			no_Micro = 4 
		elif 0.6<com[i]<0.8 :
			no_Micro = 3
		elif 0.4<com[i]<0.6:
			no_Micro = 2
		elif 0.2<com[i]<0.4:
			no_Micro = 1
		elif com[i]<0.2:
			no_Micro = 0				
		Macro = no_Macro*(period[i]*(P0_Macro+Pmax_Macro*deltaP_Macro*period[i]))/2    
		energy[i] = Macro+no_Micro*(period[i]*(P0_Micro+Pmax_Micro*deltaP_Micro*period[i]))/2
		power[i] = energy[i]*2
	return power

if __name__ == '__main__':
	mat_file=scio.loadmat('normalizedtraffic.mat')
	data = mat_file.get('normalizedtraffic')
	com = data[:,0] # 24h weekday traffic for commercial area BS
	com_end = data[:,1] # 24h weekend traffic for commercial area BS
	res = data[:,2] # 24h weekday traffic for residential area BS
	res_end = data[:,3] # 24h weekend traffic for residential area BS
	sys.exit(main(sys.argv))
