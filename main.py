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

    start = 0
    stop = 1
    step = 0.1
    iteration = start

    while iteration <= stop:


        for i in range(0,20):
            print iteration

            preface = str(iteration)+','+str(i)
            parameters['progeny_generator']['preference'] = iteration
            m = pekc_model.Model(parameters,preface,output_file)
            m.run()

        iteration +=step



    #m.run()




if __name__ == '__main__':
    main()