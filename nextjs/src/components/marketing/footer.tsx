import { PAGES, SITE_NAME } from "@/constants";

import Image from "next/image";
import Link from "next/link";

export default function Footer() {
  const socials = [
    {
      name: "LinkedIn",
      icon: "ri-linkedin-fill",
      loc: "https://www.linkedin.com/company/TODO",
    },
  ];
  const pages = PAGES.filter(
    ({ relativePath }) =>
      relativePath !== "/" && !relativePath.startsWith("/app"),
  ).map(({ name, relativePath }) => ({ name, relativePath }));

  return (
    <footer className="w-full">
      <div className="flex flex-col justify-center px-4 py-12 mx-auto space-y-8 lg:px-0 lg:w-2/3">
        <div className="flex flex-col w-full space-y-8 text-sm lg:space-y-0 lg:justify-between lg:flex-row">
          <div className="flex flex-col space-y-4">
            <Link href="/">
              <Image
                src="/assets/img/logos/wordmark.png"
                alt={SITE_NAME + " wordmark"}
                className="h-5 my-auto"
                width={60}
                height={60}
              />
            </Link>
            <p>TODO</p>
            <div className="flex items-center space-x-2">
              {socials.map((social) => (
                <Link
                  key={social.name}
                  href={social.loc}
                  target="_blank"
                  className="text-muted-foreground lg:text-opacity-75 hover:text-opacity-100"
                >
                  <i className={`text-lg ${social.icon}`}></i>
                </Link>
              ))}
            </div>
          </div>
          <div className="flex space-x-4">
            {pages.map((page, i) => (
              <Link
                key={i}
                href={page.relativePath}
                className="font-semibold lg:text-black/75 hover:text-black"
              >
                {page.name}
              </Link>
            ))}
          </div>
        </div>
        <div className="self-end text-xs text-muted-foreground">
          <p>
            © {new Date().getFullYear()} {SITE_NAME}
          </p>
        </div>
      </div>
    </footer>
  );
}
