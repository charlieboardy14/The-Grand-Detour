import Head from 'next/head';
import Layout from '../components/layout';

export default function Contact() {
  return (
    <Layout>
      <Head>
        <title>Contact Us</title>
        <meta name="description" content="Contact The Grand Detour with your questions or feedback about EvoSim and automotive content." />
      </Head>
      <section>
        <h2>Contact Us</h2>
        <p>Have questions or feedback about EvoSim? We'd love to hear from you!</p>
        <form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field">
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
      <style jsx>{`
        form {
          max-width: 600px;
          margin: 2rem auto;
          padding: 2rem;
          border: 1px solid #eee;
          border-radius: 8px;
          background-color: #f9f9f9;
        }
        label {
          display: block;
          margin-bottom: 0.5rem;
          font-weight: bold;
          color: #333;
        }
        input[type="text"],
        input[type="email"],
        textarea {
          width: 100%;
          padding: 10px;
          margin-bottom: 1rem;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 1em;
        }
        textarea {
          resize: vertical;
        }
        button {
          background-color: #0070f3;
          color: white;
          padding: 10px 20px;
          border: none;
          border-radius: 5px;
          cursor: pointer;
          font-size: 1em;
          transition: background-color 0.2s ease-in-out;
        }
        button:hover {
          background-color: #005bb5;
        }
      `}</style>
    </Layout>
  );
}