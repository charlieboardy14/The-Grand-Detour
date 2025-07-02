import { Pool } from 'pg';

let pool;

async function getDb() {
  if (!pool) {
    pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      ssl: {
        rejectUnauthorized: false, // Required for some cloud providers like Heroku, Supabase
      },
    });

    // Test the connection and create table if it doesn't exist
    try {
      const client = await pool.connect();
      await client.query(`
        CREATE TABLE IF NOT EXISTS page_views (
          id SERIAL PRIMARY KEY,
          page TEXT NOT NULL,
          timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
      `);
      client.release();
      console.log('PostgreSQL connected and table checked/created.');
    } catch (err) {
      console.error('Error connecting to PostgreSQL or creating table:', err);
      throw err;
    }
  }
  return pool;
}

export default getDb;