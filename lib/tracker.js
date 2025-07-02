export function trackPageView(path) {
  if (typeof window !== 'undefined') { // Ensure this runs only in the browser
    fetch('/api/track', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        page: path,
        timestamp: new Date().toISOString(),
        // Add more data here as needed, e.g., user ID, referrer
      }),
    }).then(response => {
      if (!response.ok) {
        console.error('Failed to send tracking data', response.statusText);
      }
    }).catch(error => {
      console.error('Error sending tracking data:', error);
    });
  }
}
