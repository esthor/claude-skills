# Design Patterns Reference

Comprehensive patterns and examples for creating high-end designs across different contexts. This file provides detailed guidance with before/after comparisons and specific implementation examples.

## Web Design Patterns

### Landing Page Pattern: Editorial Style

**Concept:** Treat landing pages like magazine layouts - bold typography, generous whitespace, asymmetric composition.

**Implementation:**

```css
/* Strong typographic hierarchy */
h1 { 
  font-size: clamp(48px, 8vw, 120px);
  font-weight: 200; /* Ultra-light for impact */
  line-height: 0.95;
  letter-spacing: -0.02em;
}

h2 { 
  font-size: clamp(32px, 5vw, 72px);
  font-weight: 800; /* Ultra-bold for contrast */
}

/* Generous spacing */
section { 
  padding: clamp(80px, 12vw, 160px) clamp(24px, 5vw, 80px);
}

/* Asymmetric grid */
.hero-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr; /* Golden ratio-ish */
  gap: 48px;
}
```

**Bad Example (AI Slop):**
- Centered hero with generic image
- "Solutions" "Features" "Pricing" nav
- Blue-purple gradient buttons
- Inter font throughout
- Card grid with drop shadows

**Good Example:**
- Off-center hero with bold statement
- Magazine-style layout with varied sections
- Context-appropriate color (not random gradient)
- Distinctive font pairing (e.g., Clash Display + JetBrains Mono)
- Intentional whitespace and rhythm

### Dashboard Pattern: Information Architecture

**Concept:** Hierarchy through size, position, and color - not decoration.

**Implementation:**

```css
/* Primary metric: unmissable */
.metric-primary {
  font-size: 64px;
  font-weight: 700;
  line-height: 1;
  color: var(--text-emphasis);
}

/* Secondary metrics: supporting context */
.metric-secondary {
  font-size: 24px;
  font-weight: 500;
  color: var(--text-subdued);
}

/* Data tables: readable, not decorated */
.data-table {
  font-variant-numeric: tabular-nums; /* Aligned numbers */
  border-spacing: 0;
}

.data-table th {
  text-align: left;
  font-weight: 600;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-subdued);
  padding: 16px 24px;
}

.data-table td {
  padding: 20px 24px;
  border-top: 1px solid var(--border-subtle);
}
```

**Color coding principles:**
- Reserve bright colors for alerts/emphasis only
- Use subtle grays for most data
- Green = positive change, Red = negative, Yellow = warning (never arbitrary)
- Ensure 4.5:1 contrast ratio minimum

### Form Pattern: Thoughtful Input Design

**Concept:** Forms should feel conversational, not bureaucratic.

**Implementation:**

```css
/* Large, comfortable inputs */
input, textarea {
  font-size: 16px; /* Prevents iOS zoom */
  padding: 16px 20px;
  border: 2px solid var(--border-default);
  border-radius: 8px;
  transition: all 0.2s;
}

input:focus {
  border-color: var(--accent);
  outline: 0;
  box-shadow: 0 0 0 4px var(--accent-transparent);
}

/* Clear, helpful labels */
label {
  font-weight: 600;
  font-size: 15px;
  margin-bottom: 8px;
  display: block;
  color: var(--text-emphasis);
}

/* Inline validation with context */
.error-message {
  color: var(--error);
  font-size: 14px;
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}
```

**Bad Example:**
- Tiny inputs with minimal padding
- Harsh red errors that feel punishing
- Generic "Submit" button
- No feedback states

**Good Example:**
- Spacious, comfortable inputs
- Helpful, friendly error messages
- Specific button text ("Create Account" not "Submit")
- Clear visual feedback on interaction

## Document Design Patterns

### Report Pattern: Professional Layout

**Structure:**

```
Cover Page:
- Bold title (48-72pt)
- Subtitle/date (14-16pt)
- Generous whitespace (60% of page)

Body Pages:
- Wide margins (1.5-2 inches)
- 1.5 line spacing for body text
- Section headers in distinct weight/color
- Pull quotes or callouts for emphasis
```

**Typography for documents:**

```
Heading 1: 32-36pt, weight 700-900
Heading 2: 24-28pt, weight 600-700
Heading 3: 18-20pt, weight 600
Body: 11-12pt, weight 400, 1.5 line spacing
Caption: 9-10pt, weight 400, subdued color
```

