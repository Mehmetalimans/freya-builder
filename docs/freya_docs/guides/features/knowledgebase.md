> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Knowledgebase

> Give your AI agents access to your company's knowledge — documents, websites, and custom answers — for accurate, grounded responses

## What is the Knowledgebase?

The Knowledgebase is a workspace-level content library that your AI agents can query in real time during calls. Instead of embedding all your information directly into an agent's system prompt, you store it in the Knowledgebase and let the agent retrieve only what's relevant to each conversation.

This keeps prompts lean, responses accurate, and your content easy to maintain — update a document once and every agent in the workspace benefits immediately.

<Note>
  The Knowledgebase is currently in **beta**. Features and limits may change as we continue to improve the system.
</Note>

## How It Works

When an agent needs information during a call, it sends a query to the Knowledgebase. The system runs a **hybrid search** — combining semantic (meaning-based) search with keyword and heading search — then returns the most relevant content with full citations back to the agent in under 200ms.

The agent uses this retrieved content to ground its response, and can cite the exact document and section it used.

## Content Types

### Articles

Articles are rich, long-form documents — product guides, FAQs, policy documents, or any structured content. They support full Markdown formatting and are displayed with auto-generated thumbnails in the dashboard.

Articles can come from:

* **Written directly** in the Freya editor
* **Uploaded files** (PDF, TXT, Markdown, DOCX)
* **Synced web pages** crawled from your website

### Snippets

Snippets are short, reusable pieces of text — policies, macros, standard phrasing, or quick reference facts. They are designed to be concise and targeted, ideal for content that agents need to recite verbatim or reference frequently.

Create a snippet and start typing immediately — no upload or processing required.

The recommended format for snippets is a top-level title, followed by questions as subheadings with their answers below:

```markdown theme={null}
# Refund Policy

## How long do refunds take?
Refunds are processed within 5–7 business days and returned to the original payment method.

## Can I get a refund after 30 days?
Refunds are only available within 30 days of purchase. After that, we can offer store credit instead.
```

This structure helps the retrieval system match the right answer to the caller's exact question.

## Adding Content

### Writing or Uploading a Document

**Create a snippet manually:**

1. Go to **Knowledgebase** in the sidebar
2. Click **New Snippet** in the top-right corner
3. A new blank snippet opens — give it a title and start writing
4. When you save your content, it is automatically processed and indexed for search

**Upload a file:**

1. In the **Add Content** section, click **Upload Document**
2. Select a PDF, TXT, Markdown, or DOCX file (up to 10MB)
3. The file is processed in the background — text is extracted, structured, and indexed
4. Once processing completes, the document is published and available to agents

<Tip>
  PDFs are processed with OCR support, so scanned documents work too. A thumbnail is generated automatically from the first page.
</Tip>

### Syncing a Website

Sync entire websites or specific pages to keep your knowledgebase up to date with your online content.

1. In the **Add Content** section, click **Sync Website**
2. Enter the URL of the website or page you want to crawl
3. Freya discovers all available pages and lists them in real time
4. Select the pages you want to include, then click **Sync**
5. Each page is fetched, cleaned, and indexed as a separate article

<Tip>
  Syncing uses OpenGraph images as thumbnails where available, with an automatic screenshot as fallback.
</Tip>

### Content Processing

After you add any content, it goes through an automatic processing pipeline:

1. **Extraction** — Text is extracted and cleaned from any supported file format
2. **Chunking** — Content is split into structured sections, respecting document headings and hierarchy
3. **Embedding** — Each section is encoded for semantic search
4. **Indexing** — Sections are stored and indexed for fast retrieval

Processing happens asynchronously in the background. You can continue working while documents are being indexed. A status indicator shows when processing is complete.

## Testing Retrieval

The right panel of the Knowledgebase page is a **live test chat**. You can type any query and see exactly what your agents would retrieve — including the matched content, document titles, and the heading path within the document (e.g. `Getting Started > Installation > Requirements`).

Use this to:

* Verify that important content is being retrieved correctly
* Check that the right document ranks first for common queries
* Identify gaps where no relevant content is found

## Using the Knowledgebase in Agents

The Knowledgebase is available to all agents in the same workspace automatically. No per-agent configuration is needed to enable retrieval — agents query the shared workspace knowledgebase during calls.

To get the best results, instruct your agent to use the knowledgebase in its system prompt. For example:

```
When a caller asks a question about our products, policies, or procedures,
search the knowledgebase before responding. Always cite the source document
when using retrieved information.
```

Agents receive search results with:

* The matched content (with surrounding context for continuity)
* Document title and type
* The hierarchical heading path within the document
* Source URL (for synced pages)

## Managing Your Content

### Published vs. Draft

Documents can be in one of three states:

| Status | Description |
| - | - |
| **Draft** | Not yet available to agents. New documents start here while processing. |
| **Published** | Indexed and available for retrieval. |
| **Archived** | Hidden from retrieval but preserved for reference. |

The count shown next to each content type (e.g. `3 / 5`) reflects **published / total** documents. An **Enabled** badge appears when at least one document of that type is published and active.

### Updating Content

Editing a published document triggers an automatic **reindex** — the old chunks are replaced with new ones derived from the updated content. Your agents always query the latest version.

## Best Practices

* **Structure your documents with clear headings.** The retrieval system uses document structure to find the right section, not just keyword matches. Well-organized content retrieves more accurately.
* **Keep snippets short and focused.** Snippets work best for single-topic content like refund policies, opening hours, or a specific product's pricing. Avoid mixing multiple topics in one snippet.
* **Use the test chat before going live.** Run your most common caller questions through the test panel to confirm the right content surfaces before connecting agents to real calls.
* **Sync website pages that change often.** Rather than manually updating documents, sync your public help center or product pages so the knowledgebase stays current automatically.
* **Avoid duplicating content across documents.** Duplicate information can confuse retrieval ranking and cause agents to return inconsistent answers.

## Next Steps

<CardGroup cols={2}>
  <Card title="AI Studio" icon="wand-magic-sparkles" href="/guides/features/ai-studio">
    Use AI Studio to refine your agent's system prompt and teach it how to best use knowledgebase results.
  </Card>

  <Card title="Simulations" icon="flask" href="/guides/features/simulations">
    Test your agents end-to-end with simulated calls to verify knowledgebase-grounded responses.
  </Card>
</CardGroup>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.