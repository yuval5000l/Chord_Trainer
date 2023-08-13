TITLE = "MusicTrainer"
WINDOW_SIZE = (500, 500)

FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (127, 127, 127)
GRAY_DARK = (70, 70, 70)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
MAGENTA_LIGHT = (127, 0, 127)
LIGHT_BLUE = (146, 250, 255)

# NOTES
C_LOWEST = 36
C_HIGHEST = 96
SIMPLE_NOTES_LIST = list(range(C_LOWEST, C_LOWEST + 13))
ALL_NOTES_LIST = list(range(C_LOWEST, C_HIGHEST + 1))
MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11, 12]
MINOR_SCALE = [0, 2, 3, 5, 7, 8, 10, 12]
MAJOR_SCALE_CHORDS = [(x,'Major') if i in (0, 3, 4) else (x, 'Minor') for i, x in enumerate(MAJOR_SCALE[:-1])]
MAJOR_SCALE_CHORDS[-1] = (MAJOR_SCALE_CHORDS[-1][0], 'Diminished')
MINOR_SCALE_CHORDS = [(x,'Minor') if i in (0, 3, 4) else (x, 'Major') for i, x in enumerate(MINOR_SCALE[:-1])]
MINOR_SCALE_CHORDS[1] = (MAJOR_SCALE_CHORDS[1][0], 'Diminished')
MAX_VOL = 127
BRIEF = .5

# print(MAJOR_SCALE_CHORDS)
# print(MINOR_SCALE_CHORDS)
NOTES_DICTIONARY = {'C': [note for note in range(C_LOWEST, C_HIGHEST + 1, 12)],
                    'Db': [note for note in
                           range(C_LOWEST + 1, C_HIGHEST + 1, 12)],
                    'D': [note for note in
                          range(C_LOWEST + 2, C_HIGHEST + 1, 12)],
                    'Eb': [note for note in
                           range(C_LOWEST + 3, C_HIGHEST + 1, 12)],
                    'E': [note for note in
                          range(C_LOWEST + 4, C_HIGHEST + 1, 12)],
                    'F': [note for note in
                          range(C_LOWEST + 5, C_HIGHEST + 1, 12)],
                    'Gb': [note for note in
                           range(C_LOWEST + 6, C_HIGHEST + 1, 12)],
                    'G': [note for note in
                          range(C_LOWEST + 7, C_HIGHEST + 1, 12)],
                    'Ab': [note for note in
                           range(C_LOWEST + 8, C_HIGHEST + 1, 12)],
                    'A': [note for note in
                          range(C_LOWEST + 9, C_HIGHEST + 1, 12)],
                    'Bb': [note for note in
                           range(C_LOWEST + 10, C_HIGHEST + 1, 12)],
                    'B': [note for note in
                          range(C_LOWEST + 11, C_HIGHEST + 1, 12)]}
CHORDS_DICTIONARY = {'Major': [0, 4, 7], 'Minor': [0, 3, 7],
                     'Diminished': [0, 3, 6], 'Augmented': [0, 4, 8]}
SCALES_DICTIONARY = {'Major': MAJOR_SCALE, 'Minor': MINOR_SCALE}

SCALES_CHORDS_DICTIONARY = {'Major': MAJOR_SCALE_CHORDS, 'Minor': MINOR_SCALE_CHORDS}