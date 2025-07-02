import Head from 'next/head';
import Link from 'next/link';
import styles from './layout.module.css';

export const siteTitle = 'The Grand Detour';

export default function Layout({ children, home }) {
  return (
    <div className={styles.container}>
      <Head>
        <link rel="icon" href="/favicon.ico" />
        <meta
          name="description"
          content="The latest news, reviews, and stories from the automotive world."
        />
        <meta name="og:title" content={siteTitle} />
      </Head>
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <a className={styles.logo}>The Grand Detour</a>
          <p className={styles.strapline}>Hitpieces On Any Car (Especially Small Hatchbacks)</p>
          <div className={styles.mainSloganContainer}>
            <h2 className={styles.mainSloganTitle}>Welcome to The Grand Detour</h2>
            <p className={styles.mainSloganText}>Hitpieces On Any Car (Especially Small Hatchbacks)</p>
          </div>
          <nav>
            <Link href="/">Home</Link> | <Link href="/posts">Blog</Link> | <Link href="/admin">Admin</Link> | <Link href="/contact">Contact</Link> | <Link href="/request">Request a Hitpiece</Link>
          </nav>
        </div>
      </header>
      <main>{children}</main>
    </div>
  );
}