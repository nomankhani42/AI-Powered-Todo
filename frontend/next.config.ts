import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Vercel handles image optimization automatically
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "**",
      },
    ],
  },
};

export default nextConfig;
