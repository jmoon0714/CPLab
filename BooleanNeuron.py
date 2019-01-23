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
    def __init__ (self, weight=1):
        super(AndGate,self).__init__(weight)
        self.N1= neuro.MCPNeuron()
        self.N2= neuro.MCPNeuron()
        self.N3= neuro.MCPNeuron()
        self.neuron_list= [self.N1, self.N2, self.N3]
        
        self.S3_1= neuro.Synapse(self.N1, self.N3, self.weight/2)
        self.S3_2= neuro.Synapse(self.N2, self.N3, self.weight/2)
        self.synapse_list= [self.S3_1, self.S3_2]
        
    def get_out(self):
        return self.N3
    
    def connect_A(self, Nin):
        self.S1_inA= neuro.Synapse(Nin, self.N1)
        self.synapse_list.append(self.S1_inA)
         
    def connect_B(self, Nin):
        self.S1_inB= neuro.Synapse(Nin, self.N2)
        self.synapse_list.append(self.S1_inB)
        
class OrGate(Gate):
    def __init__ (self, weight=1):
        super(OrGate,self).__init__(weight)
        self.N1= neuro.MCPNeuron()
        self.N2= neuro.MCPNeuron(athreshold=0)
        self.N2= neuro.MCPNeuron()
        self.N3= neuro.MCPNeuron()
        self.neuron_list= [self.N1, self.N2, self.N3]

        self.S3_1= neuro.Synapse(self.N1, self.N3, self.weight)
        self.S3_2= neuro.Synapse(self.N2, self.N3, self.weight)
        self.synapse_list= [self.S3_1, self.S3_2]
    
    def get_out(self):
        return self.N3
        
    def connect_A(self, Nin):
        self.S1_inA= neuro.Synapse(Nin, self.N1)
        self.synapse_list.append(self.S1_inA)
         
    def connect_B(self, Nin):
        self.S1_inB= neuro.Synapse(Nin, self.N2)
        self.synapse_list.append(self.S1_inB)   
    
         
class NotGate(Gate):
    def __init__ (self, weight=1):
        super(NotGate,self).__init__(weight)
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
    
    def connect_A(self, Nin):
        self.and_gate.connect_A(Nin)
         
    def connect_B(self, Nin):
        self.and_gate.connect_B(Nin)
        

class XorGate(Gate):
    def __init__ (self):
        super(XorGate,self).__init__()
        self.nand_gate_1= NandGate()
        self.nand_gate_2= NandGate()
        self.nand_gate_3= NandGate()
        self.nand_gate_4= NandGate()
        
        self.neuron_list= []
        self.synapse_list= []
        
        self.nand_gate_2.connect_B(self.nand_gate_1.get_out())
        self.nand_gate_3.connect_A(self.nand_gate_1.get_out())
        self.nand_gate_4.connect_A(self.nand_gate_2.get_out())
        self.nand_gate_4.connect_B(self.nand_gate_3.get_out())
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
        
    def connect_A(self, Nin):
        self.nand_gate_1.connect_A(Nin)
        self.nand_gate_2.connect_A(Nin)
         
    def connect_B(self, Nin):
        self.nand_gate_1.connect_B(Nin)
        self.nand_gate_3.connect_B(Nin)  

class Mux_2_1 (object):
    def __init__(self):
        self.and_gate_1= AndGate()
        self.and_gate_2= AndGate()
        self.not_gate_1= NotGate()
        self.or_gate_1= OrGate()

        self.neuron_list=[]
        self.synapse_list=[]

        self.or_gate_1.connect_A(self.and_gate_1.get_out())
        self.or_gate_1.connect_B(self.and_gate_2.get_out())
        self.and_gate_1.connect_B(self.not_gate_1.get_out())
        
        self.gates= [self.and_gate_1, self.and_gate_2, self.not_gate_1, self.or_gate_1]
    
    def connect_A(self, N_A):
        self.and_gate_1.connect_A(N_A)

    def connect_B(self, N_B):
        self.and_gate_2.connect_B(N_B)
    
    def connect_S(self, N_S):
        self.and_gate_2.connect_A(N_S)
        self.not_gate_1.connect_in(N_S)

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
        return self.or_gate_1.get_out()

