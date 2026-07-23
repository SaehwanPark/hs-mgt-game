const API_ROOT = "/api/v1/sessions";

export function createLocalActionAdapter({ fetchImpl = globalThis.fetch } = {}) {
  let activeSessionId = null;

  async function request(path, options = {}) {
    const response = await fetchImpl(path, {
      ...options,
      headers: options.body ? { "Content-Type": "application/json", ...options.headers } : options.headers,
    });
    const payload = await response.json().catch(() => null);
    if (!response.ok) {
      const error = new Error(payload?.error ?? `GUI host request failed (${response.status}).`);
      if (payload?.code) error.code = payload.code;
      throw error;
    }
    return payload;
  }

  function sessionPath(sessionId, suffix) {
    const id = String(sessionId ?? "").trim();
    if (!id) throw new Error("A live session ID is required.");
    return `${API_ROOT}/${encodeURIComponent(id)}/${suffix}`;
  }

  return {
    get sessionId() { return activeSessionId; },

    activateSession(sessionId) {
      activeSessionId = String(sessionId ?? "").trim() || null;
    },

    async startSession(options) {
      return request(API_ROOT, {
        method: "POST",
        body: JSON.stringify(options),
      });
    },

    async getPresentation(sessionId) {
      return request(sessionPath(sessionId, "presentation"));
    },

    async getRegionalWorld(sessionId) {
      return request(sessionPath(sessionId, "regional-world"));
    },

    async getHistory(sessionId) {
      return request(sessionPath(sessionId, "history"));
    },

    async getReplay(sessionId) {
      return request(sessionPath(sessionId, "replay"));
    },

    async saveSession(sessionId) {
      return request(sessionPath(sessionId, "save"), { method: "POST" });
    },

    async loadSession(sessionId) {
      return request(sessionPath(sessionId, "load"), { method: "POST" });
    },

    async endSession(sessionId) {
      return request(sessionPath(sessionId, "end"), { method: "POST" });
    },

    async getActionCatalog(sessionId) {
      return request(sessionPath(sessionId, "action-catalog"));
    },

    async validateTurn(sessionId, commandText) {
      return request(sessionPath(sessionId, "validation"), {
        method: "POST",
        body: JSON.stringify({ command_text: commandText }),
      });
    },

    async getResolution(sessionId, turn) {
      const query = turn == null ? "" : `?turn=${encodeURIComponent(turn)}`;
      return request(`${sessionPath(sessionId, "resolution")}${query}`);
    },

    async submitTurn(commandText) {
      return request(sessionPath(activeSessionId, "turns"), {
        method: "POST",
        body: JSON.stringify({ command_text: commandText }),
      });
    },
  };
}

globalThis.HsMgtGameActionAdapter ??= createLocalActionAdapter();
