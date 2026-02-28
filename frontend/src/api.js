const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function submitQuestion(question) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) throw new Error('Failed to submit question');
  return res.json();
}

export async function getChatStatus(messageId) {
  const res = await fetch(`${API_BASE}/chat/${messageId}`);
  if (res.status === 404) throw new Error('Message not found');
  if (!res.ok) throw new Error('Failed to fetch status');
  return res.json();
}

export async function getStatistics() {
  const res = await fetch(`${API_BASE}/statistics`);
  if (!res.ok) throw new Error('Failed to fetch statistics');
  return res.json();
}
