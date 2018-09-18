from tkinter import *
from tkinter.colorchooser import askcolor
import graphicalNeuron as GN
import sys
import time

#%%
class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
    NEURON_TYPES=[GN.Neuron,GN.LIFNeuron,GN.MCPNeuron]
    NEURON_TYPES_STR=["Neuron","LIFNeuron","MCPNeuron"]
    SYNAPSE_TYPES=[GN.Synapse]
    def __init__(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.root.wm_title("Neuron")
        
        self.tkvar = StringVar(self.root)
        self.tkvar.set("Neuron")
        #self.neuronButton = Button(self.root, text='Neuron', command=self.use_neuron)
        #self.neuronButton.grid(row=0, column=0)
        self.neuronButton = OptionMenu(self.root, self.tkvar, *Paint.NEURON_TYPES_STR)
        self.neuronButton.grid(row=0, column=0)
        self.tkvar.trace('w', self.use_neuron)


        self.synapseButton = Button(self.root, text='Synapse', command=self.use_synapse)
        self.synapseButton.grid(row=0, column=1)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=2)
        
        self.quit_button = Button(self.root, text='quit', command=self.root.destroy)
        self.quit_button.grid(row=0, column=6)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4)

        self.c = Canvas(self.root, bg='white', width=1000, height=900)
        self.c.grid(row=1, columnspan=7)
    
        self.setup()
        self.root.mainloop()
        

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.synapseStart = None
        self.synapseHalfBuilt= False
        self.tempSynapse = None
        
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        #self.eraser_on = False
        self.active_button = self.neuronButton
        self.c.bind('<ButtonPress-1>', self.build)
        self.c.bind('<B1-Motion>', self.move)
        self.c.bind('<ButtonRelease-1>', self.drop)
        
        self.listOfEN=[]
        self.listOfES=[]
        
        self.currentParams=None
        self.lastEvent=None
        self.currentClass=Paint.NEURON_TYPES[0]

    def use_neuron(self,*args):
        st=self.tkvar.get()
        
        for i in range(len(Paint.NEURON_TYPES)):
            if Paint.NEURON_TYPES_STR[i]==st:
                self.currentClass=Paint.NEURON_TYPES[i]
        self.activate_button(self.neuronButton)
        print("Neuron currently selected")

    def use_synapse(self):
        self.activate_button(self.synapseButton)
        print("Synapse currently selected")


    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def activate_button(self, some_button):
        self.currentParams=None
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        
    def build(self, event):
        self.lastEvent=event
        if self.active_button==self.neuronButton:
            radius=self.line_width*5
            centerX= event.x
            centerY= event.y
            if self.wouldIntersect(centerX,centerY,radius)==False:
                if(self.currentParams==None):
                    InputTaker(self.currentClass.PARAM_LIST, self.buildNeuron, self.currentClass)
                else:
                    self.buildNeuron(self.currentParams,self.currentClass)
        elif self.active_button==self.synapseButton:
            self.buildESynapse(event)
        self.old_x=event.x
        self.old_y=event.y
        
    def buildNeuron(self,params,cls):
        self.currentParams=params
        p=[]
        for entry in params:
            text  = entry
            try:
                text=int(text)
            except:
                try:
                    text=float(text)
                except:
                    text=text
            p.append(text)
        neuron=cls.arrayConstruct(p)
        self.buildENeuron(self.lastEvent,neuron)
        
        
    def buildENeuron(self,event,neuron):
        self.line_width = self.choose_size_button.get()
        currentColor =  self.color
        radius=self.line_width*5
        centerX= event.x
        centerY= event.y
        if self.wouldIntersect(centerX,centerY,radius)==False:
            self.listOfEN.append(EmbeddedNeuron(self.c,centerX, centerY, radius, currentColor,neuron))
            print("Neuron built")
        else:
            print("Error: Cannot build a neuron in this location. It is too close to another neuron.")
            
    def buildESynapse(self,event):
        if self.synapseHalfBuilt==False:
            where=self.findWhere(event.x,event.y)
            if where!=None:
                self.synapseStart=where
                self.synapseHalfBuilt=True
                self.tempSynapse=EmbeddedSynapse(self.c,self.synapseStart)
            else:
                print("Error: Cannot start synapse outside a neuron")
        
                
    def move(self, event):
        self.lastEvent=event
        where=self.findWhere(self.old_x,self.old_y)
        if self.active_button==self.neuronButton:
            if where!=None:
                if self.wouldIntersect(event.x,event.y,where.radius,exception=where)==False:
                    where.redraw(event.x,event.y)
                else:
                    print("Error: Cannot move nueron to this location. It is too close to another neuron.")
        
        elif self.synapseHalfBuilt==True:
            self.tempSynapse.drawTemp(event.x,event.y)
        self.old_x=event.x
        self.old_y=event.y


        
    def drop(self, event):
        self.lastEvent=event
        if self.active_button==self.synapseButton:
            if self.synapseHalfBuilt:
                where=self.findWhere(event.x,event.y)
                if where!=None and where!=self.tempSynapse.NFrom:
                    self.synapseEnd=where
                    if(self.currentParams==None):
                        InputTaker(GN.Synapse.PARAM_LIST, self.buildSynapse, GN.Synapse)
                    else:
                        self.buildSynapse(self.currentParams,GN.Synapse)
                else:
                    self.tempSynapse.undraw()
                    self.synapseHalfBuilt=False
                    self.tempSynapse=None
                    self.synapseStart=None

    def buildSynapse(self,params,cls):
        self.currentParams=params
        p=[self.synapseStart.neuron,self.synapseEnd.neuron]
        for entry in params:
            text  = entry
            try:
                text=int(text)
            except:
                try:
                    text=float(text)
                except:
                    text=text
            p.append(text)
        self.tempSynapse.setSynapse(cls.arrayConstruct(p))
        self.tempSynapse.setNToAndDraw(self.synapseEnd)
        self.synapseHalfBuilt=False
        self.listOfES.append(self.tempSynapse)
        self.tempSynapse=None
        self.synapseStart=None
        print("Synapse built")
        
                

    def reset(self, event):
        self.old_x, self.old_y = None, None
    
    def findWhere(self, x,y):
        for i in range(len(self.listOfEN)):
            if self.listOfEN[i].checkIfInside(x,y):
                return self.listOfEN[i]
        return None
    
    def wouldIntersect(self, x,y,r,exception=None):
        for i in range(len(self.listOfEN)):
            if self.listOfEN[i]!=exception and self.listOfEN[i].checkIntersect(x,y,r):
                return True
        return False
    
    
