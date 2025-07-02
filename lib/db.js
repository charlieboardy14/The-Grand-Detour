import sqlite3 from 'sqlite3';
import { open } from 'sqlite';

const DATABASE_PATH = './tracking.db';

async function getDb() {
  const db = await open({
    filename: DATABASE_PATH,
    driver: sqlite3.Database,
  });

  await db.exec(`
    CREATE TABLE IF NOT EXISTS page_views (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      page TEXT NOT NULL,
      timestamp TEXT NOT NULL
    );
  `);

  return db;
}

export default getDb;
