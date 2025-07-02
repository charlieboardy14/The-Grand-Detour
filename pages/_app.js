import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { trackPageView } from '../lib/tracker';
import '../styles/globals.css'; // Assuming you have a globals.css file

function MyApp({ Component, pageProps }) {
  const router = useRouter();

  useEffect(() => {
    const handleRouteChange = (url) => {
      trackPageView(url);
    };

    router.events.on('routeChangeComplete', handleRouteChange);

    // Initial page load tracking
    trackPageView(router.asPath);

    return () => {
      router.events.off('routeChangeComplete', handleRouteChange);
    };
  }, [router.events, router.asPath]);

  return <Component {...pageProps} />;
}

export default MyApp;
