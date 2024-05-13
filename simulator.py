from dict import *
class bit:
    # status bit =[]
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
        self.stack_Memory=bytearray(2**16)
        self.status=bit()
        self.register=bytearray(9)  #All the 6 general purpose register + 1 Accumulator + 1 temp register + 1 instruction register  
        self.program_Counter=bytearray(2)


        self.stack_Pointer=bytearray(2)
        self.stack_Pointer[0],self.stack_Pointer[1]=int('ff',16),int("ff",16)
        self.address_Bus=bytearray(2)
        self.data_Bus=bytearray(1)

        self.bitObject=bitManipulation()
    def to_insert_hexaDecimal_Memory(self,add,data):
        if(type(add)==str):
            add=int(add,16)
        if(type(data)==str):
            data=int(data,16)
        lowerBit,upperBit=self.bitObject.get_Lower_And_Upper(data)
        self.memory[add]=lowerBit
        add+=1
        self.memory[add]=upperBit
    
    def set_program_Counter(self,address):
        if(type(address)==str):
            address=int(address,16)
        lowerBit,upperBit=self.bitObject.get_Lower_And_Upper(address)
        self.program_Counter[0]=upperBit
        self.program_Counter[1]=lowerBit
    def get_program_Counter(self):
        bitval=self.program_Counter[0]<<8
        bitval|=self.program_Counter[1]
        return int(bitval)

    def get_Stack_Pointer(self):
        bitval=self.stack_Pointer[0]<<8
        bitval|=self.stack_Pointer[1]
        return int(bitval)
    
    def set_stack_pointer(self,address):
        if(type(address)==str):
            address=int(address,16)
        lowerBit,upperBit=self.bitObject.get_Lower_And_Upper(address)
        self.stack_Pointer[0]=upperBit
        self.stack_Pointer[1]=lowerBit

    def push_Stack_Pointer(self,address):
        if(type(address)==str):
            address=int(address,16)
        lowerBit,upperBit=self.bitObject.get_Lower_And_Upper(address)
        stack_top=self.get_Stack_Pointer()
        stack_top-=1
        if(stack_top>0):
            self.stack_Memory[stack_top]=upperBit
            stack_top-=1
            self.stack_Memory[stack_top]=lowerBit
            self.set_stack_pointer(stack_top)
        else:
            print("Stack is full")
            print("Segmentation fault")
    def pop_Stack_Pointer(self):
        top=self.get_Stack_Pointer()
        if(top==0xffff):
            print("Empty stack")
        else:
            lower=self.stack_Memory[top]
            top+=1
            upper=self.stack_Memory[top]
            top+=1
            self.set_stack_pointer(top)
            return upper<<8|lower



        
       
    def get_address_Bus(self):
        bitval=self.address_Bus[0]<<8
        bitval|=self.address_Bus[1]
        return int(bitval)
    def set_address_Bus(self,address):
        if(type(address)==str):
            address=int(address,16)
        lowerBit,upperBit=self.bitObject.get_Lower_And_Upper(address)

        # {0,1}={upperBit,lowerBit}
        self.address_Bus[1],self.address_Bus[0]=lowerBit,upperBit
    
    def set_data_Bus(self,data):
        if(type(data)==str):
            data=int(data,16)
        self.data_Bus[0]=data
    
    def get_data_Bus(self):
        return self.data_Bus[0]
    
    def twos_comp(self,val,bit):
        s=str(bin(val)[2:]).zfill(bit)
        s=''.join(reversed(s))
        ans=0
        for i in range(0,len(s),1):
            if(s[i]=='0'):
                ans+=(2**i)
        return ans+1
        

    # REGISTERS FUNCTIONS
    def set_Register(self,Reg,data):
        if(type(data)==str):
            data=int(data,16)
        if(data<0):
            data=self.twos_comp(-data,8)
        self.register[register_index[Reg]]=data
    def get_Register(self,Reg):
        return self.register[register_index[Reg]]
    
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
    def insert_data_memory(self,data,add):
        if(type(data)==str):
            data=int(data,16)
        self.memory[add]=data
    def get_data_memeory(self,add):
        return self.memory[add]
        
    
    

    
    
