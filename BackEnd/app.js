const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors());

// API primeiro
app.get('/imoveis', (req, res) => {
  res.json([{ titulo: "Casa teste", preco: 100000 }]);
});

// Servir frontend
app.use(express.static(path.join(__dirname, 'frontend_build')));

// Rota final (catch-all)
app.use((req, res) => {
  res.sendFile(path.join(__dirname, 'frontend_build', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server rodando na porta ${PORT}`));