class Mux_4_1(object):
    def __init__(self):
        self.mux1= Mux_2_1()
        self.mux2= Mux_2_1()
        self.mux3= Mux_2_1()

        self.mux3.connect_A(self.mux1.get_out())
        self.mux3.connect_B(self.mux2.get_out())

        self.units= [self.mux1, self.mux2, self.mux3]
        
        self.neuron_list= []
        self.synapse_list= []

    def connect_S1(self, N_S1):
        self.mux1.connect_S(N_S1)
        self.mux2.connect_S(N_S1)
    
    def connect_S0(self, N_S0):
        self.mux3.connect_S(N_S0)
    
    def connect_A(self, N_A):
        self.mux1.connect_A(N_A)
    
    def connect_B(self, N_B):
        self.mux1.connect_B(N_B)
    
    def connect_C(self, N_C):
        self.mux2.connect_A(N_C)
    
    def connect_D(self, N_D):
        self.mux2.connect_B(N_D)
    
    def get_neurons(self):
        for unit in self.units:
            for neuron in unit.get_neurons():
                self.neuron_list.append(neuron)
        return self.neuron_list

    def get_synapses(self):
        for unit in self.units:
            for synapse in unit.get_synapses():
                self.synapse_list.append(synapse)
        return self.synapse_list
    
    def get_out(self):
        return self.mux3.get_out()

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
        self.and_gate_2.connect_B(self.not_gate_1.get_out())
        self.and_gate_1.connect_B(self.not_gate_2.get_out())
        
        self.gates= [self.and_gate_1, self.and_gate_2, self.not_gate_1, self.not_gate_2]
    
    def connect_S_bar(self, N_S_bar):
        self.and_gate_1.connect_A(N_S_bar)

    def connect_R_bar(self, N_R_bar):
        self.and_gate_2.connect_A(N_R_bar)

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
        self.or_gate_2.connect_B(self.not_gate_1.get_out())
        self.or_gate_1.connect_B(self.not_gate_2.get_out())
        
        self.gates= [self.or_gate_1, self.or_gate_2, self.not_gate_1, self.not_gate_2]
    
    def connect_S(self, N_S):
        self.or_gate_2.connect_A(N_S)

    def connect_R(self, N_R):
        self.or_gate_1.connect_A(N_R)

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

class D_latch(object):
    def __init__(self):
        self.sbrb_latch= S_bar_R_bar_latch()
        self.nand_1= NandGate()
        self.nand_2= NandGate()
        self.not_1= NotGate()

        self.neurons=[]
        self.synapses=[]

        self.nand_2.connect_B(self.not_1.get_out())
        self.sbrb_latch.connect_S_bar(self.nand_1.get_out())
        self.sbrb_latch.connect_R_bar(self.nand_2.get_out())
        self.components= [self.sbrb_latch, self.nand_1, self.nand_2, self.not_1]

    def connect_D(self, N_D):
        self.not_1.connect_in(N_D)
        self.nand_1.connect_A(N_D)

    def connect_WE(self, N_WE):
        self.nand_1.connect_B(N_WE)
        self.nand_2.connect_A(N_WE)
    def get_neurons(self):
        for component in self.components:
            for neuron in component.get_neurons():
                self.neurons.append(neuron)
        return self.neurons
    
    def get_synapses(self):
        for component in self.components:
            for synapse in component.get_synapses():
                self.synapses.append(synapse)
        return self.synapses

    def get_out(self):
        return self.sbrb_latch.get_out()

class D_Flip_Flop(object):
    def __init__(self):
        self.latch1= D_latch()
        self.latch2= D_latch()
        self.not1= NotGate()
        self.not2= NotGate()
        
        self.neurons= []
        self.synapses= []  

        self.latch2.connect_D(self.latch1.get_out())
        self.latch1.connect_WE(self.not1.get_out())
        self.latch2.connect_WE(self.not2.get_out())
        self.not2.connect_in(self.not1.get_out())

        self.components= [self.latch1, self.latch2, self.not1, self.not2]

    def connect_D(self, N_D):
        self.latch1.connect_D(N_D)

    def connect_WE(self, N_WE):
        self.not1.connect_in(N_WE)
    
    def get_neurons(self):
        for component in self.components:
            for neuron in component.get_neurons():
                self.neurons.append(neuron)
        return self.neurons
    
    def get_synapses(self):
        for component in self.components:
            for synapse in component.get_synapses():
                self.synapses.append(synapse)
        return self.synapses

    def get_out(self):
        return self.latch2.get_out()

