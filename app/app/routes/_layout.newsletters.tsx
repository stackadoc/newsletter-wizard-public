import type { Route } from "./+types/_layout.newsletters.tsx";
import {getAllNewsletters} from "~/actions/newsletters-actions";
import type {NewsletterWithConfigSelect} from "~/lib/types/newsletter-types";
import {Link} from "react-router";
import {Card, CardHeader, CardTitle} from "~/components/ui/card";
import {AspectRatio} from "@radix-ui/react-aspect-ratio";
import BackButton from "~/components/back-button";

type ServerData = {
    groupedNewsletters: GroupedNewsletter[];
}

interface NewsletterMinimal {
    id: number;
    publishedAt: Date;
    slug: string;
    title: string;
    imageUrl: string;
}

interface GroupedNewsletter {
    id: number;
    name: string;
    imageUrl: string;
    newsletters: NewsletterMinimal[];
}

function groupNewsletters(data: NewsletterWithConfigSelect[]): GroupedNewsletter[] {
    const groupedData: Record<number, GroupedNewsletter> = {};

    data.forEach((newsletter: NewsletterWithConfigSelect) => {
        const configId = newsletter.newsletterConfig.id;

        if (!groupedData[configId]) {
            groupedData[configId] = {
                id: configId,
                name: newsletter.newsletterConfig.name,
                imageUrl: newsletter.newsletterConfig.imageUrl,
                newsletters: []
            };
        }

        groupedData[configId].newsletters.push({
            id: newsletter.id,
            publishedAt: newsletter.publishedAt,
            slug: newsletter.slug,
            title: newsletter.title,
            imageUrl: newsletter.imageUrl
        });
    });

    // Optional: Sort newsletters within each group by publishedAt date (descending)
    Object.values(groupedData).forEach((group: GroupedNewsletter) => {
        group.newsletters.sort((a: NewsletterMinimal, b: NewsletterMinimal) => new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime());
    });

    return Object.values(groupedData);
}

export async function loader({ params }: Route.LoaderArgs) {
    const newslettersFull = await getAllNewsletters();

    const groupedNewsletters = groupNewsletters(newslettersFull);

    const data = { groupedNewsletters } as ServerData;

    return data;
}

export default function Newsletters({
   loaderData,
}: Route.ComponentProps) {
    const { groupedNewsletters } = loaderData;

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="mb-4">
                <BackButton />
            </div>

            {groupedNewsletters.map((group) => (
                <section key={group.id} className="mb-12">
                    <div className="flex items-center gap-4 mb-6 border-b pb-4">
                        {group.imageUrl && (
                            <img
                                src={group.imageUrl}
                                alt={`${group.name} logo`}
                                className="w-12 h-12 rounded-md object-cover" // Added rounded corners and object-cover
                            />
                        )}
                        <h2 className="text-3xl font-bold tracking-tight text-foreground">
                            {group.name}
                        </h2>
                    </div>

                    {group.newsletters.length > 0 ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {group.newsletters.map((newsletter) => {
                                const formattedDate = new Date(newsletter.publishedAt).toISOString().split("T")[0]

                                return (
                                    // Wrap Card with Link for navigation
                                    <Link
                                        key={newsletter.id}
                                        to={`/newsletter/${newsletter.slug}`} // Adjust path as needed
                                        className="group block" // Use group for hover effects if desired
                                    >
                                        <Card className="overflow-hidden h-full transition-shadow duration-200 hover:shadow-lg border bg-card text-card-foreground flex flex-col">
                                            {newsletter.imageUrl && (
                                                <AspectRatio ratio={16 / 9} className="bg-muted border-b">
                                                    <img
                                                        src={newsletter.imageUrl}
                                                        alt={`Image for ${newsletter.title}`}
                                                        className="object-cover w-full h-full transition-transform duration-300 group-hover:scale-105" // Subtle zoom on hover
                                                    />
                                                </AspectRatio>
                                            )}
                                            <CardHeader className="p-4 flex-grow">
                                                <CardTitle className="text-lg font-semibold leading-tight mb-1 group-hover:text-primary transition-colors duration-200"> {/* Title changes color on hover */}
                                                    {newsletter.title}
                                                </CardTitle>
                                                <p className="text-xs text-muted-foreground">
                                                    Published on {formattedDate}
                                                </p>
                                            </CardHeader>
                                        </Card>
                                    </Link>
                                );
                            })}
                        </div>
                    ) : (
                        <p className="text-muted-foreground">No newsletters found for {group.name}.</p>
                    )}
                </section>
            ))}
        </div>
    );

}