**Layout principles:**
- Never use full page width for text (max 6.5 inches)
- Section breaks with visual markers (horizontal rules, page breaks)
- Consistent spacing (e.g., 24pt before headings, 12pt after)
- Footnotes in smaller type, clearly separated

### Presentation Pattern: Visual Communication

**Slide structure:**

```
Title Slide:
- One statement, large (80-120pt)
- Minimal supporting text
- 70% whitespace

Content Slide:
- One idea per slide
- Large text (minimum 24pt, prefer 32-48pt)
- Maximum 3-4 bullet points (or none)
- Strong visual hierarchy
```

**Bad Presentation:**
- 6-8 bullet points per slide
- 18pt text
- Every slide same template
- Generic transitions
- Reading from slides

**Good Presentation:**
- One clear point per slide
- Text large enough to read from distance
- Varied layouts based on content
- Minimal text, maximum impact
- Visuals support, don't decorate

## Data Visualization Patterns

### Chart Pattern: Clear Communication

**Bar Chart Principles:**

```css
/* Clear, readable bars */
.bar {
  fill: var(--primary);
  transition: fill 0.2s;
}

.bar:hover {
  fill: var(--primary-dark);
}

/* Readable labels */
.chart-label {
  font-size: 14px;
  font-weight: 500;
  fill: var(--text-default);
}

.chart-value {
  font-size: 16px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}
```

**Design rules:**
1. Start Y-axis at zero (unless compelling reason)
2. Use color sparingly and meaningfully
3. Direct labels > legend when possible
4. Remove chart junk (unnecessary gridlines, borders)
5. Make it readable in grayscale

**Bad Chart:**
- Rainbow colors without meaning
- 3D effects
- Unnecessary gridlines
- Tiny labels
- Requires legend to understand

**Good Chart:**
- Intentional color coding
- Flat, 2D design
- Minimal gridlines (only if needed)
- Large, readable labels
- Self-explanatory

### Table Pattern: Readable Data

**Implementation:**

```css
/* Scannable rows */
.data-table tr:nth-child(even) {
  background: var(--surface-subtle);
}

/* Aligned columns */
.data-table td {
  text-align: left;
  font-variant-numeric: tabular-nums;
}

.data-table td.numeric {
  text-align: right; /* Numbers right-aligned */
}

/* Clear headers */
.data-table thead {
  border-bottom: 2px solid var(--border-emphasis);
  font-weight: 600;
}
```

**Table design rules:**
1. Alternate row colors for scannability
2. Align numbers right, text left
3. Use monospace or tabular nums for numbers
4. Generous padding (16-24px)
5. Clear header separation

## Color System Examples

### Tech Startup Palette

```css
:root {
  --primary: #3B82F6; /* Confident blue */
  --accent: #F59E0B; /* Energy amber */
  --surface: #FFFFFF;
  --text: #1F2937;
  --text-subdued: #6B7280;
  --border: #E5E7EB;
}
```

**Usage:** Trust + innovation, clean and modern

### Creative Agency Palette

```css
:root {
  --primary: #8B5CF6; /* Creative purple */
  --accent: #EC4899; /* Bold pink */
  --surface: #FAFAF9;
  --text: #171717;
  --text-subdued: #737373;
  --border: #E7E5E4;
}
```

**Usage:** Creative energy, bold and distinctive

### Financial Services Palette

```css
:root {
  --primary: #0F766E; /* Trust teal */
  --accent: #0891B2; /* Professional cyan */
  --surface: #FFFFFF;
  --text: #0F172A;
  --text-subdued: #475569;
  --border: #CBD5E1;
}
```

**Usage:** Trust and stability, professional

### Health/Wellness Palette

```css
:root {
  --primary: #059669; /* Growth green */
  --accent: #3B82F6; /* Calm blue */
  --surface: #F8FAFC;
  --text: #1E293B;
  --text-subdued: #64748B;
  --border: #E2E8F0;
}
```

**Usage:** Health and growth, calming

## Typography Pairing Examples

### Editorial Style
```
Display: Playfair Display (weights 400, 700)
Body: Source Serif Pro (weights 400, 600)
Accent: JetBrains Mono (for data/code)
```

**Use:** Content-heavy sites, blogs, publications

### Modern Startup
```
Display: Clash Display (weights 600, 700)
Body: Inter (weights 400, 600) [Exception: paired with distinctive display]
Accent: Space Grotesk (for numbers/data)
```

