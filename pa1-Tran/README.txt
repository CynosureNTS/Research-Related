Author: Michael Tran
README for se.py
Supported Systems: Python Version 3.11.9
Last Modified: 12/22/2024

How to run the program:
	Unzip the folder "pa1-Tran.zip"
	Open a shell or Command Prompt and navigate into the folder "pa1-Tran"
	Type the command "python se.py"

1) Complete run of the program: 

python se.py

test()...
Obtained symbolic states for DNN with 2 inputs, 4 hidden neurons, and 2 outputs.

Solving constraints with random inputs:
[i1 = 7/2,
 n0_0 = 3,
 n1_1 = 0,
 i0 = 13/2,
 n0_1 = 10,
 o1 = 0,
 n1_0 = 0,
 o0 = 0]

Performing Concrete Execution:
[n1_1 = 0,
 i0 = 1,
 n0_1 = 0,
 o1 = -1,
 o0 = 1,
 n0_0 = 2,
 i1 = -1,
 n1_0 = 1]

Prove that if (n0_0 > 0.0 and n0_1 <= 0.0) then o0 > o1
Implies(And(n0_0 > 0, n0_1 <= 0), o0 > o1)
proved

Prove that when (i0 - i1 > 0 and i0 + i1 <= 0), then o0 > o1
Implies(And(i0 - i1 > 0, i0 + i1 <= 0), o0 > o1)
proved

Disprove that when i0 - i1 >0, then o0 > o1
Implies(i0 - i1 > 0, o0 > o1)
counterexample
[i1 = 7/2,
 n1_1 = 0,
 i0 = 13/2,
 n1_0 = 0,
 n0_1 = 10,
 n0_0 = 3,
 o1 = 0,
 o0 = 0]

test2()...
Obtained symbolic states for DNN with 2 inputs, 12 hidden neurons, and 2 outputs.

Satisfying constraints with random inputs:
[n0_0 = 0,
 o1 = 227/50,
 n2_2 = 29/10,
 n2_0 = 0,
 n2_3 = 0,
 n0_3 = 29/4,
 n0_2 = 0,
 n0_1 = 0,
 n1_3 = 37/20,
 o0 = -149/50,
 n1_0 = 57/20,
 i1 = -763/118,
 n2_1 = 0,
 n1_1 = 0,
 i0 = -797/118,
 n1_2 = 111/20]

Performing Concrete Execution:
[i0 = 1,
 n2_2 = 11/20,
 o0 = -2769/1000,
 n1_3 = 4/5,
 n2_3 = 173/100,
 n1_2 = 9/10,
 n0_0 = 1,
 n1_0 = 0,
 n0_2 = 1,
 i1 = -1,
 o1 = 824/125,
 n0_3 = 1/2,
 n1_1 = 16/5,
 n2_0 = 0,
 n2_1 = 433/100,
 n0_1 = 1]

Prove that if n2_0 >= n2_1 then o0 < 0
Implies(n2_0 >= n2_1, o0 < 0)
proved

Prove that for all i0,i1: o1 >= 0.7
ForAll([i0, i1], o1 >= 7/10)
proved

Disprove that when i0 > i1, then o0 > o1
Implies(i0 > i1, o0 > o1)
counterexample
[i1 = -9451/1104,
 n2_2 = 58933/36800,
 n2_3 = 0,
 o1 = 691999/184000,
 n0_3 = 2665/736,
 n0_1 = 0,
 n1_3 = 5071/11040,
 o0 = -500533/184000,
 n1_0 = 0,
 n0_2 = 0,
 n2_0 = 0,
 n1_1 = 757/1104,
 i0 = -4319/2208,
 n1_2 = 40169/11040,
 n2_1 = 0,
 n0_0 = 367/276]

2.i) My SE algorithm is outlined below: 
	1) Create a list called "expressions" that will contain the symbolic states
	2) Create a list called "inputs" that contains the z3 variables for each input i0, i1.
	3) For each layer in the DNN:
		Create z3 variables for each hidden neuron, calculate their weighted sums + bias, and apply Relu where applicable.
		Insert the result into the "expressions" list from step 1.
		Assign to "inputs" the newly calculated weighted sums to use as inputs for the next layer.
	4) apply z3.And() to the "expressions" list and return the result.

2.ii) My biggest obstacle to this assignment was a lack of experience using z3. I made the mistake of trying to generate a symbolic state without
	first understanding the format z3 required.

2.iii) My advice to others completing this assignment would be to play around with some simple z3 statements first to get a bit familiar with it. Only then should
	you attempt writing code to generate the symbolic states.
		
	
