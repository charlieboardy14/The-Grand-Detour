import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL, {
  tls: {
    rejectUnauthorized: false,
  },
});

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { page } = req.body; // We only need the page for counting

    try {
      // Increment total page views
      await redis.incr('total_page_views');
      // Increment views for specific page
      await redis.incr(`page_views:${page}`);

      res.status(200).json({ message: 'Tracking data received and stored in Redis' });
    } catch (error) {
      console.error('Error storing tracking data in Redis:', error);
      res.status(500).json({ message: 'Error storing tracking data' });
    }
  } else {
    res.status(405).json({ message: 'Method Not Allowed' });
  }
}
