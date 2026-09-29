import spacy


class SentimentAnalyzer:
    """
    Analisador simples de sentimento em português.

    Utiliza spaCy para processamento linguístico
    e um léxico de polaridade para classificação.
    """

    POSITIVE_WORDS = {
        "excelente",
        "ótimo",
        "ótima",
        "otimo",
        "otima",
        "bom",
        "boa",
        "maravilhoso",
        "maravilhosa",
        "perfeito",
        "perfeita",
        "incrível",
        "incrivel",
        "adorei",
        "adorar",
        "amo",
        "amar",
        "gostei",
        "gostar",
        "satisfeito",
        "satisfeita",
        "feliz",
        "rápido",
        "rapido",
        "eficiente",
        "recomendo",
        "recomendar",
        "qualidade",
        "parabéns",
        "parabens",
        "fantástico",
        "fantastica",
        "fantástico",
        "fantastico",
        "útil",
        "util",
        "facilidade",
        "facil",
        "seguro",
        "segura",
    }

    NEGATIVE_WORDS = {
        "ruim",
        "péssimo",
        "péssima",
        "pessimo",
        "pessima",
        "horrível",
        "horrivel",
        "terrível",
        "terrivel",
        "odiei",
        "odiar",
        "odeio",
        "problema",
        "problemas",
        "erro",
        "erros",
        "lento",
        "lenta",
        "demorado",
        "demorada",
        "insatisfeito",
        "insatisfeita",
        "frustrado",
        "frustrada",
        "decepcionado",
        "decepcionada",
        "defeito",
        "defeituoso",
        "falha",
        "falhou",
        "cancelar",
        "cancelamento",
        "caro",
        "cara",
        "difícil",
        "dificil",
        "péssimo",
        "pessimo",
        "enganado",
        "enganada",
        "atraso",
        "atrasado",
    }

    NEGATIONS = {
        "não",
        "nao",
        "nunca",
        "jamais",
        "nem",
        "nada",
    }

    INTENSIFIERS = {
        "muito": 1.5,
        "muita": 1.5,
        "muitos": 1.5,
        "muitas": 1.5,
        "super": 1.5,
        "extremamente": 2.0,
        "realmente": 1.3,
        "bastante": 1.3,
    }

    def __init__(self):
        try:
            self.nlp = spacy.load("pt_core_news_sm")
        except OSError:
            self.nlp = spacy.blank("pt")

    def analyze(self, text):
        """
        Analisa o sentimento do texto.
        """

        if not isinstance(text, str):
            raise ValueError("O texto precisa ser uma string.")

        text = text.strip()

        if not text:
            raise ValueError("O comentário não pode estar vazio.")

        if len(text) > 2000:
            raise ValueError(
                "O comentário não pode ultrapassar 2000 caracteres."
            )

        doc = self.nlp(text)

        score = 0.0
        positive_count = 0
        negative_count = 0

        tokens = list(doc)

        for index, token in enumerate(tokens):

            if token.is_space or token.is_punct:
                continue

            word = token.lemma_.lower().strip()

            # Caso o modelo não tenha lematização disponível
            if not word:
                word = token.text.lower().strip()

            # Verifica negação nas duas palavras anteriores
            previous_tokens = tokens[max(0, index - 2):index]

            has_negation = any(
                previous.lemma_.lower() in self.NEGATIONS
                or previous.text.lower() in self.NEGATIONS
                for previous in previous_tokens
            )

            # Intensificador imediatamente anterior
            multiplier = 1.0

            if index > 0:
                previous_word = tokens[index - 1].lemma_.lower()

                multiplier = self.INTENSIFIERS.get(
                    previous_word,
                    1.0
                )

            if word in self.POSITIVE_WORDS:

                value = 1.0 * multiplier

                if has_negation:
                    value *= -1
                    negative_count += 1
                else:
                    positive_count += 1

                score += value

            elif word in self.NEGATIVE_WORDS:

                value = -1.0 * multiplier

                if has_negation:
                    value *= -1
                    positive_count += 1
                else:
                    negative_count += 1

                score += value

        if score > 0:
            sentimento = "positivo"

        elif score < 0:
            sentimento = "negativo"

        else:
            sentimento = "neutro"

        return {
            "sentimento": sentimento,
            "score": round(score, 2),
            "positive_count": positive_count,
            "negative_count": negative_count,
        }


analyzer = SentimentAnalyzer()
