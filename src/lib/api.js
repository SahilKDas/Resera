const configuredBase = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '');

export const apiConfigured = Boolean(configuredBase) || import.meta.env.DEV;
let csrfToken = '';

async function ensureCsrf() {
  if (csrfToken) return csrfToken;
  const response = await fetch(`${configuredBase}/api/auth/csrf/`, { credentials: 'include' });
  if (!response.ok) throw new Error('The account service could not be reached.');
  csrfToken = (await response.json()).csrfToken;
  return csrfToken;
}

async function request(path, options = {}) {
  if (!apiConfigured) {
    throw new Error('The account service is not connected to this website yet.');
  }

  const method = options.method || 'GET';
  const headers = { ...(options.headers || {}) };
  if (options.body) headers['Content-Type'] = 'application/json';
  if (!['GET', 'HEAD', 'OPTIONS'].includes(method)) {
    headers['X-CSRFToken'] = await ensureCsrf();
  }

  const response = await fetch(`${configuredBase}${path}`, {
    ...options,
    method,
    headers,
    credentials: 'include'
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.error || 'Something went wrong. Please try again.');
  return payload;
}

export const authApi = {
  me: () => request('/api/auth/me/'),
  login: (payload) => request('/api/auth/login/', { method: 'POST', body: JSON.stringify(payload) }),
  register: (payload) => request('/api/auth/register/', { method: 'POST', body: JSON.stringify(payload) }),
  logout: () => request('/api/auth/logout/', { method: 'POST' })
};

export const opportunityApi = {
  list: () => request('/api/opportunities/'),
  submit: (payload) => request('/api/opportunities/', { method: 'POST', body: JSON.stringify(payload) })
};
