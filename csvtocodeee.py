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
            team_number = row['\ufeffTeam']
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


def calculate_total_score(team_data):
    scores = [calculate_points(team_data, category) for category in CATEGORIES]
    scores.append(calculate_bonus(team_data))

    rank = int(team_data["Rank"])
    scores.append(1 / rank)  # higher rank contributes more

    return sum(scores)


def calculate_score_without_rank(team_data):
    scores = [calculate_points(team_data, category) for category in CATEGORIES]
    scores.append(calculate_bonus(team_data))
    return sum(scores)


def pick_team(alliance, teams_remaining, team_data, current_alliances):
    print(f"Current alliance: {alliance}")
    print(f"Available keys in team_data: {team_data.keys()}")
    robot = team_data[alliance[-1]]

    evaluated_partners = evaluate_partners(robot, teams_remaining, team_data)

    # the next entry is alliance leader which we need to avoid in the picked up teams
    best_partner = evaluated_partners[0]
    while best_partner in [item for sublist in current_alliances for item in sublist]:
        evaluated_partners.pop(0)
        best_partner = evaluated_partners[0]

    print(f"Picked partner: {best_partner}")
    return best_partner


def evaluate_partners(robot, potential_partners_team_numbers, team_data):
    evaluations = []
    for team_number in potential_partners_team_numbers:
        partner = team_data[team_number]
        scores = {}
        for category in CATEGORIES:
            scores[category] = calculate_points(robot, category) - calculate_points(partner, category)

        max_score_diff_category = max(scores, key=scores.get)

        total_score = calculate_score_without_rank(partner)

        evaluations.append((total_score, max_score_diff_category, team_number))

    key = lambda x: (-x[0], x[1])  # do not consider rank in picking process
    evaluations.sort(key=key)

    return [team_number for _, _, team_number in evaluations]


def print_alliances(alliances):
    for i, alliance in enumerate(alliances):
        print(f'Alliance {i + 1}:')
        for robot in alliance:
            print(f' - Robot {robot}')
        print()


def create_alliances(team_data):
    key = lambda team: int(team_data[team]['Rank'])
    ranked_teams = sorted(team_data.keys(), key=key)

    alliances = []
    alliance_leaders = ranked_teams[:8]
    all_teams = set(ranked_teams)  # we use a set here for efficiency

    for leader in alliance_leaders:
        alliance = [leader]
        all_teams.discard(leader)

        for _ in range(1):
            if all_teams:  # still has robot to pick
                next_robot = pick_team(alliance, list(all_teams), team_data, alliances)
                alliance.append(next_robot)
                all_teams.discard(next_robot)

        alliances.append(alliance)

    for alliance in reversed(alliances):
        if all_teams:  # still has robot to pick
            next_robot = pick_team(alliance, list(all_teams), team_data, alliances)
            alliance.append(next_robot)
            all_teams.discard(next_robot)

    return alliances


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