__author__ = 'jgentile'

import progeny_generators


class ProgenyGenerator:
    def __init__(self,params,model):
        self.__model = model

        if params['type']=='one_to_one':
            self.__generator = progeny_generators.OneToOne(params,model)
        if params['type']=='random_marriange':
            self.__generator = progeny_generators.RandomMarriage(params,model)
        if params['type']=='assortative':
            self.__generator = progeny_generators.AssortativeMating(params,model)



    def make_next_generation(self):
        return self.__generator.make_next_generation()

