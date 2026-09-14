import http from 'node:http';
import { readFileSync } from 'node:fs';

const repo = '/Users/fsuels/Projects/dresslikemommy';
const assets = new Set(['cart.js', 'base.css', 'component-cart.css', 'component-cart-items.css', 'component-cart-drawer.css']);
const template = readFileSync(new URL('./index.html', import.meta.url), 'utf8');
const placeholder = '<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180" viewBox="0 0 180 180"><rect width="180" height="180" rx="12" fill="#eaf2f5"/><path d="M53 42 75 32H105L127 42 148 68 127 82 117 66V145H63V66L53 82 32 68Z" fill="#bfd4df" stroke="#607f90" stroke-width="2"/><path d="M75 32Q90 58 105 32" fill="none" stroke="#607f90" stroke-width="2"/></svg>';
const server = http.createServer((request, response) => {
  const url = new URL(request.url, 'http://127.0.0.1:8776');
  response.setHeader('Cache-Control', 'no-store');
  if (url.pathname === '/favicon.ico') {
    response.writeHead(204);
    response.end();
    return;
  }
  if (url.pathname === '/fixture-product.svg') {
    response.writeHead(200, { 'Content-Type': 'image/svg+xml' });
    response.end(placeholder);
    return;
  }
  const asset = url.pathname.match(/^\/assets\/([^/]+)$/)?.[1];
  if (asset && assets.has(asset)) {
    response.writeHead(200, { 'Content-Type': asset.endsWith('.js') ? 'text/javascript' : 'text/css' });
    response.end(readFileSync(`${repo}/assets/${asset}`));
    return;
  }
  if (/^\/(?:da\/|fr\/)?(?:cart|products\/[a-z0-9-]+)\/?$/.test(url.pathname)) {
    response.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    response.end(template);
    return;
  }
  response.writeHead(404);
  response.end('Unknown local fixture route');
});
server.listen(8776, '127.0.0.1', () => {
  console.log('Cart recently-viewed fixture: http://127.0.0.1:8776/da/cart?reset=1');
});
