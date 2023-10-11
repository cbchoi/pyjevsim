
from .definition import Infinite, SYSTEM_VERSION
from .executor import Executor
from abc import abstractmethod, abstractstaticmethod
import dill

#snapshot_manager.register_entity("PEx", SnapshotBehaviorExecutor.create_executor)

# SysExecutor 
# if snapshot_manager.get_snapshot_executor(bm.get_name()):
#   snapshot_manager.create_executor(be)
#      return executor_map[be.get_name()].create_executor(be)

class SnapshotBehaviorExecutor(Executor):
    #object가 생성 
    #등록시 fuction object를 부여
    @abstractstaticmethod
    def create_executor(cls, behavior_exeuctor):
        return SnapshotBehaviorExecutor(behavior_exeuctor) ##class create
    
    def __init__(
        self, behavior_executor 
    ):
        super().__init__(behavior_executor.get_create_time(), 
                         behavior_executor.get_destruct_time(), 
                         behavior_executor.get_engine_name()
                         )        
        self.behavior_executor = behavior_executor

    def get_core_model(self):
        return self.behavior_executor.get_core_model()

    def __str__(self):
        return "SNM" + self.behavior_executor.__str__()

    def get_name(self):
        return self.behavior_executor.get_name()

    def get_engine_name(self):
        return self.behavior_executor.get_engine_name()

    def set_engine_name(self, engine_name):
        self.behavior_executor.set_engine_name(engine_name)

    def get_create_time(self):
        return self.behavior_executor.get_create_time()

    def get_destruct_time(self):
        return self.behavior_executor.get_destruct_time()

    def get_obj_id(self):
        return self.behavior_executor.get_obj_id()

    # state management
    def get_cur_state(self):
        return self.behavior_executor.get_cur_state()

    def init_state(self, state):
        self.behavior_executor.init_state(state)

    # External Transition
    def ext_trans(self, port, msg):
        self.snapshot_pre_condition_ext(port, msg, self.get_cur_state())
        self.behavior_executor.ext_trans(port, msg)
        self.snapshot_post_condition_ext(port, msg, self.get_cur_state())

    # Internal Transition
    def int_trans(self):
        self.snapshot_pre_condition_int(self.get_cur_state())
        self.behavior_executor.int_trans()
        self.snapshot_post_condition_int(self.get_cur_state())

    # Output Function
    def output(self):
        self.snapshot_pre_condition_out(self.get_cur_state())
        out_msg = self.behavior_executor.output()
        self.snapshot_post_condition_out(self.get_cur_state(), out_msg)
        return out_msg
    

    # Time Advanced Function
    def time_advance(self):
        return self.behavior_executor.time_advance()
        
    def set_req_time(self, global_time):
        self.snapshot_time_condition(global_time)
        self.behavior_executor.set_req_time(global_time)
        
    def get_req_time(self):
        return self.behavior_executor.get_req_time()
    
    @abstractmethod
    def snapshot_time_condition(self, global_time):
        if int(global_time) % 2 == 1:
            self.snapshot(global_time)
    
    @abstractmethod
    def snapshot_pre_condition_ext(self, port, msg, cur_state):
        pass
    
    @abstractmethod
    def snapshot_post_condition_ext(self, port, msg, cur_state):
        pass
    
    @abstractmethod
    def snapshot_pre_condition_int(self, cur_state):
        pass
    
    @abstractmethod
    def snapshot_post_condition_int(self,cur_state):
        pass
    
    @abstractmethod
    def snapshot_pre_condition_out(self, cur_state):
        pass
    
    @abstractmethod
    def snapshot_post_condition_out(self, msg, cur_state):
        pass
    
    @abstractmethod
    def snapshot(self, name) :
        model_data = self.behavior_executor.get_core_model().model_snapshot(SYSTEM_VERSION)
            
        if model_data :
            with open(f"dump_test{name}.simx", "wb") as f :
                dill.dump(model_data, f)