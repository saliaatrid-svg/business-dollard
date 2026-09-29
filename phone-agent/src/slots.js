/** Décalage (ms) du fuseau `tz` par rapport à l'UTC à l'instant `date`. */
function tzOffsetMs(date, tz) {
  const parts = Object.fromEntries(
    new Intl.DateTimeFormat('en-US', {
      timeZone: tz,
      hourCycle: 'h23',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    })
      .formatToParts(date)
      .map((p) => [p.type, p.value]),
  );
  const asUtc = Date.UTC(+parts.year, +parts.month - 1, +parts.day, +parts.hour, +parts.minute, +parts.second);
  return asUtc - Math.floor(date.getTime() / 1000) * 1000;
}

/** Heure locale (y, m, d, h, min) dans `tz` -> Date UTC. */
export function zonedToUtc(y, m, d, h, min, tz) {
  const guess = Date.UTC(y, m - 1, d, h, min);
  let result = guess - tzOffsetMs(new Date(guess), tz);
  result = guess - tzOffsetMs(new Date(result), tz);
  return new Date(result);
}

function localYmd(date, tz) {
  const p = Object.fromEntries(
    new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' })
      .formatToParts(date)
      .map((x) => [x.type, x.value]),
  );
  return { y: +p.year, m: +p.month, d: +p.day };
}

export function formatSlot(date, tz) {
  return new Intl.DateTimeFormat('fr-FR', {
    timeZone: tz,
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
}

/**
 * Créneaux libres selon les horaires d'ouverture.
 * @param {object} o
 * @param {Date} o.now
 * @param {Record<string,[number,number]>} o.businessHours jour ISO (1=lundi) -> [ouverture, fermeture]
 * @param {{start:Date,end:Date}[]} o.busy
 */
export function generateSlots({ now, businessHours, busy, durationMin, minNoticeHours, tz, days = 14, count = 4 }) {
  const earliest = now.getTime() + minNoticeHours * 3600_000;
  const slots = [];
  const base = localYmd(now, tz);
  for (let i = 0; i <= days && slots.length < count; i++) {
    const day = new Date(Date.UTC(base.y, base.m - 1, base.d + i, 12));
    const isoDow = ((day.getUTCDay() + 6) % 7) + 1;
    const hours = businessHours[String(isoDow)];
    if (!hours) continue;
    const [open, close] = hours;
    for (let h = open; h * 60 + durationMin <= close * 60 && slots.length < count; h += durationMin / 60) {
      const hh = Math.floor(h);
      const mm = Math.round((h - hh) * 60);
      const start = zonedToUtc(day.getUTCFullYear(), day.getUTCMonth() + 1, day.getUTCDate(), hh, mm, tz);
      const end = new Date(start.getTime() + durationMin * 60_000);
      if (start.getTime() < earliest) continue;
      if (busy.some((b) => start < b.end && end > b.start)) continue;
      slots.push({ start, end, label: formatSlot(start, tz) });
    }
  }
  return slots;
}
