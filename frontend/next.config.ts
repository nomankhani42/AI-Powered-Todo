import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  basePath: '/AI-Powered-Todo',
  output: "export",
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  typescript: {
    // Allows production builds to complete even with type errors
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
