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


def scale_maker():
    root = random.randrange(C_LOWEST, C_LOWEST + 13)
    scale_name = random.choice(list(SCALES_DICTIONARY.keys()))
    notes_in_scale = [root + i for i in SCALES_DICTIONARY[scale_name]]
    return notes_in_scale, scale_name, root


def scale_checker(notes_pressed, cur_scale):
    temp_scale = [note % 12 for note in cur_scale[0]]
    temp = list(notes_pressed)
    if temp[0] % 12 == temp_scale[0]:
        cur_scale[0].pop(0)
        return True
    return False


def input_main(device_id=None):
    pg.init()
    pg.fastevent.init()
    event_get = pg.fastevent.get
    event_post = pg.fastevent.post

    pygame.midi.init()

    _print_device_info()

    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print("using input_id :%s:" % input_id)
    i = pygame.midi.Input(input_id)
    pg.display.set_mode((1, 1))
    scale_game = False
    cur_scale = None
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
                    scale_game = True
                    if scale_game:
                        if not cur_scale:
                            cur_scale = scale_maker()
                        if cur_scale:
                            print(f"Our current scale is "
                                  f"{note_check(cur_scale[2])} {cur_scale[1]}")
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

                input_output, note, timestamp\
                    = e.__dict__['status'], \
                                                e.__dict__['data1'], \
                                                e.__dict__['timestamp']
                if input_output == 144:
                    active_notes[note] = timestamp
                    # print(note_check(note))
                if input_output == 128:
                    del active_notes[note]
                if scale_game:
                    if not cur_scale:
                        cur_scale = scale_maker()
                    if len(active_notes) == 1:
                        print(f"You pressed the note {note_check(list(active_notes)[0])}")

                        if scale_checker(active_notes, cur_scale):
                            if not cur_scale[0]:
                                print("GOOD JOB!")
                                cur_scale = scale_maker()
                                score += 1
                                print(f"Our current scale is "
                                      f"{note_check(cur_scale[2])} {cur_scale[1]}"
                                      f"\nYour score is {score}")

                        else:
                            print("TOO BAD! TRY AGAIN")
                            score -= 1

        if i.poll():
            midi_events = i.read(10)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            for m_e in midi_evs:
                event_post(m_e)

    del i
    pygame.midi.quit()


input_main()
