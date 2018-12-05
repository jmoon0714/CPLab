#from random import *
import random
from graphics import *
import matplotlib
import numpy as np
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
                #print("AP at "+ str(currentTau) + " at " + self.name)
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
        
    def changeWeights(self):
        0
            
    def plotWeight(self):
        0
        
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
            #print(currentTau)
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
        
        for synapseWeightToChange in self.synapseCheckList:
            synapseWeightToChange.changeWeights()
        
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
    
class GraphicSimulator(Simulator):
    """Class Invariants:
        Inherits Simulator
        constructList: List of the neurons to be drawn. 
        storageList: List of the drawn neurons, and the Circle objects that represent them
        synapseConstList: List of drawn Synapses, and the points that are the 
        locations of the Neurons that connect them
        l: length of the graphics window
        h: Height of the graphics window
        win: the graphics window displayed
        locType: way to arrange points

    """
    def __init__(self, t= 1, finalT=10000000,l=1000, h=500, locType=""):
        """Preconditions:
        """
        self.constructList=[]
        self.h=h
        self.l=l
        self.storageList=[]
        self.storageList.append([])
        self.storageList.append([])
        self.synapseConstList=[]
        self.locType=locType
        
        #changed here
        self.previousNeuronStatusList=[]
        
        super(GraphicSimulator, self).__init__(t,finalT)
        
    def addNeuron(self, aNeuron):
        super(GraphicSimulator, self).addNeuron(aNeuron)
        self.constructList.append(aNeuron)
        
    def addSynapse(self, aSynapse):
        super(GraphicSimulator, self).addSynapse(aSynapse)
        self.synapseConstList.append(aSynapse)
        
    def addNeuronList(self, aNeuronList):
        for aNeuron in aNeuronList:
            super(GraphicSimulator, self).addNeuron(aNeuron)
        self.constructList.append(aNeuronList)
        
    def makeG(self):
        """Builds graphical representations of all the Neurons in constructList with Circles, 
        and Synapses in synapseConstList with Lines, stores 
        them in storage List and synapseConstructList[0:1] and displays them 
        on the GraphWin win
        """
        count = 0
        count1 = 0
        
        #changed here
        self.previousNeuronStatusList=[False for i in range(len(self.neuronCheckList))]
        
        self.win=GraphWin("Neurons",self.l,self.h,autoflush=False)

        for ob in self.constructList:
            if ob not in self.storageList[0]:
                count1 += 1
                a = ob
                if not isinstance(a,list):
                    a = [a]
                GraphicObjectType = 0
                if len(a) != 1:
                    GraphicObjectType = 2
                for i in range(len(a)):
                    count += 1
                    self.storageList[0].append(a[i])
                    if(GraphicObjectType==0):
                        r = 5
                    else:
                        r = 3
                    circ = Circle(self.assignLoc(count, count1, GraphicObjectType, len(a), i),r)
                    self.storageList[1].append(circ)
        for circ in self.storageList[1]:
            circ.setFill("black")
            circ.draw(self.win)
        for i in range(len(self.synapseConstList)):
            a=self.synapseConstList[i]
            pre = a.pre
            post = a.post
            preCoords = self.storageList[1][self.storageList[0].index(pre)].getCenter()
            postCoords = self.storageList[1][self.storageList[0].index(post)].getCenter()
            l = Line(preCoords,postCoords)
            if(a.weight<0):
                l.setFill("blue")
            else:
                l.setFill("green")
            l.draw(self.win)
        self.win.update()
        
    def assignLoc(self,count, count1, GraphicObjectType, l, i):
        """ Precondition
            (int) x: a nonnegative integer
            (boolean) GraphicObjectType: is this neuron in a neurongroup
            returns the desired coordinate point of an object, based on locType
        """
        if(self.locType=="linearRandom"):
            x = count*0.3
            y=self.h*random.random()
        elif(self.locType=="random"):
            x=self.l*random.random()/12
            y=self.h*random.random()/1.2
        elif(self.locType=="sinusoidal"):
            x = count*0.3
            y=-1*self.h*math.cos(x)+self.h
        else:
            x = count1*10
            if GraphicObjectType==2:
                y=self.h/l*i
            elif(GraphicObjectType==0):
                y=self.h*random.random()        
        return Point(x*10+20,y+20)
        
    def main(self):
        """ runs a loop through all instants of tau """
        self.makeG()
        for currentTau in range(0,self.finalTau):
            print(currentTau)
            firedNeurons = super(GraphicSimulator, self).runOneTimeStep(currentTau)
            
            for i,neuronToCheck in enumerate(self.neuronCheckList):
                hasAP = firedNeurons[i]
                c = self.storageList[1][self.storageList[0].index(neuronToCheck)]
                if hasAP and (self.previousNeuronStatusList[i]==False):
                    c.setFill("red")
                    c.setOutline("red")
                    self.previousNeuronStatusList[i]=True
                elif self.previousNeuronStatusList[i]:
                    c.setFill("black")
                    c.setOutline("black")
                    self.previousNeuronStatusList[i]=False
                self.win.update()
            time.sleep(self.tau)
        

