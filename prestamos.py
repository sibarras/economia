import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Prestamo:
    def __init__(self, valor_inicial: float, interes: float, anos: int):
        self.VALOR_INICIAL = valor_inicial
        self.INTERES = interes
        self.ANOS = anos
        
        # non-constants
        self.__porcentaje_inicial: float = 5.

    @property
    def porcentaje_inicial(self):
        return self.__porcentaje_inicial        

    @porcentaje_inicial.setter
    def porcentaje_inicial(self, porcentaje_inicial: float):
        assert isinstance(porcentaje_inicial, float)
        self.__porcentaje_inicial = porcentaje_inicial
    
    @porcentaje_inicial.getter
    def porcentaje_inicial(self) -> float:
        return self.__porcentaje_inicial

    @property
    def crecimiento_de_valor(self) -> float:
        i = self.INTERES / (100 * 12)
        n = self.ANOS * 12
        return np.power(1 + i, n)

    @property
    def valor_prestado(self) -> float:
        ci = self.VALOR_INICIAL
        pi = self.__porcentaje_inicial / 100
        return ci * (1 - pi)
        
    @property
    def valor_final(self) -> float:
        return self.valor_prestado * self.crecimiento_de_valor

    @property
    def letra_por_dolar(self) -> float:
        i = self.INTERES / (100 * 12)
        n = self.ANOS * 12
        return self.crecimiento_de_valor * i / (self.crecimiento_de_valor - 1)

    @property
    def letra(self) -> float:
        return self.valor_prestado * self.letra_por_dolar

    def calcular_interes(self):
        n = self.ANOS * 12
        return np.log(self.letra * n / self.valor_prestado) / n

    def get_recursive_visualization(self, mensualidad=None) -> pd.DataFrame:
        mensualidad = self.letra if mensualidad == None else mensualidad
        assert isinstance(mensualidad, float) or isinstance(mensualidad, int)
        interes = self.INTERES/(12*100)
        month_data = {
            'deuda': self.valor_prestado,
            'mensualidad': 0,
            'pagado': 0,
            'impuesto generado': 0,
            'impuesto acumulado': 0,
            'descontado de la deuda': 0,
            'balance neto': self.valor_prestado
        }
        ans = pd.DataFrame(columns=month_data.keys()).append(month_data, ignore_index=True)
        
        for i in range(self.ANOS * 12):
            balance_neto = month_data['balance neto'] - (mensualidad - month_data['balance neto'] * interes)
            mensualidad = mensualidad if balance_neto >= 0 else month_data['balance neto'] + balance_neto
            month_data = {
                'deuda': month_data['balance neto'],
                'mensualidad': mensualidad,
                'pagado': month_data['pagado'] + mensualidad,
                'impuesto generado': month_data['balance neto'] * interes,
                'impuesto acumulado': month_data['impuesto acumulado'] + month_data['balance neto'] * interes,
                'descontado de la deuda': mensualidad - month_data['balance neto'] * interes,
                'balance neto': balance_neto if balance_neto > 0.0001 else 0
            }
            ans = ans.append(month_data, ignore_index=True)
            if month_data['balance neto'] == 0: break
        return ans
            

if __name__ == "__main__":
    from pandas.plotting import table
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
    
    print("\n=====================\n")
    pagos = p1.get_recursive_visualization(mensualidad=758.40)
    print('pagos:\n\n', pagos)
    pagos[['impuesto generado', 'mensualidad', 'descontado de la deuda']].plot()
    plt.show()
