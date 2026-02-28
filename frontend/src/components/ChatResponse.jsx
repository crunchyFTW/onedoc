export default function ChatResponse({ status, messageId }) {
  if (!status) return null;

  const baseStyle = { padding: 16, borderRadius: 8, color: '#1a1a1a' };

  if (status.status === 'processing') {
    return (
      <div style={{ ...baseStyle, background: '#e3f2fd' }}>
        <p><strong>Processing...</strong> (ID: {messageId})</p>
      </div>
    );
  }

  if (status.status === 'completed') {
    return (
      <div style={{ ...baseStyle, background: '#e8f5e9', border: '1px solid #a5d6a7' }}>
        <p style={{ whiteSpace: 'pre-wrap', lineHeight: 1.5 }}>{status.answer}</p>
      </div>
    );
  }

  if (status.status === 'failed') {
    return (
      <div style={{ ...baseStyle, background: '#ffebee', border: '1px solid #ef9a9a' }}>
        <p><strong>Failed:</strong> {status.error}</p>
      </div>
    );
  }

  return null;
}
