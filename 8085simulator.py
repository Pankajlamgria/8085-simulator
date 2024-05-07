from dict import *
class bit:
    def __init__(self):
        self.array=bytearray(1) 
        self.size=8
    def set_bit(self,index):
        if(index<self.size):
            self.array[0]|=(1<<index)
        else:
            raise IndexError("Index out of range.")
    def get_bit(self,index):
        if(index<self.size):
            temp_bit=self.array[0]
            while(index):
                temp_bit>>=1
                index-=1
            return temp_bit&1
        else:
            raise IndexError("Index out of range.")
    def clear_bit(self,index):
        if(index<self.size):
            self.array[0]&=~(1<<index)
        else:
            raise IndexError("Index out of range.")
    def toogle_bit(self,index):
        if(index<self.size):
            self.array[0]^=(1<<index)
        else:
            raise IndexError("Index out of range.")
        
class bitManipulation:
    def get_Lower_And_Upper(self,number):
        lowerBit=number&0xff
        upper=number
        for i in range(8):
            upper>>=1
        return lowerBit,upper 
       
class processor_8085:
    
    # Constructor Initializing memory
    def __init__(self):
        self.memory=bytearray(2**16)
        self.status=bit()
        #TODO set and get function for register
        self.register=bytearray(9)  #All the 6 general purpose register + 1 Accumulator + 1 temp register + 1 instruction register  
        
        self.stack_Pointer=bytearray(2)
        self.address_Bus=bytearray(2)
        self.data_Bus=bytearray(1)

        self.bitObject=bitManipulation()

    def set_Stack_Pointer(self,address):
        pass                   #TODO declare stack 
    def get_Stack_Pointer(self):
        pass 
    def get_address_Bus(self):
        bitval=self.address_Bus[1]<<8
        bitval|=self.address_Bus[0]
        return int(bitval)
    def set_address_Bus(self,address):
        address=int(address,16)
        lowerBit,upperBit=self.bitObject.get_Lower_And_Upper(address)
        self.address_Bus[0],self.address_Bus[1]=lowerBit,upperBit
    
    def set_data_Bus(self,data):
        if(type(data)==str):
            data=int(data,16)
        self.data_Bus[0]=data
    
    def get_data_Bus(self):
        return self.data_Bus[0]


    # REGISTERS FUNCTIONS
    def set_Register(self,Reg,data):
        if(type(data)==str):
            data=int(data,16)
        self.register[register_name[Reg]]=data
    def get_Register(self,Reg):
        return self.register[register_name[Reg]]
    
    # Pairs
    def set_Register_Pair(self,Register,data):
        if(type(data)==str):
            data=int(data,16)
        # its a 16 bit data
        lower,upper=self.bitObject.get_Lower_And_Upper(data)
        if(Register=='B'):
            self.set_Register('B',upper)
            self.set_Register('C',lower)
        elif(Register=='D'):
            self.set_Register('D',upper)
            self.set_Register('E',lower)
        elif(Register=='H' or Register=='M'):
            self.set_Register('H',upper)
            self.set_Register('L',lower)
        else:
            print("Wrong Register Pair assigned")
    def get_Register_Pair(self,Register):
        lower,upper=0,0
        if(Register=='B'):
            upper=self.get_Register('B')
            lower=self.get_Register('C')
        elif(Register=='D'):
            upper=self.get_Register('D')
            lower=self.get_Register('E')
        elif(Register=='H' or Register=='M'):
            upper=self.get_Register('H')
            lower=self.get_Register('L')
        else:
            print("Invalid Register Pair assigned")
        return upper<<8|lower

    
    

    
    




# %Testing

obj= processor_8085()
# obj.set_address_Bus("000a")
# print(obj.get_address_Bus())
# obj.set_data_Bus(255)
# print(obj.get_data_Bus())
# obj.setAccumulator(255)
# print(obj.getAccumulator())
# obj.set_data_Bus('f')
# print(obj.get_data_Bus())
# obj.set_Register_Pair("M","ffff")
# print(obj.get_Register_Pair("H"))
# obj.set_Register('A',"CA")
# print(obj.get_Register('A'))