import { useState, useEffect } from 'react';
import { getStatistics } from '../api';

export default function StatsPage() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

  const fetchStats = async () => {
    try {
      const data = await getStatistics();
      setStats(data);
      setError(null);
    } catch (e) {
      setError(e.message || 'Failed to load statistics');
    }
  };

  useEffect(() => {
    fetchStats();
    const id = setInterval(fetchStats, 5000);
    return () => clearInterval(id);
  }, []);

  return (
    <div style={{ padding: 24, maxWidth: 600, margin: '0 auto' }}>
      <h1>System Statistics</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {stats && (
        <dl style={{ textAlign: 'left' }}>
          <dt>Messages Processed</dt>
          <dd>{stats.messagesProcessed}</dd>
          <dt>Messages Succeeded</dt>
          <dd>{stats.messagesSucceeded}</dd>
          <dt>Messages Failed</dt>
          <dd>{stats.messagesFailed}</dd>
          <dt>Total Retries</dt>
          <dd>{stats.totalRetries}</dd>
          <dt>Average Processing Time (ms)</dt>
          <dd>{stats.averageProcessingTimeMs}</dd>
          <dt>Average Tokens per Message</dt>
          <dd>{stats.averageTokensPerMessage}</dd>
          <dt>Total Tokens Used</dt>
          <dd>{stats.totalTokensUsed}</dd>
          <dt>Current Queue Length</dt>
          <dd>{stats.currentQueueLength}</dd>
          <dt>Idle Workers</dt>
          <dd>{stats.idleWorkers}</dd>
          <dt>Active Workers</dt>
          <dd>{stats.activeWorkers}</dd>
        </dl>
      )}
      <button onClick={fetchStats} style={{ marginTop: 16 }}>
        Refresh
      </button>
    </div>
  );
}
