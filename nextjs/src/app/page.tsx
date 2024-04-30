import { Metadata, Viewport } from "next";

import RootLayout from "./layout";
import Body from "@/layouts/body";
import Nav from "@/layouts/nav";
import FullHeightSplash from "@/layouts/fullheightsplash";
import Footer from "@/layouts/footer";

const SITE_BASE_DOMAIN = String(process.env.SITE_BASE_DOMAIN);
const SITE_NAME = String(process.env.SITE_NAME).replace(/\b\w/g, (char) => char.toUpperCase());
const SITE_TAGLINE = String(process.env.SITE_TAGLINE);
const SITE_DESCRIPTION = String(process.env.SITE_DESCRIPTION);

const bodyBG = "TODO";
const navBG = "TODO";
const navLogoFileName = "TODO";
const pages = ["TODO"];
const pagesLocs = ["TODO"];
const navPagesColor = "TODO";
const cta = "TODO";
const ctaLoc = "TODO";
const mobileDrawerToggleColor = "TODO";
const splashBG = "TODO";
const splashLogoFileName = "TODO";
const splashTitleColor = "TODO";
const splashTitle = "TODO";
const splashSubtitleColor = "TODO";
const splashSubtitle = "TODO";
const splashImageFileName = "TODO";
const splashImageAlt = "TODO";
const footerDividerColor = "TODO";
const footerLogoFileName = "TODO";
const footerPagesColor = "TODO";
const footerTaglineColor = "TODO";
const footerTagline = SITE_TAGLINE.charAt(0).toUpperCase() + SITE_TAGLINE.slice(1).toLowerCase();
const footerFinePrintColor = "TODO";
const socialsLocs = ["https://www.linkedin.com/company/TODO/"];
const socialsColor = "TODO";
const socialsIcons = ["bi-linkedin"];

const title = SITE_NAME + " • " + SITE_TAGLINE;
const currentYear = new Date().getFullYear();
const pageRelativePath = "/";
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
  metadataBase: new URL("https://" + SITE_BASE_DOMAIN),
  alternates: {
    canonical: "https://" + SITE_BASE_DOMAIN + pageRelativePath,
  },
  openGraph: {
    title: title,
    siteName: SITE_NAME + " • " + SITE_TAGLINE,
    description: SITE_DESCRIPTION,
    url: "https://" + SITE_BASE_DOMAIN + pageRelativePath,
    images: [
      {
        url: "https://" + SITE_BASE_DOMAIN + "/static/assets/img/logos/TODO"
      },
    ],
    type: "website",
  },
  twitter: {
    card: "summary",
    title: title,
    description: SITE_DESCRIPTION,
    images: [
      {
        url: "https://" + SITE_BASE_DOMAIN + "/static/assets/img/logos/TODO"
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
  themeColor: "TODO",
};

export default function Home() {
  return (
    <RootLayout>
      <Body bodyBG={bodyBG}>
        <Nav
          navBG={navBG}
          navLogoFileName={navLogoFileName}
          SITE_NAME={SITE_NAME}
          pages={pages}
          pagesLocs={pagesLocs}
          navPagesColor={navPagesColor}
          cta={cta}
          ctaLoc={ctaLoc}
          mobileDrawerToggleColor={mobileDrawerToggleColor}
        />
        <FullHeightSplash
          splashBG={splashBG}
          splashLogoFileName={splashLogoFileName}
          SITE_NAME={SITE_NAME}
          splashTitleColor={splashTitleColor}
          splashTitle={splashTitle}
          splashSubtitleColor={splashSubtitleColor}
          splashSubtitle={splashSubtitle}
          splashImageFileName={splashImageFileName}
          splashImageAlt={splashImageAlt}
        />
        <Footer
          footerDividerColor={footerDividerColor}
          footerLogoFileName={footerLogoFileName}
          SITE_NAME={SITE_NAME}
          pages={pages}
          pagesLocs={pagesLocs}
          footerPagesColor={footerPagesColor}
          footerTaglineColor={footerTaglineColor}
          footerTagline={footerTagline}
          socialsLocs={socialsLocs}
          socialsColor={socialsColor}
          socialsIcons={socialsIcons}
          footerFinePrintColor={footerFinePrintColor}
        />
      </Body>
    </RootLayout>
  );
}
