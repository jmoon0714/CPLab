# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 12:21:25 2018

@author: jmoon0714
"""

import Neuron as neuro
import numpy as np

class Gate(object):
   
    def __init__ (self):
        self.weight= 1
        self.N1= neuro.MCPNeuron()
        self.N2= neuro.MCPNeuron()
        self.N3= neuro.MCPNeuron()
        self.neuron_list= [self.N1, self.N2, self.N3]
       
       
    def connect_out(self, Nout):
        self.Sout_3= neuro.Synapse(self.N2, Nout)
        self.synapse_list.append(self.Sout_3)
             
    def connect_inA(self, Nin):
        self.S1_inA= neuro.Synapse(Nin, self.N1)
        self.synapse_list.append(self.S1_inA)
         
    def connect_inB(self, Nin):
        self.S1_inB= neuro.Synapse(Nin, self.N2)
        self.synapse_list.append(self.S1_inB)
         
    def get_Neurons(self):
        return self.neuron_list
     
    def get_Synapses(self):
        return self.synapse_list


class AndGate(Gate):
    def __init__ (self):
        super(AndGate,self).__init__()
        self.S3_1= neuro.Synapse(self.N1, self.N3, weight=0.5)
        self.S3_2= neuro.Synapse(self.N2, self.N3, weight=0.5)
        self.synapse_list= [self.S3_1, self.S3_2]
        
class OrGate(Gate):
    def __init__ (self):
        super(AndGate,self).__init__()
        self.S3_1= neuro.Synapse(self.N1, self.N3, weight=1)
        self.S3_2= neuro.Synapse(self.N2, self.N3, weight=1)
        self.synapse_list= [self.S3_1, self.S3_2]
    
and_gate= AndGate()
sim = neuro.Simulator(t=1, finalT=10)
sim.addNeurons(and_gate.get_Neurons())
sim.addSynapses(and_gate.get_Synapses())
sim.appendInput(1,and_gate.get_Neurons()[0],1)
sim.appendInput(1,and_gate.get_Neurons()[1],1)
sim.main()

sim.rasterPlot(and_gate.get_Neurons())

sim.clear()


sim.rasterPlot(and_gate.get_Neurons())

