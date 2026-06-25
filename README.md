# Adaptive Math Tutor

For my project, I want to build an adaptive math tutor. The basic idea is that the tutor does not just give random math questions. It tries to learn what kind of question the student should get next based on how they have been doing so far.

If the student is getting a lot right, the tutor can make the questions harder. If they are struggling, it can slow down, give easier questions, or give review questions.

## Project Idea

I want to compare three different ways of doing this:

1. A rule-based system, where I make simple rules like "if the student gets three questions right, move up a level," or "if they get two wrong, go back and review."
2. A bandit approach, where the tutor tries different types of questions and slowly learns which ones seem to help the most.
3. A Q-learning approach, where the tutor learns what action is best depending on the student's current situation.

## Initial Plan

For now, I will probably start by simulating students instead of using real students, because that makes it easier to test. I can make different fake students, like one who learns quickly, one who struggles more, and one who is good at some topics but weak in others.

Then I can run the three tutor methods on the same types of students and compare which one helps them learn faster.

## What I Want to Measure

The main things I want to measure are:

- how much the student improves
- how many questions it takes them to reach mastery
- how often each tutor actually helps the student succeed

I also want to be careful with the reward system, because I do not want the AI to just give easy questions so the student gets more correct answers. I want it to reward real learning by giving questions that are challenging but still possible.

## Why This Project Matters

This project is about more than just generating questions. It is about testing which tutoring strategy helps students improve the fastest and most effectively.

The broader goal is to explore how adaptive learning systems can make math tutoring more personalized by responding to student progress in a smarter way.

## Method v1

Week 4 of the project is a first working version of the tutor. This version uses a rule-based system instead of bandits or Q-learning.

The tutor follows simple adaptation rules:

- if a student gets 3 questions correct in a row, move up difficulty
- if a student gets 2 wrong, move down and review
- otherwise, stay near the current difficulty level

The current implementation uses simulated students:

- a fast learner
- a struggling learner
- an uneven learner

For each student, the simulation tracks:

- starting mastery
- ending mastery
- learning gain
- success rate
- questions to mastery

## Run

```bash
python3 method_v1.py
```
