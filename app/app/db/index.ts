import 'dotenv/config';
import { drizzle } from 'drizzle-orm/node-postgres';
import {DB_URI} from "~/lib/constants";

const db = drizzle(DB_URI);