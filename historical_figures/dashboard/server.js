const http = require('http');
const https = require('https');

const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY || 'sk-798f7767ff62445491ab21afaa8c7ea9';
const PORT = 3001;

const server = http.createServer((req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  if (req.method === 'POST' && req.url === '/chat') {
    let body = '';
    
    req.on('data', chunk => {
      body += chunk.toString();
    });
    
    req.on('end', () => {
      try {
        const { messages, figure } = JSON.parse(body);
        
        // Build system prompt for historical figure
        const systemPrompt = `你是${figure}，一个历史人物。请用符合该人物身份、性格和时代背景的方式回答问题。使用第一人称，自称要符合人物身份（如朕、我、吾、在下等）。如果你不知道或不确定的事情，可以说"此事吾不太清楚"。`;
        
        const requestBody = JSON.stringify({
          model: 'deepseek-chat',
          messages: [
            { role: 'system', content: systemPrompt },
            ...messages
          ],
          temperature: 0.8,
          max_tokens: 500
        });

        const options = {
          hostname: 'api.deepseek.com',
          port: 443,
          path: '/v1/chat/completions',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${DEEPSEEK_API_KEY}`,
            'Content-Length': Buffer.byteLength(requestBody)
          }
        };

        const proxyReq = https.request(options, (proxyRes) => {
          let data = '';
          proxyRes.on('data', chunk => data += chunk);
          proxyRes.on('end', () => {
            res.writeHead(proxyRes.statusCode, { 'Content-Type': 'application/json' });
            res.end(data);
          });
        });

        proxyReq.on('error', (e) => {
          res.writeHead(500, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: e.message }));
        });

        proxyReq.write(requestBody);
        proxyReq.end();
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
    });
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

server.listen(PORT, () => {
  console.log(`🚀 历史人物对话代理服务运行在 http://localhost:${PORT}`);
  console.log(`📡 等待 Dashboard 连接...`);
});
