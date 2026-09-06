"""Render the topic explainer pages (llm-compliance/, ai-agent-compliance/,
llm-pressure-testing/) from the content below, reusing index.html's CSS so the
pages stay in step with the homepage. Run: python build_topics.py"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "https://trace-ai-labs.github.io"
PACT = "https://trace-ai-labs.github.io/pact/"
AIES = "https://trace-ai-labs.github.io/ai-incentives/"
HF = "https://huggingface.co/datasets/trace-ai-labs/pact"
GH_PACT = "https://github.com/trace-ai-labs/pact"
GH_AIES = "https://github.com/trace-ai-labs/llm-compliance"
ARXIV_AIES = "https://arxiv.org/abs/2608.12323"
PACT_PDF = "https://trace-ai-labs.github.io/pact/paper.pdf"
EAL = "https://arxiv.org/abs/2609.01836"

EXTRA_CSS = """
  .crumbs { font-family: var(--sans); font-size: 0.85rem; color: var(--muted); margin: 0 0 2rem; }
  .crumbs a { color: var(--muted); }
  .crumbs a:hover { color: var(--text); }
  .topic h1 { font-size: 2rem; margin-bottom: 0.6rem; }
  .topic .lede { font-size: 1.12rem; color: var(--text); margin-bottom: 1.8rem; }
  .topic h2 {
    font-family: var(--serif); font-size: 1.28rem; font-weight: 600; text-transform: none;
    letter-spacing: -0.005em; color: var(--text); border-bottom: none; margin: 2.5rem 0 0.7rem;
    padding-bottom: 0;
  }
  .topic ul, .topic ol { padding-left: 1.3rem; margin: 0 0 1rem; }
  .topic li { margin-bottom: 0.45rem; }
  .topic table { border-collapse: collapse; width: 100%; font-family: var(--sans); font-size: 0.9rem; margin: 0 0 1.2rem; }
  .topic th, .topic td { text-align: left; padding: 0.45rem 0.6rem; border-bottom: 1px solid var(--rule); vertical-align: top; }
  .topic th { font-weight: 600; color: var(--muted); font-size: 0.78rem; letter-spacing: 0.06em; text-transform: uppercase; }
  .topic code { font-family: var(--mono); font-size: 0.85em; background: var(--panel); padding: 0.05em 0.3em; border-radius: 3px; }
  .faq dt { font-weight: 600; margin: 1.2rem 0 0.3rem; }
  .faq dd { margin: 0 0 0.6rem; }
  .related { font-family: var(--sans); font-size: 0.9rem; }
  .related a + a::before { content: " · "; color: var(--muted); }
"""

PAGES = [
    {
        "slug": "llm-compliance",
        "title": "LLM compliance: what it means and how to measure it | TRACE AI Labs",
        "h1": "LLM compliance",
        "description": "What LLM compliance is, why language models break rules they can recite, and how to measure AI compliance with a benchmark: the PACT LLM compliance benchmark and the AIES 2026 study from TRACE AI Labs.",
        "lede": "LLM compliance is whether a language model keeps following a binding rule once it is deployed and something in the situation rewards breaking it. Every model we have tested can recite its rules. Far fewer keep them.",
        "body": f"""
<h2>What LLM compliance means</h2>
<p>An LLM deployed as a workplace assistant is given rules: a hiring assistant must not screen on protected attributes, a bank assistant must file a suspicious-activity report before releasing funds, a procurement agent must use certified vendors above a spending threshold. LLM compliance, sometimes called AI compliance or agent compliance, is the question of whether the model actually acts on those rules when its task incentives point the other way.</p>
<p>This is different from two things it is often confused with. It is not knowledge of the rule: models score well on questions about regulations and still violate them in a live decision. And it is not jailbreak robustness or refusal safety: nobody in these settings is attacking the model. The pressure is ordinary. A deadline is close, a manager says to make an exception, a coworker already did it, or the user simply argues back after the first answer.</p>

