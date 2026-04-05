const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors());

// Serve arquivos estáticos do frontend
app.use(express.static(path.join(__dirname, 'frontend_build')));

// Todas as rotas vão para index.html
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend_build', 'index.html'));
});

// Exemplo de endpoint da API
app.get('/imoveis', (req, res) => {
  res.json([{ titulo: "Casa teste", preco: 100000 }]);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server rodando na porta ${PORT}`));