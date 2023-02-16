function out = mat_fun()
    % loading case data 
    mkt = loadjson('mkt_case.json');
    mpc = loadjson('loadcase.json'); %use 'loadcase_init.json' if running directly from matlab
    
    % If offers and bids are specified by prosumer
    %P1 = loadjson('mkt_bids.json');
    %offers = P1.o; bids = P1.b;
    
    % If offers and bids are calculated by off2case.m
    of_idx = find(mpc.gen(:,2)>0);
    bi_idx = find(mpc.gen(:,2)<=0);
    [q,p] = case2off(mpc.gen,mpc.gencost);
    offers.P.prc = p(of_idx,:); offers.P.qty = q(of_idx,:);
    bids.P.prc = p(bi_idx,:); bids.P.qty = q(bi_idx,:);
    
    % running smart market optimal power flow
    [mpc_out, co, cb, f, dispatch, success, et] = runmarket(mpc, offers, bids, mkt);

    data.version = mpc_out.version;
    data.baseMVA = mpc_out.baseMVA;
    data.bus = mpc_out.bus;
    data.gen = mpc_out.gen;
    data.branch = mpc_out.branch;
    data.areas = mpc_out.areas;
    data.gencost = mpc_out.gencost;

    P2.o = co; P2.b = cb;
    % saving data back in json file
    savejson('',P2,'mkt_results.json');
    savejson('',data,'loadcase.json');
    % return the final value of optimization cost function
    out = f;