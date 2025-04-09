import 'dotenv/config';
import { drizzle } from 'drizzle-orm/node-postgres';
import {DB_URI} from "~/lib/constants";
import * as schema from './schema';

export const db = drizzle(DB_URI, { schema });