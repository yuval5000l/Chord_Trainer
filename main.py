import pygame as pg
import pygame.midi
import sys
import time
from pygame._sdl2.video import Window
import random
from settings import *


class Note:
    height = 100
    length = 50
    last_note = None

    def __init__(self, screen, note_num: int, note_loc: int):
        self.num = note_num
        self.screen = screen
        self.name = note_check(note_num)
        self.pressed = False
        if Note.last_note:
            x = Note.last_note.get_rect().topright[0] - 25
        else:
            x = 0
        if 'b' not in self.name:
            self.color = WHITE, GRAY
            self.neg_color = BLACK, GRAY_DARK
            if Note.last_note and Note.last_note.get_color() == self.color:
                x = Note.last_note.get_rect().topright[0]
            self.rect = pg.Rect(x,
                                screen.get_height() - Note.height,
                                Note.length, Note.height)
        else:
            self.rect = pg.Rect(x,
                                screen.get_height() - Note.height,
                                Note.length, Note.height // 2)
            self.color = BLACK, GRAY_DARK
            self.neg_color = WHITE, GRAY
        Note.last_note = self

    def update(self):
        if self.pressed:
            pg.draw.rect(self.screen, self.color[1], self.rect)
            pg.draw.rect(self.screen, self.neg_color[1], self.rect, width=3)
        else:
            pg.draw.rect(self.screen, self.color[0], self.rect)
            pg.draw.rect(self.screen, self.neg_color[0], self.rect, width=1)

    def get_num(self):
        return self.num

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

    def get_rect(self):
        return self.rect

    def press(self):
        if self.pressed:
            self.pressed = False
        else:
            self.pressed = True

    def update_res(self):
        self.rect.topleft = (self.rect.topleft[0],
                             self.screen.get_height() - Note.height)

    def __repr__(self):
        return self.name


def run_trainer():
    clock = pg.time.Clock()
    pg.init()
    pg.fastevent.init()
    pg.midi.init()
    pg.display.set_caption(TITLE)
    pg.font.init()
    chord_game_loop(clock)


def making_notes(screen, dr_obj):
    drawing_notes = []
    black_notes = []
    dr_obj.clear()
    Note.last_note = None
    # Making KeyBoard
    for i in range(C_LOWEST, C_HIGHEST):
        note = Note(screen, i, (i - C_LOWEST) / 2)
        if note.get_rect().topright[0] > screen.get_width():
            break
        drawing_notes.append(note)
    centerize = 0
    if drawing_notes[-1].get_rect().topright[0] < screen.get_width():
        centerize = screen.get_width() - drawing_notes[-1].get_rect().topright[
            0]
    for note in drawing_notes:
        dr_obj.add(note)
        if note.get_color()[0] == BLACK:
            black_notes.append(note)
    for note in black_notes:
        drawing_notes.remove(note)
    centerize = centerize / 2
    for i in range(len(drawing_notes)):
        if not i > len(black_notes) - 1:
            black_notes[i].rect.x += centerize
        drawing_notes[i].rect.x += centerize
    return set(drawing_notes), set(black_notes)


def note_check(integer):
    for key, value in NOTES_DICTIONARY.items():
        if integer in value:
            return key


def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()


def _print_device_info():
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interface, name, input1, output, opened) = r

        in_out = ""
        if input1:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print(
            "%2i: interface :%s:, name :%s:, opened :%s:  %s"
            % (i, interface, name, opened, in_out)
        )


def chord_maker():
    root = random.randrange(C_LOWEST, C_LOWEST + 13)
    chord_name = random.choice(list(CHORDS_DICTIONARY.keys()))
    notes_in_chord = [root + i for i in CHORDS_DICTIONARY[chord_name]]
    return notes_in_chord, chord_name, root


def chord_checker(notes_pressed, cur_chord):
    temp_chord = [note % 12 for note in cur_chord[0]]
    for i, note in enumerate(notes_pressed):
        if i != len(notes_pressed) - 1:
            temp = list(notes_pressed)
            next_note = temp[temp.index(note) + 1]
            if notes_pressed[next_note] - \
                    notes_pressed[note] >= 25:
                return False
        if note % 12 not in temp_chord:
            return False
    return True


