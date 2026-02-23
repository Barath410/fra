import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  experimental: {
    turbopack: {
      root: __dirname,
    },
  },
  transpilePackages: ['react-map-gl', 'mapbox-gl'],
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
      },
      {
        protocol: 'https',
        hostname: 'upload.wikimedia.org',
      },
    ],
  },
};

export default nextConfig;
