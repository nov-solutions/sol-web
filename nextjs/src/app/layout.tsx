import "../../public/static/css/styles.css";

const SITE_BASE_DOMAIN = process.env.SITE_BASE_DOMAIN
const SITE_NAME = String(process.env.SITE_NAME).replace(/\b\w/g, (char) => char.toUpperCase());
const SITE_DESCRIPTION = process.env.SITE_DESCRIPTION

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" data-theme={ SITE_NAME }>
      <head>
        {/* schema */}
        <script type="application/ld+json" dangerouslySetInnerHTML={{
        __html: JSON.stringify({
          "@context": "https://schema.org",
          "@type": "Organization",
          "url": `https://www.${SITE_BASE_DOMAIN}/`,
          "name": `${SITE_NAME}`,
          "description": `${SITE_DESCRIPTION}`,
          "foundingDate": "TODO",
          "logo": "/public/static/assets/img/logos/TODO",
          "sameAs": ["https://www.linkedin.com/company/TODO"]
          })
        }}/>
        <script type="application/ld+json" dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
              {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": `https://www.${SITE_BASE_DOMAIN}/`
              }
            ]
          })
        }}/>

        {/* google analytics */}

        {/* google tag manager */}

        {/* icon libraries */}
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet" />
        {/* htmx */}
        <script src="https://unpkg.com/htmx.org@1.9.8"></script>
      </head>
      {children}
    </html>
  );
}
