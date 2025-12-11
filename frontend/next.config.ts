import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  basePath: "/AI-Powered-Todo",
  // Disable dynamic features for static export
  dynamicParams: false,
  // Use trailing slash for GitHub Pages compatibility
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
