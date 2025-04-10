import type { Route } from "./+types/_layout._index.tsx";

import {Button} from "~/components/ui/button";
import {BrainCircuit, Rocket, Rss, Send} from "lucide-react";
import {Card, CardContent, CardHeader, CardTitle} from "~/components/ui/card";
import React from "react";
import {Link} from "react-router";
import {getAllNewsletters} from "~/actions/newsletters-actions";
import NewsletterCard from "~/components/newsletter-card";

export function meta() {
  return [
    { title: "Newsletter Wizard" },
    { name: "description", content: "Welcome to Newsletter Wizard!" },
  ];
}

export async function loader({ params }: Route.LoaderArgs) {
  const newsletters = await getAllNewsletters();

  const lastNewsletters = newsletters
      .sort((a, b) => new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime())
      .map((newsletter) => ({
        id: newsletter.id,
        publishedAt: newsletter.publishedAt,
        slug: newsletter.slug,
        title: newsletter.title,
        imageUrl: newsletter.imagesData.small,
        newsletterConfigName: newsletter.newsletterConfig.name,
      }))
      .slice(0, 5);

  const data = { newsletters: lastNewsletters };

  return data;
}

export default function _layout_index({
  loaderData,
}: Route.ComponentProps) {
  const { newsletters } = loaderData;

  return (
      <div className="flex flex-col">
        <main className="flex-1">
          {/* Hero Section */}
          <section className="w-full my-12 md:my-36">
            <div className="container px-4 md:px-6 mx-auto">
              <div className="flex flex-col items-center space-y-4 text-center">
                <div className="space-y-2">
                  <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none animate-in fade-in slide-in-from-bottom duration-700">
                    Your AI-Powered Tech Digest
                  </h1>
                  <p className="mx-auto max-w-[700px] text-neutral-700 dark:invert md:text-xl animate-in fade-in slide-in-from-bottom duration-700 delay-150">
                    Keeping up is impossible. Our AI monitors countless posts across Reddit, Discord, HackerNews, Telegram, Twitter & more, distilling the crucial info you'd otherwise miss.
                  </p>
                </div>
                <div className="space-x-4 animate-in fade-in slide-in-from-bottom duration-700 delay-300">

                  <Link to="/newsletters">
                    <Button variant="outline" effect="expandIcon" icon={Rss} iconPlacement="right">
                      Read Last News
                    </Button>
                  </Link>

                  <Button effect="expandIcon" icon={Send} iconPlacement="right">
                    Subscribe
                  </Button>
                </div>
              </div>
            </div>
          </section>

          {/* Newsletter Carousel section */}
          <section className="w-full my-12 md:my-36">
            <h2 className="text-3xl font-bold tracking-tighter text-center sm:text-4xl md:text-5xl mb-12">
              Last News
            </h2>
            <div className="flex flex-wrap justify-center gap-6 container px-4 md:px-6 mx-auto">
              {newsletters.map((newsletter) => (
                  <div
                      key={newsletter.id}
                      className="w-full sm:w-[45%] md:w-[30%] lg:w-[22%] xl:w-[18%] flex flex-col"
                  >
                    <NewsletterCard
                        publishedAt={newsletter.publishedAt}
                        slug={newsletter.slug}
                        imageUrl={newsletter.imageUrl}
                        title={newsletter.title}
                        newsletterConfigName={newsletter.newsletterConfigName}
                    />
                  </div>
              ))}
            </div>
          </section>

          {/* Use Cases Section */}
          <section className="w-full my-12 md:my-36">
            <div className="container px-4 md:px-6 mx-auto">
              <h2 className="text-3xl font-bold tracking-tighter text-center sm:text-4xl md:text-5xl mb-12">
                How It Works
              </h2>
              <div className="grid gap-6 md:grid-cols-3 lg:gap-12">
                <Card className="transform transition-transform duration-300 hover:scale-105 hover:shadow-lg bg-white dark:bg-black border dark:border-neutral-700">
                  <CardHeader className="flex flex-col items-center text-center">
                    <Rss className="w-12 h-12 mb-4" />
                    <CardTitle>Beyond Manual Reach</CardTitle>
                  </CardHeader>
                  <CardContent className="text-center text-neutral-700 dark:invert">
                    <p>We monitor an overwhelming number of public and private tech channels daily – a scale impossible for manual tracking.</p>
                  </CardContent>
                </Card>
                <Card className="transform transition-transform duration-300 hover:scale-105 hover:shadow-lg bg-white dark:bg-black border dark:border-neutral-700">
                  <CardHeader className="flex flex-col items-center text-center">
                    <BrainCircuit className="w-12 h-12 mb-4 " />
                    <CardTitle>Intelligent Distillation</CardTitle>
                  </CardHeader>
                  <CardContent className="text-center text-neutral-700 dark:invert">
                    <p>Advanced AI processes this vast data stream, extracting key signals and summarizing the essential information.</p>
                  </CardContent>
                </Card>
                <Card className="transform transition-transform duration-300 hover:scale-105 hover:shadow-lg bg-white dark:bg-black border dark:border-neutral-700">
                  <CardHeader className="flex flex-col items-center text-center">
                    <Rocket className="w-12 h-12 mb-4 " />
                    <CardTitle>Your Daily Briefing</CardTitle>
                  </CardHeader>
                  <CardContent className="text-center text-neutral-700 dark:invert">
                    <p>Get the synthesized, crucial insights delivered concisely to your inbox, ensuring you never miss out while saving hours.</p>
                  </CardContent>
                </Card>
              </div>
            </div>
          </section>

        </main>
      </div>
  );
}
