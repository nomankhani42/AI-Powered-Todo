import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  basePath: "/AI-Powered-Todo",
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  typescript: {
    // Allows production builds to complete even with type errors
    ignoreBuildErrors: true,
  },
  eslint: {
    // Allows production builds to complete even with ESLint errors
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;