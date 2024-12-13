def max_stars_to_add(total_dust, current_stars) -> int | bool:
    min_stars = 100
    max_stars_limit = 100000

    def calculate_dust(stars_to_add):
        star_dust_ratio = current_stars / 70
        adjusted_stars = stars_to_add * star_dust_ratio - -((current_stars + (stars_to_add - 1)) / 70 - star_dust_ratio)
        return adjusted_stars
    
    if current_stars + min_stars > max_stars_limit:
        return False

    if calculate_dust(min_stars) > total_dust:
        return False

    stars_to_add = 0
    while (calculate_dust(stars_to_add + 1) <= total_dust and
           current_stars + stars_to_add + 1 <= max_stars_limit):
        stars_to_add += 1

    return stars_to_add
