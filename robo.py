import wikipedia
wikipedia.set_lang("pt")
class Robo:
     def __init__(self):
        self.bateria = 100
        self.temperatura = 30
        self.armazenamento = 50
        self.ligado = False
     def ligar(self):
         self.ligado = True
         print("robo ligado")
     def pesquisar(self):
         if self.ligado == False:
             print("ainda não ligou")
         else:
            self.bateria = self.bateria - 5
            if self.bateria <= 0:
                self.ligado = False
                print("bateria fraca, desligando!", self.bateria)
            self.armazenamento = self.armazenamento - 1
            if self.armazenamento <= 0:
                self.ligado = False
                print("Armazenamento cheio!")
            elif self.armazenamento == 10:
                print("Armazenamento quase cheio!", self.armazenamento)
            self.temperatura = self.temperatura + 5
            if self.temperatura >= 100:
                self.ligado = False
                print("Temperatura em estado critico, DESLIGANDO!")
            elif self.temperatura >= 80:
                print("Temperatura muito alta!", self.temperatura)
         pesquisa = input(print("O que você deseja pesquisar?  "))
         resultado = wikipedia.summary(pesquisa)
         print("\033[34m" + resultado + "\033[32m")
     def desligar(self):
         if self.ligado == False:
             print("ainda não ligou")
         else:
            self.ligado = False
            print("Desligando")


meu_robo = Robo()
while True:
    comando = input("O que você deseja fazer? : ")
    if comando == "ligar":
        meu_robo.ligar()
    elif comando == "pesquisar":
        meu_robo.pesquisar()
    elif comando == "desligar":
        meu_robo.desligar()
        break
    if meu_robo.ligado == False:
        break