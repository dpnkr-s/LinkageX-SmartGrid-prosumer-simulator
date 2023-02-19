# LinkageX Simulator

Co-simulation framework for simulating the interaction between the smart grid prosumers and self-sustainable communication network. It realistically simulates the interaction of the cellular networks within the smart grid system to analyze the impact of energy saving techniques on the overall performance and provides a virtual reality to test various technologies, regulations, decision making strategies, etc. ex-ante.

- [LinkageX Simulator](#linkagex-simulator)
    + [Development environment](#development-environment)
    + [Overview of simulation system](#overview-of-simulation-system)
    + [Identification and definition of main components](#identification-and-definition-of-main-components)
      - [Prosumers](#prosumers)
      - [Battery](#battery)
      - [Energy consumption](#energy-consumption)
      - [Renewable energy production](#renewable-energy-production)
      - [Price prediction](#price-prediction)
      - [Decision algorithm](#decision-algorithm)
      - [Smart grid system](#smart-grid-system)
    + [Communication network](#communication-network)
    + [Definition of district](#definition-of-district)
    + [Map representation](#map-representation)
    + [Energy savings in communication networks](#energy-savings-in-communication-networks)
    + [Final Remarks](#final-remarks)
      - [Authors](#authors)

### Development environment
MATLAB is used as a block in which we insert some data from prosumers (energy consumptions, prices etc). This block will perform some math operations in a pre-configured MATLAB package and generates an output that contains information about power consumptions and prices, with these outputs, prosumers can decide by itself whether to sell/buy energy to/from the grid.

All the operations involving power flow optimization and/or energy trading market are performed using MATLAB (*matpower package*) and rest of the objects and main simulator design is programmed in PYTHON. For example, prosumers are ‘python objects’, with some methods and parameters. Both of these languages are very powerful and are connected by using a reliable bridge developed by MATLAB.

All the data files are stored in JSON format which makes it easy for both MATLAB, PYTHON and human users to read and process the data. Data and traffic profiles are in CSV format.

<img width="420" alt="smart-grid-system" src="https://user-images.githubusercontent.com/25234772/219974289-4ee057c5-8ee7-4993-8124-2303338ce385.png">

### Overview of simulation system

From a simplistic representation of the system in the diagram below, it is to be noted that the system design contains multiple modules or components. These components and their interactions within the system are elaborated and described in detail in the following sub-sections.

<img width="520" alt="simplistic-flow-diagram" src="https://user-images.githubusercontent.com/25234772/219974677-f1d4dfc8-5309-4719-bd57-33c238a0ac13.png">

To quickly summarize the system functionality, prosumer is considered as an independent agent which receives values of its **energy consumption** and **renewable energy production**, also the past values of **traded energy with prices** to be used for **price prediction**. Using this information prosumer makes a decision about selling or buying energy, after checking its **battery storage** and current estimated prices. After making the decision, prosumer sends the values of power to be traded with offer/bid price to the **smart grid system** to perform power flow simulation and trade market simulation, which then outputs the result of each iteration.

### Identification and definition of main components 

#### Prosumers
Prosumers are one of the most important component of our system. Every prosumer in the system is connected to all the modules depicted in the previous figure, which are,
- Energy consumption
- Renewableenergy production
- Battery storage
- Price prediction and decision algorithm
- Smartgrid system

The scope of price prediction and decision making algorithm is limited to a single prosumer, this means that each prosumer will have its unique prediction model based on its own past data, not considering the global system data.

#### Battery
Battery component stores the energy at the command of prosumer associated with it. Prosumer decides to use energy from battery or from the grid, also when to charge the battery, after considering all the important factors like SoC, price difference between power generated and power load. Battery capacity is defined as different for each type of prosumer i.e. residential, office, base station, small commercial and large commercial.

#### Energy consumption
Energy consumed by each prosumer for the current simulation step is obtained by the simulator from power load profiles. Different load profiles are prepared for each type of prosumer describing the power consumption pattern of each type. Similar to battery capacity, each type of prosumer also has its different energy consumption profile. These profiles are obtained from U.S. department of energy (DOE) online portal and already consider daily variations in user activities and weather changes.

#### Renewable energy production
Power generated through renewable energy sources for current simulation step is obtained in a similar manner to energy consumption profiles. We are considering only solar energy in this project. Each prosumer type is associated with a solar panel of a specific size. The power output of each of these solar panels depends on the solar angle, radiation and weather conditions which are already accounted for in our profiles. 

The solar energy profiles are sourced from the same TMY3 station (city) as that of energy consumption profiles, this makes our simulation very realistic in terms of power demand and generation.

#### Price prediction
Electricity pricing models could lead to economic and environmental advantages as they provide consumers the possibility to reduce their electricity expenditures by reacting to pricing that changes during the day. Knowledge of estimated prices helps prosumers to implement efficient energy saving strategies. Tensorflow regression is used in this simulator. 

In the first phase the machine is trained using some inputs (like past electricity consumption trends) and the desired outputs (electricity prices for a given day). After having trained the machine, the current electricity consumptions is used as input for the neural network model to obtain the estimated prices which are used to make the best decisions related to electricity consumption.

<img width="420" alt="real-vs-predicted-prices " src="https://user-images.githubusercontent.com/25234772/219976123-1b502f5c-b3af-47e6-baf6-89b7e9b42884.png">

#### Decision algorithm
After the price prediction, the energy and price saving strategy is made by considering four values: **produced and demanded electricity, and real and predicted prices**. Firstly, the difference between the two electricity values is calculated, if the demand is greater then we have the possibility to either drop or use the battery depending on its level, also when the conditions are favourable we could buy extra electricity to charge the battery. On the other hand when demand is lower, we could sell or charge the battery, selling stored energy later when real prices are greater than the expected ones; but if that price is not greater and battery is full, the resting electricity must be sold at a safe price.

#### Smart grid system
Finally, the smart grid system is the most import component of our simulation system. It receives power and prices from each prosumer for current step then creates a case file describing current power grid scenario. Along with power grid scenario, a case file for market scenario is also generated. This market case file describes the power offered or demanded by prosumer at prices decided by each prosumer.

Smart grid system comprises PYTHON and MATLAB scripts. Grid and market case files are read by MATLAB, where matpower package is utilized to perform optimal power flow calculations and simulate market auctions using matpower’s proprietary modules. When MATLAB finishes its operations and modifies the same case files with the new results, smart grid system reads the case file again and updates the parameters on every prosumer and other components.

### Communication network

As we would like to observe the interaction between base transceiver stations with the smart grids, we start by defining the scenario. From the example scenario shown in the image below, there are two clusters of base transceiver stations or BSs, macro-BS control five micro-BSs in a master-slave fashion. Upper cluster (zone ‘Santa Rita’) has relatively denser population, thus, we have taken it as “business area”. The cluster below (zone ‘Mirafiori Nord’) instead taken as “residential area”. This way we are approaching the problem in a realistic way, by differentiating regions of high and low network traffic.

<img width="520" alt="comm-network-scenario" src="https://user-images.githubusercontent.com/25234772/219976689-11cb5b53-6dbf-4936-9aa2-b67987d868d9.png">

In our district definition when we mention a base station (BS), we mean macro-BS which controls precisely five micro-BSs, where macro-BSs are categorized into high traffic and low traffic BS. Thus BS is a special case of prosumer from simulator point of view. In this step, our aim was to develop a simple strategy to efficiently manage radio resources (*Resource on Demand*) by simply switching on/off and ignoring the losses during transitions. The following snippet of python code shows us how we have implemented the strategy:

```
traffic = traffic * 5

for i in range(len(traffic)):
  if 4.0 < traffic[i] < 5: no_micro = 4 
  elif 3.0 < traffic[i] < 4: no_micro = 3
  elif 2.0 < traffic[i] < 3: no_micro = 2 
  elif 1.0 < traffic[i] < 2: no_micro = 1
  elif traffic[i] < 1.0: no_micro = 0

load = traffic[i] / (no_micro + no_macro)

macro = no_macro *(ntrx_macro *(p0_macro + pmax_macro * deltaP_macro * load) / 2) self.energy[i] =macro+(no_micro*(ntrx_micro*(p0_micro+pmax_micro*deltaP_micro* load)/2)) self.power[i] = self.energy*2
```
Where the normalized load value is first multiplied by 5 to be considered as distributed among 5 base stations. Then according to the load, the number of micro BS are defined while the only macro base station is always kept working.

Examples of randomized load profiles used to simulate network traffic is shown in the image below.

<img width="520" alt="randomized-traffic-profiles" src="https://user-images.githubusercontent.com/25234772/219977066-1d636ff8-8395-44f6-b055-545947d1839b.png">

### Definition of district
A district in our context is defined as a set of different prosumers connected to the power grid. Firstly, a layout of power grid is created by defining the number of nodes present in the grid and declare if nodes are fixed generators, consumers and prosumers in the grid. Also, the distances and branch parameters between nodes are defined in this step.

Then, smart grid system reads the grid layout file and scans for position of nodes declared as prosumers. After obtaining the list of prosumer nodes, prosumer objects are created and associated with node. All types of prosumers including BSs can be associated in this way making a district. An example of a district is shown below.

<img width="420" alt="district-definition" src="https://user-images.githubusercontent.com/25234772/219977190-ba8d81d5-e9b4-4a6b-a985-672e7aa3f0bd.png">

### Map representation
A large number of prosumers and iterations can make it very difficult to display all results at one place in a concise and clear manner. Hence, we decided to utilize geographic coordinates of each node and represent the data using Google Maps API. Map is updated by report generated at each iteration. This way it becomes easier to notice the dynamics of the system and identify errors or outliers.

**BusID, Bus Type, power trade (in kWh) and prices** along with rest of the data are dumped and stored as a JSON log file, which can also be accessed and analyzed as per user’s requirements but the all data is not utilized in our case. Legends can be set accordingly, like in the representation below solid circles represent net power bought from the grid while tags represent net power sold to the grid. (yellow = 0-25 kWh, green = 25-50 kWh, red = 50-150 kWh)

<img width="520" alt="map-representation" src="https://user-images.githubusercontent.com/25234772/219977506-50ef6ad1-c19f-43d4-92eb-b4c146a35172.png">

### Energy savings in communication networks
Some positive results are obtained from energy saving or green network strategies implemented for communication network in LinkageX. Energy consumption graphs for each type of base station used in the test case scenario for a period of 24 hours or 48 steps of 30 minutes is shown in the following images.

#### Energy savings in 'residential area' Base Station on weekdays

<img width="550" alt="BS-energy-savings-residential" src="https://user-images.githubusercontent.com/25234772/219977796-106d9175-0871-476a-996d-40acc251550d.png">

- Daily energy consumption without strategy applied: **29.62 kWh** 
- Daily energy consumption with strategy applied: **22.598 kWh**  
- Daily energy savings: **7.02 kWh**

#### Energy savings in 'commercial area' Base Station on weekdays

<img width="550" alt="BS-energy-savings-in-commercial" src="https://user-images.githubusercontent.com/25234772/219977837-9f23a916-7731-4d74-adf3-8421f1449f6d.png">

- Daily energy consumption without strategy applied: **29.12 kWh** 
- Daily energy consumption with strategy applied: **21.92 kWh** 
- Daily energy savings: **7.19 kWh**

### Final Remarks
Key components involved in LinkageX co-simulation framework are identified and described above and the scenario for communication and definition of district is presented. The key features of the simulation system are,

- Agent-based simulation with prosumers as independent decision making agents
- Co-simulation with energy aware communication network
- Flexible and scalable district size and prosumer distribution
- Map representation for monitoring and debugging

Simulation system has been evaluated by monitoring its performance real-time, using map represenation and analyzing log files for a test case scenario. Positive results are obtained from communication network within our system, as base stations have been shown to save considerable amount of energy while using proposed energy saving strategy.

LinkageX is capable to analyze more complex scenarios with bigger districts. In future, complex decision making and trading algorithms can be implemented to have more realistic simulation. Also, due to its modular nature, the simulator can be used as a base to develop further co-simulation environments based on smart grids like blockchain based renewable energy trading platform.

#### Authors
Deepankar Sharma

Ani Dever
