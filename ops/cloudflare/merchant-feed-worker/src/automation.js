import host from './host.js';
import { runtimeConfig } from './worker.js';
import { enqueueRefresh, consumeRefresh } from './checkpoint.js';

export default {
  fetch: host.fetch,
  async scheduled(controller, env) {
    const config = runtimeConfig(env);
    const key = config.schedules?.[controller.cron] || (controller.cron === '0 * * * *' ? 'us-en' : null);
    if (key && config.markets.some(m => m.key === key && m.enabled)) await enqueueRefresh(env, key);
  },
  async queue(batch, env) {
    // Never multiply the per-invocation request budget on a misbound consumer.
    if (batch.messages.length !== 1) { for (const message of batch.messages) message.retry({ delaySeconds: 60 }); return; }
    for (const message of batch.messages) {
      try { await consumeRefresh(env, message.body); message.ack(); }
      catch { message.retry({ delaySeconds: 60 }); }
    }
  },
};
