import "../../public/static/css/styles.css";

const SITE_BASE_DOMAIN = String(process.env.NEXT_PUBLIC_SITE_BASE_DOMAIN);
import { SITE_NAME, SITE_DESCRIPTION } from "@/config";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" data-theme={SITE_NAME} className="antialiased">
      <head>
        {/* schema */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "Organization",
              url: `https://www.${SITE_BASE_DOMAIN}/`,
              name: `${SITE_NAME}`,
              description: `${SITE_DESCRIPTION}`,
              foundingDate: "TODO",
              logo: "/static/assets/img/logos/app.png",
              sameAs: ["https://www.linkedin.com/company/TODO"],
            }),
          }}
        />
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
                  name: "Home",
                  item: `https://www.${SITE_BASE_DOMAIN}/`,
                },
              ],
            }),
          }}
        />

        {/* google analytics */}

        {/* google tag manager */}

        {/* icon library */}
        <link
          href="https://cdn.jsdelivr.net/npm/remixicon@4.5.0/fonts/remixicon.css"
          rel="stylesheet"
        />
      </head>
      {children}
    </html>
  );
}
