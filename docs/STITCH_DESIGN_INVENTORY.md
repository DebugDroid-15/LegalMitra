# STITCH DESIGN INVENTORY & ASSET SPECIFICATION
**Project:** LegalMitra AI Chatbot  
**Stitch Project ID:** `projects/8831007758695300394`  
**Design Theme:** Constitutional Modernism  
**Primary Colours:** Deep Navy `#172B4D`, Constitutional Ivory `#FAF8F2`  
**Extracted Date:** 2026-10-16

---

## 1. Retrieved Screens

| Screen ID | Title | Device Type | Native Canvas (W x H) | Status |
|:---|:---|:---|:---|:---|
| `0c374f1959c84942af81a504339d0852` | LegalMitra — Landing Page (Constitutional Modernism) | DESKTOP | 2560 x 21770 | Full HTML & High-Res PNG Downloaded |
| `cd0e181670be4edf8672f44f197a114f` | LegalMitra — Active Legal Inquiry & Citations | DESKTOP | 2560 x 5958 | Full HTML & High-Res PNG Downloaded |
| `add712def45f44d89719fbf12bcf76fa` | LegalMitra — New Chat (Empty State) | DESKTOP | 2560 x 2400 | Full HTML & High-Res PNG Downloaded |

---

## 2. Design Tokens & Styling Architecture

### 2.1 Color Palette
- **Primary Brand Anchor (Deep Navy)**: `#172B4D` (Heading, primary navigation, solid CTA buttons, structural frames)
- **Deep Navy Dark**: `#0E1D36` / `#001637`
- **Foundational Canvas (Constitutional Ivory)**: `#FAF8F2` / `#FBF9F3` (Soft archival bond paper background, reduces eye fatigue)
- **Constitutional Ivory Dim / Borders**: `#F2EDE2` / `#E4E1D9` / `#E4E2DD`
- **Ashoka Blue (Interactive Functional Hue)**: `#244A78` / `#3C608F` (Active navigation, cross-citations, hyperlinks)
- **Muted Saffron (Precedent & Ratio Accent)**: `#D99A35` / `#C38722` (Crucial advisory warnings, ratio decidendi tags)
- **Forest Green (Statutory Validity)**: `#356B55` / `#22543D` (In-force statutes, good law badges, valid gazette pips)
- **Forest Green Background Tint**: `#EDF5F1` / `#EBF3EF`
- **Ink Black (Body Typography)**: `#20252B` / `#1B1C19`
- **Slate Grey (Secondary Metadata)**: `#687386` / `#44474E`
- **Card Surface**: `#FFFFFF` / Pure Parchment White

### 2.2 Typography
- **Headings & Brand Title**: `Manrope` (Weights: 600 SemiBold, 700 Bold, 800 ExtraBold)
- **Workhorse Body & System UI**: `Inter` (Weights: 400 Regular, 500 Medium, 600 SemiBold)
- **Judicial Quotation & Statutory Clause Accent**: `Merriweather` (Weights: 300 Light, 400 Regular, Italic)
- **Indic Script Support**: `Noto Sans Devanagari`

### 2.3 Elevation & Shadows
- **Base Canvas**: Low-contrast document styling, zero default drop-shadows.
- **Card Layer (Layer 1)**: `1px solid #E4E1D9` border with soft ambient elevation `0 1px 4px rgba(0,0,0,0.03)`.
- **Flyout / Popovers (Layer 2)**: `0 4px 16px -2px rgba(23, 43, 77, 0.08)`.
- **Modals / Dossier Drawers (Layer 3)**: `0 16px 36px -8px rgba(23, 43, 77, 0.16)`.

### 2.4 Watermarks & Emblems
- Concentric Ashoka Chakra vector line watermark (2-3% opacity, 24 traditional spokes).
- Authentic LegalMitra emblem insignia: concentric gold-accented legal pillar within a deep navy shield.

---

## 3. UI Component Inventory

1. **BrandLogo**: Deep Navy rounded glyph with concentric Ashoka rings and gold center pip, paired with Manrope bold title and uppercase subtitle.
2. **StickyHeader**: Frosted ivory backdrop (`backdrop-blur-md`), jurisdiction telemetry badge, search/export controls.
3. **ConversationSidebar (72rem / 280px)**: Collapsible navigation rail featuring New Consultation CTA, instant search, navigation groupings, categorized history (Today, Yesterday, 7 Days), and user role card.
4. **ChatComposer**: Floating bottom dock with multi-line auto-expanding field, quick suggestion chips ("Explain BNS 318", "Precedents on Anticipatory Bail"), attachment action, and keyboard shortcut telemetry.
5. **ChatMessage (User)**: Compact `#F4F1EA` parchment container with user metadata and timestamp.
6. **ChatMessage (Assistant)**: Multi-section legal intelligence dossier container:
   - Header with provision tag and temporal validity indicator.
   - Quick action controls (Copy, Bookmark, Audio, PDF Export).
   - "Short Answer" executive summary callout.
   - "Statutory Foundation" with verbatim clause in Merriweather font.
   - "Supreme Court Guiding Principles & Test" structured doctrine cards.
   - "Exceptions & Limitations" caution block.
   - "Legal Sources & Statutory Authorities" citation mosaic.
   - Statutory disclaimer footer with precision feedback thumbs.
7. **EmptyChatState**: Sovereign status pill, 2x2 domain query starter cards, and quick regulatory chips.
8. **LegalSourceCard**: Verified Act/Judgment cards with authority badges (Binding/Persuasive), commencement date, and source provenance links.

