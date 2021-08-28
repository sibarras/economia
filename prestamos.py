import matplotlib.pyplot as plt
import numpy as np

class Prestamo:
    def __init__(self, valor_inicial: float, interes: float, anos: int):
        self.VALOR_INICIAL = valor_inicial
        self.INTERES = interes
        self.ANOS = anos
        
        # non-constants
        self.__porcentaje_inicial: float = 0.

    @property
    def porcentaje_inicial(self):
        return self.__porcentaje_inicial        

    @porcentaje_inicial.setter
    def porcentaje_inicial(self, porcentaje_inicial: float):
        assert isinstance(porcentaje_inicial, float)
        self.__porcentaje_inicial = porcentaje_inicial
    
    @porcentaje_inicial.getter
    def porcentaje_inicial(self):
        return self.__porcentaje_inicial

    @property
    def crecimiento_de_valor(self):
        i = self.INTERES / (100 * 12)
        n = self.ANOS * 12
        return np.power(1 + i, n)

    @property
    def valor_prestado(self):
        ci = self.VALOR_INICIAL
        pi = self.__porcentaje_inicial / 100
        return ci * (1 - pi)
        
    @property
    def valor_final(self):
        return self.valor_prestado * self.crecimiento_de_valor

    @property
    def letra_por_dolar(self):
        i = self.INTERES / (100 * 12)
        n = self.ANOS * 12
        return self.crecimiento_de_valor * i / (self.crecimiento_de_valor - 1)

    @property
    def letra(self):
        return self.valor_prestado * self.letra_por_dolar

    def calcular_interes(self):
        n = self.ANOS * 12
        return np.log(self.letra * n / self.valor_prestado) / n

if __name__ == "__main__":
    p1 = Prestamo(159000, 6.025, 30)
    p1.porcentaje_inicial = 5.
    print('valor final:', p1.valor_final)
    print('valor inicial:', p1.VALOR_INICIAL)
    print('valor prestado:', p1.valor_prestado)
    print('porcentaje inicial pagado:', p1.porcentaje_inicial)
    print('letra:', p1.letra)
    total_pagado = p1.letra * p1.ANOS * 12
    print(f'total pagado:', total_pagado)
    print('crecimiento real:', total_pagado / p1.valor_prestado)
    print('crecimiento calculado:', p1.crecimiento_de_valor)
    print('calculo_de interes:', p1.calcular_interes() * 100 * 12)
    
