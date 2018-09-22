#from random import *
import random
import matplotlib
import numpy
import time
import math

#%%
class Neuron(object):

    """ Class Invariant: 
    "threshold": threshold voltage of the neuron; default initialized to 1.
    "voltage": current voltage of the neuron; default initialized to 0.
    "postSynapses": list of synapses to which the neuron is sending output.
    "preSynapses": list of synapses to which the neuron is receiving input.
    "sumInputs": sum of inputs at each time step before check method called (see below).
    "refractory": set refractory period of the neuron in tau; 
        default initialized to 1; must be greater than zero.
    "refractCount": is the refractory time left since this neuron last 
        fired. Must be between 0 and "refractory", inclusive.
    """
    PARAM_LIST=["avoltage", "athreshold", "arefractory", "aname"]
    PARAM_DEFAULTS=["0","1","1","An Intergrater Neuron"]
    @classmethod
    def arrayConstruct(cls, p):
        print("building Neuron: ",p)
        return cls(p[0],p[1],p[2],p[3])
    
    def __init__(self, avoltage = 0, athreshold = 1, arefractory = 1, aname=""): 
        """ "avoltage": initial voltage; by default initialized to 0.
            "athreshold": this neuron's threshold; by default initialized to 1.
            "arefractory": how many time steps the neuron is inactive following an AP;
                by default is initialized to 1.
            "aname": a descriptive name, used in printouts about this Neuron
            
            1) A variable called "refractCount" is initialized to 0, 
                refractCount represents the amount of time steps before 
                this neuron can fire again, at most "refractory" steps. 
            
            2) Each neuron holds two lists, "postSynapses" and 
                "preSynapses," which store instances of Synapse, representing 
                the synapses on the axon and dendrites of this neuron.
            
            4) Each neuron has lists spikeTimes and voltageHistory; the former 
                tracks the voltage over time, and the latter tracks the spikes over time.
        """
        self.threshold = athreshold
        self.voltage = avoltage
        self.postSynapses = []
        self.preSynapses = []
        self.sumInputs = 0
        self.refractory = arefractory
        self.refractCount = 0
        self.spikeTimes = []
        self.voltageHistory = [avoltage]
        self.name = aname
        if self.name=="":
            self.name = str(self)
    
    def addVoltage(self, aSum):
        """ Precondition:
            "v": adds "v" to sumInputs.
        """
        self.sumInputs += aSum
    
    def AP(self):
        """ activates this neuron's postSynapses """
        for synapse in self.postSynapses:
            synapse.activate()
                
    def check(self, currentTau):
        """ called by simulator
        adds all the previously incoming inputs
        if voltage>=threshold calls AP(), reduces the voltage by threshold, returns True
        else returns False
        """
        self.voltage += self.sumInputs
        self.sumInputs = 0
        self.refractCount -= 1
        self.voltageHistory.append(self.voltage)
        if(self.refractCount <= 0):
            self.refractCount = 0 
            if(self.voltage >= self.threshold):
                self.spikeTimes.append(currentTau)
                self.AP()
                self.voltage -= abs(self.threshold)
                self.refractCount = self.refractory
                print("AP at "+ str(currentTau) + " at " + self.name)
                return True
        return False
    
    def getCompleteSpikeTimes(self):
        """builds and returns completeSpikeTimes,
        which is a list of the spikes at all times
        """
        maxTauToDisplay = max(self.spikeTimes)
        self.completeSpikeTimes= []
        for i in range(maxTauToDisplay): 
            if(i in self.spikeTimes):
                self.completeSpikeTimes.append(1)
            else:
                self.completeSpikeTimes.append(0)
        return self.completeSpikeTimes
                
    def plotSpikes(self):
        """ using matplotlib.pyplot.plot, plots spikes verses time graph"""
        self.getCompleteSpikeTimes()
        b=numpy.ones_like(self.completeSpikeTimes)
        matplotlib.pyplot.plot(b)
        matplotlib.pyplot.eventplot(self.spikeTimes)
        matplotlib.pyplot.xlabel("time")        
        matplotlib.pyplot.title("single neuron raster plot of Neuron "+self.name)
        matplotlib.pyplot.show()
        
        
    def plotVoltage(self):
        """ using matplotlib.pyplot.plot, plots voltage verses time graph"""
        matplotlib.pyplot.plot(self.voltageHistory)
        matplotlib.pyplot.xlabel("time")
        matplotlib.pyplot.ylabel("Voltage")
        matplotlib.pyplot.title("Voltage/time graph of Neuron "+self.name)
        matplotlib.pyplot.show()
    
