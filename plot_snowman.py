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
start_day = datetime.datetime(2018,3,7,0,0,0)
parsed = []
time_format = '%d.%m.%Y %H:%M:%S'
now = datetime.datetime.now()
day_diff = (now-start_day).days

for g in guess:
    parse = tregex.name('^(?P<name>.*?),(?P<time>\d.*\d)$', g)[0]
    try:
        parse['time'] = datetime.datetime.strptime(parse['time'], '%d.%m.%Y %H:%M')
    except:
        parse['time'] = datetime.datetime.strptime(parse['time'], time_format)
    parse['diff'] = (now-parse['time']).total_seconds()
    parse['abs_diff'] = abs(parse['diff'])
    parsed += [parse]

parsed = sorted(parsed, key=lambda x: x['diff'], reverse=True)

def get_name(items):
    if not items:
        return 'ingen'
    else:
        return '@'+', @'.join([i['name'] for i in items])

closest = [min(parsed, key=lambda x: x['abs_diff'])]
out = [candidate for candidate in parsed if candidate['diff']>0 and candidate not in closest]
rest = [candidate for candidate in parsed if not candidate in closest + out]
print(f'Dag {day_diff}: Snømannen står fremdeles!\n'
      f'Men hvis snømannen faller NÅ, så er:\n'
      f'Nærmest: {get_name(closest)}\n'
      f'Resten (kronologisk): {get_name(rest)}\n'
      f'Ute av gamet: {get_name(out)}\n'
      f'#harsnømannenfalt')

timesplit = []
previous = closest[0]
for current in rest:
    diff = current['time'] - previous['time']
    split_time = previous['time'] + diff/2

    tot = diff.total_seconds()
    hours = floor(tot / 3600)
    minutes = floor(fmod(tot, 3600) / 60)
    seconds = fmod(tot, 60)
    timesplit += [f'    {hours:02d}:{minutes:02d}:{seconds:02.0f}']
    timesplit += ['{} - {}'.format(split_time.strftime('%d.%m %H:%M:%S'),'@'+current['name'])]
    previous = current

for p in timesplit:
    print(p)




