# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 02:19:42 2018

@author: jmoon0714
"""
#from random import *
import random

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
    ([(int)]) APLog: List of times this Neuron has had an action potential.
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
        self.toBeChecked= False   #new variable
        self.refractory= refractory
        self.refractCount= 0
        self.APLog=[]
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
        
#==============================================================================
#     def connect(self, neuron2, w):
#         """ Precondition:
#         			neuron2: must be instance of neuron that isn't equal to itself
#             appends neuron2 to postSynapses and appends this instance to neuron2's preSynapses
#         """
#         self.postSynapses.append(Synapse(self, neuron2, w))
#         neuron2.preSynapses.append(Synapse(self,neuron2, w))
#==============================================================================
    
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
        if(self.refractCount<= 0):
            self.refractCount= 0        #moved here, no change 
            if(self.voltage>= self.threshold):
                self.AP()
                self.voltage-= abs(self.threshold)
                self.refractCount= self.refractory
                self.APLog.append(currentTau)
                print("AP at "+ str(currentTau) + " at " + str(self))
            elif(self.threshold>0):     #never remove a "not neuron" from checklist
                self.simulator.neuronCheckList.remove(self)
                self.toBeChecked= False  #maybe make a function to implement these two lines
        self.lastTau= currentTau
    
    def getNeuronList(self):
        temp= []
        temp.append(self)
        return temp
        
    
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
        super().check(currentTau)	

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
          (Neuron) pre: The Neuron instance from which this Synapse is activated. Must be defined in the constructor and is final.
          (Neuron) post: The Neuron instance which this Synapse affects. Must be defined in the constructor and is final.
          (float) weight: The amount this Synapse changes the voltage of neuron2.
          (int) delay: The number of tau's necessary for the synapse to fire
          ([(int)]) activePhase: The list of AP coming through this synapse; each element shouldn't exceed delay in terms of tau; greater than 0;
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
        for countPhase in range(0,len(self.activePhase)):
            self.activePhase[countPhase]-=1
            if(self.activePhase[countPhase]<=0):
                self.activePhase.remove(self.activePhase[countPhase])
                self.fire()
        if(len(self.activePhase)==0):
            self.simulator.synapseCheckList.remove(self)  
            self.toBeChecked=False    #maybe make a function to implement these two lines
            
            
            
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
        for time in self.masterInput[0]:
            if(t< time): 
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
        """ inputs user data at currentTau and checks all the synapses and neurons that are to be checked """
        while(self.pointer<len(self.masterInput[0]) and currentTau==self.masterInput[0][self.pointer]):
            self.masterInput[1][self.pointer].addVoltage(self.masterInput[2][self.pointer])
            self.pointer+=1
        
        tempSCL=list(self.synapseCheckList)
        for synapsesToCheck in tempSCL:     #temporary list necessary as remove in check messes up the for loop
            synapsesToCheck.check(currentTau)
            
        tempNCL=list(self.neuronCheckList)  #temporary list necessary as remove in check messes up the for loop
        for neuronToCheck in tempNCL:
            neuronToCheck.check(currentTau)
            
            

class NeuronGroup(object):
    """ Class Invariant:
    (Simulator) simulator: the corresponding simulator that uses this neuron group
    ([(Neuron)]) Neurons: the list of all neurons stored in this neuron group
    """
    def __init__(self, sim, N= 1, v= 0, theta= 1, refractory= 1, d= 5, type= ""):
        """ Precondition:
                (Simulator) simulator: instance of Simulator
                (int) N: nonnegative integer; default value is 1
                (float) v: must be a float; default value is 0
                (float) theta: must be a float; default value is 1
                (int) refractory: nonnegative integer; default value is 1
                (float) d: real number greater than or equal to one.
        """
        self.simulator= sim
        self.Neurons= []
        if(type == ""):
            for i in range(N):
                self.Neurons.append(Neuron(sim, v, theta, refractory))
        elif(type == "LIF"):
            for i in range(N):
                self.Neurons.append(LIFNeuron(sim, v, theta, refractory, d))
        elif(type == "MCP"):
            for i in range(N):
                self.Neurons.append(MCPNeuron(sim, v, theta, refractory)) 
                
    def getNeuronList(self):
    		""" returns a list of all the neurons in this neuron group """
        
    		return self.Neurons
    
class Synapses(object):
    """ Class Invariant:
            (Simulator) simulator: the corresponding simulator which uses these Synapses
            ([(Neuron)]) NG1Neurons: list of presynaptic neurons
            ([(Neuron)]) NG2Neurons: list of postsynaptic neurons
            (float) weight: The weight given to each Synapse
            (int) delay: The number of tau's necessary for the synapse to fire
    """
    def __init__(self, sim, NG1, NG2, weight= 1, d= 1):
        """ Precondition:
            (Neuron/NeuronGroup) NG1
            (Neuron/NeuronGroup) NG2  
            (float) weight: a real number
            (int) d: a positive integer
        """
        self.NG1Neurons= NG1.getNeuronList()
        self.NG2Neurons= NG2.getNeuronList()
        self.simulator= sim
        self.weight= weight
        self.delay= d
        self.connect()
        
        
    def connect(self):
        """ connects each neuron in NG1Neurons to all neurons in NG2Neurons """
        for a in self.NG1Neurons:
            for b in self.NG2Neurons:
                Synapse(self.simulator, a, b, self.weight, self.delay)
        
