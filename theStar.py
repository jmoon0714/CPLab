from tkinter import *
from tkinter.colorchooser import askcolor
import Neuron
class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()

        self.neuronButton = Button(self.root, text='Neuron', command=self.use_neuron)
        self.neuronButton.grid(row=0, column=0)

        self.synapseButton = Button(self.root, text='Synapse', command=self.use_synapse)
        self.synapseButton.grid(row=0, column=1)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=2)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4)

        self.c = Canvas(self.root, bg='white', width=1000, height=900)
        self.c.grid(row=1, columnspan=5)
    
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

    def use_neuron(self):
        self.activate_button(self.neuronButton)
        print("Neuron currently selected")

    def use_synapse(self):
        self.activate_button(self.synapseButton)
        print("Synapse currently selected")


    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def activate_button(self, some_button):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        
    def build(self, event):
        if self.active_button==self.neuronButton:
            self.buildNeuron(event)
        elif self.active_button==self.synapseButton:
            self.buildSynapse(event)
        self.old_x=event.x
        self.old_y=event.y
        
    def buildNeuron(self,event):
        self.line_width = self.choose_size_button.get()
        currentColor =  self.color
        radius=self.line_width*5
        centerX= event.x
        centerY= event.y
        if self.wouldIntersect(centerX,centerY,radius)==False:
            self.listOfEN.append(EmbeddedNeuron(self.c,centerX, centerY, radius, currentColor,0))
            print("Neuron built")
        else:
            print("Error: Cannot build a neuron in this location. It is too close to another neuron.")
            
    def buildSynapse(self,event):
        if self.synapseHalfBuilt==False:
            where=self.findWhere(event.x,event.y)
            if where!=None:
                self.synapseStart=where
                self.synapseHalfBuilt=True
                self.tempSynapse=EmbeddedSynapse(self.c,self.synapseStart)
            else:
                print("Error: Cannot start synapse outside a neuron")
        
                
    def move(self, event):
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
        if self.active_button==self.synapseButton:
            if self.synapseHalfBuilt:
                where=self.findWhere(event.x,event.y)
                if where!=None and where!=self.tempSynapse.NFrom:
                    self.tempSynapse.setNToAndDraw(where)
                    self.synapseHalfBuilt=False
                    self.listOfES.append(self.tempSynapse)
                    self.tempSynapse=None
                    self.synapseStart=None
                    print("Synapse built")
                else:
                    self.tempSynapse.undraw()
                    self.synapseHalfBuilt=False
                    self.tempSynapse=None
                    self.synapseStart=None

                

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
        
        #(2.0**0.5)
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
        if isinstance(self.synapse, Neuron.Synapse):
            lineWdt= min(self.synapse.weight, self.NFrom.radius*2)
        else:
            lineWdt= 2
        endCircleRadius=EmbeddedSynapse.END_CIRCLE_RADIUS*lineWdt
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
        if isinstance(self.synapse, Neuron.Synapse):
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
            
        
        

if __name__ == '__main__':
    Paint()
