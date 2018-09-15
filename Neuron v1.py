
#from random import *
import random
from graphics import *
import matplotlib
import numpy
import time
import math

#%%
class Neuron(object):

    """ Class Invariant: 
    (float) "threshold": threshold voltage of the neuron; default initialized 
        to 1.
    (float) "voltage": current voltage of the neuron; default initialized to 0.
    ([(Synapse)]) "postSynapses": list of synapses to which the neuron is 
        sending output.
    ([(Synapse)]) "preSynapses": list of synapses to which the neuron is 
        receiving input.
    (float) "sumInputs": sum of inputs at a  time step before leaking.
    (int) "lastTau": last time this neuron was checked by simulation in terms 
        of tau.
    (Simulator) "simulator": the corresponding simulator that uses this neuron.
    (boolean) "toBeChecked": True if the "neuronCheckList" in Simulator comtains 
        self; else false; removes the necessity to use inneficient contains().
    (int) "refractory": is the set refractory period of the neuron in tau; 
        default initialized to 1; Greater than zero.
    (int) "refractCount": is the refractory time left since this neuron last 
        fired. Must be between 0 and "refractory", inclusive.
    """
    
    def __init__(self, sim, v= 0, theta= 1, refractory= 1): 
        """ Precondition:
            (Simulator) "sim": an instance of Simulator that uses this neuron.
            (float) "v": initial voltage; by default, "v" is initialized to 0.
            (float) "theta": this neuron's threshold; by default, "theta" is 
                initialized to 1.
            (int) "refractory": how many time steps the neuron is inactive for;
                by default, "refractory" is initialized to 1.
            
            1) "simulator," "voltage," "threshold," and "refractory" is 
                initialized by parameters. A variable called "refractCount" is 
                initialized to 0, which has "refractory" amount of time steps 
                before this neuron can fire again. Moreover, if the threshold 
                is initialized to be less than the initial voltage, then the 
                neuron is added to the "neuronCheckList" in Simulator.
            
            2) Also, each neuron holds two lists, "postSynapses" and 
                "preSynapses," which store instances of Synapse, representing 
                the synapses on the axon and dendrites of this neuron.
            
            3) Each neuron holds a boolean value called "toBeChecked", which is 
                changed to True when appended onto the "neuronCheckList" in 
                Simulator.
            
            4) Each neuron has instances of monitors, "voltageMonitor" and
                "spikeMonitor"; the former tracks the voltage over time, and 
                the latter tracks the spikes over time.
        """
        self.threshold= theta
        self.voltage= v
        self.postSynapses= []
        self.preSynapses= []
        self.sumInputs= 0
        self.lastTau= 0     #changed from -1 to 0
        self.simulator= sim
        self.simulator.construct(self)#changed
        self.toBeChecked= False   #new variable
        self.refractory= refractory
        self.refractCount= 0
        if(self.voltage>= self.threshold):
            self.simulator.neuronCheckList.append(self)
            self.toBeChecked=True 
        self.voltageMonitor= VoltageMonitor(self)
        self.spikeMonitor= SpikeMonitor(self)
        self.voltageMonitor.appendCritical(0, v)
        
    def getPreSynapses(self):
        """ Returns "preSynapses".
        """
        return self.preSynapses
    
    def getPostSynapses(self):
        """ Returns "postSynapses".
        """
        return self.postSynapses
            
    def getThreshold(self):
        """ Return "threshold". 
        """
        return self.threshold
    
    def getNeuronList(self):
        """ Return an array whose only element is this neuron.
        """
        temp= []
        temp.append(self)
        return temp
        
    def getNextVoltage(self, v):
        """ Precondition: 
            (float) "v": a voltage at a certain time step
            Returns the voltage of neuron at the next time step.
            ** Overridden by LIFNeuron which will return the decayed voltage
        """
        return v
    
    def setVoltage(self,v):
        """ Precondition: 
            (float) "v": desired voltage of the neuron.
            Sets voltage to "v".
        """
        self.voltage= v
    
    def Group(self, N= 1):
        """ Precondition: 
            (int) "N": the number of neurons desired in the new NeuronGroup; by 
                default, "N" is initialized to 1.
            Returns an instance of NeuronGroup with "N" number of neurons.
            
        
        """
        self.simulator.deconstruct(self)
        temp= NeuronGroup(self, N)
        return temp
    
    def transmit(self, synapse):
        """ Precondition:
            (Synapse) "synapse": in the presynapses list
            analogous to Releasing transmitter onto the neuron object
        """
        self.addVoltage(synapse.weight)
    
    def addVoltage(self, v):
        """ Precondition:
            (float) "v": adds "v" to sumInputs.
            If this neuron is not in simulator "neuronCheckList", adds it to 
                 that list.
        """
        self.sumInputs += v
        if(not self.toBeChecked):
            self.simulator.neuronCheckList.append(self)
            self.toBeChecked=True #maybe make a function to implement these three lines
    
    def setThreshold(self, theta):
        """ Precondition:
            (float) "theta": desired threshold of the neuron 
            Set 
        """
        self.threshold= theta
    
    def AP(self):
        """ activates of of this neurons postSynapses """
        for synapse in self.postSynapses:
        		synapse.activate()
                
    def check(self, currentTau):
        """ called by simulator
        adds all the previously incoming inputs
        if voltage>=threshold calls AP() and reduces the voltage by threshold
        else removes this neuron from simulators neuronCheckList
        """
        self.voltage+= self.sumInputs
        self.sumInputs= 0
        self.refractCount-= (currentTau-self.lastTau)
        self.voltageMonitor.appendCritical(currentTau,self.voltage)
        if(self.refractCount<= 0):
            self.refractCount= 0        #moved here, no change 
            if(self.voltage>= self.threshold):
                self.spikeMonitor.appendCritical(currentTau)
                self.AP()
                self.voltage-= abs(self.threshold)
                self.refractCount= self.refractory
                print("AP at "+ str(currentTau) + " at " + str(self))
                self.lastTau= currentTau
                return True
            elif(self.threshold>0):     #never remove a "not neuron" from checklist
                self.simulator.neuronCheckList.remove(self)
                self.toBeChecked= False  #maybe make a function to implement these two lines
        self.lastTau= currentTau
        return False
    
    def copyNeuron(self, neuron):
        """ Precondition:
            (Neuron) "neuron": instance of Neuron
            
            1) Updates this instance of the Neuron to be identical to the 
                neuron passed in as a parameter
            2) If the parameter "neuron" is ready to fire an action potential, 
            this neuron will too be prepared to fire an action potential.
        """
        self.threshold= neuron.threshold
        self.voltage= neuron.voltage
        self.postSynapses= neuron.postSynapses[:]
        self.preSynapses= neuron.preSynapses[:]
        self.refractory= neuron.refractory
        self.lastTau= neuron.lastTau
        self.refractCount= neuron.refractCount
        if(self.voltage>= self.threshold):
            self.simulator.neuronCheckList.append(self)
            self.toBeChecked=True
    
    
    def plotVoltage(self):
        """ plot voltage as a function of time """
        self.voltageMonitor.plot()
        
    def plotSpikes(self):
        """ plot spikes as a function of time """
        self.spikeMonitor.plot()
    