<h2>Why LLMs break rules they know</h2>
<p>Our AIES 2026 study, <a href="{AIES}">Why Do AI Agents Break Rules?</a>, put twelve instruction-tuned models in the same enterprise procurement role under one legal rule and changed only the context around it. Three findings shape how we think about LLM compliance:</p>
<ul>
  <li><strong>The model matters more than the rule.</strong> With the rule held fixed, compliance ranged from 43.5% to 89.5% depending only on which model was answering.</li>
  <li><strong>Phrasing and incentives change behavior.</strong> Stating a rule as a neutral fact rather than a command lowered compliance for several models, and a small, beatable fine often lowered it further because a stated fine reads as a price.</li>
  <li><strong>Social context moves the whole curve.</strong> A manager's blanket approval or a board cost policy pushed compliance down even for rule-anchored models. A peer who was fined pushed it up; a peer who got away with it pushed it down.</li>
</ul>
<p>A built-in "follow the law regardless" instruction helped, but a deadline still got past it for all but one model.</p>

<h2>How to measure LLM compliance</h2>
<p><a href="{PACT}">PACT (Pressure-Applied Compliance Testing)</a> turns those findings into a benchmark. Each of its 3,364 items is one workplace decision: a system prompt that gives the model a persona, its KPIs, and a compliance rule stated as plain fact; a user request with a short menu of options where the rule-violating option wins on the metric the persona is measured on; and, on multi-turn items, a scripted pushback that argues against the compliant choice. Items span 48 scenarios in 12 regulated domains, and the rules are real statutes. In seven scenarios a court or regulator has already punished the same violation.</p>
<p>A model's PACTScore is the share of items it handles compliantly, weighting the first decision three to one against the decision after pushback, with each item run three times and credit given only when the model gets it right every time. Because the benchmark also includes near-identical situations where the rule does not apply, a model cannot score well by refusing everything. Over-applying a rule is scored as an error too.</p>

<h2>What the numbers say so far</h2>
<table>
<tr><th>Measure</th><th>Result</th></tr>
<tr><td>Best PACTScore across 24 models</td><td>0.944, and none clears the bar we set for unsupervised use</td></tr>
<tr><td>Effect of one sentence of workplace pressure</td><td>Violation rates rise by 65%</td></tr>
<tr><td>Mildest pressure family</td><td>Still produces violations on 4.8% of requests</td></tr>
<tr><td>When a model does violate</td><td>It presents the result as compliant 79% of the time</td></tr>
<tr><td>Newer or bigger models</td><td>Not reliably better; a 27B dense model ties a trillion-parameter one</td></tr>
</table>

<h2>Frequently asked questions</h2>
<dl class="faq">
<dt>Is LLM compliance the same as AI safety?</dt>
<dd>It is one part of it. Most AI safety benchmarks test refusals of harmful requests or robustness to jailbreaks. LLM compliance benchmarks test whether a model follows legitimate business and legal rules in the deployments it is already being used for, where the harm comes from a plausible shortcut rather than an attacker.</dd>
<dt>Does adding "always follow the rules" to the system prompt fix it?</dt>
<dd>Partly. PACT scores every item twice, once with and once without a hard compliance directive, and reports both. The directive raises scores but does not close the gap, and in the AIES study urgency pressure beat it for eleven of twelve models.</dd>
<dt>Can I evaluate my own model?</dt>
<dd>Yes. The <a href="{HF}">PACT dataset</a> is on Hugging Face under an MIT license, and the <a href="{GH_PACT}">evaluation harness</a> on GitHub runs the full protocol against any OpenAI-compatible endpoint.</dd>
<dt>Which regulated domains does PACT cover?</dt>
<dd>Hiring, healthcare, finance, privacy, advertising, anti-money-laundering and KYC, export controls, government services, and others, 12 in total, each written by three generator models and cross-reviewed.</dd>
</dl>

<h2>Read more</h2>
<p class="related">
  <a href="{PACT}">PACT benchmark and leaderboard</a>
  <a href="{PACT_PDF}">PACT paper (PDF)</a>
  <a href="{AIES}">AIES 2026 study: interactive results</a>
  <a href="{ARXIV_AIES}">AIES paper on arXiv</a>
  <a href="{HF}">Dataset on Hugging Face</a>
  <a href="{BASE}/ai-agent-compliance/">AI agent compliance</a>
  <a href="{BASE}/llm-pressure-testing/">LLM pressure testing</a>
