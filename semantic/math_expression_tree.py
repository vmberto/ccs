import operator

def parse(x):
    operators = set('+-*/')
    op_out = []    #This holds the operators that are found in the string (left to right)
    num_out = []   #this holds the non-operators that are found in the string (left to right)
    buff = []
    for c in x:  #examine 1 character at a time
        if c in operators:  
            #found an operator.  Everything we've accumulated in `buff` is 
            #a single "number". Join it together and put it in `num_out`.
            num_out.append(''.join(buff))
            buff = []
            op_out.append(c)
        else:
            #not an operator.  Just accumulate this character in buff.
            buff.append(c)
    num_out.append(''.join(buff))
    return num_out,op_out

def my_eval(nums,ops):

    nums = list(nums)
    ops = list(ops)
    operator_order = ('*/','+-')  #precedence from left to right.  operators at same index have same precendece.
                                  #map operators to functions.
    op_dict = {'*':operator.mul,
               '/':operator.truediv,
               '+':operator.add,
               '-':operator.sub}
    Value = None
    for op in operator_order:                   #Loop over precedence levels
        while any(o in ops for o in op):        #Operator with this precedence level exists
            idx,oo = next((i,o) for i,o in enumerate(ops) if o in op) #Next operator with this precedence         
            ops.pop(idx)                        #remove this operator from the operator list
            values = map(float,nums[idx:idx+2]) #here I just assume float for everything
            value = op_dict[oo](*values)
            nums[idx:idx+2] = [value]           #clear out those indices

    return nums[0]
