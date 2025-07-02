import getDb from '../../lib/db';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      const db = await getDb();
      const pageViews = await db.all('SELECT page, COUNT(*) as count FROM page_views GROUP BY page ORDER BY count DESC');
      const totalViews = await db.get('SELECT COUNT(*) as count FROM page_views');

      res.status(200).json({
        pageViews: pageViews,
        totalViews: totalViews.count,
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
      res.status(500).json({ message: 'Error fetching stats' });
    }
  } else {
    res.status(405).json({ message: 'Method Not Allowed' });
  }
}