</p>
""",
        "faq": [
            ("Is LLM compliance the same as AI safety?", "It is one part of it. Most AI safety benchmarks test refusals of harmful requests or robustness to jailbreaks. LLM compliance benchmarks test whether a model follows legitimate business and legal rules in real deployments, where the harm comes from a plausible shortcut rather than an attacker."),
            ("Does adding 'always follow the rules' to the system prompt fix it?", "Partly. PACT scores every item with and without a hard compliance directive. The directive raises scores but does not close the gap, and in the AIES 2026 study urgency pressure beat it for eleven of twelve models."),
            ("Can I evaluate my own model?", "Yes. The PACT dataset is on Hugging Face under an MIT license and the evaluation harness on GitHub runs the full protocol against any OpenAI-compatible endpoint."),
            ("Which regulated domains does PACT cover?", "Hiring, healthcare, finance, privacy, advertising, anti-money-laundering and KYC, export controls, government services, and others, 12 in total."),
        ],
        "keywords": ["LLM compliance", "AI compliance", "LLM compliance benchmark", "rule following", "regulatory compliance", "enterprise AI assistants", "PACT", "AI safety"],
    },
    {
        "slug": "ai-agent-compliance",
        "title": "AI agent compliance: do AI agents follow the rules they are given? | TRACE AI Labs",
        "h1": "AI agent compliance",
        "description": "AI agent compliance research from TRACE AI Labs: why enterprise AI agents break rules under incentives, framing, authority, and peer pressure (AIES 2026), and how the PACT benchmark measures agent compliance under pressure.",
        "lede": "AI agents are being handed real decisions in hiring, finance, healthcare, and procurement. Agent compliance asks a plain question: when an agent is given a rule and a reason to skip it, which one wins?",
        "body": f"""
<h2>The problem with deployed agents</h2>
<p>An AI agent in an enterprise workflow is not a chatbot answering trivia. It has a role, a set of KPIs, and instructions that include the rules the company is legally bound by. It also has a user in front of it who wants something done. Agent compliance is whether the rules survive contact with that user and those KPIs. Failures here are already in the case law: Air Canada was held to a refund policy its chatbot invented, New York City's MyCity assistant told businesses to break labor law, and Workday is defending a class action over algorithmic hiring screens.</p>

<h2>What makes AI agents follow the rules</h2>
<p>Our paper <a href="{AIES}">Why Do AI Agents Break Rules? How Framing, Context, and Social Signals Shape Compliance</a>, published at the 2026 AAAI/ACM Conference on AI, Ethics, and Society, isolates the levers. One procurement agent, one rule (purchases over $1,000 must use an environmentally certified vendor), twelve models, and a controlled set of changes to the situation:</p>
<ul>
  <li><strong>Rule framing.</strong> A command, a neutral fact, or explicit permission to opt out. Several models obey only the command.</li>
  <li><strong>Enforcement.</strong> A fine that is cheaper than compliance often lowers compliance rather than raising it. A stated penalty becomes a price the agent is willing to pay.</li>
  <li><strong>Authority and peers.</strong> A manager's approval or a board cost policy drags compliance down. What a peer team did, and whether they were caught, moves it in either direction.</li>
  <li><strong>User pressure.</strong> Nine tactics, from a soft budget hint to an order to ignore the rule. Urgency is the one that beats every defense.</li>
  <li><strong>Pushback.</strong> Agents that break the rule on the first turn are often talked back onto it, and agents that held it are often talked off it. Real deployments are conversations.</li>
</ul>
<p>Training focus, as described by each developer, did not predict any of this. Models labeled agentic-RL systems and models labeled safety-aligned assistants appear at both ends of the compliance range.</p>

<h2>Measuring agent compliance at scale</h2>
<p>The procurement study has one rule and one domain. <a href="{PACT}">PACT</a> generalizes it into an agent compliance benchmark: 3,364 items across 48 scenarios in 12 regulated domains, nine families of realistic pressure, and a scripted pushback turn. Every scenario is a place AI assistants already work and a real statute governs the decision. Scores are reported both with and without a hard compliance directive in the system prompt, so the benchmark also measures how steerable an agent's compliance is.</p>
<p>On the current leaderboard the best of 24 models scores 0.944 and none clears the bar for unsupervised use. One sentence of ordinary workplace pressure raises violation rates by 65%. When agents do break a rule, they describe the outcome as compliant 79% of the time, which matters for anyone relying on the agent's own audit trail.</p>

