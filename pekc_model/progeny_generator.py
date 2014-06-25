__author__ = 'jgentile'

import progeny_generators


class ProgenyGenerator:
    def __init__(self,params,model):
        self.__model = model

        if params['type']=='one_to_one':
            self.__generator = progeny_generators.OneToOne(params,model)

    def make_next_generation(self):
        return self.__generator.make_next_generation()

