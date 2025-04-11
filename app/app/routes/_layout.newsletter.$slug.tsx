import type { Route } from "./+types/_layout.newsletter.$slug.tsx";
import {
    getFirstNewsletterBeforeDate,
    getNewsletterBySlug,
    incrementReadCount
} from "~/actions/newsletters-actions";
import {addTargetBlankToLinks, markdownToHtml} from "~/lib/utils";
import {Card, CardContent, CardHeader, CardTitle} from "~/components/ui/card";
import {AspectRatio} from "~/components/ui/aspect-ratio";

import styles from "~/styles/newsletter.css?url";
import type {LinksFunction} from "react-router";
import BackButton from "~/components/back-button";
import SubscribeButton from "~/components/subscribe-button";
import NewsletterCard from "~/components/newsletter-card";
import {ReadCountBadge} from "~/components/read-count-badge";

export const links: LinksFunction = () => [
    { rel: "stylesheet", href: styles },
];

export const meta = ({ data }: Route.MetaArgs) => {
    const defaultTitle = "Newsletter Wizard";
    const defaultDescription = "Read last fresh news from Newsletter Wizard.";

    // Use optional chaining to safely access nested properties
    const newsletterTitle = data?.newsletter?.title;
    const title = newsletterTitle ? `${newsletterTitle} | ${defaultTitle}` : defaultTitle;
    const description = newsletterTitle ? `Read the newsletter: ${newsletterTitle}` : defaultDescription;

    return [
        { title: title },
        { name: "description", content: description },
    ];
};


type ServerData = {
    newsletter: {
        publishedAt: Date;
        outputHtml: string;
        title: string;
        imageUrl: string;
        modelName: string;
        nbRead: number;
    };
    previousNewsletter?: {
        publishedAt: Date;
        slug: string;
        imageUrl: string;
        title: string;
        nbRead: number;
    }
}

export async function loader({ params }: Route.LoaderArgs) {
    // Increment read count
    incrementReadCount(params.slug);

    const newsletterFull = await getNewsletterBySlug(params.slug);
    if (!newsletterFull) {
        throw new Response("Not Found", { status: 404 });
    }
    let outputHtml = markdownToHtml(newsletterFull.outputMarkdown);
    // Modify the HTML string to add target="_blank" to links
    outputHtml = addTargetBlankToLinks(outputHtml);

    // Get previousNewsletter
    const previousNewsletter = await getFirstNewsletterBeforeDate(newsletterFull.publishedAt, newsletterFull.newsletterConfigId);

    const data: ServerData = {
        newsletter: {
            publishedAt: newsletterFull.publishedAt,
            outputHtml: outputHtml, // Use the modified HTML
            title: newsletterFull.title,
            imageUrl: newsletterFull.imagesData.medium,
            modelName: newsletterFull.modelName,
            nbRead: newsletterFull.nbRead,
        },
        previousNewsletter: previousNewsletter ? {
            publishedAt: previousNewsletter.publishedAt,
            slug: previousNewsletter.slug,
            imageUrl: previousNewsletter.imagesData.medium,
            title: previousNewsletter.title,
            nbRead: previousNewsletter.nbRead,
        } : undefined,
    };

    return data;
}

export default function Newsletter({
    loaderData,
}: Route.ComponentProps) {
    const { newsletter } = loaderData;

    const formattedDate = new Date(newsletter.publishedAt).toISOString().split("T")[0];

    return (
        <div className="container mx-auto px-4 py-8 max-w-4xl">
            <div className="mb-4">
                <div className="flex justify-between items-center">
                    <BackButton />
                    <SubscribeButton />
                </div>
            </div>

            <Card className="overflow-hidden bg-card text-card-foreground border">
                {newsletter.imageUrl && (
                    <AspectRatio ratio={16 / 9} className="bg-muted border-b">
                        <img
                            src={newsletter.imageUrl}
                            alt={`Image for ${newsletter.title}`}
                            className="object-cover w-full h-full"
                        />
                    </AspectRatio>
                )}
                <div
                    className="flex flex-col md:flex-row items-center justify-between px-6 pt-3 pb-1 gap-6"
                >
                    <span className="block text-xs italic text-muted-foreground text-center md:text-left">
                        AI-generated content and visuals, informed by online data.
                    </span>
                    <ReadCountBadge count={newsletter.nbRead} />
                </div>
                <CardHeader className="p-6">
                    <CardTitle className="text-3xl lg:text-4xl font-bold mb-2">{newsletter.title}</CardTitle>
                    <p className="text-sm text-muted-foreground">
                        Published on {formattedDate}
                    </p>
                </CardHeader>
                <CardContent className="p-6 pt-0">
                    <article
                        className="newsletter-content"
                        dangerouslySetInnerHTML={{ __html: newsletter.outputHtml }}
                    />
                    <hr />
                    <span className="block text-xs italic text-muted-foreground pt-3 pb-1 text-center md:text-left">
                        This newsletter has been generated using the <strong>{newsletter.modelName}</strong> model.
                    </span>
                    {loaderData.previousNewsletter && (
                        <div className="mt-8">
                            <h1 className="text-lg font-semibold text-center mb-4">Read more</h1>
                            <div className="max-w-xs mx-auto">
                                <NewsletterCard
                                    publishedAt={loaderData.previousNewsletter.publishedAt}
                                    slug={loaderData.previousNewsletter.slug}
                                    imageUrl={loaderData.previousNewsletter.imageUrl}
                                    title={loaderData.previousNewsletter.title}
                                    nbRead={loaderData.previousNewsletter.nbRead}
                                />
                            </div>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}