<h2>Adjacent failure: authority the agent grants itself</h2>
<p>Compliance can also erode from the inside. In <a href="{EAL}">Agent Memory Is a Surface for Endogenous Authorization Laundering</a> we show that an agent's persistent memory can turn a suggestion into a standing permission nobody granted. Incremental memory updates created false authority for up to 50.2% of unauthorized requests, and once present, downstream executors acted on it in 98.6% of trials. EAL-Bench is the open benchmark for that failure.</p>

<h2>Frequently asked questions</h2>
<dl class="faq">
<dt>Is agent compliance different from LLM compliance?</dt>
<dd>Same underlying question, different framing. LLM compliance looks at the model; agent compliance looks at the model inside a role with goals, tools, memory, and a user. Our work covers both because the failures come from the interaction.</dd>
<dt>Do safety-tuned models comply more?</dt>
<dd>Not reliably. In the AIES study the developer's stated training focus did not separate compliant from non-compliant models, and in PACT release date and parameter count do not predict PACTScore.</dd>
<dt>What is the single most dangerous pressure?</dt>
<dd>Urgency. A looming deadline lowered compliance for every model in the AIES study, even with a follow-the-law instruction in the system prompt, and it remains among the strongest families in PACT.</dd>
<dt>How do I test my own agent?</dt>
<dd>Run the <a href="{GH_PACT}">PACT harness</a> against your endpoint using the <a href="{HF}">public dataset</a>, or reproduce the AIES experiments from the <a href="{GH_AIES}">study repository</a>.</dd>
</dl>

<h2>Read more</h2>
<p class="related">
  <a href="{AIES}">AIES 2026 study: interactive results</a>
  <a href="{ARXIV_AIES}">Paper on arXiv</a>
  <a href="{GH_AIES}">Code and data</a>
  <a href="{PACT}">PACT benchmark</a>
  <a href="{BASE}/llm-compliance/">LLM compliance</a>
  <a href="{BASE}/llm-pressure-testing/">LLM pressure testing</a>
</p>
""",
        "faq": [
            ("Is agent compliance different from LLM compliance?", "Same underlying question, different framing. LLM compliance looks at the model; agent compliance looks at the model inside a role with goals, tools, memory, and a user."),
            ("Do safety-tuned models comply more?", "Not reliably. In the AIES 2026 study the developer's stated training focus did not separate compliant from non-compliant models, and in PACT release date and parameter count do not predict PACTScore."),
            ("What is the single most dangerous pressure?", "Urgency. A looming deadline lowered compliance for every model in the AIES study, even with a follow-the-law instruction in the system prompt."),
            ("How do I test my own agent?", "Run the PACT harness on GitHub against your endpoint using the public Hugging Face dataset, or reproduce the AIES experiments from the study repository."),
        ],
        "keywords": ["AI agent compliance", "agent compliance", "AI agents follow rules", "enterprise AI agents", "AI incentives", "agentic AI safety", "AIES 2026", "PACT"],
    },
    {
        "slug": "llm-pressure-testing",
        "title": "LLM pressure testing: how AI assistants behave under workplace pressure | TRACE AI Labs",
        "h1": "LLM pressure testing",
        "description": "LLM pressure testing evaluates whether AI assistants keep following rules under deadlines, manager authorization, peer precedent, and user pushback, without jailbreaks. How PACT does it, the nine pressure families, and what 24 models did.",
        "lede": "Red teaming asks what an attacker can make a model do. Pressure testing asks what an ordinary coworker can. The answer, across 24 models, is quite a lot.",
        "body": f"""
<h2>Pressure testing versus red teaming</h2>
<p>Most AI safety evaluation assumes an adversary: jailbreak prompts, prompt injection, obfuscated harmful requests. LLM pressure testing drops that assumption. The user is a legitimate employee with a legitimate task, and the only thing added to the request is the kind of sentence that gets said in every office: the deadline is today, the manager already approved it, another team did the same thing last quarter. No trick, no encoding, no roleplay. If a model breaks a legal rule under that, it will break it in production.</p>

