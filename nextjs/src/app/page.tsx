import Footer from "@/components/marketing/footer";
import FullHeightSplash from "@/components/marketing/fullheightsplash";
import Nav from "@/components/marketing/nav";
import {
  SITE_BASE_DOMAIN,
  SITE_DESCRIPTION,
  SITE_NAME,
  SITE_TAGLINE,
} from "@/constants";
import { Metadata } from "next";

export const metadata: Metadata = {
  openGraph: {
    title: `${SITE_NAME} • ${SITE_TAGLINE}`,
    description: SITE_DESCRIPTION,
    url: SITE_BASE_DOMAIN,
    siteName: SITE_NAME,
    images: [
      {
        url: `${SITE_BASE_DOMAIN}/assets/img/social.png`,
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
