document.addEventListener("DOMContentLoaded", () => {
  const uploadForm = document.getElementById("uploadForm");
  const imageFile = document.getElementById("imageFile");
  const resultDiv = document.getElementById("result");


  uploadForm.addEventListener("submit", (e) => {
      e.preventDefault();

      const formData = new FormData();
      formData.append("file", imageFile.files[0]);

      fetch("/predict", {
          method: "POST",
          body: formData,
      })
          .then((response) => response.json())
          .then((data) => {
              if (data.predicted_class) {
                  resultDiv.innerHTML = `<h2>Prediction: ${data.predicted_class}</h2>
                                          <h2>${data.info}</h2>
                                        <h2>Confidence: ${data.confidence}%</h2>`;

              } else if (data.error) {
                  resultDiv.innerHTML = `<h2>Error: ${data.error}</h2>`;
              }
          })
          .catch(() => {
              resultDiv.innerHTML = `<h2>Error: Could not process the image</h2>`;
          });
  });
});

document.addEventListener('DOMContentLoaded', () => {
    console.log("Consultancy page loaded successfully!");
});
