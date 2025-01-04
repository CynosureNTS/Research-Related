from z3 import *
import random
import time

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

def create_random(sizes):
    nn = []
    
    #for each layer (except input layer):
    for i in range(1,len(sizes)):
        layer = []

        #determine whether to relu
        relu = True
        if i == len(sizes) - 1:
            relu = False

        #for each node in the layer:
        for k in range(sizes[i]):

            #generate weights and bias
            weights = []
            for j in range(sizes[i-1]):
                weights.append(random.randint(-50,50)/10)
            bias = random.randint(-50,50)/10
        
            layer.append((weights,bias,relu))

        nn.append(layer)
            
    return nn

def my_interval_execution(dnn,pre):
    result = pre
    inputs = list(pre.values())
   
    #for each layer (except inputs):
    for l in range(len(dnn)):
        curr = []
        # for each node in the layer:
        for n in range(len(dnn[l])):
    
            #calculate intervals
            lowerBound, upperBound = 0, 0
            for w in range(len(dnn[l][n][0])): 
                weight = dnn[l][n][0][w]
                
                if weight >= 0:
                    lowerBound += weight * min(inputs[w]) 
                    upperBound += weight * max(inputs[w]) 
                else:
                    lowerBound += weight * max(inputs[w]) 
                    upperBound += weight * min(inputs[w]) 
            
            #add bias
            bias = dnn[l][n][1]
            lowerBound += bias
            upperBound += bias
            
            #apply relu or not
            if dnn[l][n][2]:
                lowerBound = max(0,lowerBound)
                upperBound = max(0,upperBound)
            
            #store results
            curr.append([lowerBound,upperBound])
            if l != len(dnn) - 1:
                node = "n" + str(l) + str(n)
            else:
                node = "o" + str(n)
            result.update({node:[lowerBound,upperBound]})

        # use outputs of current layer as inputs to next layer
        inputs = curr  
          
    return result

def test1():
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

    print("\nAbstract Interval Domain test1()...")

    print("Simulating a concrete execution with fixed inputs: [i0 == 1, i1 == -1]")
    # finding outputs when inputs are fixed [i0 == 1, i1 == -1]
    states = my_interval_execution(dnn, pre={'i0':[1,1], 'i1':[-1,-1]})
    print(states)
    # {... 'o0': [1.0, 1.0], 'o1': [-1.0, -1.0]}

    print("\nSimulating execution with precondition:  0.1 <= i0 <= 0.3, -0.7 <= i1 <= 0.0")
    # executing using precondition 0.1 <= i0 <= 0.3, -0.7 <= i1 <= 0.0 
    states = my_interval_execution(dnn, pre={'i0':[0.1, 0.3], 'i1':[-0.7, 0.]})
    print(states)
    # {..., 'o0': [0.0, 0.5], 'o1': [-0.5, 0.0]}

    # MANUAL checking if 0.1 <= i0 <= 0.3, -0.7 <= i1 <= 0.0  implies 0 <= o0 <= 1
    # check that the output interval of o0 is COMPLETELY BETWEEN [0, 1].  If the answer is YES, then the property is proved. Otherwise, it is not proved.  
    # If the output is {..., 'o0': [0.0, 0.5], 'o1': [-0.5, 0.0]} (like in this example) then YES, this property 0 <= o0 <= 1 is proved because 0.0, 0.5 is included in [0.1]
    # If the output is {..., 'o0': [0.0, 1.2], 'o1': [-0.5, 0.0]}, then NO, you cannot say anything about this property 0 <= o0 <= 1 being valid or not.  

    # Proved

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
    o0 = ([0.2, 0.1, -0.2, 0.4], 0.2, False)  
    o1 = ([0.5, 0.4, 0.6, 1.0], -0.7, False)
    output_layer = [o0, o1]

    dnn = [hidden_layer0, hidden_layer1, hidden_layer2, output_layer]

    numInputs = len(dnn[0][0][0])
    numHiddenNodes = 0
    for r in range(len(dnn)-1):
        numHiddenNodes += len(dnn[r])
    
    print("\nAbstract Interval Domain test2() for DNN with {} inputs, {} hidden neurons, and {} outputs...".format(numInputs,numHiddenNodes,len(output_layer)))


    print("Simulating a concrete execution with fixed inputs: [i0 == 1, i1 == -1]")
    # finding outputs when inputs are fixed [i0 == 1, i1 == -1]
    states = my_interval_execution(dnn, pre={'i0':[1,1], 'i1':[-1,-1]})
    print(states)
    # {... 'o0': [0.7202000000000002, 0.7202000000000002], 'o1': [0.9308000000000003, 0.9308000000000003]}

    print("\nSimulating execution with precondition:  0.1 <= i0 <= 0.3, -0.7 <= i1 <= 0.0")
    # executing using precondition 0.1 <= i0 <= 0.3, -0.7 <= i1 <= 0.0 
    states = my_interval_execution(dnn, pre={'i0':[0.1, 0.3], 'i1':[-0.7, 0.]})
    print(states)
    # {..., 'o0': [0.12505000000000005, 0.60449], 'o1': [-0.6394199999999999, 0.7760999999999998]}
    
    # MANUAL checking if 0.1 <= i0 <= 0.3, -0.7 <= i1 <= 0.0  implies 0 <= o0 <= 1
    # check that the output interval of o0 is COMPLETELY BETWEEN [0, 1].  If the answer is YES, then the property is proved. Otherwise, it is not proved.  
    # If the output is {..., 'o0': [0.0, 0.5], 'o1': [-0.5, 0.0]}, then YES, this property 0 <= o0 <= 1 is proved because 0.0, 0.5 is included in [0.1]
    # If the output is {..., 'o0': [0.0, 1.2], 'o1': [-0.5, 0.0]}, then NO, you cannot say anything about this property 0 <= o0 <= 1 being valid or not.  

    # Proved

if __name__ == "__main__":

    ############################# Part 1: DNN Encoding #############################
    print("\nPerforming and solving Symbolic Execution on a randomly generated dnn:")
    l = [2,3,4,3,3]
    dnn = create_random(l)
    symbolic_state = my_symbolic_execution(dnn)
    
    #time the execution
    st = time.time()
    _ = z3.solve(symbolic_state)
    print('time to solve: ', time.time() - st)
    
    ####################### Part 2: Abstract Interval Domain #######################
    test1()
    test2()

    
    
   