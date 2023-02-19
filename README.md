# LinkageX Simulator

Co-simulation framework for simulating the interaction between the smart grid prosumers and self-sustainable communication network.

### Development environment
MATLAB is used as a block in which we insert some data from prosumers (energy consumptions, prices etc). This block will perform some math operations in a pre-configured MATLAB package and generates an output that contains information about power consumptions and prices, with these outputs, prosumers can decide by itself whether to sell/buy energy to/from the grid.

All the operations involving power flow optimization and/or energy trading market are performed using MATLAB (*matpower package*) and rest of the objects and main simulator design is programmed in PYTHON. For example, prosumers are ‘python objects’, with some methods and parameters. Both of these languages are very powerful and are connected by using a reliable bridge developed by MATLAB.

All the data files are stored in JSON format which makes it easy for both MATLAB, PYTHON and human users to read and process the data. Data and traffic profiles are in CSV format.

![This is an image](https://github.com/dpnkr-s/SmartGrid-Prosumer-simulator/blob/main/images/smart%20grid%20system.png)

### Overview of simulation system

