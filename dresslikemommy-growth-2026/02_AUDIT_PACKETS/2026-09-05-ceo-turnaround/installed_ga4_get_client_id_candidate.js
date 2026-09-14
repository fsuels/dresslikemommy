async function getClientId() {
    const ga = await cookies.get("_ga");
    if (ga && typeof ga === "string") {
      await storage.set(CLIENT_ID_STORAGE_KEY, ga);
      return ga;
    }
    const stored = await storage.get(CLIENT_ID_STORAGE_KEY);
    if (stored) return stored;
    const fresh = `${Math.floor(Math.random() * 1e10)}.${Math.floor(Date.now() / 1000)}`;
    await storage.set(CLIENT_ID_STORAGE_KEY, fresh);
    return fresh;
  }
