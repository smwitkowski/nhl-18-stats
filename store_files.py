import os
import cv2


def create_game_folder(id):
    if not os.path.exists(id):
        path = '/'.join(['data', str(id)])
        os.mkdir(path)
        return path


def store_data(stats, away_score, away_team, home_score, home_team, path)
    cv2.imwrite('/'.join([path, 'away_score.jpg']), away_score)
    cv2.imwrite('/'.join([path, 'away_team.jpg']), away_team)
    cv2.imwrite('/'.join([path, 'home_score.jpg']), home_score)
    cv2.imwrite('/'.join([path, 'home_team.jpg']), home_team)
    with open('stats.txt', 'w') as f:
        for stat in stats:
            f.write('%s\n' % stat)
