import {Carousel, CarouselContent, CarouselItem} from "~/components/ui/carousel";
import NewsletterCard from "~/components/newsletter-card";

interface NewsletterProps {
    newsletters: {
        id: number,
        publishedAt: Date,
        slug: string,
        title: string,
        imageUrl: string,
        newsletterConfigName: string,
    }[];
}

export default function NewsletterCarousel({
    newsletters
}: NewsletterProps) {
    return (
        <Carousel>
            <CarouselContent>
                {
                    newsletters.map((newsletter) => (
                        <CarouselItem
                            key={newsletter.id}
                            className="basis-1/3"
                        >
                            <NewsletterCard
                                key={newsletter.id}
                                publishedAt={newsletter.publishedAt}
                                slug={newsletter.slug}
                                imageUrl={newsletter.imageUrl}
                                title={newsletter.title}
                            />
                        </CarouselItem>
                    ))
                }
            </CarouselContent>
        </Carousel>
    )
}