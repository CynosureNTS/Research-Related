from z3 import *

def my_symbolic_execution(dnn):
    # create symbolic states for each input
    inputs = []
    for i in range(len(dnn[0][0][0])):
        inputs.append(z3.Real("i" + str(i)))
    
    expressions = []

    # for layer in dnn: 
    for l in range(len(dnn)):
     
        currentLayer = []
        # create symbolic state for each node in the layer and
        # add each node in the layer to currentLayer
        for n in range(len(dnn[l])): 
            if l == len(dnn)-1:
                currentLayer.append(z3.Real("o" + str(n)))
            else:
                currentLayer.append(z3.Real("n" + str(l) + "_" + str(n)))

            weightedSums = []
            # calculate weighted sums + bias
            for i in range(len(inputs)):
                weightedSums.append(inputs[i] * dnn[l][n][0][i] + dnn[l][n][1])
            
            # apply relu
            if(dnn[l][n][2]):
                expressions.append(currentLayer[n] == z3.If(sum(weightedSums) >= 0, sum(weightedSums),0))
            # no relu
            else: 
                expressions.append(currentLayer[n] == sum(weightedSums))

        # previous layer becomes input for next layer
        inputs = currentLayer 

    symbolic_states = z3.And(expressions)
    return symbolic_states

def test():
    # (weights, bias, use activation function relu or not)
    n00 = ([1.0, -1.0], 0.0, True)
    n01 = ([1.0, 1.0], 0.0, True)
    hidden_layer0 = [n00,n01]

    n10 = ([0.5, -0.2], 0.0, True)
    n11 = ([-0.5, 0.1], 0.0, True)
    hidden_layer1 = [n10, n11]

    # don't use relu for outputs
    o0 = ([1.0, -1.0], 0.0, False)  
    o1 = ([-1.0, 1.0], 0.0, False)
    output_layer = [o0, o1]

    dnn = [hidden_layer0, hidden_layer1, output_layer]

    symbolic_states = my_symbolic_execution(dnn)
    assert z3.is_expr(symbolic_states)

    numInputs = len(dnn[0][0][0])
    numHiddenNodes = 0
    for r in range(len(dnn)-1):
        numHiddenNodes += len(dnn[r])
    
    print("\ntest()...")
    print("Obtained symbolic states for DNN with {} inputs, {} hidden neurons, and {} outputs.".format(numInputs,numHiddenNodes,len(output_layer)))

    # Test 1: Generate Random Inputs
    print("\nSolving constraints with random inputs: ")
    z3.solve(symbolic_states)

    # Test 2: Concrete Execution
    print("\nPerforming Concrete Execution: ")
    i0, i1, n0_0, n0_1, o0, o1 = z3.Reals("i0 i1 n0_0 n0_1 o0 o1")

    # finding outputs when inputs are fixed [i0 == 1, i1 == -1]
    g = z3.And([i0 == 1.0, i1 == -1.0])
    z3.solve(z3.And(symbolic_states, g))  # you should get o0, o1 = 1, -1

    # Test 3: Check Assertions
    print("\nProve that if (n0_0 > 0.0 and n0_1 <= 0.0) then o0 > o1")
    g = z3.Implies(z3.And([n0_0 > 0.0, n0_1 <= 0.0]), o0 > o1)
    print(g)  #  Implies (And(n0_0 > 0, n0_1 <= 0), o0 > o1)
    z3.prove(z3.Implies(symbolic_states, g))  # proved

    print("\nProve that when (i0 - i1 > 0 and i0 + i1 <= 0), then o0 > o1")
    g = z3.Implies(z3.And([i0 - i1 > 0.0, i0 + i1 <= 0.0]), o0 > o1)
    print(g)  # Implies(And(i0 - i1 > 0, i0 + i1 <= 0), o0 > o1)
    z3.prove(z3.Implies(symbolic_states, g))
    # proved

    print("\nDisprove that when i0 - i1 >0, then o0 > o1")
    g = z3.Implies(i0 - i1 > 0.0, o0 > o1)
    print(g)  # Implies(And(i0 - i1 > 0, i0 + i1 <= 0), o0 > o1)
    z3.prove(z3.Implies(symbolic_states, g))
    # counterexample  (you might get different counterexamples)
    # [n0_1 = 15/2,
    # i1 = 7/2,
    # o0 = -1/2,
    # o1 = 1/2,
    # n1_0 = 0,
    # i0 = 4,
    # n1_1 = 1/2,
    # n0_0 = 1/2]

