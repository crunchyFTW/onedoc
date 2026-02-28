import { useState } from 'react';

export default function ChatForm({ onSubmit, disabled }) {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!question.trim() || disabled) return;
    onSubmit(question.trim());
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: 16 }}>
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a medical question..."
        rows={3}
        disabled={disabled}
        style={{ width: '100%', padding: 8, marginBottom: 8 }}
      />
      <button type="submit" disabled={disabled || !question.trim()}>
        {disabled ? 'Processing...' : 'Submit'}
      </button>
    </form>
  );
}