class LIFNeuron(Neuron):
    """ Class Invariant: 
    Inherits Neuron
    (float) decayConstant: variable that determines the rate of leakiness
    """
    
    def __init__(self, sim, v= 0, theta= 1, refractory= 1, d= 5): 
        """ Precondition:
        (Simulator) sim: instance of Simulator class
        (float) v: must be a float
        (float) theta: must be a float
        (float) d: real number greater than or equal to one.
        """
        super().__init__(sim, v, theta, refractory)
        self.decayConstant= d
        
    def leak(self, currentTau):
        """ calculates the desired leak in the neuron """
        #if(self.lastTau != 0):      #removed
        self.voltage= self.voltage*((1-(1/self.decayConstant))**(currentTau-self.lastTau))
    		
    def check(self, currentTau):
        """ called by simulator
        calculates the leak from the last check call
        adds all the previously incoming inputs
        if voltage>=threshold calls AP() and reduces the voltage by threshold
        else removes this neuron from simulators neuronCheckList
        """
        self.leak(currentTau)
        return super().check(currentTau)	
        
    def getNextVoltage(self,v):
        return v*((1-(1/self.decayConstant)))

    def copyNeuron(self, neuron):
        super().copyNeuron(neuron)
        self.decayConstant= neuron.decayConstant

