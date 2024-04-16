import random
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'merda'

@app.route('/')
def index():    
    return render_template('index.html', titulo="Jogo")

@app.route('/iniciar', methods=['POST'])
def escolher_grupo():
    grupo_escolhido = request.form.get("grupo")
    dificuldade_escolhida = request.form.get("dificuldade")
    palavra_secreta = carrega_palavra_secreta(grupo_escolhido)
    letras_acertadas = inicializa_letras_acertadas(palavra_secreta)
    session['palavra_secreta'] = palavra_secreta
    session['letras_acertadas'] = letras_acertadas
    session['grupo_escolhido'] = grupo_escolhido
    session['dificuldade_escolhida'] = dificuldade_escolhida
    erros = 0
    session['erros'] = erros

  
    return render_template('jogo.html', grupo_escolhido=grupo_escolhido
                                        , dificuldade_escolhida=dificuldade_escolhida
                                        , palavra_secreta=palavra_secreta
                                        , letras_palavra=letras_acertadas
                                        , letras_acertadas=letras_acertadas
                                        , titulo="Jogo Forca"
                                        , erros=erros
                            )


@app.route('/jogar', methods=['POST'])
def jogar():
    chute = request.form.get("letra")
    enforcou = False
    acertou = False
    erros = session.get('erros', 0)
    palavra_secreta = session.get('palavra_secreta', None)
    letras_acertadas = session.get('letras_acertadas', None)
    grupo_escolhido = session.get('grupo_escolhido', None)
    dificuldade_escolhida = session.get('dificuldade_escolhida', None)
    max_erros = nivel_dificuldade(dificuldade_escolhida)
    
    if(chute in palavra_secreta):
        marca_chute_correto(chute, letras_acertadas, palavra_secreta)
    else:
        erros += 1
        session['erros'] = erros
    if session['erros'] >= max_erros:
        enforcou = True
    if "_" not in letras_acertadas:
        acertou = True
    return render_template('jogo.html', titulo="Jogo Forca"
                                        , grupo_escolhido=grupo_escolhido
                                        , dificuldade_escolhida=dificuldade_escolhida
                                        , palavra_secreta=palavra_secreta
                                        , letras_palavra=letras_acertadas
                                        , letras_acertadas=letras_acertadas
                                        , letra=chute
                                        , erros=erros
                                        , enforcou=enforcou
                                        , acertou=acertou)



def carrega_palavra_secreta(grupo_escolhido): #passar o grupo escolhido
    arquivo = open("palavras.txt", "r")
    palavras_grupo = []

    for linha in arquivo:
        linha = linha.strip()
        coluna = linha.split(";")
        if coluna[0].strip().upper() == grupo_escolhido.upper():
            palavras_grupo.append(coluna[1].strip().upper())
    arquivo.close()

    numero = random.randrange(0, len(palavras_grupo))
    palavra_secreta = palavras_grupo[numero].upper()
    return palavra_secreta


def marca_chute_correto(chute, letras_acertadas, palavra_secreta):
    index = 0
    for letra in palavra_secreta:
        if (chute == letra):
            letras_acertadas[index] = letra
        index += 1
    # Atualiza a lista de letras acertadas na sessão
    session['letras_acertadas'] = letras_acertadas


def pede_chute():
    chute = input("Qual letra? ")
    chute = chute.strip().upper()
    return chute

def inicializa_letras_acertadas(palavra): # retorna o numero de caracteres da palavra
    return ["_" for letra in palavra]


def nivel_dificuldade(dificuldade):
    if dificuldade == "FACIL":
        max_erros = 10
    elif dificuldade == "MEDIO":
        max_erros = 5
    elif dificuldade == "DIFICIL":
        max_erros = 2
    return max_erros

if __name__ == "__main__":
    app.run(debug=True)
