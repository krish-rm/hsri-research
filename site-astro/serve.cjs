const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 4321;
const DIST = path.join(__dirname, 'dist');

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.mjs': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.csv': 'text/csv; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
  '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
  let urlPath = decodeURIComponent(req.url.split('?')[0]);
  let filePath = path.join(DIST, urlPath);
  
  // Check exact file
  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    serveFile(filePath, res);
    return;
  }
  
  // Check directory index.html
  if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
    const idx = path.join(filePath, 'index.html');
    if (fs.existsSync(idx)) {
      serveFile(idx, res);
      return;
    }
  }
  
  // Check url + /index.html
  const directIdx = path.join(filePath, 'index.html');
  if (fs.existsSync(directIdx)) {
    serveFile(directIdx, res);
    return;
  }
  
  // Check url + .html
  if (fs.existsSync(filePath + '.html')) {
    serveFile(filePath + '.html', res);
    return;
  }
  
  res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('404 Not Found');
});

function serveFile(fPath, res) {
  const ext = path.extname(fPath).toLowerCase();
  res.writeHead(200, {
    'Content-Type': MIME[ext] || 'application/octet-stream',
    'Access-Control-Allow-Origin': '*',
    'Cache-Control': 'no-cache'
  });
  fs.createReadStream(fPath).pipe(res);
}

server.listen(PORT, '127.0.0.1', () => {
  console.log(`HSRI Benchmark Server running at http://127.0.0.1:${PORT}`);
  console.log(`Serving 45 static pages from: ${DIST}`);
});
