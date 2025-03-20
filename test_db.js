const { Pool } = require('pg');

// PostgreSQL 連線設定
const pool = new Pool({
    user: '您的名稱', // 替換為你的 PostgreSQL 使用者名稱
    host: '127.0.0.1',       // 替換為你的資料庫主機
    database: 'ipas',
    password: '您的密碼',    // 替換為你的密碼
    port: 5432
});

console.log('開始測試 PostgreSQL 連線...');

// 測試連線函數
async function testConnection() {
    let client;
    try {
        // 建立連線
        console.log('嘗試連接到資料庫...');
        client = await pool.connect();
        console.log('成功連接到 PostgreSQL 資料庫！');

        // 測試查詢：檢查資料庫版本
        const res = await client.query('SELECT version()');
        console.log('資料庫版本：', res.rows[0].version);

        // 測試查詢：檢查 IPAS_index 表格
        const indexRes = await client.query('SELECT test_index FROM IPAS_index');
        console.log('IPAS_index 表格內容：', indexRes.rows);

        const tableRes = await client.query(`SELECT * FROM "108-2" LIMIT 1`);
        console.log('108-2 表格內容：', tableRes.rows);
    } catch (err) {
        console.error('連線或查詢失敗，錯誤訊息：', err.message);
        console.error('完整錯誤：', err.stack);
    } finally {
        if (client) {
            client.release();
            console.log('客戶端已釋放');
        }
        await pool.end();
        console.log('連線池已關閉');
    }
}

// 執行測試
testConnection();