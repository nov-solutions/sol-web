import { MetadataRoute } from "next";

import { SITE_BASE_DOMAIN, PAGES } from "@/constants";

export default function Sitemap(): MetadataRoute.Sitemap {
  const sitemap = PAGES.map((page) => ({
    url:
      page.relativePath == "/"
        ? SITE_BASE_DOMAIN
        : `${SITE_BASE_DOMAIN}${page.relativePath}`,
    lastModified: new Date(),
    changeFrequency: "monthly" as "monthly",
    priority: page.relativePath == "/" ? 1 : 0.8,
  }));

  return sitemap;
}
