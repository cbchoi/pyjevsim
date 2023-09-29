from system_executor import SysExecutor
from system_message import SysMessage
from definition import *
import datetime
from behavior_model import BehaviorModel
from behavior_model_executor import BehaviorModelExecutor

class PEG(BehaviorModel):
    def __init__(self, name):
        BehaviorModel.__init__(self, name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate", 1)

        self.insert_input_port("start")
        self.insert_output_port("process")
    
    def ext_trans(self,port, msg):
        if port == "start":
            print(f"[Gen][IN]: {datetime.datetime.now()}")
            self._cur_state = "Generate"

    def output(self):
        msg = SysMessage(self.get_name(), "process")
        msg.insert(f"[Gen][OUT]: {datetime.datetime.now()}")
        return msg
        
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"


class MsgRecv (BehaviorModel):
    def __init__(self, name):
        BehaviorModel.__init__(self, name)

        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_input_port("recv")

    def ext_trans(self,port, msg):
        if port == "recv":
            print(f"[MsgRecv][IN]: {datetime.datetime.now()}")
            data = msg.retrieve()
            print(data[0])
            self._cur_state = "Wait"

    def output(self):
        return None
        
    def int_trans(self):
        if self._cur_state == "Wait":
            self._cur_state = "Wait"

# System Simulator Initialization
ss = SysExecutor(1, _sim_mode="REAL_TIME")
#ss.register_engine("first", "REAL_TIME", 1)
ss.insert_input_port("start")
gen = PEG("Gen")
ss.register_entity(gen)

proc = MsgRecv("Proc")
ss.register_entity(proc)

ss.coupling_relation(None, "start", gen, "start")
ss.coupling_relation(gen, "process", proc, "recv")
ss.insert_external_event("start", None)
ss.simulate()