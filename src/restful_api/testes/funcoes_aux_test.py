# -*- coding: utf-8 -*-
import sys
sys.path.append("../api")
import unittest
import datetime
import funcoes_aux


'''
    Para rodar este test deve-se comentar os imports da funcoes_aux
    import bd
    from api import app
    from flask import abort, request, make_response,Response
'''
class FuncoesAuxTest(unittest.TestCase):

    def test_create_travels_comparison(self):
        # Testar se a função é injetora(onde cada x tem um y diferente)
        travels = [{'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}]
        frame_schedules = [{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}]
        actual = funcoes_aux.create_travels_comparison(travels, frame_schedules)
        expected = [({'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)},{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'is_paired': True,'chegada': datetime.timedelta(0, 26105, 331753)})]
        self.assertEquals(expected, actual)

        travels = [{'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, {'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}]
        frame_schedules = [{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}]
        actual = funcoes_aux.create_travels_comparison(travels, frame_schedules)
        expected = [({'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)},{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'is_paired': True,'chegada': datetime.timedelta(0, 26105, 331753)}), ({'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, None)]
        self.assertEquals(expected, actual)

        #Testa os 5 minutos antes
        travels = [{'saida': datetime.timedelta(0, 19988, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}]
        frame_schedules = [{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}]
        actual = funcoes_aux.create_travels_comparison(travels, frame_schedules)
        expected = [({'saida': datetime.timedelta(0, 19988, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)},{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'is_paired': True,'chegada': datetime.timedelta(0, 26105, 331753)})]
        self.assertNotEquals(expected, actual)

        travels = [{'saida': datetime.timedelta(0, 19989, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}]
        frame_schedules = [{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}]
        actual = funcoes_aux.create_travels_comparison(travels, frame_schedules)
        expected = [({'saida': datetime.timedelta(0, 19989, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)},{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'is_paired': True,'chegada': datetime.timedelta(0, 26105, 331753)})]
        self.assertEquals(expected, actual)

        #Testa os 5 minutos depois
        travels = [{'saida': datetime.timedelta(0, 20590, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}]
        frame_schedules = [{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}]
        actual = funcoes_aux.create_travels_comparison(travels, frame_schedules)
        expected = [({'saida': datetime.timedelta(0, 20590, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)},{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'is_paired': True,'chegada': datetime.timedelta(0, 26105, 331753)})]
        self.assertNotEquals(expected, actual)

        travels = [{'saida': datetime.timedelta(0, 20589, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}]
        frame_schedules = [{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}]
        actual = funcoes_aux.create_travels_comparison(travels, frame_schedules)
        expected = [({'saida': datetime.timedelta(0, 20589, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)},{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'is_paired': True,'chegada': datetime.timedelta(0, 26105, 331753)})]
        self.assertEquals(expected, actual)

        # Testar quando tem o mesmo número de x e y (testar quando tem viagens a mais)
        travels = [{'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, {'saida': datetime.timedelta(0, 12345, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}]
        frame_schedules = [{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}, {'duracao': 70L, 'saida': datetime.timedelta(0, 20999, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}]
        actual = funcoes_aux.create_travels_comparison(travels, frame_schedules)
        expected = [({'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)},{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'is_paired': True,'chegada': datetime.timedelta(0, 26105, 331753)}),({'saida': datetime.timedelta(0, 12345, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, None), (None, {'duracao': 70L, 'saida': datetime.timedelta(0, 20999, 668246),'is_paired': False, 'chegada': datetime.timedelta(0, 26105, 331753)})]
        self.assertEquals(expected, actual)

        travels = [{'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, {'saida': datetime.timedelta(0, 12345, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, {'saida': datetime.timedelta(0, 20000, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}]
        frame_schedules = [{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}, {'duracao': 80L, 'saida': datetime.timedelta(0, 19800, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}, {'duracao': 70L, 'saida': datetime.timedelta(0, 20999, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}]
        actual = funcoes_aux.create_travels_comparison(travels, frame_schedules)
        expected = [({'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)},{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'is_paired': True,'chegada': datetime.timedelta(0, 26105, 331753)}),({'saida': datetime.timedelta(0, 12345, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, None), ({'saida': datetime.timedelta(0, 20000, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, {'duracao': 80L, 'saida': datetime.timedelta(0, 19800, 668246),'is_paired': True, 'chegada': datetime.timedelta(0, 26105, 331753)}), (None, {'duracao': 70L, 'saida': datetime.timedelta(0, 20999, 668246),'is_paired': False, 'chegada': datetime.timedelta(0, 26105, 331753)})]
        self.assertEquals(expected, actual)

        # Testar quando tem o mesmo número de x e y (testar quando tem viagens a menos)
        travels = [{'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}]
        frame_schedules = [{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}, {'duracao': 70L, 'saida': datetime.timedelta(0, 20999, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}]
        actual = funcoes_aux.create_travels_comparison(travels, frame_schedules)
        expected = [({'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)},{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'is_paired': True,'chegada': datetime.timedelta(0, 26105, 331753)}),(None, {'duracao': 70L, 'saida': datetime.timedelta(0, 20999, 668246),'is_paired': False, 'chegada': datetime.timedelta(0, 26105, 331753)})]
        self.assertEquals(expected, actual)

        # Testar quando tem mais x do que y (deve ter viagens a mais)
        travels = [{'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, {'saida': datetime.timedelta(0, 12345, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}]
        frame_schedules = [{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}]
        actual = funcoes_aux.create_travels_comparison(travels, frame_schedules)
        expected = [({'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)},{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'is_paired': True,'chegada': datetime.timedelta(0, 26105, 331753)}),({'saida': datetime.timedelta(0, 12345, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, None)]
        self.assertEquals(expected, actual)

        travels = [{'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, {'saida': datetime.timedelta(0, 12345, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, {'saida': datetime.timedelta(0, 20000, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}]
        frame_schedules = [{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}]
        actual = funcoes_aux.create_travels_comparison(travels, frame_schedules)
        expected = [({'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)},{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'is_paired': True,'chegada': datetime.timedelta(0, 26105, 331753)}),({'saida': datetime.timedelta(0, 12345, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, None), ({'saida': datetime.timedelta(0, 20000, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, None)]
        self.assertEquals(expected, actual)

        travels = [{'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, {'saida': datetime.timedelta(0, 12345, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, {'saida': datetime.timedelta(0, 20000, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}]
        frame_schedules = [{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}, {'duracao': 80L, 'saida': datetime.timedelta(0, 19800, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}]
        actual = funcoes_aux.create_travels_comparison(travels, frame_schedules)
        expected = [({'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)},{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'is_paired': True,'chegada': datetime.timedelta(0, 26105, 331753)}),({'saida': datetime.timedelta(0, 12345, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, None), ({'saida': datetime.timedelta(0, 20000, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, {'duracao': 80L, 'saida': datetime.timedelta(0, 19800, 668246),'is_paired': True, 'chegada': datetime.timedelta(0, 26105, 331753)})]
        self.assertEquals(expected, actual)

        # Testar quando tem mais x do que y (testar quando tem viagens a menos)

        travels = [{'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, {'saida': datetime.timedelta(0, 12345, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, {'saida': datetime.timedelta(0, 20000, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}]
        frame_schedules = [{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}, {'duracao': 80L, 'saida': datetime.timedelta(0, 19500, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}]
        actual = funcoes_aux.create_travels_comparison(travels, frame_schedules)
        expected = [({'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)},{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'is_paired': True,'chegada': datetime.timedelta(0, 26105, 331753)}),({'saida': datetime.timedelta(0, 12345, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, None), ({'saida': datetime.timedelta(0, 20000, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}, None),(None, {'duracao': 80L, 'saida': datetime.timedelta(0, 19500, 668246),'is_paired': False, 'chegada': datetime.timedelta(0, 26105, 331753)})]
        self.assertEquals(expected, actual)

        # Testar quando tem menos x do que y (deve ter viagens a menos)
        travels = [{'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}]
        frame_schedules = [{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}, {'duracao': 80L, 'saida': datetime.timedelta(0, 19500, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}]
        actual = funcoes_aux.create_travels_comparison(travels, frame_schedules)
        expected = [({'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)},{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'is_paired': True,'chegada': datetime.timedelta(0, 26105, 331753)}),(None, {'duracao': 80L, 'saida': datetime.timedelta(0, 19500, 668246),'is_paired': False, 'chegada': datetime.timedelta(0, 26105, 331753)})]
        self.assertEquals(expected, actual)

        #dois y pra um x
        travels = [{'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)}]
        frame_schedules = [{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}, {'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'chegada': datetime.timedelta(0, 26105, 331753)}]
        actual = funcoes_aux.create_travels_comparison(travels, frame_schedules)
        expected = [({'saida': datetime.timedelta(0, 20289, 668246), 'chegada': datetime.timedelta(0, 26105, 331753)},{'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'is_paired': True,'chegada': datetime.timedelta(0, 26105, 331753)}),(None, {'duracao': 70L, 'saida': datetime.timedelta(0, 20289, 668246),'is_paired': False, 'chegada': datetime.timedelta(0, 26105, 331753)})]
        self.assertEquals(expected, actual)

if __name__ == '__main__':
    unittest.main()

