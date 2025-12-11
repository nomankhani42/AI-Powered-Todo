import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  // Disable dynamic features for static export
  dynamicParams: false,
};

export default nextConfig;
