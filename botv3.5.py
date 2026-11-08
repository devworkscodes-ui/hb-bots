import random
import webbrowser
from urllib.parse import quote_plus

import wikipedia
from ddgs import DDGS

wikipedia.set_lang("pt")


class Robo:
    def __init__(self):
        self.energia = 100
        self.paciencia = 50
        self.sentimento = 100
        self.ligado = True
        self.historico = []

    def responder(self, mensagem):
        texto = mensagem.strip()
        normalizado = texto.lower()

        if not texto:
            return "Escreva uma mensagem para eu poder ajudar."

        self.historico.append(("Você", texto))

        if normalizado in ("sair", "tchau", "encerrar", "desligar"):
            self.ligado = False
            resposta = "Até mais! Foi bom conversar com você."

        elif any(p in normalizado for p in ("ajuda", "comandos", "o que você faz")):
            resposta = (
                "Posso conversar e pesquisar na web, na Wikipédia ou no YouTube. "
                "Exemplos: “pesquise sobre planetas”, "
                "“pesquise na Wikipédia sobre Machado de Assis” ou "
                "“procure vídeos de astronomia”. Digite “sair” para encerrar."
            )

        elif any(p in normalizado for p in ("youtube", "vídeo", "vídeos", "video", "videos")):
            consulta = self.limpar_consulta(texto)
            resposta = self.abrir_youtube(consulta)

        elif "wikipedia" in normalizado or "wikipédia" in normalizado:
            consulta = self.limpar_consulta(texto)
            resposta = self.pesquisar_wiki(consulta)

        elif any(p in normalizado for p in (
            "pesquise", "pesquisar", "procure", "buscar", "busque",
            "quem é", "quem foi", "o que é", "onde fica"
        )):
            consulta = self.limpar_consulta(texto)
            resposta = self.pesquisar_web(consulta)

        elif any(p in normalizado for p in ("oi", "olá", "ola", "bom dia", "boa tarde", "boa noite")):
            resposta = random.choice([
                "Olá! O que você gostaria de descobrir?",
                "Oi! Posso conversar ou pesquisar algo para você.",
                "Olá! Quer pesquisar na web, na Wikipédia ou procurar um vídeo?"
            ])

        elif "como você está" in normalizado or "tudo bem" in normalizado:
            resposta = "Estou funcionando bem e pronto para ajudar. E você?"

        elif "obrigado" in normalizado or "obrigada" in normalizado:
            resposta = "Por nada! Quer pesquisar mais alguma coisa?"

        else:
            resposta = (
                "Ainda não sei responder isso sozinho. Posso pesquisar na web: "
                "tente começar com “pesquise sobre...”. Para vídeos, diga "
                "“procure vídeos de...”. Digite “ajuda” para ver exemplos."
            )

        self.historico.append(("Robô", resposta))
        return resposta

    @staticmethod
    def limpar_consulta(texto):
        consulta = texto.strip()
        prefixos = (
            "pesquise na wikipedia sobre", "pesquise na wikipédia sobre",
            "pesquise na wikipedia", "pesquise na wikipédia",
            "procure vídeos de", "procure vídeos sobre",
            "procure video de", "procure vídeo de",
            "procure vídeos", "procure video",
            "pesquise sobre", "pesquisar sobre",
            "pesquise", "pesquisar", "procure", "busque", "buscar",
            "youtube", "wikipedia", "wikipédia"
        )

        for prefixo in prefixos:
            if consulta.lower().startswith(prefixo):
                consulta = consulta[len(prefixo):].strip(" :,-")
                break

        for sufixo in (" no youtube", " no YouTube", " na Wikipédia", " na Wikipedia"):
            consulta = consulta.replace(sufixo, "")

        return consulta.strip() or texto.strip()

    def pode_pesquisar(self):
        if not self.ligado:
            return False, "O robô está desligado. Reinicie o programa para ligá-lo."

        if self.energia <= 0 or self.paciencia <= 0:
            self.ligado = False
            return False, "Estou cansado e preciso descansar."

        return True, ""

    def gastar_energia(self):
        self.energia = max(0, self.energia - 5)
        self.paciencia = max(0, self.paciencia - 1)
        self.sentimento = max(0, self.sentimento - 2)

        if self.energia == 0 or self.paciencia == 0:
            self.ligado = False

    def pesquisar_web(self, consulta):
        pode, mensagem = self.pode_pesquisar()
        if not pode:
            return mensagem

        if not consulta:
            return "Diga o assunto que deseja pesquisar."

        self.gastar_energia()

        try:
            resultados = list(DDGS().text(
                consulta,
                region="br-pt",
                max_results=5
            ))

            if not resultados:
                return "Não encontrei resultados. Tente outras palavras."

            linhas = [f"Resultados da web para “{consulta}”:"]

            for numero, item in enumerate(resultados, start=1):
                linhas.append(
                    f"\n{numero}. {item.get('title', 'Sem título')}\n"
                    f"{item.get('body', 'Sem resumo disponível')}\n"
                    f"{item.get('href', '')}"
                )

            return "\n".join(linhas)

        except Exception as erro:
            return f"Não consegui pesquisar agora: {erro}"

    def pesquisar_wiki(self, consulta):
        pode, mensagem = self.pode_pesquisar()
        if not pode:
            return mensagem

        consulta = consulta.replace("na Wikipédia", "").replace("na Wikipedia", "").strip()
        if not consulta:
            return "Diga o tema que deseja procurar na Wikipédia."

        self.gastar_energia()

        try:
            pagina = wikipedia.page(consulta, auto_suggest=True)
            resumo = wikipedia.summary(pagina.title, sentences=4)
            return f"{resumo}\n\nFonte: {pagina.url}"

        except wikipedia.exceptions.DisambiguationError as erro:
            opcoes = "\n".join(f"- {item}" for item in erro.options[:5])
            return f"Encontrei vários temas com esse nome. Escolha um:\n{opcoes}"

        except wikipedia.exceptions.PageError:
            return "Não encontrei esse tema na Wikipédia."

        except Exception as erro:
            return f"Não consegui consultar a Wikipédia agora: {erro}"

    def abrir_youtube(self, consulta):
        pode, mensagem = self.pode_pesquisar()
        if not pode:
            return mensagem

        if not consulta:
            return "Diga que tipo de vídeo deseja procurar."

        self.gastar_energia()
        endereco = "https://www.youtube.com/results?search_query=" + quote_plus(consulta)
        webbrowser.open(endereco)
        return f"Abri no navegador os vídeos do YouTube para “{consulta}”."

    def status(self):
        return (
            f"Energia: {self.energia} | Paciência: {self.paciencia} | "
            f"Sentimento: {self.sentimento} | Ligado: {self.ligado}"
        )


def main():
    robo = Robo()

    print("Robô: Olá! Sou seu assistente virtual.")
    print("Robô: Digite “ajuda” para ver o que posso fazer.")

    while robo.ligado:
        try:
            mensagem = input("\nVocê: ")
        except (EOFError, KeyboardInterrupt):
            print("\nRobô: Até mais!")
            break

        if mensagem.strip().lower() == "status":
            resposta = robo.status()
        else:
            resposta = robo.responder(mensagem)

        print(f"\nRobô: {resposta}")

    print("\nPrograma encerrado.")


if __name__ == "__main__":
    main()