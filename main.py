__author__ = 'jgentile'


import sys
import pekc_model
import json

def main():

    if len(sys.argv) < 2:
        print 'Usage main.py parameter_file'
        exit(0)

    parameter_filename = sys.argv[1]
    parameters = json.load(open(parameter_filename))

    print parameters


    output_filename = sys.argv[2]
    output_file = open(output_filename,'w')

    start = 0.0
    stop = 1.0
    step = 0.1
    iteration = start

    
    while iteration <= stop:

        if iteration > 0.8:
            print 'here'
            step = 0.01


        for i in range(0,20):
            print iteration,',',i,step

            preface = str(iteration)+','+str(i)
            parameters['progeny_generator']['preference'] = iteration
            m = pekc_model.Model(parameters,preface,output_file)
            m.run()

        iteration += step

    for i in range(0,20):
            preface = str(-1)+','+str(i)
            print 'one_to_one',',',i
            parameters['progeny_generator']['type'] = 'one_to_one'
            m = pekc_model.Model(parameters,preface,output_file)
            m.run()



    #m.run()




if __name__ == '__main__':
    main()