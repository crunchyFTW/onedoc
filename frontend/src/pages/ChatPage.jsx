import { useState } from 'react';
import { submitQuestion, getChatStatus } from '../api';
import ChatForm from '../components/ChatForm';
import ChatResponse from '../components/ChatResponse';

export default function ChatPage() {
  const [messageId, setMessageId] = useState(null);
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);

  const pollUntilDone = async (id) => {
    // Keep retrieval attempts small and predictable for assignment simplicity.
    const maxAttempts = 3;
    const pollIntervalMs = 5000;
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
    setError('Response timed out after 3 retrieval attempts');
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
