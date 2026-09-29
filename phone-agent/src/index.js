import { createServer } from 'node:http';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import Anthropic from '@anthropic-ai/sdk';
import { WebSocketServer } from 'ws';
import { loadConfig } from './config.js';
import { validateTwilioSignature, signToken, verifyToken } from './security.js';
import { buildVoiceTwiml, REFUSAL_TWIML } from './twiml.js';
import { buildSystemPrompt } from './prompt.js';
import { createStore } from './store.js';
import { createNotifier } from './notify.js';
import { createCalendar } from './calendar.js';
import { CallSession } from './session.js';

const cfg = loadConfig();
const here = dirname(fileURLToPath(import.meta.url));
const systemPrompt = await buildSystemPrompt(join(here, '..', 'config', 'dms-info.md'));
const store = createStore(cfg.dataDir, cfg.retentionDays);
const deps = {
  cfg,
  store,
  notify: createNotifier(cfg.slackWebhook),
  calendar: createCalendar(cfg),
  client: new Anthropic({ apiKey: cfg.anthropicKey }),
};

async function readForm(req) {
  const chunks = [];
  let size = 0;
  for await (const c of req) {
    size += c.length;
    if (size > 64_000) throw new Error('Corps trop volumineux');
    chunks.push(c);
  }
  return Object.fromEntries(new URLSearchParams(Buffer.concat(chunks).toString('utf8')));
}

const server = createServer(async (req, res) => {
  const path = new URL(req.url, 'http://x').pathname;
  if (req.method === 'GET' && path === '/health') {
    res.writeHead(200).end('ok');
    return;
  }
  if (req.method === 'POST' && path === '/voice') {
    try {
      const params = await readForm(req);
      const ok = validateTwilioSignature(
        cfg.twilioAuthToken,
        `${cfg.publicUrl}/voice`,
        params,
        req.headers['x-twilio-signature'],
      );
      if (!ok) {
        res.writeHead(403).end('Forbidden');
        return;
      }
      const token = signToken(cfg.signingSecret, params.CallSid || 'x', Date.now() + 5 * 60_000);
      const wsUrl = `${cfg.publicUrl.replace(/^http/, 'ws')}/relay?t=${encodeURIComponent(token)}`;
      res.writeHead(200, { 'content-type': 'text/xml' }).end(
        buildVoiceTwiml({
          wsUrl,
          language: cfg.language,
          ttsProvider: cfg.ttsProvider,
          ttsVoice: cfg.ttsVoice,
          sttProvider: cfg.sttProvider,
        }),
      );
    } catch (err) {
      console.error('Erreur /voice', err.message);
      res.writeHead(200, { 'content-type': 'text/xml' }).end(REFUSAL_TWIML);
    }
    return;
  }
  res.writeHead(404).end();
});

const wss = new WebSocketServer({ noServer: true });
server.on('upgrade', (req, socket, head) => {
  const url = new URL(req.url, 'http://x');
  if (url.pathname !== '/relay' || !verifyToken(cfg.signingSecret, url.searchParams.get('t'))) {
    socket.write('HTTP/1.1 403 Forbidden\r\n\r\n');
    socket.destroy();
    return;
  }
  wss.handleUpgrade(req, socket, head, (ws) => {
    const session = new CallSession({ ws, deps, systemPrompt });
    ws.on('message', (data) => session.handle(data.toString()));
    ws.on('close', () => session.finish().catch((e) => console.error('Erreur de clôture', e.message)));
  });
});

const purge = () => store.purge().then((n) => n && console.log(`Purge RGPD : ${n} fichier(s) supprimé(s)`));
await purge();
setInterval(purge, 24 * 3600_000).unref();

server.listen(cfg.port, () => console.log(`Agent téléphonique DMS à l'écoute sur le port ${cfg.port}`));
