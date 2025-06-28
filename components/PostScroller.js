import { useState, useEffect } from 'react';
import Link from 'next/link';
import styles from './PostScroller.module.css';

const PostScroller = ({ posts }) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % posts.length);
    }, 3000); // Change slide every 3 seconds

    return () => clearInterval(interval);
  }, [posts.length]);

  return (
    <div className={styles.scrollerContainer}>
      {posts.length > 0 && (
        <div
          key={posts[currentIndex].id}
          className={`${styles.slide} ${styles.active}`}>
          <img src={posts[currentIndex].image} alt={posts[currentIndex].title} className={styles.image} />
          <div className={styles.caption}>
            <h3>{posts[currentIndex].title}</h3>
            <Link href={`/posts/${posts[currentIndex].id}`}>Read More</Link>
          </div>
        </div>
      )}
    </div>
  );
};

export default PostScroller;