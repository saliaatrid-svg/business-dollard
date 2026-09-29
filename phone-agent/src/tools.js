export const TOOL_DEFINITIONS = [
  {
    name: 'save_message',
    description:
      "Enregistre un message pour que la responsable de DMS rappelle la personne. À utiliser dès que l'appelant veut être rappelé ou pose une question sans réponse dans les informations.",
    input_schema: {
      type: 'object',
      properties: {
        caller_name: { type: 'string', description: 'Prénom et nom' },
        callback_number: { type: 'string', description: "Numéro de rappel ; omettre si l'appelant demande d'utiliser le numéro d'appel" },
        commune: { type: 'string', description: 'Commune, si donnée' },
        reason_category: {
          type: 'string',
          enum: ['information', 'nouvelle_demande', 'rendez_vous', 'client_existant', 'autre'],
        },
        urgency: { type: 'string', enum: ['normale', 'haute'] },
        note: { type: 'string', description: 'Une phrase sur le besoin, sans détail de santé' },
      },
      required: ['caller_name', 'reason_category', 'urgency'],
    },
  },
  {
    name: 'check_availability',
    description: "Donne les prochains créneaux de rendez-vous libres dans l'agenda de DMS.",
    input_schema: { type: 'object', properties: {} },
  },
  {
    name: 'request_appointment',
    description:
      "Enregistre une demande de rendez-vous sur un des créneaux renvoyés par check_availability. Le rendez-vous reste à confirmer par DMS.",
    input_schema: {
      type: 'object',
      properties: {
        caller_name: { type: 'string' },
        callback_number: { type: 'string' },
        slot_start_iso: { type: 'string', description: "Le champ start_iso exact d'un créneau proposé" },
        reason_category: {
          type: 'string',
          enum: ['information', 'nouvelle_demande', 'rendez_vous', 'client_existant', 'autre'],
        },
      },
      required: ['caller_name', 'slot_start_iso', 'reason_category'],
    },
  },
  {
    name: 'alert_urgent',
    description: "Prévient DMS d'une situation d'urgence ou de danger signalée par l'appelant.",
    input_schema: { type: 'object', properties: {} },
  },
  {
    name: 'refuse_transcription',
    description: "L'appelant refuse que l'appel soit transcrit : la conversation ne sera pas conservée.",
    input_schema: { type: 'object', properties: {} },
  },
  {
    name: 'end_call',
    description: "Termine l'appel, après avoir dit au revoir.",
    input_schema: { type: 'object', properties: {} },
  },
];

/**
 * Exécute un outil. `session` porte : from, transcribe, endRequested, slots.
 * `deps` : store, notify, calendar (peut être null), cfg.
 */
export async function runTool(name, input, session, deps) {
  const { store, notify, calendar, cfg } = deps;
  switch (name) {
    case 'save_message': {
      const id = await store.saveMessage({
        callSid: session.callSid,
        callerName: input.caller_name,
        callbackNumber: input.callback_number || session.from,
        commune: input.commune || '',
        category: input.reason_category,
        urgency: input.urgency,
        note: input.note || '',
      });
      const flag = input.urgency === 'haute' ? 'URGENT ' : '';
      await notify(
        `${flag}Nouveau message téléphonique #${id} : ${input.caller_name}, ${input.callback_number || session.from}, motif : ${input.reason_category}. Détail sur le serveur.`,
      );
      session.messageSaved = true;
      return { ok: true, id };
    }
    case 'check_availability': {
      if (!calendar) return { available: false, reason: "Agenda non connecté : propose de prendre un message pour un rappel." };
      const slots = await calendar.listSlots();
      session.slots = slots;
      return {
        available: slots.length > 0,
        slots: slots.map((s) => ({ start_iso: s.start.toISOString(), label: s.label })),
      };
    }
    case 'request_appointment': {
      const slot = (session.slots || []).find((s) => s.start.toISOString() === input.slot_start_iso);
      if (!slot) return { ok: false, reason: "Ce créneau n'a pas été proposé. Appelle d'abord check_availability." };
      const phone = input.callback_number || session.from;
      const eventId = await calendar.createTentative({
        start: slot.start,
        end: slot.end,
        name: input.caller_name,
        phone,
        category: input.reason_category,
      });
      await store.saveMessage({
        callSid: session.callSid,
        callerName: input.caller_name,
        callbackNumber: phone,
        category: 'rendez_vous',
        urgency: 'normale',
        note: `Demande de rendez-vous ${slot.label} (événement ${eventId})`,
      });
      await notify(`Demande de rendez-vous à confirmer : ${input.caller_name}, ${phone}, ${slot.label}.`);
      session.messageSaved = true;
      return { ok: true, label: slot.label, statut: 'à confirmer par DMS' };
    }
    case 'alert_urgent':
      await notify(`URGENT : un appelant (${session.from}) signale une situation d'urgence. Rappeler sans délai.`);
      return { ok: true };
    case 'refuse_transcription':
      session.transcribe = false;
      return { ok: true };
    case 'end_call':
      session.endRequested = true;
      return { ok: true };
    default:
      return { ok: false, reason: `Outil inconnu : ${name}` };
  }
}
