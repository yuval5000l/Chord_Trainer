import pygame as pg
import pygame.midi
from settings import *
import random


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


def input_main(device_id=None):
    pg.init()
    pg.fastevent.init()
    event_get = pg.fastevent.get
    event_post = pg.fastevent.post

    pygame.midi.init()

    # _print_device_info()  # For debugging and checking midi input

    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print("using input_id :%s:" % input_id)
    i = pygame.midi.Input(input_id)
    pg.display.set_mode((1, 1))
    chord_game = False
    cur_chord = None
    active_notes = {}
    running = True
    score = 0
    while running:
        events = event_get()
        for e in events:
            if e.type == pg.QUIT:
                running = False
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    running = False
                if e.key == pg.K_c:
                    chord_game = True
                    if chord_game:
                        if not cur_chord:
                            cur_chord = chord_maker()
                        if cur_chord:
                            print(f"Our current chord is "
                                  f"{note_check(cur_chord[2])} {cur_chord[1]}")
            if e.type == pygame.midi.MIDIIN:
                # print(e)
                # print(e.__dict__['status']) # If status == 144 it's input,
                # 128 is output
                # print(e.__dict__["data2"]) # I think that this is the power
                # (or volume), always returns as 64 in the output
                # print(e.__dict__["data3"]) # Always 0, not sure what this is
                # print(e.__dict__["timestamp"]) # Shows the timestamp of
                # our note
                # print(e.__dict__['data1'])  # It's our note!
                # print(note_check(e.__dict__['data1']))

                input_output, note, timestamp = e.__dict__['status'], \
                                                e.__dict__['data1'], \
                                                e.__dict__['timestamp']
                if input_output == 144:
                    active_notes[note] = timestamp
                    # print(note_check(note))
                if input_output == 128:
                    del active_notes[note]
                if chord_game:
                    if not cur_chord:
                        cur_chord = chord_maker()
                    if len(active_notes) == 3:
                        if chord_checker(active_notes, cur_chord):
                            print("GOOD JOB!")
                            cur_chord = chord_maker()
                            score += 1
                        else:
                            print("TOO BAD! TRY AGAIN")
                            score -= 1
                        if cur_chord:
                            print(f"Our current chord is "
                                  f"{note_check(cur_chord[2])} {cur_chord[1]}"
                                  f"\nYour score is {score}")
        if i.poll():
            midi_events = i.read(10)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            for m_e in midi_evs:
                event_post(m_e)

    del i
    pygame.midi.quit()


input_main()
