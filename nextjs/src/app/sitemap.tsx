import { MetadataRoute } from "next";

const SITE_BASE_DOMAIN = String(process.env.NEXT_PUBLIC_SITE_BASE_DOMAIN);

export default function Sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: SITE_BASE_DOMAIN,
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 1,
    },
  ];
}
