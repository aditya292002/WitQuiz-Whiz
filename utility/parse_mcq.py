def parse_mcq(mcqs):    
    ans = []
    for mcq in mcqs:
        lst = mcq.split(" ")
        option_format = None
        for i in lst:
            if(i == '1.'):
                option_format = "Number"
            elif(i == 'A.'):
                option_format = "Character"
        ind_op1, ind_op2, ind_op3, ind_op4 = -1,-1,-1,-1
        for i,e in enumerate(lst):
            if(option_format == "Number"):
                if(e in ("1.","1", "1:")):
                    ind_op1 = i
                elif(e in ("2.", "2:", "2")):
                    ind_op2 = i
                elif(e in ("3:", "3.", "3")):
                    ind_op3 = i
                elif(e in ("4", "4.", "4:")):
                    ind_op4 = i
                    break
            elif(option_format == "Character"):
                if(e in ("A.", "A:", "A")):
                    ind_op1 = i
                elif(e in ("B", "B.", "B:")):
                    ind_op2 = i
                elif(e in ("C", "C.", "C:")):
                    ind_op3 = i
                elif(e in ("D.", "D:", "D")):
                    ind_op4 = i
                    break
        ind_op_answer = -1

        for i in range(ind_op4+1, len(lst)):
            if(option_format == "Number"):
                if(lst[i] in ("1.","1", "1:", "2.", "2:", "2", "3:", "3.", "3", "4", "4.", "4:")):
                    ind_op_answer = i
                    break
            elif(option_format == "Character"):
                if(lst[i] in ("A.", "A:", "A", "B", "B.", "B:", "C", "C.", "C:", "D.", "D:", "D")):
                    ind_op_answer = i
                    break
                
        ans.append({
            "question": ' '.join(lst[:ind_op1]),
            "options": [' '.join(lst[ind_op1:ind_op2]), ' '.join(lst[ind_op1:ind_op2]), ' '.join(lst[ind_op2:ind_op3]), ' '.join(lst[ind_op4:ind_op_answer])],
            "answer": ' '.join(lst[ind_op_answer:])
        })
    return ans