class LIFNeuron(Neuron):
    """ Class Invariant: 
    Inherits Neuron
    decayConstant: number that determines the rate of leakiness
    """
    PARAM_LIST=["avoltage", "athreshold", "arefractory","adecay", "aname"]
    PARAM_DEFAULTS=["0","1","1","5","A LIF Neuron"]

    @classmethod
    def arrayConstruct(cls, p):
        return cls(p[0],p[1],p[2],p[3],p[4])
    
    def __init__(self, avoltage=0, athreshold=1, arefractory=1, adecay=5, aname=""): 
        """ Precondition:
        "avoltage": see Neuron documentation
        "athreshold": see Neuron documentation
        "arefractory": see Neuron documentation
        "adecay": controls rate of leakiness, default initialized to 5
        "aname": see Neuron documentation
        """
        super(LIFNeuron, self).__init__(avoltage=avoltage, athreshold=athreshold,\
             arefractory=arefractory, aname=aname)
        self.decayConstant= adecay
        
    def leak(self, numTauSteps):
        """ calculates the desired leak in the neuron for numTauSteps"""
        self.voltage= self.voltage*((1-(1/self.decayConstant))**(numTauSteps))
    		
    def check(self, currentTau):
        """ called by simulator
        calculates the leak from one time step
        calls check for superclass Neuron
        """
        self.leak(1)
        return super(LIFNeuron, self).check(currentTau)	

class MCPNeuron(LIFNeuron): 
    """ Class Invariant:
    Inherits LIFNeuron
    Essentially the same as an LIF neuron with decay constant of 1, which ensures
    the neuron "forgets" all inputs before the current time step due to large leak
    """
    
    PARAM_LIST=["avoltage", "athreshold", "arefractory", "aname"]
    PARAM_DEFAULTS=["0","1","1","A MCPNeuron"]

    @classmethod
    def arrayConstruct(cls, p):
        return cls(p[0],p[1],p[2],p[3])
    
    def __init__(self, avoltage=0, athreshold=1, arefractory=1, aname=""):
        """ Precondition:
        "avoltage": see Neuron documentation
        "athreshold": see Neuron documentation
        "arefractory": see Neuron documentation
        "aname": see Neuron documentation
        """
        super(MCPNeuron, self).__init__(avoltage=avoltage, athreshold=athreshold,\
             arefractory=arefractory, aname=aname, adecay=1)

