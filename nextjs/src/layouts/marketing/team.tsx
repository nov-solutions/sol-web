import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card";
import { RiLinkedinFill } from "@remixicon/react";
import Image from "next/image";
import Link from "next/link";

export default function Team() {
  const team = [
    {
      headshotLoc: "TODO",
      name: "TODO",
      role: "TODO",
      linkedInLoc: "https://www.linkedin.com/in/TODO/",
    },
  ];

  return (
    <div className="px-4 py-12 grow bg-background lg:px-0">
      <div className="grid items-stretch gap-4 mx-auto lg:grid-cols-4 lg:w-2/3">
        {team.map((teammate, i) => (
          <Card key={i} className="">
            <CardHeader className="flex flex-col items-center justify-center w-full">
              <Image
                src={`/assets/img/headshots/${teammate.headshotLoc}`}
                alt={`${teammate.name}'s headshot`}
                className="w-1/3 mx-auto border rounded-full filter grayscale border-muted-foreground"
                width={150}
                height={150}
              />
            </CardHeader>
            <CardContent className="flex flex-col items-center justify-center w-full">
              <h4 className="text-sm font-medium">{teammate.name}</h4>
              <p className="text-xs text-muted-foreground">{teammate.role}</p>
            </CardContent>
            <CardFooter className="flex justify-center w-full">
              <Button variant="link" asChild>
                <Link
                  href={teammate.linkedInLoc}
                  target="_blank"
                  className="mt-4"
                >
                  <RiLinkedinFill className="h-5" />
                </Link>
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
}
