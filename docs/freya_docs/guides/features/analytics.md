> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Analytics

> Track call performance, visualize trends, and build custom dashboards with structured data widgets

## What is Analytics?

The Analytics page is your central hub for understanding how your voice agents are performing. It gives you a real-time view of call volume, duration, sentiment, outcomes, and conversation themes — all filterable by date range, call type, and phone number.

Beyond the built-in call metrics, you can create custom widgets that visualize structured data collected during calls, letting you track the business-specific metrics that matter most to your team.

## The Two Tabs

Analytics is split into two views, each serving a different purpose:

| Tab | Purpose |
| - | - |
| **Calls** | Pre-built charts for call volume, duration, status breakdown, and detected themes |
| **Structured Data** | Custom widgets you build yourself, powered by the structured data your agents collect during calls |

Switch between them using the tab bar at the top of the page. Filters like date range and call type are shared across both tabs.

## Calls Tab

The Calls tab gives you three metric cards, a status breakdown, and a theme map — all updating in real time as new calls come in.

### Metric Cards

Three interactive cards sit at the top of the page. Click any card to select it and see its trend chart below:

**Total Calls** shows the number of calls in the selected period, with a percentage change compared to the previous equivalent period. When selected, the chart below breaks down calls by **caller sentiment** — Very Happy, Happy, Neutral, Unhappy, Very Unhappy, and Untagged — displayed as a stacked stream chart so you can see how sentiment shifts over time.

**Average Duration** displays the mean call length in MM:SS format with a trend line chart. This helps you spot whether calls are getting longer (potentially more complex issues) or shorter (potentially more efficient handling).

**Total Talk Time** shows cumulative minutes across all calls. This is useful for capacity planning and understanding overall agent utilization.

Each card includes a percentage indicator showing the change from the previous period, so you can tell at a glance whether a metric is trending up or down.

### Call Status Breakdown

A pie chart shows how calls ended — Connected, Abandoned, Failed, Voicemail, and other outcomes. Each slice displays its percentage (hidden for slices under 5% to keep the chart readable), and a legend below shows the exact count for each status.

This is the fastest way to spot problems. If your "Failed" or "Abandoned" slice suddenly grows, something needs attention — maybe a provider issue, a misconfigured agent, or an unexpected spike in traffic.

### Call Themes

A treemap visualization shows the top 15 conversation themes detected across your calls. Larger blocks represent more frequently occurring themes, giving you an instant read on what callers are asking about most.

If no themes have been detected yet, the card displays a "No themes detected" message. Themes are generated automatically from call transcripts.

## Structured Data Tab

The Structured Data tab is a blank canvas where workspace admins can build custom widgets that visualize the data agents collect during calls — things like customer satisfaction ratings, deal values, issue categories, or any other structured field you've defined in **Insights**.

### Creating a Widget

1. Click the **Add Widget** button in the filter bar (visible to admins only)
2. Give the widget a **name** and optional **description**
3. Select the **structured data source** — this is the Insight definition your agents report against
4. Choose a **chart type** based on your data:

| Chart Type | Best For | Field Types |
| - | - | - |
| **Area** | Trends over time (averages) | Numeric only |
| **Stream** | Composition changes over time | Numeric only |
| **Stacked Bar** | Comparing categories across periods | Numeric only |
| **Radar** | Multi-dimensional comparison | Numeric only |
| **Pie** | Proportional breakdown | All types |
| **Donut** | Same as pie with a cleaner look | All types |
| **Treemap** | Hierarchical volume comparison | All types |

5. For charts that support it (Area, Stacked Bar, Stream, Radar), you can enable **multi-field selection** to plot several numeric fields on the same chart
6. Optionally filter by specific **agents** if you only want data from certain agents
7. Pick a **color theme** — Ocean, Purple, Forest, Sunset, or Rainbow
8. Set a **default date range** for the widget, or leave it to follow the global filter

### Managing Widgets

Once created, widgets appear as cards on the Structured Data tab. You can:

* **Drag and drop** widgets to reorder them into rows
* **Edit** any widget to change its chart type, data source, or filters
* **Delete** widgets you no longer need

Each widget can have its own date range preset. When a widget uses a custom range instead of the global filter, a label appears showing which preset is active — so you always know what time window you're looking at.

<Note>
  Only workspace admins (owners and members with the admin role) can create, edit, or delete widgets. All other members can view them.
</Note>

## Shared Filters

Both tabs share a filter bar with the following controls:

* **Date Range** — Preset options like "Last 7 Days", "Last 30 Days", or a custom range. The system automatically picks an appropriate granularity (hourly, daily, weekly, monthly) based on the range you select.
* **View Mode** — Toggle between **Regular** and **Cumulative** to see values per-period or as a running total. Cumulative mode is useful for tracking progress toward targets.
* **Call Type** — Multi-select filter for inbound, outbound, and other call types. Shows "All Call Types" when nothing is selected, or a count like "2 selected" when filtered.
* **Phone Number** — Filter to a specific phone number to isolate its performance.
* **Refresh** — Manually reload the data if you want the latest numbers without waiting for the auto-refresh cycle.

## Best Practices

* **Start with the Calls tab for daily health checks.** The three metric cards and status pie give you an instant pulse on system health. Make it a habit to check these at the start of each day.
* **Use the themes treemap to inform agent training.** If you notice a theme appearing frequently that your agents aren't handling well, update the agent's system prompt or add relevant content to the Knowledgebase.
* **Build Structured Data widgets for business KPIs.** The Calls tab tells you about call operations; the Structured Data tab tells you about business outcomes. Create widgets for the metrics your stakeholders care about — conversion rates, satisfaction scores, issue resolution.
* **Set widget-specific date ranges for dashboards.** If you have a widget tracking weekly targets, set it to "This Week" so it always shows current progress regardless of the global date filter.
* **Filter by phone number to compare lines.** If you have different numbers for different purposes (support vs. sales), filter by number to compare performance across lines.

## Next Steps

<CardGroup cols={2}>
  <Card title="Insights" icon="chart-mixed" href="/guides/fundamentals/agents">
    Define structured data fields that your agents collect during calls — the data that powers Structured Data widgets.
  </Card>

  <Card title="Campaigns" icon="megaphone" href="/guides/features/campaigns">
    Launch outbound calling campaigns and track their performance in Analytics.
  </Card>
</CardGroup>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.