import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { SITE_NAME } from "@/constants";
import Image from "next/image";
import Link from "next/link";

export default function ErrorPage({
  statusCode,
  statusDescription,
}: {
  statusCode: string;
  statusDescription: string;
}) {
  return (
    <div className="flex flex-col items-center justify-center h-screen px-4 lg:px-0 bg-background">
      <div className="flex flex-col items-center space-y-4 lg:w-1/5">
        <Image
          className="w-10 aspect-square"
          src="/assets/img/logos/logo.png"
          alt={SITE_NAME + " logo"}
          width={100}
          height={100}
        />

        <div className="mt-2! flex items-center space-x-4">
          <h2 className="text-foreground">{statusCode}</h2>
          <Separator orientation="vertical" />
          <h4 className="text-foreground">{statusDescription}</h4>
        </div>

        <Button asChild>
          <Link href="/" className="text-sm btn btn-sm btn-primary">
            Home
          </Link>
        </Button>
      </div>
    </div>
  );
}
