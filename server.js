const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');
const config = require('./config'); // 引入設定檔

const app = express();

const pool = new Pool(config.database); // 使用設定檔中的資料庫設定

app.use(cors());
app.use(express.static('public'));
app.use(express.json());

app.get('/api/indexes', async (req, res) => {
    try {
        const result = await pool.query('SELECT test_index FROM IPAS_index');
        res.json(result.rows.map(row => row.test_index));
    } catch (err) {
        console.error(err);
        res.status(500).send('伺服器錯誤');
    }
});

app.get('/api/questions/:testIndex', async (req, res) => {
    const testIndex = req.params.testIndex;
    try {
        const result = await pool.query(`SELECT id, question, A, B, C, D, answer FROM "${testIndex}" ORDER BY id`);
        res.json(result.rows);
    } catch (err) {
        console.error(`查詢表格 "${testIndex}" 失敗:`, err.message);
        res.status(500).send(`無法讀取試題表格 "${testIndex}"`);
    }
});

app.listen(config.server.port, () => { // 使用設定檔中的端口
    console.log(`伺服器運行在 http://localhost:${config.server.port}`);
});