import { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch('/api/stats');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setStats(data);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) return <div style={styles.container}>Loading analytics...</div>;
  if (error) return <div style={styles.container}>Error: {error}</div>;
  if (!stats) return <div style={styles.container}>No analytics data available.</div>;

  return (
    <div style={styles.container}>
      <Head>
        <title>Analytics Dashboard</title>
      </Head>
      <h1 style={styles.heading}>Website Analytics Dashboard</h1>

      <div style={styles.summaryContainer}>
        <div style={styles.summaryBox}>
          <h2 style={styles.summaryHeading}>Total Page Views</h2>
          <p style={styles.summaryValue}>{stats.totalViews}</p>
        </div>
      </div>

      <h2 style={styles.subHeading}>Page View Breakdown</h2>
      <div style={styles.tableContainer}>
        <table style={styles.table}>
          <thead>
            <tr>
              <th style={styles.th}>Page Path</th>
              <th style={styles.th}>Views</th>
            </tr>
          </thead>
          <tbody>
            {stats.pageViews.map((item, index) => (
              <tr key={index} style={index % 2 === 0 ? styles.trEven : styles.trOdd}>
                <td style={styles.td}>{item.page}</td>
                <td style={styles.td}>{item.count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={styles.backLinkContainer}>
        <Link href="/">
          <a style={styles.backLink}>← Back to Home</a>
        </Link>
      </div>
    </div>
  );
};

const styles = {
  container: {
    fontFamily: 'Arial, sans-serif',
    maxWidth: '900px',
    margin: '40px auto',
    padding: '20px',
    backgroundColor: '#f9f9f9',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    color: '#333',
  },
  heading: {
    textAlign: 'center',
    color: '#2c3e50',
    marginBottom: '30px',
    fontSize: '2.5em',
    borderBottom: '2px solid #eee',
    paddingBottom: '15px',
  },
  summaryContainer: {
    display: 'flex',
    justifyContent: 'center',
    marginBottom: '30px',
  },
  summaryBox: {
    backgroundColor: '#ffffff',
    padding: '20px 30px',
    borderRadius: '8px',
    boxShadow: '0 1px 5px rgba(0, 0, 0, 0.08)',
    textAlign: 'center',
    minWidth: '200px',
  },
  summaryHeading: {
    color: '#34495e',
    fontSize: '1.2em',
    margin: '0 0 10px 0',
  },
  summaryValue: {
    fontSize: '2.8em',
    fontWeight: 'bold',
    color: '#2980b9',
    margin: '0',
  },
  subHeading: {
    color: '#2c3e50',
    marginBottom: '20px',
    fontSize: '1.8em',
    borderBottom: '1px solid #eee',
    paddingBottom: '10px',
  },
  tableContainer: {
    overflowX: 'auto',
    marginBottom: '30px',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    backgroundColor: '#ffffff',
    borderRadius: '8px',
    overflow: 'hidden',
    boxShadow: '0 1px 5px rgba(0, 0, 0, 0.08)',
  },
  th: {
    backgroundColor: '#3498db',
    color: 'white',
    padding: '12px 15px',
    textAlign: 'left',
    fontWeight: 'bold',
    textTransform: 'uppercase',
    fontSize: '0.9em',
  },
  td: {
    padding: '10px 15px',
    borderBottom: '1px solid #ecf0f1',
    fontSize: '0.95em',
  },
  trEven: {
    backgroundColor: '#fefefe',
  },
  trOdd: {
    backgroundColor: '#f9f9f9',
  },
  backLinkContainer: {
    textAlign: 'center',
    marginTop: '30px',
  },
  backLink: {
    color: '#2980b9',
    textDecoration: 'none',
    fontSize: '1.1em',
    fontWeight: 'bold',
    padding: '10px 20px',
    border: '1px solid #2980b9',
    borderRadius: '5px',
    transition: 'background-color 0.3s ease, color 0.3s ease',
  },
  'a.backLink:hover': {
    backgroundColor: '#2980b9',
    color: 'white',
  },
};

export default Dashboard;
