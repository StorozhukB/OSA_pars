from config import l_ans_mask,p_ans_mask,max_mark

def mask_pars(mask:list):
    """
    Generate dict of diferent types of questions based of result of database request
    """
    lec_15 = []
    prac_15 = []
    lec_yn = []
    prac_yn = []
    for i in mask:
        if i[1] == "lecture":
            if i[2] == "1_5":
                lec_15.append(i[0])
            elif i[2] == "yes/no":
                lec_yn.append(i[0])
        elif i[1] == "practice":
            if i[2] == "1_5":
                prac_15.append(i[0])
            elif i[2] == "yes/no":
                prac_yn.append(i[0])
        elif i[1] == "both":
            if i[2] == "1_5":
                lec_15.append(i[0])
                prac_15.append(i[0])
            elif i[2] == "yes/no":
                lec_yn.append(i[0])
                prac_yn.append(i[0])
    return {"l_1_5":lec_15, "p_1_5":prac_15, "l_y_n":lec_yn, "p_y_n":prac_yn}


def results_pars(res:list, mask:dict):
    """
    Transform answers from database to structured data ready to usage in graph module functions
    """
    out = {"l_1_5":{mask["l_1_5"][i]:[] for i in range(len(mask["l_1_5"]))},"p_1_5":{mask["p_1_5"][i]:[] for i in range(len(mask["p_1_5"]))}
         ,"l_y_n":{mask["l_y_n"][i]:[] for i in range(len(mask["l_y_n"]))},"p_y_n":{mask["p_y_n"][i]:[] for i in range(len(mask["p_y_n"]))}}

    stud_l = []
    stud_p = []

    for i in res:
        if i[2] not in stud_l and i[0] == "lecture":
            stud_l.append(i[2])
        elif i[2] not in stud_p and i[0] == "practice":
            stud_p.append(i[2])

        if i[0] == "lecture":
            for j in i[1].keys():
                j = int(j)
                if j in mask["l_1_5"]:
                    out["l_1_5"][j].append(i[1][str(j)])
                elif j in mask["l_y_n"]:
                    out["l_y_n"][j].append(i[1][str(j)])
        else:
            for j in i[1].keys():
                j=int(j)
                if j in mask["p_1_5"]:
                    out["p_1_5"][j].append(i[1][str(j)])
                elif j in mask["p_y_n"]:
                    out["p_y_n"][j].append(i[1][str(j)])

    result={"l_rad":[],"l_hist":[],"p_rad":[],"p_hist":[],"l_pr":[],"p_pr":[],"num_l":len(stud_l),"num_p":len(stud_p)}

    for i in l_ans_mask["radar"]:
        list = out["l_1_5"][i]
        aprox = 0

        for j in list:
            aprox += j

        if not list == []:
            aprox = aprox/len(list)
            result["l_rad"].append(aprox)

    for i in p_ans_mask["radar"]:
        list = out["p_1_5"][i]
        aprox = 0

        for j in list:
            aprox += j

        if not list == []:
            aprox = aprox/len(list)
            result["p_rad"].append(aprox)

    for i in l_ans_mask["hist"]:
        list = out["l_1_5"][i]
        hh = [0] * max_mark

        for i in range(max_mark):
            for j in range(len(list)):
                if list[j] == i+1:
                    hh[i] += 1

        if not list == []:
            result["l_hist"].append(hh)

    for i in p_ans_mask["hist"]:
        list = out["p_1_5"][i]
        hh = [0] * max_mark

        for i in range(max_mark):
            for j in range(len(list)):
                if list[j] == i + 1:
                    hh[i] += 1

        if not list == []:
            result["p_hist"].append(hh)

    for i in mask["l_y_n"]:
        list = out["l_y_n"][i]
        aprox = 0

        for j in list:
            aprox += j

        if not list == []:
            aprox = int(round((aprox/len(list))*100,0))
            result["l_pr"].append(aprox)

    for i in mask["p_y_n"]:
        list = out["p_y_n"][i]
        aprox = 0

        for j in list:
            aprox += j

        if not list == []:
            aprox = int(round((aprox/len(list))*100,0))
            result["p_pr"].append(aprox)
    return result
