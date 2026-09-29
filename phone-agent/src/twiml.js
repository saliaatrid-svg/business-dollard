const esc = (s) =>
  String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

export const GREETING =
  "Bonjour, vous êtes bien chez DMS, De la Mémoire aux Soins. " +
  "Je suis l'assistante virtuelle. Votre appel est transcrit pour traiter votre demande ; " +
  "dites-le-moi si vous préférez qu'il ne le soit pas. " +
  "En cas d'urgence, raccrochez et appelez le 15. Comment puis-je vous aider ?";

export function buildVoiceTwiml({ wsUrl, language, ttsProvider, ttsVoice, sttProvider }) {
  const voice = ttsVoice ? ` voice="${esc(ttsVoice)}"` : '';
  return (
    `<?xml version="1.0" encoding="UTF-8"?>` +
    `<Response><Connect>` +
    `<ConversationRelay url="${esc(wsUrl)}" language="${esc(language)}" ` +
    `ttsProvider="${esc(ttsProvider)}"${voice} transcriptionProvider="${esc(sttProvider)}" ` +
    `welcomeGreeting="${esc(GREETING)}" interruptible="true"/>` +
    `</Connect></Response>`
  );
}

export const REFUSAL_TWIML =
  `<?xml version="1.0" encoding="UTF-8"?><Response><Reject/></Response>`;
