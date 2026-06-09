import { pgTable, serial, text, real, timestamp } from "drizzle-orm/pg-core";

export const orphanages = pgTable("orphanages", {
  id: serial().primaryKey(),
  name: text().notNull(),
  address: text().notNull().default(""),
  city: text().notNull(),
  state: text().notNull().default(""),
  phone: text().notNull().default(""),
  email: text().notNull().default(""),
  latitude: real("latitude"),
  longitude: real("longitude"),
  needs: text().notNull().default(""),
  structured_needs: text("structured_needs").notNull().default("[]"),
  created_at: timestamp("created_at").defaultNow(),
});
