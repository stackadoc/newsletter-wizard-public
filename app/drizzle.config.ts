import 'dotenv/config';
import { defineConfig } from 'drizzle-kit';
import {DB_URI} from "~/lib/constants";

export default defineConfig({
    out: './drizzle',
    schema: './app/db/schema.ts',
    dialect: 'postgresql',
    dbCredentials: {
        url: DB_URI,
    },
});
