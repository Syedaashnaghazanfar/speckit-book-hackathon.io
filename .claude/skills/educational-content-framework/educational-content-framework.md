---
name: "educational-content-framework"
description: "Structured framework for writing course content with professional pedagogy. Use when creating chapters, lessons, or educational materials. Ensures consistency, progressive difficulty, and coherent learning paths."
version: "1.0.0"
---

# Educational Content Framework Skill 📚

## When to Use This Skill

- Creating course chapters or lessons
- Writing technical tutorials or documentation
- Developing learning materials for any subject
- Ensuring educational content consistency
- Planning a multi-week course structure

## Core Framework Components

### 1. Chapter Template Structure

Every chapter should follow this consistent structure:

```markdown
# Week [N]: [Topic Name]

## Learning Objectives
By the end of this week, you will be able to:
- [Action Verb] [Specific Skill/Knowledge] [Context/Criteria]
- [Action Verb] [Specific Skill/Knowledge] [Context/Criteria]
- [Action Verb] [Specific Skill/Knowledge] [Context/Criteria]

## Prerequisites
- [Required prior knowledge]
- [Required tools/setup]
- [Recommended background]

## Overview
[2-3 paragraph introduction that:]
- Hooks the learner with relevance
- Previews key concepts
- Connects to prior and future weeks

## Core Concepts

### Concept 1: [Name]
**What**: [Definition in plain language]
**Why**: [Relevance and application]
**How**: [Step-by-step explanation or demonstration]

[Code examples, diagrams, or illustrations]

**Common Pitfalls**:
- [Mistake 1 and how to avoid it]
- [Mistake 2 and how to avoid it]

### Concept 2: [Name]
[Same structure as Concept 1]

## Hands-On Practice

### Exercise 1: [Descriptive Name]
**Difficulty**: [Beginner/Intermediate/Advanced]
**Time Estimate**: [X minutes]
**Objective**: [What skill this builds]

**Task**: [Clear, actionable instructions]

**Expected Output**: [What success looks like]

**Hints**:
- [Hint 1]
- [Hint 2]

**Solution**: [Link to solution file or expandable section]

## Deep Dive (Optional Advanced Content)
[Advanced topics for interested learners]
[Can be skipped without breaking flow]

## Summary
- [Key takeaway 1]
- [Key takeaway 2]
- [Key takeaway 3]

## Self-Assessment
1. [Question testing understanding]
2. [Question testing application]
3. [Question testing synthesis]

## Next Steps
- Preview of Week [N+1]
- Optional resources for deeper learning
- Community challenges or projects

## References
- [Authoritative sources]
- [Related documentation]
- [Further reading]
```

### 2. Learning Objectives Framework

Use **Bloom's Taxonomy** action verbs for measurable objectives:

**Beginner Level (Remember/Understand)**:
- Define, List, Describe, Explain, Identify, Recognize

**Intermediate Level (Apply/Analyze)**:
- Implement, Use, Execute, Demonstrate, Compare, Categorize

**Advanced Level (Evaluate/Create)**:
- Design, Build, Construct, Evaluate, Critique, Optimize

**Format**: `[Action Verb] + [Specific Knowledge/Skill] + [Context/Criteria]`

**Examples**:
- ✅ "Implement a basic ROS 2 publisher-subscriber pattern using Python"
- ✅ "Analyze sensor data to identify noise patterns and filtering requirements"
- ❌ "Understand ROS 2" (too vague, not measurable)

### 3. Assessment Rubric Templates

#### Exercise Rubric

| Criteria | Beginner (1-2) | Intermediate (3-4) | Advanced (5) |
|----------|----------------|-------------------|--------------|
| **Correctness** | Code runs with errors | Code runs correctly for basic cases | Handles edge cases elegantly |
| **Code Quality** | Hardcoded values, unclear naming | Some abstraction, decent naming | Modular, well-documented, reusable |
| **Complexity** | Solves basic requirement | Adds helpful features | Optimized, production-ready |

#### Chapter Completion Checklist

- [ ] All learning objectives addressed
- [ ] Code examples tested and working
- [ ] At least 2 exercises per major concept
- [ ] Prerequisites clearly stated
- [ ] References to official documentation included
- [ ] Cross-references to related chapters
- [ ] Self-assessment questions provided

### 4. Exercise Difficulty Levels

**Beginner (Foundation)**:
- Follow clear step-by-step instructions
- Single concept focus
- Expected time: 10-15 minutes
- Success rate target: 90%+

**Intermediate (Integration)**:
- Combine 2-3 concepts
- Some problem-solving required
- Expected time: 20-30 minutes
- Success rate target: 70%+

**Advanced (Application)**:
- Open-ended challenge
- Multiple concepts + independent research
- Expected time: 45-60 minutes
- Success rate target: 50%+ (stretch goal)

**Progressive Difficulty Pattern**:
- Week 1-3: 80% Beginner, 20% Intermediate
- Week 4-7: 50% Intermediate, 30% Beginner, 20% Advanced
- Week 8-13: 60% Advanced, 30% Intermediate, 10% Beginner

### 5. Technical Writing Style Guide

