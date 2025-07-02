import Head from 'next/head';
import Layout from '../../components/layout';
import { getAllPostIds, getPostData } from '../../lib/posts';
import Date from '../../components/date';

export async function getStaticProps({ params }) {
  const postData = await getPostData(params.id);
  return {
    props: {
      postData,
    },
  };
}

export async function getStaticPaths() {
  const paths = getAllPostIds();
  return {
    paths,
    fallback: false,
  };
}

export default function Post({ postData }) {
  return (
    <Layout>
        <Head>
            <title>{postData.title}</title>
            <meta name="description" content={postData.description || postData.contentHtml.replace(/<[^>]*>?/gm, '').substring(0, 160)} />
        </Head>
        <article>
            <h1 className={Layout.postTitle}>{postData.title}</h1>
            <div className={Layout.lightText}>
                <Date dateString={postData.date} />
            </div>
            <div dangerouslySetInnerHTML={{ __html: postData.contentHtml }} />
        </article>
        <div style={{ marginTop: '3rem' }}>
          <h2>Comments</h2>
          <UtterancesRepo />
        </div>
    </Layout>
  );
}

function UtterancesRepo() {
  // Replace with your actual GitHub repo for comments
  const repo = 'charlieboardy14/EVOsimBlog-comments'; // IMPORTANT: CHANGE THIS TO YOUR COMMENTS REPO

  return (
    <section
      ref={(elem) => {
        if (!elem) return;
        const scriptElem = document.createElement('script');
        scriptElem.src = 'https://utteranc.es/client.js';
        scriptElem.async = true;
        scriptElem.setAttribute('repo', repo);
        scriptElem.setAttribute('issue-term', 'pathname');
        scriptElem.setAttribute('label', 'comment');
        scriptElem.setAttribute('theme', 'github-light');
        scriptElem.setAttribute('crossorigin', 'anonymous');
        elem.appendChild(scriptElem);
      }}
    />
  );
}