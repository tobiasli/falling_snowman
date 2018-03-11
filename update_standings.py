import tregex
import datetime
from math import fmod, floor

guess = '''runarws,08.03.2018 08:00
tiram1990,09.03.2018 09:03:18
linetysdahl,09.03.2018 11:00
askeladden29,15.03.2018 04:25
finnkr,09.03.2018 12:01
tinarenate,13.03.2018 16:07
runakv,13.03.2018 13:05
margmo,30.03.2018 12:32
siri_fors,10.03.2018 13:45
idaeris,17.03.2018 17:13
marijohannaa,12.03.2018 13:34
margarethaurora,11.03.2018 20:41
broxplots,14.03.2018 12:00
c.aanerud,15.03.2018 14:30'''

guess = guess.split('\n')
start_day = datetime.datetime(2018, 3, 7, 0, 0, 0)
parsed = []
time_format = '%d.%m.%Y %H:%M:%S'
now = datetime.datetime.now()
day_diff = (now - start_day).days

for g in guess:
    parse = tregex.name('^(?P<name>.*?),(?P<time>\d.*\d)$', g)[0]
    try:
        parse['time'] = datetime.datetime.strptime(parse['time'], '%d.%m.%Y %H:%M')
    except:
        parse['time'] = datetime.datetime.strptime(parse['time'], time_format)
    parse['diff'] = (now - parse['time']).total_seconds()
    parse['abs_diff'] = abs(parse['diff'])
    parsed += [parse]

parsed = sorted(parsed, key=lambda x: x['diff'], reverse=True)

# Calculate split_times:
previous = None
for current in parsed:
    if previous:
        diff = current['time'] - previous['time']
        split_time = previous['time'] + diff / 2
        current['split_time'] = split_time

        # Get timespan:
        if 'split_time' in previous:
            current['timespan'] = current['split_time'] - previous['split_time']

    previous = current


def _get_name(items):
    if not items:
        return 'ingen'
    else:
        return '@' + ', @'.join([i['name'] for i in items])


def _get_split_time_as_str(user):
    if not 'split_time' in user:
        return '∞'
    else:
        return user['split_time'].strftime('%d.%m %H:%M:%S')


def _get_timespan_as_str(user):
    if not 'timespan' in user:
        return '∞'
    tot = user['timespan'].total_seconds()
    hours = floor(tot / 3600)
    minutes = floor(fmod(tot, 3600) / 60)
    seconds = fmod(tot, 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02.0f}'


def print_standings():
    closest = [min(parsed, key=lambda x: x['abs_diff'])]
    out = sorted([candidate for candidate in parsed if candidate['diff'] > 0 and candidate not in closest], key= lambda x: x['diff'])
    rest = [candidate for candidate in parsed if not candidate in closest + out]
    print(f'Dag {day_diff}: Snømannen står fremdeles!\n'
          f'Men hvis snømannen faller NÅ, så er:\n'
          f'Nærmest: {_get_name(closest)}\n'
          f'Resten (kronologisk): {_get_name(rest)}\n'
          f'Ute av gamet: {_get_name(out)}\n'
          f'#harsnømannenfalt')

def print_split_times():
    timesplit = []
    for user in parsed:
        timesplit += [_get_timespan_as_str(user)]
        timesplit += ['{} - {}'.format(_get_split_time_as_str(user), '@' + user['name'])]

    for p in timesplit:
        print(p)

if __name__ == '__main__':
    print_standings()