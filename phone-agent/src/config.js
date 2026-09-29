const env = process.env;

function required(name) {
  const v = env[name];
  if (!v) throw new Error(`Variable d'environnement manquante : ${name}`);
  return v;
}

export function loadConfig() {
  return {
    port: Number(env.PORT || 8080),
    publicUrl: required('PUBLIC_URL').replace(/\/$/, ''),
    anthropicKey: required('ANTHROPIC_API_KEY'),
    twilioAuthToken: required('TWILIO_AUTH_TOKEN'),
    signingSecret: required('SIGNING_SECRET'),
    model: env.CLAUDE_MODEL || 'claude-haiku-4-5-20251001',
    language: env.LANGUAGE || 'fr-FR',
    ttsProvider: env.TTS_PROVIDER || 'Google',
    ttsVoice: env.TTS_VOICE || '',
    sttProvider: env.STT_PROVIDER || 'Google',
    slackWebhook: env.SLACK_WEBHOOK_URL || '',
    calendarId: env.GOOGLE_CALENDAR_ID || '',
    serviceAccountFile: env.GOOGLE_SERVICE_ACCOUNT_FILE || '',
    timezone: env.TIMEZONE || 'Europe/Paris',
    businessHours: JSON.parse(
      env.BUSINESS_HOURS || '{"1":[9,17],"2":[9,17],"3":[9,17],"4":[9,17],"5":[9,17]}',
    ),
    appointmentMinutes: Number(env.APPOINTMENT_MINUTES || 60),
    minNoticeHours: Number(env.MIN_NOTICE_HOURS || 24),
    retentionDays: Number(env.RETENTION_DAYS || 30),
    dataDir: env.DATA_DIR || './data',
  };
}
