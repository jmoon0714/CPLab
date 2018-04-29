

#from random import *
import random
from graphics import *
import matplotlib
import time
import math

class Neuron(object):

    """ Class Invariant: 
    (float) threshold: threshold voltage of the neuron; default initialized to 1
    (float) voltage: current voltage of the neuron; default initialized to 0
    ([(Synapse)]) postSynapses: list of synapses to which the neuron is sending output
    ([(Synapse)]) preSynapses: list of synapses to which the neuron is receiving input
    (float) sumInputs: sum of Inputs before leaking
    (float) decayConstant: variable that determines the rate of leakiness
    (int) lastTau: last time this neuron was checked by simulation in terms of tau
    (Simulator) simulator: the corresponding simulator that uses this neuron
    (boolean) toBeChecked: True if the simulator check list comtains self; else false;
        removes the necessity to use inneficient contains()
    (int) refractory: is the set refractory period of the neuron in tau; default initialized to 1; Greater than zero.
    (int) refractCount: is the refractory time left since this neuron last fired. Must be between
    		0 and refractory, inclusive.
    """
    
    def __init__(self, sim, v= 0, theta= 1, refractory= 1): 
        """ Precondition:
            (Simulator) sim: instance of Simulator class
            (float) v: must be a float
            (float) theta: must be a float
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
            
    def copyNeuron(self, neuron):
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




    def getOutput(self):
        """ returns boolean value for neuron firing """
        if self.voltage>= self.threshold:
            return True
        else:
            return False
        
    def getPreSynapses(self):
        """ returns preSynapses"""
        return self.preSynapses
    
    def getPostSynapses(self):
        """ returns postSynapses """
        return self.postSynapses
    
    def setVoltage(self,v):
        """ Precondition: 
        			v: must be a float
            sets voltage to v
        """
        self.voltage= v
    
    def Group(self, N= 1):
        self.simulator.deconstruct(self)
        temp= NeuronGroup(self, N)
        return temp.getNeuronList()
        
    def getThreshold(self):
        """ return threshold """
        return self.threshold
        
    def addVoltage(self, v):
        """ Precondition:
        			v: must be a float
        adds v to sumInputs
        if this neuron is not in simulator neuronCheckList, adds it to that list
        """
        self.sumInputs += v
        if(not self.toBeChecked):
            self.simulator.neuronCheckList.append(self)
            self.toBeChecked=True #maybe make a function to implement these three lines
    
    def setThreshold(self, theta):
        """ Precondition:
        			theta: must be a float 
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
    
    def getNeuronList(self):
        temp= []
        temp.append(self)
        return temp
        
    def getNextVoltage(self,v):
    		return v
        
    def plotVoltage(self):
        self.voltageMonitor.plot()
        
    def plotSpikes(self):
    		self.spikeMonitor.plot()
    
class LIFNeuron(Neuron):
    """ Class Invariant: 
    Inherits Neuron
    (float) decayConstant: variable that determines the rate of leakiness
    """
    
    def __init__(self, sim, v= 0, theta= 1, d= 5): 
        """ Precondition:
        (Simulator) sim: instance of Simulator class
        (float) v: must be a float
        (float) theta: must be a float
        (float) d: real number greater than or equal to one.
        """
        super().__init__(sim, v, theta)
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

class MCPNeuron(LIFNeuron): 
    """ Class Invariant:
    Inherits Neuron
    Essentially the same as a normal neuron as a MCP is a the most basic All-Or-Nothing neuron
    """
    
    def __init__(self, sim, v= 0, theta= 1):
        """ Precondition:
        (Simulator) sim: instance of Simulator class
        (float) v: must be a float
        (float) theta: must be a float
        """
        super().__init__(sim, v, theta, d= 1)

            
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
        self.post.addVoltage(self.weight)
            
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
            self.toBeChecked=False    #maybe make a function to implement these two lines
        elif(self.activePhase[0]<=0):
            self.activePhase.pop(0)
            self.fire()
            self.checkHelper()
            
            
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
    def __init__(self, t= 1, finalT=10000000):
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
        pass
    
    def deconstruct(self,ob):
        pass
    
    def synConstruct(self,ob):
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
            
