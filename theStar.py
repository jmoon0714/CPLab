from tkinter import *
from tkinter.colorchooser import askcolor
import graphicalNeuron as GN
import sys
import time
import threading

#%%
class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = "#000000"
    NEURON_TYPES=[GN.Neuron,GN.LIFNeuron,GN.MCPNeuron]
    NEURON_TYPES_STR=["Neuron","LIFNeuron","MCPNeuron"]
    SYNAPSE_TYPES=[GN.Synapse]
    
    """Class Variables:
    Tkinter variables
        "root": the tkinter mainframe
        "tkvar": The variable that the Neuron drop down is set to, which changes the current neuron selected
        "neuronButton": the dropdown that chooses a neuron. also selects neuron. 
        "synapseButton": the button that chooses a synapse. 
        "colorButton": the button to choose the color of next neurons.
        "quitButton": the button that terminates the program and closes the window
        "choose_size_button": the slider that lets you choose a tool size
        "c": the canvas on which items are drawn
    Event Locations
        "old_x", "old_y": the location the cursor was at the last time a event was triggered
        "lastEvent": a pointer to the last event
    Synapse Construction
        "synapseStart": Usually null. when a synapse is in the process of being build, points to the neuron where it starts.
        "synapseHaldBuilt": true iff a synapse is in the process of being built.
        "tempSynapse": Usually null. when a synapse is in the process of being build, points to the half built synapse.
    Current Selections
        "line_width": the current tool size
        "color": the current color selected
        "activeButton": the current active button
    Objects contained
        "listOfEN": A list of all the embeddedNeurons currently built
        "listOfES": A list of all the embedded  synapses currently built
    Parametric construction details
        "currentParams": A store of set parameters (for repeated same param constructions)
        "currentClass": The class of object that can currently be built
    """
    
    """Paint Constructor.
    Builds a window where you can build neural nets
    """
    def __init__(self):
        global simulator
        simulator= GUISimulator(self,1,40)
        self.root = Tk()    
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)
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
        
        
        self.run_button = Button(self.root, text='Run', command=self.run)
        self.run_button.grid(row=0, column=6)
        
        self.quit_button = Button(self.root, text='quit', command=self.destroy)
        self.quit_button.grid(row=0, column=7)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4)

        self.c = Canvas(self.root, bg='white', width=1000, height=900)
        self.c.grid(row=1, columnspan=8)
    
        self.setup()
        self.root.mainloop()
        
        
    """Helper function to the constructor"""
    def setup(self):
        self.old_x = None
        self.old_y = None
        self.lastEvent=None

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
        self.currentClass=Paint.NEURON_TYPES[0]
        
    def destroy(self):
        Paint.root.destroy()
        simulator.terminate()
        sys.exit()

    def run(self):
        mt=threading.Thread(target=simulator.main)
        mt.start()
        
    """"
        Called when the user selects a new Neuron
        Allocates currentClass to the selected class
        sets active_button to neuronButton
    
    """
    def use_neuron(self,*args):
        st=self.tkvar.get()
        
        for i in range(len(Paint.NEURON_TYPES)):
            if Paint.NEURON_TYPES_STR[i]==st:
                self.currentClass=Paint.NEURON_TYPES[i]
        self.activate_button(self.neuronButton)
        print("Neuron currently selected")

    """"
        Called when the user selects Synapse
        sets active_button to synapseButton
    
    """
    def use_synapse(self):
        self.activate_button(self.synapseButton)
        print("Synapse currently selected")

    """
        displays a window that lets the user choose a color
    """
    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    """
        Implements visual changes for when a button is activated
    """
    def activate_button(self, some_button):
        self.currentParams=None
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        
    """Called when the user left clicks on the canvas
        Looks at the current parameters and initiates the building process accordingly
        If there are no current params, displays a input screen
    """
    def build(self, event):
        self.lastEvent=event
        if self.active_button==self.neuronButton:
            radius=self.line_width*5
            centerX= event.x
            centerY= event.y
            if self.wouldIntersect(centerX,centerY,radius)==False:
                if(self.currentParams==None):
                    InputTaker(self.buildNeuron, self.currentClass)
                else:
                    self.buildNeuron(self.currentParams,self.currentClass)
        elif self.active_button==self.synapseButton:
            self.buildESynapse(event)
        self.old_x=event.x
        self.old_y=event.y
        
    """
        constructs a GN.Neuron object and uses it to build an EmbeddedNeuron
    """
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
        simulator.addNeuron(neuron)
        self.buildENeuron(self.lastEvent,neuron)
        
    """
        Builds an EmbeddedNeuron at where the mouse was clicked, based on the toolSize and current color
    """
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
            
    """starts the proccess of building a synapse
        sets synapseHalfBuild to True
        links the first neuron up
    """
    def buildESynapse(self,event):
        if self.synapseHalfBuilt==False:
            where=self.findWhere(event.x,event.y)
            if where!=None:
                self.synapseStart=where
                self.synapseHalfBuilt=True
                self.tempSynapse=EmbeddedSynapse(self.c,self.synapseStart)
            else:
                print("Error: Cannot start synapse outside a neuron")
        
    """Click and drag a neuron around, or if synapseHalfBuilt is true, move a synapse end point around"""
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


    """
        If synapseHalfBuilt is true, it tries to build a synapse depending on drop location. 
        if currentparameters is none, opens a input window
    """
    def drop(self, event):
        self.lastEvent=event
        if self.active_button==self.synapseButton:
            if self.synapseHalfBuilt:
                where=self.findWhere(event.x,event.y)
                if where!=None and where!=self.tempSynapse.NFrom:
                    self.synapseEnd=where
                    if(self.currentParams==None):
                        InputTaker(self.buildSynapse, GN.Synapse)
                    else:
                        self.buildSynapse(self.currentParams,GN.Synapse)
                else:
                    self.tempSynapse.undraw()
                    self.synapseHalfBuilt=False
                    self.tempSynapse=None
                    self.synapseStart=None

    """
        Builds a GN.Synapse object which is used to build the embedded synapse
    """
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
        simulator.addSynapse(self.tempSynapse.synapse)
        self.tempSynapse.setNToAndDraw(self.synapseEnd)
        self.synapseHalfBuilt=False
        self.listOfES.append(self.tempSynapse)
        self.tempSynapse=None
        self.synapseStart=None
        print("Synapse built")
        
    """If the cursor is in a neuron returns that neuron
        else returns None
    """
    def findWhere(self, x,y):
        for i in range(len(self.listOfEN)):
            if self.listOfEN[i].checkIfInside(x,y):
                return self.listOfEN[i]
        return None
    
    """
        returns true if a neuron built at this location would intersect another neuron
    """
    def wouldIntersect(self, x,y,r,exception=None):
        for i in range(len(self.listOfEN)):
            if self.listOfEN[i]!=exception and self.listOfEN[i].checkIntersect(x,y,r):
                return True
        return False
    
    
