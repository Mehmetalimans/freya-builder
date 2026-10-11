> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Call Routing

> Configuring and optimizing call routing for various scenarios and use cases

## Call Routing Overview

Call routing determines how calls are directed and processed in Freyavoice AI. Effective routing ensures calls reach the right agent or workflow, are handled efficiently, and provide the best possible experience for callers.

## Routing Types

### Direct Agent Routing

**Simple Routing**: Route calls directly to a specific agent. This is the simplest routing method.

**Use Cases**: Best for straightforward use cases where a single agent can handle all calls.

**Configuration**: Simply select an agent for inbound or outbound routing.

**Advantages**: Simple setup, low latency, easy to manage.

**Limitations**: No conditional logic, can't route based on caller information.

### Workflow-Based Routing

**Complex Routing**: Route calls through workflows that can implement complex logic.

**Use Cases**: Best when you need conditional routing, multiple agents, or complex processing.

**Configuration**: Select a workflow that handles routing decisions.

**Advantages**: Flexible, powerful, supports complex scenarios.

**Considerations**: More complex to set up and maintain.

## Routing Strategies

### Time-Based Routing

**Business Hours**: Route to different agents or workflows based on time of day.

**After Hours**: Handle after-hours calls with special agents or voicemail.

**Holiday Routing**: Special routing for holidays or special dates.

**Timezone Handling**: Properly handle timezones for global operations.

### Caller-Based Routing

**Caller ID Routing**: Route based on the caller's phone number.

**VIP Routing**: Route known customers or VIPs to specialized agents.

**New vs Returning**: Different routing for new vs returning callers.

**Language Routing**: Route to agents that speak the caller's language.

### Purpose-Based Routing

**Department Routing**: Route to different departments based on caller selection or IVR.

**Service Type**: Route based on the type of service needed.

**Product Routing**: Route to agents specialized in specific products.

**Issue Type**: Route based on the type of issue or inquiry.

### Geographic Routing

**Area Code Routing**: Route based on caller's area code or location.

**Regional Agents**: Route to agents in specific regions.

**Local Presence**: Use local numbers for regional presence.

**International Routing**: Handle international calls appropriately.

## Routing Configuration

### Basic Setup

**Number Configuration**: Configure routing at the phone number level.

**Agent Selection**: Choose which agent handles calls (for direct routing).

**Workflow Selection**: Choose which workflow processes calls (for workflow routing).

**Fallback Options**: Set up fallback routing for when primary routing fails.

### Advanced Configuration

**Conditional Logic**: Set up conditions that determine routing paths.

**Multi-Path Routing**: Configure multiple possible routing paths.

**Priority Routing**: Set routing priorities for different scenarios.

**Dynamic Routing**: Implement dynamic routing based on real-time conditions.

## Routing Optimization

### Performance

**Minimize Latency**: Optimize routing to minimize time to agent response.

**Efficient Paths**: Design routing paths for efficiency.

**Reduce Complexity**: Simplify routing when possible to improve performance.

**Cache Decisions**: Cache routing decisions when appropriate.

### User Experience

**Quick Connection**: Route calls quickly to avoid long wait times.

**Appropriate Routing**: Ensure calls reach the right agent or department.

**Smooth Transfers**: Handle transfers smoothly when needed.

**Clear Communication**: Communicate routing decisions to users when appropriate.

### Cost Optimization

**Efficient Routing**: Route calls efficiently to minimize costs.

**Right-Size Agents**: Use appropriate agents for each call type.

**Optimize Workflows**: Optimize workflows to reduce processing time.

**Monitor Costs**: Track routing costs and optimize accordingly.

## Common Routing Patterns

### IVR-Style Routing

**Menu Options**: Present menu options to callers for self-service routing.

**Digit Selection**: Route based on caller's digit selection.

**Multi-Level Menus**: Support multi-level menu structures.

**Default Options**: Provide default routing for timeouts or invalid selections.

### Skill-Based Routing

**Agent Skills**: Route calls to agents with appropriate skills.

**Skill Matching**: Match call requirements with agent capabilities.

**Load Balancing**: Distribute calls across available agents.

**Queue Management**: Manage queues when all agents are busy.

### Priority Routing

**Priority Levels**: Define priority levels for different call types.

**VIP Handling**: Route high-priority calls immediately.

**Queue Prioritization**: Prioritize calls in queues.

**Resource Allocation**: Allocate resources based on priority.

## Best Practices

### Planning

**Define Requirements**: Clearly define routing requirements before implementation.

**Map Flows**: Map out routing flows to visualize logic.

**Consider Edge Cases**: Plan for edge cases and error conditions.

**Test Scenarios**: Plan test scenarios for all routing paths.

### Implementation

**Start Simple**: Begin with simple routing and add complexity as needed.

**Test Thoroughly**: Test all routing paths before going live.

**Document Logic**: Document routing logic for future reference.

**Monitor Performance**: Monitor routing performance continuously.

### Optimization

**Analyze Patterns**: Analyze call patterns to optimize routing.

**A/B Testing**: Test different routing strategies to find what works best.

**Iterate**: Continuously improve routing based on data and feedback.

**Simplify**: Simplify routing when complexity doesn't add value.

## Troubleshooting

### Common Issues

**Wrong Routing**: Verify routing configuration and test with simulations.

**Slow Routing**: Optimize routing logic and check system performance.

**Failed Routing**: Check fallback options and error handling.

**Unexpected Behavior**: Review routing logic and test edge cases.

### Debugging

**Routing Logs**: Review routing logs to understand routing decisions.

**Test Calls**: Make test calls to verify routing behavior.

**Configuration Review**: Verify all routing configurations are correct.

**Provider Issues**: Check provider-side routing if applicable.

## Next Steps

<Card title="Voice Configuration" icon="microphone" href="/guides/telephony/voice-configuration">
  Learn how to configure voice settings for optimal audio quality and user experience.
</Card>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.