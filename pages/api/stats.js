import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL, {
  tls: {
    rejectUnauthorized: false,
  },
});

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      const totalViews = await redis.get('total_page_views') || 0;

      // Get all page view keys (e.g., 'page_views:/about')
      const keys = await redis.keys('page_views:*');
      const pageViews = [];

      for (const key of keys) {
        const page = key.replace('page_views:', '');
        const count = await redis.get(key);
        pageViews.push({ page, count: parseInt(count, 10) });
      }

      // Sort by count in descending order
      pageViews.sort((a, b) => b.count - a.count);

      res.status(200).json({
        pageViews: pageViews,
        totalViews: parseInt(totalViews, 10),
      });
    } catch (error) {
      console.error('Error fetching stats from Redis:', error);
      res.status(500).json({ message: 'Error fetching stats' });
    }
  } else {
    res.status(405).json({ message: 'Method Not Allowed' });
  }
}