#%%    
class InputTaker(object):
    def __init__(self, function, cls):
        """
        Class Variables:
            "function": a refrence to the function that is called when go is clicked
            "cls": the class of the object that "function will build"
            "root": The Tkinter root that takes the inputs
        """
        params=cls.PARAM_LIST
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
        
    """
    Builds the input locations, based on fields
    """
    def makeform(self,root, fields):
        defaults=self.cls.PARAM_DEFAULTS
        entries = []
        i=0
        for field in fields:
            row = Frame(root)
            lab = Label(row, width=15, text=field, anchor='w')
            try:
                default=defaults[i]
            except:
                default=""
            v = StringVar(root, value=default)
            ent = Entry(row, textvariable=v)
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries.append((field, ent))
            i=i+1
        return entries

    """Collects the inputs and sends them to self.function"""
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
    """
    Class Variables:
    Tkinter:
        "canvas": The canvas where self is drawn
        "mainColor": The color of self
        "shape": The circle that represents this neuron
    Dimentions:
        "centerX": The X coord of center where this neuron will be drawn.cs 
        "centerY": The Y coord of center where this neuron will be drawn. 
        "radius": The radius of this Neuron
        "topLeftX": The X coord of the point that would be at the top left of a 
            quadrilateral that enclosed the circle
        "topLeftY": The Y coord of the point that would be at the top left of a 
            quadrilateral that enclosed the circle
        "bottomRightX": The X coord of the point that would be at the bottom right of a 
            quadrilateral that enclosed the circle
        "bottomRightY": The Y coord of the point that would be at the bottom right of a 
            quadrilateral that enclosed the circle
    Neuron Details:
        "synapsesOut": a list of embedded synapses that leave this neuron
        "synapseIn": a list of embedded synapses to this neuron

        
    """
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

    """Checks if a point is inside this neuron"""
    def checkIfInside(self,x,y):
        return (x-self.centerX)**2 + (y-self.centerY)**2 < self.radius**2
    
    """checks if a circle would intersect this neuron"""
    def checkIntersect(self,x,y,r):
        return (x-self.centerX)**2 + (y-self.centerY)**2 < (self.radius+r+2)**2
    
    """redraws this neuron to a new Center"""
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
        
    """Erases this neuron"""
    def undraw(self):
        self.canvas.delete(self.shape)
        
