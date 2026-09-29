import { createHmac, timingSafeEqual } from 'node:crypto';

function safeEqual(a, b) {
  const ba = Buffer.from(a);
  const bb = Buffer.from(b);
  return ba.length === bb.length && timingSafeEqual(ba, bb);
}

/** Vérifie l'en-tête X-Twilio-Signature (HMAC-SHA1 de l'URL + paramètres triés). */
export function validateTwilioSignature(authToken, url, params, signature) {
  if (!signature) return false;
  const data = Object.keys(params)
    .sort()
    .reduce((acc, k) => acc + k + params[k], url);
  const expected = createHmac('sha1', authToken).update(data).digest('base64');
  return safeEqual(expected, signature);
}

/** Jeton court qui autorise une connexion WebSocket pour un appel donné. */
export function signToken(secret, callSid, expiresAtMs) {
  const payload = `${callSid}.${expiresAtMs}`;
  const mac = createHmac('sha256', secret).update(payload).digest('hex');
  return `${payload}.${mac}`;
}

export function verifyToken(secret, token, now = Date.now()) {
  if (!token) return null;
  const parts = token.split('.');
  if (parts.length !== 3) return null;
  const [callSid, exp, mac] = parts;
  const expected = createHmac('sha256', secret).update(`${callSid}.${exp}`).digest('hex');
  if (!safeEqual(expected, mac)) return null;
  if (Number(exp) < now) return null;
  return callSid;
}
