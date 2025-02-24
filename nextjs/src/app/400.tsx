import { Metadata, Viewport } from "next";

import { SITE_NAME, SITE_DESCRIPTION, SITE_BASE_DOMAIN } from "@/constants";

import ErrorPage from "@/layouts/errorpage";

const statusCode = "400";
const statusDescription = "That was a bad request!";

export const metadata: Metadata = {
  title: statusCode,
  openGraph: {
    title: `${statusCode} • ${SITE_NAME}`,
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

export const viewport: Viewport = {
  themeColor: "#000000",
};

export default function BadRequest() {
  return (
    <ErrorPage statusCode={statusCode} statusDescription={statusDescription} />
  );
}
