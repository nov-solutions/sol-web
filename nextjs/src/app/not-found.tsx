import { Metadata, Viewport } from "next";

import RootLayout from "./layout";
import ErrorPageContainer from "@/layouts/errorpagecontainer";
import ErrorPage from "@/layouts/errorpage";
import Body from "@/layouts/body";

const SITE_BASE_DOMAIN = String(process.env.NEXT_PUBLIC_SITE_BASE_DOMAIN);
import { SITE_NAME, SITE_TAGLINE, SITE_DESCRIPTION } from "@/config";

const statusCode = "404";
const statusDescription = "We can't find that page!";

const title = statusCode + " • " + SITE_NAME;
const currentYear = new Date().getFullYear();
const pageRelativePath = "/404";
export const metadata: Metadata = {
  title: title,
  description: SITE_DESCRIPTION,
  authors: [{ name: "© " + SITE_NAME + " " + currentYear }],
  icons: {
    icon: "/static/assets/img/favicon.png",
    apple: "/static/assets/img/apple_touch_icon.png",
  },
  applicationName: SITE_NAME,
  appleWebApp: {
    title: SITE_NAME,
    statusBarStyle: "default",
  },
  metadataBase: new URL(SITE_BASE_DOMAIN),
  alternates: {
    canonical: SITE_BASE_DOMAIN + pageRelativePath,
  },
  openGraph: {
    title: title,
    siteName: SITE_NAME + " • " + SITE_TAGLINE,
    description: SITE_DESCRIPTION,
    url: SITE_BASE_DOMAIN + pageRelativePath,
    images: [
      {
        url: SITE_BASE_DOMAIN + "/static/assets/img/social.png",
      },
    ],
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: title,
    description: SITE_DESCRIPTION,
    images: [
      {
        url: SITE_BASE_DOMAIN + "/static/assets/img/social.png",
      },
    ],
  },
  robots: {
    follow: true,
    index: true,
  },
};

export const viewport: Viewport = {
  width: "device-width",
  height: "device-height",
  initialScale: 1,
  minimumScale: 1,
  maximumScale: 1,
  userScalable: false,
  viewportFit: "cover",
  themeColor: "#000000",
};

export default function NotFound() {
  return (
    <RootLayout>
      <Body bodyBG={"bg-black"}>
        <ErrorPageContainer>
          <ErrorPage
            statusCode={statusCode}
            statusDescription={statusDescription}
          />
        </ErrorPageContainer>
      </Body>
    </RootLayout>
  );
}
