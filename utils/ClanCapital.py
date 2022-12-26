from datetime import datetime
from datetime import timedelta
import datetime as dt
from coc.miscmodels import Timestamp
from coc.raid import RaidLogEntry
import coc
import pytz
utc = pytz.utc

def gen_raid_weekend_datestrings(number_of_weeks: int):
    weekends = []
    for x in range(number_of_weeks):
        now = datetime.utcnow().replace(tzinfo=utc)
        now = now - timedelta(x * 7)
        current_dayofweek = now.weekday()
        if (current_dayofweek == 4 and now.hour >= 7) or (current_dayofweek == 5) or (current_dayofweek == 6) or (
                current_dayofweek == 0 and now.hour < 7):
            if current_dayofweek == 0:
                current_dayofweek = 7
            fallback = current_dayofweek - 4
            raidDate = (now - timedelta(fallback)).date()
        else:
            forward = 4 - current_dayofweek
            raidDate = (now + timedelta(forward)).date()
        weekends.append(str(raidDate))
    return weekends

def weekend_to_cocpy_timestamp(weekend: str, end=False) -> coc.Timestamp:
    weekend_to_iso = datetime.strptime(weekend, "%Y-%m-%d")
    weekend_to_iso = weekend_to_iso.replace(hour=7)
    if end:
        weekend_to_iso = weekend_to_iso + timedelta(days=3)
    return Timestamp(data=weekend_to_iso.strftime('%Y%m%dT%H%M%S.000Z'))

async def get_raidlog_entry(clan: coc.Clan, weekend: str, bot):
    raidlog = await bot.coc_client.get_raidlog(clan.tag)
    weekend_timestamp = weekend_to_cocpy_timestamp(weekend)
    weekend_raid: RaidLogEntry = coc.utils.get(raidlog, start_time=weekend_timestamp)
    if weekend_raid is not None and sum(member.capital_resources_looted for member in weekend_raid.members) != 0:
        return weekend_raid
    else:
        raid_data = await bot.raid_weekend_db.find_one({"clan_tag" : clan.tag, "data.startTime" : f"{weekend_timestamp.time.strftime('%Y%m%dT%H%M%S.000Z')}"})
        if raid_data is not None:
            entry: RaidLogEntry = RaidLogEntry(data=raid_data.get("data"), client=bot.coc_client)
            return entry

    raid_data = await player_results_to_json(clan=clan, weekend=weekend, player_stats=bot.player_stats)
    if raid_data is not None:
        return RaidLogEntry(data=raid_data, client=bot.coc_client)
    return None

async def player_results_to_json(clan: coc.Clan, weekend: str, player_stats):
    tags = await player_stats.distinct("tag", filter={f"capital_gold.{weekend}.raided_clan": clan.tag})
    if not tags:
        return None
    all_players = await player_stats.find({f"capital_gold.{weekend}.raided_clan": clan.tag}).to_list(length=100)
    member_list = []
    for player in all_players:
        player_cc = player.get("capital_gold")
        if player_cc is None:
            continue
        player_cc = player_cc.get(f"{weekend}")
        if player_cc is None:
            continue
        raided_amount = player_cc.get("raid")
        if raided_amount is None:
            raided_amount = player_cc.get("raided")
            if raided_amount is None:
                continue
            raided_amount = [raided_amount]
        limit_hits = player_cc.get("limit_hits")
        if limit_hits is None:
            limit_hits = max(len(raided_amount), 5)
            limit_hits = min(limit_hits, 6)
        member_list.append({
            "tag" : player.get("tag"),
            "name" : player.get("name"),
            "attacks" : len(raided_amount),
            "attackLimit" : limit_hits,
            "bonusAttackLimit" : 0,
            "capitalResourcesLooted" : sum(raided_amount)
        })
    if not member_list:
        return None
    return {
      "state": "ended",
      "startTime": weekend_to_cocpy_timestamp(weekend).time.strftime('%Y%m%dT%H%M%S.000Z'),
      "endTime": weekend_to_cocpy_timestamp(weekend, end=True).time.strftime('%Y%m%dT%H%M%S.000Z'),
      "capitalTotalLoot": 0,
      "raidsCompleted": 0,
      "totalAttacks": 0,
      "enemyDistrictsDestroyed": 0,
      "offensiveReward": 0,
      "defensiveReward": 0,
      "members": member_list,
      "attackLog": []
    }