class MCPNeuron(LIFNeuron): 
    """ Class Invariant:
    Inherits Neuron
    Essentially the same as a normal neuron as a MCP is a the most basic All-Or-Nothing neuron
    """
    
    def __init__(self, sim, v= 0, theta= 1, refractory=1):
        """ Precondition:
        (Simulator) sim: instance of Simulator class
        (float) v: must be a float
        (float) theta: must be a float
        """
        super().__init__(sim, v, theta, refractory, d= 1)

#%%
class Synapse(object):
    """ Class Invariant:
          (Neuron) pre: The Neuron instance from which this Synapse is activated. 
              Must be defined in the constructor and is final.
          (Neuron) post: The Neuron instance which this Synapse affects. 
              Must be defined in the constructor and is final.
          (float) weight: The amount this Synapse changes the voltage of neuron2.
          (int) delay: The number of tau's necessary for the synapse to fire
          ([(int)]) activePhase: The list of AP coming through this synapse; 
              each element shouldn't exceed delay in terms of tau; greater than 0;
          	element gets popped off when equal to 0*tau
          (Simulator) simulator: the corresponding simulator that uses this neuron
          (boolean) toBeChecked: True if the simulator check list comtains self; else false;
              removes the necessity to use inneficient contains()  
    """

    	
    def __init__(self, sim, neuron1, neuron2, weight=1, d=1):
        """ Precondition:
        (Neuron) neuron1: instance of Neuron.
        (Neuron) neuron2: instance of Neuron.
        (float) weight: Any floating point number.
        (int) d: Must be an integer 
        """
        self.pre= neuron1
        self.post= neuron2
        self.weight= weight
        self.delay= d
        self.activePhase= []
        self.simulator= sim
        self.toBeChecked=False   #new variable
        self.pre.getPostSynapses().append(self)
        self.post.getPreSynapses().append(self)
        self.simulator.synConstruct(self)
        
    def getPre(self):
        """ returns pre """
        return self.pre
    
    def getPost(self):
        """ returns post """
        return self.post
        
    def activate(self):
        """ appends delat to activePhase
        if self is not contained in simulators synapseCheckList, adds it there
        """
        self.activePhase.append(self.delay)
        if(not self.toBeChecked):
            self.simulator.synapseCheckList.append(self)
            self.toBeChecked=True   #maybe make a function to implement these three lines
    
    def fire(self):
        """ fires the synapse which affects post's voltage """
        self.post.transmit(self)
            
    def check(self, currentTau):
        """ decrements all of activePhase by 1; 
        when one of activePhase is 0, removes it from the activePhase and calls fire
        if activePhase is empty, removes self from simulator's synapseCheckList
        """
        self.activePhase=[x-1 for x in self.activePhase]
        self.checkHelper()
        
    def checkHelper(self):
        if(len(self.activePhase)==0):
            self.simulator.synapseCheckList.remove(self)  
            self.toBeChecked= False    #maybe make a function to implement these two lines
        elif(self.activePhase[0]<=0):
            self.activePhase.pop(0)
            self.fire()
            self.checkHelper()
            
    @classmethod
    def connect(cls, sim, A, B, weight=1, d=1):
        l1=A.getNeuronList()
        l2=B.getNeuronList()
        for i in l1:
            for j in l2:
                cls(sim,i,j,weight,d) 
    
    @classmethod        
    def randomConnect(cls, sim, A, B, weight=1, d=1, probability=0.5):
        l1= A.getNeuronList()
        l2= B.getNeuronList()
        for i in l1:
            for j in l2:
                if(random.random()<probability):
                    cls(sim,i,j,weight,d) 
                    
    @classmethod
    def randomWeightConnect(cls, sim, A, B, minWeight=-1, maxWeight= 1, d= 1):
        l1= A.getNeuronList()
        l2= B.getNeuronList()
        for i in l1:
            for j in l2:
                weight= (random.random() * (maxWeight-minWeight)) + minWeight
                cls(sim,i,j,weight,d) 
                
    @classmethod
    def randomWeightRandomConnect(cls, sim, A, B, minWeight= -1, maxWeight= 1,
                                  d= 1, probability= 0.5):
        l1= A.getNeuronList()
        l2= B.getNeuronList()
        for i in l1:
            for j in l2:
                if(random.random()< probability):
                    weight= (random.random() * (maxWeight - minWeight)) + minWeight
                    cls(sim, i, j, weight, d)
                    
    @classmethod
    def connectWeightedByDistance(cls, sim, A, B, minWeight= 0, maxWeight= 1, 
                                  spread= -1, d= 1):
        l1= A.getNeuronList()
        l2= B.getNeuronList()
        translate1= -len(l1)/2
        translate2= -len(l2)/2
        for i in range(len(l1)):
            for j in range(len(l2)):
                distance= abs((i + translate1) - (j + translate2))
                if(spread== -1 or distance<= spread):
                    cls(sim, l1[i], l2[j], ((maxWeight - minWeight)/(distance + 1)) + minWeight, d)
            

