clear all     
clc
fprintf('Start\n')

%save('loadgenprofiles.mat', 'loadgenprofiles')
load('loadgenprofiles.mat')
data = loadgenprofiles;

%Initial values
SOCmax = 0.9;
SOCmin = 0.1;
SOC1 = 0.5;
efficiency = 1;%0.9;
PnomBat = 500;%1000; %[W] => soc1 must have equivalent to PnomBat
EnomBat = 1000; %[W/h]
time = linspace(0, 1440, 96); %every 15 minutes during 24 hours
delta_time = 0.25; %15 minutes
Pnet = data(:,1) - data(:,2);%NET_consumption = load - gen
i = 1;

while i < 97
    flag = 0; %To skip step 3 and 4
    fprintf('Iterarion: %d\n', i)
    %SOC1
    %Working mode
    if Pnet(i) > 0
        mode = 1; %Discharging
        fprintf ('Discharging\n')
    else
        mode = 0; %Charging
        fprintf ('Charging\n')
    end

    %1
    if Pnet(i) < PnomBat
        p1 = Pnet(i);
    %elseif Pnet(i) > PnomBat
    else
        p1 = PnomBat;
    end

    %2 If program enters to this loop, go to the next iteration
    if (SOC1 > SOCmax && mode == 0) || (SOC1 < SOCmin && mode == 1)
        p2 = 0;
        SOC2 = SOC1;
        flag = 1;
    end

    if flag == 0
    %3
        if mode == 1 %Discharging
            SOC2 = SOC1 - abs(p1) / efficiency * delta_time / EnomBat;
            PnomBat = PnomBat - abs((data(i,1) - data(i,2))) / 4;
        elseif mode == 0 %Charging   
            SOC2 = SOC1 + abs(p1) * efficiency * delta_time / EnomBat;
            PnomBat = PnomBat + abs((data(i,1) - data(i,2))) / 4;
        end
    
    %4
        if SOC2 > SOCmax
            SOC2 = SOCmax;
            PnomBat = 0.9 * 1000;
            %p2 = p1;
        end
        
        if SOC2 < SOCmin
            SOC2 = SOCmin;
            PnomBat = 0.1 * 1000;
            %p2 = p1;
        end
        p2 = p1;
        
    end
    
    SOC1 = SOC2;
    PnomBat;
    p2;
    level(i) = SOC1;
    fprintf('SOC1 = %.3f; PnomBat = %.3f; p2 = %.3f\n', SOC1,PnomBat,p2)
    fprintf('--------------------------------------------------------\n')
    %PnomBat = PnomBat - data(i,1) / 4;
    out_bat(i) = p2;
    i = i + 1;
    
end
plot(time, level)    
figure 
plot(time, Pnet) %NET_consumption
figure
plot(time, data(:,1)) %Load
figure
plot(time, data(:,2)) %Generation

%Output of the battery
figure
plot(time, out_bat)

fprintf('End\n')