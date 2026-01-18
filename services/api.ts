/**
 * API Client
 *
 * Responsibility: HTTP client for communicating with the FastAPI backend.
 * All backend API calls should go through this client.
 *
 * TODO: Add request/response interceptors
 * TODO: Add auth token injection
 * TODO: Add error handling and retry logic
 */

const API_URL = process.env.EXPO_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Base fetch wrapper with common configuration
 */
async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_URL}${endpoint}`;

  // TODO: Get auth token from session and inject into headers
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    // TODO: Implement proper error handling
    throw new Error(`API Error: ${response.status}`);
  }

  return response.json();
}

/**
 * API client with typed methods for each endpoint
 *
 * TODO: Add methods for each backend endpoint
 */
export const api = {
  // Health check
  health: () => request<{ status: string }>("/health"),

  // TODO: Add drill endpoints
  // drills: {
  //   getToday: () => request<Drill>("/drills/today"),
  //   submit: (drillId: string, response: string) => request("/drills/submit", { ... }),
  // },

  // TODO: Add progress endpoints
  // TODO: Add tracks endpoints
};