class HebbianSynapse(Synapse):
    def __init__(self, neuron1, neuron2, weight=1, adelay=1, aHebbianConstant=0.05, aCooincidence=3):
        super(HebbianSynapse, self).__init__(neuron1, neuron2, weight, adelay)
        self.changeConstant=aHebbianConstant
        self.weightData=[]
        self.weightData.append(self.weight)
        self.CDT=aCooincidence
        
    def changeWeights(self):
        #xpost=self.post.voltageHistory[len(self.post.voltageHistory)-1] if (self.post.voltageHistory[len(self.post.voltageHistory)-1] >=self.post.threshold) else 0
        #Implements linear threshold
        #xprev=self.pre.voltageHistory[len(self.pre.voltageHistory)-1] if (self.pre.voltageHistory[len(self.pre.voltageHistory)-1] >=self.pre.threshold) else 0
        #Note that it is important that the hebbian synapses are evaluated after all other synapses.
        xpost=0
        for i in range(self.CDT):
            if (self.post.voltageHistory[max(len(self.post.voltageHistory)-1-i,0)] >=self.post.threshold) :
                xpost=1
                break
            
        xprev=0
        for i in range(self.CDT):
            if (self.pre.voltageHistory[max(len(self.pre.voltageHistory)-1-i,0)] >=self.pre.threshold) :
                xprev=1
                break
            
        self.weight=self.weight+(self.changeConstant*(xpost)*(xprev))
        if self.weight>= 2: # weight boundry
            self.weight=2
        self.weightData.append(self.weight)
        
    def fire(self):
        """ fires the synapse, which affects post's voltage """
        pre= max(self.pre.voltageHistory[len(self.pre.voltageHistory)-1]-self.pre.threshold,0)
        self.post.addVoltage(self.weight*pre)
        
    def plotWeight(self):
        """ using matplotlib.pyplot.plot, plots voltage verses time graph"""
        matplotlib.pyplot.plot(self.weightData)
        matplotlib.pyplot.xlabel("time")
        matplotlib.pyplot.ylabel("weight")
        matplotlib.pyplot.title("weight/time graph of synapse ")
        matplotlib.pyplot.show()
        
