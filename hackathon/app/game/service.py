from typing import List

PERFECT_THRESHOLD = 50  # Example threshold in milliseconds
GOOD_THRESHOLD = 150    # Example threshold in milliseconds

async def calculate_score(submitted_timestamps: List[int], answer_timestamps: List[int]) -> dict:
    """
    Calculates the score based on submitted timestamps and the answer key.
    """
    normal_count = 0
    good_count = 0
    perfect_count = 0
    total_score = 0

    if not answer_timestamps:
        return {"normal": 0, "good": 0, "perfect": 0, "score": 0}

    if len(submitted_timestamps) != len(answer_timestamps):
        raise ValueError("Incorrect number of timestamps submitted") # Or handle differently

    for submitted, correct in zip(submitted_timestamps, answer_timestamps):
        difference = abs(submitted - correct)

        if difference <= PERFECT_THRESHOLD:
            perfect_count += 1
            total_score += 30
        elif difference <= GOOD_THRESHOLD:
            good_count += 1
            total_score += 20
        else:
            normal_count += 1
            total_score += 10

    return {
        "normal": normal_count,
        "good": good_count,
        "perfect": perfect_count,
        "score": total_score
    }