import csv, json

def read_csv(fname):
    try:
        with open(fname, encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except:
        return []

base = 'ipl_stats/'
seasons = ['2019','2023','2024','2025','2026']

print("=== TOP RUN SCORERS ALL TIME ===")
rows = read_csv(base+'alltime_toprunsscorers.csv')
for r in rows[:10]:
    print(r.get('StrikerName',''), r.get('TeamName',''), r.get('TotalRuns',''), r.get('Matches',''), r.get('BattingAverage',''), r.get('StrikeRate',''), r.get('Centuries',''), r.get('FiftyPlusRuns',''), r.get('HighestScore',''))

print()
print("=== TOP WICKET TAKERS ALL TIME ===")
rows = read_csv(base+'alltime_mostwickets.csv')
for r in rows[:10]:
    print(r.get('BowlerName',''), r.get('TeamName',''), r.get('Wickets',''), r.get('Matches',''), r.get('BowlingAverage',''), r.get('EconomyRate',''), r.get('BBIW',''))

print()
print("=== ALL TIME MOST SIXES ===")
rows = read_csv(base+'alltime_mostsixes.csv')
for r in rows[:10]:
    print(r.get('StrikerName',''), r.get('TeamName',''), r.get('Sixes',''), r.get('StrikeRate',''))

print()
print("=== ALL TIME MOST FOURS ===")
rows = read_csv(base+'alltime_mostfours.csv')
for r in rows[:10]:
    print(r.get('StrikerName',''), r.get('TeamName',''), r.get('Fours',''))

print()
print("=== ALL TIME MOST CENTURIES ===")
rows = read_csv(base+'alltime_mostcenturies.csv')
for r in rows[:10]:
    print(r.get('StrikerName',''), r.get('TeamName',''), r.get('Centuries',''), r.get('HighestScore',''))

print()
print("=== ALL TIME MOST FIFTIES ===")
rows = read_csv(base+'alltime_mostfifties.csv')
for r in rows[:10]:
    print(r.get('StrikerName',''), r.get('TeamName',''), r.get('FiftyPlusRuns',''))

print()
print("=== ALL TIME HAT-TRICKS ===")
rows = read_csv(base+'alltime_mosthattricks.csv')
print('Columns:', list(rows[0].keys()) if rows else 'empty')
for r in rows[:10]:
    print(r)

print()
print("=== ALL TIME BEST BOWLING FIGURES ===")
rows = read_csv(base+'alltime_bestbowlingfigures.csv')
print('Columns:', list(rows[0].keys()) if rows else 'empty')
for r in rows[:10]:
    print(r)

print()
print("=== SEASON-BY-SEASON TOP SCORERS ===")
for s in seasons:
    rows = read_csv(base+s+'_toprunsscorers.csv')
    if rows:
        r = rows[0]
        print(f"{s}: {r.get('StrikerName','')} ({r.get('TeamName','')}) - {r.get('TotalRuns','')} runs, {r.get('Matches','')} matches, avg {r.get('BattingAverage','')}, SR {r.get('StrikeRate','')}")

print()
print("=== SEASON-BY-SEASON TOP WICKET TAKERS ===")
for s in seasons:
    rows = read_csv(base+s+'_mostwickets.csv')
    if rows:
        r = rows[0]
        print(f"{s}: {r.get('BowlerName','')} ({r.get('TeamName','')}) - {r.get('Wickets','')} wkts, avg {r.get('BowlingAverage','')}, eco {r.get('EconomyRate','')}")

print()
print("=== SEASON-BY-SEASON MOST SIXES ===")
for s in seasons:
    rows = read_csv(base+s+'_mostsixes.csv')
    if rows:
        r = rows[0]
        print(f"{s}: {r.get('StrikerName','')} - {r.get('Sixes','')} sixes")

print()
print("=== METEORS REPORT OUTPUT ===")
rows = read_csv('output/meteors.csv')
print('Columns:', list(rows[0].keys()) if rows else 'empty')
for r in rows:
    print(r)

print()
print("=== PLAYER CAREERS SAMPLE ===")
rows = read_csv('output/player_careers.csv')
print('Columns:', list(rows[0].keys()) if rows else 'empty')
for r in rows[:5]:
    print(r)

print()
print("=== BATTING SEASONS CLEAN SAMPLE ===")
rows = read_csv('output/batting_seasons_clean.csv')
print('Columns:', list(rows[0].keys()) if rows else 'empty')
for r in rows[:5]:
    print(r)
