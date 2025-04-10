import {newsletterTable} from "~/db/schema";
import type {NewsletterConfigSelect} from "~/lib/types/newsletter-config-types";

export type NewsletterSelect = typeof newsletterTable.$inferSelect;

export type NewsletterWithConfigSelect = NewsletterSelect & {
    newsletterConfig: NewsletterConfigSelect;
}