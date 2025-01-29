function uploadPDF() {
    var fileInput = document.getElementById('pdf-upload');
    var file = fileInput.files[0];
    if (file) {
        var formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            displayMessage('PDF Uploaded. File ID: ' + data.file_id);
            // Save file_id to use later for questions
            window.file_id = data.file_id;
        })
        .catch(error => console.error('Error:', error));
    }
}

function askQuestion(question) {
    var data = {
        file_id: window.file_id,
        question: question
    };

    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        displayMessage('Bot: ' + data.answer);
    })
    .catch(error => console.error('Error:', error));
}











