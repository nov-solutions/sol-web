import { Metadata, Viewport } from "next";

import RootLayout from "./layout";
import ErrorPage from "@/layouts/errorpage";
import Body from "@/layouts/body";

const SITE_BASE_DOMAIN = String(process.env.NEXT_PUBLIC_SITE_BASE_DOMAIN);
const SITE_NAME = String(process.env.NEXT_PUBLIC_SITE_NAME).replace(/\b\w/g, (char) =>
  char.toUpperCase(),
);
const SITE_TAGLINE = String(process.env.NEXT_PUBLIC_SITE_TAGLINE);
const SITE_DESCRIPTION = String(process.env.NEXT_PUBLIC_SITE_DESCRIPTION);

const statusCode = "400";
const statusDescription = "That was a bad request!";

const title = statusCode + " • " + SITE_NAME;
const currentYear = new Date().getFullYear();
const pageRelativePath = "/400";
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
        url: SITE_BASE_DOMAIN + "/static/assets/img/logos/TODO"
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
        url: SITE_BASE_DOMAIN + "/static/assets/img/logos/TODO"
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

export default function BadRequest() {
  return (
    <RootLayout>
      <Body bodyBG={"bg-black"}>
        <ErrorPage
          statusCode={statusCode}
          statusDescription={statusDescription}
        />
      </Body>
    </RootLayout>
  );
}
