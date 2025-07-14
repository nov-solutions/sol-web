import { Button } from "@/components/ui/button";
import { SITE_NAME } from "@/constants";
import Image from "next/image";
import Link from "next/link";

export default function Splash() {
  return (
    <div className="px-4 pb-24 bg-background pt-36 lg:pt-48 lg:px-0">
      <div className="grid items-center gap-16 mx-auto lg:grid-cols-2 lg:w-2/3">
        <div className="flex flex-col items-center space-y-4 text-center lg:items-start lg:text-left">
          <Image
            src="/assets/img/logos/logo.png"
            alt={SITE_NAME + " logo"}
            className="w-1/6 lg:w-1/12"
            width={100}
            height={100}
          />
          <h1 className="mt-2!">TODO</h1>
          <h2 className="font-medium lg:text-lg text-gray">TODO</h2>
          <Button asChild>
            <Link href="TODO">TODO</Link>
          </Button>
        </div>
        <Image
          src="/assets/img/logos/wordmark.png"
          alt={SITE_NAME + " wordmark"}
          className="lg:mx-auto"
          width={350}
          height={350}
        />
      </div>
    </div>
  );
}
