const express = require('express');
const { exec } = require('child_process');
const app = express();

app.use(express.json());

app.post('/record-mood', (req, res) => {
  exec("cd d:/mental_health_pattern_app && python -c \"from src.data_collection import DataCollector; collector = DataCollector('data'); collector.record_mood(7, 'Sample mood')\"", (err) => {
    if (err) {
      console.error('Error:', err);
      return res.status(500).send(err.message);
    }
    res.send('Success');
  });
});

app.listen(3000, () => console.log('Server running on port 3000'));