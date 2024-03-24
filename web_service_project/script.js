const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let isDrawing = false;

function startDrawing(e) {
  isDrawing = true;
  draw(e);
}

function stopDrawing() {
  isDrawing = false;
  ctx.beginPath();
}

function draw(e) {
  if (!isDrawing) return;
  ctx.lineWidth = 5;
  ctx.lineCap = 'round';
  ctx.strokeStyle = 'black';
  ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
}

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mousemove', draw);

document.getElementById('resetButton').addEventListener('click', function() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
});

document.getElementById('saveButton').addEventListener('click', function() {
  const imageData = canvas.toDataURL('image/png').replace('data:image/png;base64,', '');
  fetch('/save', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ imageData })
  })
  .then(response => response.json())
  .then(data => {
    updateImageList(data.fileName);
  })
  .catch(error => {
    console.error('Error saving the image:', error);
  });
});

function updateImageList(imageName) {
  const list = document.getElementById('savedImagesList');
  const listItem = document.createElement('div');
  listItem.textContent = imageName;
  listItem.addEventListener('click', () => {
    window.location.href = '/saved_images/' + imageName;
  });
  list.appendChild(listItem);
}

// Load and display the list of saved images on page load
window.addEventListener('load', () => {
  fetch('/images')
    .then(response => response.json())
    .then(images => {
      images.forEach(updateImageList);
    });
});
