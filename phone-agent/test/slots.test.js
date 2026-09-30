import test from 'node:test';
import assert from 'node:assert/strict';
import { generateSlots, zonedToUtc } from '../src/slots.js';

const hours = { 1: [9, 17], 2: [9, 17], 3: [9, 17], 4: [9, 17], 5: [9, 17] };
const base = { businessHours: hours, durationMin: 60, minNoticeHours: 24, tz: 'Europe/Paris' };

test('conversion heure de Paris été / hiver', () => {
  assert.equal(zonedToUtc(2026, 7, 1, 9, 0, 'Europe/Paris').toISOString(), '2026-07-01T07:00:00.000Z');
  assert.equal(zonedToUtc(2026, 1, 15, 9, 0, 'Europe/Paris').toISOString(), '2026-01-15T08:00:00.000Z');
});

test('créneaux : jours ouvrés, préavis, pas de week-end', () => {
  const now = new Date('2026-09-29T13:00:00Z'); // mardi 15h à Paris
  const slots = generateSlots({ ...base, now, busy: [], count: 20 });
  assert.ok(slots.length > 0);
  assert.ok(slots.every((s) => s.start.getTime() >= now.getTime() + 24 * 3600_000));
  assert.ok(slots.every((s) => ![0, 6].includes(s.start.getUTCDay())));
  assert.equal(slots[0].start.toISOString(), '2026-09-30T13:00:00.000Z'); // mercredi 15h Paris (préavis 24 h)
});

test('créneaux : évite les plages occupées', () => {
  const now = new Date('2026-09-29T13:00:00Z');
  const busy = [{ start: new Date('2026-09-30T13:00:00Z'), end: new Date('2026-09-30T14:00:00Z') }];
  const slots = generateSlots({ ...base, now, busy, count: 2 });
  assert.equal(slots[0].start.toISOString(), '2026-09-30T14:00:00.000Z');
});
