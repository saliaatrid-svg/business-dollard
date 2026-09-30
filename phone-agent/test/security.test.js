import test from 'node:test';
import assert from 'node:assert/strict';
import { createHmac } from 'node:crypto';
import { validateTwilioSignature, signToken, verifyToken } from '../src/security.js';

test('signature Twilio valide et invalide', () => {
  const url = 'https://ex.fr/voice';
  const params = { CallSid: 'CA1', From: '+33600000000' };
  const data = url + 'CallSid' + 'CA1' + 'From' + '+33600000000';
  const sig = createHmac('sha1', 'tok').update(data).digest('base64');
  assert.equal(validateTwilioSignature('tok', url, params, sig), true);
  assert.equal(validateTwilioSignature('autre', url, params, sig), false);
  assert.equal(validateTwilioSignature('tok', url, params, undefined), false);
});

test('jeton WebSocket : valide, expiré, falsifié', () => {
  const t = signToken('s', 'CA1', 2000);
  assert.equal(verifyToken('s', t, 1000), 'CA1');
  assert.equal(verifyToken('s', t, 3000), null);
  assert.equal(verifyToken('autre', t, 1000), null);
  assert.equal(verifyToken('s', t.replace('CA1', 'CA2'), 1000), null);
  assert.equal(verifyToken('s', 'nimporte', 1000), null);
});
