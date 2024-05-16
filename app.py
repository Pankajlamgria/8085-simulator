from tkinter import *
from interpretor import *
from dict import *
class simulator:
    def update_Register(self):
        self.registerValues.config(text=str(f"REGISTERS :    A={hex(self.interpreterObj.simulatorObj.register[register_index['A']])[2:].upper()}  |  B={hex(self.interpreterObj.simulatorObj.register[register_index['B']])[2:].upper()}   |  C={hex(self.interpreterObj.simulatorObj.register[register_index['C']])[2:].upper()}   |  D={hex(self.interpreterObj.simulatorObj.register[register_index['D']])[2:].upper()}  |  E={hex(self.interpreterObj.simulatorObj.register[register_index['E']])[2:].upper()}   |   H={hex(self.interpreterObj.simulatorObj.register[register_index['H']])[2:].upper()}   |   L={hex(self.interpreterObj.simulatorObj.register[register_index['L']])[2:].upper()}"))
    def __init__(self):
        self.interpreterObj=interpretor()
        self.window=Tk()
        self.mainWindow()
        # self.Areg=StringVar()
    def run(self):
        self.window.mainloop()
    def mainWindow(self):
        self.window.title("8085-Simulator")
        self.window.configure(width='1150px',height='580px',bg="#d1d1e0")
        header=Label(text="!!!WRITE 8085 CODE HERE!!!",bg='#66a3ff',fg="white",font=('Helvetica', 14, 'bold'))
        header.place(relheight=.04,relwidth=.5)  

        self.startingAddLabel=Label(text="STARTING ADDRESS:",font=('Arial',12),relief="flat")
        self.startingAddLabel.place(rely=.04,relheight=.03)

        self.startingAddInput=Text(font=('Arial', 12),padx=2)
        self.startingAddInput.place(rely=.04,relx=.11,relheight=.03,relwidth=.06)

        self.compileBtn=Button(self.window,text="Compile",font=
                               ('Arial',10,'bold'),cursor='hand2',borderwidth=1,relief='ridge')
        self.compileBtn.place(rely=.04,relx=.4,relwidth=.05,relheight=.03)
        self.runBtn=Button(self.window,text="Run",font=
                               ('Arial',10,"bold"),cursor='hand2',borderwidth=1,relief='ridge',command=self.update_Register)
        self.runBtn.place(rely=.04,relx=.45,relwidth=.05,relheight=.03)


        self.textArea=Text(font=('Times', 16),padx=4,pady=4)
        self.textArea.place(rely=.07,relheight=.65,relwidth=.49)

        scrollbar=Scrollbar(self.window)


        scrollbar.place(relheight=.65,relx=.4899,relwidth=.01,rely=.07)
        scrollbar.configure(command=self.textArea.yview)

        registerFrame=Frame(self.window,border=1,relief="groove")
        registerFrame.place(rely=.72,relheight=.4,relwidth=.5)


        self.registerValues=Label(registerFrame,text=f"REGISTERS :    A={hex(self.interpreterObj.simulatorObj.register[register_index['A']])[2:].upper()}  |  B={hex(self.interpreterObj.simulatorObj.register[register_index['B']])[2:].upper()}   |  C={hex(self.interpreterObj.simulatorObj.register[register_index['C']])[2:].upper()}   |  D={hex(self.interpreterObj.simulatorObj.register[register_index['D']])[2:].upper()}  |  E={hex(self.interpreterObj.simulatorObj.register[register_index['E']])[2:].upper()}   |   H={hex(self.interpreterObj.simulatorObj.register[register_index['H']])[2:].upper()}   |   L={hex(self.interpreterObj.simulatorObj.register[register_index['L']])[2:].upper()}",font=('Times', 16),border=1,relief='groove',bg="white",padx=12)
        self.registerValues.place(x=15,y=5)

        self.SignFrame=Frame(registerFrame,border=1,relief='groove',height=50, width=700)
        self.SignFrame.place(relheight='.5',relwidth=.96,relx=.02,rely=.14)
        signBtn=Button(self.SignFrame,text='S',font=('Times',18),cursor='hand2',borderwidth=1,relief='ridge')
        zeroBtn=Button(self.SignFrame,text='Z',font=('Times',18),cursor='hand2',borderwidth=1,relief='ridge')
        Empty1=Button(self.SignFrame,text='',font=('Times',18),cursor='hand2',borderwidth=1,relief='ridge')
        auqCarryBtn=Button(self.SignFrame,text='AC',font=('Times',18),cursor='hand2',borderwidth=1,relief='ridge')
        Empty2=Button(self.SignFrame,text='',font=('Times',18),cursor='hand2',borderwidth=1,relief='ridge')
        parityBtn=Button(self.SignFrame,text='P',font=('Times',18),cursor='hand2',borderwidth=1,relief='ridge')
        Empty3=Button(self.SignFrame,text='',font=('Times',18),cursor='hand2',borderwidth=1,relief='ridge')
        carryBtn=Button(self.SignFrame,text='CY',font=('Times',18),cursor='hand2',borderwidth=1,relief='ridge')
        
        signBtn.place(relx=.01,rely=.03,relwidth=.1,relheight=.4)
        zeroBtn.place(relx=.1,rely=.03,relwidth=.1,relheight=.4)
        Empty1.place(relx=.19,rely=.03,relwidth=.1,relheight=.4)
        auqCarryBtn.place(relx=.28,rely=.03,relwidth=.1,relheight=.4)
        Empty2.place(relx=.37,rely=.03,relwidth=.1,relheight=.4)
        parityBtn.place(relx=.46,rely=.03,relwidth=.1,relheight=.4)
        Empty3.place(relx=.55,rely=.03,relwidth=.1,relheight=.4)
        carryBtn.place(relx=.64,rely=.03,relwidth=.1,relheight=.4)

        



app=simulator()
app.interpreterObj.simulatorObj.register[register_index['A']]=23
app.interpreterObj.simulatorObj.register[register_index['B']]=1
app.interpreterObj.simulatorObj.register[register_index['H']]=255
print(app.interpreterObj.simulatorObj.register[register_index['A']])
app.run()