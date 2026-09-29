/**
 * Notification Slack minimale : jamais de détail de santé, uniquement de quoi rappeler la personne.
 * Le détail reste dans le stockage local du serveur.
 */
export function createNotifier(webhookUrl, log = console) {
  return async function notify(text) {
    if (!webhookUrl) {
      log.info(`[notification] ${text}`);
      return;
    }
    try {
      const res = await fetch(webhookUrl, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      if (!res.ok) log.error(`Slack a répondu ${res.status}`);
    } catch (err) {
      log.error('Échec de la notification Slack', err.message);
    }
  };
}
