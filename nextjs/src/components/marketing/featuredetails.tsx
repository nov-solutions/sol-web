import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { RiHome2Line } from "@remixicon/react";

export default function FeatureDetails() {
  return (
    <div className="px-4 py-24 lg:px-0 bg-background">
      <div className="flex flex-col mx-auto space-y-10 lg:w-2/3">
        <div className="flex flex-col space-y-2 text-left lg:text-center lg:items-center">
          <p className="text-muted-foreground">TODO</p>
          <h2>TODO</h2>
        </div>
        <div className="grid gap-8 text-left lg:grid-cols-3">
          <Card className="w-full">
            <CardHeader>
              <CardTitle>
                <div className="flex items-center">
                  <RiHome2Line className="mr-2 TODO" />
                  TODO
                </div>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p>TODO Sample text</p>
              <p>TODO Sample text</p>
              <p>TODO Sample text</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>
                <div className="flex items-center">
                  <RiHome2Line className="mr-2 TODO" />
                  TODO
                </div>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p>TODO Sample text</p>
              <p>TODO Sample text</p>
              <p>TODO Sample text</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>
                <div className="flex items-center">
                  <RiHome2Line className="mr-2 TODO" />
                  TODO
                </div>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p>TODO Sample text</p>
              <p>TODO Sample text</p>
              <p>TODO Sample text</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
