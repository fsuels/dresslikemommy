import { createAdminReader, SourceError } from './collector.js';
import { resolveShopifyAdminToken } from './shopify-auth.js';

// Cloud uses an explicit, catalog-only credential mode. The existing local
// rehearsal may still supply its legacy token without entering this new mode.
export async function createConfiguredAdminReader(env, config, options = {}) {
  let token;
  if (env.SHOPIFY_AUTH_MODE === 'client_credentials') {
    token = await resolveShopifyAdminToken(env, { ...options, domain: config.storeDomain });
  } else {
    if (env.SHOPIFY_AUTH_MODE !== undefined) throw new SourceError('shopify_auth_mode_invalid');
    if (env.SHOPIFY_CLIENT_ID || env.SHOPIFY_CLIENT_SECRET) throw new SourceError('shopify_auth_mode_required');
    token = env.SHOPIFY_ADMIN_ACCESS_TOKEN;
  }
  return createAdminReader({ domain: config.storeDomain, token, apiVersion: config.apiVersion,
    ...(options.fetchImpl ? { fetchImpl: options.fetchImpl } : {}) });
}
