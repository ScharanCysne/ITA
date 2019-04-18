from environment import *

if __name__ == "__main__":

    #mode = "WITHOUT"
    #mode = "TEST_BLOCK"
    mode = "EVALUATION_OBJECT"

    environment = Environment(mode, False)
    time.sleep(10)

    while True: 
    
        environment.rotate_environment(dtheta, vs.vec(0, 1, 0), environment.lower_bar.pos)
        environment.action(vs.vec(0, 1, 0), environment.lower_bar.pos)