class EmbeddedSynapse(EmbeddedCanvas):
    END_CIRCLE_RADIUS=3
    SYNAPTIC_CLEFT_DISTANCE=2
    """Class Variables
    Statics:
        "END_CIRCLE_RADIUS": the radius of the circle at the end of a synapse
        "SYNAPTIC_CLEFT_DISTANCE": the distance between the end of a synapse and the next neuron
    Tkinter: 
        "canvas": The canvas this synapse is drawn on
        "shape": A refrence to the line that represents the axon
        "shapeBulb": a refrence to teh circle representing the end of a synapse
    Synapse Details:
        "synapse": A refrence to the synapse self represents
        "NTo": The embeddedNeuron this synapse is going to
        "NFrom": The embeddedNeuron this synapse comes from
        
    """
    def __init__(self, c, NFrom, NTo=None, s=None):
        self.canvas=c
        self.NFrom=NFrom
        self.NTo=NTo
        self.shape=None
        self.shapeBulb=None
        self.synapse=s
        self.shapePulses=[]
        self.shapeBulbFire=None
        
    """sets self.synapse to s"""
    def setSynapse(self,s):
        self.synapse=s

    """Sets self.NTo to NTo, and then draws the completed synapse to that EmbeddedNeuron"""
    def setNToAndDraw(self, NTo):
        self.undraw()
        self.NTo=NTo
        self.redraw()
        if isinstance(self.NFrom, EmbeddedNeuron) and self not in self.NFrom.synapsesOut:
            self.NFrom.synapsesOut.append(self)
        if isinstance(self.NFrom, EmbeddedNeuron) and self not in self.NTo.synapsesIn:
            self.NTo.synapsesIn.append(self)
            
    """redraws this synapse. takes into account changes in the locations of self.NTo and self.NFrom, and the synaptic weight"""
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
    
    """draws a line to help in building synapses. stars an self.NFrom"""
    def drawTemp(self, x, y):
        self.undraw()
        if isinstance(self.synapse, GN.Synapse):
            lineWdt= min(self.synapse.weight, self.NFrom.radius*2)
        else:
            lineWdt= 2
        self.shape=self.canvas.create_line(self.NFrom.centerX, self.NFrom.centerY, x, y,\
                                           fill=self.NFrom.mainColor, width=lineWdt)
        
    """erases all currently drawn pulses
    checks if there are pulses to draw and draws them
    """
    def drawAllPulses(self):
        self.undrawPulses()
        if isinstance(self.synapse, GN.Synapse):
            lineWdt= min(self.synapse.weight, self.NFrom.radius*2)
        else:
            return
        activeDelays=self.synapse.activateFireDelays
        print(activeDelays)
        delay=self.synapse.delay
        for i in range(len(activeDelays)):
            self.drawPulse(delay-activeDelays[i], lineWdt)
            
        
    """
    draws a red line that is a part of the axon. this signifies where the pulse is along the axon
    t indicates the location of the pulse. 0<=t<self.synapse.delay
    if the pulse is at the end of the axon, also turns the bulb red
    """
    def drawPulse(self,t, wdt):
        
        endCircleRadius=EmbeddedSynapse.END_CIRCLE_RADIUS*2
        delD=endCircleRadius+EmbeddedSynapse.SYNAPTIC_CLEFT_DISTANCE+self.NTo.radius
        bigD=((self.NFrom.centerX-self.NTo.centerX)**2 + (self.NFrom.centerY-self.NTo.centerY)**2)**0.5
        newEndX=int((((bigD-delD)*self.NTo.centerX) + (delD*self.NFrom.centerX))/bigD)
        newEndY=int((((bigD-delD)*self.NTo.centerY) + (delD*self.NFrom.centerY))/bigD)
        
        
        x1=(t*newEndX + (self.synapse.delay - t)* self.NFrom.centerX )/self.synapse.delay
        y1=(t*newEndY + (self.synapse.delay - t)* self.NFrom.centerY )/self.synapse.delay
        x2=((t+1)*newEndX + (self.synapse.delay - t - 1)* self.NFrom.centerX )/self.synapse.delay
        y2=((t+1)*newEndY + (self.synapse.delay - t - 1)* self.NFrom.centerY )/self.synapse.delay
        print("coords ",x1," ",y1," ",x2," ",y2)
        temp=self.canvas.create_line(x1, y1, x2, y2,\
                                           fill=get_N_foreground_color(self.NFrom.mainColor), width=wdt)
        if x2==newEndX and y2==newEndY:
            coords=self.canvas.coords(self.shapeBulb)
            self.shapeBulbFire=self.canvas.create_oval(coords[0],coords[1],\
                                           coords[2],coords[3], outline=self.NFrom.mainColor, fill="red", width=1)
        self.shapePulses.append(temp)
        
    """
    Earses all currently drawn pulses
    """
    def undrawPulses(self):
        for p in self.shapePulses:
            self.canvas.delete(p)
        if self.shapeBulbFire!=None:
            self.canvas.delete(self.shapeBulbFire)
        self.shapeBulbFire=None
        self.shapePulses=[]

    """erases the entire synapse from the canvas"""
    def undraw(self):
        if self.shape!=None:
            self.canvas.delete(self.shape)
        if self.shapeBulb!=None:
            self.canvas.delete(self.shapeBulb)
            
