import Head from 'next/head';
import Layout from '../components/layout';
import styles from '../styles/Request.module.css';

export default function Request() {
  return (
    <Layout>
      <Head>
        <title>Request a Hitpiece</title>
      </Head>
      <div className={styles.container}>
        <h1>Request a Hitpiece on Your Car</h1>
        <p>Do you have a car that just grinds your gears? A four-wheeled menace that deserves to be roasted? Send us the details and a picture, and we might just write a glorious hitpiece on it!</p>
        <p>We're looking for the quirks, the flaws, the infuriating design choices. The more "bad points" you give us, the better the hitpiece will be!</p>

        <form name="hitpiece-request" method="POST" data-netlify="true" data-netlify-honeypot="bot-field" enctype="multipart/form-data" className={styles.form}>
          <input type="hidden" name="form-name" value="hitpiece-request" />
          <p className={styles.hidden}>
            <label>Don’t fill this out if you’re human: <input name="bot-field" /></label>
          </p>
          
          <div className={styles.formGroup}>
            <label htmlFor="car-make-model">Car Make and Model (e.g., 2007 Kia Picanto):</label>
            <input type="text" name="car-make-model" id="car-make-model" required className={styles.input} />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="car-year">Year (Optional):</label>
            <input type="text" name="car-year" id="car-year" className={styles.input} />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="user-email">Your Email (Optional - for follow-up questions):</label>
            <input type="email" name="user-email" id="user-email" className={styles.input} />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="bad-points">The "Bad Points" (Tell us everything that's wrong with it!):</label>
            <textarea name="bad-points" id="bad-points" rows="8" required className={styles.textarea}></textarea>
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="car-picture">Picture of Your Car (Optional - Max 5MB):</label>
            <input type="file" name="car-picture" id="car-picture" accept="image/*" className={styles.fileInput} />
          </div>

          <button type="submit" className={styles.submitButton}>Send in Your Car for Roasting!</button>
        </form>
      </div>
    </Layout>
  );
}
