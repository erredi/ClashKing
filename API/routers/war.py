
import coc
import operator

from collections import defaultdict
from fastapi import  Request, Response, HTTPException
from fastapi import APIRouter
from fastapi_cache.decorator import cache
from typing import List
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from .utils import fix_tag, capital, leagues, cwl_groups, clan_wars, war_logs_db, basic_clan
from datetime import datetime

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(tags=["War Endpoints"])


#WAR STATS
@router.get("/war/{clan_tag}/log",
         tags=["War Endpoints"],
         name="Warlog for a clan, filled in with data where possible")
@cache(expire=300)
@limiter.limit("30/second")
async def war_log(clan_tag: str, request: Request, response: Response, limit: int= 50):
    clan_tag = fix_tag(clan_tag)
    clan_results = await war_logs_db.find({"clan.tag" : clan_tag}).to_list(length=None)
    opponent_results = await war_logs_db.find({"opponent.tag" : clan_tag}).to_list(length=None)

    data_ids = list(set([result["endTime"] for result in clan_results] + [result["endTime"] for result in opponent_results]))
    full_wars = await clan_wars.find({"$and" : [{"$or" : [{"data.clan.tag" : clan_tag}, {"data.opponent.tag" : clan_tag}]},{"data.endTime" : {"$in" : data_ids}}]}).to_list(length=None)
    wars_by_endtime = {}
    for war in full_wars:
        try:
            del war["data"]["_response_retry"]
        except:
            pass
        wars_by_endtime[war["data"]["endTime"]] = war["data"]

    times_alr_found = set()
    actual_results = []
    for result in clan_results:
        del result["_id"]
        if wars_by_endtime.get(result["endTime"]) is not None:
            result["data"] = wars_by_endtime.get(result["endTime"])
        actual_results.append(result)
        times_alr_found.add(result["timeStamp"])

    for result in opponent_results:
        if result["timeStamp"] not in times_alr_found:
            del result["_id"]
            if result["result"] == "win":
                result["result"] = "lose"
            elif result["result"] == "lose":
                result["result"] = "win"
            old_opponent = result["opponent"]
            result["opponent"] = result["clan"]
            result["clan"] = old_opponent
            result["clan"]["attacks"] = 0
            result["clan"]["expEarned"] = 0
            if wars_by_endtime.get(result["endTime"]) is not None:
                result["data"] = wars_by_endtime.get(result["endTime"])
            actual_results.append(result)

    actual_results = sorted(actual_results, key=lambda x: x["timeStamp"], reverse=True)
    return actual_results[:limit]


@router.get("/war/{clan_tag}/previous",
         tags=["War Endpoints"],
         name="Previous Wars for a clan")
@cache(expire=300)
@limiter.limit("30/second")
async def war_previous(clan_tag: str, request: Request, response: Response, limit: int= 50):
    clan_tag = fix_tag(clan_tag)
    full_wars = await clan_wars.find({"$and" : [{"$or" : [{"data.clan.tag" : clan_tag}, {"data.opponent.tag" : clan_tag}]}]}).to_list(length=None)
    found_ids = set()
    new_wars = []
    for war in full_wars:
        id = war.get("data").get("preparationStartTime")
        if id in found_ids:
            continue
        try:
            del war["_response_retry"]
        except:
            pass
        new_wars.append(war.get("data"))
        found_ids.add(id)

    actual_results = sorted(new_wars, key=lambda x: x.get("endTime", 0), reverse=True)
    return actual_results[:limit]


@router.get("/war/{clan_tag}/basic",
         tags=["War Endpoints"],
         name="Basic War Info, Bypasses Private War Log if Possible")
@cache(expire=300)
@limiter.limit("30/second")
async def basic_war_info(clan_tag: str, request: Request, response: Response):
    now = datetime.utcnow().timestamp() - 183600
    result = await clan_wars.find_one({"$and" : [{"clan" : fix_tag(clan_tag)}, {"custom_id": None}, {"endTime" : {"$gte" : now}}]})
    if result is None:
        result = await clan_wars.find_one({"$and" : [{"opponent" : fix_tag(clan_tag)}, {"custom_id" : None}, {"endTime" : {"$gte" : now}}]})
    if result is not None:
        del result["_id"]
    return result

@router.get("/cwl/{clan_tag}/{season}",
         tags=["War Endpoints"],
         name="Cwl Info for a clan in a season (yyyy-mm)")
@cache(expire=300)
@limiter.limit("30/second")
async def cwl(clan_tag: str, season: str, request: Request, response: Response):
    clan_tag = fix_tag(clan_tag)
    cwl_result = await cwl_groups.find_one({"$and" : [{"data.clans.tag" : clan_tag}, {"data.season" : season}]})

    rounds = cwl_result.get("data").get("rounds")
    war_tags = []
    for round in rounds:
        for tag in round.get("warTags"):
            war_tags.append(tag)
    matching_wars = await clan_wars.find({"data.tag" : {"$in" : war_tags}}).to_list(length=None)
    matching_wars = {w.get("data").get("tag") : w.get("data") for w in matching_wars}
    for r_count, round in enumerate(rounds):
        for count, tag in enumerate(round.get("warTags")):
            rounds[r_count].get("warTags")[count] = matching_wars.get(tag)
    cwl_result = cwl_result["data"]
    cwl_result["rounds"] = rounds
    cwl_result["clan_rankings"] = ranking_create(data=cwl_result)
    return cwl_result


def ranking_create(data: dict):

    star_dict = defaultdict(int)
    dest_dict = defaultdict(int)
    tag_to_name = defaultdict(str)
    rounds_won = defaultdict(int)
    rounds_lost = defaultdict(int)
    rounds_tied = defaultdict(int)

    for round in data.get("rounds"):
        for war in round.get("warTags"):
            war = coc.ClanWar(data=war, client=None)
            if str(war.status) == "won":
                rounds_won[war.clan.tag] += 1
                rounds_lost[war.opponent.tag] += 1
                star_dict[war.clan.tag] += 10
            elif str(war.status) == "lost":
                rounds_won[war.opponent.tag] += 1
                rounds_lost[war.clan.tag] += 1
                star_dict[war.opponent.tag] += 10
            else:
                rounds_tied[war.clan.tag] += 1
                rounds_tied[war.opponent.tag] += 1

            tag_to_name[war.clan.tag] = war.clan.name
            tag_to_name[war.opponent.tag] = war.opponent.name
            on_each_player = {}
            for player in war.members:
                for attack in player.attacks:
                    if on_each_player.get(attack.defender_tag) is None:
                        on_each_player[attack.defender_tag] = (attack, player.clan.tag)
                    else:
                        prev, clan_tag = on_each_player.get(attack.defender_tag)
                        if attack.stars > prev.stars or (attack.stars == prev.stars and attack.destruction > prev.destruction):
                            on_each_player[attack.defender_tag] = (attack, player.clan.tag)

            for attack, clan_tag in on_each_player.values():
                star_dict[clan_tag] += attack.stars
                dest_dict[clan_tag] += attack.destruction

    star_list = []
    for tag, stars in star_dict.items():
        destruction = dest_dict[tag]
        name = tag_to_name[tag]
        star_list.append([name, tag, stars, destruction])

    sorted_list = sorted(star_list, key=operator.itemgetter(2, 3), reverse=True)
    return  [{"name" : x[0], "tag" : x[1], "stars": x[2], "destruction" : x[3],
              "rounds" : {"won" : rounds_won.get(x[1], 0), "tied" : rounds_tied.get(x[1], 0), "lost" : rounds_lost.get(x[1], 0)}} for x in sorted_list]

