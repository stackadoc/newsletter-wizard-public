import type {NewsletterSelect, NewsletterWithConfigSelect} from "~/lib/types/newsletter-types";
import {db} from "~/db";
import {and, desc, eq, lt, sql} from "drizzle-orm";
import {newsletterTable} from "~/db/schema";

export const getNewsletterBySlug = async (slug: string): Promise<NewsletterSelect | undefined> => {
    return db.query.newsletterTable.findFirst({
        where: eq(newsletterTable.slug, slug),
    });
}

export const getFirstNewsletterBeforeDate = async (date: Date, newsletterConfigId: number): Promise<NewsletterSelect | undefined> => {
    return db.query.newsletterTable.findFirst({
        where: and(
            eq(newsletterTable.newsletterConfigId, newsletterConfigId),
            lt(newsletterTable.publishedAt, date),
        ),
        orderBy: [desc(newsletterTable.publishedAt)],
    });
}

export const getAllNewsletters = async (): Promise<NewsletterWithConfigSelect[]> => {
    return db.query.newsletterTable.findMany({
        with: {
            newsletterConfig: true,
        },
    });
}

export const incrementReadCount = async (slug: string): Promise<void> => {
    await db.update(newsletterTable).set({
        nbRead: sql`${newsletterTable.nbRead} + 1`,
    }).where(eq(newsletterTable.slug, slug)).execute();
}