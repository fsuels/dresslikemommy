// Review-only preload. Any accidental network attempt fails this offline check.
import http from 'node:http';
import https from 'node:https';
import net from 'node:net';
import tls from 'node:tls';
import { syncBuiltinESMExports } from 'node:module';
const deny = () => { throw new Error('independent_review_network_forbidden'); };
globalThis.fetch = deny;
for (const module of [http, https]) { module.request = deny; module.get = deny; }
net.connect = deny; net.createConnection = deny; tls.connect = deny;
syncBuiltinESMExports();
