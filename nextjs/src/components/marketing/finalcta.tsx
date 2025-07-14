import { Button } from "@/components/ui/button";
import Image from "next/image";
import Link from "next/link";

export default function FinalCTA() {
  return (
    <div className="px-4 py-24 bg-background lg:px-0">
      <div className="grid items-center gap-8 p-8 mx-auto lg:grid-cols-2 lg:w-2/3">
        <div className="flex flex-col items-center space-y-4 text-center lg:items-start lg:text-left">
          <h2 className="text-foreground">TODO</h2>
          <p className="text-muted-foreground">TODO</p>
          <Button asChild>
            <Link href="TODO">TODO</Link>
          </Button>
        </div>
        <Image
          src="/assets/img/logos/wordmark.png"
          alt="TODO"
          className="mx-auto rounded-lg"
          width={550}
          height={550}
        />
      </div>
    </div>
  );
}
