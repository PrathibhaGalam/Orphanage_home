CREATE TABLE "orphanages" (
	"id" serial PRIMARY KEY,
	"name" text NOT NULL,
	"address" text DEFAULT '' NOT NULL,
	"city" text NOT NULL,
	"state" text DEFAULT '' NOT NULL,
	"phone" text DEFAULT '' NOT NULL,
	"email" text DEFAULT '' NOT NULL,
	"latitude" real,
	"longitude" real,
	"needs" text DEFAULT '' NOT NULL,
	"structured_needs" text DEFAULT '[]' NOT NULL,
	"created_at" timestamp DEFAULT now()
);
