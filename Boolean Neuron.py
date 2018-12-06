# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 12:21:25 2018

@author: jmoon0714
"""

import Neuron as neuro

class Gate(object):
    def __init__ (self, weight=1): 
        self.weight= weight
        self.neuron_list=[]
        self.synapse_list=[]
    
    def get_out(self):
        raise Exception("NotImplementedException")
         
    def get_neurons(self):
        return self.neuron_list
     
    def get_synapses(self):
        return self.synapse_list


class AndGate(Gate):    
    def __init__ (self):
        super(AndGate,self).__init__()
        self.N1= neuro.MCPNeuron()
        self.N2= neuro.MCPNeuron()
        self.N3= neuro.MCPNeuron()
        self.neuron_list= [self.N1, self.N2, self.N3]
        
        self.S3_1= neuro.Synapse(self.N1, self.N3, self.weight/2)
        self.S3_2= neuro.Synapse(self.N2, self.N3, self.weight/2)
        self.synapse_list= [self.S3_1, self.S3_2]
        
    def get_out(self):
        return self.N3
    
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
        return self.N3
        
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
        return self.N2
        
    def connect_in(self, Nin):
        self.S1_in= neuro.Synapse(Nin, self.N1)
        self.synapse_list.append(self.S1_in)

class NandGate(Gate):
    
    def __init__(self):
        super(NandGate,self).__init__()
        self.and_gate= AndGate()
        self.not_gate= NotGate()
        
        self.neuron_list= []
        self.synapse_list= []
        
        self.not_gate.connect_in(self.and_gate.get_out())
        self.gates = [self.and_gate, self.not_gate]
        
        
    def get_out(self):
       return self.not_gate.get_out()
   
    def get_neurons(self):
        for gate in self.gates:
            for neuron in gate.get_neurons():
                self.neuron_list.append(neuron)
        return self.neuron_list
    
    def get_synapses(self):
        for gate in self.gates:
            for synapse in gate.get_synapses():
                self.synapse_list.append(synapse)
        return self.synapse_list
    
    def connect_inA(self, Nin):
        self.and_gate.connect_inA(Nin)
         
    def connect_inB(self, Nin):
        self.and_gate.connect_inB(Nin)
        

class XorGate(Gate):
    def __init__ (self):
        super(XorGate,self).__init__()
        self.nand_gate_1= NandGate()
        self.nand_gate_2= NandGate()
        self.nand_gate_3= NandGate()
        self.nand_gate_4= NandGate()
        
        self.neuron_list= []
        self.synapse_list= []
        
        self.nand_gate_2.connect_inB(self.nand_gate_1.get_out())
        self.nand_gate_3.connect_inA(self.nand_gate_1.get_out())
        self.nand_gate_4.connect_inA(self.nand_gate_2.get_out())
        self.nand_gate_4.connect_inB(self.nand_gate_3.get_out())
        self.gates = [self.nand_gate_1, self.nand_gate_2 ,self.nand_gate_3, self.nand_gate_4]
    
    def get_out(self):
        return self.nand_gate_4.get_out()
    
    def get_neurons(self):
        for gate in self.gates:
            for neuron in gate.get_neurons():
                self.neuron_list.append(neuron)
        return self.neuron_list
    
    def get_synapses(self):
        for gate in self.gates:
            for synapse in gate.get_synapses():
                self.synapse_list.append(synapse)
        return self.synapse_list
        
    def connect_inA(self, Nin):
        self.nand_gate_1.connect_inA(Nin)
        self.nand_gate_2.connect_inA(Nin)
         
    def connect_inB(self, Nin):
        self.nand_gate_1.connect_inB(Nin)
        self.nand_gate_3.connect_inB(Nin)  


class S_bar_R_bar_latch (object):
    def __init__(self):
        self.and_gate_1= AndGate()
        self.and_gate_2= AndGate()
        self.not_gate_1= NotGate()
        self.not_gate_2= NotGate()

        self.neuron_list=[]
        self.synapse_list=[]

        self.not_gate_1.connect_in(self.and_gate_1.get_out())
        self.not_gate_2.connect_in(self.and_gate_2.get_out())
        self.and_gate_2.connect_inB(self.not_gate_1.get_out())
        self.and_gate_1.connect_inB(self.not_gate_2.get_out())
        
        self.gates= [self.and_gate_1, self.and_gate_2, self.not_gate_1, self.not_gate_2]
    
    def connect_S_bar(self, N_S_bar):
        self.and_gate_1.connect_inA(N_S_bar)

    def connect_R_bar(self, N_R_bar):
        self.and_gate_2.connect_inA(N_R_bar)

    def get_neurons(self):
        for gate in self.gates:
            for neuron in gate.get_neurons():
                self.neuron_list.append(neuron)
        return self.neuron_list
    def get_synapses(self):
        for gate in self.gates:
            for synapse in gate.get_synapses():
                self.synapse_list.append(synapse)
        return self.synapse_list

    def get_out(self):
        return self.not_gate_1.get_out()

class S_R_latch (object):
    def __init__(self):
        self.or_gate_1= OrGate()
        self.or_gate_2= OrGate()
        self.not_gate_1= NotGate()
        self.not_gate_2= NotGate()

        self.neurons=[]
        self.synapses=[]

        self.not_gate_1.connect_in(self.or_gate_1.get_out())
        self.not_gate_2.connect_in(self.or_gate_2.get_out())
        self.or_gate_2.connect_inB(self.not_gate_1.get_out())
        self.or_gate_1.connect_inB(self.not_gate_2.get_out())
        
        self.gates= [self.or_gate_1, self.or_gate_2, self.not_gate_1, self.not_gate_2]
    
    def connect_S(self, N_S):
        self.or_gate_2.connect_inA(N_S)

    def connect_R(self, N_R):
        self.or_gate_1.connect_inA(N_R)

    def get_neurons(self):
        for gate in self.gates:
            for neuron in gate.get_neurons():
                self.neurons.append(neuron)
        return self.neurons
    
    def get_synapses(self):
        for gate in self.gates:
            for synapse in gate.get_synapses():
                self.synapses.append(synapse)
        return self.synapses

    def get_out(self):
        return self.not_gate_1.get_out()
    
class one_bit_adder(object):
    def __init__(self):
        self.xor_gate_1= XorGate()
        self.xor_gate_2= XorGate()
        self.and_gate_1= AndGate()
        self.and_gate_2= AndGate()
        self.and_gate_3= AndGate()
        self.or_gate_1= OrGate()
        self.or_gate_2= OrGate()

        self.neuron_list=[]
        self.synapse_list=[]

        self.xor_gate_2.connect_inA(self.xor_gate_1.get_out())
        self.xor_gate_2.connect_inA(self.xor_gate_1.get_out())
        self.or_gate_1.connect_inA(self.and_gate_1.get_out())
        self.or_gate_1.connect_inB(self.and_gate_2.get_out())
        self.or_gate_2.connect_inA(self.or_gate_1.get_out())
        self.or_gate_2.connect_inB(self.and_gate_3.get_out())
        
        self.gates= [self.xor_gate_1, self.xor_gate_2, self.and_gate_1, \
                     self.and_gate_2, self.and_gate_3, self.or_gate_1, \
                     self.or_gate_2]
    
    def connect_A(self, N_A):
        self.xor_gate_1.connect_inA(N_A)
        self.and_gate_1.connect_inB(N_A)
        self.and_gate_3.connect_inB(N_A)

    def connect_B(self, N_B):
        self.xor_gate_1.connect_inB(N_B)
        self.and_gate_2.connect_inB(N_B)
        self.and_gate_3.connect_inA(N_B)
    
    def connect_Cin(self, N_Cin):
        self.xor_gate_2.connect_inB(N_Cin)
        self.and_gate_1.connect_inA(N_Cin)
        self.and_gate_2.connect_inA(N_Cin)

    def get_neurons(self):
        for gate in self.gates:
            for neuron in gate.get_neurons():
                self.neuron_list.append(neuron)
        return self.neuron_list
    
    def get_synapses(self):
        for gate in self.gates:
            for synapse in gate.get_synapses():
                self.synapse_list.append(synapse)
        return self.synapse_list

    def get_Sout(self):
        return self.xor_gate_2.get_out()
    def get_Cout(self):
        return self.or_gate_2.get_out()

class n_bit_adder (object):
    def __init__(self, n=4):
        self.adders= []

        self.neuron_list=[]
        self.synapse_list=[]

        for i in range(n):
            self.adders= self.adders+[one_bit_adder()]
        
    def connect_As(self, N_As):
        if (len(self.adders)!=len(N_As)):
            raise Exception("Nonmatching length between the number of one-bit adders and the number of input A neurons.")
        for N_A, adder in zip(N_As, self.adders):
            adder.connect_A(N_A)

    def connect_Bs(self, N_Bs):
        if (len(self.adders)!=len(N_Bs)):
            raise Exception("Nonmatching length between the number of one-bit adders and the number of input B neurons.")
        for N_B, adder in zip(N_Bs, self.adders):
            adder.connect_B(N_B)
    
    def connect_Cin(self, N_Cin):
        self.adders[0].connect_Cin(N_Cin)
        previous_adder= self.adders[0]
        for adder in self.adders[1::]:
            adder.connect_Cin(previous_adder.get_Cout())
            previous_adder=adder

    def get_neurons(self):
        for adder in self.adders:
            for neuron in adder.get_neurons():
                self.neuron_list.append(neuron)
        return self.neuron_list
    
    def get_synapses(self):
        for gate in self.adders:
            for synapse in gate.get_synapses():
                self.synapse_list.append(synapse)
        return self.synapse_list

    def get_Sout(self):
        N_Ys= []
        for adder in self.adders:
            N_Ys= N_Ys+[adder.get_Sout()]
        return N_Ys
    
    def get_Cout(self):
        return self.adders[len(self.adders)-1].get_Cout()


sim_final_tau= 800
sim= neuro.Simulator(t=1, finalT=sim_final_tau)

# AND GATE
A= neuro.MCPNeuron()
B= neuro.MCPNeuron()
and_gate= AndGate()
and_gate.connect_inA(A)
and_gate.connect_inB(B)

sim.addNeurons(and_gate.get_neurons())
sim.addSynapses(and_gate.get_synapses())
sim.addNeurons([A,B])

sim.applyConstantInput(A, 0, 100, 0) #0,0
sim.applyConstantInput(B, 0, 100, 0)
sim.applyConstantInput(A, 0, 200, 100) #0,1
sim.applyConstantInput(B, 1, 200, 100)
sim.applyConstantInput(A, 1, 300, 200) #1,0
sim.applyConstantInput(B, 0, 300, 200)
sim.applyConstantInput(A, 1, 400, 300) #1,1
sim.applyConstantInput(B, 1, 400, 300)
sim.main()

#==============================================================================
# sim.rasterPlot([A,B, and_gate.get_out()])
#==============================================================================
sim.clear()

# OR GATE
A= neuro.MCPNeuron()
B= neuro.MCPNeuron()
or_gate= OrGate()
or_gate.connect_inA(A)
or_gate.connect_inB(B)

sim.addNeurons(or_gate.get_neurons())
sim.addSynapses(or_gate.get_synapses())
sim.addNeurons([A,B])

sim.applyConstantInput(A, 0, 100, 0) #0,0
sim.applyConstantInput(B, 0, 100, 0)
sim.applyConstantInput(A, 0, 200, 100) #0,1
sim.applyConstantInput(B, 1, 200, 100)
sim.applyConstantInput(A, 1, 300, 200) #1,0
sim.applyConstantInput(B, 0, 300, 200)
sim.applyConstantInput(A, 1, 400, 300) #1,1
sim.applyConstantInput(B, 1, 400, 300)
sim.main()

#==============================================================================
# sim.rasterPlot([A,B, or_gate.get_out()])
#==============================================================================

sim.clear()

# NOT GATE
not_gate= NotGate()
sim.addNeurons(not_gate.get_neurons())
sim.addSynapses(not_gate.get_synapses())
sim.appendInput(1,not_gate.get_neurons()[0],1)
sim.main()
#==============================================================================
# sim.rasterPlot(not_gate.get_neurons())
#==============================================================================

sim.clear()

# NAND GATE

A= neuro.MCPNeuron()
B= neuro.MCPNeuron()
nand_gate= NandGate()
nand_gate.connect_inA(A)
nand_gate.connect_inB(B)

sim.addNeurons(nand_gate.get_neurons())
sim.addSynapses(nand_gate.get_synapses())
sim.addNeurons([A,B])

sim.applyConstantInput(A, 0, 100, 0) #0,0
sim.applyConstantInput(B, 0, 100, 0)
sim.applyConstantInput(A, 0, 200, 100) #0,1
sim.applyConstantInput(B, 1, 200, 100)
sim.applyConstantInput(A, 1, 300, 200) #1,0
sim.applyConstantInput(B, 0, 300, 200)
sim.applyConstantInput(A, 1, 400, 300) #1,1
sim.applyConstantInput(B, 1, 400, 300)
sim.main()

#==============================================================================
# sim.rasterPlot([A,B, nand_gate.get_out()])
#==============================================================================

sim.clear()

# XOR GATE

A= neuro.MCPNeuron()
B= neuro.MCPNeuron()
xor_gate = XorGate()
xor_gate.connect_inA(A)
xor_gate.connect_inB(B)

sim.addNeurons(xor_gate.get_neurons())
sim.addSynapses(xor_gate.get_synapses())
sim.addNeurons([A,B])

sim.applyConstantInput(A, 0, 100, 0) #0,0
sim.applyConstantInput(B, 0, 100, 0)
sim.applyConstantInput(A, 0, 200, 100) #0,1
sim.applyConstantInput(B, 1, 200, 100)
sim.applyConstantInput(A, 1, 300, 200) #1,0
sim.applyConstantInput(B, 0, 300, 200)
sim.applyConstantInput(A, 1, 400, 300) #1,1
sim.applyConstantInput(B, 1, 400, 300)
sim.main()

#==============================================================================
# sim.rasterPlot([A,B, xor_gate.get_out()])
#==============================================================================

sim.clear()

# S bar R bar latch
S_bar= neuro.MCPNeuron()
R_bar= neuro.MCPNeuron()

sbrb_latch = S_bar_R_bar_latch()
sbrb_latch.connect_S_bar(S_bar)
sbrb_latch.connect_R_bar(R_bar)

sim.addNeurons(sbrb_latch.get_neurons())
sim.addSynapses(sbrb_latch.get_synapses())
sim.addNeuron(S_bar)
sim.addNeuron(R_bar)

sim.applyConstantInput(S_bar, 0, 100, 0) #set Q to 1
sim.applyConstantInput(R_bar, 1, 100, 0)
sim.applyConstantInput(S_bar, 1, 200, 100) #hold
sim.applyConstantInput(R_bar, 1, 200, 100)
sim.applyConstantInput(S_bar, 1, 300, 200) #reset
sim.applyConstantInput(R_bar, 0, 300, 200)
sim.applyConstantInput(S_bar, 1, 400, 300) #hold
sim.applyConstantInput(R_bar, 1, 400, 300)
sim.applyConstantInput(S_bar, 0, 500, 400) #set Q to 1
sim.applyConstantInput(R_bar, 1, 500, 400)
sim.applyConstantInput(S_bar, 1, 600, 500) #hold
sim.applyConstantInput(R_bar, 1, 600, 500)
sim.main()

#==============================================================================
# sim.rasterPlot([S_bar, R_bar, sbrb_latch.get_out()])
#==============================================================================

sim.clear()

# S R latch
S= neuro.MCPNeuron()
R= neuro.MCPNeuron()

sr_latch = S_R_latch()
sr_latch.connect_S(S)
sr_latch.connect_R(R)

sim.addNeurons(sr_latch.get_neurons())
sim.addSynapses(sr_latch.get_synapses())
sim.addNeuron(S)
sim.addNeuron(R)

sim.applyConstantInput(S, 1, 100, 0) #set Q to 1
sim.applyConstantInput(R, 0, 100, 0)
sim.applyConstantInput(S, 0, 200, 100) #hold
sim.applyConstantInput(R, 0, 200, 100)
sim.applyConstantInput(S, 0, 300, 200) #reset
sim.applyConstantInput(R, 1, 300, 200)
sim.applyConstantInput(S, 0, 400, 300) #hold
sim.applyConstantInput(R, 0, 400, 300)
sim.applyConstantInput(S, 1, 500, 400) #set Q to 1
sim.applyConstantInput(R, 0, 500, 400)
sim.applyConstantInput(S, 0, 600, 500) #hold
sim.applyConstantInput(R, 0, 600, 500)
sim.main()

#==============================================================================
# sim.rasterPlot([S, R, sr_latch.get_out()])
#==============================================================================
sim.clear()

# One Bit Adder 
A= neuro.MCPNeuron()
B= neuro.MCPNeuron()
C= neuro.MCPNeuron()

adder = one_bit_adder()
adder.connect_A(A)
adder.connect_B(B)
adder.connect_Cin(C)

sim.addNeurons(adder.get_neurons())
sim.addSynapses(adder.get_synapses())
sim.addNeurons([A,B,C])

sim.applyConstantInput(A, 0, 100, 0) #0+0 + 0=0 Cout=0
sim.applyConstantInput(B, 0, 100, 0)
sim.applyConstantInput(C, 0, 100, 0) 
sim.applyConstantInput(A, 0, 200, 100) #0+0 + 1=1 Cout=0
sim.applyConstantInput(B, 0, 200, 100) 
sim.applyConstantInput(C, 1, 200, 100)
sim.applyConstantInput(A, 0, 300, 200) #0+1 + 0=1 Cout=0
sim.applyConstantInput(B, 1, 300, 200)
sim.applyConstantInput(C, 0, 300, 200) 
sim.applyConstantInput(A, 0, 400, 300) #0+1 + 1=0 Cout=1
sim.applyConstantInput(B, 1, 400, 300) 
sim.applyConstantInput(C, 1, 400, 300)
sim.applyConstantInput(A, 1, 500, 400) #1+0 + 0=1 Cout=0
sim.applyConstantInput(B, 0, 500, 400)
sim.applyConstantInput(C, 0, 500, 400) 
sim.applyConstantInput(A, 1, 600, 500) #1+0 + 1=0 Cout=1
sim.applyConstantInput(B, 0, 600, 500) 
sim.applyConstantInput(C, 1, 600, 500)
sim.applyConstantInput(A, 1, 700, 600) #1+1 + 0=0 Cout=1
sim.applyConstantInput(B, 1, 700, 600)
sim.applyConstantInput(C, 0, 700, 600)
sim.applyConstantInput(A, 1, 800, 700) #1+1 + 1=1 Cout=1
sim.applyConstantInput(B, 1, 800, 700) 
sim.applyConstantInput(C, 1, 800, 700)
sim.main()

sim.rasterPlot([A, B, C] + [adder.get_Sout()]+[adder.get_Cout()])

sim.clear()

# 8 Bit Adder 
n=8
N_As= []
N_Bs= []
for Nin in range(n):
    N_As.append(neuro.MCPNeuron())
    N_Bs.append(neuro.MCPNeuron())

N_Cin= neuro.MCPNeuron()

neurons= N_As+N_Bs+[N_Cin]

byte_adder = n_bit_adder(n)
byte_adder.connect_As(N_As)
byte_adder.connect_Bs(N_Bs)
byte_adder.connect_Cin(N_Cin)

sim.addNeurons(byte_adder.get_neurons())
sim.addSynapses(byte_adder.get_synapses())
sim.addNeurons(neurons)

sim.applyConstantInput(N_Cin, 0, sim_final_tau, 0)

#8'b00101101+8'b01010111= 45+87= 8'b10000100= 132
A= [0,0,1,0,1,1,0,1][::-1]
B= [0,1,0,1,0,1,1,1][::-1]
for N_A, a in zip(N_As,A):
    sim.applyConstantInput(N_A, a, 300,0)

for N_B, b in zip(N_Bs,B):
    sim.applyConstantInput(N_B, b, 300,0)

sim.main()

#8'b10000100= 132
out_neurons= byte_adder.get_Sout()+[byte_adder.get_Cout()]

sim.rasterPlot(neurons)
sim.rasterPlot(out_neurons)


