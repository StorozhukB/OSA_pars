import json

import pars
import graph
import db_handle
from config import debug,hist_12_name,hist_11_name
from config import host,port,db_name,user,password
from os_handle import cur_dir,ch_cr



def faculty(db,fq:str,mask:dict):
    """
    Runs program for every teacher in specific faculty
    get database as db, fq as faculty name 
    and mask as list of answers parameters
    """
    t_list = db_handle.get_teachers_list_by_faculty(db,fq)
    for i in t_list:
        teacher(db, i, fq, mask)


def teacher(db,teacher:list,fq:str,mask:dict):
    """
    Get and parse results of OSA for every specific teacher
    Also generate graphic repr of those results
    """
    r = db_handle.get_results(db, fq, teacher[0])

    if debug:
        rt = "name:" + teacher[1] + "|id:" + str(teacher[0]) + "\n"
        for i in r:
            if not r:
                rt += str(i[0]) + "|" + str(i[1]) + "\n"
        with open("res_raw.txt", "a", encoding="utf-8") as file:
            file.write(rt)
    r = pars.results_pars(r, mask)
    p = cur_dir + "/res/" + fq + "/" + str(teacher[0])

    if r["num_l"] >= 3 :
        ch_cr(p+"/lector")
        graph.create_radar("l", r["l_rad"], path=p+"/lector/lector_rad")
        graph.create_hist(r["l_hist"][0], path=p+"/lector/lector_hist_11", hist_name=hist_11_name)
        graph.create_hist(r["l_hist"][1], path=p+"/lector/lector_hist_12", hist_name=hist_12_name)
        pr = {mask["l_y_n"][i]:r["l_pr"][i] for i in range(len(mask["l_y_n"]))}
        info = {"l_full_name":teacher[1], "number_of_votes_as_l":r["num_l"]}
        json.dump({**info,**pr}, open(p+"/lector/"+str(teacher[0]) + "_l.json", "w", encoding="utf-8"), indent=10)
        print("[INFO] Lecture " + fq + "|"+teacher[1] + " created")

    if r["num_p"] >= 3:
        ch_cr(p+"/practice")
        graph.create_radar("p", r["p_rad"], path=p+"/practice/practice_rad")
        graph.create_hist(r["p_hist"][0], path=p+"/practice/practice_hist_11", hist_name=hist_11_name)
        graph.create_hist(r["p_hist"][1], path=p+"/practice/practice_hist_12", hist_name=hist_12_name)
        pr={mask["p_y_n"][i]:r["p_pr"][i] for i in range(len(mask["p_y_n"]))}
        info={"p_full_name":teacher[1], "number_of_votes_as_p":r["num_p"]}
        json.dump({**info, **pr}, open(p+"/practice/" + str(teacher[0]) + "_p.json", "w", encoding="utf-8"), indent=10)
        print("[INFO] Practice " + fq + "|" + teacher[1] + " created")


def mainhandler():
    """
    Run thru all faculties existed in database
    Call faculty func
    Handle database connection
    """
    fq_list = []
    db = db_handle.connect(host, port, db_name, user, password)
    if db != "Exception":
        fq_list = db_handle.get_faculty_list(db)
        mask = db_handle.get_answer_mask(db)
        if debug:
            file = open("res_raw.txt", "w", encoding="utf-8")
            file.close()
            faculty(db, "fbme", mask)
        else:
            for i in fq_list:
                faculty(db, i, mask)
        db.close()