def test2():
    # (weights, bias, use activation function relu or not)
    n00 = ([0.4, -0.2], .2, True)
    n01 = ([-0.3, 0.7], 1.0, True)
    n02 = ([1.4, -0.4], -0.4, True)
    n03 = ([-0.8, -0.1], 0.6, True)
    hidden_layer0 = [n00,n01,n02,n03]

    n10 = ([0.5, -0.2, -0.3, 1.0], -1.1, True)
    n11 = ([-0.2, 0.1, 1.1, -0.4], 0.6, True)
    n12 = ([0.2, -0.2, -0.6, 0.6], .3, True)
    n13 = ([-0.5, 0.1, 0.7, 0.2], 0.1, True)
    hidden_layer1 = [n10, n11, n12, n13]

    n20 = ([-0.9, -0.4, 0.3, 0.1], -0.8, True)
    n21 = ([0.4, 1.1, -0.7, -0.7], 0.5, True)
    n22 = ([0.5, -0.5, -0.1, -0.2], 0.6, True)
    n23 = ([-0.8, 0.7, -0.3, -1.2], 0.18, True)
    hidden_layer2 = [n20, n21, n22, n23]

    # don't use relu for outputs
    o0 = ([-1.0, 0.1, -0.2, -0.4], -0.6, False)  
    o1 = ([0.5, 0.4, 0.6, 1.0], 0.7, False)
    output_layer = [o0, o1]

    dnn = [hidden_layer0, hidden_layer1, hidden_layer2, output_layer]

    symbolic_states = my_symbolic_execution(dnn)
    assert z3.is_expr(symbolic_states)

    numInputs = len(dnn[0][0][0])
    numHiddenNodes = 0
    for r in range(len(dnn)-1):
        numHiddenNodes += len(dnn[r])
    
    print("\ntest2()...")
    print("Obtained symbolic states for DNN with {} inputs, {} hidden neurons, and {} outputs.".format(numInputs,numHiddenNodes,len(output_layer)))

    # Test 1: Random Inputs
    print("\nSatisfying constraints with random inputs: ")
    z3.solve(symbolic_states)

    # Test 2: Simulating a Concrete Execution
    print("\nPerforming Concrete Execution: ")
    i0, i1, n2_0, n2_1, o0, o1 = z3.Reals("i0 i1 n2_0 n2_1 o0 o1")

    # # finding outputs when inputs are fixed [i0 == 1, i1 == -1]
    g = z3.And([i0 == 1.0, i1 == -1.0])
    z3.solve(z3.And(symbolic_states, g))

    print("\nProve that if n2_0 >= n2_1 then o0 < 0")
    g = z3.Implies(n2_0 >= n2_1, o0 < 0)
    print(g)  #  Implies (n2_0 >= n2_1, o0 < 0)
    z3.prove(z3.Implies(symbolic_states, g))  # proved

    print("\nProve that for all i0,i1: o1 >= 0.7")
    g = ForAll([i0,i1], o1 >= 0.7)
    print(g)  # ForAll([i0,i1], o1 >= 0.7)
    z3.prove(z3.Implies(symbolic_states, g)) # proved

    print("\nDisprove that when i0 > i1, then o0 > o1")
    g = Implies(i0 > i1, o0 > o1)
    print(g)  
    z3.prove(z3.Implies(symbolic_states, g))

if __name__ == "__main__":
    test()
    test2()


    
   