class STDPSynapse(Synapse):
    def __init__(self, neuron1, neuron2, weight=1, adelay=1):
        super(STDPSynapse, self).__init__(neuron1, neuron2, weight, adelay)
        self.weightData=[]
        self.weightData.append(self.weight)
        self.negCount=0
        self.posCount=0
        
    def changeWeights(self):
        if(self.post.voltageHistory[len(self.post.voltageHistory)-1] >=self.post.threshold) and\
            (self.pre.voltageHistory[len(self.pre.voltageHistory)-1] >=self.pre.threshold): 
                1
        
        elif (self.pre.voltageHistory[len(self.pre.voltageHistory)-1] >=self.pre.threshold) :
            #If pre fired checki f post fired before it
            for tp in range(20):
                if (self.post.voltageHistory[max(len(self.post.voltageHistory)-1-tp,0)] >=self.post.threshold) :
                    self.negCount=self.negCount+1
                    if tp<=5:
                        self.weight=self.weight/1.4
                    elif tp<=10:
                        self.weight=self.weight/1.2
                    else:
                        self.weight=self.weight/1.1
                    break
        elif (self.post.voltageHistory[len(self.post.voltageHistory)-1] >=self.post.threshold) :
            #If post fired check if pre was "responsible"
            for tp in range(20):
                if (self.pre.voltageHistory[max(len(self.pre.voltageHistory)-1-tp,0)] >=self.pre.threshold) :
                    self.posCount=self.posCount+1
                    if tp<=5:
                        self.weight=1.4*self.weight
                    elif tp<=10:
                        self.weight=1.2*self.weight
                    else:
                        self.weight=1.1*self.weight
                    break
        self.weightData.append(self.weight)
        
    def fire(self):
        """ fires the synapse, which affects post's voltage """
        pre= self.pre.voltageHistory[len(self.pre.voltageHistory)-1]
        
        self.post.addVoltage(self.weight*pre)
        
    def plotWeight(self):
        """ using matplotlib.pyplot.plot, plots voltage verses time graph"""
        matplotlib.pyplot.plot(self.weightData)
        matplotlib.pyplot.xlabel("time")
        matplotlib.pyplot.ylabel("weight")
        matplotlib.pyplot.title("weight/time graph of synapse ")
        matplotlib.pyplot.show()
        
class RandomNeuron(Neuron):
    
    def __init__(self, avoltage=0, athreshold=1, arefractory=1, arate=120, aname=""): 
        """ Precondition:
        "avoltage": see Neuron documentation
        "athreshold": see Neuron documentation
        "arefractory": see Neuron documentation
        "adecay": controls rate of leakiness, default initialized to 5
        "aname": see Neuron documentation
        """
        super(RandomNeuron, self).__init__(avoltage=avoltage, athreshold=athreshold,\
             arefractory=arefractory, aname=aname)
        self.rateConstant= arate
        
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
            if(self.voltage >= self.threshold or random.random()*1000<self.rateConstant):
                self.spikeTimes.append(currentTau)
                #self.AP()
                self.voltage = 0
                self.refractCount = self.refractory
                self.voltageHistory[len(self.voltageHistory)-1] = self.voltageHistory[len(self.voltageHistory)-1] +1
                #print("AP at "+ str(currentTau) + " at " + self.name)
                return True
        return False
        
class competitiveInhibitor(Neuron):
    def __init__(self, avoltage=0, aname=""):
        """ Precondition:
        "avoltage": see Neuron documentation
        "athreshold": see Neuron documentation
        "arefractory": see Neuron documentation
        "aname": see Neuron documentation
        """
        super(competitiveInhibitor, self).__init__(avoltage=avoltage\
             , aname=aname)
        
    def addVoltage(self, aSum):
        """ Precondition:
            "v": adds "v" to sumInputs.
        """
        0
        
    def check(self, currentTau):
        """ forces all presynaptic neurons to have no inputs
        except the one with the highest input
        """
        voltages=[]
        for i in self.preSynapses:
            voltages.append(i.pre.sumInputs)
        #print(voltages)
        m=max(voltages)
        if m==0:
            return
        
        for i in range(len(voltages)):
            voltages[i]-=m
        for i in range(len(voltages)):
            if voltages[i]<0:
                self.preSynapses[i].pre.sumInputs=0
            else:
                self.preSynapses[i].pre.sumInputs=max(self.preSynapses[i].pre.sumInputs\
                                ,self.preSynapses[i].pre.threshold)
        
    