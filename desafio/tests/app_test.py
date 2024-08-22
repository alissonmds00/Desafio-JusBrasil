import unittest
from desafio.services.app import App

class TestApp(unittest.TestCase):

    def test_estado_invalido(self):
        numero_processo = '0000000-00.0000.0.00.0000'
        with self.assertRaises(ValueError) as context:
            app = App(numero_processo)
        self.assertEqual(str(context.exception), 'Estado não suportado')

    def test_numero_processo_invalido(self):
        numero_processo_curto = '1234567890123456789'  # 19 caracteres
        numero_processo_longo = '12345678901234567890123456'  # 26 caracteres

        with self.assertRaises(ValueError) as context:
            app = App(numero_processo_curto)
        self.assertEqual(str(context.exception), 'Código inválido')

        with self.assertRaises(ValueError) as context:
            app = App(numero_processo_longo)
        self.assertEqual(str(context.exception), 'O número deve ter exatamente 20 dígitos.')
    
    
    def test_numero_processo_inexistente(self):
        numero_processo = '07108025520188020009' #O último digito 9 é inválido
    
        app = App(numero_processo)
        resultado = app.iniciar_consulta()

        #Ele deve executar o navegador para crawling uma única vez
        self.assertIsNone(resultado) #Resultado deve ser nulo
            

if __name__ == '__main__':
    unittest.main()