class RandomSynapses(Synapses):
    """ Class Invariant:
    				Inherits Synapses
    				(float) probability: the probability that a neuron in NG1Neurons will connect to a neuron in NG2Neurons
    """
    def __init__(self, sim, NG1, NG2, weight= 1, d= 1, probability= 0.5):
        """ Precondition:
    				(Neuron/NeuronGroup) NG1
        		(Neuron/NeuronGroup) NG2  
            (float) weight: a real number
            (int) d: a positive integer
            (float) probability: 0<= probability< 1
        """
        self.probability= probability
        super().__init__(sim, NG1, NG2, weight, d)
    
    def connect(self):
        """ connects a neuron in NG1Neurons to a neuron in NG2Neurons only if the random number is less than probability """
        for a in self.NG1Neurons:
            for b in self.NG2Neurons:
                if(random.random() <= self.probability):
                    Synapse(self.simulator, a, b, self.weight, self.delay)

class RSwithRW(Synapses):
    """ Class Invariant:
    				Inherits Synapses
            (float) probability: the probability that a neuron in NG1Neurons will connect to a neuron in NG2Neurons
            (float) maxWeight: the maximum weight that can be given to a synapse
    """
    def __init__(self, sim, NG1, NG2, maxWeight= 1, d= 1, probability= 0.5):
        """ Precondition:
    				(Neuron/NeuronGroup) NG1
        		(Neuron/NeuronGroup) NG2  
            (float) maxWeight: a non-negative number
            (int) d: a positive integer
            (float) probability: 0<= probability< 1
        """
        super().__init__(sim, NG1, NG2, 1, d)
        self.probability= probability
    
    def connect(self):
        """ connects a neuron in NG1Neurons to a neuron in NG2Neurons only if the random number is less than probability
        with a synapse with a random weight less than the maxWeight """
        
        for a in self.NG1Neurons:
            for b in self.NG2Neurons:
                Synapse(self.simulator, a, b, random.random()*self.maxWeight, self.delay)
       	
        
class SynapsesWeightedByDistance(Synapses):
    """ Class Invariants: 
    				Subclass of Synapses
            (float) maxWeight: the maximum weight that can be given to a synapse
            (int) spread: the maximum distance from a neuron that synapses can form at. If -1, no limit.
    """
    def __init__(self, sim, NG1, NG2, maxWeight=1, d= 1, spread= -1):
        """ Precondition:
    				(Neuron/NeuronGroup) NG1
        		(Neuron/NeuronGroup) NG2
        		(float) maxWeight: a non-negative number
        		(int) d: a positive integer
        		(float) spread: either -1 or a nonnegative number
        """
        self.maxWeight= maxWeight
        self.spread= spread
        super().__init__(sim, NG1, NG2, 1, d)
        
    def connect(self):
        """ connects two neuron groups, making the weights for neurons closer together greater."""
        for i in range(len(self.NG1Neurons)):
            for j in range(len(self.NG2Neurons)):
                if(self.spread==-1 or abs(i-j)<=self.spread):
                    Synapse(self.simulator, self.NG1Neurons[i], self.NG2Neurons[j], self.maxWeight/(abs(i-j)+1), self.delay)
        
            
sim= Simulator(finalT=30)

#N1= Neuron(sim)
#N2= LIFNeuron(sim,theta=-0.5,d=2)
#Synapse(sim,N1,N2,weight=-1)
#print(N1)
#print(N2)
#sim.appendInput(5,N1,1)
#print(sim.masterInput)
#sim.main()

NL1=Neuron(sim)
NL2=Neuron(sim)
NM1= LIFNeuron(sim, theta=0.5,d=1)
NM2= LIFNeuron(sim, theta=-1.5,d=1)
NR= LIFNeuron(sim, theta=1.5,d=1)
print(NR)
Synapse(sim,NL1,NM1)
Synapse(sim,NL2,NM1)
Synapse(sim,NL1,NM2,-1)
Synapse(sim,NL2,NM2,-1)
Synapse(sim,NM1,NR)
Synapse(sim,NM2,NR)
sim.appendInput(0,NL1,1)
sim.appendInput(0,NL2,1)

sim.appendInput(10,NL1,0)
sim.appendInput(10,NL2,1)

sim.appendInput(20,NL1,1)
sim.appendInput(20,NL2,1)

sim.main()
#
#A= NeuronGroup(sim, 10)
#B= NeuronGroup(sim, 10)
#SynapsesWeightedByDistance(sim, A, B, 10)
##Stim= Neuron(sim)
##Synapses(sim, Stim, A)
#sim.appendInput(0,A,1)
#sim.main()



