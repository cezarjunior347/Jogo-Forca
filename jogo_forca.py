import random


def jogar():
    print("Iniciando Jogo Forca")
    palavra_secreta = carrega_palavra_secreta("Automovel")
    
    letras_acertadas = inicializa_letras_acertadas(palavra_secreta)
    print(letras_acertadas)

    enforcou = False
    acertou = False
    erros = 0

    while(not enforcou and not acertou):

        chute = pede_chute() # vai receber a letra selecionada

        if(chute in palavra_secreta):
            marca_chute_correto(chute, letras_acertadas, palavra_secreta)
        else:
            erros += 1
            desenha_forca(erros) # informa a quantidade de erros

        enforcou = erros == max_erros # verifica se "erros" é igual ao "max_erros" se for "enforcou" recebe True
        acertou = "_" not in letras_acertadas # verifica se ainda tem letra para ser acerta, se não tiver mais letras, "acertou" recebe Trua

        print(letras_acertadas) # informa as letras que acertou ven da def marcar_cute_correto()

    if(acertou):
        imprime_mensagem_vencedor()
    else:
        imprime_mensagem_perdedor(palavra_secreta)


def desenha_forca(erros):
    print(f"total de erros: {erros}")


def imprime_mensagem_vencedor():
    print("VENCEU!!!!")
def imprime_mensagem_perdedor(palavra_secreta):
    print(f"Perdeu! a palavra correta era: {palavra_secreta}")

def marca_chute_correto(chute, letras_acertadas, palavra_secreta):
    index = 0
    for letra in palavra_secreta:
        if (chute == letra):
            letras_acertadas[index] = letra
        index += 1

def pede_chute():
    chute = input("Qual letra? ")
    chute = chute.strip().upper()
    return chute

def inicializa_letras_acertadas(palavra): # retorna o numero de caracteres da palavra
    return ["_" for letra in palavra]


def carrega_palavra_secreta(grupo): #passar o grupo escolhido
    arquivo = open("Jogo_forca/palavras.txt", "r")
    palavras_grupo = []

    for linha in arquivo:
        linha = linha.strip()
        coluna = linha.split(";")
        if coluna[0].strip().upper() == grupo.upper():
            palavras_grupo.append(coluna[1].strip().upper())
    arquivo.close()

    numero = random.randrange(0, len(palavras_grupo))
    palavra_secreta = palavras_grupo[numero].upper()
    return palavra_secreta

def nivel_dificuldade(dificuldade):
    if dificuldade == 1:
        max_erros = 20
    elif dificuldade == 2:
        max_erros = 10
    elif dificuldade == 3:
        max_erros = 5
    return max_erros

max_erros = nivel_dificuldade(3) #passar nivel de dificuldade escolhido

if(__name__ == "__main__"):
    jogar()