class T_Flip_Flop(object):
    def __init__(self):
        self.d_ff= D_Flip_Flop()
        self.not1= NotGate()
        
        self.neurons= []
        self.synapses= []

        self.not1.connect_in(self.d_ff.get_out())
        self.d_ff.connect_D(self.not1.get_out())

        self.components= [self.d_ff, self.not1]

    def connect_WE(self, N_WE):
        self.d_ff.connect_WE(N_WE)
    
    def get_neurons(self):
        for component in self.components:
            for neuron in component.get_neurons():
                self.neurons.append(neuron)
        return self.neurons
    
    def get_synapses(self):
        for component in self.components:
            for synapse in component.get_synapses():
                self.synapses.append(synapse)
        return self.synapses

    def get_out(self):
        return self.d_ff.get_out()

class n_bit_register(object):
    def __init__(self, n=8):
        self.ffs= []
        self.neurons= []
        self.synapses= []  

        for i in range(n):
            self.ffs= self.ffs + [D_Flip_Flop()]

    def connect_Ds(self, N_Ds):
        if (len(self.ffs)!=len(N_Ds)):
            raise Exception("Nonmatching length between the number of flip flops and the number of input D neurons.")
        for N_D, ff in zip(N_Ds, self.ffs):
            ff.connect_D(N_D)

    def connect_WE(self, N_WE):
        for ff in self.ffs:
            ff.connect_WE(N_WE)
    
    def get_neurons(self):
        for ff in self.ffs:
            for neuron in ff.get_neurons():
                self.neurons.append(neuron)
        return self.neurons
    
    def get_synapses(self):
        for ff in self.ffs:
            for synapse in ff.get_synapses():
                self.synapses.append(synapse)
        return self.synapses

    def get_out(self):
        N_Qs= []
        for ff in self.ffs:
            N_Qs= N_Qs+[ff.get_out()]
        return N_Qs

class One_bit_adder(object):
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

        self.xor_gate_2.connect_A(self.xor_gate_1.get_out())
        self.xor_gate_2.connect_A(self.xor_gate_1.get_out())
        self.or_gate_1.connect_A(self.and_gate_1.get_out())
        self.or_gate_1.connect_B(self.and_gate_2.get_out())
        self.or_gate_2.connect_A(self.or_gate_1.get_out())
        self.or_gate_2.connect_B(self.and_gate_3.get_out())
        
        self.gates= [self.xor_gate_1, self.xor_gate_2, self.and_gate_1, \
                     self.and_gate_2, self.and_gate_3, self.or_gate_1, \
                     self.or_gate_2]
    
    def connect_A(self, N_A):
        self.xor_gate_1.connect_A(N_A)
        self.and_gate_1.connect_B(N_A)
        self.and_gate_3.connect_B(N_A)

    def connect_B(self, N_B):
        self.xor_gate_1.connect_B(N_B)
        self.and_gate_2.connect_B(N_B)
        self.and_gate_3.connect_A(N_B)
    
    def connect_Cin(self, N_Cin):
        self.xor_gate_2.connect_B(N_Cin)
        self.and_gate_1.connect_A(N_Cin)
        self.and_gate_2.connect_A(N_Cin)

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

class N_bit_adder (object):
    def __init__(self, n=4):
        self.adders= []

        self.neuron_list=[]
        self.synapse_list=[]

        for i in range(n):
            self.adders= self.adders+[One_bit_adder()]
            
        previous_adder= self.adders[0]
        for adder in self.adders[1::]:
            adder.connect_Cin(previous_adder.get_Cout())
            previous_adder=adder
        
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

class One_bit_A_S(object):
    def __init__(self):
        self.adder= One_bit_adder()
        self.xor_gate = XorGate()
        
        self.adder.connect_B(self.xor_gate.get_out())
        
        self.units= [self.adder, self.xor_gate]
        self.neuron_list=[]
        self.synapse_list=[]
    
    def connect_A(self, N_A):
        self.adder.connect_A(N_A)
    
    def connect_B(self, N_B):
        self.xor_gate.connect_A(N_B)
        
    def connect_Cin(self, N_Cin):
        self.adder.connect_Cin(N_Cin)
        
    def connect_S(self, N_S):
        self.xor_gate.connect_B(N_S)
    
    def get_neurons(self):
        for unit in self.units:
            for neuron in unit.get_neurons():
                self.neuron_list.append(neuron)
        return self.neuron_list
    
    def get_synapses(self):
        for unit in self.units:
            for synapse in unit.get_synapses():
                self.synapse_list.append(synapse)
        return self.synapse_list
        
    def get_Sout(self):
        return self.adder.get_Sout()
    
    def get_Cout(self):
        return self.adder.get_Cout()

