import {Link} from "react-router";
import {Card, CardHeader, CardTitle} from "~/components/ui/card";
import {AspectRatio} from "@radix-ui/react-aspect-ratio";

interface NewsletterCardProps {
    publishedAt: Date;
    slug: string;
    imageUrl: string;
    title: string;
}

export default function NewsletterCard({
    publishedAt,
    slug,
    imageUrl,
    title,
}: NewsletterCardProps) {

    const formattedDate = new Date(publishedAt).toISOString().split("T")[0]

    return (
        // Wrap Card with Link for navigation
        <Link
            to={`/newsletter/${slug}`} // Adjust path as needed
            className="group block" // Use group for hover effects if desired
        >
            <Card className="overflow-hidden h-full transition-shadow duration-200 hover:shadow-lg border bg-card text-card-foreground flex flex-col">
                {imageUrl && (
                    <AspectRatio ratio={16 / 9} className="bg-muted border-b">
                        <img
                            src={imageUrl}
                            alt={`Image for ${title}`}
                            className="object-cover w-full h-full transition-transform duration-300 group-hover:scale-105" // Subtle zoom on hover
                        />
                    </AspectRatio>
                )}
                <CardHeader className="p-4 flex-grow">
                    <CardTitle className="text-lg font-semibold leading-tight mb-1 group-hover:text-primary transition-colors duration-200"> {/* Title changes color on hover */}
                        {title}
                    </CardTitle>
                    <p className="text-xs text-muted-foreground">
                        Published on {formattedDate}
                    </p>
                </CardHeader>
            </Card>
        </Link>
    );

}