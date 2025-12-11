import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  basePath: "/AI-Powered-Todo",
  trailingSlash: true,
  dynamicParams: false,
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
