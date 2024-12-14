def max_stars_to_add(total_dust: int, current_stars: int) -> int:
    if not total_dust or not current_stars:
        return 0

    max_cost_per_star = (total_dust * 70 + 1) // (current_stars + 1)

    max_total_stars = 100000 - current_stars

    maximum_stars = min(max_cost_per_star, max_total_stars)

    if maximum_stars >= 100:
        return maximum_stars
    else:
        return 0
