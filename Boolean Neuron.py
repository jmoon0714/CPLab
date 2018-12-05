# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 12:21:25 2018

@author: jmoon0714
"""

import Neuron as neuro
import numpy as np

class Gate:
    def __init__ (self, weight=1): 
        self.weight= weight
       
    def connect_out(self, Nout):
        self.Sout_3= neuro.Synapse(self.N2, Nout)
        self.synapse_list.append(self.Sout_3)
    
    def get_out(self):
        raise Exception("NotImplementedException")
         
    def get_Neurons(self):
        return self.neuron_list
     
    def get_Synapses(self):
        return self.synapse_list


class AndGate(Gate):
    def __init__ (self):
        super(AndGate,self).__init__()
        self.N1= neuro.MCPNeuron()
        self.N2= neuro.MCPNeuron()
        self.N3= neuro.MCPNeuron()
        self.neuron_list= [self.N1, self.N2, self.N3]
        
        self.S3_1= neuro.Synapse(self.N1, self.N3, self.weight/25)
        self.S3_2= neuro.Synapse(self.N2, self.N3, self.weight/2)
        self.synapse_list= [self.S3_1, self.S3_2]
        
    def get_out(self):
        self.N3
    
    def connect_inA(self, Nin):
        self.S1_inA= neuro.Synapse(Nin, self.N1)
        self.synapse_list.append(self.S1_inA)
         
    def connect_inB(self, Nin):
        self.S1_inB= neuro.Synapse(Nin, self.N2)
        self.synapse_list.append(self.S1_inB)
        
class OrGate(Gate):
    def __init__ (self):
        super(OrGate,self).__init__()
        self.N1= neuro.MCPNeuron()
        self.N2= neuro.MCPNeuron(athreshold=0)
        self.N2= neuro.MCPNeuron()
        self.N3= neuro.MCPNeuron()
        self.neuron_list= [self.N1, self.N2, self.N3]
        self.S3_1= neuro.Synapse(self.N1, self.N3, self.weight)
        self.S3_2= neuro.Synapse(self.N2, self.N3, self.weight)
        
        self.S2_1= neuro.Synapse(self.N1, self.N3, self.weight*-1)
        self.synapse_list= [self.S3_1, self.S3_2]
    
    def get_out(self):
        self.N3
        
    def connect_inA(self, Nin):
        self.S1_inA= neuro.Synapse(Nin, self.N1)
        self.synapse_list.append(self.S1_inA)
         
    def connect_inB(self, Nin):
        self.S1_inB= neuro.Synapse(Nin, self.N2)
        self.synapse_list.append(self.S1_inB)   
    
         
class NotGate(Gate):
    def __init__ (self):
        super(NotGate,self).__init__()
        self.N1= neuro.MCPNeuron()
        self.N2= neuro.MCPNeuron(athreshold=0)
        self.neuron_list= [self.N1, self.N2]
        self.S2_1= neuro.Synapse(self.N1, self.N2, self.weight*-1)
        self.synapse_list= [self.S2_1]
        
    def get_out(self):
        self.N2
        
    def connect_in(self, Nin):
        self.S1_inA= neuro.Synapse(Nin, self.N1)
        self.synapse_list.append(self.S1_inA)


sim= neuro.Simulator(t=1, finalT=10)

# AND GATE
and_gate= AndGate()
sim.addNeurons(and_gate.get_Neurons())
sim.addSynapses(and_gate.get_Synapses())
sim.appendInput(1,and_gate.get_Neurons()[0],1)
sim.appendInput(1,and_gate.get_Neurons()[1],1)
sim.main()
sim.rasterPlot(and_gate.get_Neurons())

sim.clear()

# OR GATE
or_gate= OrGate()
sim.addNeurons(or_gate.get_Neurons())
sim.addSynapses(or_gate.get_Synapses())
sim.appendInput(1,or_gate.get_Neurons()[0],0)
sim.appendInput(1,or_gate.get_Neurons()[1],1)
sim.main()
sim.rasterPlot(or_gate.get_Neurons())

sim.clear()

# NOT GATE
not_gate= NotGate()
sim.addNeurons(not_gate.get_Neurons())
sim.addSynapses(not_gate.get_Synapses())
sim.appendInput(1,not_gate.get_Neurons()[0],1)
sim.main()
sim.rasterPlot(not_gate.get_Neurons())