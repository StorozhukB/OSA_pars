from threading_handle import mainhandler
import time

def main():
    """
    main function of program 
    Also output time of life for all program
    """
    start=time.time()
    mainhandler()
    print("[INFO] Program runs ",time.time()-start," s")
    pass

if __name__=="__main__":
    main()