#%%
class Synapse(object):
    """ Class Invariant:
          "pre": The Neuron instance from which this Synapse is activated. 
          "post": The Neuron instance which this Synapse affects. 
          "weight": The amount this Synapse changes the voltage of the post neuron.
          "delay": The number of tau's necessary between activation and firing of this synapse
          "activateFireDelays": A list of delays between activations and firings of
          this neuron. Each element decremented by 1 with each time step. Synapse
          firing when element reaches 0, and element is popped off activateFireDelays.
    """

    PARAM_LIST=["weight", "adelay"]
    PARAM_DEFAULTS=["1","1"]

    @classmethod
    def arrayConstruct(cls, p):
        print("building Synapse: ",p)
        return cls(p[0],p[1],p[2],p[3])

    def __init__(self, neuron1, neuron2, weight=1, adelay=1):
        """ Precondition:
        "neuron1": instance of Neuron.
        "neuron2": instance of Neuron.
        "weight": Any floating point number.
        "adelay": Must be an integer 
        """
        self.pre = neuron1
        self.post = neuron2
        self.weight = weight
        self.delay = adelay
        self.activateFireDelays = []
        self.pre.postSynapses.append(self)
        self.post.preSynapses.append(self)
        
    def activate(self):
        """ appends delay to activateFireDelays
        """
        self.activateFireDelays.append(self.delay)
    
    def fire(self):
        """ fires the synapse, which affects post's voltage """
        self.post.addVoltage(self.weight)
            
    def check(self, currentTau):
        """ decrements all of activateFireDelays by 1; 
        when one of activateFireDelays is 0, pops it off the list and calls fire
        """
        self.activateFireDelays = [x-1 for x in self.activateFireDelays]
        count = 0
        while count < len(self.activateFireDelays) and self.activateFireDelays[count]==0:
            self.fire()
            count += 1
        self.activateFireDelays = self.activateFireDelays[count:]
            
    @classmethod
    def connect(cls, Alist, Blist, weight=1, d=1):
        synapseList = []
        for i in Alist:
            for j in Blist:
                synapseList.append(cls(i,j,weight,d)) 
        return synapseList
    
    @classmethod        
    def randomConnect(cls, Alist, Blist, weight=1, d=1, probability=0.5):
        synapseList = []
        for i in Alist:
            for j in Blist:
                if(random.random()<probability):
                    synapseList.append(cls(i,j,weight,d))
        return synapseList
                    
    @classmethod
    def randomWeightConnect(cls, Alist, Blist, minWeight=-1, maxWeight=1, d=1):
        synapseList = []
        for i in Alist:
            for j in Blist:
                weight= (random.random() * (maxWeight-minWeight)) + minWeight
                synapseList.append(cls(i,j,weight,d))
        return synapseList
                
    @classmethod
    def randomWeightRandomConnect(cls, Alist, Blist, minWeight= -1, maxWeight= 1,
                                  d=1, probability= 0.5):
        synapseList = []
        for i in Alist:
            for j in Blist:
                if(random.random()< probability):
                    weight= (random.random() * (maxWeight - minWeight)) + minWeight
                    synapseList.append(cls(i, j, weight, d))
        return synapseList
                    
    @classmethod
    def connectWeightedByDistance(cls, Alist, Blist, minWeight=0, maxWeight=1, 
                                  spread=-1, d=1):
        synapseList = []
        translate1= -len(Alist)/2
        translate2= -len(Blist)/2
        for i in range(len(Alist)):
            for j in range(len(Blist)):
                distance= abs((i + translate1) - (j + translate2))
                if(spread== -1 or distance<= spread):
                    synapseList.append(cls(Alist[i], Blist[j],\
                    weight=((maxWeight - minWeight)/(distance + 1)) + minWeight, adelay=d))
        return synapseList
            

