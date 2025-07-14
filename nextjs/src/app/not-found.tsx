import { SITE_BASE_DOMAIN, SITE_DESCRIPTION, SITE_NAME } from "@/constants";
import ErrorPage from "@/layouts/errorpage";
import { Metadata } from "next";

const statusCode = "404";
const statusDescription = "We can't find that page!";

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

export default function NotFound() {
  return (
    <ErrorPage statusCode={statusCode} statusDescription={statusDescription} />
  );
}
