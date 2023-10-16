import csv

BONUS_AUTO = 3
BONUS_TELEOP = 5
SCORES = {'High': 5, 'Mid': 3, 'Low': 2}
CATEGORIES = ['Auto Cones', 'Auto Cubes', 'Teleop Cones', 'Teleop Cubes']


def get_csv_data(file_name):
    team_data = {}
    with open(file_name, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            team_number = row['\ufeffTeam']  # use '\ufeffTeam' instead of 'Team'
            if team_number not in team_data:
                team_data[team_number] = {}
            for column, value in row.items():
                team_data[team_number][column] = value
    return team_data


def calculate_points(data, category):
    points = 0
    for level, score in SCORES.items():
        key = f'{category} {level}'
        if key in data and data[key]:
            points += score * float(data[key])
    return round(points, 2)


def calculate_bonus(data):
    bonus_points = 0
    if ('Auto Cones High' in data and float(data['Auto Cones High']) > 0 or
        'Auto Cones Mid' in data and float(data['Auto Cones Mid']) > 0 or
        'Auto Cones Low' in data and float(data['Auto Cones Low']) > 0) and \
       ('Auto Cubes High' in data and float(data['Auto Cubes High']) > 0 or
        'Auto Cubes Mid' in data and float(data['Auto Cubes Mid']) > 0 or
        'Auto Cubes Low' in data and float(data['Auto Cubes Low']) > 0):
           bonus_points += BONUS_AUTO

    if ('Teleop Cones High' in data and float(data['Teleop Cones High']) > 0 or
        'Teleop Cones Mid' in data and float(data['Teleop Cones Mid']) > 0 or
        'Teleop Cones Low' in data and float(data['Teleop Cones Low']) > 0) and \
       ('Teleop Cubes High' in data and float(data['Teleop Cubes High']) > 0 or
        'Teleop Cubes Mid' in data and float(data['Teleop Cubes Mid']) > 0 or
        'Teleop Cubes Low' in data and float(data['Teleop Cubes Low']) > 0):
            bonus_points += BONUS_TELEOP
    return bonus_points


def pick_team(alliance, teams_remaining, team_data):
    print(f"Current alliance: {alliance}")
    print(f"Available keys in team_data: {team_data.keys()}")
    robot = team_data[alliance[-1]]

    evaluated_partners = evaluate_partners(robot, teams_remaining, team_data)


    best_partner = evaluated_partners[0]

    print(f"Picked partner: {best_partner}")
    return best_partner


def evaluate_partners(robot, potential_partners_team_numbers, team_data):
    evaluations = []
    for team_number in potential_partners_team_numbers:
        partner = team_data[team_number]
        scores = {}
        for category in CATEGORIES:
            # store the score difference for each category
            scores[category] = calculate_points(robot, category) - calculate_points(partner, category)

        # find the category with max score difference, i.e. max weakness
        max_score_diff_category = max(scores, key=scores.get)

        # total score is same as your previous implementation
        total_score = sum(calculate_points(partner, category) for category in CATEGORIES) + calculate_bonus(partner)

        # store team_number and its total score and max score difference category
        evaluations.append((total_score, max_score_diff_category, team_number))

    # Sort by total score descending, and then by max weakness
    # so that partners with same total score are then sorted by their max weakness
    evaluations.sort(key=lambda x: (-x[0], x[1]))

    # Return list of team_numbers of best partners
    return [team_number for _, _, team_number in evaluations]


def print_alliances(alliances):
    for i, alliance in enumerate(alliances):
        print(f'Alliance {i+1}:')
        for robot in alliance:
            print(f' - Robot {robot}')
        print()


def create_alliances(team_data):
    ranked_teams = sorted(team_data.keys(), key=lambda team: calculate_total_score(team_data[team]), reverse=True)

    alliances = []

    alliance_leaders = ranked_teams[:8]

    teams_remaining = ranked_teams[8:]

    for leader in alliance_leaders:
        alliance = [leader]

        for _ in range(1):
            next_robot = pick_team(alliance, teams_remaining, team_data)
            alliance.append(next_robot)
            teams_remaining.remove(next_robot)

        alliances.append(alliance)

    # Now do the second round 8-1 rank order
    for alliance in reversed(alliances):
        next_robot = pick_team(alliance, teams_remaining, team_data)
        alliance.append(next_robot)
        teams_remaining.remove(next_robot)

    return alliances

def calculate_total_score(team_data):
    scores = [calculate_points(team_data, category) for category in CATEGORIES]
    scores.append(calculate_bonus(team_data))
    return sum(scores)


def main():
    team_data = get_csv_data('C:/Users/tzvik/PycharmProjects/pythonProject1/allteammetrics.csv')
    for team_number, data in team_data.items():
        print(f'Team Number: {team_number}, Rank: {data["Rank"]}')
        for category in CATEGORIES:
            score = calculate_points(data, category)
            print(f'Score for {category}: {score}')
        bonus = calculate_bonus(data)
        print(f'Bonus points: {bonus}\n')

    alliances = create_alliances(team_data)
    print_alliances(alliances)


if __name__ == '__main__':
    main()