class GraphicSimulator(Simulator):
    def __init__(self, t= 1, finalT=10000000,l=1000, h=100):
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
        super().__init__(t,finalT)
        
    def construct(self,ob):
        self.constructList.append(ob)
        
    def deconstruct(self,ob):
        self.constructList.remove(ob)
        
    def synConstruct(self,ob):
        self.synapseConstList[0].append(ob)

        
    def makeG(self):
        count=0
        self.win=GraphWin("Neurons",self.l,self.h*3,autoflush=False)

        for ob in self.constructList:
            if ob not in self.storageList[0]:
                a=ob.getNeuronList()
                #if len(a)==1:
                for i in range(len(a)):
                    self.build(a[i],count)
                    count+=0.3
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
        
    def build(self, ob, pt):
        self.storageList[0].append(ob)
        circ=Circle(self.assignLoc(pt),5)
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
                break
            time.sleep(self.tau)
        #self.win.promptClose(win.getWidth()/2, 20)

        
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
            a=neuronToCheck.check(currentTau)
            if(a):
                c=self.storageList[1][self.storageList[0].index(neuronToCheck)]
                c.setFill("red")
            else:
                c=self.storageList[1][self.storageList[0].index(neuronToCheck)]
                c.setFill("black")
        self.win.update()

            
    def assignLoc(self,x,locType=""):
        y=-1*self.h*math.cos(x)+self.h
        return Point(x*10+20,y+20)
        
        
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
    
            
class Monitor(object):
    def __init__(self, neuron):
        self.critical= []
        self.neuron= neuron

class VoltageMonitor(Monitor):
    def __init__(self, neuron):
        super().__init__(neuron)
        self.critical.append([])
        self.critical.append([])
    
    def appendCritical(self, time, voltage):
        self.critical[1].append(voltage)
        self.critical[0].append(time)
    
    def getAllVoltages(self):
        self.master= []
        self.master.append(self.critical[1][0])
        for i in range(1,self.critical[0][len(self.critical[0])-1]):		
            if(i not in self.critical[0]):
                self.master.append(self.neuron.getNextVoltage(self.master[i-1]))
            else:
                self.master.append(self.critical[1][self.critical[0].index(i)])
        return self.master
        
        
    def plot(self):
        self.getAllVoltages()
        matplotlib.pyplot.plot(self.master)
        matplotlib.pyplot.show()

    		
    
class SpikeMonitor(Monitor):
    def __init__(self, neuron):
    		super().__init__(neuron)
    
    def appendCritical(self, time):
    		self.critical.append(time)
    
    def getAllSpikes(self):
        self.master= []
        for i in range(self.critical[len(self.critical)-1]+5): 
            if(i in self.critical):
                self.master.append(1)
            else:
                self.master.append(0)
        return self.master
                
    def plot (self):
        self.getAllSpikes()
        matplotlib.pyplot.plot(self.master)
        matplotlib.pyplot.show()
        
# =============================================================================
#             
# sim= GraphicSimulator(t=0.1,finalT=300)
# A= NeuronGroup(sim,20)
# 
# start=Neuron(sim)
# RandomSynapses(sim,start,A,probability=0.05)
# sim.appendInput(2,start,1)
# sim.main()
# 
# 
# =============================================================================

sim= GraphicSimulator(t=0.3,finalT=100)

NL1=Neuron(sim)
NL2=Neuron(sim)
NM1= MCPNeuron(sim, theta=0.5)
NM2= MCPNeuron(sim, theta=-1.5)
NR= MCPNeuron(sim, theta=1.5)
print(NR)
Synapse(sim,NL1,NM1,1,1)
Synapse(sim,NL2,NM1,1,1)
Synapse(sim,NL1,NM2,-1,1)
Synapse(sim,NL2,NM2,-1,1)
Synapse(sim,NM1,NR,1,1)
Synapse(sim,NM2,NR,1,1)

sim.appendInput(5,NL1,1)
sim.appendInput(5,NL2,1)

sim.appendInput(10,NL1,0)
sim.appendInput(10,NL2,1)

sim.appendInput(20,NL1,1)
sim.appendInput(20,NL2,1)

sim.appendInput(70,NL1,0)
sim.appendInput(70,NL2,1)
D=LIFNeuron(sim)
Synapse(sim,NR,D,3.5)
Synapse(sim,NM1,D)

E=Neuron(sim).Group(1000)
sim.main()

D.plotVoltage()
D.plotSpikes()



