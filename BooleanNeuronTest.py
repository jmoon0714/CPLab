# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 10:02:29 2019

@author: jmoon0714
"""

import BooleanNeuron as bn
import Neuron as neuro

sim_tau= 1
sim_final_tau= 800
sim= neuro.Simulator(t=sim_tau, finalT=sim_final_tau)

def bin_byte_arr (num):
    raw= bin(num)
    number= raw[2::]
    arr= []
    for i in range(8-len(number)):
        arr.append(0)
    for char in number:
        arr.append(int(char))
    return arr
        
#==============================================================================
# # AND GATE
# A= neuro.MCPNeuron()
# B= neuro.MCPNeuron()
# and_gate= bn.AndGate()
# and_gate.connect_A(A)
# and_gate.connect_B(B)
# 
# sim.addNeurons(and_gate.get_neurons())
# sim.addSynapses(and_gate.get_synapses())
# sim.addNeurons([A,B])
# 
# sim.applyConstantInput(A, 0, 100, 0) #0,0
# sim.applyConstantInput(B, 0, 100, 0)
# sim.applyConstantInput(A, 0, 200, 100) #0,1
# sim.applyConstantInput(B, 1, 200, 100)
# sim.applyConstantInput(A, 1, 300, 200) #1,0
# sim.applyConstantInput(B, 0, 300, 200)
# sim.applyConstantInput(A, 1, 400, 300) #1,1
# sim.applyConstantInput(B, 1, 400, 300)
# sim.main()
# 
# sim.rasterPlot([A,B, and_gate.get_out()])
# sim.clear()
#==============================================================================

#==============================================================================
# # OR GATE
# A= neuro.MCPNeuron()
# B= neuro.MCPNeuron()
# or_gate= bn.OrGate()
# or_gate.connect_A(A)
# or_gate.connect_B(B)
# 
# sim.addNeurons(or_gate.get_neurons())
# sim.addSynapses(or_gate.get_synapses())
# sim.addNeurons([A,B])
# 
# sim.applyConstantInput(A, 0, 100, 0) #0,0
# sim.applyConstantInput(B, 0, 100, 0)
# sim.applyConstantInput(A, 0, 200, 100) #0,1
# sim.applyConstantInput(B, 1, 200, 100)
# sim.applyConstantInput(A, 1, 300, 200) #1,0
# sim.applyConstantInput(B, 0, 300, 200)
# sim.applyConstantInput(A, 1, 400, 300) #1,1
# sim.applyConstantInput(B, 1, 400, 300)
# sim.main()
# 
# sim.rasterPlot([A,B, or_gate.get_out()])
# sim.clear()
#==============================================================================

#==============================================================================
# # NOT GATE
# not_gate= bn.NotGate()
# sim.addNeurons(not_gate.get_neurons())
# sim.addSynapses(not_gate.get_synapses())
# sim.appendInput(1,not_gate.get_neurons()[0],1)
# sim.main()
# 
# sim.rasterPlot(not_gate.get_neurons())
# sim.clear()
#==============================================================================

#==============================================================================
# # NAND GATE
# A= neuro.MCPNeuron()
# B= neuro.MCPNeuron()
# nand_gate= bn.NandGate()
# nand_gate.connect_A(A)
# nand_gate.connect_B(B)
# 
# sim.addNeurons(nand_gate.get_neurons())
# sim.addSynapses(nand_gate.get_synapses())
# sim.addNeurons([A,B])
# 
# sim.applyConstantInput(A, 0, 100, 0) #0,0
# sim.applyConstantInput(B, 0, 100, 0)
# sim.applyConstantInput(A, 0, 200, 100) #0,1
# sim.applyConstantInput(B, 1, 200, 100)
# sim.applyConstantInput(A, 1, 300, 200) #1,0
# sim.applyConstantInput(B, 0, 300, 200)
# sim.applyConstantInput(A, 1, 400, 300) #1,1
# sim.applyConstantInput(B, 1, 400, 300)
# sim.main()
# 
# sim.rasterPlot([A,B, nand_gate.get_out()])
# sim.clear()
#==============================================================================

#==============================================================================
# # XOR GATE
# A= neuro.MCPNeuron()
# B= neuro.MCPNeuron()
# xor_gate = bn.XorGate()
# xor_gate.connect_A(A)
# xor_gate.connect_B(B)
# 
# sim.addNeurons(xor_gate.get_neurons())
# sim.addSynapses(xor_gate.get_synapses())
# sim.addNeurons([A,B])
# 
# sim.applyConstantInput(A, 0, 100, 0) #0,0
# sim.applyConstantInput(B, 0, 100, 0)
# sim.applyConstantInput(A, 0, 200, 100) #0,1
# sim.applyConstantInput(B, 1, 200, 100)
# sim.applyConstantInput(A, 1, 300, 200) #1,0
# sim.applyConstantInput(B, 0, 300, 200)
# sim.applyConstantInput(A, 1, 400, 300) #1,1
# sim.applyConstantInput(B, 1, 400, 300)
# sim.main()
# 
# sim.rasterPlot([A,B, xor_gate.get_out()])
# sim.clear()
#==============================================================================

#==============================================================================
# # S bar R bar latch
# S_bar= neuro.MCPNeuron()
# R_bar= neuro.MCPNeuron()
# 
# sbrb_latch = bn.S_bar_R_bar_latch()
# sbrb_latch.connect_S_bar(S_bar)
# sbrb_latch.connect_R_bar(R_bar)
# 
# sim.addNeurons(sbrb_latch.get_neurons())
# sim.addSynapses(sbrb_latch.get_synapses())
# sim.addNeuron(S_bar)
# sim.addNeuron(R_bar)
# 
# sim.applyConstantInput(S_bar, 1, 100, 0) #set Q to 1
# sim.applyConstantInput(R_bar, 1, 100, 0)
# sim.applyConstantInput(S_bar, 1, 200, 100) #hold
# sim.applyConstantInput(R_bar, 1, 200, 100)
# sim.applyConstantInput(S_bar, 1, 300, 200) #reset Q to 0
# sim.applyConstantInput(R_bar, 0, 300, 200)
# sim.applyConstantInput(S_bar, 1, 400, 300) #hold
# sim.applyConstantInput(R_bar, 1, 400, 300)
# sim.applyConstantInput(S_bar, 0, 500, 400) #set Q to 1
# sim.applyConstantInput(R_bar, 1, 500, 400)
# sim.applyConstantInput(S_bar, 1, 600, 500) #hold
# sim.applyConstantInput(R_bar, 1, 600, 500)
# sim.applyConstantInput(S_bar, 1, 700, 600) #set Q to 0
# sim.applyConstantInput(R_bar, 0, 700, 600)
# sim.applyConstantInput(S_bar, 1, 800, 700) #hold
# sim.applyConstantInput(R_bar, 1, 800, 700)
# sim.main()
# 
# sim.rasterPlot([S_bar, R_bar, sbrb_latch.get_out()])
# sim.clear()
#==============================================================================

#==============================================================================
# # S R latch
# S= neuro.MCPNeuron()
# R= neuro.MCPNeuron()
# 
# sr_latch = bn.S_R_latch()
# sr_latch.connect_S(S)
# sr_latch.connect_R(R)
# 
# sim.addNeurons(sr_latch.get_neurons())
# sim.addSynapses(sr_latch.get_synapses())
# sim.addNeuron(S)
# sim.addNeuron(R)
# 
# sim.applyConstantInput(S, 1, 100, 0) #set Q to 1
# sim.applyConstantInput(R, 0, 100, 0)
# sim.applyConstantInput(S, 0, 200, 100) #hold
# sim.applyConstantInput(R, 0, 200, 100)
# sim.applyConstantInput(S, 0, 300, 200) #reset
# sim.applyConstantInput(R, 1, 300, 200)
# sim.applyConstantInput(S, 0, 400, 300) #hold
# sim.applyConstantInput(R, 0, 400, 300)
# sim.applyConstantInput(S, 1, 500, 400) #set Q to 1
# sim.applyConstantInput(R, 0, 500, 400)
# sim.applyConstantInput(S, 0, 600, 500) #hold
# sim.applyConstantInput(R, 0, 600, 500)
# sim.main()
# 
# sim.rasterPlot([S, R, sr_latch.get_out()])
# sim.clear()
#==============================================================================

#==============================================================================
# # D latch
# D= neuro.MCPNeuron()
# WE= neuro.MCPNeuron()
# 
# d_latch = bn.D_latch()
# d_latch.connect_D(D)
# d_latch.connect_WE(WE)
# 
# sim.addNeurons(d_latch.get_neurons())
# sim.addSynapses(d_latch.get_synapses())
# sim.addNeuron(D)
# sim.addNeuron(WE)
# 
# sim.applyConstantInput(WE, 0, 200, 0)
# sim.applyConstantInput(WE, 1, 400, 200)
# sim.applyConstantInput(WE, 0, 600, 400)
# sim.applyConstantInput(WE, 1, 800, 600)
# sim.applyConstantInput(WE, 0, 1000, 800)
# sim.applyConstantInput(WE, 1, 1200, 1000)
# sim.applyConstantInput(WE, 0, 1400, 1200)
# 
# sim.applyConstantInput(D, 1, 650, 600)
# sim.applyConstantInput(D, 0, 700, 650)
# sim.applyConstantInput(D, 1, 750, 700)
# sim.applyConstantInput(D, 0, 850, 750)
# sim.main()
# 
# sim.rasterPlot([D, WE, d_latch.get_out()])
# sim.clear()
#==============================================================================

#==============================================================================
# # D flip flop
# D= neuro.MCPNeuron()
# CLK= neuro.MCPNeuron()
# 
# d_ff = bn.D_Flip_Flop()
# d_ff.connect_D(D)
# d_ff.connect_WE(CLK)
# 
# sim.addNeurons(d_ff.get_neurons())
# sim.addSynapses(d_ff.get_synapses())
# sim.addNeuron(D)
# sim.addNeuron(CLK)
# 
# sim.applyConstantInput(CLK, 0, 300, 0)
# sim.applyConstantInput(CLK, 1, 600, 300)
# sim.applyConstantInput(CLK, 0, 900, 600)
# sim.applyConstantInput(CLK, 1, 1200, 900)
# sim.applyConstantInput(CLK, 0, 1500, 1200)
# sim.applyConstantInput(CLK, 1, 1800, 1500)
# sim.applyConstantInput(CLK, 0, 2100, 1800)
# 
# sim.applyConstantInput(D, 1, 250, 350)
# sim.applyConstantInput(D, 0, 950, 850)
# sim.applyConstantInput(D, 1, 1550, 1450)
# sim.main()
# 
# sim.rasterPlot([D, CLK, d_ff.get_out()])
# sim.clear()
#==============================================================================

#==============================================================================
# # T flip flop
# N_CLK= neuro.MCPNeuron()
# 
# t_ff = bn.T_Flip_Flop()
# t_ff.connect_WE(N_CLK)
# 
# sim.addNeurons(t_ff.get_neurons())
# sim.addSynapses(t_ff.get_synapses())
# sim.addNeuron(N_CLK)
# 
# sim.applyConstantInput(N_CLK, 0, 500, 0)
# sim.applyConstantInput(N_CLK, 1, 1000, 500)
# sim.applyConstantInput(N_CLK, 0, 1500, 1000)
# sim.applyConstantInput(N_CLK, 1, 2000, 1500)
# sim.applyConstantInput(N_CLK, 0, 2500, 2000)
# sim.applyConstantInput(N_CLK, 1, 3000, 2500)
# sim.applyConstantInput(N_CLK, 0, 3500, 3000)
# sim.applyConstantInput(N_CLK, 1, 4000, 3500)
# sim.applyConstantInput(N_CLK, 0, 4500, 4000)
# sim.applyConstantInput(N_CLK, 1, 5000, 4500)
# sim.applyConstantInput(N_CLK, 0, 5500, 5000)
# sim.applyConstantInput(N_CLK, 1, 6000, 5500)
# sim.main()
# 
# sim.rasterPlot([N_CLK, t_ff.get_out()])
# sim.clear()
#==============================================================================

#==============================================================================
# # byte register
# N_Ds= []
# N_CLK= neuro.MCPNeuron()
# n=8
# for i in range(n):
#     N_Ds.append(neuro.MCPNeuron())
# neurons= N_Ds+[N_CLK]
# 
# byte_register = bn.n_bit_register(n)
# byte_register.connect_Ds(N_Ds)
# byte_register.connect_WE(N_CLK)
# 
# sim.addNeurons(byte_register.get_neurons())
# sim.addSynapses(byte_register.get_synapses())
# sim.addNeurons(neurons)
# 
# sim.applyConstantInput(N_CLK, 0, 500, 0)
# sim.applyConstantInput(N_CLK, 1, 1000, 500)
# 
# D= [0,1,0,1,0,1,1,1][::-1]
# for N_D, d in zip(N_Ds, D):
#     sim.applyConstantInput(N_D, d, 550, 450)
#     
# sim.main()  
# sim.rasterPlot(N_Ds +[N_CLK])
# sim.rasterPlot(byte_register.get_out())
# sim.clear()
#==============================================================================

#==============================================================================
# # One Bit Adder 
# A= neuro.MCPNeuron()
# B= neuro.MCPNeuron()
# C= neuro.MCPNeuron()
# 
# adder = bn.One_bit_adder()
# adder.connect_A(A)
# adder.connect_B(B)
# adder.connect_Cin(C)
# 
# sim.addNeurons(adder.get_neurons())
# sim.addSynapses(adder.get_synapses())
# sim.addNeurons([A,B,C])
# 
# sim.applyConstantInput(A, 0, 100, 0) #0+0 + 0=0 Cout=0
# sim.applyConstantInput(B, 0, 100, 0)
# sim.applyConstantInput(C, 0, 100, 0) 
# sim.applyConstantInput(A, 0, 200, 100) #0+0 + 1=1 Cout=0
# sim.applyConstantInput(B, 0, 200, 100) 
# sim.applyConstantInput(C, 1, 200, 100)
# sim.applyConstantInput(A, 0, 300, 200) #0+1 + 0=1 Cout=0
# sim.applyConstantInput(B, 1, 300, 200)
# sim.applyConstantInput(C, 0, 300, 200) 
# sim.applyConstantInput(A, 0, 400, 300) #0+1 + 1=0 Cout=1
# sim.applyConstantInput(B, 1, 400, 300) 
# sim.applyConstantInput(C, 1, 400, 300)
# sim.applyConstantInput(A, 1, 500, 400) #1+0 + 0=1 Cout=0
# sim.applyConstantInput(B, 0, 500, 400)
# sim.applyConstantInput(C, 0, 500, 400) 
# sim.applyConstantInput(A, 1, 600, 500) #1+0 + 1=0 Cout=1
# sim.applyConstantInput(B, 0, 600, 500) 
# sim.applyConstantInput(C, 1, 600, 500)
# sim.applyConstantInput(A, 1, 700, 600) #1+1 + 0=0 Cout=1
# sim.applyConstantInput(B, 1, 700, 600)
# sim.applyConstantInput(C, 0, 700, 600)
# sim.applyConstantInput(A, 1, 800, 700) #1+1 + 1=1 Cout=1
# sim.applyConstantInput(B, 1, 800, 700) 
# sim.applyConstantInput(C, 1, 800, 700)
# sim.main()
# 
# sim.rasterPlot([A, B, C] + [adder.get_Sout()]+[adder.get_Cout()])
# sim.clear()
#==============================================================================

#==============================================================================
# # 8 Bit Adder 
# n=8
# N_As= []
# N_Bs= []
# N_Cin= neuro.MCPNeuron()
# for Nin in range(n):
#     N_As.append(neuro.MCPNeuron())
#     N_Bs.append(neuro.MCPNeuron())
# neurons= N_As+N_Bs+[N_Cin]
# 
# byte_adder = bn.N_bit_adder(n)
# byte_adder.connect_As(N_As)
# byte_adder.connect_Bs(N_Bs)
# byte_adder.connect_Cin(N_Cin)
# 
# sim.addNeurons(byte_adder.get_neurons())
# sim.addSynapses(byte_adder.get_synapses())
# sim.addNeurons(neurons)
# 
# sim.applyConstantInput(N_Cin, 0, sim_final_tau, 0)
# 
# #8'b00100010+8'b00100010= 34+34= 8'b01000100= 68
# A= [0,0,1,0,0,0,1,0][::-1]
# B= [0,0,1,0,0,0,1,0][::-1]
# for N_A, a in zip(N_As,A):
#     sim.applyConstantInput(N_A, a, 3000,0)
# 
# for N_B, b in zip(N_Bs,B):
#     sim.applyConstantInput(N_B, b, 3000,0)
# 
# sim.main()
# 
# #8'b10000100= 132
# out_neurons= byte_adder.get_Sout()+[byte_adder.get_Cout()]
# 
# sim.rasterPlot(neurons)
# sim.rasterPlot(out_neurons)
# print(len(byte_adder.get_neurons()))    
# sim.clear()
#==============================================================================

#==============================================================================
# # 2 to 1 Mux
# N_A= neuro.MCPNeuron()
# N_B= neuro.MCPNeuron()
# N_Select= neuro.MCPNeuron()
# 
# mux= bn.Mux_2_1()
# mux.connect_A(N_A)
# mux.connect_B(N_B)
# mux.connect_S(N_Select)
# 
# sim.addNeurons([N_A, N_B, N_Select])
# sim.addNeurons(mux.get_neurons())
# sim.addSynapses(mux.get_synapses())
# 
# sim.applyConstantInput(N_A, 1, 800)
# sim.applyConstantInput(N_B, 1, 800)
# sim.applyConstantInput(N_Select, 0, 400)
# sim.applyConstantInput(N_Select, 1, 800, 400)
# 
# sim.main()
# sim.rasterPlot([N_A, N_B, N_Select, mux.get_out()])
# sim.clear()
# 
#==============================================================================
#==============================================================================
# # 4 to 1 Mux
# N_A= neuro.MCPNeuron()
# N_B= neuro.MCPNeuron()
# N_C= neuro.MCPNeuron()
# N_D= neuro.MCPNeuron()
# N_S0= neuro.MCPNeuron()
# N_S1= neuro.MCPNeuron()
# 
# in_neurons= [N_A, N_B, N_C, N_D, N_S0, N_S1]
# 
# mux= bn.Mux_4_1()
# mux.connect_A(N_A)
# mux.connect_B(N_B)
# mux.connect_C(N_D)
# mux.connect_D(N_D)
# mux.connect_S0(N_S0)
# mux.connect_S1(N_S1)
# 
# sim.addNeurons(in_neurons)
# sim.addNeurons(mux.get_neurons())
# sim.addSynapses(mux.get_synapses())
# 
# sim.applyConstantInput(N_A, 1, 800)
# sim.applyConstantInput(N_B, 0, 800)
# sim.applyConstantInput(N_C, 1, 800)
# sim.applyConstantInput(N_D, 0, 800)
# sim.applyConstantInput(N_S0, 0, 200)
# sim.applyConstantInput(N_S1, 0, 200)
# sim.applyConstantInput(N_S0, 1, 400, 200)
# sim.applyConstantInput(N_S1, 0, 400, 200)
# sim.applyConstantInput(N_S0, 0, 600, 400)
# sim.applyConstantInput(N_S1, 1, 600, 400)
# sim.applyConstantInput(N_S0, 1, 800, 600)
# sim.applyConstantInput(N_S1, 1, 800, 600)
# 
# 
# sim.main()
# sim.rasterPlot(in_neurons + [mux.get_out()])
# sim.clear()
#==============================================================================

#==============================================================================
# # One Bit Adder and Subtractor
# A= neuro.MCPNeuron()
# B= neuro.MCPNeuron()
# C= neuro.MCPNeuron()
# 
# add_sub = bn.One_bit_A_S()
# add_sub.connect_A(A)
# add_sub.connect_B(B)
# add_sub.connect_Cin(C)
# add_sub.connect_S(C)
# 
# sim.addNeurons(add_sub.get_neurons())
# sim.addSynapses(add_sub.get_synapses())
# sim.addNeurons([A,B,C])
# 
# # reminder: values are expressed in two's complement
# # 1 here can equal either 1 or -1 because 1 usually means -1 in 2's complement
# # but with the lack of more adders, it makes it hard to express just 1.
# sim.applyConstantInput(A, 0, 100, 0) #0+0 + 0=0 Cout=0
# sim.applyConstantInput(B, 0, 100, 0) # de facto: 0+0=0
# sim.applyConstantInput(C, 0, 100, 0) 
# sim.applyConstantInput(A, 0, 200, 100) #0+(-1) + 1=0 Cout=1
# sim.applyConstantInput(B, 0, 200, 100) # de facto: 0-0=0
# sim.applyConstantInput(C, 1, 200, 100) 
# sim.applyConstantInput(A, 0, 300, 200) #0+1 + 0=1 Cout=0
# sim.applyConstantInput(B, 1, 300, 200) # de facto: 0+1=1
# sim.applyConstantInput(C, 0, 300, 200) 
# sim.applyConstantInput(A, 0, 400, 300) #0+(0) + 1=1 Cout=0
# sim.applyConstantInput(B, 1, 400, 300) # de facto: 0-1=-1 OVERFLOW
# sim.applyConstantInput(C, 1, 400, 300) 
# sim.applyConstantInput(A, 1, 500, 400) #1+0 + 0=1 Cout=0
# sim.applyConstantInput(B, 0, 500, 400) # de facto: 1+0=1
# sim.applyConstantInput(C, 0, 500, 400) 
# sim.applyConstantInput(A, 1, 600, 500) #1+(-1) + 1=1 Cout=1
# sim.applyConstantInput(B, 0, 600, 500) # de facto: 1-0=-1
# sim.applyConstantInput(C, 1, 600, 500)
# sim.applyConstantInput(A, 1, 700, 600) #1+1 + 0=0 Cout=1
# sim.applyConstantInput(B, 1, 700, 600) # de facto: 1+1=2 OVERFLOW
# sim.applyConstantInput(C, 0, 700, 600)
# sim.applyConstantInput(A, 1, 800, 700) #1+(0) + 1=0 Cout=1
# sim.applyConstantInput(B, 1, 800, 700) # de facto: 1-1=0
# sim.applyConstantInput(C, 1, 800, 700)
# sim.main()
# 
# sim.rasterPlot([A, B, C] + [add_sub.get_Sout()]+[add_sub.get_Cout()])
# sim.clear()
#==============================================================================

#==============================================================================
# # 8 Bit Adder and Subtractor
# n= 8
# N_As= []
# N_Bs= []
# N_Cin= neuro.MCPNeuron()
# for i in range(n):
#     N_As.append(neuro.MCPNeuron())
#     N_Bs.append(neuro.MCPNeuron())
# neurons= N_As+N_Bs+[N_Cin]
# 
# byte_AS= bn.N_bit_A_S(n)
# byte_AS.connect_As(N_As)
# byte_AS.connect_Bs(N_Bs)
# byte_AS.connect_S(N_Cin)
# 
# sim.addNeurons(byte_AS.get_neurons())
# sim.addSynapses(byte_AS.get_synapses())
# sim.addNeurons(neurons)
# 
# sim.applyConstantInput(N_Cin, 0, sim_final_tau, 0)
# 
# #8'b00100010+8'b00100010= 34+34= 8'b01000100= 68
# A= bin_byte_arr(34)[::-1]
# B= [0,0,1,0,0,0,1,0][::-1]
# for N_A, a in zip(N_As, A):
#     sim.applyConstantInput(N_A, a, 3000, 0)
# 
# for N_B, b in zip(N_Bs, B):
#     sim.applyConstantInput(N_B, b, 3000, 0)
# 
# sim.main()
# 
# #8'b01000100= 68
# out_neurons= byte_AS.get_Sout()+[byte_AS.get_Cout(), byte_AS.get_V()]
# 
# sim.rasterPlot(neurons)
# sim.rasterPlot(out_neurons)
# print(len(byte_AS.get_neurons()))
# sim.clear()
#==============================================================================

# 8 Bit Logical
n= 8
N_As= []
N_Bs= []
N_LOP= neuro.MCPNeuron()
for i in range(n):
    N_As.append(neuro.MCPNeuron())
    N_Bs.append(neuro.MCPNeuron())
neurons= N_As+N_Bs+[N_LOP]

byte_logical= bn.N_bit_logical(n)
byte_logical.connect_As(N_As)
byte_logical.connect_Bs(N_Bs)
byte_logical.connect_LOP(N_LOP)

sim.addNeurons(byte_logical.get_neurons())
sim.addSynapses(byte_logical.get_synapses())
sim.addNeurons(neurons)

sim.applyConstantInput(N_LOP, 1, 400)
sim.applyConstantInput(N_LOP, 0, 800, 400)

#8'b10101010 && 8'b00100100 = 8'b00100000
#8'b10101010 || 8'b00100100 = 8'b10101010
A= [1,0,1,0,1,0,1,0][::-1]
B= [0,0,1,0,0,1,0,0][::-1]  
for N_A, a in zip(N_As, A):
    sim.applyConstantInput(N_A, a, 800, 0)

for N_B, b in zip(N_Bs, B):
    sim.applyConstantInput(N_B, b, 800, 0)

sim.main()

#8'b01000100= 68
out_neurons= byte_logical.get_out()

sim.rasterPlot(neurons)
sim.rasterPlot(out_neurons+ [byte_logical.ands[2].get_out()])
print(len(byte_logical.get_neurons()))
sim.clear()
