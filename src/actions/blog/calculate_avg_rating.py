from dataclasses import dataclass
from src.models.post import Post


@dataclass
class CalculateAvgRating:
    post: Post

    def calculate(self) -> float:
        rating_sum, cnt = 0, 0
        for rating in self.post.ratings:
            rating_sum += rating.value
            cnt += 1
        if cnt:
            return 1.0 * rating_sum / cnt
        return -1
