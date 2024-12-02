import { Metadata, Viewport } from "next";

import "../../public/static/css/styles.css";

import { SITE_NAME, SITE_TAGLINE, SITE_DESCRIPTION, SITE_BASE_DOMAIN } from "@/constants";

import ProgressBarProvider from "@/providers/progressbarprovider";

export const metadata: Metadata = {
  title: {
    template: `%s • ${SITE_NAME}`,
    default: `${SITE_NAME} • ${SITE_TAGLINE}`,
  },
  description: SITE_DESCRIPTION,
  applicationName: SITE_NAME,
  referrer: "origin-when-cross-origin",
  keywords: ["TODO"],
  authors: [{ name: `${SITE_NAME}` }],
  creator: `${SITE_NAME}`,
  publisher: `${SITE_NAME}`,
  metadataBase: new URL(SITE_BASE_DOMAIN),
  robots: {
    index: true,
    follow: true,
    nocache: true,
    googleBot: {
      index: true,
      follow: true,
    }
  },
  icons: {
    icon: "/static/assets/img/favicon.png",
    shortcut: "/static/assets/img/favicon.png",
    apple: "/static/assets/img/apple_touch_icon.png",
  },
  appleWebApp: {
    title: SITE_NAME,
    statusBarStyle: "default",
  },
  manifest: `${SITE_BASE_DOMAIN}/manifest.json`,
  twitter: {
    card: "summary_large_image",
    title: `${SITE_NAME} • ${SITE_TAGLINE}`,
    description: SITE_DESCRIPTION,
    images: {
      url: `${SITE_BASE_DOMAIN}/static/assets/img/social.png`,
    },
  },
};

export const viewport: Viewport = {
  themeColor: "#FFFFFF",
  width: "device-width",
  height: "device-height",
  initialScale: 1,
  minimumScale: 1,
  maximumScale: 1,
  userScalable: false,
  viewportFit: "cover",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" data-theme={SITE_NAME} className="antialiased">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "WebSite",
              url: SITE_BASE_DOMAIN,
              name: SITE_NAME,
              description: SITE_DESCRIPTION,
              foundingDate: "2024",
              logo: "/public/static/assets/img/logos/logo.png",
              sameAs: ["https://www.linkedin.com/company/TODO"],
            }),
          }}
        />
        <link
          href="https://cdn.jsdelivr.net/npm/remixicon@4.5.0/fonts/remixicon.css"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-[100dvh]">
        <ProgressBarProvider>
          {children}
        </ProgressBarProvider>
      </body>
    </html>
  );
}
