# -*- coding: utf-8 -*-

# importing libraries and scripts
import matlab.engine
import pandas as pd
import numpy as np
import json
from battery import battery
from prosumer import *

# starting matlab engine
eng = matlab.engine.start_matlab()

# reading json containing statistical data (standard deviation for each hour)
my_data = json.loads(open("stat.json").read())
dev_gen0 = np.asarray(my_data['dev_gen0'])
dev_load0 = np.asarray(my_data['dev_load0'])
dev_gen1 = np.asarray(my_data['dev_gen1'])
dev_load1 = np.asarray(my_data['dev_load1'])
#dev_gen2 = np.asarray(my_data['dev_gen2'])
#dev_load2 = np.asarray(my_data['dev_load2'])
dev_gen3 = np.asarray(my_data['dev_gen3'])
dev_load3 = np.asarray(my_data['dev_load3'])
dev_gen4 = np.asarray(my_data['dev_gen4'])
dev_load4 = np.asarray(my_data['dev_load4'])

# reading initial loadcase for powerflow simulation
loadcase = json.loads(open("loadcase_init.json").read())
bus = np.asarray(loadcase['bus'])
gen = np.asarray(loadcase['gen'])
fix_gen = gen[0] #first generator in gen is always fixed generator
gen_template_sell = gen[1] # gen vector template for selling power
gen_template_buy = gen[6]  # gen vector template for buying power

# same for generator cost vectors
gencost = np.asarray(loadcase['gencost'])
gencost_sell = gencost[0]
gencost_buy = gencost[8]

# extracting bus_ids of variable loads from initial loadcase
# although, in our case there are no fixed loads
bus_id = []
end = len(bus[:,1])
for i in range(0,end): 
    if (bus[i,1] == 2):
        bus_id.append(int(bus[i,0]))

# defining bus types to load different profiles and startegies for prosumers
# having different types of prosumers in our simulation allows us to analyse
# different trading dynamics of system
#
# type 0 -- residential prosumer
# type 1 -- medium office prosumer
# type 2 -- base station prosumer
# type 3 -- large commercial prosumer
# type 4 -- small commercial prosumer 

# as of now theres no data for type 2 hence its omitted
bus_type = [4,0,0,4,0,0,1,0,0,0,4,3,4,0,0,1,4,0,0,0,4,0,1,0,0,0,1,0,0]
buy_id = []
sell_id = []        

if __name__ == '__main__':
        
        sim = prosumer_sim()

        n_age = 10 #number of agents (optional)
        n_days = 1 #number of simulation days
        n_steps = 24 #there are 24, 1 hour simulation steps each day
        
        df0 = pd.read_csv('residential.csv', sep=',')
        df1 = pd.read_csv('medium_office.csv', sep=',')
        #df2 = pd.read_csv('base_station.csv', sep=',')
        df4 = pd.read_csv('small_commercial.csv', sep=',')
        df3 = pd.read_csv('large_commercial.csv', sep=',')
        end_idx = len(df0)
        
        sim.add_agents(bus_id, bus_type)
        
        time = 0
        for j in range(0,n_days):
            for hour in range(0,n_steps):
                
                if (time == 0):
                    msg = 'lazy coding'
                else:
                    loadcase = json.loads(open("loadcase.json").read())
                    bus = np.asarray(loadcase['bus'])
                    gencost = np.asarray(loadcase['gencost'])
                
                # Getting price data after the auction is ended
                mkt_result = json.loads(open("mkt_results.json").read())
                bP = mkt_result['b']
                oP = mkt_result['o']
                bP = bP['P']
                oP = oP['P']
                cleared_buyP = np.asarray(bP['prc'])
                
                shb = cleared_buyP.shape
                
                if (len(shb) == 1):  #To find avg prices over 3 blocks
                    mn = np.mean(cleared_buyP)
                    cleared_buyP = []
                    cleared_buyP.append(mn)
                elif (len(shb) == 0):
                    cleared_buyP = [0, 0, 0]
                else:
                    cleared_buyP = np.mean(cleared_buyP,1)
                    
                cleared_sellP = np.asarray(oP['prc'])
                shs = cleared_sellP.shape
                if (len(shs) == 1):
                    mn = np.mean(cleared_sellP)
                    cleared_sellP = []
                    cleared_sellP.append(mn)
                else:
                    cleared_sellP = np.array(np.mean(cleared_sellP,1))
                    
                # sim.price_update(cleared_sellP, cleared_buyP, buy_id, sell_id)
                for j in range(0,len(buy_id)):
                    sim.agents[buy_id[j]].bus_price = -1*cleared_buyP[j]
                for j in range(0,len(sell_id)):
                    sim.agents[sell_id[j]].bus_price = cleared_sellP[j]
                    
                # loading profiles on prosumer objects    
                sim.profile_load(df0.AC_out[time], df0.Electricity[time], dev_gen0[hour], dev_load0[hour],0)
                sim.profile_load(df1.AC_out[time], df1.Electricity[time], dev_gen1[hour], dev_load1[hour],1)
                #sim.profile_load(df2.AC_out[time], df2.Electricity[time], dev_gen2[hour], dev_load2[hour],2)
                sim.profile_load(df3.AC_out[time], df3.Electricity[time], dev_gen3[hour], dev_load3[hour],3)
                sim.profile_load(df4.AC_out[time], df4.Electricity[time], dev_gen4[hour], dev_load4[hour],4)
                
                sim.step_agents()
                
                buy_id = []
                sell_id = []
                gen = fix_gen
                gencost = gencost_sell
                for idx in range(0,len(sim.agents)):
                    b_id = sim.agents[idx].bus_id
                    b_w = sim.agents[idx].bus_watts
                    if (b_w < 0): #buy
                        bus[b_id-1,2] = 0 #not demanding power from grid but only from prosumers
                        bus[b_id-1,3] = 0
                        gen_template_buy[0] = b_id
                        gen_template_buy[1] = b_w*0.001 #in kW
                        gen_template_buy[2] = 0
                        gen = np.vstack((gen,gen_template_buy))
                        gencost = np.vstack((gencost,gencost_buy))
                        buy_id.append(idx)
                    else: #sell
                        bus[b_id-1,2] = 0
                        bus[b_id-1,3] = 0
                        gen_template_sell[0] = b_id
                        gen_template_sell[1] = b_w*0.001
                        gen_template_sell[2] = 0
                        gen = np.vstack((gen,gen_template_sell))
                        gencost = np.vstack((gencost,gencost_sell))
                        sell_id.append(idx)
                        
                busL = bus.tolist()
                genL = gen.tolist()
                gencL = gencost.tolist()
                dat = {u'version':loadcase['version'], u'baseMVA':loadcase['baseMVA'],
                       u'bus':busL, u'gen':genL, u'branch':loadcase['branch'],
                       u'areas':loadcase['areas'], u'gencost':gencL}
                    
                with open('loadcase.json', 'w') as file:
                    json.dump(dat, file, indent=2)
                    
                # now json file is updated so it can be used by matpower
                gg = eng.mat_fun()
                print gg
                time = time+1
        
        # At this stage Output power to be bought or sold on grid
        # is updated in agents for given hour
        # Now data will go into Matlab for price market and powergrid simulation 
        for i in range(0,len(sim.agents)):
            print sim.agents[i].bus_watts
            print sim.agents[i].bus_price
            print time