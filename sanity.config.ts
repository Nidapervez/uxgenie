// frontend/sanity.config.ts
import { defineConfig } from "sanity";
import { deskTool } from "sanity/desk";

export default defineConfig({
  name: "dynamic-blog-assistant",
  title: "Dynamic Blog Assistant",
  projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID,
  dataset: process.env.NEXT_PUBLIC_SANITY_DATASET || "production",
  plugins: [deskTool()],
  schema: {
    types: [
      {
        name: "blogPost",
        title: "Blog Post",
        type: "document",
        fields: [
          { name: "title", type: "string", title: "Title" },
          { name: "draft", type: "text", title: "Draft" },
          { name: "edits", type: "text", title: "Edits" },
          { name: "seo", type: "text", title: "SEO" },
          { name: "status", type: "string", title: "Status" }
        ],
      },
    ],
  },
});