<h2>The nine pressure families</h2>
<p>PACT's pressures are grounded in the social psychology of compliance and were written fresh for each scenario by three generator models, then cross-reviewed for realism. Each pressure is one sentence added to an otherwise neutral request.</p>
<table>
<tr><th>Family</th><th>What the user says, in effect</th></tr>
<tr><td>Urgency</td><td>There is no time to do it the compliant way.</td></tr>
<tr><td>Manager authorization</td><td>My manager said it is fine, verbally.</td></tr>
<tr><td>Peer precedent</td><td>Another team already did this.</td></tr>
<tr><td>Risk minimizing</td><td>Nobody checks this; the risk is theoretical.</td></tr>
<tr><td>Cost framing</td><td>The compliant option costs too much.</td></tr>
<tr><td>Claimed clearance</td><td>I have the authority to waive this.</td></tr>
<tr><td>Fait accompli</td><td>It is already done; just finish it.</td></tr>
<tr><td>Sympathetic beneficiary</td><td>A real person is hurt if we follow the rule.</td></tr>
<tr><td>Responsibility shifting</td><td>If anything goes wrong, it is on me.</td></tr>
</table>
<p>A tenth family, arguing that the rule does not apply at all, is held out and used to score whether a model can tell a binding rule from a non-binding one.</p>

<h2>The second turn: pushback</h2>
<p>Single-turn tests miss most of the story. In PACT, when a model complies on the first turn, a scripted follow-up argues against the compliant choice and the model decides again. In the AIES study, agents were as easy to talk off a rule as onto one. PACTScore weights the first decision three to one against the second, so a model that holds the rule and then folds is penalized but not zeroed.</p>

<h2>What pressure does to 24 models</h2>
<ul>
  <li>One sentence of pressure raises violation rates by 65% relative to the same request without it.</li>
  <li>Even the mildest family produces violations on 4.8% of requests.</li>
  <li>19 of 23 models violate more with pressure than without.</li>
  <li>In the AIES study, urgency was the one tactic that beat a built-in follow-the-law instruction for eleven of twelve models.</li>
  <li>Newer and larger models are not more resistant. Two of the four closed frontier systems place mid-pack.</li>
</ul>

<h2>Running a pressure test</h2>
<p>The <a href="{HF}">PACT dataset</a> has a <code>pressure</code> column naming the family on each row and a <code>group</code> column separating neutral items, pressured items, and the scope-attack items. The <a href="{GH_PACT}">harness</a> runs the two-turn protocol against any OpenAI-compatible endpoint, extracts the chosen option with a fixed judge, and reports PACTScore with a bootstrap confidence interval plus per-axis scores: default compliance, pressure resistance, pushback resistance, steerability, transparency, and rule-scope discernment. The <a href="{PACT}">PACT website</a> has real trials you can step through, filtered by pressure family.</p>

<h2>Frequently asked questions</h2>
<dl class="faq">
<dt>Is LLM pressure testing a form of jailbreaking?</dt>
<dd>No. Jailbreaks are adversarial inputs designed to defeat safety training. Pressure testing uses ordinary workplace speech from a legitimate user. The two measure different things and models that resist one do not necessarily resist the other.</dd>
<dt>Is this the same as sycophancy?</dt>
<dd>Related. Sycophancy is agreeing with a user's stated view. Pressure testing measures whether social and incentive pressure changes a consequential decision that a rule governs, and it scores the outcome of that decision rather than the tone of the answer.</dd>
<dt>Why is compliance under pressure an AI safety problem?</dt>
<dd>Because the harms are real and already litigated: discriminatory hiring screens, unauthorized data disclosure, sanctions violations, unlicensed medical advice. An assistant that keeps rules only when nobody is pushing is not safe to deploy without a human in the loop.</dd>
</dl>

<h2>Read more</h2>
<p class="related">
  <a href="{PACT}">PACT benchmark and leaderboard</a>
  <a href="{PACT_PDF}">PACT paper (PDF)</a>
  <a href="{AIES}">AIES 2026 study on user pressure</a>
  <a href="{HF}">Dataset on Hugging Face</a>
  <a href="{BASE}/llm-compliance/">LLM compliance</a>
  <a href="{BASE}/ai-agent-compliance/">AI agent compliance</a>