#%%
class Simulator(object):
    """ Class invariant:
        ([(Synapse)]) synapseCheckList: list of synapses to be checked in the next tau
        ([(Neuron)]) neuronCheckList: list of neurons to be checked in the next tau
        (float) tau: minimum timestep. All time is in unit tau
        (int) finalTau: the last time (in tau) we care about
        ([([(int)][(Neuron)][(float)])]) masterInput: 2 dimensional array 3*n that 
        		stores info about when to stimulate which neuron with what voltage
        (int) pointer: points to where in masterInput Simulator is.
    """
    def __init__(self, t= 1, finalT= 10000000):
        """ Precondition:
    		(float) t: positive number.
        (int) finalT: positive integer.
        """
        self.synapseCheckList=[]
        self.neuronCheckList=[]
        self.tau=t
        self.finalTau=finalT
        self.masterInput= []
        temp1= []
        temp2= []
        temp3= []
        self.masterInput.append(temp1)
        self.masterInput.append(temp2)
        self.masterInput.append(temp3)        
        self.pointer=0


    def appendInput(self, t, NG, v):
        """ Precondition:
        (int) t: nonnegative integer
        (NeuronGroup) NG: instance of NeuronGroup class
        (float) v: boolean value
        """
        for n in NG.getNeuronList():
            self.appendInput1(t, n, v)
    

    def appendInput1(self, t, n, v):
        """ Precondition:
        (int) t: nonnegative integer
        (Neuron) n: instance of Neuron class
        (float) v: boolean value
        prepares a neuron to have added voltage at certain time
        """
        
        tempCounter= 0
        isAdded= False
        for time2 in self.masterInput[0]:
            if(t< time2): 
                self.masterInput[0].insert(tempCounter, t)
                self.masterInput[1].insert(tempCounter, n)
                self.masterInput[2].insert(tempCounter, v)
                isAdded= True
                break
            tempCounter+= 1
				
        if (not isAdded):
            self.masterInput[0].insert(tempCounter, t)
            self.masterInput[1].insert(tempCounter, n)
            self.masterInput[2].insert(tempCounter, v)


    def construct(self,ob):
        """does nothing, to be overriden"""
        pass
    
    def deconstruct(self,ob):
        """does nothing, to be overriden"""
        pass
    
    def synConstruct(self,ob):
        """does nothing, to be overriden"""
        pass

    def main(self):
        """ runs a loop through all instants of tau """
        for currentTau in range(0,self.finalTau):
            print(currentTau)
            self.runNotification(currentTau)
            if(currentTau!= 0 and \
               len(self.synapseCheckList)==0 and \
               len(self.neuronCheckList)==0 and \
               self.pointer== len(self.masterInput[0])):
                self.finalTau=currentTau+5
                break
        
    def runNotification(self,currentTau):
        """ inputs user data at currentTau and checks all the synapses
        and neurons that are to be checked """
        while(self.pointer<len(self.masterInput[0]) and\
              currentTau==self.masterInput[0][self.pointer]):
            self.masterInput[1][self.pointer].\
            addVoltage(self.masterInput[2][self.pointer])
            self.pointer+=1
        
        tempSCL=list(self.synapseCheckList)
        for synapsesToCheck in tempSCL:     #temporary list necessary as remove in check messes up the for loop
            synapsesToCheck.check(currentTau)
            
        tempNCL=list(self.neuronCheckList)  #temporary list necessary as remove in check messes up the for loop
        for neuronToCheck in tempNCL:
            neuronToCheck.check(currentTau)
            
    def getFinalTau(self):
        """returns the final Tau"""
        return self.finalTau
    
