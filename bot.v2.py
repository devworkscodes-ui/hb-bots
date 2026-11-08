import wikipedia
wikipedia.set_lang("pt")
class Robo:
     def __init__(self):
        self.energia = 100
        self.sentimento = 100 #sentimento é a capacidade de sentir emoções, quanto mais alto, mais empático o robô é
        self.pasciencia = 50 #pasciencia é a capacidade de aprender, quanto mais alto, mais rápido o robô aprende
        self.ligado = False
     def ligar(self):
         self.ligado = True
         print("robo ligado")
     def pesquisar(self):
         if self.ligado == False:
             print("ainda não ligou")
         else:
            self.energia = self.energia - 5
            if self.energia <= 0:
                self.ligado = False
                print("estou cansado, energia baixa, desligando!", self.energia)
            self.pasciencia = self.pasciencia - 1
            if self.pasciencia <= 0:
                self.ligado = False
                print("estou confuso, pasciencia baixa, desligando!", self.pasciencia)
            elif self.pasciencia == 100:
                print("estou aprendendo, pasciencia alta!", self.pasciencia)
            self.sentimento = self.sentimento - 10
            if self.sentimento <= 0:
                self.ligado = False
                print("estou triste, sentimento baixo, desligando!", self.sentimento)
            elif self.sentimento >= 90:
                print("estou feliz, sentimento alto!", self.sentimento)
            pesquisa = input("")
            frase = pesquisa.split()
            inuteis = ["me", "fala", "sobre", "o", "a", "de", "do", "da", "que", "e", "com", "um", "uma", "para", "em", "no", "na", "se", "por", "ao", "as", "os", "dos", "das", "que", "como", "mas", "foi", "ser", "tem", "são", "eu", "você", "ele", "ela", "nós", "vocês", "eles", "elas", "meu", "minha", "meus", "minhas", "teus", "tuas", "seus", "suas", "nossos", "nossas", "vossos", "vossas", "oi", "olá", "bom", "boa", "tarde", "dia", "noite", "obrigado", "obrigada", "por favor", "desculpe", "com licença", "até logo", "adeus", "sim", "não", "talvez", "claro", "então", "mas", "porque", "quando", "onde", "quem", "como", "quanto", "qual", "quais", "ser", "estar", "está", "ter", "haver", "fazer",  "poder", "dizer", "ir", "ver", "dar", "saber", "querer", "chegar", "passar", "dever", "ficar", "trazer", "levar", "começar", "terminar", "gostar", "amar", "?", "!", ".", ",", ";", ":", "-", "_", "(", ")", "[", "]", "{", "}", "\"", "'", "“", "”", "‘", "’"]
            importantes = []
            for palavra in frase:
                if palavra not in inuteis:
                    importantes.append(palavra)
                    importantes2 = " ".join(importantes)
         resultado = wikipedia.summary(importantes2)
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


#pesquisa = input("")
#frase = pesquisa.split()
#print(frase)
#inuteis = ["me", "fala", "sobre", "o", "a", "de", "do", "da", "que", "e", "com", "um", "uma", "para", "em", "no", "na", "se", "por", "ao", "as", "os", "dos", "das", "que", "como", "mas", "foi", "ser", "tem", "são", "eu", "você", "ele", "ela", "nós", "vocês", "eles", "elas", "meu", "minha", "meus", "minhas", "teus", "tuas", "seus", "suas", "nossos", "nossas", "vossos", "vossas", "oi", "olá", "bom", "boa", "tarde", "dia", "noite", "obrigado", "obrigada", "por favor", "desculpe", "com licença", "até logo", "adeus", "sim", "não", "talvez", "claro", "então", "mas", "porque", "quando", "onde", "quem", "como", "quanto", "qual", "quais", "ser", "estar", "está", "ter", "haver", "fazer",  "poder", "dizer", "ir", "ver", "dar", "saber", "querer", "chegar", "passar", "dever", "ficar", "trazer", "levar", "começar", "terminar", "gostar", "amar", "?", "!", ".", ",", ";", ":", "-", "_", "(", ")", "[", "]", "{", "}", "\"", "'", "“", "”", "‘", "’"]
#importantes = []
#for palavra in frase:
    #if palavra not in inuteis:
        importantes.append(palavra)
