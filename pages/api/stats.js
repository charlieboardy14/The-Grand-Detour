import getDb from '../../lib/db';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      const pool = await getDb();
      const pageViewsResult = await pool.query('SELECT page, COUNT(*) as count FROM page_views GROUP BY page ORDER BY count DESC');
      const totalViewsResult = await pool.query('SELECT COUNT(*) as count FROM page_views');

      res.status(200).json({
        pageViews: pageViewsResult.rows,
        totalViews: totalViewsResult.rows[0].count,
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
      res.status(500).json({ message: 'Error fetching stats' });
    }
  } else {
    res.status(405).json({ message: 'Method Not Allowed' });
  }
}
