import test from 'node:test';
import assert from 'node:assert/strict';
import { CallSession } from '../src/session.js';

function fakeStream(message, texts = []) {
  const handlers = {};
  return {
    on(evt, fn) { handlers[evt] = fn; },
    async finalMessage() { texts.forEach((t) => handlers.text?.(t)); return message; },
  };
}

function setup(replies) {
  const sent = [];
  const ws = { readyState: 1, send: (s) => sent.push(JSON.parse(s)) };
  const saved = [];
  const notified = [];
  const transcripts = [];
  const client = { messages: { stream: () => fakeStream(...replies.shift()) } };
  const deps = {
    cfg: { model: 'm' },
    client,
    calendar: null,
    notify: async (t) => notified.push(t),
    store: {
      saveMessage: async (m) => { saved.push(m); return 'abc123'; },
      saveTranscript: async (id, turns) => transcripts.push({ id, turns }),
    },
  };
  const session = new CallSession({ ws, deps, systemPrompt: 'sys', log: { error() {}, info() {} } });
  return { session, sent, saved, notified, transcripts };
}

test("message pris via outil, puis fin d'appel", async () => {
  const { session, sent, saved, notified, transcripts } = setup([
    [{ stop_reason: 'tool_use', content: [
      { type: 'tool_use', id: 't1', name: 'save_message', input: { caller_name: 'Marie D.', reason_category: 'information', urgency: 'normale', note: 'secret médical' } },
      { type: 'tool_use', id: 't2', name: 'end_call', input: {} },
    ] }],
    [{ stop_reason: 'end_turn', content: [{ type: 'text', text: 'Merci, au revoir.' }] }, ['Merci, au revoir.']],
  ]);
  session.handle(JSON.stringify({ type: 'setup', callSid: 'CA9', from: '+33611111111' }));
  session.handle(JSON.stringify({ type: 'prompt', voicePrompt: 'Bonjour, rappelez-moi.', last: true }));
  await session.queue;
  assert.equal(saved[0].callbackNumber, '+33611111111');
  assert.match(notified[0], /Marie D\./);
  assert.ok(!notified[0].includes('secret médical'), 'la note ne doit pas partir dans Slack');
  assert.deepEqual(sent.at(-1), { type: 'end' });
  await session.finish();
  assert.equal(transcripts[0].id, 'CA9');
  assert.equal(notified.length, 1);
});

test("refus de transcription : rien n'est conservé", async () => {
  const { session, transcripts } = setup([
    [{ stop_reason: 'tool_use', content: [{ type: 'tool_use', id: 't1', name: 'refuse_transcription', input: {} }] }],
    [{ stop_reason: 'end_turn', content: [{ type: 'text', text: "C'est noté." }] }, ["C'est noté."]],
  ]);
  session.handle(JSON.stringify({ type: 'prompt', voicePrompt: 'Je ne veux pas être transcrit.' }));
  await session.queue;
  await session.finish();
  assert.equal(transcripts.length, 0);
});