**Code Examples**:
```python
# ✅ GOOD: Annotated, runnable, focused
# Initialize ROS 2 node for temperature monitoring
rclpy.init(args=args)
node = rclpy.create_node('temperature_monitor')

# Create publisher on 'sensor/temp' topic
publisher = node.create_publisher(Temperature, 'sensor/temp', 10)
```

```python
# ❌ BAD: No context, unexplained magic numbers
rclpy.init(args=args)
n = rclpy.create_node('tm')
p = n.create_publisher(Temperature, 'st', 10)
```

**Explanations**:
- Use second person ("you will implement...")
- Present tense for general truths
- Active voice preferred
- Define jargon on first use
- Use analogies for complex concepts

**Structure**:
- Short paragraphs (3-4 sentences max)
- Bullet points for lists
- Consistent heading hierarchy
- Code blocks with syntax highlighting

**Tone**:
- Encouraging but not patronizing
- Technical but accessible
- Assumes intelligence, not prior knowledge

### 6. Cross-Referencing Patterns

**Internal References**:
```markdown
As we learned in [Week 2: ROS 2 Basics](../week-02/README.md#publishers), publishers...

This concept builds on [sensor integration](../week-05/README.md#sensor-drivers) from Week 5.

We'll use this pattern again in [Week 10: VLA Integration](../week-10/README.md).
```

**Dependency Graph**:
```markdown
## Week 5 Dependencies
**Required**: Week 2 (ROS 2 basics), Week 3 (Nodes and Topics)
**Recommended**: Week 4 (Services and Actions)
**Builds toward**: Week 8 (Sensor Fusion), Week 10 (VLA)
```

**Forward References**:
```markdown
> **Coming Up**: In Week 8, we'll use this sensor data for multi-modal fusion with vision systems.
```

## Quality Checklist for Educational Content

### Content Quality
- [ ] Learning objectives are measurable and achievable
- [ ] Prerequisites are clearly stated
- [ ] Core concepts explained with "What-Why-How" structure
- [ ] At least one real-world example per concept
- [ ] Common pitfalls and mistakes addressed

### Technical Quality
- [ ] All code examples are tested and working
- [ ] Code follows consistent style conventions
- [ ] Commands include expected output
- [ ] Error messages and troubleshooting included
- [ ] Dependencies and versions specified

### Pedagogical Quality
- [ ] Progressive difficulty (easy → hard)
- [ ] Concepts build on each other logically
- [ ] Multiple learning modalities (text, code, visuals)
- [ ] Immediate practice opportunities
- [ ] Self-assessment and reflection prompts

### Course Coherence (13-Week View)
- [ ] Each week connects to previous weeks
- [ ] Skill progression is evident
- [ ] Capstone project integrates earlier concepts
- [ ] Vocabulary is consistent across weeks
- [ ] References are bidirectional

## 13-Week Course Structure Template

### Foundation Phase (Weeks 1-4)
- **Focus**: Core concepts, tool setup, basic patterns
- **Difficulty**: Beginner-heavy
- **Projects**: Small, isolated exercises
- **Assessment**: Can you follow instructions and run basic examples?

### Development Phase (Weeks 5-9)
- **Focus**: Integration, problem-solving, best practices
- **Difficulty**: Intermediate-heavy
- **Projects**: Multi-component systems
- **Assessment**: Can you combine concepts to solve new problems?

### Mastery Phase (Weeks 10-13)
- **Focus**: Advanced topics, optimization, real-world application
- **Difficulty**: Advanced-heavy
- **Projects**: Capstone project
- **Assessment**: Can you design and build independently?

## Example Usage

**User Request**: "Create Week 7 content on ROS 2 sensor fusion"

**Framework Application**:

1. **Check Dependencies**: Verify Weeks 2-6 covered ROS 2 basics, sensors, data processing
2. **Set Learning Objectives** (Intermediate level):
   - "Implement a basic Kalman filter for sensor fusion in ROS 2"
   - "Analyze multi-sensor data streams to improve state estimation"
   - "Compare fusion strategies for different sensor combinations"

3. **Structure Content**:
   - Overview: Why sensor fusion matters (autonomous navigation example)
   - Concept 1: Sensor Fusion Fundamentals (What-Why-How)
   - Concept 2: Kalman Filtering Basics
   - Concept 3: ROS 2 Multi-Subscriber Pattern
   - Exercise 1 (Intermediate): Fuse IMU + Odometry
   - Exercise 2 (Advanced): Add vision data to fusion

4. **Apply Style Guide**:
   - Annotated code examples
   - Real robot scenarios
   - Troubleshooting section

5. **Cross-Reference**:
   - Reference Week 5 (sensor drivers)
   - Preview Week 10 (VLA multi-modal input)

6. **Quality Check**: Run through all checklists before publishing

## Output Format

When using this skill, produce:

1. **Chapter outline** following the template
2. **Learning objectives** using Bloom's taxonomy
3. **Exercise scaffolding** with difficulty levels
4. **Cross-references** to related content
5. **Quality checklist** confirmation

---

**Remember**: Consistency is key. Every chapter should feel like part of the same course, with the same structure, tone, and quality standards. This framework ensures learners can focus on learning, not decoding different formats each week.