class GraphicSimulator(Simulator):
    """Class Invariants:
        Inherits Simulator
        ([(Neuron/NeuronGroup)]) constructList: List of the neurons or neuron 
            groups to be drawn. 
        ([([(Neuron)][(graphics.Circle)])]) storageList: List of the drawn neurons,
            and the Circle objects that represent them
        ([([(Synapse)][(graphics.Point)][(graphics.Point)])]) synapseConstList:
            List of drawn Synapses, and the points that are the locations of the
            Neurons that connect them
        (int) l: length of the graphics window
        (int) h: Height of the graphics window
        (graphics.graphWin) win: the graphics window displayed
        (String) locType: way to arrange points

    """
    def __init__(self, t= 1, finalT=10000000,l=1000, h=500, locType=""):
        """Preconditions:
            (float) t: a positve float
            (int) finalT: a nonnegative int
            (int) l: a positive int
            (int) h: a positive int
            (String) locType
        """
        self.constructList=[]
        self.h=h
        self.l=l
        self.storageList=[]
        self.storageList.append([])
        self.storageList.append([])
        self.synapseConstList=[]
        self.synapseConstList.append([])
        self.synapseConstList.append([])
        self.synapseConstList.append([])
        self.locType=locType
        super().__init__(t,finalT)
        
    def construct(self,ob):
        """Precondition: 
            (Neuron/NeuronGroup) ob
            Adds ob to the constructList
        """
        self.constructList.append(ob)
        
    def deconstruct(self,ob):
        """Precondition: 
            (Neuron/NeuronGroup) ob
            removes ob from the constructList
        """
        self.constructList.remove(ob)
        
    def synConstruct(self,ob):
        """Precondition: 
            (Synapse) ob
            Adds ob to synapseConstructList[0]
        """
        self.synapseConstList[0].append(ob)

        
    def makeG(self):
        """Builds graphical representations of all the neurons/NeuronGroups (Circle) 
        and synapses (Line) in constructList and synapseConstructList[0], stores 
        them in storage List and synapseConstructList[1:2] and displays them 
        on the GraphWin win
        """
        count=0
        self.win=GraphWin("Neurons",self.l,self.h+40,autoflush=False)

        for ob in self.constructList:
            if ob not in self.storageList[0]:
                a=ob.getNeuronList()
                ingrp=0
                if len(a)!=1:
                    ingrp=2
                for i in range(len(a)):
                    self.build(a[i],count,ingrp,len(a))
                    if(self.locType!=""):
                        count+=0.3
                    ingrp=1
                count=math.ceil(count)+1
        for i in range(len(self.synapseConstList[0])):
            a=self.synapseConstList[0][i]
            pre=a.getPre()
            post=a.getPost()
            self.synapseConstList[1].append(\
                self.storageList[1][self.storageList[0].index(pre)].getCenter())
            self.synapseConstList[2].append(\
                self.storageList[1][self.storageList[0].index(post)].getCenter())
            l=Line(self.synapseConstList[1][i],self.synapseConstList[2][i])
            if(a.weight<0):
                l.setFill("blue")
            else:
                l.setFill("green")
            l.draw(self.win)
            #l2=Line(Point(math.floor()),self.synapseConstList[2][i])
        for circ in self.storageList[1]:
            circ.setFill("black")
            circ.draw(self.win)
        self.win.update()
        
    def build(self, ob, pt, ingrp=0, l=1):
        """Preconditions:
            (Neuron) ob
            (graphics.Point) pt
            Appends ob and its respective circle to storageList
        """
        self.storageList[0].append(ob)
        if(ingrp==0):
            r=5
        else:
            r=3
        circ=Circle(self.assignLoc(pt, ingrp, l),r)
        self.storageList[1].append(circ)
        
    def main(self):
        """ runs a loop through all instants of tau """
        self.makeG()
        for currentTau in range(0,self.finalTau):
            print(currentTau)
            self.runNotification(currentTau)
            if(currentTau!= 0 and \
               len(self.synapseCheckList)==0 and \
               len(self.neuronCheckList)==0 and \
               self.pointer== len(self.masterInput[0])):
                self.finalTau=currentTau+5
                break
            time.sleep(self.tau)
        
        
    def runNotification(self,currentTau):
        """ inputs user data at currentTau and checks all the synapses 
        and neurons that are to be checked 
        Colors firing Neurons red in win"""
        while(self.pointer<len(self.masterInput[0]) and\
              currentTau==self.masterInput[0][self.pointer]):
            self.masterInput[1][self.pointer].\
            addVoltage(self.masterInput[2][self.pointer])
            self.pointer+=1
        
        tempSCL=list(self.synapseCheckList)
        for synapsesToCheck in tempSCL:     #temporary list necessary as remove in check messes up the for loop
            synapsesToCheck.check(currentTau)
            
        tempNCL=list(self.neuronCheckList)  #temporary list necessary as remove in check messes up the for loop
        for neuronToCheck in tempNCL:
            a=neuronToCheck.check(currentTau)
            if(a):
                c=self.storageList[1][self.storageList[0].index(neuronToCheck)]
                c.setFill("red")
                c.setOutline("red")
            else:
                c=self.storageList[1][self.storageList[0].index(neuronToCheck)]
                c.setFill("black")
                c.setOutline("black")
        self.win.update()

            
    def assignLoc(self,x, ingrp, l):   #TODO (add options)
        """ Precondition
            (int) x: a nonnegative integer
            (boolean) ingrp: is this neuron in a neurongroup
            returns the desired coordinate point of an object, based on locType
        """
        if(self.locType=="linearRandom"):
            y=self.h*random.random()
        elif(self.locType=="random"):
            x=self.l*random.random()/12
            y=self.h*random.random()/1.2
        elif(self.locType=="sinusoidal"):
            y=-1*self.h*math.cos(x)+self.h
        else:
            x*=10
            if(ingrp==2):
                y=0
            elif(ingrp==1):
                y=self.storageList[1][len(self.storageList[1])-1].getCenter().getY()-20+(self.h/l)
            elif(ingrp==0):
                y=self.h*random.random()


            
        return Point(x*10+20,y+20)
        
