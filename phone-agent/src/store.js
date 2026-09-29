import { mkdir, writeFile, readdir, stat, rm } from 'node:fs/promises';
import { join } from 'node:path';
import { randomUUID } from 'node:crypto';

/** Stockage local (fichiers JSON, droits 0600). Le dossier doit être sur un volume chiffré. */
export function createStore(dataDir, retentionDays) {
  const dirs = { messages: join(dataDir, 'messages'), transcripts: join(dataDir, 'transcripts') };

  async function write(kind, id, obj) {
    await mkdir(dirs[kind], { recursive: true, mode: 0o700 });
    await writeFile(join(dirs[kind], `${id}.json`), JSON.stringify(obj, null, 2), { mode: 0o600 });
  }

  return {
    async saveMessage(msg) {
      const id = randomUUID().slice(0, 8);
      await write('messages', id, { id, createdAt: new Date().toISOString(), ...msg });
      return id;
    },
    saveTranscript(callSid, turns) {
      return write('transcripts', callSid, { callSid, savedAt: new Date().toISOString(), turns });
    },
    /** Supprime les fichiers plus vieux que la durée de conservation. */
    async purge(now = Date.now()) {
      const limit = now - retentionDays * 86_400_000;
      let removed = 0;
      for (const dir of Object.values(dirs)) {
        let files = [];
        try {
          files = await readdir(dir);
        } catch {
          continue;
        }
        for (const f of files) {
          const p = join(dir, f);
          if ((await stat(p)).mtimeMs < limit) {
            await rm(p);
            removed++;
          }
        }
      }
      return removed;
    },
  };
}
