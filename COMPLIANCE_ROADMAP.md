# Neurovibe Compliance Roadmap 2026

This document outlines the steps taken and future requirements for making Neurovibe a leader in neuro-inclusive digital platforms.

## Phase 1: Foundations (Completed 2026-04-06)

### WCAG 2.1 (Accessibility)
- [x] **ARIA Live Regions**: Implemented `aria-live="polite"` on the chat interface to ensure real-time screen reader announcements.
- [x] **Semantic Landmarks**: Updated `<header>`, `<main>`, `<section>`, and `<button>` usage to aid navigation.
- [x] **Focus Management**: Enhanced focus-visible states for keyboard users.
- [x] **Contrast**: Adjusted low-opacity text from 20% to 40%-60% to meet minimum contrast ratios for small/mono text.
- [x] **Labeling**: Added `aria-label` to all icon-only interactive elements (Close buttons, Send button, Menu).

### GDPR (Privacy)
- [x] **Transparency**: Added an accessible Privacy Policy modal explaining data flow.
- [x] **Consent**: Implemented a mandatory checkbox for the Beta Signup (`/api/lead`) to ensure informed consent.
- [x] **Third-Party Disclosure**: Explicitly disclosed usage of OpenAI for chat processing.
- [x] **Contact for Erasure**: Provided `simon@adviseo.se` as the contact point for Right to Erasure requests.

---

## Phase 2: Professionalization (Upcoming)

### ISO 30415:2021 (Diversity & Inclusion)
- **Goal**: Align Neurovibe with the international standard for D&I in organizations.
- **Action**: Use the "Workplace Philosophy" section to document how Neurovibe supports HR in fulfilling their D&I obligations.

### ISO 27001 (Information Security)
- **Goal**: Secure enterprise-level contracts.
- **Action**: Implement formal risk assessment for how NPF/Health data is stored in PostgreSQL.

### MDR (Medical Device Regulation)
- **Monitoring**: Ensure Neurovibe remains a "wellness/productivity" tool. If we introduce diagnostic features (e.g., "This pattern suggests ADHD"), we must register as a Class I/IIa Medical Device under EU MDR.

---

## Technical Notes
- **Hosting**: Managed via Railway (TLS/HTTPS enabled by default).
- **Database**: PostgreSQL (Adviseo MCC setup).
- **AI**: GPT-4o-mini (via OpenAI API).
