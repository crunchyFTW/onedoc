import { useState } from 'react';
import { submitQuestion, getChatStatus } from '../api';
import ChatForm from '../components/ChatForm';
import ChatResponse from '../components/ChatResponse';

export default function ChatPage() {
  const [messageId, setMessageId] = useState(null);
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);

  const pollUntilDone = async (id) => {
    const maxAttempts = 90; // ~7.5 min max at 5s intervals
    const pollIntervalMs = 5000; // Poll every 5s (backend may take 30-45s on rate limits)
    for (let i = 0; i < maxAttempts; i++) {
      try {
        const data = await getChatStatus(id);
        setStatus(data);
        if (data.status === 'completed' || data.status === 'failed') return;
      } catch (e) {
        setError(e.message || 'Something went wrong');
        setStatus(null);
        return;
      }
      await new Promise((r) => setTimeout(r, pollIntervalMs));
    }
    setError('Response timed out');
    setStatus(null);
  };

  const handleSubmit = async (question) => {
    setError(null);
    setStatus(null);
    setMessageId(null);
    try {
      const { messageId: id } = await submitQuestion(question);
      setMessageId(id);
      setStatus({ status: 'processing' });
      await pollUntilDone(id);
    } catch (e) {
      setError(e.message || 'Something went wrong');
      setStatus(null);
    }
  };

  return (
    <div style={{ padding: 24, maxWidth: 600, margin: '0 auto' }}>
      <h1>Medical Expert AI Chat</h1>
      <ChatForm onSubmit={handleSubmit} disabled={status?.status === 'processing'} />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {status && !error && <ChatResponse status={status} messageId={messageId} />}
    </div>
  );
}