#%%    
class InputTaker(object):
    def __init__(self, params, function, cls):
        self.function=function
        self.cls=cls
        self.root = Tk()
        self.root.wm_title("InputTaker")
        Label(self.root, text="Input Parameters.").pack()
        ents = self.makeform(self.root, params)
        #self.root.bind('<Return>', (lambda event, e=ents: self.fetch(e)))  
        b1 = Button(self.root, text='Show',\
          command=(lambda e=ents: self.fetch(e)))
        b1.pack(side=LEFT, padx=5, pady=5)
        b2 = Button(self.root, text='Quit', command=self.root.destroy)
        b2.pack(side=LEFT, padx=5, pady=5)
        self.root.mainloop()
        
    def makeform(self,root, fields):
        entries = []
        for field in fields:
            row = Frame(root)
            lab = Label(row, width=15, text=field, anchor='w')
            ent = Entry(row)
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries.append((field, ent))
        return entries

    def fetch(self,entries):
        p=[]
        for entry in entries:
            field = entry[0]
            text  = entry[1].get()
            p.append(text)
            print('%s: "%s"' % (field, text)) 
        self.function(p, self.cls)
        self.root.destroy()
    

    
#%%    
class EmbeddedCanvas(object):
    
    def checkIfInside():
        return False;
    
