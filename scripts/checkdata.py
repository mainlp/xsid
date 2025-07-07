import os
import myutils
rootDir = 'data/xSID-0.7/'

def checkText(path):
    counter = 0
    curText = ''
    words = []
    for lineIdx, line in enumerate(open(path)):
        if line.startswith('# text = '):
            if ''.join(words) != curText.replace(' ', '') and curText != '':
                print('MISMATCH in ' + path + ': ' + str(lineIdx) )
                print(' '.join(words))
                print(curText)
                print(''.join(words))
                print(curText.replace(' ', ''))
                print()
                counter += 1
            curText = line[8:].strip()
            words = []
        if len(line.split('\t')) == 4:
            words.append(line.split('\t')[1])


def checkBIO(path):
    labels = []
    for lineIdx, line in enumerate(open(path)):
        if line.startswith('# text = '):
            for label_idx in range(len(labels)):
                if labels[label_idx][0] == 'I':
                    if labels[label_idx-1][1:] != labels[label_idx][1:] or label_idx == 0:
                        print('invalid BIO sequence', path, lineIdx)
            labels = []
        if len(line.split('\t')) == 4:
            labels.append(line.strip().split('\t')[3])


def checkFormat(path):
    all_slot_labels = ["alarm/alarm_modifier", "album", "artist", "best_rating", "condition_description", "condition_temperature", "cuisine", "datetime", "entity_name", "facility", "genre", "location", "movie_name", "movie_type", "music_item", "negation", "news/type", "object_location_type", "object_name", "object_part_of_series_type", "object_select", "object_type", "party_size_description", "party_size_number", "playlist", "rating_unit", "rating_value", "recurring_datetime", "reference", "reminder/reminder_modifier", "reminder/todo", "restaurant_name", "restaurant_type", "served_dish", "service", "sort", "timer/attributes", "track", "weather/attribute", "weather/temperatureUnit", 'reference-part']
    all_intents = ["AddToPlaylist", "BookRestaurant", "PlayMusic", "RateBook", "SearchCreativeWork", "SearchScreeningEvent", "alarm/cancel_alarm", "alarm/modify_alarm", "alarm/set_alarm", "alarm/show_alarms", "alarm/snooze_alarm", "alarm/time_left_on_alarm", "reminder/cancel_reminder", "reminder/set_reminder", "reminder/show_reminders", "weather/checkSunrise", "weather/checkSunset", "weather/find"]
    cur_sent = []
    for lineIdx, line in enumerate(open(path)):
        if len(line.strip()) < 2:
            # check for number of columns, and numbers in column 1
            num_comments = len([piece for piece in cur_sent if piece[0] == '#'])
            for pieceIdx, piece in enumerate(cur_sent[num_comments:]):
                if len(piece.split('\t')) != 4:
                    print('incorrect number of columns: ', lineIdx)
                if str(pieceIdx +1) != piece.split('\t')[0]:
                    print('incorrect numbering  of words: ', path, lineIdx)
            # check for text-en, text, id, intent. Strip all
            if 'en.' not in path and 'no.' not in path:
                num_en = len([piece for piece in cur_sent if piece.startswith('# text-en')])
                if num_en != 1:
                    print('not 1 text-en found', path, lineIdx)
            num_txt = len([piece for piece in cur_sent if piece.startswith('# text ')])
            if num_txt != 1:
                print('not 1 text found', path, lineIdx)
            num_id = len([piece for piece in cur_sent if piece.startswith('# id')])
            if num_id != 1 and 'en.' not in path:
                print('not 1 id found', path, lineIdx)
            num_intent = len([piece for piece in cur_sent if piece.startswith('# intent')])
            if num_intent != 1:
                print('not 1 inent found', path, lineIdx)
            intent = [piece for piece in cur_sent if piece.startswith('# intent')][0]
            intent = intent.split(' ')[-1]
            if intent not in all_intents:
                print('not a valid intent label', intent, path, lineIdx)
            for piece in cur_sent[num_comments:]:
                slot_label = piece.split('\t')[3]
                if slot_label == 'O':
                    continue
                slot_label = slot_label[2:]
                if slot_label not in all_slot_labels:
                    print('not a valid slot label', slot_label, path, lineIdx)
                
            cur_sent = []
        else:
            cur_sent.append(line.strip())

for conllFile in sorted(os.listdir(rootDir)):
    if conllFile[0] == '.':
        continue
    if 'train' in conllFile:
        continue
    checkText(rootDir + conllFile)
    checkBIO(rootDir + conllFile)
    checkFormat(rootDir + conllFile)

