const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();

app.use(express.static(path.join(__dirname, '/')));
app.use(express.json());

app.post('/save', (req, res) => {
  const data = req.body.imageData;
  const imageName = 'drawing-' + Date.now() + '.png';
  const filePath = path.join(__dirname, '/saved_images/', imageName);
  fs.writeFileSync(filePath, data, 'base64');
  res.send({ fileName: imageName });
});

app.get('/images', (req, res) => {
  const imagesDir = path.join(__dirname, '/saved_images/');
  fs.readdir(imagesDir, (err, files) => {
    if (err) {
      res.status(500).send('Error reading saved images');
      return;
    }
    res.send(files);
  });
});

app.listen(3000, () => console.log('Server running on port 3000'));

