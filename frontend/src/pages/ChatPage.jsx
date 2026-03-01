import { useState } from 'react';
import { submitQuestion, getChatStatus } from '../api';
import ChatForm from '../components/ChatForm';
import ChatResponse from '../components/ChatResponse';

export default function ChatPage() {
  const [messageId, setMessageId] = useState(null);
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);

  const pollUntilDone = async (id) => {
    const maxAttempts = 7;
    const timeoutMs = 20000;
    const pollIntervalMs = 3000;
    const startMs = Date.now();

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
      const elapsedMs = Date.now() - startMs;
      const remainingMs = timeoutMs - elapsedMs;
      if (remainingMs <= 0) break;
      await new Promise((r) => setTimeout(r, Math.min(pollIntervalMs, remainingMs)));
    }
    setError('Response timed out after 20 seconds (7 retrieval attempts)');
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
