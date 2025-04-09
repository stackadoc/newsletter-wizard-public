import type { Route } from "./+types/_layout.newsletter.$slug.tsx";
import {getNewsletterBySlug} from "~/actions/newsletters-actions";
import {markdownToHtml} from "~/lib/utils";
import {Card, CardContent, CardHeader, CardTitle} from "~/components/ui/card";
import {AspectRatio} from "~/components/ui/aspect-ratio";

type ServerData = {
    newsletter: {
        publishedAt: Date;
        outputHtml: string;
        title: string;
        imageUrl: string;
    };
}

export async function loader({ params }: Route.LoaderArgs) {
    const newsletterFull = await getNewsletterBySlug(params.slug);
    if (!newsletterFull) {
        throw new Response("Not Found", { status: 404 });
    }
    const data: ServerData = {
        newsletter: {
            publishedAt: newsletterFull.publishedAt,
            outputHtml: markdownToHtml(newsletterFull.outputMarkdown),
            title: newsletterFull.title,
            imageUrl: newsletterFull.imageUrl,
        }
    };

    return data;
}

export default function Newsletter({
    loaderData,
}: Route.ComponentProps) {
    const { newsletter } = loaderData;

    const formattedDate = new Date(newsletter.publishedAt).toLocaleDateString();

    return (
        <div className="container mx-auto px-4 py-8 max-w-4xl">
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
                <CardHeader className="p-6">
                    <CardTitle className="text-3xl lg:text-4xl font-bold mb-2">{newsletter.title}</CardTitle>
                    <p className="text-sm text-muted-foreground">
                        Published on {formattedDate}
                    </p>
                </CardHeader>
                <CardContent className="p-6 pt-0">
                    {/* Apply prose styles for Tailwind Typography plugin */}
                    {/* Ensure you have @tailwindcss/typography installed and configured */}
                    <div
                        className="prose dark:prose-invert max-w-none prose-headings:font-semibold prose-a:text-primary hover:prose-a:underline"
                        dangerouslySetInnerHTML={{ __html: newsletter.outputHtml }}
                    />
                    <i>AI-generated content and visuals, informed by online data.</i>
                </CardContent>
            </Card>
        </div>
    );
}