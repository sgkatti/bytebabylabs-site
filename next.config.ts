import type { NextConfig } from 'next';

const repoName = 'bytebabylabs-site';
const isGitHubActions = process.env.GITHUB_ACTIONS === 'true';
const basePath = isGitHubActions ? `/${repoName}` : '';
const assetPrefix = isGitHubActions ? `${basePath}/` : '';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: 'export',
  trailingSlash: true,
  skipTrailingSlashRedirect: true,
  images: {
    unoptimized: true,
  },
  basePath,
  assetPrefix,
};

export default nextConfig;