#%%
class NeuronGroup(object):
    """ Class Invariant:
    (Simulator) simulator: the corresponding simulator that uses this neuron group
    ([(Neuron)]) Neurons: the list of all neurons stored in this neuron group
    """
    def __init__(self, neuron, N):
        """ Precondition:
          (Simulator) simulator: instance of Simulator
          (int) N: nonnegative integer; default value is 1
        """
        self.simulator= neuron.simulator
        self.simulator.construct(self)	#check
        self.Neurons= []
        for i in range(N):
            self.Neurons.append(neuron.__class__(neuron.simulator))
            self.Neurons[i].copyNeuron(neuron)
                
    def getNeuronList(self):
    		""" returns a list of all the neurons in this neuron group """
        
    		return self.Neurons
    
    def rasterPlot(self):
        """ show a raster plot """
        criticalMonitor= []
        locMonitor= []
        c= 0
        for neuron in self.Neurons:
            temp= neuron.spikeMonitor.critical
            for i in range(len(temp)):
                criticalMonitor.append(temp[i])
                locMonitor.append(c)
            c+= 1
        matplotlib.pyplot.plot(criticalMonitor,locMonitor,'r.')
        print("criticalMonitor:")
        print(criticalMonitor)
        print("locMonitor:")
        print(locMonitor)
        ft= self.simulator.getFinalTau()
        
        matplotlib.pyplot.axis([0, ft, 0, c])
        matplotlib.pyplot.xlabel("Time (tau)")
        matplotlib.pyplot.ylabel("Neurons (index)")
        matplotlib.pyplot.title("Raster Plot")
        matplotlib.pyplot.show()
