from simulator import *
from dict import *
class interpretor:
    def __init__(self):
        self.simulatorObj=processor_8085()

    def starting_address(self,add):
        self.simulatorObj.set_program_Counter(add)

    def decode_insert(self,instruction):
        instruction=instruction.upper()
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
                value=int(inst_arr[2],16)
                if(value<0):
                    value=self.twos_comp(value,8)
                value%=(2**8)
                self.simulatorObj.memory[pc]=value
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
            elif(inst_arr[0]=='SBI' or inst_arr[0]=='XRI'):
                self.simulatorObj.memory[pc]=int(oppcode[inst_arr[0]],16)
                pc+=1
                self.simulatorObj.memory[pc]=int(inst_arr[1],16)
                pc+=1
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
    def find_Command(self,data):
        data=data.zfill(2)
        instruction=swapped_opcode[data]
        instruction=instruction.split()
        return instruction[0]
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
    
    def addFunc(self,a,b):
        # data is integer
        lower_nibble1,lower_nibble2=a&15,b&15
        upper_nibble1,upper_nibble2=a>>4,b>>4
        lower_res=lower_nibble1+lower_nibble2
        carry=0
        if(lower_res/16>=1):
            self.simulatorObj.status.set_bit(status_index['AC'])
            lower_res%=16
            carry=1
        else:
            self.simulatorObj.status.clear_bit(status_index['AC'])
        upper_res=upper_nibble1+upper_nibble2+carry
        if(upper_res/16>=1):
            self.simulatorObj.status.set_bit(status_index['C'])
            upper_res%=16
        else:
            self.simulatorObj.status.clear_bit(status_index['C'])
        
        if(upper_res&1<<3==8):
            self.simulatorObj.status.set_bit(status_index['S'])
        else:
            self.simulatorObj.status.clear_bit(status_index['S'])
        
        lowerHex=hex(lower_res)[2:]
        upperHex=hex(upper_res)[2:]
        res=upperHex+lowerHex
        res=res.upper()
        res=int(res,16)
        if(res==0):
            self.simulatorObj.status.set_bit(status_index['Z'])
        else:
            self.simulatorObj.status.clear_bit(status_index['Z'])
        binNumber=str(bin(res)[2:])
        oneCount=0
        for i in binNumber:
            if(i=='1'):
                oneCount+=1


        if(oneCount%2==0):
            self.simulatorObj.status.set_bit(status_index['P'])
        else:
            self.simulatorObj.status.clear_bit(status_index['P'])
        
        return res
    
    # ADDITION WITH CARRY
    def executeADC(self,int_Code):
        binNumber=str(bin(int_Code)[2:])
        regCode=binNumber[-3::1]
        regCode=register[regCode]
        if(regCode=='M'):
            add=self.simulatorObj.get_Register_Pair('H')
            reg_val=self.simulatorObj.memory[add]
            if(self.simulatorObj.status.get_bit(status_index['C'])):
                reg_val+=1
            acc_val=self.simulatorObj.register[register_index['A']]
            res=self.addFunc(acc_val,reg_val)
            self.simulatorObj.register[register_index['A']]=res

        else:
            reg_val=self.simulatorObj.register[register_index[regCode]]
            if(self.simulatorObj.status.get_bit(status_index['C'])):
                reg_val+=1
            acc_val=self.simulatorObj.register[register_index['A']]
            res=self.addFunc(acc_val,reg_val)
            self.simulatorObj.register[register_index['A']]=res
    # ADDITION
    def executeADD(self,int_Code):
        binNumber=str(bin(int_Code)[2:])
        regCode=binNumber[-3::1]
        regCode=register[regCode]
        if(regCode=='M'):
            add=self.simulatorObj.get_Register_Pair('H')
            reg_val=self.simulatorObj.memory[add]
            acc_val=self.simulatorObj.register[register_index['A']]
            res=self.addFunc(acc_val,reg_val)
            self.simulatorObj.register[register_index['A']]=res

        else:
            reg_val=self.simulatorObj.register[register_index[regCode]]
            acc_val=self.simulatorObj.register[register_index['A']]
            res=self.addFunc(acc_val,reg_val)
            self.simulatorObj.register[register_index['A']]=res

    def handleUpdateStatus(self,data):
        binNumber=str(bin(data)[2:])
        self.simulatorObj.status.clear_bit(status_index['AC'])
        self.simulatorObj.status.clear_bit(status_index['C'])
        oneCount=0
        for i in binNumber:
            if(i=='1'):
                oneCount+=1
        if(oneCount%2==0):
            self.simulatorObj.status.set_bit(status_index['P'])
        else:
            self.simulatorObj.status.clear_bit(status_index['P'])
        if(data==0):
            self.simulatorObj.status.set_bit(status_index['Z'])
        else:
            self.simulatorObj.status.clear_bit(status_index['Z'])
        if(data&1<<7==1<<7):
            self.simulatorObj.status.set_bit(status_index['S'])
        else:
            self.simulatorObj.status.clear_bit(status_index['S'])
            
    # BITWISE AND
    def executeANA(self,int_Code):
        binNumber=str(bin(int_Code)[2:])
        regCode=binNumber[-3::1]
        regCode=register[regCode]
        if(regCode=='M'):
            add=self.simulatorObj.get_Register_Pair('H')
            reg_val=self.simulatorObj.memory[add]
            self.simulatorObj.register[register_index['A']]&=reg_val
            self.handleUpdateStatus(self.simulatorObj.register[register_index['A']])
        else:
            reg_val=self.simulatorObj.register[register_index[regCode]]
            self.simulatorObj.register[register_index['A']]&=reg_val
            self.handleUpdateStatus(self.simulatorObj.register[register_index['A']])
        self.simulatorObj.status.clear_bit(status_index['C'])
        self.simulatorObj.status.clear_bit(status_index['AC'])
    def executeCMA(self,int_data):
        acc_Data=self.simulatorObj.register[register_index['A']]
        self.simulatorObj.register[register_index['A']]=acc_Data^255

    def compare(self,regData,accData):
        res=accData-regData
        regLowerNibble,accLowerNibble=regData&15,accData&15
        if(regData>accData):
            self.simulatorObj.status.set_bit(status_index['S'])
            self.simulatorObj.status.set_bit(status_index['C'])
        else:
            self.simulatorObj.status.clear_bit(status_index['S'])
            self.simulatorObj.status.clear_bit(status_index['C'])
        if(res==0):
            self.simulatorObj.status.set_bit(status_index['Z'])
        else:
            self.simulatorObj.status.clear_bit(status_index['Z'])
        if(regData>accData):
            res=str(bin(res)[3:])
        else:
            res=str(bin(res)[2:])
        oneCount=0
        for i in res:
            if(i=='1'):
                oneCount+=1
        if(oneCount%2==0):
            self.simulatorObj.status.set_bit(status_index['P'])
        else:
            self.simulatorObj.status.clear_bit(status_index['P'])
        if(regLowerNibble>accLowerNibble):
            self.simulatorObj.status.set_bit(status_index['AC'])
        else:
            self.simulatorObj.status.clear_bit(status_index['AC'])

            




    def executeCMP(self,int_Code):
        binNumber=str(bin(int_Code)[2:])
        regCode=binNumber[-3::1]
        regCode=register[regCode]
        if(regCode=='M'):
            add=self.simulatorObj.get_Register_Pair('H')
            reg_val=self.simulatorObj.memory[add]
            acc_val=self.simulatorObj.register[register_index['A']]
            self.compare(reg_val,acc_val)
        else:
            reg_val=self.simulatorObj.register[register_index[regCode]]
            acc_val=self.simulatorObj.register[register_index['A']]
            self.compare(reg_val,acc_val)
    def executeDAD(self,int_Code):
        regCode=''
        if(int_Code==9):
            regCode='B'
        elif(int_Code==25):
            regCode=='D'
        elif(int_Code=='41'):
            regCode='H'
        elif(int_Code=='57'):
            regCode='H'
        else:
            print("incorect register")
        hl_data=self.simulatorObj.get_Register_Pair('H')
        reg_data=self.simulatorObj.get_Register_Pair(regCode)
        res=hl_data+reg_data
        if(res>2**16-1):
            self.simulatorObj.status.set_bit(status_index['C'])
            res&=2**16-1
        else:
            self.simulatorObj.status.clear_bit(status_index['C'])
        self.simulatorObj.set_Register_Pair('H',res)


    def updateAuxCarry(self,n1,n2,bit):
        res=n1+n2
        if(res>=2**bit):
            self.simulatorObj.status.set_bit(status_index['AC'])
        else:
            self.simulatorObj.status.clear_bit(status_index['AC'])
    def updateFlag(self,data,bit):
        if(data>=(2**bit)):
            self.simulatorObj.status.set_bit(status_index['C'])
            data%=(2**bit)
        else:
            self.simulatorObj.status.clear_bit(status_index['C'])
        if(data==0):
            self.simulatorObj.status.set_bit(status_index['Z'])
        else:
            self.simulatorObj.status.clear_bit(status_index['Z'])
        binNumber=str(bin(data)[2:]).zfill(bit)
        if(binNumber[0]=='1'):
            self.simulatorObj.status.set_bit(status_index['S'])
        else:
            self.simulatorObj.status.clear_bit(status_index['S'])
        oneCount=0
        for i in binNumber:
            if(i=='1'):
                oneCount+=1
        if(oneCount%2==0):
            self.simulatorObj.status.set_bit(status_index['P'])
        else:
            self.simulatorObj.status.clear_bit(status_index['P'])


    def add(self,first,second,bit):
        lowerNibble1,lowerNibble2=first&(int)(2**(bit/2)-1),second&(int)(2**(bit/2)-1)
        res=first+second
        self.updateAuxCarry(lowerNibble1,lowerNibble2,bit/2)
        self.updateFlag(res,bit)
        return res&(2**bit-1)

    def twos_comp(self,val,bit):
        s=str(bin(val)[2:]).zfill(bit)
        s=''.join(reversed(s))
        ans=0
        for i in range(0,len(s),1):
            if(s[i]=='0'):
                ans+=(2**i)
        return ans+1
        
    def sub(self,val1,val2,bit):
        two_Comp=self.twos_comp(val2,bit)
        two_Comp%=(2**bit)
        res=self.add(val1,two_Comp,bit)
        if(val2>val1):
            self.simulatorObj.status.set_bit(status_index['C'])
        else:
            self.simulatorObj.status.clear_bit(status_index['C'])
        return res
    
    def subWithoutStatus(self,val1,val2,bit):
        two_Comp=self.twos_comp(val2,bit)
        two_Comp%=(2**bit)
        res=(val1+two_Comp)&(2**bit-1)
        return res
    
    def executeDCR(self,int_Code):
        binNumber=str(bin(int_Code)[2:]).zfill(8)
        regCode=binNumber[2:5:1]
        regCode=register[regCode]
        oldCarry=self.simulatorObj.status.get_bit(status_index['C'])
        if(regCode=='M'):
            add=self.simulatorObj.get_Register_Pair('H')
            reg_val=self.simulatorObj.memory[add]
            self.simulatorObj.memory[add]=self.sub(reg_val,1,8)
        else:
            reg_val=self.simulatorObj.register[register_index[regCode]]
            self.simulatorObj.register[register_index[regCode]]=self.sub(reg_val,1,8)
        if(oldCarry==1):
            self.simulatorObj.status.set_bit(status_index['C'])
        else:
            self.simulatorObj.status.clear_bit(status_index['C'])
            
    def executeDCX(self,int_Code):
        binNumber=str(bin(int_Code)[2:]).zfill(8)
        regCode=binNumber[2:4:1]
        regName=register_pairs[regCode]
        if(regName!='SP'):
            regValue=self.simulatorObj.get_Register_Pair(regName)
            # this is a 16bit data
            res_val=self.subWithoutStatus(regValue,1,16)
            self.simulatorObj.set_Register_Pair(regName,res_val)
    def executeINR(self,int_Code):
        binNumber=str(bin(int_Code)[2:]).zfill(8)
        regCode=binNumber[2:5:1]
        regCode=register[regCode]
        oldCarry=self.simulatorObj.status.get_bit(status_index['C'])
        if(regCode=='M'):
            add=self.simulatorObj.get_Register_Pair('H')
            reg_val=self.simulatorObj.memory[add]
            res=self.add(reg_val,1,8)
            self.simulatorObj.memory[add]=res
        else:
            reg_val=self.simulatorObj.register[register_index[regCode]]
            res=self.add(reg_val,1,8)
            self.simulatorObj.register[register_index[regCode]]=res
        if(oldCarry==1):
            self.simulatorObj.status.set_bit(status_index['C'])
        else:
            self.simulatorObj.status.clear_bit(status_index['C'])
    def executeINX(self,int_Code):
        binNumber=str(bin(int_Code)[2:]).zfill(8)
        regCode=binNumber[2:4:1]
        regName=register_pairs[regCode]
        if(regName!='SP'):
            regValue=self.simulatorObj.get_Register_Pair(regName)
            # this is a 16bit data
            res_val=(regValue+1)&(2**16-1)
            self.simulatorObj.set_Register_Pair(regName,res_val)

    def executeORA(self,int_Code):
        binNumber=str(bin(int_Code)[2:]).zfill(8)
        regCode=binNumber[-3::1]
        regCode=register[regCode]
        if(regCode=='M'):
            add=self.simulatorObj.get_Register_Pair('H')
            reg_val=self.simulatorObj.memory[add]
            acc_val=self.simulatorObj.register[register_index['A']]
            acc_val=reg_val|acc_val
            self.simulatorObj.register[register_index['A']]=acc_val
        else:
            reg_val=self.simulatorObj.register[register_index[regCode]]
            acc_val=self.simulatorObj.register[register_index['A']]
            acc_val=reg_val|acc_val
            self.simulatorObj.register[register_index['A']]=acc_val
        self.updateFlag(self.simulatorObj.register[register_index['A']],8)
        self.simulatorObj.status.clear_bit(status_index['AC'])
        self.simulatorObj.status.clear_bit(status_index['C'])
    def executeRLC(self,int_Code):
        acc_val=self.simulatorObj.register[register_index['A']]
        binNumber=str(bin(acc_val)[2:]).zfill(8)
        acc_val<<=1
        acc_val%=(2**8)
        if(binNumber[0]=='1'):
            self.simulatorObj.status.set_bit(status_index['C'])
            acc_val+=1
        else:
            self.simulatorObj.status.clear_bit(status_index['C'])
        self.simulatorObj.register[register_index['A']]=acc_val
    def executeRRC(self,int_Code):
        acc_val=self.simulatorObj.register[register_index['A']]
        binNumber=str(bin(acc_val)[2:]).zfill(8)
        acc_val>>=1
        if(binNumber[7]=='1'):
            self.simulatorObj.status.set_bit(status_index['C'])
            acc_val|=(1<<7)
        else:
            self.simulatorObj.status.clear_bit(status_index['C'])
        self.simulatorObj.register[register_index['A']]=acc_val
    def executeRAL(self,int_Code):
        acc_val=self.simulatorObj.register[register_index['A']]
        binNumber=str(bin(acc_val)[2:]).zfill(8)
        acc_val<<=1
        if(self.simulatorObj.status.get_bit(status_index['C'])==1):
            acc_val+=1
        if(binNumber[0]=='1'):
            self.simulatorObj.status.set_bit(status_index['C'])
        else:
            self.simulatorObj.status.clear_bit(status_index['C'])
        acc_val%=(2**8)
        self.simulatorObj.register[register_index['A']]=acc_val
    def executeRAR(self,int_Code):
        acc_val=self.simulatorObj.register[register_index['A']]
        binNumber=str(bin(acc_val)[2:]).zfill(8)
        acc_val>>=1
        if(self.simulatorObj.status.get_bit(status_index['C'])==1):
            acc_val|=(1<<7)
        if(binNumber[7]=='1'):
            self.simulatorObj.status.set_bit(status_index['C'])
        else:
            self.simulatorObj.status.clear_bit(status_index['C'])
        self.simulatorObj.register[register_index['A']]=acc_val
    def executeSUB(self,int_Code):
        binNumber=str(bin(int_Code)[2:]).zfill(8)
        regCode=binNumber[-3::1]
        regCode=register[regCode]
        if(regCode=='M'):
            add=self.simulatorObj.get_Register_Pair('H')
            reg_val=self.simulatorObj.memory[add]
            acc_val=self.simulatorObj.register[register_index['A']]
            acc_val=self.sub(acc_val,reg_val,8)
            self.simulatorObj.register[register_index['A']]=acc_val
        else:
            reg_val=self.simulatorObj.register[register_index[regCode]]
            acc_val=self.simulatorObj.register[register_index['A']]
            acc_val=self.sub(acc_val,reg_val,8)
            self.simulatorObj.register[register_index['A']]=acc_val
    def executeSBB(self,int_Code):
        binNumber=str(bin(int_Code)[2:]).zfill(8)
        regCode=binNumber[-3::1]
        regCode=register[regCode]
        oldBorrow=self.simulatorObj.status.get_bit(status_index['C'])
        if(regCode=='M'):
            add=self.simulatorObj.get_Register_Pair('H')
            reg_val=self.simulatorObj.memory[add]
            acc_val=self.simulatorObj.register[register_index['A']]
            acc_val=self.sub(acc_val,reg_val,8)
            if(oldBorrow==1):
                acc_val=self.sub(acc_val,1,8)
            self.simulatorObj.register[register_index['A']]=acc_val
        else:
            reg_val=self.simulatorObj.register[register_index[regCode]]
            acc_val=self.simulatorObj.register[register_index['A']]
            acc_val=self.sub(acc_val,reg_val,8)
            if(oldBorrow==1):
                acc_val=self.sub(acc_val,1,8)
            self.simulatorObj.register[register_index['A']]=acc_val
    def executeXCHG(self,int_Code):
        HLVal=self.simulatorObj.get_Register_Pair("H")
        DEVal=self.simulatorObj.get_Register_Pair("D")
        self.simulatorObj.set_Register_Pair('H',DEVal)
        self.simulatorObj.set_Register_Pair('D',HLVal)
    def executeXRA(self,int_Code):
        binNumber=str(bin(int_Code)[2:]).zfill(8)
        regCode=binNumber[-3::1]
        regCode=register[regCode]
        if(regCode=='M'):
            add=self.simulatorObj.get_Register_Pair('H')
            reg_val=self.simulatorObj.memory[add]
            acc_val=self.simulatorObj.register[register_index['A']]
            acc_val^=reg_val
            self.updateFlag(acc_val,8)
            self.simulatorObj.register[register_index['A']]=acc_val
        else:
            reg_val=self.simulatorObj.register[register_index[regCode]]
            acc_val=self.simulatorObj.register[register_index['A']]
            acc_val^=reg_val
            self.updateFlag(acc_val,8)
            self.simulatorObj.register[register_index['A']]=acc_val

        self.simulatorObj.status.clear_bit(status_index['C'])
        self.simulatorObj.status.clear_bit(status_index['AC'])
    
    def executeMVI(self,int_Code):
        binNumber=str(bin(int_Code)[2:]).zfill(8)
        regCode=binNumber[2:5:1]
        regCode=register[regCode]
        program_Counter=self.simulatorObj.get_program_Counter()
        program_Counter+=1
        value=self.simulatorObj.memory[program_Counter]
        if(regCode=='M'):
            add=self.simulatorObj.get_Register_Pair('H')
            self.simulatorObj.memory[add]=value
        else:
            self.simulatorObj.register[register_index[regCode]]=value
    def executeADI(self,int_Code):
        program_Counter=self.simulatorObj.get_program_Counter()
        program_Counter+=1
        acc_val=self.simulatorObj.register[register_index['A']]
        value=self.simulatorObj.memory[program_Counter]
        res=self.add(acc_val,value,8)
        self.simulatorObj.register[register_index['A']]=res
    def executeANI(self,program_Counter):
        program_Counter+=1
        acc_val=self.simulatorObj.register[register_index['A']]
        value=self.simulatorObj.memory[program_Counter]    
        acc_val&=value
        self.updateFlag(acc_val,8)
        self.simulatorObj.register[register_index['A']]=acc_val
        self.simulatorObj.status.clear_bit(status_index['C'])
        self.simulatorObj.status.clear_bit(status_index['AC'])
    def executeORI(self,program_Counter):
        program_Counter+=1
        acc_val=self.simulatorObj.register[register_index['A']]
        value=self.simulatorObj.memory[program_Counter]    
        acc_val|=value
        self.updateFlag(acc_val,8)
        self.simulatorObj.register[register_index['A']]=acc_val
        self.simulatorObj.status.clear_bit(status_index['C'])
        self.simulatorObj.status.clear_bit(status_index['AC'])
    def executeSBI(self,program_counter):
        program_counter+=1
        oldBorrow=self.simulatorObj.status.get_bit(status_index['C']) 
        acc_val=self.simulatorObj.register[register_index['A']]
        value=self.simulatorObj.memory[program_counter]    
        acc_val=self.sub(acc_val,value,8)
        if(oldBorrow==1):
            acc_val=self.sub(acc_val,1,8)
        self.simulatorObj.register[register_index['A']]=acc_val
    def executeSUI(self,program_counter):
        program_counter+=1
        acc_val=self.simulatorObj.register[register_index['A']]
        value=self.simulatorObj.memory[program_counter]    
        acc_val=self.sub(acc_val,value,8)
        self.simulatorObj.register[register_index['A']]=acc_val
    def executeXRI(self,program_Counter):
        program_Counter+=1
        acc_val=self.simulatorObj.register[register_index['A']]
        value=self.simulatorObj.memory[program_Counter]    
        acc_val^=value
        self.updateFlag(acc_val,8)
        self.simulatorObj.register[register_index['A']]=acc_val
        self.simulatorObj.status.clear_bit(status_index['C'])
        self.simulatorObj.status.clear_bit(status_index['AC'])

    #RUNNING THE CODE 
    def execute_Code(self):
        pc=self.simulatorObj.get_program_Counter()
        while(self.simulatorObj.memory[pc]!=int("76",16) and self.simulatorObj.memory[pc+1]!=0):
            hexaData=hex(self.simulatorObj.memory[pc])[2:]
            hexaData=hexaData.upper()
            command_type=self.find_Command(hexaData)
            if(command_type=='MOV'):
                self.executeMOV(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='ADC'):
                self.executeADC(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='ADD'):
                self.executeADD(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='ANA'):
                self.executeANA(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='CMA'):
                self.executeCMA(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='CMC'):
                if(self.simulatorObj.status.get_bit(status_index['C'])==1):
                    self.simulatorObj.status.clear_bit(status_index['C'])
                else:
                    self.simulatorObj.status.set_bit(status_index['C'])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='CMP'):
                self.executeCMP(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='DAD'):
                self.executeDAD(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='DCR'):
                self.executeDCR(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='DCX'):
                self.executeDCX(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='INR'):
                self.executeINR(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='INX'):
                self.executeINX(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='ORA'):
                self.executeORA(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='RLC'):
                self.executeRLC(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='RRC'):
                self.executeRRC(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='RAL'):
                self.executeRAL(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            
            elif(command_type=='RAR'):
                self.executeRAR(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='SUB'):
                self.executeSUB(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif (command_type=='SBB'):
                self.executeSBB(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='XCHG'):
                self.executeXCHG(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='XRA'):
                self.executeXRA(self.simulatorObj.memory[pc])
                pc+=1
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='MVI'):
                self.executeMVI(self.simulatorObj.memory[pc])
                pc+=2
                self.simulatorObj.set_program_Counter(pc)
            
            elif(command_type=='ADI'):
                self.executeADI(self.simulatorObj.memory[pc])
                pc+=2
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='ANI'):
                self.executeANI(pc)
                pc+=2
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='ORI'):
                self.executeORI(pc)
                pc+=2
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='SBI'):
                self.executeSBI(pc)
                pc+=2
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='SUI'):
                self.executeSUI(pc)
                pc+=2
                self.simulatorObj.set_program_Counter(pc)
            elif(command_type=='XRI'):
                self.executeXRI(pc)
                pc+=2
                self.simulatorObj.set_program_Counter(pc)





