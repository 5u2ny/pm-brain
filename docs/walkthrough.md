# A week with PM Brain — Lena's first five days

PM Brain is easier to *see* than to describe. This is a short story about one product manager — Lena — using it for a week. You'll see what she sees, what the brain catches, and what she decides.

> **First, the words we'll use.** A *brain* here is just a folder of markdown files in a git repo on your laptop. To *ingest* something means to feed it into that folder so the brain knows about it. *Provenance* is shorthand for "where this claim came from" — every important note in the brain wears a small tag saying whether it came from an interview, a Slack message, a verbal hallway exchange, or your own hunch. There is a one-page [glossary](./glossary.md) at the end if anything else gets jargon-y.

---

## Monday — onboarding into a real team

**Lena Vasquez** just took over PM for a B2B project-collaboration tool called **Mosaic**. The previous PM left on good terms but didn't leave much beyond a Notion workspace, a Jira project, and a 3-month-old Miro discovery board. Lena's job: get on top of it.

She opens Claude, plugs in the **Notion**, **Jira**, and **Miro** app connectors (or, for any tool she can't connect, she exports the pages she cares about as files and drops them in a folder — either path works). Then she runs:

```
/pm-brain
```

The skill detects that there's no brain here yet but there are real PM artifacts to absorb. It enters **migration mode** and walks Lena through a short interview — company, role, current priorities, top stakeholders, what's in flight. Five batches of questions, about 10 minutes.

Then it reads through what's in Notion, Jira, and Miro. Forty-five minutes later, Lena has:

- A folder of markdown files: hypotheses being tracked, decisions on record, stakeholder profiles, knowledge files for strategy and product
- An `INDEX.md` she can use to navigate everything
- A short report from the brain saying *what it found, what it couldn't make sense of, and the questions she should answer this week*

That last part is where it gets interesting.

### The strategy-vs-shipped-work gap

Buried in the brain's onboarding report is one line:

> **Tension surfaced.** The strategy doc in Notion (`Q2 Strategy v3`, last edited 2026-02-10) says the team's north-star is *activation: 60% of new accounts invite a teammate by day 3*. But of the 47 Jira tickets shipped in Q1 and Q2, 38 are tagged "enterprise permissions" or "admin tooling." Only 4 touch the activation funnel. The work and the stated strategy don't match.

Lena would have eventually noticed this herself — probably in week three, in a 1:1 with engineering, after she'd already absorbed the official strategy and built her plans on top of it. The brain noticed it on day one because it cross-checked two folders that humans tend to read separately.

She has options. She can update the Notion strategy to reflect what's actually being built. She can take the gap to the leadership team as a real question: *which one is right?* She can do both. The brain doesn't fix the Notion doc for her — that's not its job. It just makes the conversation possible.

She writes a quick line in the brain's `knowledge/strategy.md` saying she's going to raise it with the CEO Wednesday, and moves on.

> **Benefit, in plain words.** A new PM usually spends three weeks absorbing the official story before they have enough context to question it. Lena had a real question to ask on day one. The brain caught what humans smooth over.

---

## Tuesday — a discovery call with a real account

Lena has a 45-minute discovery call with **Talia Brennan**, Head of Operations at **Northridge Construction** — a mid-sized account on Mosaic for eight months. Talia's been a quiet user, no complaints, but their seat count plateaued.

Lena records the call. After it ends, she drops the transcript into the brain:

```
/ingest northridge-talia-transcript.md
```

The brain reads the transcript and does four things at once:

1. **Saves the original transcript** under `source/interviews/2026-05-19-northridge-talia.md`, untouched. This is the audit anchor — it never gets edited.
2. **Writes a synthesis note** under `ingestion/interviews/...` that pulls out the observations Talia actually made, tagged with her name and the date.
3. **Tells Lena, right there in chat, what context she should know about Talia's account before drawing conclusions:**
   - Two other stakeholders flagged the same pattern Talia mentioned — invite-link friction — back in March. The brain quotes them.
   - There's already a `candidate` hypothesis in the brain about invite-link expiry. The previous PM had opened it but never collected enough evidence to validate it.
   - The Miro discovery board from January has a sticky note that says "magic-link onboarding?" — never explored.
4. **Adds Talia's observation as a new evidence row** on the existing invite-link hypothesis. Promotes it from `candidate` to `proposed` because there are now three independent observations.

Lena reads the chat reply and sees not just *what Talia said* but *what Talia said in the context of everything else the team has heard about this exact problem*. One call, but it lands with the weight of three. She didn't have to remember the Miro sticky note or the March stakeholder comments — the brain put them in front of her.

> **Benefit, in plain words.** Each new signal lands in the context of what the team already knew. You stop re-discovering things. You stop missing the connection between today's call and last quarter's research.

---

## Wednesday — the marketing manager wants dark mode

Lena's Slack lights up with a message from **Rahul Pillai**, the marketing manager:

> "We need to ship dark mode this quarter. Every single demo I run, prospects ask for it. It's killing our conversion rate."

It's loud, it's recent, it's plausible. A less-confident PM might tell engineering to start scoping it.

Lena types a quick line into Claude:

```
Rahul (marketing) just messaged: "We need dark mode this quarter, every demo
asks for it, it's killing conversion." Capture as verbal stakeholder claim,
flag any conflict with what's documented.
```

The brain captures Rahul's claim with the right tag — `(stakeholder-verbal, rahul-pillai, 2026-05-20)` — meaning *Rahul said this verbally, on this date, no document behind it yet*. Then it does something more interesting: it scans what's already in the brain and surfaces the documented counter-evidence.

> **Conflicting documented evidence.**
> - Last quarter's sales-call audit (Q1 close-loss review, 2026-04-02): 27 demos analyzed. Dark mode appears as a wishlist line item in 2 of them. Cited as a *blocker* in zero.
> - Customer interview, Cascadia Health, 2026-03-15: when asked what would tip them toward upgrading, the buyer named integrations and admin controls. Dark mode wasn't mentioned.
> - Customer interview, Brillstone, 2026-04-18: same question, same answer. Dark mode not mentioned.
> - Documented Q2 strategy (Notion, 2026-02-10): activation north-star, not feature parity.

The brain doesn't argue with Rahul. It doesn't tell Lena what to do. It just puts the documented evidence on the table next to the verbal claim, both tagged for what they are — *one verbal observation from marketing* vs *27 documented sales calls, two customer interviews, and the team's stated strategy*.

Lena replies to Rahul:

> "Want to dig into this. I've got us on Friday — I'll pull what we know about dark-mode demand and we can look at it together. If it's bigger than the audit suggests, we should figure out why we missed it."

She's not capitulating. She's not dismissing. She has the documented case ready, and she has a productive conversation booked instead of an argument.

> **Benefit, in plain words.** The brain keeps documented evidence and the loudest recent voice in their proper proportion. When a stakeholder makes a priority claim, you walk into the next conversation with what the team has actually learned, not vibes.

---

## Thursday — engineering proposes an alternative

In Lena's Thursday 1:1, **Mateus Okafor** (engineering lead) brings up the invite-link work.

> "We've been talking about building a redesigned teammate-invite flow. What if we ran a 1-week spike instead — try magic-invite-links, see if a simpler thing works? If it does, we save four weeks of UI work."

This is the kind of suggestion that often dies in DM scrollback. Lena adds a line to the brain:

```
Mateus suggested: 1-week spike on magic-invite-links as alternative to
rebuilding the teammate-invite UI. Capture as verbal, route to the
invite-link hypothesis as a solution-discovery option.
```

The brain records the verbal — `(stakeholder-verbal, mateus-okafor, 2026-05-21)` — and adds it to the invite-link hypothesis under a *solution options* section. It's now findable next to Talia's customer-side evidence and the Miro sticky note from January.

> **Benefit, in plain words.** Cross-functional input — from engineering, design, marketing, sales — lands where it's findable later, instead of being lost in chat history.

---

## Friday — `/review`, then the strategy meeting

It's Friday afternoon. Lena runs:

```
/review
```

This is the weekly maintenance sweep. The brain reads the whole folder and produces one page covering what changed this week, what's drifting, and what to take into next week. For Lena, that page reads:

> **This week**
> - **Strategy gap** (still open): Q2 strategy vs Q1/Q2 shipped work. You flagged it Monday, you haven't raised it with the CEO yet. Wednesday's meeting was on a different agenda.
> - **Invite-link hypothesis** moved from `candidate` to `proposed` after Talia's interview Tuesday. Three independent observations now. The next step toward `validated` would be a structured 5-interview round on the same persona; you have a list of candidate accounts in `knowledge/users/personas.md`.
> - **Dark mode tension** (Rahul, Wednesday): captured as verbal claim, flagged against documented evidence. Friday's meeting with Rahul is your action item.
> - **Magic-invite-links spike** (Mateus, Thursday): captured as a solution option on the invite-link hypothesis. No action needed until you decide direction.
>
> **Drifting**
> - The `enterprise-permissions-v2` hypothesis hasn't had new evidence in 47 days. Last touched March. It's still listed as a Q3 candidate but nobody is sourcing evidence for it. Worth deciding: revive, demote, or archive?
>
> **For your Monday strategy meeting**
> 1. Open with the strategy-vs-shipped-work gap. Suggest a decision: are we activation-first or enterprise-first? The team has shipped enterprise; the doc says activation. One of them is wrong.
> 2. Bring the invite-link hypothesis forward. Three observations, one engineering alternative on the table. Ask for a go/no-go on the 1-week spike.
> 3. Park dark mode. You're meeting Rahul Friday, you'll have a real answer next week.

Lena reads this in five minutes. Her Monday meeting prep is done.

She walks into Monday with the conversations she needs to have, the evidence to support each one, and no surprise gaps. The brain didn't make any of these decisions for her. It made the week's signal *legible*.

> **Benefit, in plain words.** The Friday sweep is the forcing function. It's the moment the brain pays you back for the small captures you made all week. Skip it for a month and the system rots; do it weekly and the next week starts with momentum.

---

## What Lena got — in five lines

- **Monday:** a real question to ask the CEO, on day one
- **Tuesday:** a customer call that landed with the weight of three
- **Wednesday:** documented evidence ready when a loud voice contradicted it
- **Thursday:** an engineering suggestion that didn't die in Slack
- **Friday:** a one-page summary that made Monday's meeting easy

None of this is automation. None of it is the brain making decisions Lena should be making. It's the brain doing the small, boring, easy-to-forget work of cross-referencing what you already know — so the judgment work, which is your job, gets easier.

## Want to try it?

- [Install](../README.md#install) takes about three minutes
- [How it works](./how-it-works.md) — the technical version, with files and folder structure
- [Architecture](./architecture.md) — the design choices and why they're what they are
- [Glossary](./glossary.md) — every term used in PM Brain, in one place
