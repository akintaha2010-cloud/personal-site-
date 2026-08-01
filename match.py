#Calculate similarity score between two item category and descriptions
def calculate_match_score(lost_item, found_item):
    score = 0

    lost_name = lost_item["name"].lower()
    found_name = found_item["name"].lower()

    lost_location = lost_item["location"].lower()
    found_location = found_item["location"].lower()

    lost_category = lost_item["category"].lower()
    found_category = found_item["category"].lower()

    lost_description = (
        lost_item["description"] or ""
    ).lower()

    found_description = (
        found_item["description"] or ""
    ).lower()

    #30 pts for same category items
    if lost_category == found_category:
        score += 30

    #25 pts for same location items
    if lost_location == found_location:
        score += 25

    #25 pts for simiilar named items
    if lost_name in found_name or found_name in lost_name:
        score += 25

    lost_words = set(lost_description.split())
    found_words = set(found_description.split())

    common_words = lost_words.intersection(found_words)

    #Common words can contribute at most 20 similarity points
    if common_words:
        score += min(len(common_words) * 5, 20)

    return score