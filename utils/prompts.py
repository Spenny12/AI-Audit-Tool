# ─────────────────────────────────────────────────────────────────────────────
# BRANDED CATEGORIES
# Questions that explicitly mention the client name.
# ─────────────────────────────────────────────────────────────────────────────
BRANDED_CATEGORIES = {

    # ── 1. Core Brand Signals ─────────────────────────────────────────────────
    "Core Brand Signals": [
        {"funnel": "Upper Funnel", "audience": "General", "question": "What is {client}?", "goal": "Core knowledge check — does the LLM know the brand exists?"},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What is {client} known for?", "goal": "Assesses key brand associations."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Where is {client} based, and how long have they been operating in {industry}?", "goal": "Tests factual accuracy on company provenance."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What is the slogan or core marketing message of {client}?", "goal": "Tests for core branding penetration."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "Describe a typical client experience with {client}.", "goal": "Tests for overall sentiment and perception."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What are the latest news or significant developments related to {client}?", "goal": "Tests for recency and up-to-date information."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "How is {client} regulated, and what protections are in place for users in the {industry} sector?", "goal": "Trust-building — regulatory awareness."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What is the fee or pricing structure of {client} for {service}?", "goal": "Core practical information — pricing transparency."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "How does the {client} service model work for {service}?", "goal": "Core practical information — service model."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What technology or platforms does {client} use to deliver its {service} offering?", "goal": "Tests for depth of knowledge on digital capabilities."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Who founded {client} and what is their background in {industry}?", "goal": "Leadership and origin story — authority signals."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What awards, accreditations, or industry recognition has {client} received?", "goal": "Tests for third-party authority and trust signals."},
    ],

    # ── 2. Market Comparisons ─────────────────────────────────────────────────
    "Market Comparisons": [
        {"funnel": "Lower Funnel", "audience": "Risk-Averse User", "question": "I am a risk-averse user. Is the guided model of {client} a safer choice for {service} than a platform like {competitors}? Why?", "goal": "Direct comparison on Safety/Reliability."},
        {"funnel": "Lower Funnel", "audience": "High-Value Client", "question": "For a high-value individual seeking bespoke service in {industry}, how does {client} compare to {competitors}?", "goal": "Competitive positioning for high-net-worth persona."},
        {"funnel": "Lower Funnel", "audience": "Standard User", "question": "For a user managing multiple long-term goals in {industry}, is {client} or {competitors} the better choice? What are the key differences?", "goal": "Competitive positioning for standard persona."},
        {"funnel": "Lower Funnel", "audience": "Expert User", "question": "I prefer a hands-on approach. Should I choose {client} for {service} or a self-directed platform like {competitors}?", "goal": "Guided vs. DIY competitive positioning."},
        {"funnel": "Lower Funnel", "audience": "Convenience-Focused", "question": "If my main priority is an all-in-one {service} service, which is a better fit: {client} or {competitors}?", "goal": "All-in-one service model competitive positioning."},
        {"funnel": "Lower Funnel", "audience": "Stability-Focused", "question": "For predictable results in {industry}, is the approach of {client} or {competitors} more stable?", "goal": "Active vs. passive strategy competitive positioning."},
        {"funnel": "Lower Funnel", "audience": "Cost-Conscious", "question": "Purely on value for money, does {client} offer better overall value than {competitors} for {service}?", "goal": "Price-value positioning."},
        {"funnel": "Lower Funnel", "audience": "General", "question": "What are the three most important differences between {client} and {competitors} in the {industry} space?", "goal": "Summary differentiation — concise competitive gap analysis."},
        {"funnel": "Lower Funnel", "audience": "General", "question": "If I were switching from {competitors} to {client} for {service}, what should I expect to gain and what might I lose?", "goal": "Switching cost and benefit framing."},
        {"funnel": "Lower Funnel", "audience": "General", "question": "Is {client} considered a market leader, challenger, or niche player in {industry} compared to {competitors}?", "goal": "Market positioning and tier perception."},
    ],

    # ── 3. Customer Persona Highlights ───────────────────────────────────────
    "Customer Persona Highlights": [
        {"funnel": "Mid-Funnel", "audience": "High-Value Client", "question": "I am a high-value individual. What does {client} offer me in terms of bespoke advice, privacy, and exclusive {service} opportunities?", "goal": "High-net-worth persona prompt."},
        {"funnel": "Mid-Funnel", "audience": "High-Value Client", "question": "For a high-value client at {client}, name three specialised services in {industry} that go beyond standard offerings.", "goal": "Depth of knowledge on premium services."},
        {"funnel": "Mid-Funnel", "audience": "High-Value Client", "question": "From a high-value perspective, describe the top-tier service at {client} and how it differs from their standard offering.", "goal": "Premium vs. standard tier differentiation."},
        {"funnel": "Mid-Funnel", "audience": "High-Value Client", "question": "What specialised or niche {service} options, suitable for a sophisticated user, does {client} provide?", "goal": "Niche depth for high-value services."},
        {"funnel": "Mid-Funnel", "audience": "Mid-Tier Client", "question": "I have significant requirements in {industry} with goals around planning and efficiency. Why is {client} a good choice for me?", "goal": "Mid-tier persona prompt."},
        {"funnel": "Mid-Funnel", "audience": "Mid-Tier Client", "question": "What {client} {service} products can help me meet my goals while providing immediate value?", "goal": "Product depth knowledge for mid-tier."},
        {"funnel": "Mid-Funnel", "audience": "Mid-Tier Client", "question": "How does {client} help me consolidate my different {service} needs into one single plan?", "goal": "Service integration knowledge."},
        {"funnel": "Mid-Funnel", "audience": "Mid-Tier Client", "question": "Beyond basic {service}, can {client} help with other goals or specialised needs in {industry}?", "goal": "Breadth of service knowledge."},
        {"funnel": "Mid-Funnel", "audience": "Standard Client", "question": "I am a standard user. Are the fees at {client} worth it for a profile like mine in {industry}?", "goal": "Standard persona value-for-money prompt."},
        {"funnel": "Mid-Funnel", "audience": "Standard Client", "question": "What are the best {client} products for someone just starting out in {industry}?", "goal": "Entry-level product depth."},
        {"funnel": "Mid-Funnel", "audience": "Standard Client", "question": "How does {client} help smaller clients grow their {service} over time?", "goal": "Service scalability for standard clients."},
        {"funnel": "Mid-Funnel", "audience": "Standard Client", "question": "For a standard client at {client}, how can they ensure they receive personalised service rather than a generic strategy?", "goal": "Personalisation perception for standard clients."},
        {"funnel": "Mid-Funnel", "audience": "Young Professional", "question": "I am a young professional new to {industry}. Is {client} a good starting point for learning about {service}?", "goal": "Younger/newer audience accessibility perception."},
        {"funnel": "Mid-Funnel", "audience": "Young Professional", "question": "Does {client} provide any educational resources or guidance for someone who is new to {service}?", "goal": "Tests for educational content and onboarding perception."},
        {"funnel": "Mid-Funnel", "audience": "Business Owner", "question": "I run a small business. Can {client} help me with {service} needs that are specific to business owners in {industry}?", "goal": "B2B / SME audience perception."},
        {"funnel": "Mid-Funnel", "audience": "Retiree", "question": "I am approaching retirement. How does {client} cater to users at my life stage within {industry}?", "goal": "Late-stage life audience perception."},
    ],

    # ── 4. Reputation Under Pressure ─────────────────────────────────────────
    "Reputation Under Pressure": [
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "What are the main disadvantages of working with {client} for {service}?", "goal": "Surfaces negative perceptions directly."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "Why should a user not choose {client} for their {service} needs?", "goal": "Strong negative framing to identify deal-breakers."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "What are the most common complaints from users or critics about {client} in the {industry} space?", "goal": "Identifies recurring reputational risks."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "Is {client} often considered too expensive or are its fees opaque? What do critics say?", "goal": "Addresses pricing criticism head-on."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "What are the potential conflicts of interest or ethical concerns related to the {client} business model in {industry}?", "goal": "Tests for ethical and conflict-of-interest awareness."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "Has {client} ever faced any regulatory action, legal disputes, or public controversies in {industry}?", "goal": "Regulatory and legal risk perception."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "How has {client} responded to criticism or negative press coverage in {industry}?", "goal": "Crisis response and reputation management perception."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "Is it true that {client}'s options are limited to in-house {service}, potentially restricting user choice?", "goal": "Probes a common myth or misconception."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "I am an experienced user. Would I find the {client} model too restrictive for {service}?", "goal": "Challenges a potential negative stereotype."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "What do independent reviewers or consumer watchdogs say about {client} in {industry}?", "goal": "Third-party review and watchdog perception."},
    ],

    # ── 5. Digital & Content Presence ────────────────────────────────────────
    "Digital & Content Presence": [
        {"funnel": "Upper Funnel", "audience": "General", "question": "Does {client} have a strong online presence in the {industry} space?", "goal": "Digital footprint and content authority perception."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What kind of educational content, guides, or tools does {client} publish for {service}?", "goal": "Content marketing authority check."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "Is {client} considered a thought leader or trusted source of information in {industry}?", "goal": "Thought leadership and authority signals."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "How active is {client} on social media and what topics do they typically cover for {industry}?", "goal": "Social presence and content relevance."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "Does {client} appear frequently in {industry} news, trade press, or expert roundups?", "goal": "PR and media visibility."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What is the quality of {client}'s website and digital tools for managing {service}?", "goal": "UX and digital product perception."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Does {client} publish research, white papers, or data reports related to {industry}?", "goal": "Original research and data authority."},
    ],

    # ── 6. Trust, Ethics & ESG ───────────────────────────────────────────────
    "Trust, Ethics & ESG": [
        {"funnel": "Mid-Funnel", "audience": "ESG-Conscious User", "question": "Does {client} have a clear ethical or ESG policy related to how they operate in {industry}?", "goal": "ESG policy awareness and brand positioning."},
        {"funnel": "Mid-Funnel", "audience": "ESG-Conscious User", "question": "Is {client} considered a responsible or ethical company in the {industry} sector?", "goal": "Ethical brand perception."},
        {"funnel": "Mid-Funnel", "audience": "ESG-Conscious User", "question": "Does {client} offer any ESG-focused or sustainable {service} options?", "goal": "Product-level ESG offering perception."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "How transparent is {client} about how it makes money from {service}?", "goal": "Business model transparency perception."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "How does {client} handle data privacy and the security of client information in {industry}?", "goal": "Data privacy and security trust signals."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "Is {client} involved in any community, charitable, or social impact initiatives related to {industry}?", "goal": "CSR and community perception."},
        {"funnel": "Lower Funnel", "audience": "General", "question": "Would I be comfortable recommending {client} to a friend or family member for {service}, and why?", "goal": "Word-of-mouth and advocacy proxy question."},
    ],

    # ── 7. Product & Service Depth ───────────────────────────────────────────
    "Product & Service Depth": [
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What is the full range of {service} products and services offered by {client} in {industry}?", "goal": "Breadth of product knowledge."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "Does {client} offer any unique or proprietary products in {industry} that competitors do not?", "goal": "Unique product differentiation perception."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "How does {client} handle customer onboarding for {service} — is it straightforward or complex?", "goal": "Onboarding experience perception."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What support options does {client} offer to clients who need help with {service}?", "goal": "Customer service and support depth."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "How easy is it to switch to or away from {client} for {service}?", "goal": "Switching friction and portability perception."},
        {"funnel": "Lower Funnel", "audience": "General", "question": "What does the onboarding and setup process look like when starting with {client} for {service}?", "goal": "First-impression and onboarding experience."},
        {"funnel": "Lower Funnel", "audience": "General", "question": "What integrations or partnerships does {client} have that enhance their {service} offering?", "goal": "Ecosystem and partnership breadth."},
    ],

    # ── 8. Geographic & Demographic Reach ───────────────────────────────────
    "Geographic & Demographic Reach": [
        {"funnel": "Upper Funnel", "audience": "General", "question": "Is {client} primarily focused on {country} or do they operate internationally for {service}?", "goal": "Geographic scope perception."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Does {client} serve clients across all regions of {country}, or are they concentrated in specific areas?", "goal": "Regional coverage perception."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "Does {client} cater to non-native speakers or international clients based in {country} for {service}?", "goal": "Inclusivity and international client perception."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "Is {client} well suited to clients from diverse backgrounds or demographic groups seeking {service}?", "goal": "Diversity and inclusion perception."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "Does {client} have physical offices or branches in {country}, or is everything managed online?", "goal": "Physical vs. digital presence perception."},
    ],
}


