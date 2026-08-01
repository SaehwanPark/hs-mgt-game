const API_ROOT = "/api/v1/sessions";

export function createLocalActionAdapter({ fetchImpl = globalThis.fetch } = {}) {
  let activeSessionId = null;
  let activeCampaign = null;

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
    get campaign() { return activeCampaign; },

    activateSession(sessionId, campaign = null) {
      activeSessionId = String(sessionId ?? "").trim() || null;
      activeCampaign = campaign;
    },

    async startSession(options) {
      const envelope = await request(API_ROOT, {
        method: "POST",
        body: JSON.stringify(options),
      });
      activeSessionId = envelope?.session_id ?? null;
      activeCampaign = envelope?.campaign ?? options?.campaign ?? null;
      return envelope;
    },

    async getPresentation(sessionId) {
      return request(sessionPath(sessionId, "presentation"));
    },

    async getSession(sessionId) {
      return request(`${API_ROOT}/${encodeURIComponent(String(sessionId ?? "").trim())}`);
    },

    async listCheckpoints() {
      return request("/api/v1/checkpoints");
    },

    async downloadCheckpointArtifact(sessionId, storage) {
      const query = storage ? `?storage=${encodeURIComponent(storage)}` : "";
      const response = await fetchImpl(`${sessionPath(sessionId, "save-artifact")}${query}`);
      if (!response.ok) {
        const payload = await response.json().catch(() => null);
        const error = new Error(payload?.error ?? `GUI host request failed (${response.status}).`);
        if (payload?.code) error.code = payload.code;
        throw error;
      }
      const disposition = response.headers?.get?.("Content-Disposition") ?? "";
      const match = disposition.match(/filename="([A-Za-z0-9_.-]+)"/);
      return {
        blob: await response.blob(),
        filename: match?.[1] ?? `hs-mgt-checkpoint-${String(sessionId).trim()}.save`,
      };
    },

    async getCampaignCoverage(sessionId) {
      return request(sessionPath(sessionId, "campaign-coverage"));
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
