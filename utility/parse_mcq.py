def remove_newlines(input_string):
    return input_string.replace('\n', '')

def parse_mcq(mcqs):    
    ans = []
    for mcq in mcqs:
        temp_ans = {}
        lst = remove_newlines(mcq)
        lst = mcq.split(" ")
        option_format = None
        for e in lst:
            curr_ele = e[-2:]
            if curr_ele in ('1.', '1', '1:', '1,', 'A.', 'A:', 'A', 'A,'):
                option_format = "Number"
            elif curr_ele in ('A.', 'A:', 'A', 'A,', 'B', 'B.', 'B:', 'B,'):
                option_format = "Character"
        
        ind_op1, ind_op2, ind_op3, ind_op4 = -1, -1, -1, -1
        for i, e in enumerate(lst):
            curr_ele = e[-2:]
            if option_format == "Number":
                if curr_ele in ('1.', '1', '1:', '1,'):
                    ind_op1 = i
                elif curr_ele in ('2.', '2:', '2', '2,'):
                    ind_op2 = i
                elif curr_ele in ('3:', '3.', '3', '3,'):
                    ind_op3 = i
                elif curr_ele in ('4', '4.', '4:', '4,'):
                    ind_op4 = i
                    break
            elif option_format == "Character":
                if curr_ele in ('A.', 'A:', 'A', 'A,'):
                    ind_op1 = i
                elif curr_ele in ('B', 'B.', 'B:', 'B,'):
                    ind_op2 = i
                elif curr_ele in ('C', 'C.', 'C:', 'C,'):
                    ind_op3 = i
                elif curr_ele in ('D.', 'D:', 'D', 'D,'):
                    ind_op4 = i
                    break
        
        temp_ans["question"] = ' '.join(lst[:ind_op1 + 1])
        temp_ans["question"] = temp_ans["question"][:-2] 
        ind_op_answer = -1
        for i in range(ind_op4 + 1, len(lst)):
            if option_format == "Number":
                if lst[i] in ('1.', '1', '1:', '1,', '2.', '2:', '2', '2,', '3:', '3.', '3', '3,', '4', '4.', '4:', '4,'):
                    ind_op_answer = i
                    break
            elif option_format == "Character":
                if lst[i] in ('A.', 'A:', 'A', 'A,', 'B', 'B.', 'B:', 'B,', 'C', 'C.', 'C:', 'C,', 'D.', 'D:', 'D', 'D,'):
                    ind_op_answer = i
                    break
                
        temp_ans["options"] = [' '.join(lst[ind_op1 + 1:ind_op2 + 1]), ' '.join(lst[ind_op2 + 1:ind_op3 + 1]), ' '.join(lst[ind_op3 + 1:ind_op4 + 1])]
        temp_ans["solution"] = ' '.join(lst[ind_op_answer + 1:])
        ans.append(temp_ans)
    return ans
           