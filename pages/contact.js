import Head from 'next/head';
import Layout from '../components/layout';
import styles from '../styles/contact.module.css';

export default function Contact() {
  return (
    <Layout>
      <Head>
        <title>Get in Touch</title>
      </Head>
      <section className={styles.contactSection}>
        <h2 className={styles.contactHeading}>We'd Love to Hear From You</h2>
        <p className={styles.contactDescription}>Whether you have a question, feedback, or just want to say hello, feel free to reach out. We're always happy to connect with our readers.</p>
        <form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field" className={styles.form}>
          <input type="hidden" name="form-name" value="contact" />
          <p style={{ display: 'none' }}>
            <label>Don’t fill this out if you’re human: <input name="bot-field" /></label>
          </p>
          <p>
            <label htmlFor="name">Name:</label>
            <input type="text" id="name" name="name" required />
          </p>
          <p>
            <label htmlFor="email">Email:</label>
            <input type="email" id="email" name="email" required />
          </p>
          <p>
            <label htmlFor="message">Message:</label>
            <textarea id="message" name="message" rows="5" required></textarea>
          </p>
          <p>
            <button type="submit">Send Message</button>
          </p>
        </form>
      </section>
    </Layout>
  );
}
