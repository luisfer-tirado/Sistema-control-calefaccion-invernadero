''' instalar dependencias
pip install -U scikit-fuzzy
pip install matplotlib '''

# importar librerías
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# creación de la clase
class sistema_control_difuso():

    # metodo constructor
    def __init__(self):
        # variables de entrada (antecedentes)
        self.temperatura = ctrl.Antecedent(np.arange(0, 41, 1), 'temperatura')
        self.humedad = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad')

        # variable de salida (consecuente)
        self.variacion = ctrl.Consequent(np.arange(-15, 16, 0.5), 'variacion')

        # funciones de pertenencia
        self.funciones_pertenencia_temperatura()
        self.funciones_pertenencia_humedad()
        self.funciones_pertenencia_variacion()

        # reglas difusas
        self.reglas_difusas()

        # sistema del control
        self.sistema_control()


    # asignando funciones de pertenencia a la variable temperatura
    def funciones_pertenencia_temperatura(self):
        # Temperatura: Se asumen 5 términos lingüísticos: Muy Baja (MB), Baja (B), Normal (N), Alta (A) y Muy Alta (MA).

        self.temperatura['MB'] = fuzz.trapmf(self.temperatura.universe, [0, 0, 10, 15])
        self.temperatura['B'] = fuzz.trimf(self.temperatura.universe, [10, 15, 20])
        self.temperatura['N'] = fuzz.trimf(self.temperatura.universe, [18, 20, 22])
        self.temperatura['A'] = fuzz.trimf(self.temperatura.universe, [20, 25, 30])
        self.temperatura['MA'] = fuzz.trapmf(self.temperatura.universe, [25, 30, 40, 40])


    # asignando funciones de pertenencia a la variable humedad
    def funciones_pertenencia_humedad(self):
        # Humedad: Se asumen 5 términos lingüísticos: Muy Baja (MB), Baja(B), Normal (N), Alta (A) y Muy Alta (MA).

        self.humedad['MB'] = fuzz.trapmf(self.humedad.universe, [0, 0, 10, 20])
        self.humedad['B'] = fuzz.trimf(self.humedad.universe, [10, 25, 40])
        self.humedad['N'] = fuzz.trimf(self.humedad.universe, [30, 40, 50])
        self.humedad['A'] = fuzz.trimf(self.humedad.universe, [40, 55, 70])
        self.humedad['MA'] = fuzz.trapmf(self.humedad.universe, [60, 70, 100, 100])


    # asignando funciones de pertenencia a la variable variacion
    def funciones_pertenencia_variacion(self):
        # Variación de temperatura: Se asumen 7 términos lingüísticos: Bajada Grande (BG), Bajada Normal (BN), Bajada Pequeña (BP), Mantener (M), Subida Pequeña (SP), Subida Normal (SN) y Subida Grande (SG).

        self.variacion['BG'] = fuzz.trimf(self.variacion.universe, [-15, -10, -7.5])
        self.variacion['BN'] = fuzz.trimf(self.variacion.universe, [-10, -5, -2.5])
        self.variacion['BP'] = fuzz.trimf(self.variacion.universe, [-7.5, -2.5, 0])
        self.variacion['M'] = fuzz.trimf(self.variacion.universe, [-1, 0, 1])
        self.variacion['SP'] = fuzz.trimf(self.variacion.universe, [0, 2.5, 7.5])
        self.variacion['SN'] = fuzz.trimf(self.variacion.universe, [2.5, 5, 10])
        self.variacion['SG'] = fuzz.trimf(self.variacion.universe, [7.5, 10, 15])


    # declaración de reglas difusas
    def reglas_difusas(self):
        self.r01 = ctrl.Rule(antecedent=(self.temperatura['MB'] & self.humedad['MB']),
                            consequent=self.variacion['SN'])

        self.r02 = ctrl.Rule(antecedent=(self.temperatura['MB'] & self.humedad['B']),
                            consequent=self.variacion['SN'])

        self.r03 = ctrl.Rule(antecedent=(self.temperatura['MB'] & self.humedad['N']),
                            consequent=self.variacion['SG'])

        self.r04 = ctrl.Rule(antecedent=(self.temperatura['MB'] & self.humedad['A']),
                            consequent=self.variacion['SG'])

        self.r05 = ctrl.Rule(antecedent=(self.temperatura['MB'] & self.humedad['MA']),
                            consequent=self.variacion['SG'])
        #-----------------------------------------------------------------------
        self.r06 = ctrl.Rule(antecedent=(self.temperatura['B'] & self.humedad['MB']),
                            consequent=self.variacion['M'])

        self.r07 = ctrl.Rule(antecedent=(self.temperatura['B'] & self.humedad['B']),
                            consequent=self.variacion['M'])

        self.r08 = ctrl.Rule(antecedent=(self.temperatura['B'] & self.humedad['N']),
                            consequent=self.variacion['SP'])

        self.r09 = ctrl.Rule(antecedent=(self.temperatura['B'] & self.humedad['A']),
                            consequent=self.variacion['SP'])

        self.r10 = ctrl.Rule(antecedent=(self.temperatura['B'] & self.humedad['MA']),
                            consequent=self.variacion['SN'])
        #-----------------------------------------------------------------------
        self.r11 = ctrl.Rule(antecedent=(self.temperatura['N'] & self.humedad['MB']),
                            consequent=self.variacion['M'])

        self.r12 = ctrl.Rule(antecedent=(self.temperatura['N'] & self.humedad['B']),
                            consequent=self.variacion['M'])

        self.r13 = ctrl.Rule(antecedent=(self.temperatura['N'] & self.humedad['N']),
                            consequent=self.variacion['M'])

        self.r14 = ctrl.Rule(antecedent=(self.temperatura['N'] & self.humedad['A']),
                            consequent=self.variacion['M'])

        self.r15 = ctrl.Rule(antecedent=(self.temperatura['N'] & self.humedad['MA']),
                            consequent=self.variacion['BP'])
        #-----------------------------------------------------------------------
        self.r16 = ctrl.Rule(antecedent=(self.temperatura['A'] & self.humedad['MB']),
                            consequent=self.variacion['M'])

        self.r17 = ctrl.Rule(antecedent=(self.temperatura['A'] & self.humedad['B']),
                            consequent=self.variacion['M'])

        self.r18 = ctrl.Rule(antecedent=(self.temperatura['A'] & self.humedad['N']),
                            consequent=self.variacion['BP'])

        self.r19 = ctrl.Rule(antecedent=(self.temperatura['A'] & self.humedad['A']),
                            consequent=self.variacion['BP'])

        self.r20 = ctrl.Rule(antecedent=(self.temperatura['A'] & self.humedad['MA']),
                            consequent=self.variacion['BN'])
        #-----------------------------------------------------------------------
        self.r21 = ctrl.Rule(antecedent=(self.temperatura['MA'] & self.humedad['MB']),
                            consequent=self.variacion['BP'])

        self.r22 = ctrl.Rule(antecedent=(self.temperatura['MA'] & self.humedad['B']),
                            consequent=self.variacion['BN'])

        self.r23 = ctrl.Rule(antecedent=(self.temperatura['MA'] & self.humedad['N']),
                            consequent=self.variacion['BN'])

        self.r24 = ctrl.Rule(antecedent=(self.temperatura['MA'] & self.humedad['A']),
                            consequent=self.variacion['BG'])

        self.r25 = ctrl.Rule(antecedent=(self.temperatura['MA'] & self.humedad['MA']),
                            consequent=self.variacion['BG'])


    # creación del sistema de control y asignación de las reglas difusas
    def sistema_control(self):
        self.sistema_ctrl = ctrl.ControlSystem(rules=[self.r01, self.r02, self.r03, self.r04, self.r05,
                                                     self.r06, self.r07, self.r08, self.r09, self.r10,
                                                     self.r11, self.r12, self.r13, self.r14, self.r15,
                                                     self.r16, self.r17, self.r18, self.r19, self.r20,
                                                     self.r21, self.r22, self.r23, self.r24, self.r25])


    # simulación del sistema de control difusa asignando entradas
    def simulacion(self, temperatura, humedad):
        sistema = ctrl.ControlSystemSimulation(self.sistema_ctrl)

        sistema.input['temperatura'] = temperatura
        sistema.input['humedad'] = humedad

        sistema.compute()

        return sistema.output['variacion']

# Instancia de la clase
# sistema = sistema_control_difuso()
# print("La variacion es de: ", sistema.simulacion(25, 80))
