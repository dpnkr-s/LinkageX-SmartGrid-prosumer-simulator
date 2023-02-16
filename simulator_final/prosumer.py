# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 18:49:51 2017

@author: lenovo
"""
from battery import battery
import numpy as np

class Prosumer(object):
    
    def __init__(self, bus_id=0, bus_type=0, bus_watts=0, bus_price=0, capacity=4800.0, soc=0.2): #SET VALUES FOR ID,TYPE,WATTS,PRICE,BATTERY ...
        #Attributes related to bus on the grid
        self.bus_id = bus_id # bus id on power grid
        self.bus_type = bus_type # to identify type of prosumer i.e residential, office etc
        self.bus_watts = bus_watts
        self.bus_price = bus_price
        #ATtributes related to battery
        self.capacity = capacity # battery capacity
        self.soc = soc  # battery soc
        
        self.p_gen = 0 # generated power
        self.p_load = 0 # power load
        
        
    def step(self):
        self.soc, self.bus_watts = battery(self.soc, self.capacity, self.p_gen, self.p_load)
        
#DEF VARIABLES
	def get_id(self):
		return self.bus_id
	
	def get_type(self):
		return self.bus_type
        
	def get_watts(self):
		return self.bus_watts
        
	def get_price(self):
		return self.bus_price
  
#SET VARIABLES
	def set_type(self,bus_type):
		self.bus_type=bus_type
		
	def set_watts(self,bus_watts):
		self.bus_watts=bus_watts
		
	def set_price(self,bus_price):
		self.bus_price=bus_price	


class prosumer_sim(object):
    def __init__(self):
        self.agents = []
        self.data = []

    # add a list in bus id to add multiple agents
    def add_agents(self, bus_id = [], bus_type = []):
        for idx in range(0, len(bus_id)):
            if bus_type[idx] == 0: # battery capacity for residential
                bat_cap = 4800.0 
            elif bus_type[idx] == 1: # battery capacity for office
                bat_cap = 38400.
            elif bus_type[idx] == 2: # battery capacity for office
                bat_cap = 38400.0
            elif bus_type[idx] == 3: # battery capacity for large commercial
                bat_cap = 192000.0
            elif bus_type[idx] == 4: # battery capacity for small commercial
                bat_cap = 9600.0
            agent = Prosumer(bus_id=bus_id[idx], bus_type=bus_type[idx], capacity=bat_cap)
            self.agents.append(agent)
            
            
    def profile_load(self, p_gen, p_load, dev_gen, dev_load, bus_type):
        p_gen = float(p_gen)
        p_load = float(p_load)
        dev_gen = float(dev_gen)/2
        dev_load = float(dev_load)/2
        n_gen = len(self.agents)
        for idx in range(0, n_gen):
            if self.agents[idx].bus_type == bus_type:  
                if (dev_gen == 0):
                    self.agents[idx].p_gen = p_gen
                else:
                    var1 = p_gen + np.random.normal(0,dev_gen,1)
                    if (var1 >= 340000): #max gen limit
                        self.agents[idx].p_gen = 340000
                    else:
                        self.agents[idx].p_gen = var1    
            
                var2 = p_load + np.random.normal(0,dev_load,1)
                if (var2 >= 0.0):
                    self.agents[idx].p_load = 1000*var2 #convert kW to W

    def step_agents(self):
        for idx in range(0,len(self.agents)):
            self.agents[idx].step()

                        
        