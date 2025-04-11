import type { Route } from "./+types/_layout.newsletter.$slug.tsx";
import {getNewsletterBySlug} from "~/actions/newsletters-actions";
import {addTargetBlankToLinks, markdownToHtml} from "~/lib/utils";
import {Card, CardContent, CardHeader, CardTitle} from "~/components/ui/card";
import {AspectRatio} from "~/components/ui/aspect-ratio";

import styles from "~/styles/newsletter.css?url";
import type {LinksFunction} from "react-router";
import BackButton from "~/components/back-button";

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
    };
}

export async function loader({ params }: Route.LoaderArgs) {
    const newsletterFull = await getNewsletterBySlug(params.slug);
    if (!newsletterFull) {
        throw new Response("Not Found", { status: 404 });
    }
    let outputHtml = markdownToHtml(newsletterFull.outputMarkdown);
    // Modify the HTML string to add target="_blank" to links
    outputHtml = addTargetBlankToLinks(outputHtml);

    const data: ServerData = {
        newsletter: {
            publishedAt: newsletterFull.publishedAt,
            outputHtml: outputHtml, // Use the modified HTML
            title: newsletterFull.title,
            imageUrl: newsletterFull.imagesData.medium,
            modelName: newsletterFull.modelName,
        }
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
                <BackButton />
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
                <span className="block text-xs italic text-muted-foreground px-6 pt-3 pb-1 text-center md:text-left">
                    AI-generated content and visuals, informed by online data.
                </span>
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
                </CardContent>
            </Card>
        </div>
    );
}