import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

nlp = spacy.load("pt_core_news_sm")

def remove_stopwords(text):
    doc = nlp(text.lower())
    return ' '.join([token.text for token in doc if not token.is_stop and not token.is_punct])

with open('src/data.json', 'r', encoding='utf-8') as file:
    dataset = json.load(file)

perguntas = dataset["perguntas"]
respostas = dataset["respostas"]
mapeamento = dataset["mapeamento"]

perguntas_limpas = [remove_stopwords(pergunta) for pergunta in perguntas]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(perguntas_limpas)

model = MultinomialNB()
model.fit(X, mapeamento)

def get_response(user_input):
    user_input_clean = remove_stopwords(user_input)
    user_input_vectorized = vectorizer.transform([user_input_clean])
    probabilities = model.predict_proba(user_input_vectorized)
    prediction = model.predict(user_input_vectorized)

    if max(probabilities[0]) < 0.10:
        return "Desculpe, não entendi sua pergunta. Poderia reformular? Tenha em mente que sou focado em saciar suas dúvidas no mundo imobiliário. Caso queira encerrar a nossa conversa pode digitar 'sair' ou 'encerrar atendimento'."

    return respostas[prediction[0]]

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('question', '').strip()

    if not user_input:
        return jsonify({'answer': 'Por favor, envie uma mensagem válida.'}), 400

    response = get_response(user_input)
    return jsonify({'answer': response})

if __name__ == "__main__":
    import threading

    def run_terminal_chat():
        while True:
            user_input = input("Você: ")
            if user_input.lower() in ["sair", "exit", "quit", "encerrar atendimento", "finalizar conversa", "finalizar", "finalizar atendimento"]:
                print("CorretorBot: Até mais!")
                break
            response = get_response(user_input)
            print(f"Chatbot: {response}")

    threading.Thread(target=run_terminal_chat, daemon=True).start()

    print("Iniciando servidor Flask...")
    app.run(debug=True, port=5000)
