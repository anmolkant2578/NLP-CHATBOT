from flask import Flask, request, render_template
import fitz 
from transformers import pipeline
import re

app = Flask(__name__, template_folder='template')  

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        pdf_file = request.files['pdf']
        question = request.form.get('question', '')  
        if pdf_file:
            text = read_pdf(pdf_file)
            summary = summarize_text(text)
            answer = answer_question(text, question) if question else "No question asked."
            references = find_references(text)
            return render_template('index.html', summary=summary, answer=answer, question=question, references=references)
    return render_template('index.html')

def read_pdf(file_stream):
    doc = fitz.open(stream=file_stream.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close() 
    return text

def summarize_text(text):
    if not text.strip():
        return "No text was found in the PDF or text is not extractable."
    
    try:
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        if summary:
            return " ".join([summ['summary_text'] for summ in summary])
        else:
            return "Failed to generate a summary, possibly due to the text being too short or unsuitable."
    except Exception as e:
        return f"An error occurred during summarization: {str(e)}"

def answer_question(text, question):
    try:
        answer = qa_pipeline({'context': text, 'question': question})
        return answer['answer']
    except Exception as e:
        return f"An error occurred while trying to answer the question: {str(e)}"

def find_references(text):
    references = re.findall(r'\[\d+\]', text)
    return references if references else "No references found."

if __name__ == "__main__":
    app.run(debug=True)
