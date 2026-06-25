"""Rule-based adaptive math tutor simulation.

Method v1 is a simple baseline tutor that adjusts question difficulty
using hand-written rules and simulated students.
"""

from dataclasses import dataclass, field
from random import Random
from typing import Dict, List, Optional


DIFFICULTIES = ["easy", "medium", "hard"]


@dataclass
class StudentProfile:
    name: str
    skill_by_difficulty: Dict[str, float]
    learning_rate: float
    mastery_threshold: float = 0.85
    skill_growth: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.skill_growth:
            self.skill_growth = {difficulty: 0.0 for difficulty in DIFFICULTIES}

    def answer_probability(self, difficulty: str) -> float:
        base_skill = self.skill_by_difficulty[difficulty]
        growth = self.skill_growth[difficulty]
        return max(0.05, min(0.98, base_skill + growth))

    def update_learning(self, difficulty: str, correct: bool) -> None:
        # Students learn more from questions that are challenging but possible.
        current_prob = self.answer_probability(difficulty)
        challenge_factor = 1.0 - abs(0.7 - current_prob)
        outcome_factor = 1.0 if correct else 0.6
        gain = self.learning_rate * challenge_factor * outcome_factor

        self.skill_growth[difficulty] += gain

        # Some learning transfers to nearby difficulties.
        index = DIFFICULTIES.index(difficulty)
        if index > 0:
            easier = DIFFICULTIES[index - 1]
            self.skill_growth[easier] += gain * 0.25
        if index < len(DIFFICULTIES) - 1:
            harder = DIFFICULTIES[index + 1]
            self.skill_growth[harder] += gain * 0.15

        for key in self.skill_growth:
            self.skill_growth[key] = min(self.skill_growth[key], 0.5)

    def mastery_score(self) -> float:
        return sum(self.answer_probability(d) for d in DIFFICULTIES) / len(DIFFICULTIES)


@dataclass
class TutorState:
    difficulty_index: int = 1
    correct_streak: int = 0
    wrong_streak: int = 0
    history: List[Dict[str, object]] = field(default_factory=list)

    @property
    def current_difficulty(self) -> str:
        return DIFFICULTIES[self.difficulty_index]


class RuleBasedTutor:
    """Simple hand-written adaptation rules for Method v1."""

    def choose_difficulty(self, state: TutorState) -> str:
        if state.wrong_streak >= 2:
            return "easy"
        return state.current_difficulty

    def update_state(self, state: TutorState, was_correct: bool) -> None:
        if was_correct:
            state.correct_streak += 1
            state.wrong_streak = 0
            if state.correct_streak >= 3 and state.difficulty_index < len(DIFFICULTIES) - 1:
                state.difficulty_index += 1
                state.correct_streak = 0
        else:
            state.wrong_streak += 1
            state.correct_streak = 0
            if state.wrong_streak >= 2 and state.difficulty_index > 0:
                state.difficulty_index -= 1
                state.wrong_streak = 0


def simulate_session(
    student: StudentProfile,
    tutor: RuleBasedTutor,
    seed: int = 7,
    max_questions: int = 30,
) -> Dict[str, object]:
    rng = Random(seed)
    state = TutorState()
    starting_mastery = student.mastery_score()
    mastery_step: Optional[int] = None

    for step in range(1, max_questions + 1):
        difficulty = tutor.choose_difficulty(state)
        probability = student.answer_probability(difficulty)
        correct = rng.random() < probability
        student.update_learning(difficulty, correct)
        tutor.update_state(state, correct)

        mastery = student.mastery_score()
        state.history.append(
            {
                "step": step,
                "difficulty": difficulty,
                "correct": correct,
                "probability": round(probability, 3),
                "mastery": round(mastery, 3),
            }
        )

        if mastery_step is None and mastery >= student.mastery_threshold:
            mastery_step = step

    successes = sum(1 for entry in state.history if entry["correct"])
    return {
        "student": student.name,
        "starting_mastery": round(starting_mastery, 3),
        "ending_mastery": round(student.mastery_score(), 3),
        "learning_gain": round(student.mastery_score() - starting_mastery, 3),
        "success_rate": round(successes / len(state.history), 3),
        "questions_to_mastery": mastery_step,
        "history": state.history,
    }


def build_students() -> List[StudentProfile]:
    return [
        StudentProfile(
            name="fast_learner",
            skill_by_difficulty={"easy": 0.82, "medium": 0.62, "hard": 0.38},
            learning_rate=0.05,
        ),
        StudentProfile(
            name="struggling_learner",
            skill_by_difficulty={"easy": 0.65, "medium": 0.4, "hard": 0.2},
            learning_rate=0.035,
        ),
        StudentProfile(
            name="uneven_learner",
            skill_by_difficulty={"easy": 0.88, "medium": 0.5, "hard": 0.25},
            learning_rate=0.04,
        ),
    ]


def print_summary(result: Dict[str, object]) -> None:
    print(f"Student: {result['student']}")
    print(f"  Starting mastery: {result['starting_mastery']}")
    print(f"  Ending mastery:   {result['ending_mastery']}")
    print(f"  Learning gain:    {result['learning_gain']}")
    print(f"  Success rate:     {result['success_rate']}")

    mastery_step = result["questions_to_mastery"]
    mastery_text = str(mastery_step) if mastery_step is not None else "not reached"
    print(f"  Questions to mastery: {mastery_text}")
    print("  First 5 tutor decisions:")

    for entry in result["history"][:5]:
        outcome = "correct" if entry["correct"] else "wrong"
        print(
            "   "
            f"Q{entry['step']}: {entry['difficulty']} -> {outcome} "
            f"(p={entry['probability']}, mastery={entry['mastery']})"
        )
    print()


def main() -> None:
    tutor = RuleBasedTutor()
    students = build_students()

    print("Method v1: Rule-based adaptive tutor")
    print("------------------------------------")

    for index, student in enumerate(students):
        result = simulate_session(student, tutor, seed=10 + index)
        print_summary(result)


if __name__ == "__main__":
    main()