#%%
            
class GUISimulator(GN.Simulator):
    def __init__(self,Paint2, t, finalT):
        super(GUISimulator, self).__init__(t=t, finalT=finalT)
        global Paint
        Paint=Paint2
        
    def main(self):
        self.appendInput(4,Paint.listOfEN[0].neuron,1)
        super(GUISimulator, self).main(useDelay=True)
        
        
    def runOneTimeStep(self, currentTau):
        super(GUISimulator, self).runOneTimeStep(currentTau=currentTau)
        for aESynapse in Paint.listOfES:
            aESynapse.drawAllPulses()
        
    def terminate(self):
        sys.exit()


def get_N_foreground_color(color):
    print(color)
    color=color[1:]
    each=int(len(color)/3)
    print(each)
    r=color[:-2*each]
    g=color[each:-each]
    b=color[-each:]
    string_list=["#"]
    string_list.append(hex_incr(r,100))
    string_list.append(hex_incr(g,100))
    string_list.append(hex_incr(b,100))
    
    return string_list[0]+string_list[1]+string_list[2]+string_list[3]
        
def hex_incr (c, add):
    l=len(c)
    print("len",l)
    n=int(c,16)
    print("int",n)
    n=n+add
    s=hex(n)
    s=s[2:]
    s="000"+s
    print("hex",s)
    return s[len(s)-l:]
    
    
#%%        
        

if __name__ == '__main__':
    Paint()
    print("mainExit")
    
