import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const downloadsDirectory = path.join(process.cwd(), 'downloads');

export function getSortedDownloadsData() {
  const fileNames = fs.readdirSync(downloadsDirectory);
  const allDownloadsData = fileNames.map((fileName) => {
    const id = fileName.replace(/\.md$/, '');
    const fullPath = path.join(downloadsDirectory, fileName);
    const fileContents = fs.readFileSync(fullPath, 'utf8');
    const matterResult = matter(fileContents);
    return {
      id,
      ...matterResult.data,
    };
  });
  return allDownloadsData.sort((a, b) => {
    if (a.title < b.title) {
      return 1;
    } else {
      return -1;
    }
  });
}