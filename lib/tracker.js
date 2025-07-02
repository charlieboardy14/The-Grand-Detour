export function trackPageView(path) {
  if (typeof window !== 'undefined') {
    const pageViews = JSON.parse(localStorage.getItem('pageViews') || '{}');
    pageViews[path] = (pageViews[path] || 0) + 1;
    localStorage.setItem('pageViews', JSON.stringify(pageViews));

    // For total views
    let totalViews = parseInt(localStorage.getItem('totalViews') || '0', 10);
    totalViews += 1;
    localStorage.setItem('totalViews', totalViews.toString());

    console.log(`Page view tracked (localStorage): ${path}, Total: ${totalViews}`);
  }
}