class N_bit_A_S(object):
    def __init__(self, n=4):
        self.num= n
        self.asers= []
        
        self.neuron_list= []
        self.synapse_list= []
        
        for i in range(n):
            self.asers.append(One_bit_A_S())
        
        previous_aser= self.asers[0]
        for aser in self.asers[1::]:
            aser.connect_Cin(previous_aser.get_Cout())
            previous_aser= aser

    def connect_As(self, N_As):
        if (self.num != len(N_As)):
            raise Exception("Nonmatching length between the number of one-bit \
                            adder/subtractor units and the number of input A \
                            neurons.")
            
        for N_A, aser in zip(N_As, self.asers):
            aser.connect_A(N_A)

    def connect_Bs(self, N_Bs):
        if (self.num != len(N_Bs)):
            raise Exception("Nonmatching length between the number of one-bit \
                            adder/subtractor units and the number of input B \
                            neurons.")
        for N_B, aser in zip(N_Bs, self.asers):
            aser.connect_B(N_B)
    
    def connect_S(self, N_S):
        self.asers[0].connect_Cin(N_S)
        for aser in self.asers:
            aser.connect_S(N_S)

    def get_neurons(self):
        for aser in self.asers:
            for neuron in aser.get_neurons():
                self.neuron_list.append(neuron)
        return self.neuron_list
    
    def get_synapses(self):
        for gate in self.asers:
            for synapse in gate.get_synapses():
                self.synapse_list.append(synapse)
        return self.synapse_list

    def get_Sout(self):
        N_Ys= []
        for asers in self.asers:
            N_Ys.append(asers.get_Sout())
        return N_Ys
    
    def get_Cout(self):
        return self.asers[len(self.asers)-1].get_Cout()
    
    def get_V(self):
        V= XorGate()
        V.connect_A(self.asers[self.num-2].get_Cout())
        V.connect_B(self.asers[self.num-1].get_Cout())
        return V.get_out()

class N_bit_logical(object):
    def __init__(self, n):
        self.num= n
        self.muxes= [] 
        self.ands= []
        self.ors= []

        for i in range(n):
            temp_and= AndGate()
            temp_or= OrGate()
            temp_mux= Mux_2_1()

            temp_mux.connect_A(temp_and.get_out())
            temp_mux.connect_B(temp_or.get_out())
            
            self.ands.append(temp_and)
            self.ors.append(temp_or)
            self.muxes.append(temp_mux)
        
        self.units= self.ands + self.ors + self.muxes
        self.neuron_list= []
        self.synapse_list= []

    def connect_LOP(self, N_LOP):
        for mux in self.muxes:
            mux.connect_S(N_LOP)
    
    def connect_As(self, N_As):
        if (self.num != len(N_As)):
            raise Exception("Nonmatching length between the number of logical \
             units and the number of input A neurons.")
        for N_A, and_gate in zip(N_As, self.ands):
            and_gate.connect_A(N_A)

        for N_A, or_gate in zip(N_As, self.ors):
            or_gate.connect_A(N_A)
    
    def connect_Bs(self, N_Bs):
        if (self.num != len(N_Bs)):
            raise Exception("Nonmatching length between the number of logical \
             units and the number of input B neurons.")
        for N_B, and_gate in zip(N_Bs, self.ands):
            and_gate.connect_B(N_B)
        for N_B, or_gate in zip(N_Bs, self.ors):
            or_gate.connect_B(N_B)
    
    def get_neurons(self):
        for unit in self.units:
            for neuron in unit.get_neurons():
                self.neuron_list.append(neuron)
        return self.neuron_list
    
    def get_synapses(self):
        for unit in self.units:
            for synapse in unit.get_synapses():
                self.synapse_list.append(synapse)
        return self.synapse_list
    
    def get_out(self):
        N_Ys= []
        for mux in self.muxes:
            N_Ys.append(mux.get_out())
        return N_Ys
        
