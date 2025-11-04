---
name: high-end-design
description: Comprehensive design system for creating high-end, contextually relevant, refined designs that never look like AI slop. Use for ANY design task including websites, artifacts, documents, presentations, reports, posters, landing pages, dashboards, visualizations, or any visual output. Produces distinctive, professional designs with strong typography, thoughtful color choices, and refined aesthetics appropriate to the context.
---

# High-End Design

Create exceptional, contextually appropriate designs that avoid generic "AI slop" aesthetics. This skill transforms any design task into a refined, professional output with strong visual identity.

## Core Philosophy

**Never create generic, templated designs.** Every design should:
- Match the specific context and purpose
- Have a clear, distinctive visual identity
- Feel crafted, not generated
- Use thoughtful, intentional choices at every level

## Universal Design Principles

### 1. Typography: The Foundation

Typography is 80% of design. Get this right, everything else follows.

**NEVER use boring, default fonts:**
- ❌ Inter, Roboto, Open Sans, Lato, system fonts
- These scream "I didn't think about this"

**Use distinctive, contextually appropriate fonts:**

```
Code/Technical: JetBrains Mono, Fira Code, Space Grotesk, IBM Plex Mono
Editorial/Elegant: Playfair Display, Crimson Pro, Fraunces, Newsreader
Modern/Startup: Clash Display, Satoshi, Cabinet Grotesk, Obviously
Technical/Clean: IBM Plex family, Source Sans 3, DM Sans
Distinctive: Bricolage Grotesque, Syne, Outfit, Manrope
```

**Font pairing principles:**
- High contrast = interesting
- Display + monospace, serif + geometric sans
- Variable fonts across extreme weights
- One distinctive font used decisively > multiple mediocre fonts

**Use extremes, not midpoints:**
- Weights: 100-200 vs 800-900 (not 400 vs 600)
- Sizes: 3x+ jumps (not 1.5x)
- Example: 12px → 40px → 120px

**Always state your font choice before coding** - this forces intentionality.

### 2. Color: Context-Driven Palettes

**No generic blue-purple gradients.** Colors must serve the content.

**Selection process:**
1. What's the context? (Brand, industry, emotion, function)
2. What associations matter? (Trust, energy, calm, technical)
3. Choose a dominant color that fits
4. Build a cohesive palette around it

**Color palette principles:**
- 1 dominant color + neutral base + 1-2 accent colors
- Use color psychology: blue=trust, green=growth, orange=energy, purple=creative
- Ensure sufficient contrast for accessibility (WCAG AA minimum)
- Dark mode: don't just invert, rethink the palette

**Avoid:**
- Rainbow palettes without reason
- Neon on dark (usually)
- Pure black (#000) or pure white (#fff) - use near-blacks and off-whites

### 3. Whitespace & Hierarchy

**Generous whitespace = premium feel.** Cramped = cheap.

**Hierarchy rules:**
1. One clear focal point per section
2. Size differences should be dramatic (not subtle)
3. Use whitespace to create groups
4. Rhythm: consistent spacing patterns

**Spacing scale (use consistently):**
```
4px, 8px, 16px, 24px, 32px, 48px, 64px, 96px, 128px
```

### 4. Layout Patterns

**Break the grid (thoughtfully).**

**Strong layouts:**
- Asymmetric balance (more interesting than symmetric)
- Full-bleed images with text overlay
- Magazine-style multi-column
- Generous margins (15-20% of viewport width for premium feel)

**Weak layouts:**
- Centered columns of text
- Generic card grids without variation
- Everything the same width
- Cramped edges

### 5. Details & Polish

Small details create big impressions.

**Elevated details:**
- Subtle shadows (not harsh drop shadows)
- Micro-interactions and transitions
- Custom iconography or distinctive use of icons
- Intentional image treatments (not just raw uploads)
- Consistent border radius (pick one: 0, 4px, 8px, 16px - not random)

**Avoid:**
- Stock photo look (crop boldly, apply treatments)
- Uniform borders on everything
- Generic icons from free packs
- Arbitrary decorative elements

## Context-Specific Guidelines

### Websites & Landing Pages
- Hero section must be distinctive and clear
- CTA buttons: high contrast, bold, unmissable
- Testimonials/social proof: real-looking, not stock
- Mobile-first thinking

### Documents & Reports
- Professional typography hierarchy
- Generous margins (1.5-2 inches)
- Section breaks with visual markers
- Data visualizations with clear labels and intentional colors
- Avoid: Times New Roman, uniform text blocks

### Presentations
- One idea per slide
- Large, readable text from distance
- Minimal text, maximum impact
- Consistent but not boring template
- Avoid: bullet point walls, generic slide transitions

### Dashboards & Data Viz
- Information hierarchy: most important = most prominent
- Color coding must be consistent and meaningful
- Generous padding around data
- Clear labels, no jargon without explanation
- Avoid: rainbow charts, 3D effects, chartjunk

### Posters & Visual Content
- Bold typography as primary element
- Strong focal point
- Limited color palette (3-4 colors max)
- Negative space as active element

## Quality Checklist

Before finalizing ANY design, verify:

- [ ] Fonts: Distinctive and appropriate (not defaults)?
- [ ] Colors: Contextually meaningful (not arbitrary)?
- [ ] Hierarchy: Clear focal points and dramatic size differences?
- [ ] Whitespace: Generous and intentional?
- [ ] Details: Small touches that show care?
- [ ] Context: Actually fits the purpose and audience?
- [ ] Distinctive: Doesn't look like template or generic AI output?

## When to Read References

For deep-dives on specific design patterns and detailed examples:
- `references/design_patterns.md` - Comprehensive patterns for web, document, and visualization design with before/after examples