def chord_game_loop(clock, device_id=None):
    pg.init()
    pg.fastevent.init()
    event_get = pg.fastevent.get
    event_post = pg.fastevent.post
    pygame.midi.init()
    my_font = pg.font.Font(pg.font.get_default_font(), 16)
    monitor_size = [pg.display.Info().current_w, pg.display.Info().current_h]
    screen = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE)
    full_screen = False
    drawable_objects = set()
    window_pos = Window.from_display_module()

    # _print_device_info()  # For debugging and checking midi input

    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print("using input_id :%s:" % input_id)
    midi_input = pygame.midi.Input(input_id)
    chord_game = False
    cur_chord = None
    active_notes = {}
    running = True
    score = 0
    # Making KeyBoard
    b_notes, w_notes = making_notes(screen, drawable_objects)
    # all_notes = b_notes.union(w_notes)
    texts = [f"score"]
    while running:
        screen.fill(LIGHT_BLUE)
        for note in b_notes:
            note.update()
        for note in w_notes:
            note.update()

        events = event_get()
        for e in events:
            if e.type == pg.QUIT:
                running = False
            if e.type == pg.VIDEORESIZE:
                if not full_screen:
                    screen = pg.display.set_mode((e.w, e.h),
                                                 pg.RESIZABLE)
                    b_notes, w_notes = making_notes(screen,
                                                    drawable_objects)
                    for thing in drawable_objects:
                        thing.update_res()
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    running = False
                if e.key == pg.K_f:
                    full_screen = not full_screen
                    if full_screen:
                        screen = pg.display.set_mode(
                            (monitor_size[0], monitor_size[1]), pg.FULLSCREEN)
                        b_notes, w_notes = making_notes(screen,
                                                        drawable_objects)
                        for thing in drawable_objects:
                            thing.update_res()
                    else:
                        screen = pg.display.set_mode(WINDOW_SIZE,
                                                     pg.RESIZABLE)
                        window_pos.position = (200, 200)
                        b_notes, w_notes = making_notes(screen,
                                                        drawable_objects)
                        for thing in drawable_objects:
                            thing.update_res()
                if e.key == pg.K_c:
                    chord_game = True
                    if chord_game:
                        if not cur_chord:
                            cur_chord = chord_maker()
                        if cur_chord:
                            texts.append(my_font.render(f"Play the chord "
                                                        f"{note_check(cur_chord[2])} {cur_chord[1]}",
                                                        True, (0, 128, 0)))
                            print(f"Play the chord "
                                  f"{note_check(cur_chord[2])} {cur_chord[1]}")
            if e.type == pygame.midi.MIDIIN:
                input_output, note, timestamp = e.__dict__['status'], \
                                                e.__dict__['data1'], \
                                                e.__dict__['timestamp']
                # print(input_output, note, timestamp)
                if input_output == 144:
                    active_notes[note] = timestamp
                    for note_d in b_notes.union(w_notes):
                        if note == note_d.get_num():
                            note_d.press()
                if input_output == 128:
                    del active_notes[note]
                    for note_d in b_notes.union(w_notes):
                        if note == note_d.get_num():
                            note_d.press()
                if chord_game:
                    if not cur_chord:
                        cur_chord = chord_maker()
                    if len(active_notes) == 3:
                        if chord_checker(active_notes, cur_chord):
                            texts = []
                            texts.append(
                                my_font.render("GOOD JOB!", True, (0, 128, 0)))
                            print("GOOD JOB!")
                            cur_chord = chord_maker()
                            score += 1
                        else:
                            texts = []
                            print("TOO BAD! TRY AGAIN")
                            texts.append(
                                my_font.render("TOO BAD! TRY AGAIN", True,
                                               (0, 128, 0)))
                            score -= 1
                        if cur_chord:
                            texts.append(
                                my_font.render(f"Our current chord is "
                                               f"{note_check(cur_chord[2])} {cur_chord[1]}",
                                               True, (0, 128, 0)))
                            print(f"Our current chord is "
                                  f"{note_check(cur_chord[2])} {cur_chord[1]}"
                                  f"\nYour score is {score}")
        if midi_input.poll():
            midi_events = midi_input.read(10)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events,
                                                midi_input.device_id)

            for m_e in midi_evs:
                event_post(m_e)
        texts[0] = my_font.render(f"Your score is: {score}", True, (0, 128, 0))
        for i in range(len(texts)):
            screen.blit(texts[i], (
            screen.get_width() // 4, screen.get_height() // (3 + i)))
        pg.display.update()
        clock.tick(60)

    del midi_input
    pygame.midi.quit()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_trainer()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
