import { TOOL_DEFINITIONS, runTool } from './tools.js';

/**
 * Une session = un appel. Reçoit les messages Twilio ConversationRelay
 * (setup, prompt, interrupt, dtmf, error) et répond en streaming avec Claude.
 */
export class CallSession {
  constructor({ ws, deps, systemPrompt, log = console }) {
    this.ws = ws;
    this.deps = deps;
    this.systemPrompt = systemPrompt;
    this.log = log;
    this.callSid = '';
    this.from = '';
    this.transcribe = true;
    this.messageSaved = false;
    this.endRequested = false;
    this.slots = [];
    this.history = [];
    this.turns = [];
    this.abort = null;
    this.queue = Promise.resolve();
    this.heardSomething = false;
  }

  send(obj) {
    if (this.ws.readyState === 1) this.ws.send(JSON.stringify(obj));
  }

  handle(raw) {
    let msg;
    try {
      msg = JSON.parse(raw);
    } catch {
      return;
    }
    switch (msg.type) {
      case 'setup':
        this.callSid = msg.callSid || this.callSid;
        this.from = msg.from || this.from;
        break;
      case 'prompt':
        if (msg.voicePrompt && msg.voicePrompt.trim()) {
          this.heardSomething = true;
          this.queue = this.queue.then(() => this.respond(msg.voicePrompt.trim())).catch((e) => {
            this.log.error('Erreur pendant la réponse', e);
            this.say("Excusez-moi, j'ai un souci technique. Je transmets votre demande à la responsable, qui vous rappellera.");
          });
        }
        break;
      case 'interrupt':
        this.abort?.abort();
        break;
      case 'error':
        this.log.error('Erreur ConversationRelay', msg.description);
        break;
      default:
        break; // dtmf, etc.
    }
  }

  say(text) {
    this.send({ type: 'text', token: text, last: true });
  }

  async respond(userText) {
    this.history.push({ role: 'user', content: userText });
    this.turns.push({ role: 'appelant', text: userText, at: new Date().toISOString() });
    this.abort = new AbortController();
    let spoken = '';
    try {
      for (let i = 0; i < 6; i++) {
        const stream = this.deps.client.messages.stream(
          {
            model: this.deps.cfg.model,
            max_tokens: 400,
            system: this.systemPrompt,
            tools: TOOL_DEFINITIONS,
            messages: this.history,
          },
          { signal: this.abort.signal },
        );
        stream.on('text', (t) => {
          spoken += t;
          this.send({ type: 'text', token: t, last: false });
        });
        const final = await stream.finalMessage();
        this.history.push({ role: 'assistant', content: final.content });
        if (final.stop_reason !== 'tool_use') break;
        const results = [];
        for (const block of final.content.filter((b) => b.type === 'tool_use')) {
          try {
            const out = await runTool(block.name, block.input, this, this.deps);
            results.push({ type: 'tool_result', tool_use_id: block.id, content: JSON.stringify(out) });
          } catch (err) {
            this.log.error(`Outil ${block.name} en échec`, err.message);
            results.push({
              type: 'tool_result',
              tool_use_id: block.id,
              is_error: true,
              content: "L'outil a échoué. Propose de prendre un message pour un rappel.",
            });
          }
        }
        this.history.push({ role: 'user', content: results });
      }
    } catch (err) {
      if (this.abort.signal.aborted) {
        // L'appelant a coupé la parole : on garde ce qui a été dit.
        if (spoken) this.history.push({ role: 'assistant', content: spoken });
      } else {
        throw err;
      }
    } finally {
      if (spoken) this.turns.push({ role: 'assistante', text: spoken, at: new Date().toISOString() });
    }
    this.send({ type: 'text', token: '', last: true });
    if (this.endRequested) this.send({ type: 'end' });
  }

  /** Appelé à la fermeture de la connexion. */
  async finish() {
    await this.queue.catch(() => {});
    const { store, notify } = this.deps;
    if (this.transcribe && this.turns.length > 0) {
      await store.saveTranscript(this.callSid || `inconnu-${Date.now()}`, this.turns);
    }
    if (this.heardSomething && !this.messageSaved) {
      await notify(`Appel de ${this.from || 'numéro inconnu'} terminé sans message enregistré.`);
    }
  }
}