# TESTING AREA
obj=interpretor()
# obj.simulatorObj.register[register_index['A']]=34
obj.simulatorObj.set_Register_Pair('H','2000')
obj.simulatorObj.set_Register_Pair('D','FFFF')

obj.simulatorObj.memory[int("2000",16)]=7
# s=["MOV C, A",'MOV B, C',"MOV B, M",'HLT']
obj.simulatorObj.register[register_index['A']]=255
obj.simulatorObj.register[register_index['C']]=2
# obj.simulatorObj.set_Register_Pair('B',-1)

obj.simulatorObj.status.set_bit(status_index['C'])  
obj.simulatorObj.status.set_bit(status_index['AC'])
obj.simulatorObj.status.set_bit(status_index['S'])
obj.simulatorObj.status.set_bit(status_index['P'])
# s=["DCR B","INR B","INR M",'HLT']
s=["MVI A, 03","MVI B, 02","XRI 05",'HLT']

obj.starting_address(4000)

for i in s:
    (obj.decode_insert(i))
obj.starting_address(4000)
print("running code")
obj.execute_Code()
print("\nAccumulator:",obj.simulatorObj.register[register_index['A']],end=" ,")
print("B Register:",obj.simulatorObj.register[register_index['B']],end=" ,")
print("C Register:",obj.simulatorObj.register[register_index['C']],end=' ,')
print("D Register:",obj.simulatorObj.register[register_index['D']],end=' ,')
print("E Register:",obj.simulatorObj.register[register_index['E']],end=' ,')
print("H Register:",obj.simulatorObj.register[register_index['H']],end=' ,')
print("L Register:",obj.simulatorObj.register[register_index['L']],)
print("\nZero:",obj.simulatorObj.status.get_bit(status_index['Z']),end=' ,')
print("SIGN:",obj.simulatorObj.status.get_bit(status_index['S']),end=' ,')
print("CARRY:",obj.simulatorObj.status.get_bit(status_index['C']),end=' ,')
print("PARITY:",obj.simulatorObj.status.get_bit(status_index['P']),end=' ,')
print("AUXILARY CARRY:",obj.simulatorObj.status.get_bit(status_index['AC']))
print("\nBC register Pair:",hex(obj.simulatorObj.get_Register_Pair('B')),end=" ,")
print("DE register Pair:",hex(obj.simulatorObj.get_Register_Pair('D')),end=" ,")
print("HL register Pair:",hex(obj.simulatorObj.get_Register_Pair('H')))
print("\nData int  memeory(HL):",obj.simulatorObj.memory[obj.simulatorObj.get_Register_Pair('H')])
