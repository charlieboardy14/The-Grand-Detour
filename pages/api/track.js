import getDb from '../../lib/db';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { page, timestamp } = req.body;

    try {
      const pool = await getDb();
      await pool.query('INSERT INTO page_views (page, timestamp) VALUES ($1, $2)', [page, timestamp]);
      res.status(200).json({ message: 'Tracking data received and stored' });
    } catch (error) {
      console.error('Error storing tracking data:', error);
      res.status(500).json({ message: 'Error storing tracking data' });
    }
  } else {
    res.status(405).json({ message: 'Method Not Allowed' });
  }
}
