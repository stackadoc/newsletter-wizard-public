import { Link } from "react-router";
import { Card, CardHeader, CardTitle } from "~/components/ui/card";
import { AspectRatio } from "@radix-ui/react-aspect-ratio";
import { Badge } from "~/components/ui/badge";
import {ReadCountBadge} from "~/components/read-count-badge"; // Import Badge

interface NewsletterCardProps {
    publishedAt: Date;
    slug: string;
    imageUrl: string;
    title: string;
    nbRead: number;
    newsletterConfigName?: string; // Keep this prop
}

export default function NewsletterCard({
    publishedAt,
    slug,
    imageUrl,
    title,
    newsletterConfigName,
    nbRead,
}: NewsletterCardProps) {

    const formattedDate = new Date(publishedAt).toISOString().split("T")[0]

    return (
        // Wrap Card with Link for navigation
        <Link
            to={`/newsletter/${slug}`} // Adjust path as needed
            className="group block h-full" // Use group for hover effects if desired
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
                    {newsletterConfigName && ( // Conditionally render the Badge
                        <Badge variant="secondary">{newsletterConfigName}</Badge>
                    )}
                    <div className="flex items-center justify-between mt-2"> {/* Flex container for date and badge */}
                        <p className="text-xs text-muted-foreground">
                            Published on {formattedDate}
                        </p>
                        <ReadCountBadge count={nbRead} />
                    </div>
                </CardHeader>
            </Card>
        </Link>
    );

}