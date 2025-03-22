function uploadImage() {
    let file = document.getElementById('imageInput').files[0];
    if (!file) {
        alert("Please select an image!");
        return;
    }

    document.getElementById('disease-content').innerHTML = "Analyzing...";
    document.getElementById('symptoms-content').innerHTML = "Analyzing...";
    document.getElementById('treatment-content').innerHTML = "Analyzing...";
    document.getElementById('disease-image').innerHTML = '';

    let formData = new FormData();
    formData.append('image', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || `HTTP error! status: ${response.status}`);
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            document.getElementById('disease-content').innerHTML = `<strong style="color: red;">Error:</strong> ${data.error}`;
            document.getElementById('symptoms-content').innerHTML = '';
            document.getElementById('treatment-content').innerHTML = '';
            document.getElementById('disease-image').innerHTML = '';
        } else {
            document.getElementById('disease-content').innerHTML = data.disease;
            document.getElementById('symptoms-content').innerHTML = data.symptoms;
            document.getElementById('treatment-content').innerHTML = data.treatment;
            document.getElementById('disease-image').innerHTML = '<p>Image not available</p>';
        }
    })
    .catch(error => {
        document.getElementById('disease-content').innerHTML = `<strong style="color: red;">Error:</strong> ${error.message}`;
        document.getElementById('symptoms-content').innerHTML = '';
        document.getElementById('treatment-content').innerHTML = '';
        document.getElementById('disease-image').innerHTML = '';
        console.error('Error:', error);
    });
}