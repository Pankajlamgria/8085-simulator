from simulator import *
from dict import *
class interpretor:
    def __init__(self):
        self.simulatorObj=processor_8085()

    def starting_address(self,add):
        self.simulatorObj.set_program_Counter(add)

    def decode_insert(self,instruction):
        mnemonics=instruction.split()[0]
        pc=self.simulatorObj.get_program_Counter()

        if(instruction in oppcode.keys()):
           self.simulatorObj.memory[pc]=int(oppcode[instruction],16)
           pc+=instruction_byte[mnemonics]
           self.simulatorObj.set_program_Counter(pc)
           return pc
        else:
            inst_arr=instruction.split()
            # DONE MVI
            if(inst_arr[0]=='MVI'):
                code=inst_arr[0]+" "+inst_arr[1]
                self.simulatorObj.memory[pc]=int(oppcode[code],16)
                pc+=1
                self.simulatorObj.memory[pc]=int(inst_arr[2],16)
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
                return pc
            

            elif(inst_arr[0]==''):
                pass






# TESTING AREA
obj=interpretor()
s="MVI A, 23"
obj.starting_address(4000)
print(obj.decode_insert(s))
