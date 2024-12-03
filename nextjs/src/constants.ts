export const SITE_NAME = String(process.env.NEXT_PUBLIC_SITE_NAME).replace(
  /\b\w/g,
  (char) => char.toUpperCase(),
);
// TODO: replace with the project's tagline
export const SITE_TAGLINE = "All-in-one web app template";
// TODO: replace with the project's description
export const SITE_DESCRIPTION =
  "Sol is an all-in-one template that enables developers to create robust, reliable and responsive web apps in minutes.";
export const SITE_BASE_DOMAIN = String(
  process.env.NEXT_PUBLIC_SITE_BASE_DOMAIN,
);

export interface Page {
  name: string;
  relativePath: string;
  appPage?: boolean;
  icon?: string;
  external?: boolean;
}
export const PAGES: Page[] = [{ name: "Home", relativePath: "/" }];
