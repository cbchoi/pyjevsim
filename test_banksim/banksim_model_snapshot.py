"""
Author: Changbeom Choi (@cbchoi)
Copyright (c) 2014-2020 Handong Global University
Copyright (c) 2021-2024 Hanbat National University
License: MIT.  The full license text is available at:
https://github.com/eventsim/pyjevsim/blob/main/LICENSE

Example of snapshot a BankGenerator model during a Bank Simulation run.

The User Generator Model generates a Bank User periodically.
The Bank Accountatnt handles the Bank User's operations,
Bank Queue stores the Bank User's data and passes the Bank User's information to the Bank Accountant when no Bank Accountant is available. 

Usage:
In a terminal in the parent directory, run the following command.

   pytest -s ./test_banksim/banksim_model_snapshot.py 
"""
import time

from pyjevsim.definition import *
from pyjevsim.system_executor import SysExecutor

from pyjevsim.snapshot_condition import SnapshotCondition
from pyjevsim.snapshot_manager import SnapshotManager

from .model_accountant import BankAccountant
from .model_queue import BankQueue
from .model_user_gen import BankUserGenerator

class BankGenModelCondition(SnapshotCondition) :
    @staticmethod
    def create_executor(behavior_executor) :
        return BankGenModelCondition(behavior_executor)
    
    def __init__(self, behavior_executor):
        super().__init__(behavior_executor) #set behavior_executor
        self.check = True
        
    def snapshot_time_condition(self, global_time):
        #if global time >= 50000 : snapshot model
        if global_time >= 10000 and self.check:
            self.check = False
            return True

def execute_simulation(t_resol=1, execution_mode=ExecutionType.V_TIME):
    snapshot_manager = SnapshotManager()
    ss = SysExecutor(t_resol, ex_mode=execution_mode, snapshot_manager=snapshot_manager)
    
    gen_num = 10            #Number of BankUserGenerators 
    queue_size = 100        #BankQueue size
    proc_num = 30           #Number of BankAccountant
    
    user_process_time = 5   #BankUser's processing speed
    gen_cycle = 2           #BankUser Generattion cycle
    max_user = 500000       #Total number of users generated
    
    max_simtime = 50001    #simulation time
           
    
    ## model set & register entity
    gen_list = []
    user = int(max_user / gen_num)
    for i in range(gen_num) :
        if i == gen_num-1:
            user += max_user % gen_num
        gen = BankUserGenerator(f'gen{i}', gen_cycle, user, user_process_time)
        gen_list.append(gen)    
        
        #Associating snapshot conditions with models 
        snapshot_manager.register_snapshot_condition(f"gen{i}", BankGenModelCondition.create_executor)
        ss.register_entity(gen)    
        
        
    que = BankQueue('Queue', queue_size, proc_num)
    ss.register_entity(que)
    
    
    account_list = []
    for i in range(proc_num) :
        account = BankAccountant(f'processor{i}', i)
        account_list.append(account)
        ss.register_entity(account)
        
    
    ## Model Relation
    ss.insert_input_port('start')

    for gen in gen_list : 
        ss.coupling_relation(None, 'start', gen, 'start')
        ss.coupling_relation(gen, 'user_out', que, 'user_in')
    for i in range(proc_num) : 
        ss.coupling_relation(que, f'proc{i}', account_list[i], 'in')
        ss.coupling_relation(account_list[i], 'next', que, 'proc_checked')
        
    ss.insert_external_event('start', None)

    ## simulation run
    for i in range(max_simtime):
        print("[time] : ", i)
        ss.simulate(1)
    
start_time = time.time()
execute_simulation(1, ExecutionType.V_TIME)
end_time = time.time()
execution_time = end_time - start_time
print(f"run time: {execution_time} sec")
    