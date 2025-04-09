CREATE TABLE "extract" (
	"id" serial PRIMARY KEY NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"last_update" timestamp DEFAULT now() NOT NULL,
	"extractor_type" text NOT NULL,
	"config" jsonb NOT NULL,
	"content" jsonb NOT NULL,
	"content_date" timestamp NOT NULL,
	"content_id" text NOT NULL,
	"source_id" integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE "llm_config" (
	"id" serial PRIMARY KEY NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"last_update" timestamp DEFAULT now() NOT NULL,
	"name" text NOT NULL,
	"base_url" text NOT NULL,
	"api_key_name" text NOT NULL,
	"model_name" text NOT NULL,
	"system_prompt" text NOT NULL,
	"params" jsonb NOT NULL
);
--> statement-breakpoint
CREATE TABLE "newsletter_config" (
	"id" serial PRIMARY KEY NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"last_update" timestamp DEFAULT now() NOT NULL,
	"name" text NOT NULL,
	"slug" text NOT NULL,
	"llm_config_id" integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE "newsletter" (
	"id" serial PRIMARY KEY NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"last_update" timestamp DEFAULT now() NOT NULL,
	"base_url" text NOT NULL,
	"model_name" text NOT NULL,
	"params" jsonb NOT NULL,
	"system_prompt" text NOT NULL,
	"input_text" text NOT NULL,
	"output_markdown" text NOT NULL,
	"output_html" text NOT NULL,
	"title" text NOT NULL,
	"slug" text NOT NULL,
	"image_url" text NOT NULL,
	"newsletter_config_id" integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE "source_newsletter_config_association" (
	"source_id" integer NOT NULL,
	"newsletter_config_id" integer NOT NULL,
	CONSTRAINT "source_newsletter_config_association_source_id_newsletter_config_id_pk" PRIMARY KEY("source_id","newsletter_config_id")
);
--> statement-breakpoint
CREATE TABLE "source" (
	"id" serial PRIMARY KEY NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"last_update" timestamp DEFAULT now() NOT NULL,
	"name" text NOT NULL,
	"type" text NOT NULL,
	"config" jsonb NOT NULL
);
--> statement-breakpoint
ALTER TABLE "extract" ADD CONSTRAINT "extract_source_id_source_id_fk" FOREIGN KEY ("source_id") REFERENCES "public"."source"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "newsletter_config" ADD CONSTRAINT "newsletter_config_llm_config_id_llm_config_id_fk" FOREIGN KEY ("llm_config_id") REFERENCES "public"."llm_config"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "newsletter" ADD CONSTRAINT "newsletter_newsletter_config_id_newsletter_config_id_fk" FOREIGN KEY ("newsletter_config_id") REFERENCES "public"."newsletter_config"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "source_newsletter_config_association" ADD CONSTRAINT "source_newsletter_config_association_source_id_source_id_fk" FOREIGN KEY ("source_id") REFERENCES "public"."source"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "source_newsletter_config_association" ADD CONSTRAINT "source_newsletter_config_association_newsletter_config_id_newsletter_config_id_fk" FOREIGN KEY ("newsletter_config_id") REFERENCES "public"."newsletter_config"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
CREATE UNIQUE INDEX "uq_extract_source_id_content_id" ON "extract" USING btree ("source_id","content_id");--> statement-breakpoint
CREATE INDEX "extract_source_id_idx" ON "extract" USING btree ("source_id");--> statement-breakpoint
CREATE INDEX "newsletter_config_id_idx" ON "newsletter" USING btree ("newsletter_config_id");--> statement-breakpoint
CREATE INDEX "assoc_source_id_idx" ON "source_newsletter_config_association" USING btree ("source_id");--> statement-breakpoint
CREATE INDEX "assoc_newsletter_config_id_idx" ON "source_newsletter_config_association" USING btree ("newsletter_config_id");