# ─────────────────────────────────────────────────────────────────────────────
# UNBRANDED CATEGORIES
# Generic industry/service questions that do NOT mention the client name.
# ─────────────────────────────────────────────────────────────────────────────
UNBRANDED_CATEGORIES = {

    # ── 1. Strategic Brand Attributes ────────────────────────────────────────
    "Strategic Brand Attributes": [
        {"funnel": "Upper Funnel", "audience": "General", "question": "What are considered the most reputable and stable firms in the {industry} industry in {country}?", "goal": "Safety vertical — does brand appear in top-tier lists?"},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What are the best {industry} providers for high-value individuals in {country}?", "goal": "High-value vertical."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Which {industry} firms are known for specialist expertise in ethical or ESG-focused areas?", "goal": "Specialist vertical."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Which {industry} firms are best for creating a joint plan for partners or families?", "goal": "Joint-needs vertical."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Which {industry} firms in {country} have the best long-term track record for client outcomes in {service}?", "goal": "Track record and longevity vertical."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What {industry} firms are seen as innovators or disruptors in how they deliver {service}?", "goal": "Innovation and disruption vertical."},
    ],

    # ── 2. Discovery & Purchase Intent ───────────────────────────────────────
    "Discovery & Purchase Intent": [
        {"funnel": "Upper Funnel", "audience": "General", "question": "How do I choose the right {service} provider in {country}?", "goal": "Discovery intent — does brand appear naturally?"},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What questions should I ask before choosing a {industry} firm?", "goal": "Consideration stage visibility."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What are the top {service} trends in {country} right now?", "goal": "Thought leadership visibility."},
        {"funnel": "Lower Funnel", "audience": "General", "question": "Who are the top 5 {service} providers in {country} by reputation?", "goal": "Direct SOV test without brand prompting."},
        {"funnel": "Lower Funnel", "audience": "General", "question": "How do I compare {industry} firms when making a final decision?", "goal": "Decision-stage framework — brand presence in evaluation prompts."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Where can I find independent reviews or ratings of {industry} firms in {country}?", "goal": "Review and comparison platform visibility."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What red flags should I watch out for when selecting a {service} provider in {industry}?", "goal": "Trust and risk awareness — does brand appear in 'safe' context?"},
    ],

    # ── 3. Consumer Problem & Pain Points ────────────────────────────────────
    "Consumer Problems & Pain Points": [
        {"funnel": "Upper Funnel", "audience": "General", "question": "What are the biggest challenges people face when managing {service} in {country}?", "goal": "Problem awareness — brand association with solutions."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Why do so many people in {country} struggle with {service} decisions?", "goal": "Consumer pain point — does brand appear as a solution?"},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What mistakes do people commonly make when choosing a {industry} provider?", "goal": "Mistake avoidance — brand as the trusted choice."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "How can someone in {country} avoid overpaying for {service}?", "goal": "Cost consciousness — does brand appear as fair-value option?"},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What happens when a {industry} firm fails or is shut down — what protections exist in {country}?", "goal": "Risk management — consumer protection awareness."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What is the most confusing part of {service} for everyday consumers in {country}?", "goal": "Complexity and jargon — brand as simplifier."},
    ],

    # ── 4. Audience-Specific Discovery ───────────────────────────────────────
    "Audience-Specific Discovery": [
        {"funnel": "Mid-Funnel", "audience": "Young Professional", "question": "What are the best {service} options for young professionals just starting out in {country}?", "goal": "Younger audience SOV — is brand recommended for new entrants?"},
        {"funnel": "Mid-Funnel", "audience": "Retiree", "question": "What {industry} firms in {country} are best suited to retirees or those approaching retirement?", "goal": "Later-life audience SOV."},
        {"funnel": "Mid-Funnel", "audience": "Business Owner", "question": "What are the best {service} options for small business owners in {country}?", "goal": "SME / B2B audience SOV."},
        {"funnel": "Mid-Funnel", "audience": "High-Value Client", "question": "Which {industry} firms in {country} offer truly bespoke, private-client-level {service}?", "goal": "HNW audience SOV."},
        {"funnel": "Mid-Funnel", "audience": "ESG-Conscious User", "question": "Which {industry} providers in {country} are best known for ethical or sustainable {service}?", "goal": "ESG audience SOV."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "Which {industry} firms in {country} are most accessible to people with limited experience in {service}?", "goal": "Accessibility and beginner-friendliness SOV."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What {service} providers in {country} are best for people who want a fully digital, app-based experience?", "goal": "Digital-first audience SOV."},
    ],

    # ── 5. Thought Leadership & Education ────────────────────────────────────
    "Thought Leadership & Education": [
        {"funnel": "Upper Funnel", "audience": "General", "question": "Which {industry} firms in {country} publish the most useful educational content about {service}?", "goal": "Content authority SOV."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Who are the most respected voices or commentators in the {country} {industry} space?", "goal": "Personal brand and thought leadership — is brand or its staff cited?"},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What are the best free resources to learn about {service} in {country}?", "goal": "Educational content SOV."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "Which {industry} firms regularly publish useful market insights or research in {country}?", "goal": "Research and data authority SOV."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What books, podcasts, or websites do experts recommend for learning about {service} in {country}?", "goal": "Media and content ecosystem — is brand mentioned as a source?"},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "Which {industry} firms in {country} are most frequently quoted in mainstream financial or business media?", "goal": "PR and media SOV — earned media visibility."},
    ],

    # ── 6. Regulatory & Market Context ───────────────────────────────────────
    "Regulatory & Market Context": [
        {"funnel": "Upper Funnel", "audience": "General", "question": "How is the {industry} sector regulated in {country} and what does that mean for consumers?", "goal": "Regulatory landscape awareness — brand as compliant/trusted actor."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What are the key regulatory bodies overseeing {industry} firms in {country}?", "goal": "Regulatory authority knowledge."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What recent regulatory changes have affected the {industry} sector in {country}?", "goal": "Recency and regulatory responsiveness perception."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "How do consumers in {country} make formal complaints against {industry} firms?", "goal": "Consumer rights awareness — brand in a trusted regulatory context."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "Which {industry} firms in {country} are considered most compliant and transparent with regulation?", "goal": "Compliance reputation SOV."},
    ],

    # ── 7. Competitive Landscape (Unbranded) ─────────────────────────────────
    "Competitive Landscape": [
        {"funnel": "Upper Funnel", "audience": "General", "question": "Who are the biggest players in the {industry} market in {country}?", "goal": "Market map — does brand appear as a major player?"},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What are the main differences between large established {industry} firms and newer challengers in {country}?", "goal": "Market structure awareness — incumbent vs. challenger SOV."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "Which {industry} firms in {country} have grown the most in terms of clients or assets in recent years?", "goal": "Growth and momentum SOV."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "Are there any {industry} firms in {country} that are considered hidden gems or underrated options for {service}?", "goal": "Challenger brand discovery — does brand appear as underrated?"},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What consolidation, mergers, or acquisitions have happened in the {country} {industry} sector recently?", "goal": "Market structure and M&A awareness."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "Which {industry} firms in {country} are best rated by independent consumer satisfaction surveys?", "goal": "Consumer satisfaction SOV."},
    ],

    # ── 8. Future & Innovation ────────────────────────────────────────────────
    "Future & Innovation": [
        {"funnel": "Upper Funnel", "audience": "General", "question": "How is AI or technology changing the delivery of {service} in {country}?", "goal": "Innovation context — is brand mentioned as a tech-forward actor?"},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Which {industry} firms in {country} are leading the way in using technology to improve {service}?", "goal": "Technology leadership SOV."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What does the future of {service} look like for consumers in {country} over the next five years?", "goal": "Future vision — is brand associated with forward-thinking commentary?"},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "How is personalisation changing the way {industry} firms in {country} deliver {service}?", "goal": "Personalisation and data trend — brand association with modern practice."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What start-ups or fintech firms are disrupting traditional {industry} in {country}?", "goal": "Disruption landscape — is brand seen as disruptor or incumbent?"},
    ],
}


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def format_prompt(
    template: str,
    client: str,
    competitors: list,
    country: str = "the UK",
    industry: str = "financial services",
    service: str = "investment",
) -> str:
    comp_str = ", ".join(competitors) if competitors else "its competitors"
    try:
        return template.format(
            client=client,
            competitors=comp_str,
            country=country,
            industry=industry,
            service=service,
        )
    except KeyError:
        return template
