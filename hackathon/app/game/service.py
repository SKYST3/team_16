from typing import List, Tuple
from hackathon.app.common import values

PERFECT_THRESHOLD = 500  # Example threshold in milliseconds
GOOD_THRESHOLD = 1500    # Example threshold in milliseconds

async def process_submission_and_calculate_score(
    submitted_timestamps: List[int],
    answer_timestamps: List[int],
    team_name: str
) -> dict:
    """
    Merges timestamps, finds the closest submitted timestamp for each answer,
    and directly calculates the score.
    """
    merged_timestamps: List[Tuple[int, str]] = []
    for ts in submitted_timestamps:
        merged_timestamps.append((ts, 'submitted'))
    for ts in answer_timestamps:
        merged_timestamps.append((ts, 'answer'))

    merged_timestamps.sort()

    normal_count = 0
    good_count = 0
    perfect_count = 0
    total_score = 0
    n = len(merged_timestamps)
    used_indices = [False] * n

    for i in range(n):
        current_ts, current_type = merged_timestamps[i]
        if current_type == 'answer':
            closest_diff = float('inf')
            closest_submitted_index = -1

            # Check previous
            if i > 0:
                prev_ts, prev_type = merged_timestamps[i - 1]
                if prev_type == 'submitted' and not used_indices[i - 1]:
                    diff_prev = abs(prev_ts - current_ts)
                    if diff_prev < closest_diff:
                        closest_diff = diff_prev
                        closest_submitted_index = i - 1

            # Check next
            if i < n - 1:
                next_ts, next_type = merged_timestamps[i + 1]
                if next_type == 'submitted' and not used_indices[i + 1]:
                    diff_next = abs(next_ts - current_ts)
                    if diff_next < closest_diff:
                        closest_diff = diff_next
                        closest_submitted_index = i + 1
                    elif diff_next == closest_diff and closest_submitted_index != -1 and (i - 1 >= 0 and merged_timestamps[i-1][1] == 'submitted'):
                        # Tie-breaker: prefer the earlier submitted timestamp
                        pass
                    elif closest_submitted_index == -1 and diff_next < float('inf'):
                        closest_diff = diff_next
                        closest_submitted_index = i + 1

            if closest_submitted_index != -1:
                used_indices[closest_submitted_index] = True
                if closest_diff <= PERFECT_THRESHOLD:
                    perfect_count += 1
                    total_score += 4
                elif closest_diff <= GOOD_THRESHOLD:
                    good_count += 1
                    total_score += 2
                else:
                    normal_count += 1
                    total_score += 0
            else:
                # No close submitted timestamp found for this answer, it's a miss
                pass # You could track misses if needed

    for score_dict in values['scores']:
        for team_enum in score_dict:  # Iterate through the keys (Team enums)
            if team_enum.value == team_name:
                score_dict[team_enum] += total_score
                break
        else:
            continue
        break
    
    return {
        "normal": normal_count,
        "good": good_count,
        "perfect": perfect_count,
        "score": total_score
    }