#%%
class Simulator(object):
    """ Class invariant:
        "synapseCheckList": list of synapses to be checked in the next timestep
        "neuronCheckList": list of neurons to be checked in the next timestep
        "tau": minimum timestep. All time is in unit tau
        "finalTau": the last time (in tau) we care about
        inputArray: 2 dimensional array, dimensions 3*n, that 
        		stores info about when to stimulate which neuron with what voltage
    """
    def __init__(self, t= 1, finalT= 10000000):
        """ Precondition:
        """
        self.synapseCheckList=[]
        self.neuronCheckList=[]
        self.tau=t
        self.finalTau=finalT
        self.inputArray= []      

    def addNeuron(self, aNeuron):
        self.neuronCheckList.append(aNeuron)
        
    def addSynapse(self, aSynapse):
        self.synapseCheckList.append(aSynapse)
        
    def appendInput(self, aTime, aNeuron, aVoltage):
        """ Precondition:
        """
        self.inputArray.append([aTime, aNeuron, aVoltage])
        self.inputArray.sort(key = lambda x: x[0])

    def main(self, useDelay = False):
        """ runs a loop through all instants of tau """
        for currentTau in range(0,self.finalTau):
            print(currentTau)
            self.runOneTimeStep(currentTau)
            if useDelay:
                time.sleep(self.tau)
            
    def runOneTimeStep(self, currentTau):
        count = 0
        while(count < len(self.inputArray) and\
              currentTau==self.inputArray[count][0]):
            self.inputArray[count][1].\
            addVoltage(self.inputArray[count][2])
            count += 1
        self.inputArray = self.inputArray[count:]
        
        for synapseToCheck in self.synapseCheckList:
            synapseToCheck.check(currentTau)
        
        firedNeurons = []
        for neuronToCheck in self.neuronCheckList:
            firedNeurons.append(neuronToCheck.check(currentTau))
        return firedNeurons
    
    def rasterPlot(self, aNeuronList):
        """ show a raster plot """
        xLocs = []
        yLocs = []
        yLoc = 0
        for neuron in aNeuronList:
            spikeTimes = neuron.spikeTimes
            for i in range(len(spikeTimes)):
                xLocs.append(spikeTimes[i])
                yLocs.append(yLoc)
            yLoc += 1
        matplotlib.pyplot.plot(xLocs,yLocs,'r.')
        matplotlib.pyplot.axis([0, self.finalTau, 0, yLoc])
        matplotlib.pyplot.xlabel("Time (tau)")
        matplotlib.pyplot.ylabel("Neurons (index)")
        matplotlib.pyplot.title("Raster Plot")
        matplotlib.pyplot.show()
    
        
if __name__=='__main__':
    #create graphics simulator for 120 seconds, timestep=0.1 seconds
    sim = GraphicSimulator(t=0.1, finalT=120)
    
    #create a single Neuron that will receive all inputs, and add it to simulator
    inputNeuron = Neuron(aname="inputNeuron")
    sim.addNeuron(inputNeuron)
    
    #create list of 10 LIF Neurons linked to inputNeuron, and list of 10 MCP
    #Neurons linked to LIF Neurons
    Alist = []
    Blist = []
    for i in range(10):
        Alist.append(LIFNeuron(adecay=5, aname="LIF Neuron "+str(i)))
        Blist.append(MCPNeuron(aname="MCP Neuron "+str(i)))
    #add Neurons to Simulator
    sim.addNeuronList(Alist)
    sim.addNeuronList(Blist)
    #add Synapses weighted by distance between inputNeuron and Alist, and between
    #Alist and Blist, and add them to simulator
    synapseList = Synapse.connectWeightedByDistance([inputNeuron], Alist, 1, 50, 40)
    for i in range(len(synapseList)):
        sim.addSynapse(synapseList[i])
    synapseList = Synapse.connectWeightedByDistance(Alist, Blist, 6, -3, 1)
    for i in range(len(synapseList)):
        sim.addSynapse(synapseList[i])
    
    #add input voltage to inputNeuron at 5, 20, 40, 60 and 80 seconds
    sim.appendInput(5, inputNeuron, 1)
    sim.appendInput(20, inputNeuron, 1)
    sim.appendInput(40, inputNeuron, 1)
    sim.appendInput(60, inputNeuron, 3)
    sim.appendInput(80, inputNeuron, 1)
    
    #run simulation
    sim.main()
    
    #plot voltage history and spike times of each neuron in Alist
    for i in range(10):
        Alist[i].plotVoltage()
        Alist[i].plotSpikes()
    
    #print weights of synapses from inputNeuron to Alist
    for i in range(len(inputNeuron.postSynapses)):
        print("synaptic weight of neuron " + str(i) + ": "+ str(inputNeuron.postSynapses[i].weight))
    
    #print raster plots of Alist and Blist
    sim.rasterPlot(Alist)
    sim.rasterPlot(Blist)
