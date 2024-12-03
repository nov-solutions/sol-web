import { Metadata } from "next";

import {
  SITE_NAME,
  SITE_TAGLINE,
  SITE_DESCRIPTION,
  SITE_BASE_DOMAIN,
} from "@/constants";

import Nav from "@/components/marketing/nav";
import FullHeightSplash from "@/components/marketing/fullheightsplash";
import Footer from "@/components/marketing/footer";

export const metadata: Metadata = {
  openGraph: {
    title: `${SITE_NAME} • ${SITE_TAGLINE}`,
    description: SITE_DESCRIPTION,
    url: SITE_BASE_DOMAIN,
    siteName: SITE_NAME,
    images: [
      {
        url: `${SITE_BASE_DOMAIN}/static/assets/img/social.png`,
        width: 1200,
        height: 630,
      },
    ],
    locale: "en_US",
    type: "website",
  },
  alternates: {
    canonical: SITE_BASE_DOMAIN,
  },
};

export default function Home() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            itemListElement: [
              {
                "@type": "ListItem",
                position: 1,
                name: SITE_NAME,
                item: SITE_BASE_DOMAIN,
              },
            ],
          }),
        }}
      />
      <Nav />
      <FullHeightSplash />
      <Footer />
    </>
  );
}
