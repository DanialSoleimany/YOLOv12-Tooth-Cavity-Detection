function previewImage(event) {
  try {
    const input = event.target;
    const preview = document.getElementById('image-preview');
    const file = input.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function(e) {
        preview.src = e.target.result;
        preview.style.display = 'block';
      }
      reader.readAsDataURL(file);
    }
  } catch (error) {
    alert("Error loading image: " + error.message);
  }
}

function showSection(sectionId) {
  try {
    ['prediction', 'gradcam', 'search'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.classList.add('d-none');
    });
    document.getElementById(sectionId).classList.remove('d-none');
  } catch (error) {
    alert("Error switching section: " + error.message);
  }
}
