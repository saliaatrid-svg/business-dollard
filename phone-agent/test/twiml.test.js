import test from 'node:test';
import assert from 'node:assert/strict';
import { buildVoiceTwiml, GREETING } from '../src/twiml.js';

test('TwiML : URL WebSocket, annonce de transcription et du 15', () => {
  const x = buildVoiceTwiml({
    wsUrl: 'wss://ex.fr/relay?t=a.b.c', language: 'fr-FR', ttsProvider: 'Google', ttsVoice: '', sttProvider: 'Google',
  });
  assert.match(x, /<ConversationRelay url="wss:\/\/ex\.fr\/relay\?t=a\.b\.c"/);
  assert.match(GREETING, /transcrit/);
  assert.match(GREETING, /15/);
  assert.doesNotMatch(x, / voice=/);
  assert.equal((x.match(/"/g) || []).length % 2, 0);
});
