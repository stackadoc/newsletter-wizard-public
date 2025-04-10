import type {NewsletterSelect, NewsletterWithConfigSelect} from "~/lib/types/newsletter-types";
import {db} from "~/db";
import {eq} from "drizzle-orm";
import {newsletterTable} from "~/db/schema";

export const getNewsletterBySlug = async (slug: string): Promise<NewsletterSelect | undefined> => {
    return db.query.newsletterTable.findFirst({
        where: eq(newsletterTable.slug, slug),
    });
}

export const getAllNewsletters = async (): Promise<NewsletterWithConfigSelect[]> => {
    return db.query.newsletterTable.findMany({
        with: {
            newsletterConfig: true,
        },
    });
}