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
            

            elif(inst_arr[0]=='ADI' or inst_arr[0]=='ANI'):
                self.simulatorObj.memory[pc]=int(oppcode[inst_arr[0]],16)
                pc+=1
                self.simulatorObj.memory[pc]=int(inst_arr[1],16)
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
                return pc

            elif(inst_arr[0]=='JC' or inst_arr[0]=='JM'or inst_arr[0]=='JMP'or inst_arr[0]=='JNC'or inst_arr[0]=='JNZ' or inst_arr[0]=='JP' or inst_arr[0]=='JPE' or inst_arr[0]=='JPO' or inst_arr[0]=='JZ' or inst_arr[0]=='LDA' or inst_arr[0]=='LHLD' or inst_arr[0]=='LDA'):
                self.simulatorObj.memory[pc]=int(oppcode[inst_arr[0]],16)
                pc+=1
                self.simulatorObj.to_insert_hexaDecimal_Memory(pc,int(inst_arr[1],16))
                pc+=2
                self.simulatorObj.set_program_Counter(pc)
                return pc
            # LOADING IMEDIATE 16BIT VALUE IN REGISTER PAIR 
            elif(inst_arr[0]=='LXI'):
                code=inst_arr[0]+' '+inst_arr[1]
                self.simulatorObj.memory[pc]=int(oppcode[code],16)
                pc+=1
                self.simulatorObj.to_insert_hexaDecimal_Memory(pc,int(inst_arr[2]))
                pc+=2
                self.simulatorObj.set_program_Counter(pc)
                return pc
            elif(inst_arr[0]=='SHLD' or inst_arr[0]=='STA'):
                self.simulatorObj.memory[pc]=int(oppcode[inst_arr[0]],16)
                pc+=1
                self.simulatorObj.to_insert_hexaDecimal_Memory(pc,int(inst_arr[1]))
                pc+=2
                self.simulatorObj.set_program_Counter(pc)
                return pc
            elif(inst_arr[0]=='SUI'):
                self.simulatorObj.memory[pc]=int(oppcode[inst_arr[0]],16)
                pc+=1
                self.simulatorObj.memory[pc]=int(inst_arr[1],16)
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
                return pc
    def isMOV(self,data):
        data=data.upper()
        instruction=swapped_opcode[data]
        instruction=instruction.split()
        if(instruction[0]=='MOV'):
            return True
        return False

    # For MOV Command
    def executeMOV(self,int_Code):
        binNumber=str(bin(int_Code)[2:])
        source=binNumber[-3::1]
        destination=binNumber[-6:-3:1]
        sourceReg,desReg=register[source],register[destination]
        if(sourceReg=='M' or desReg=='M'):
            if(sourceReg=='M'):
                sourceAdd=self.simulatorObj.get_Register_Pair('H')
                self.simulatorObj.register[register_index[desReg]]=self.simulatorObj.memory[sourceAdd]
            else:
                desAdd=self.simulatorObj.get_Register_Pair('H')
                self.simulatorObj.memory[desAdd]=self.simulatorObj.register[register_index[sourceReg]]
        else:    
            self.simulatorObj.register[register_index[desReg]]=self.simulatorObj.register[register_index[sourceReg]]


    #RUNNING THE CODE 
    def execute_Code(self):
        pc=self.simulatorObj.get_program_Counter()
        while(self.simulatorObj.memory[pc]!=int("76",16) and self.simulatorObj.memory[pc+1]!=0):
            hexaData=hex(self.simulatorObj.memory[pc])[2:]
            if(self.isMOV(hexaData)):
                self.executeMOV(self.simulatorObj.memory[pc],)
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            # elif(self.is)








# TESTING AREA
# obj=interpretor()
# obj.simulatorObj.register[register_index['A']]=34
# obj.simulatorObj.set_Register_Pair('H','2000')
# obj.simulatorObj.memory[int("2000",16)]=250
# s=["MOV C, A",'MOV B, C',"MOV B, M",'HLT']
# obj.starting_address(4000)

# for i in s:
#     (obj.decode_insert(i))
# obj.starting_address(4000)
# print("running code")
# obj.execute_Code()
# print(obj.simulatorObj.register[register_index['A']])
# print(obj.simulatorObj.register[register_index['C']])
# print(obj.simulatorObj.register[register_index['B']])
# print(obj.simulatorObj.memory[int("2000",16)])
# print(obj.simulatorObj.register[register_index['B']])
