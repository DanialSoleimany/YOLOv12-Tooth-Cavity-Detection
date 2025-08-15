let probabilityChart = null;

function previewImage(event) {
  const reader = new FileReader();
  reader.onload = function(){
    const imgElement = document.getElementById('preview-img');
    imgElement.src = reader.result;
    imgElement.style.display = 'block';
    document.getElementById('image-placeholder').style.display = 'none';
    document.getElementById('image-box').style.display = 'block';
  }
  reader.readAsDataURL(event.target.files[0]);
}

function removeImage() {
  const imgElement = document.getElementById('preview-img');
  imgElement.src = '#';
  imgElement.style.display = 'none';
  document.getElementById('image-placeholder').style.display = 'block';
  document.getElementById('image-box').style.display = 'none';
  document.getElementById("prediction-result").textContent = "-";
  document.getElementById("inference-time").textContent = "-- ms";
  if (probabilityChart) {
    probabilityChart.destroy();
    probabilityChart = null;
  }
}

function updateProbabilityChart(detections) {
  const ctx = document.getElementById('probabilityChart').getContext('2d');
  
  // Sort detections by confidence in descending order
  detections.sort((a, b) => b.confidence - a.confidence);

  const labels = detections.map((d, index) => {
    const class_name = d.class_name.charAt(0).toUpperCase() + d.class_name.slice(1);
    return `Obj ${index + 1} (${class_name})`;
  });
  const cavityProbs = detections.map(d => d.class_id === 0 ? d.confidence : 0);
  const normalProbs = detections.map(d => d.class_id === 1 ? d.confidence : 0);

  if (probabilityChart) {
    probabilityChart.destroy();
  }

  probabilityChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Cavity (Red)',
          data: cavityProbs,
          backgroundColor: 'rgba(255, 0, 0, 0.6)',
          borderColor: 'rgba(255, 0, 0, 1)',
          borderWidth: 1
        },
        {
          label: 'Normal (Green)',
          data: normalProbs,
          backgroundColor: 'rgba(0, 255, 0, 0.6)',
          borderColor: 'rgba(0, 255, 0, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y', // Make it horizontal
      plugins: {
        title: {
          display: true,
          text: 'Prediction Probabilities (Red=Cavity, Green=Normal)',
          font: { size: 14, weight: 'bold', color: '#fff' }
        },
        legend: {
          position: 'top',
          labels: {
            usePointStyle: true,
            padding: 20,
            color: '#fff'
          }
        }
      },
      scales: {
        x: { 
          beginAtZero: true, 
          max: 1,
          title: { 
            display: true, 
            text: 'Confidence Score',
            color: '#fff'
          },
          ticks: {
            color: '#fff'
          },
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          }
        },
        y: { 
          title: { 
            display: true, 
            text: 'Detected Objects',
            color: '#fff'
          },
          ticks: {
            color: '#fff'
          },
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          }
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

    // Display the annotated image directly from base64
    if (data.annotated_image) {
      const imgElement = document.getElementById("preview-img");
      imgElement.src = `data:image/jpeg;base64,${data.annotated_image}`;
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
