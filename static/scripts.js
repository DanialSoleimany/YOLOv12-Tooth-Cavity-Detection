// showSection function removed - not needed for this layout

function previewImage(event) {
  const file = event.target.files[0];
  if (file && file.type.startsWith('image/')) {
    document.getElementById('image-placeholder').style.display = 'none';
    const reader = new FileReader();
    reader.onload = function(e) {
      const img = document.getElementById('preview-img');
      img.src = e.target.result;
      img.style.display = 'block';
      document.getElementById('image-box').style.display = 'block';
    };
    reader.readAsDataURL(file);
  }
}

function removeImage() {
  document.getElementById('preview-img').src = '#';
  document.getElementById('image-box').style.display = 'none';
  document.getElementById('image-placeholder').style.display = 'block';
  const fileInput = document.querySelector('input[name="image"]');
  fileInput.value = '';
}

function updateProbabilityChart(detections) {
  const labels = detections.map(d => `Obj ${d.object_id} (${d.class_name})`);
  const cavityProbs = detections.map(d => d.probabilities[0]); // red
  const normalProbs = detections.map(d => d.probabilities[1]); // green

  const ctx = document.getElementById('probabilityChart').getContext('2d');
  if (window.probChart) window.probChart.destroy();

  window.probChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Cavity (Red)',
          data: cavityProbs,
          backgroundColor: 'rgba(255, 0, 0, 0.8)',
          borderColor: 'rgba(255, 0, 0, 1)',
          borderWidth: 1
        },
        {
          label: 'Normal (Green)',
          data: normalProbs,
          backgroundColor: 'rgba(0, 255, 0, 0.8)',
          borderColor: 'rgba(0, 255, 0, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: { 
          display: true, 
          text: 'Prediction Probabilities (Red=Cavity, Green=Normal)',
          font: { size: 14, weight: 'bold' }
        },
        legend: { 
          position: 'top',
          labels: {
            usePointStyle: true,
            padding: 20
          }
        }
      },
      scales: {
        y: { 
          beginAtZero: true, 
          max: 1,
          title: { display: true, text: 'Confidence Score' }
        },
        x: { 
          title: { display: true, text: 'Detected Objects' }
        }
      }
    }
  });
}

function sendPrediction() {
  const fileInput = document.querySelector('input[name="image"]');
  if (!fileInput.files.length) {
    alert("Please select an image first.");
    return;
  }

  const formData = new FormData();
  formData.append("image", fileInput.files[0]);
  formData.append("confidence", document.getElementById("confidence").value);

  document.getElementById("prediction-result").textContent = "Processing...";
  document.getElementById("inference-time").textContent = "-- ms";

  fetch("/api/predict", {
    method: "POST",
    body: formData
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    if (data.error) {
      alert("Error: " + data.error);
      document.getElementById("prediction-result").textContent = "-";
      return;
    }

    // Count detections by class
    const cavityCount = data.detections.filter(d => d.class_id === 0).length;
    const normalCount = data.detections.filter(d => d.class_id === 1).length;
    
    document.getElementById("prediction-result").textContent =
      data.num_detections > 0
        ? `${data.num_detections} objects detected (${cavityCount} cavity, ${normalCount} normal)`
        : "No objects detected";

    document.getElementById("inference-time").textContent =
      `${data.inference_time_ms} ms`;

    if (data.detections.length > 0) {
      updateProbabilityChart(data.detections);
    } else {
      updateProbabilityChart([]);
    }

    if (data.saved_image_path) {
      const annotatedImageUrl = `/download/image/${data.saved_image_path}`;
      const imgElement = document.getElementById("preview-img");
      imgElement.src = annotatedImageUrl + `?t=${new Date().getTime()}`;
      imgElement.style.display = "block";
      document.getElementById("image-placeholder").style.display = "none";
      document.getElementById("image-box").style.display = "block";
    }
  })
  .catch(err => {
    console.error("Prediction error:", err);
    alert("An error occurred while predicting: " + err.message);
    document.getElementById("prediction-result").textContent = "-";
  });
}
