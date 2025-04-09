import {
    pgTable,
    serial,
    text,
    timestamp,
    integer,
    jsonb,
    primaryKey,
    uniqueIndex,
    index,
} from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';

// --- Tables ---

export const sourceTable = pgTable('source', {
    id: serial('id').primaryKey(),
    createdAt: timestamp('created_at').defaultNow().notNull(),
    lastUpdate: timestamp('last_update').defaultNow().notNull(),
    name: text('name').notNull(),
    type: text('type').notNull(),
    config: jsonb('config').notNull(),
});

export const llmConfigTable = pgTable('llm_config', {
    id: serial('id').primaryKey(),
    createdAt: timestamp('created_at').defaultNow().notNull(),
    lastUpdate: timestamp('last_update').defaultNow().notNull(),
    name: text('name').notNull(),
    baseUrl: text('base_url').notNull(),
    apiKeyName: text('api_key_name').notNull(),
    modelName: text('model_name').notNull(),
    systemPrompt: text('system_prompt').notNull(),
    params: jsonb('params').notNull(),
});

export const newsletterConfigTable = pgTable('newsletter_config', {
    id: serial('id').primaryKey(),
    createdAt: timestamp('created_at').defaultNow().notNull(),
    lastUpdate: timestamp('last_update').defaultNow().notNull(),
    name: text('name').notNull(),
    slug: text('slug').notNull(),
    imageUrl: text('image_url').notNull(),
    llmConfigId: integer('llm_config_id')
        .notNull()
        .references(() => llmConfigTable.id),
});

export const extractTable = pgTable('extract', {
    id: serial('id').primaryKey(),
    createdAt: timestamp('created_at').defaultNow().notNull(),
    lastUpdate: timestamp('last_update').defaultNow().notNull(),
    extractorType: text('extractor_type').notNull(),
    config: jsonb('config').notNull(),
    content: jsonb('content').notNull(),
    contentDate: timestamp('content_date').notNull(),
    contentId: text('content_id').notNull(),
    sourceId: integer('source_id')
        .notNull()
        .references(() => sourceTable.id),
}, (table) => {
    return {
        uqExtractSourceIdContentId: uniqueIndex('uq_extract_source_id_content_id').on(table.sourceId, table.contentId),
        sourceIdIdx: index("extract_source_id_idx").on(table.sourceId), // Optional: Index for FK
    };
});

export const newsletterTable = pgTable('newsletter', {
    id: serial('id').primaryKey(),
    createdAt: timestamp('created_at').defaultNow().notNull(),
    lastUpdate: timestamp('last_update').defaultNow().notNull(),
    publishedAt: timestamp('published_at').notNull(),
    baseUrl: text('base_url').notNull(),
    modelName: text('model_name').notNull(),
    params: jsonb('params').notNull(),
    systemPrompt: text('system_prompt').notNull(),
    outputMarkdown: text('output_markdown').notNull(),
    title: text('title').notNull(),
    slug: text('slug').notNull(),
    imageUrl: text('image_url').notNull(),
    newsletterConfigId: integer('newsletter_config_id')
        .notNull()
        .references(() => newsletterConfigTable.id),
}, (table) => {
    return {
        newsletterConfigIdIdx: index("newsletter_config_id_idx").on(table.newsletterConfigId), // Optional: Index for FK
    };
});

// Junction table for Source <-> NewsletterConfig many-to-many relationship
export const sourceNewsletterConfigAssociationTable = pgTable(
    'source_newsletter_config_association',
    {
        sourceId: integer('source_id')
            .notNull()
            .references(() => sourceTable.id, { onDelete: 'cascade' }),
        newsletterConfigId: integer('newsletter_config_id')
            .notNull()
            .references(() => newsletterConfigTable.id, { onDelete: 'cascade' }),
    },
    (table) => {
        return {
            pk: primaryKey({ columns: [table.sourceId, table.newsletterConfigId] }),
            sourceIdIdx: index("assoc_source_id_idx").on(table.sourceId), // Optional: Index for FK
            newsletterConfigIdIdx: index("assoc_newsletter_config_id_idx").on(table.newsletterConfigId), // Optional: Index for FK
        };
    }
);

// --- Relations ---

export const sourceRelations = relations(sourceTable, ({ many }) => ({
    extracts: many(extractTable),
    sourceNewsletterConfigs: many(sourceNewsletterConfigAssociationTable),
}));

export const llmConfigRelations = relations(llmConfigTable, ({ many }) => ({
    newsletterConfigs: many(newsletterConfigTable),
}));

export const newsletterConfigRelations = relations(
    newsletterConfigTable,
    ({ one, many }) => ({
        llmConfig: one(llmConfigTable, {
            fields: [newsletterConfigTable.llmConfigId],
            references: [llmConfigTable.id],
        }),
        sourceNewsletterConfigs: many(sourceNewsletterConfigAssociationTable),
        newsletters: many(newsletterTable),
    })
);

export const extractRelations = relations(extractTable, ({ one }) => ({
    source: one(sourceTable, {
        fields: [extractTable.sourceId],
        references: [sourceTable.id],
    }),
}));

export const newsletterRelations = relations(newsletterTable, ({ one }) => ({
    newsletterConfig: one(newsletterConfigTable, {
        fields: [newsletterTable.newsletterConfigId],
        references: [newsletterConfigTable.id],
    }),
}));

export const sourceNewsletterConfigAssociationRelations = relations(
    sourceNewsletterConfigAssociationTable,
    ({ one }) => ({
        source: one(sourceTable, {
            fields: [sourceNewsletterConfigAssociationTable.sourceId],
            references: [sourceTable.id],
        }),
        newsletterConfig: one(newsletterConfigTable, {
            fields: [sourceNewsletterConfigAssociationTable.newsletterConfigId],
            references: [newsletterConfigTable.id],
        }),
    })
);