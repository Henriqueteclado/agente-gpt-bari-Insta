import openai
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Chave da API do OpenAI armazenada como variável de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

# Banco de respostas do Guinada Bari
respostas = {
    "O que está incluído no Guinada Bari?": "O Guinada Bari inclui o método dos 3Cs da Bari, o app Calcula Bari, o Cardápio Musa Bari e uma comunidade exclusiva...",
    "Como funciona a Comunidade Guinada Bari?": "A comunidade tem três grupos: Lagarta/Casulo, Borboleta e ReBorboleta...",
    "Qual o valor do Guinada Bari?": "O investimento no Guinada Bari é de R$1.797, parcelável em 12x...",
}

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    pergunta = data.get("text", "").lower()

    # Buscar resposta no banco de dados primeiro
    resposta = respostas.get(pergunta, None)
    
    # Se não encontrar no banco, recorrer ao GPT
    if not resposta:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Você é um assistente especializado no Guinada Bari."},
                      {"role": "user", "content": pergunta}]
        )
        resposta = response["choices"][0]["message"]["content"]

    return jsonify({"text": resposta})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
