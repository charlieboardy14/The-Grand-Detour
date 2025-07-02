import Head from 'next/head';
import Script from 'next/script';
import '../styles/globals.css'; // Assuming you have a globals.css file

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        {/* Google Analytics */}
        <Script strategy="beforeInteractive" src="https://www.googletagmanager.com/gtag/js?id=G-EMZVLSXEFN" />
        <Script id="google-analytics" strategy="beforeInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-EMZVLSXEFN', { 'branch': process.env.NEXT_PUBLIC_BRANCH });
          `}
        </Script>
      </Head>
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;
