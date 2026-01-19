PROJECT CONTEXT
Project Name: Init
1. What Init Is

Init is a structured, daily learning system for computer science students and early-career engineers who want to master the real foundations of software engineering that are typically underemphasized in school.

Init focuses on:

systems fundamentals

operating systems concepts

networking

concurrency and memory

DevOps and infrastructure basics

applied system design thinking

The product teaches these topics through active recall, applied drills, explain-back, and feedback, not lectures or passive content.

Init exists to answer a single question for the user:

“Do I actually understand how real systems work?”

2. The Problem Init Solves

Most CS undergraduates experience a gap between:

what they learn in classes

what interviews expect

what real production systems require

Common symptoms:

strong at algorithms, weak at systems intuition

can write code, cannot explain how it behaves under load

unfamiliar with OS concepts beyond definitions

uncomfortable debugging failures, logs, or performance issues

unsure how software actually runs in production

Init does not replace coursework.
It fills the missing middle layer between theory and practice.

3. What Init Is Not

Init is explicitly not:

a bootcamp

a video course platform

a certification program

a LeetCode replacement

a documentation mirror

a generic learning app

It does not aim for breadth first.
It aims for depth, clarity, and confidence.

4. Target User

Primary users:

CS undergraduates (years 2 to 4)

internship and new-grad SWE candidates

self-motivated learners who want strong fundamentals

Assumed user characteristics:

technically curious

short on time

overwhelmed by topic sprawl

values structure and feedback

wants to feel “industry-ready”

UX should feel:

calm

professional

focused

non-gimmicky

5. Core Learning Philosophy

Init is built on four principles:

Active recall beats passive reading

Explaining a concept reveals understanding gaps

Small, daily practice compounds

Feedback is more valuable than volume

Every feature must reinforce at least one of these.

6. The Core Learning Loop

The core loop is the heart of the product and must remain simple and reliable.

User starts a daily session or receives a reminder

User completes a small drill

User explains or solves something in their own words

System evaluates the response against a rubric

Feedback is returned

Mastery is updated

Future drills adapt based on mastery

This loop should be achievable in 10 to 25 minutes per day.

7. Tracks and Scope

Init is organized into tracks, each representing a coherent learning path.

Initial focus:

Systems Foundations (the first and most important track)

Future tracks, only after the first is excellent:

DevOps Foundations

System Design Foundations

Backend Fundamentals

Tracks are intentionally finite and structured, not endless.

8. Systems Foundations Track (First Track)

Purpose:
Teach how modern software systems actually execute, communicate, and fail.

Topics include:

processes vs threads

user mode vs kernel mode

context switching

virtual memory and paging

stack vs heap

concurrency and synchronization

deadlocks and race conditions

file descriptors and I/O

networking fundamentals

latency vs throughput

debugging mental models

Each concept appears multiple times across drills to reinforce mastery.

9. Drill Types

Init uses small, atomic drills.

Explain drills

User explains a concept clearly and correctly in their own words.

Example:
“Explain the difference between a process and a thread, and why it matters.”

Debug drills

User reasons about a failure, bug, or symptom.

Example:
“A service is slow under load but CPU usage is low. What are likely causes?”

Quiz drills

Used sparingly for quick checks and spaced repetition.

Drills are intentionally short and reusable.

10. Rubric-Based Evaluation

Every drill has a predefined rubric.

A rubric includes:

scoring criteria

expected key points

common mistakes

guidance for feedback

Evaluation focuses on:

correctness

completeness

clarity

use of correct terminology

The goal is not perfection, but clear improvement signals.

11. Mastery Model

Understanding is tracked numerically.

Mastery score range:

0: unseen

1: exposed

2: basic recall

3: clear explanation

4: applied understanding

5: confident and consistent

Mastery can decay over time if not reinforced.

Future drills are scheduled based on mastery and review timing.

12. Content as Data

Init treats learning content as structured data, not prose.

Content is:

versioned

schema-validated

stored as files in the repo

seeded into the database

This enables:

clean iteration

review via pull requests

reproducibility

eventual community contribution

13. Technical Philosophy

Init is built like a real production system, even as an MVP.

Guiding principles:

clear separation of concerns

minimal but explicit abstractions

no premature optimization

boring architecture over cleverness

predictable behavior over novelty

14. Technology Stack

Frontend:

React Native (Expo)

TypeScript

Expo Router

NativeWind for styling

Zustand for local state

TanStack Query for server state

Backend:

Python FastAPI

Pydantic for models

Modular router and service structure

Database:

Supabase PostgreSQL

Supabase Auth

Row Level Security for access control

AI:

OpenAI API

Used only for grading and feedback

Accessed only from backend services

15. Boundaries and Non-Negotiables

No raw SQL in frontend

No business logic in UI components

No AI calls from the client

No feature that bypasses the core loop

No over-engineering early

If a feature does not strengthen learning, feedback, or mastery, it does not belong.

16. Success Criteria

Init is successful if users say:

“I finally understand how this works.”

“I can explain this clearly now.”

“Interviews feel less mysterious.”

“Debugging makes more sense.”

The metric is confidence backed by understanding, not completion badges.

17. North Star

If Init disappeared tomorrow, a user should still walk away with:

A stronger mental model of how real software systems behave in the real world.

That is the standard every decision should be judged against.