class EmbeddedNeuron(EmbeddedCanvas):
    def __init__(self, c, centerX, centerY, radius, color, Neuron):
        self.canvas=c
        self.centerX=centerX
        self.centerY=centerY
        self.radius=radius
        self.topLeftX=centerX-(radius)
        self.topLeftY=centerY-(radius)
        self.bottomRightX=centerX+(radius)
        self.bottomRightY=centerY+(radius)
        self.mainColor=color
        
        self.shape=c.create_oval(self.topLeftX,self.topLeftY,self.bottomRightX,self.bottomRightY, outline=self.mainColor, fill=self.mainColor, width=2)
        
        self.synapsesOut=[]
        self.synapsesIn=[]
        
        self.neuron=Neuron

        
    def checkIfInside(self,x,y):
        return (x-self.centerX)**2 + (y-self.centerY)**2 < self.radius**2
    
    def checkIntersect(self,x,y,r):
        return (x-self.centerX)**2 + (y-self.centerY)**2 < (self.radius+r+2)**2
    
    def redraw(self, centerX, centerY):
        self.undraw()
        self.centerX=centerX
        self.centerY=centerY
        self.topLeftX=centerX-(self.radius)
        self.topLeftY=centerY-(self.radius)
        self.bottomRightX=centerX+(self.radius)
        self.bottomRightY=centerY+(self.radius)
        
        self.shape=self.canvas.create_oval(self.topLeftX,self.topLeftY,\
                                           self.bottomRightX,self.bottomRightY, outline=self.mainColor, fill=self.mainColor, width=2)
        for S in self.synapsesOut:
            S.redraw()
        for S in self.synapsesIn:
            S.redraw()
        
    def undraw(self):
        self.canvas.delete(self.shape)
        
class EmbeddedSynapse(EmbeddedCanvas):
    END_CIRCLE_RADIUS=3
    SYNAPTIC_CLEFT_DISTANCE=2
    def __init__(self, c, NFrom, NTo=None, s=None):
        self.canvas=c
        self.NFrom=NFrom
        self.NTo=NTo
        self.shape=None
        self.shapeBulb=None
        self.synapse=s
        
    def setSynapse(self,s):
        self.synapse=s

    def setNToAndDraw(self, NTo):
        self.undraw()
        self.NTo=NTo
        self.redraw()
        if isinstance(self.NFrom, EmbeddedNeuron) and self not in self.NFrom.synapsesOut:
            self.NFrom.synapsesOut.append(self)
        if isinstance(self.NFrom, EmbeddedNeuron) and self not in self.NTo.synapsesIn:
            self.NTo.synapsesIn.append(self)
            
    def redraw(self):
        self.undraw()
        if isinstance(self.synapse, GN.Synapse):
            lineWdt= min(self.synapse.weight, EmbeddedSynapse.END_CIRCLE_RADIUS*2)
        else:
            lineWdt= 2
        endCircleRadius=EmbeddedSynapse.END_CIRCLE_RADIUS*2
        delD=endCircleRadius+EmbeddedSynapse.SYNAPTIC_CLEFT_DISTANCE+self.NTo.radius
        bigD=((self.NFrom.centerX-self.NTo.centerX)**2 + (self.NFrom.centerY-self.NTo.centerY)**2)**0.5
        newEndX=int((((bigD-delD)*self.NTo.centerX) + (delD*self.NFrom.centerX))/bigD)
        newEndY=int((((bigD-delD)*self.NTo.centerY) + (delD*self.NFrom.centerY))/bigD)
        self.shape=self.canvas.create_line(self.NFrom.centerX, self.NFrom.centerY, newEndX, newEndY,\
                                           fill=self.NFrom.mainColor, width=lineWdt)
        
        topLeftX=newEndX-(EmbeddedSynapse.END_CIRCLE_RADIUS)
        topLeftY=newEndY-(EmbeddedSynapse.END_CIRCLE_RADIUS)
        bottomRightX=newEndX+(EmbeddedSynapse.END_CIRCLE_RADIUS)
        bottomRightY=newEndY+(EmbeddedSynapse.END_CIRCLE_RADIUS)
        self.shapeBulb=self.canvas.create_oval(topLeftX,topLeftY,\
                                           bottomRightX,bottomRightY, outline=self.NFrom.mainColor, fill=self.NFrom.mainColor, width=1)
        
    def drawTemp(self, x, y):
        self.undraw()
        if isinstance(self.synapse, GN.Synapse):
            lineWdt= min(self.synapse.weight, self.NFrom.radius*2)
        else:
            lineWdt= 2
        self.shape=self.canvas.create_line(self.NFrom.centerX, self.NFrom.centerY, x, y,\
                                           fill=self.NFrom.mainColor, width=lineWdt)

    def undraw(self):
        if self.shape!=None:
            self.canvas.delete(self.shape)
        if self.shapeBulb!=None:
            self.canvas.delete(self.shapeBulb)
            
#%%        
        

if __name__ == '__main__':
    Paint()
    print("mainExit")
    