**Use:** SaaS products, tech startups

### Technical/Developer
```
Display: Space Grotesk (weights 700, 900)
Body: IBM Plex Sans (weights 400, 500)
Code: JetBrains Mono (weights 400, 600)
```

**Use:** Developer tools, technical documentation

### Creative/Agency
```
Display: Cabinet Grotesk (weights 900)
Body: Obviously (weights 400, 600)
Accent: Fraunces (for emphasis)
```

**Use:** Creative agencies, portfolios

## Responsive Design Patterns

### Mobile-First Typography Scale

```css
/* Mobile base (320px+) */
:root {
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 20px;
  --text-xl: 24px;
  --text-2xl: 32px;
  --text-3xl: 40px;
}

/* Tablet (768px+) */
@media (min-width: 768px) {
  :root {
    --text-2xl: 40px;
    --text-3xl: 56px;
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  :root {
    --text-2xl: 48px;
    --text-3xl: 72px;
  }
}
```

### Responsive Spacing

```css
/* Use clamp for fluid spacing */
.section {
  padding: clamp(40px, 8vw, 120px) clamp(16px, 4vw, 80px);
}

/* Container max-widths */
.container {
  max-width: min(1200px, calc(100vw - 48px));
  margin: 0 auto;
}
```

## Anti-Patterns to Avoid

### The "Generic SaaS" Anti-Pattern
❌ Blue gradient background
❌ "Boost productivity" headline
❌ Generic illustration (people at computers)
❌ Three features in cards
❌ Purple CTA button
❌ Inter font throughout

✅ Context-specific color
✅ Specific value proposition
✅ Real product screenshots or custom visuals
✅ Varied layout, not uniform grid
✅ Distinctive typography

### The "Corporate Boring" Anti-Pattern
❌ Times New Roman
❌ Blue headers, black text only
❌ Full-justified text
❌ Clipart or generic stock photos
❌ No whitespace

✅ Modern, readable font
✅ Purposeful color hierarchy
✅ Left-aligned (easier to read)
✅ Real photos or intentional visuals
✅ Generous whitespace

### The "Over-Designed" Anti-Pattern
❌ Multiple gradients
❌ Every element has a shadow
❌ 6+ colors in palette
❌ Animations on everything
❌ Decorative elements without purpose

✅ Restrained color palette
✅ Subtle shadows where meaningful
✅ 3-4 colors maximum
✅ Purposeful micro-interactions
✅ Every element serves the design

## Quick Reference: Design Decision Tree

```
Starting a new design?
│
├─ What's the context?
│  ├─ Professional/Corporate → Clean, trustworthy colors (blue/teal), readable fonts
│  ├─ Creative/Agency → Bold colors, distinctive typography, asymmetric layouts
│  ├─ Technical/Developer → Monospace accents, technical precision, dark mode
│  └─ Consumer/Lifestyle → Warm colors, editorial style, approachable
│
├─ What's the primary goal?
│  ├─ Inform → Clear hierarchy, generous whitespace, readable typography
│  ├─ Convert → Strong CTAs, social proof, clear value prop
│  ├─ Engage → Interactive elements, varied layouts, visual interest
│  └─ Present → Large text, minimal content, strong visuals
│
└─ What's the medium?
   ├─ Web → Mobile-first, interactive, progressive disclosure
   ├─ Print → High contrast, generous margins, print-optimized
   ├─ Presentation → Large text, one idea per slide, high impact
   └─ Document → Professional hierarchy, readable body text, clear structure
```

## Implementation Checklist

Before considering any design complete:

- [ ] Typography: Distinctive font choice stated and implemented
- [ ] Typography: Extreme weight/size contrasts (not midpoint)
- [ ] Color: Contextually appropriate palette (not arbitrary)
- [ ] Color: Accessible contrast ratios (4.5:1 minimum)
- [ ] Hierarchy: Clear focal points with dramatic differences
- [ ] Whitespace: Generous padding and margins
- [ ] Layout: Intentional asymmetry or balanced symmetry (not accidental)
- [ ] Details: Consistent border radius, subtle shadows
- [ ] Responsive: Works on mobile (if web)
- [ ] Context: Actually fits the purpose and audience
- [ ] Distinctiveness: Doesn't look generic or templated
- [ ] Polish: Small details show care and intention
