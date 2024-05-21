from tkinter import *
from interpretor import *

from dict import *
class simulator:

    def __init__(self):
        self.interpreterObj=interpretor()
        self.MemorySearchFlag=False
        self.window=Tk()
        self.mainWindow()
    def run(self):
        self.window.mainloop()




    def update_Register(self):
        self.registerValues.config(text=str(f"REGISTERS :A={hex(self.interpreterObj.simulatorObj.register[register_index['A']])[2:].upper()} | B={hex(self.interpreterObj.simulatorObj.register[register_index['B']])[2:].upper()}  | C={hex(self.interpreterObj.simulatorObj.register[register_index['C']])[2:].upper()}  | D={hex(self.interpreterObj.simulatorObj.register[register_index['D']])[2:].upper()} | E={hex(self.interpreterObj.simulatorObj.register[register_index['E']])[2:].upper()}  |  H={hex(self.interpreterObj.simulatorObj.register[register_index['H']])[2:].upper()}  |  L={hex(self.interpreterObj.simulatorObj.register[register_index['L']])[2:].upper()}"))
    def update_Register_Pair(self):
        self.registerPairValues.config(text=str(f"REGISTER PAIR :     BC  =  {hex(self.interpreterObj.simulatorObj.get_Register_Pair('B'))[2:].upper()}    |    DE  =  {hex(self.interpreterObj.simulatorObj.get_Register_Pair('D'))[2:].upper()}    |    HL/M  =  {hex(self.interpreterObj.simulatorObj.get_Register_Pair('H'))[2:].upper()}"))
    def update_Status(self):
        self.signInput.config(text=f"{self.interpreterObj.simulatorObj.status.get_bit(status_index['S'])}")
        self.zeroInput.config(text=f"{self.interpreterObj.simulatorObj.status.get_bit(status_index['Z'])}")
        self.auqCarryInput.config(text=f"{self.interpreterObj.simulatorObj.status.get_bit(status_index['AC'])}")
        self.parityInput.config(text=f"{self.interpreterObj.simulatorObj.status.get_bit(status_index['P'])}")
        self.carryInput.config(text=f"{self.interpreterObj.simulatorObj.status.get_bit(status_index['C'])}")

    def setSign(self,event):
        self.interpreterObj.simulatorObj.status.set_bit(status_index['S'])
        self.update_Status()
    def setZero(self,event):
        self.interpreterObj.simulatorObj.status.set_bit(status_index['Z'])
        self.update_Status()
    def setAuqCarry(self,event):
        self.interpreterObj.simulatorObj.status.set_bit(status_index['AC'])
        self.update_Status()
    def setParity(self,event):
        self.interpreterObj.simulatorObj.status.set_bit(status_index['P'])
        self.update_Status()
    def setCarry(self,event):
        self.interpreterObj.simulatorObj.status.set_bit(status_index['C'])
        self.update_Status()


    def limitAddress(self,event=None):
        text=self.startingAddInput.get('1.0','end-1c')
        if len(text) > 4:
            self.startingAddInput.delete("1.0", "end")
            self.startingAddInput.insert("1.0", text[:4])
            
    def handleCompileFunction(self,event):
            if(self.startingAddInput.get('1.0',END).strip()!=''):
                memAdd=self.startingAddInput.get("1.0",END).strip()
                self.interpreterObj.starting_address(memAdd)
                code=self.textArea.get('1.0',END).strip()
                linesOfCode=code.splitlines()
                linesOfCode = [item for item in linesOfCode if item != ""]
                for line in linesOfCode:
                    self.interpreterObj.decode_insert(line)
    
    def handleRunFunction(self,event):
            if(self.startingAddInput.get('1.0',END).strip()!=''):
                memAdd=self.startingAddInput.get("1.0",END).strip()
                self.interpreterObj.starting_address(memAdd)
                self.interpreterObj.execute_Code()
                self.update_Register()
                self.update_Status()
                self.update_Register_Pair()
                if(self.memoryAddEntry.get()!=''):
                    self.updateMemoryTable(self.searchedMemAddStart)

    def updateMemoryTable(self,start):
        dataList=[self.data1,self.data2,self.data3,self.data4,self.data5,self.data6,self.data7,self.data8,self.data9,self.data10,self.data11,self.data12,self.data13,self.data14,self.data15,self.data16]
        addList=[self.memoryAddress1,self.memoryAddress2,self.memoryAddress3,self.memoryAddress4,self.memoryAddress5,self.memoryAddress6,self.memoryAddress7,self.memoryAddress8,self.memoryAddress9,self.memoryAddress10,self.memoryAddress11,self.memoryAddress12,self.memoryAddress13,self.memoryAddress14,self.memoryAddress15,self.memoryAddress16]

        i,upperLimit=start,65536
        ind=0
        while(ind<16):
            hexAdd=hex(i)[2:].upper()
            data=hex(self.interpreterObj.simulatorObj.memory[i])[2:].upper()
            addList[ind].config(text=f'{hexAdd}')
            dataList[ind].delete(0,END)
            dataList[ind].insert(0,f'{data}')
            ind+=1
            i=(i+1)%upperLimit
    def handleNextMemoryShow(self,event):
        if(self.MemorySearchFlag):
            if(self.searchedMemAddStart==65535):
                self.searchedMemAddStart=0
            else:
               self.searchedMemAddStart+=1 
            self.updateMemoryTable(self.searchedMemAddStart)
    def handlePrevMemoryShow(self,event):
        if(self.MemorySearchFlag):
            if(self.searchedMemAddStart==0):
                self.searchedMemAddStart=65535
            else:
                self.searchedMemAddStart-=1
            self.updateMemoryTable(self.searchedMemAddStart)

    def setStartingMemorytag(self,event):
        if(self.memoryAddEntry.get()!=''):
            self.searchedMemAddStart=int(self.memoryAddEntry.get(),16)
            if(not self.MemorySearchFlag):
                self.MemorySearchFlag=True
            self.updateMemoryTable(self.searchedMemAddStart)
    
    def handleUpdateMemory1(self,event):
        add=self.memoryAddress1.cget('text')
        if(add!=''):
            data=self.data1.get()
            if(data[0]!='-'):
                self.interpreterObj.simulatorObj.memory[int(add,16)]=int(data,16)
            else:
                absNumber=abs(int(data,16))
                twoscomp=self.interpreterObj.simulatorObj.twos_comp(absNumber,8)
                self.interpreterObj.simulatorObj.memory[int(add,16)]=twoscomp


    def handleUpdateMemory2(self,event):
        add=self.memoryAddress2.cget('text')
        if(add!=''):
            data=self.data2.get()
            if(data[0]=='-'):
                data=hex(self.interpreterObj.simulatorObj.twos_comp(abs(int(data,16)),8))[2:]
            self.interpreterObj.simulatorObj.memory[int(add,16)]=int(data,16)
    def handleUpdateMemory3(self,event):
        add=self.memoryAddress3.cget('text')
        if(add!=''):
            data=self.data3.get()
            if(data[0]=='-'):
                data=hex(self.interpreterObj.simulatorObj.twos_comp(abs(int(data,16)),8))[2:]
            self.interpreterObj.simulatorObj.memory[int(add,16)]=int(data,16)
    def handleUpdateMemory4(self,event):
        add=self.memoryAddress4.cget('text')
        if(add!=''):
            data=self.data4.get()
            if(data[0]=='-'):
                data=hex(self.interpreterObj.simulatorObj.twos_comp(abs(int(data,16)),8))[2:]
            self.interpreterObj.simulatorObj.memory[int(add,16)]=int(data,16)
    def handleUpdateMemory5(self,event):
        add=self.memoryAddress5.cget('text')
        if(add!=''):
            data=self.data5.get()
            if(data[0]=='-'):
                data=hex(self.interpreterObj.simulatorObj.twos_comp(abs(int(data,16)),8))[2:]
            self.interpreterObj.simulatorObj.memory[int(add,16)]=int(data,16)
    def handleUpdateMemory6(self,event):
        add=self.memoryAddress6.cget('text')
        if(add!=''):
            data=self.data6.get()
            if(data[0]=='-'):
                data=hex(self.interpreterObj.simulatorObj.twos_comp(abs(int(data,16)),8))[2:]
            self.interpreterObj.simulatorObj.memory[int(add,16)]=int(data,16)
    def handleUpdateMemory7(self,event):
        add=self.memoryAddress7.cget('text')
        if(add!=''):
            data=self.data7.get()
            if(data[0]=='-'):
                data=hex(self.interpreterObj.simulatorObj.twos_comp(abs(int(data,16)),8))[2:]
            self.interpreterObj.simulatorObj.memory[int(add,16)]=int(data,16)
    def handleUpdateMemory8(self,event):
        add=self.memoryAddress8.cget('text')
        if(add!=''):
            data=self.data8.get()
            if(data[0]=='-'):
                data=hex(self.interpreterObj.simulatorObj.twos_comp(abs(int(data,16)),8))[2:]
            self.interpreterObj.simulatorObj.memory[int(add,16)]=int(data,16)
    def handleUpdateMemory9(self,event):
        add=self.memoryAddress9.cget('text')
        if(add!=''):
            data=self.data9.get()
            if(data[0]=='-'):
                data=hex(self.interpreterObj.simulatorObj.twos_comp(abs(int(data,16)),8))[2:]
            self.interpreterObj.simulatorObj.memory[int(add,16)]=int(data,16)
    def handleUpdateMemory10(self,event):
        add=self.memoryAddress10.cget('text')
        if(add!=''):
            data=self.data10.get()
            if(data[0]=='-'):
                data=hex(self.interpreterObj.simulatorObj.twos_comp(abs(int(data,16)),8))[2:]
            self.interpreterObj.simulatorObj.memory[int(add,16)]=int(data,16)
    def handleUpdateMemory11(self,event):
        add=self.memoryAddress11.cget('text')
        if(add!=''):
            data=self.data11.get()
            if(data[0]=='-'):
                data=hex(self.interpreterObj.simulatorObj.twos_comp(abs(int(data,16)),8))[2:]
            self.interpreterObj.simulatorObj.memory[int(add,16)]=int(data,16)
    def handleUpdateMemory12(self,event):
        add=self.memoryAddress12.cget('text')
        if(add!=''):
            data=self.data12.get()
            if(data[0]=='-'):
                data=hex(self.interpreterObj.simulatorObj.twos_comp(abs(int(data,16)),8))[2:]
            self.interpreterObj.simulatorObj.memory[int(add,16)]=int(data,16)
    def handleUpdateMemory13(self,event):
        add=self.memoryAddress13.cget('text')
        if(add!=''):
            data=self.data13.get()
            if(data[0]=='-'):
                data=hex(self.interpreterObj.simulatorObj.twos_comp(abs(int(data,16)),8))[2:]
            self.interpreterObj.simulatorObj.memory[int(add,16)]=int(data,16)
    def handleUpdateMemory14(self,event):
        add=self.memoryAddress14.cget('text')
        if(add!=''):
            data=self.data14.get()
            if(data[0]=='-'):
                data=hex(self.interpreterObj.simulatorObj.twos_comp(abs(int(data,16)),8))[2:]
            self.interpreterObj.simulatorObj.memory[int(add,16)]=int(data,16)
    def handleUpdateMemory15(self,event):
        add=self.memoryAddress15.cget('text')
        if(add!=''):
            data=self.data15.get()
            if(data[0]=='-'):
                data=hex(self.interpreterObj.simulatorObj.twos_comp(abs(int(data,16)),8))[2:]
            self.interpreterObj.simulatorObj.memory[int(add,16)]=int(data,16)
    def handleUpdateMemory16(self,event):
        add=self.memoryAddress16.cget('text')
        if(add!=''):
            data=self.data16.get()
            if(data[0]=='-'):
                data=hex(self.interpreterObj.simulatorObj.twos_comp(abs(int(data,16)),8))[2:]
            self.interpreterObj.simulatorObj.memory[int(add,16)]=int(data,16)
    def validate_address(self,new_value):
        return len(new_value)<=4
    def validate_data(self,new_value):
        return len(new_value)<=3

    def handleClearStatus(self,event):
        self.interpreterObj.simulatorObj.status.clear_bit(status_index['S'])
        self.interpreterObj.simulatorObj.status.clear_bit(status_index['Z'])
        self.interpreterObj.simulatorObj.status.clear_bit(status_index['AC'])
        self.interpreterObj.simulatorObj.status.clear_bit(status_index['P'])
        self.interpreterObj.simulatorObj.status.clear_bit(status_index['C'])
        for i in range(0,8):
            self.interpreterObj.simulatorObj.register[i]=0
        self.update_Register()
        self.update_Status()
        self.update_Register_Pair()
        
    def handleClearMemory(self,event):
        for i in range(0,2**16):
            self.interpreterObj.simulatorObj.memory[i]=0 
        if(self.MemorySearchFlag):         
            self.updateMemoryTable(self.searchedMemAddStart)
    def handleToHexadecimal(self,event):
        if(self.decimalEntry.get()!=''):
            intNumber=int(self.decimalEntry.get())
            hexNumber=hex(intNumber)[2:].upper()
            self.hexadecimalEntry.delete(0,END)
            self.hexadecimalEntry.insert(0,f'{hexNumber}')
    def handleToDecimal(self,event):
        if(self.hexadecimalEntry.get()!=''):
            hexNumber=self.hexadecimalEntry.get()
            intNumber=int(hexNumber,16)
            self.decimalEntry.delete(0,END)
            self.decimalEntry.insert(0,f'{intNumber}')


    def mainWindow(self):
        self.window.title("8085-Simulator")

        self.window.configure(width='1150px',height='580px')
        header=Label(text="!!!WRITE 8085 CODE HERE!!!",font=('Helvetica', 14, 'bold'),borderwidth=2,relief='raised')
        header.place(relheight=.04,relwidth=.5)  

        self.startingAddLabel=Label(text="STARTING ADDRESS:",font=('Arial',12),relief="flat")
        self.startingAddLabel.place(rely=.04,relheight=.03)

        self.startingAddInput=Text(font=('Arial', 12),padx=8)
        self.startingAddInput.place(rely=.04,relx=.11,relheight=.03,relwidth=.08)


        self.compileBtn=Button(self.window,text="Compile",font=
                               ('Arial',10,'bold'),cursor='hand2',borderwidth=3,relief='ridge')
        self.compileBtn.place(rely=.04,relx=.4,relwidth=.05,relheight=.03)
        self.runBtn=Button(self.window,text="Run",font=
                               ('Arial',10,"bold"),cursor='hand2',borderwidth=3,relief='ridge',command=self.update_Register)
        self.runBtn.place(rely=.04,relx=.45,relwidth=.05,relheight=.03)

        self.validateData=self.window.register(self.validate_data)
        self.validateADD=self.window.register(self.validate_address)
        

        self.textArea=Text(font=('Times', 16),padx=4,pady=4)
        self.textArea.place(rely=.07,relheight=.65,relwidth=.49)

        scrollbar=Scrollbar(self.window)


        scrollbar.place(relheight=.65,relx=.4899,relwidth=.01,rely=.07)
        scrollbar.configure(command=self.textArea.yview)

        registerFrame=Frame(self.window,border=1,relief="groove")
        registerFrame.place(rely=.72,relheight=.4,relwidth=.5)

  

        self.registerValues=Label(registerFrame,text=f"REGISTERS :A={hex(self.interpreterObj.simulatorObj.register[register_index['A']])[2:].upper()} | B={hex(self.interpreterObj.simulatorObj.register[register_index['B']])[2:].upper()}  | C={hex(self.interpreterObj.simulatorObj.register[register_index['C']])[2:].upper()}  | D={hex(self.interpreterObj.simulatorObj.register[register_index['D']])[2:].upper()} | E={hex(self.interpreterObj.simulatorObj.register[register_index['E']])[2:].upper()}  |  H={hex(self.interpreterObj.simulatorObj.register[register_index['H']])[2:].upper()}  |  L={hex(self.interpreterObj.simulatorObj.register[register_index['L']])[2:].upper()}",font=('Times', 16),border=1,relief='groove',bg="white",padx=12,pady=8)
        self.registerValues.place(x=15,y=5)

        self.ClearSignBtn=Button(registerFrame,text='Clear',borderwidth=3,relief='ridge',font=('Arial',14),cursor='hand2')
        self.ClearSignBtn.place(y=6,relx=.83,relwidth=.15)


        self.SignFrame=Frame(registerFrame,border=1,relief='ridge',height=50, width=700,pady=10)
        self.SignFrame.place(relheight='.5',relwidth=.96,relx=.02,rely=.16)

        self.signBtn=Button(self.SignFrame,text='S',font=('Times',18),cursor='hand2',borderwidth=2,relief='ridge')
        self.zeroBtn=Button(self.SignFrame,text='Z',font=('Times',18),cursor='hand2',borderwidth=2,relief='ridge')
        Empty1=Button(self.SignFrame,text='',font=('Times',18),cursor='hand2',borderwidth=1,relief='ridge')
        self.auqCarryBtn=Button(self.SignFrame,text='AC',font=('Times',18),cursor='hand2',borderwidth=2,relief='ridge')
        Empty2=Button(self.SignFrame,text='',font=('Times',18),cursor='hand2',borderwidth=1,relief='ridge')
        self.parityBtn=Button(self.SignFrame,text='P',font=('Times',18),cursor='hand2',borderwidth=2,relief='ridge')
        Empty3=Button(self.SignFrame,text='',font=('Times',18),cursor='hand2',borderwidth=1,relief='ridge')
        self.carryBtn=Button(self.SignFrame,text='CY',font=('Times',18),cursor='hand2',borderwidth=2,relief='ridge')
        
        self.signBtn.place(relx=.01,rely=.03,relwidth=.1225,relheight=.4)
        self.zeroBtn.place(relx=.1325,rely=.03,relwidth=.1225,relheight=.4)
        Empty1.place(relx=.255,rely=.03,relwidth=.1225,relheight=.4)
        self.auqCarryBtn.place(relx=.3775,rely=.03,relwidth=.1225,relheight=.4)
        Empty2.place(relx=.5,rely=.03,relwidth=.1225,relheight=.4)
        self.parityBtn.place(relx=.6225,rely=.03,relwidth=.1225,relheight=.4)
        Empty3.place(relx=.745,rely=.03,relwidth=.1225,relheight=.4)
        self.carryBtn.place(relx=.8675,rely=.03,relwidth=.1225,relheight=.4)

        self.signInput=Label(self.SignFrame,text=f"{self.interpreterObj.simulatorObj.status.get_bit(status_index['S'])}",font=('Times', 22),padx=28,pady=14,borderwidth=1,relief='ridge')
        self.zeroInput=Label(self.SignFrame,text=f"{self.interpreterObj.simulatorObj.status.get_bit(status_index['Z'])}",font=('Times',22),padx=28 ,pady=14,borderwidth=1,relief='ridge')
        EmptyInput1=Label(self.SignFrame,font=('Times',22),padx=28 ,pady=14,borderwidth=1,relief='ridge')
        self.auqCarryInput=Label(self.SignFrame,text=f"{self.interpreterObj.simulatorObj.status.get_bit(status_index['AC'])}",font=('Times',22),padx=28 ,pady=14,borderwidth=1,relief='ridge')
        EmptyInput2=Label(self.SignFrame,font=('Times',22),padx=28 ,pady=14,borderwidth=1,relief='ridge')
        self.parityInput=Label(self.SignFrame,text=f"{self.interpreterObj.simulatorObj.status.get_bit(status_index['P'])}",font=('Times',22),padx=28 ,pady=14,borderwidth=1,relief='ridge')
        EmptyInput3=Label(self.SignFrame,font=('Times',22),padx=28 ,pady=14,borderwidth=1,relief='ridge')
        self.carryInput=Label(self.SignFrame,text=f"{self.interpreterObj.simulatorObj.status.get_bit(status_index['C'])}",font=('Times',22),padx=28 ,pady=14,borderwidth=1,relief='ridge')


        self.signInput.place(rely=.44,relx=.011,relwidth=.1225,relheight=.4)
        self.zeroInput.place(relx=.1326,rely=.44,relwidth=.1225,relheight=.4)
        EmptyInput1.place(relx=.256,rely=.44,relwidth=.1225,relheight=.4)
        self.auqCarryInput.place(relx=.3776,rely=.44,relwidth=.1225,relheight=.4)
        EmptyInput2.place(relx=.501,rely=.44,relwidth=.1225,relheight=.4)   
        self.parityInput.place(relx=.6226,rely=.44,relwidth=.1225,relheight=.4)
        EmptyInput3.place(relx=.746,rely=.44,relwidth=.1225,relheight=.4)
        self.carryInput.place(relx=.8676,rely=.44,relwidth=.1225,relheight=.4)

        self.rightFrame=Frame(self.window,borderwidth=1,relief='groove')
        self.rightFrame.place(relx=.5,relheight=1,relwidth=.5)

        memoryHeader=Label(self.rightFrame,text="!!!MEMORY!!!",font=('Helvetica', 16, 'bold'),borderwidth=2,relief='raised')
        memoryHeader.place(relheight=.07,relwidth=1)

        # horLine2=Label(self.rightFrame,text="")
        # horLine2.place(rely=.07,relheight=.1,relwidth=1)

        memoryAddLabel=Label(self.rightFrame,text="Starting Address:",font=('Times',16),relief="ridge")
        memoryAddLabel.place(rely=.07,relheight=.06,relwidth=.25)


        self.memoryAddEntry=Entry(self.rightFrame,font=('Times',16),borderwidth=1,relief='ridge',justify='center',validate='key',validatecommand=(self.validateADD,'%P'))
        self.memoryAddEntry.place(rely=.07,relx=.25,relheight=.06,relwidth=.18)
        
        self.searchBtn=Button(self.rightFrame,text="FIND",font=('Arial',14),cursor='hand2',borderwidth=3,relief='ridge')
        self.searchBtn.place(rely=.07,relx=.43,relheight=.06,relwidth=.1)

        self.clearMemoryBtn=Button(self.rightFrame,text="CLEAR MEMORY",borderwidth=3,relief='ridge',font=('Arial',12),cursor='hand2')
        self.clearMemoryBtn.place(rely=.07,relx=.77,relheight=.06,relwidth=.22)

        self.memoryAddTableFrame=Frame(self.rightFrame,borderwidth=1,relief='ridge')
        self.memoryAddTableFrame.place(rely=.13,relwidth=1,relheight=.7)

        addressLabel=Label(self.memoryAddTableFrame,text='ADDRESS',font=('Times',14),justify='center',borderwidth=1,relief='ridge')
        addressLabel.place(relheight=.07 ,relwidth=.2)

        dataLabel=Label(self.memoryAddTableFrame,text='DATA',font=('Times',14),justify='center',borderwidth=1,relief='ridge')
        dataLabel.place(relheight=.07,relwidth=.8,relx=.2)

        self.memoryAddress1=Label(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',bg='white') 
        self.memoryAddress1.place(relheight=.05,relwidth=.2,rely=.07)
        self.data1=Entry(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',validate='key',validatecommand=(self.validateData,'%P'))
        self.data1.place(relheight=.05,relwidth=.8,rely=.07,relx=.2)
         
        self.memoryAddress2=Label(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',bg='white')
        self.memoryAddress2.place(relheight=.05,relwidth=.2,rely=.12)
        self.data2=Entry(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',validate='key',validatecommand=(self.validateData,'%P'))
        self.data2.place(relheight=.05,relwidth=.8,rely=.12,relx=.2)
         
        self.memoryAddress3=Label(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',bg='white')
        self.memoryAddress3.place(relheight=.05,relwidth=.2,rely=.17)
        self.data3=Entry(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',validate='key',validatecommand=(self.validateData,'%P'))
        self.data3.place(relheight=.05,relwidth=.8,rely=.17,relx=.2)
         
        self.memoryAddress4=Label(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',bg='white')
        self.memoryAddress4.place(relheight=.05,relwidth=.2,rely=.22)
        self.data4=Entry(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',validate='key',validatecommand=(self.validateData,'%P'))
        self.data4.place(relheight=.05,relwidth=.8,rely=.22,relx=.2)
         
        self.memoryAddress5=Label(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',bg='white')
        self.memoryAddress5.place(relheight=.05,relwidth=.2,rely=.27)
        self.data5=Entry(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',validate='key',validatecommand=(self.validateData,'%P'))
        self.data5.place(relheight=.05,relwidth=.8,rely=.27,relx=.2)
         
        self.memoryAddress6=Label(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',bg='white')
        self.memoryAddress6.place(relheight=.05,relwidth=.2,rely=.32)
        self.data6=Entry(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',validate='key',validatecommand=(self.validateData,'%P'))
        self.data6.place(relheight=.05,relwidth=.8,rely=.32,relx=.2)
         
        self.memoryAddress7=Label(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',bg='white')
        self.memoryAddress7.place(relheight=.05,relwidth=.2,rely=.37)
        self.data7=Entry(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',validate='key',validatecommand=(self.validateData,'%P'))
        self.data7.place(relheight=.05,relwidth=.8,rely=.37,relx=.2)

        self.memoryAddress8=Label(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',bg='white')
        self.memoryAddress8.place(relheight=.05,relwidth=.2,rely=.42)
        self.data8=Entry(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',validate='key',validatecommand=(self.validateData,'%P'))
        self.data8.place(relheight=.05,relwidth=.8,rely=.42,relx=.2)
         
        self.memoryAddress9=Label(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',bg='white')
        self.memoryAddress9.place(relheight=.05,relwidth=.2,rely=.47)
        self.data9=Entry(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',validate='key',validatecommand=(self.validateData,'%P'))
        self.data9.place(relheight=.05,relwidth=.8,rely=.47,relx=.2)
         
        self.memoryAddress10=Label(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',bg='white')
        self.memoryAddress10.place(relheight=.05,relwidth=.2,rely=.52)
        self.data10=Entry(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',validate='key',validatecommand=(self.validateData,'%P'))
        self.data10.place(relheight=.05,relwidth=.8,rely=.52,relx=.2)
         
        self.memoryAddress11=Label(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',bg='white')
        self.memoryAddress11.place(relheight=.05,relwidth=.2,rely=.57)
        self.data11=Entry(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',validate='key',validatecommand=(self.validateData,'%P'))
        self.data11.place(relheight=.05,relwidth=.8,rely=.57,relx=.2)
         
        self.memoryAddress12=Label(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',bg='white')
        self.memoryAddress12.place(relheight=.05,relwidth=.2,rely=.62)
        self.data12=Entry(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',validate='key',validatecommand=(self.validateData,'%P'))
        self.data12.place(relheight=.05,relwidth=.8,rely=.62,relx=.2)
         
        self.memoryAddress13=Label(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',bg='white')
        self.memoryAddress13.place(relheight=.05,relwidth=.2,rely=.67)
        self.data13=Entry(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',validate='key',validatecommand=(self.validateData,'%P'))
        self.data13.place(relheight=.05,relwidth=.8,rely=.67,relx=.2)
         
        self.memoryAddress14=Label(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',bg='white')
        self.memoryAddress14.place(relheight=.05,relwidth=.2,rely=.72)
        self.data14=Entry(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',validate='key',validatecommand=(self.validateData,'%P'))
        self.data14.place(relheight=.05,relwidth=.8,rely=.72,relx=.2)
        
        self.memoryAddress15=Label(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',bg='white')
        self.memoryAddress15.place(relheight=.05,relwidth=.2,rely=.77)
        self.data15=Entry(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',validate='key',validatecommand=(self.validateData,'%P'))
        self.data15.place(relheight=.05,relwidth=.8,rely=.77,relx=.2)

        self.memoryAddress16=Label(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',bg='white')
        self.memoryAddress16.place(relheight=.05,relwidth=.2,rely=.82)
        self.data16=Entry(self.memoryAddTableFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',validate='key',validatecommand=(self.validateData,'%P'))
        self.data16.place(relheight=.05,relwidth=.8,rely=.82,relx=.2)

        hline=Label(self.memoryAddTableFrame,text="",bg='grey')
        hline.place(relheight=.001,relwidth=1,rely=.871)
         
        self.prevBtn=Button(self.memoryAddTableFrame,text="PREV",font=('Arial',14),cursor='hand2',borderwidth=3,relief='ridge')
        self.prevBtn.place(rely=.89,relx=.75,relheight=.08,relwidth=.1)

        self.nextBtn=Button(self.memoryAddTableFrame,text="NEXT",font=('Arial',14),cursor='hand2',borderwidth=3,relief='ridge')
        self.nextBtn.place(rely=.89,relx=.86,relheight=.08,relwidth=.1)

        self.registerPairFrame=Frame(self.rightFrame,borderwidth=1,relief='groove')
        self.registerPairFrame.place(rely=.83,relwidth=1,relheight=.17)

        self.registerPairValues=Label(self.registerPairFrame,text=f"REGISTER PAIR :     BC  =  {hex(self.interpreterObj.simulatorObj.get_Register_Pair('B'))[2:].upper()}    |    DE  =  {hex(self.interpreterObj.simulatorObj.get_Register_Pair('D'))[2:].upper()}    |    HL/M  =  {hex(self.interpreterObj.simulatorObj.get_Register_Pair('H'))[2:].upper()}",font=('Time',16),borderwidth=1,relief='groove',bg='white',padx=12,pady=8)
        self.registerPairValues.place(relx=.01,rely=.05)

        horLine=Label(self.registerPairFrame,bg='black')
        horLine.place(rely=.43,relwidth=1,relheight=.015)

        self.hexadecimalEntry=Entry(self.registerPairFrame,font=('Times',16),borderwidth=1,relief="ridge",justify='center')
        self.hexadecimalEntry.place(rely=.5,relx=.01,relwidth=.2,relheight=.3)
        self.toDecimalBtn=Button(self.registerPairFrame,text="To Dec ⇒",font=("Times",16),borderwidth=2,relief='ridge',cursor='hand2')
        self.toDecimalBtn.place(rely=.5,relx=.21,relwidth=.2,relheight=.3)
        
        equalLabel=Label(self.registerPairFrame,text="⇆",font=('Times',20,'bold'),justify='center')
        equalLabel.place(rely=.5,relx=.41,relwidth=.09,relheight=.3)

        self.toHexadecimalBtn=Button(self.registerPairFrame,text="⇐ To Hex",font=("Times",16),borderwidth=2,relief='ridge',cursor='hand2')
        self.toHexadecimalBtn.place(rely=.5,relx=.5,relwidth=.2,relheight=.3)
        self.decimalEntry=Entry(self.registerPairFrame,font=('Times',16),borderwidth=1,relief="ridge",justify='center')
        self.decimalEntry.place(rely=.5,relx=.7,relwidth=.2,relheight=.3)




        


        self.startingAddInput.bind("<KeyRelease>",self.limitAddress)
        self.compileBtn.bind('<Button-1>',self.handleCompileFunction)
        self.runBtn.bind('<Button-1>',self.handleRunFunction)

        self.signBtn.bind('<Button-1>',self.setSign)
        self.zeroBtn.bind('<Button-1>',self.setZero)
        self.auqCarryBtn.bind('<Button-1>',self.setAuqCarry)
        self.parityBtn.bind('<Button-1>',self.setParity)
        self.carryBtn.bind('<Button-1>',self.setCarry)

        self.searchBtn.bind("<Button-1>",self.setStartingMemorytag)
        self.startingAddInput.bind('<Return>',self.setStartingMemorytag)
        self.nextBtn.bind("<Button-1>",self.handleNextMemoryShow)
        self.prevBtn.bind("<Button-1>",self.handlePrevMemoryShow)

        self.data1.bind("<Return>",self.handleUpdateMemory1)
        self.data2.bind("<Return>",self.handleUpdateMemory2)
        self.data3.bind("<Return>",self.handleUpdateMemory3)
        self.data4.bind("<Return>",self.handleUpdateMemory4)
        self.data5.bind("<Return>",self.handleUpdateMemory5)
        self.data6.bind("<Return>",self.handleUpdateMemory6)
        self.data7.bind("<Return>",self.handleUpdateMemory7)
        self.data8.bind("<Return>",self.handleUpdateMemory8)
        self.data9.bind("<Return>",self.handleUpdateMemory9)
        self.data10.bind("<Return>",self.handleUpdateMemory10)
        self.data11.bind("<Return>",self.handleUpdateMemory11)
        self.data12.bind("<Return>",self.handleUpdateMemory12)
        self.data13.bind("<Return>",self.handleUpdateMemory13)
        self.data14.bind("<Return>",self.handleUpdateMemory14)
        self.data15.bind("<Return>",self.handleUpdateMemory15)
        self.data16.bind("<Return>",self.handleUpdateMemory16)
    
        self.ClearSignBtn.bind('<Button-1>',self.handleClearStatus)
        self.clearMemoryBtn.bind('<Button-1>',self.handleClearMemory)

        self.toHexadecimalBtn.bind('<Button-1>',self.handleToHexadecimal)
        self.toDecimalBtn.bind('<Button-1>',self.handleToDecimal)


try:
    app=simulator()
    app.run()
except Exception as e:
    print("SomeError Occured")
    print(e)