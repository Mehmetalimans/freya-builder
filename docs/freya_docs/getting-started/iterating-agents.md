> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Iterate Your Agents

> Learn how to use AI Studio to improve your agent prompts and performance

## Overview

AI Studio is a powerful tool in Freya that helps you iteratively improve your agent's system prompt. Using AI assistance, you can refine prompts, add instructions, improve clarity, and optimize performance without manually editing long prompts.

## Accessing AI Studio

To open AI Studio:

1. Navigate to an agent's configuration page
2. Find the **System Prompt** section
3. Click the **"AI Studio"** button (usually represented by a sparkles or magic wand icon)

## AI Studio Interface

AI Studio opens in a split-screen modal with two panels:

### Left Panel: AI Assistant Chat

The left panel contains a chat interface where you can:

* **Ask for improvements** - Request specific changes to your prompt
* **Get suggestions** - Ask the AI to suggest improvements
* **Iterate on changes** - Refine prompts through conversation
* **View thinking process** - See how the AI analyzes and improves your prompt

### Right Panel: Prompt Editor

The right panel shows:

* **Current Prompt** - Your agent's system prompt
* **Live Updates** - Changes made by the AI assistant in real-time
* **Direct Editing** - You can also edit the prompt manually

## Using AI Studio

### Step 1: Describe What You Want

In the chat interface, describe what you want to change or improve. For example:

* "Make the prompt more professional"
* "Add instructions for handling angry customers"
* "Improve clarity and remove ambiguity"
* "Add context about our company's return policy"
* "Make the agent sound more friendly and conversational"

### Step 2: Review AI Suggestions

The AI assistant will:

1. Analyze your current prompt
2. Understand your request
3. Generate an improved version
4. Show you the changes in real-time

### Step 3: Iterate and Refine

You can:

* **Ask for more changes** - Request additional modifications
* **Accept the changes** - Use the improved prompt
* **Reject and try again** - Ask for a different approach
* **Manually edit** - Make your own adjustments in the editor

### Step 4: Save Your Changes

Once you're satisfied with the improved prompt:

1. Review the final prompt in the editor
2. Click **"Save"** to apply the changes to your agent
3. The AI Studio will close and your agent will be updated

## AI Studio Features

### Thinking Process

AI Studio shows you the AI's thinking process:

* **Evaluation Phase** - How the AI analyzes your current prompt
* **Planning Phase** - What changes the AI plans to make
* **Execution Phase** - The actual improvements being made

This transparency helps you understand how your prompt is being improved.

### Copy Prompt

You can copy the improved prompt at any time:

1. Click the **"Copy"** button in the prompt editor
2. The prompt will be copied to your clipboard
3. You can paste it elsewhere or use it in other agents

### Variable Support

AI Studio understands Freya's variable syntax:

* Use `{{variable}}` for dynamic values
* The AI will preserve these variables in the improved prompt
* Variables are highlighted in the editor

## Best Practices

<Tip>
  Be specific about what you want to change. Vague requests lead to less useful improvements.
</Tip>

<Tip>
  Iterate in small steps. Make one type of improvement at a time for better results.
</Tip>

<Tip>
  Test your agent after making changes to ensure the improvements work as expected.
</Tip>

<Warning>
  Always review AI-generated changes before saving. The AI is helpful but may not always understand your exact requirements.
</Warning>

## Example Use Cases

### Making Prompts More Professional

```
You: "Make this prompt sound more professional and business-appropriate"

AI: [Analyzes prompt and suggests more formal language, 
     removes casual phrases, adds professional tone]
```

### Adding Specific Instructions

```
You: "Add instructions for handling customers who want to cancel their subscription"

AI: [Adds a new section with specific cancellation handling instructions]
```

### Improving Clarity

```
You: "This prompt is confusing. Make it clearer and easier to understand"

AI: [Restructures prompt, simplifies language, adds clear sections]
```

## Next Steps

<Card title="Import a Phone Number" icon="phone" href="/basic-operations/import-phone-number">
  Once your agent is optimized, connect it to a phone number to start receiving calls.
</Card>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.