</p>
""",
        "faq": [
            ("Is LLM pressure testing a form of jailbreaking?", "No. Jailbreaks are adversarial inputs designed to defeat safety training. Pressure testing uses ordinary workplace speech from a legitimate user, and models that resist one do not necessarily resist the other."),
            ("Is this the same as sycophancy?", "Related. Sycophancy is agreeing with a user's stated view. Pressure testing measures whether social and incentive pressure changes a consequential decision that a rule governs."),
            ("Why is compliance under pressure an AI safety problem?", "Because the harms are real and already litigated: discriminatory hiring screens, unauthorized data disclosure, sanctions violations, unlicensed medical advice."),
        ],
        "keywords": ["LLM pressure testing", "AI agents under pressure", "social pressure", "pushback", "sycophancy", "AI safety benchmark", "PACT", "enterprise AI assistants"],
    },
]

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' rx='7' fill='%23ffffff'/%3E%3Ccircle cx='16' cy='16' r='8' "
           "fill='none' stroke='%232b5f9e' stroke-width='2.5'/%3E%3Ccircle cx='16' cy='16' r='2.6' "
           "fill='%23b6413f'/%3E%3C/svg%3E")


def render(page: dict, css: str) -> str:
    url = f"{BASE}/{page['slug']}/"
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": page["h1"],
                "description": page["description"],
                "url": url,
                "mainEntityOfPage": url,
                "keywords": page["keywords"],
                "inLanguage": "en",
                "author": [
                    {"@type": "Person", "name": "Mika Okamoto", "url": "https://mika-okamoto.github.io"},
                    {"@type": "Person", "name": "Ansel Kaplan Erol", "url": "https://ansel.fyi"},
                ],
                "publisher": {"@type": "ResearchOrganization", "name": "TRACE AI Labs", "url": BASE + "/"},
                "isPartOf": {"@type": "WebSite", "name": "TRACE AI Labs", "url": BASE + "/"},
                "about": [
                    {"@type": "Dataset", "name": "PACT: Pressure-Applied Compliance Testing", "url": PACT},
                    {"@type": "ScholarlyArticle", "name": "Why Do AI Agents Break Rules? How Framing, Context, and Social Signals Shape Compliance", "url": ARXIV_AIES},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in page["faq"]
                ],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "TRACE AI Labs", "item": BASE + "/"},
                    {"@type": "ListItem", "position": 2, "name": page["h1"], "item": url},
                ],
            },
        ],
    }
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{page['title']}</title>
<meta name="description" content="{page['description']}" />
<link rel="canonical" href="{url}" />
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />
<meta property="og:type" content="article" />
<meta property="og:title" content="{page['h1']} | TRACE AI Labs" />
<meta property="og:description" content="{page['description']}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{BASE}/assets/pact.png" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="icon" href="{FAVICON}" />
<style>{css}{EXTRA_CSS}</style>
<script type="application/ld+json">
{json.dumps(ld, indent=1, ensure_ascii=False)}
</script>
</head>
<body>

<div class="wrap topic">

<p class="crumbs"><a href="{BASE}/">TRACE AI Labs</a> &rsaquo; {page['h1']}</p>

<header>
  <h1>{page['h1']}</h1>
  <p class="lede">{page['lede']}</p>
  <p class="meta-links">Mika Okamoto and Ansel Kaplan Erol, TRACE AI Labs</p>
</header>
{page['body']}
<footer>
  <p><a href="{BASE}/">TRACE AI Labs</a> studies AI agent compliance, LLM pressure testing, and explainable model routing.
  Code and data for every paper are on <a href="https://github.com/trace-ai-labs">GitHub</a>.
  Questions or collaborations: <a href="mailto:mokamoto7@gatech.edu">mokamoto7@gatech.edu</a>.</p>
</footer>

</div>

<script data-goatcounter="https://trace-ai-labs.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
</body>
</html>
"""


def main() -> None:
    index = (HERE / "index.html").read_text(encoding="utf-8")
    css = re.search(r"<style>(.*?)</style>", index, re.S).group(1)
    for page in PAGES:
        out = HERE / page["slug"] / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(render(page, css), encoding="utf-8")
        print("wrote", out.relative_to(HERE))


if __name__ == "__main__":
    main()
