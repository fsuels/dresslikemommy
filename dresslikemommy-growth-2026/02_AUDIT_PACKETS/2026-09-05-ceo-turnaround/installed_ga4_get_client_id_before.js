async function getClientId() {
    const ga = await cookies.get("_ga");
    if (ga && typeof ga === "string") {
      const parts = ga.split(".");
      if (parts.length >= 4) {
        const candidate = parts.slice(2, parts.length - 1).join(".");
        if (candidate) {
          await storage.set(CLIENT_ID_STORAGE_KEY, candidate);
          return candidate;
        }
      }
    }
    const stored = await storage.get(CLIENT_ID_STORAGE_KEY);
    if (stored) return stored;
    const fresh = `${Math.floor(Math.random() * 1e10)}.${Math.floor(Date.now() / 1000)}`;
    await storage.set(CLIENT_ID_STORAGE_KEY, fresh);
    return fresh;
  }
