import type { Config } from "@netlify/functions";
import { db } from "../../db/index.js";
import { orphanages } from "../../db/schema.js";
import { eq } from "drizzle-orm";

export default async (req: Request) => {
  const corsHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };

  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  if (req.method === "GET") {
    const url = new URL(req.url);
    // Handle /api/orphanages/:id
    const idParam = url.searchParams.get("id") || url.pathname.split("/").pop();
    if (idParam && !isNaN(Number(idParam))) {
      const id = parseInt(idParam, 10);
      const rows = await db.select().from(orphanages).where(eq(orphanages.id, id));
      if (rows.length === 0) {
        return Response.json({ success: false, error: "Not found" }, { status: 404, headers: corsHeaders });
      }
      return Response.json({ success: true, data: rows[0] }, { headers: corsHeaders });
    }

    const rows = await db.select().from(orphanages).orderBy(orphanages.created_at);
    return Response.json({ success: true, data: rows }, { headers: corsHeaders });
  }

  if (req.method === "POST") {
    const body = await req.json();
    const { name, address, city, state, phone, email, latitude, longitude, needs, structured_needs } = body;

    if (!name || !city) {
      return Response.json(
        { success: false, error: "name and city are required" },
        { status: 400, headers: corsHeaders }
      );
    }

    const [inserted] = await db
      .insert(orphanages)
      .values({
        name: String(name),
        address: String(address || ""),
        city: String(city),
        state: String(state || ""),
        phone: String(phone || ""),
        email: String(email || ""),
        latitude: latitude ? Number(latitude) : null,
        longitude: longitude ? Number(longitude) : null,
        needs: String(needs || ""),
        structured_needs: JSON.stringify(structured_needs || []),
      })
      .returning();

    return Response.json({ success: true, data: inserted }, { status: 201, headers: corsHeaders });
  }

  return new Response("Method not allowed", { status: 405, headers: corsHeaders });
};

export const config: Config = {
  path: ["/api/orphanages", "/api/orphanages/:id"],
};
