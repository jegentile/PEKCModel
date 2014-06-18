__author__ = 'jgentile'


import sys
import peck_model

def main():

    if len(sys.argv) < 2:
        print 'Usage main.py parameter_file'
        exit(0)

    parameter_filename = sys.argv[1]
    print parameter_filename

    m = peck_model.Model(parameter_filename)

    m.run()




if __name__ == '__main__':
    main()