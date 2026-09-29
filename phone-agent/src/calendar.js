import { google } from 'googleapis';
import { generateSlots } from './slots.js';

/** Agenda Google via compte de service. Renvoie null si non configuré. */
export function createCalendar(cfg) {
  if (!cfg.calendarId || !cfg.serviceAccountFile) return null;
  const auth = new google.auth.GoogleAuth({
    keyFile: cfg.serviceAccountFile,
    scopes: ['https://www.googleapis.com/auth/calendar'],
  });
  const api = google.calendar({ version: 'v3', auth });

  async function listSlots(now = new Date()) {
    const horizon = new Date(now.getTime() + 15 * 86_400_000);
    const res = await api.freebusy.query({
      requestBody: { timeMin: now.toISOString(), timeMax: horizon.toISOString(), items: [{ id: cfg.calendarId }] },
    });
    const busy = (res.data.calendars?.[cfg.calendarId]?.busy ?? []).map((b) => ({
      start: new Date(b.start),
      end: new Date(b.end),
    }));
    return generateSlots({
      now,
      businessHours: cfg.businessHours,
      busy,
      durationMin: cfg.appointmentMinutes,
      minNoticeHours: cfg.minNoticeHours,
      tz: cfg.timezone,
    });
  }

  async function createTentative({ start, end, name, phone, category }) {
    const res = await api.events.insert({
      calendarId: cfg.calendarId,
      requestBody: {
        summary: `RDV à confirmer : ${name}`,
        description: `Demande prise par l'assistante téléphonique.\nTéléphone : ${phone}\nMotif : ${category}\nÀ confirmer par DMS par rappel.`,
        start: { dateTime: start.toISOString(), timeZone: cfg.timezone },
        end: { dateTime: end.toISOString(), timeZone: cfg.timezone },
        status: 'tentative',
      },
    });
    return res.data.id;
  }

  return { listSlots, createTentative };
}
