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

function showSection(sectionId) {
  document.querySelectorAll('.sidebar a').forEach(a => a.classList.remove('active'));
  document.getElementById('btn-' + sectionId).classList.add('active');
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.getElementById(sectionId).classList.add('active');
}

function removeImage() {
  document.getElementById('preview-img').src = '#';
  document.getElementById('image-box').style.display = 'none';
  document.getElementById('image-placeholder').style.display = 'block';
  const fileInput = document.querySelector('input[name="image"]');
  fileInput.value = '';
}

function updateProbabilityChart(labels, probabilities) {
  const ctx = document.getElementById('probabilityChart').getContext('2d');
  if (window.probChart) window.probChart.destroy();
  window.probChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Probability',
        data: probabilities,
        backgroundColor: '#9966ff',
        borderRadius: 8,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: false }
      },
      scales: {
        y: { beginAtZero: true, max: 1 }
      }
    }
  });
}
// Example usage (replace with real data after prediction):
// updateProbabilityChart(['Tooth 1', 'Tooth 2', 'Tooth 3'], [0.85, 0.42, 0.67]);