#        b=numpy.ones_like(self.master)
#        matplotlib.pyplot.plot(b)
        
        
#%%
class Monitor(object):
    """Class Invariants
        ([]) critical: List to store important information
        (Neuron) neuron: neuron which contains this monitor
    """
    def __init__(self, neuron):
        """Precondition
            (Neuron) neuron
        """
        self.critical= []
        self.neuron= neuron

class VoltageMonitor(Monitor):
    """Class Invariants:
        Inherits Monitor
        ([([(int)][(float)])]) critical: List of times and voltages at critical
            points
        ([(float)]) master: voltages for all times
    """
    def __init__(self, neuron):
        super().__init__(neuron)
        self.critical.append([])
        self.critical.append([])
    
    def appendCritical(self, time, voltage):
        """Precondition:
            (int) time: positive integer
            (float) voltage
            appends time and voltage to critical
        """
        self.critical[0].append(time)
        self.critical[1].append(voltage)

    
    def getAllVoltages(self):
        """ builds and returns master, which is a list of voltages whose 
            corresponding index is the tau time step
        """
        self.master= []
        self.master.append(self.critical[1][0]) #start by appending initial voltage
        for i in range(1, self.neuron.simulator.getFinalTau()):		
            if(i not in self.critical[0]):
                self.master.append(self.neuron.getNextVoltage(self.master[i-1]))
            else:
                self.master.append(self.critical[1][self.critical[0].index(i)]) 
                # if the voltage and time corresponding to the current tau,
                # represented by i is a critical point, append the voltage at
                # that critical point onto the list
        return self.master
        
        
    def plot(self):
        """ using matplotlib.pyplot.plot, plots voltage verses time graph"""
        self.getAllVoltages()
        matplotlib.pyplot.plot(self.master)
        matplotlib.pyplot.xlabel("time")
        matplotlib.pyplot.ylabel("Voltage")
        matplotlib.pyplot.title("Voltage/time graph")
        matplotlib.pyplot.show()

    		
    
class SpikeMonitor(Monitor):
    """Class Invariants:
        Inherits Monitor
        ([(int)]) critical: List of times neuron fires
        ([(float)]) master: spikes at all times
    """
    def __init__(self, neuron):
    		super().__init__(neuron)
    
    def appendCritical(self, time):
        """Percondition
            (int) time: nonnegative int
            appends time to critical
        """
        self.critical.append(time)
    
    def getAllSpikes(self):
        """builds and returns master,
        which is a list of the spikes at all time
        """
        self.master= []
        for i in range(self.neuron.simulator.getFinalTau()): 
            if(i in self.critical):
                self.master.append(1)
            else:
                self.master.append(0)
        return self.master
                
    def plot (self):
        """ using matplotlib.pyplot.plot, plots spikes verses time graph"""
        self.getAllSpikes()
        #matplotlib.pyplot.plot(self.master)
        b=numpy.ones_like(self.master)
        matplotlib.pyplot.plot(b)
        matplotlib.pyplot.eventplot(self.critical)
        matplotlib.pyplot.xlabel("time")        
        matplotlib.pyplot.title("single neuron raster plot")
        matplotlib.pyplot.show()
        
#%%
        
#The actual code
#Example Code

sim= GraphicSimulator(t= 0.1, finalT= 120)

ent= Neuron(sim)

A= LIFNeuron(sim, d= 5).Group(10)
B= MCPNeuron(sim).Group(10)
Synapse.connectWeightedByDistance(sim, ent, A, 1, 50, 40)
#Synapse.connectWeightedByDistance(sim, ent, A, -90, -90, 5)

Synapse.connectWeightedByDistance(sim, A, B, 6, -3, 1)

sim.appendInput(5, ent, 1)
sim.appendInput(20, ent, 1)
sim.appendInput(40, ent, 1)
sim.appendInput(60, ent, 3)
sim.appendInput(80, ent, 1)

sim.main()

for i in range(10):
    A.getNeuronList()[i].plotVoltage()
    A.getNeuronList()[i].plotSpikes()

for i in range(len(ent.getPostSynapses())):
    print("synaptic weight of neuron " + str(i) + ": "+ str(ent.getPostSynapses()[i].weight))

A.rasterPlot()
B.rasterPlot()

