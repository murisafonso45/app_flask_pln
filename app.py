from flask import Flask, render_template, request, redirect, url_for, flash

from database import (
    init_database,
    salvar_comentario,
    listar_comentarios
)

from nlp_engine import analyzer


app = Flask(__name__)

# Em produção, coloque essa chave em variável de ambiente.
app.config["SECRET_KEY"] = "troque-esta-chave-em-producao"


@app.after_request
def add_security_headers(response):
    """
    Adiciona headers básicos de segurança.
    """

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response


@app.route("/", methods=["GET", "POST"])
def index():

    resultado = None

    if request.method == "POST":

        texto = request.form.get("comentario", "").strip()

        if not texto:
            flash("Digite um comentário para analisar.", "error")

        elif len(texto) > 2000:
            flash(
                "O comentário não pode ultrapassar 2000 caracteres.",
                "error"
            )

        else:
            try:

                resultado = analyzer.analyze(texto)

                salvar_comentario(
                    texto,
                    resultado["sentimento"],
                    resultado["score"]
                )

                flash(
                    "Comentário analisado com sucesso.",
                    "success"
                )

            except ValueError as error:

                flash(str(error), "error")

            except Exception:

                app.logger.exception(
                    "Erro durante análise de sentimento."
                )

                flash(
                    "Não foi possível analisar o comentário.",
                    "error"
                )

    comentarios = listar_comentarios()

    return render_template(
        "index.html",
        resultado=resultado,
        comentarios=comentarios
    )


@app.route("/limpar", methods=["POST"])
def limpar():

    # Mantemos a rota preparada, mas a operação de limpeza
    # pode ser adicionada posteriormente com autenticação.
    flash(
        "A limpeza do histórico deve ser protegida em produção.",
        "error"
    )

    return redirect(url_for("index"))


if __name__ == "__main__":

    init_database()

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
