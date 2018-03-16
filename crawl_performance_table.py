from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import time

driver = webdriver.Chrome()
#driver = webdriver.Safari()
start_url = "https://www.whoscored.com/Regions/108/Tournaments/5/Seasons/6461/Stages/14014/Fixtures/Italy-Serie-A-2016-2017"
driver.get(start_url)

# Find the link of each match
match_table = {}

prev_month_button = driver.find_element_by_xpath("//*[@id=\"date-controller\"]/a[1]")
prev_button_status = prev_month_button.get_attribute("title")
previous_month = ""
current_month = driver.find_element_by_xpath("//*[@id=\"date-config-toggle-button\"]/span[1]").text

while (prev_button_status == "View previous month"):
    while (current_month == previous_month):
        prev_month_button.click()
        time.sleep(1)
        current_month = driver.find_element_by_xpath("//*[@id=\"date-config-toggle-button\"]/span[1]").text
        prev_button_status = prev_month_button.get_attribute("title")

    while True:
        try:
            # match_table = {}
            trs = driver.find_elements_by_xpath("//*[@id=\"tournament-fixture\"]/tbody/tr")

            for tr in trs:
                tds = tr.find_elements_by_xpath("td")
                if(len(tds)):
                    match_id = tr.get_attribute("data-id")
                    match_table[match_id] = {}
                for i, td in enumerate(tds):
                    if(i == 4):
                        match_table[match_id]["match_link"] = td.find_element_by_tag_name("a").get_attribute("href")
            break
        except:
            print("wait")
            time.sleep(0.5)

    previous_month = current_month

# Crawl data of each match performance
performance_table = {}

print("Total number of matches:{}.".format(len(match_table)))
cnt = 1
subdriver = webdriver.Chrome()
for match_id, match_details in match_table.items():
    performance_table[match_id] = {}
    match_link = match_details["match_link"]
    # Change into the match page
    print(">>> {}: Crawling {}...".format(cnt, match_id))
    cnt += 1
    
    subdriver.get(match_link)
    # Change into player statistic page
    subdriver.get(subdriver.find_element_by_xpath("//*[@id=\"sub-sub-navigation\"]/ul/li[2]/a").get_attribute("href"))
    time.sleep(1)

    # Click through all player statistic tables such that they can be loaded
    home_offensive_button = subdriver.find_element_by_xpath("//*[@id=\"live-player-home-options\"]/li[2]/a")
    home_offensive_button.click()
    home_defensive_button = subdriver.find_element_by_xpath("//*[@id=\"live-player-home-options\"]/li[3]/a")
    home_defensive_button.click()
    home_passing_button = subdriver.find_element_by_xpath("//*[@id=\"live-player-home-options\"]/li[4]/a")
    home_passing_button.click()
    away_offensive_button = subdriver.find_element_by_xpath("//*[@id=\"live-player-away-options\"]/li[2]/a")
    away_offensive_button.click()
    away_defensive_button = subdriver.find_element_by_xpath("//*[@id=\"live-player-away-options\"]/li[3]/a")
    away_defensive_button.click()
    away_passing_button = subdriver.find_element_by_xpath("//*[@id=\"live-player-away-options\"]/li[4]/a")
    away_passing_button.click()
    # Crawl match performance .find_element_by_id("player-table-statistics-body").find_elements_by_tag_name("tr")
    home_offensive_trs = subdriver.find_element_by_xpath("//*[@id=\"statistics-table-home-offensive\"]").find_elements_by_xpath("//*[@id=\"player-table-statistics-body\"]/tr")
    home_defensive_trs = subdriver.find_element_by_xpath("//*[@id=\"statistics-table-home-defensive\"]").find_elements_by_xpath("//*[@id=\"player-table-statistics-body\"]/tr")
    home_passing_trs = subdriver.find_element_by_xpath("//*[@id=\"statistics-table-home-passing\"]").find_elements_by_xpath("//*[@id=\"player-table-statistics-body\"]/tr")
    away_offensive_trs = subdriver.find_element_by_xpath("//*[@id=\"statistics-table-away-offensive\"]").find_elements_by_xpath("//*[@id=\"player-table-statistics-body\"]/tr")
    away_defensive_trs = subdriver.find_element_by_xpath("//*[@id=\"statistics-table-away-defensive\"]").find_elements_by_xpath("//*[@id=\"player-table-statistics-body\"]/tr")
    away_passing_trs = subdriver.find_element_by_xpath("//*[@id=\"statistics-table-away-passing\"]").find_elements_by_xpath("//*[@id=\"player-table-statistics-body\"]/tr")
    total_offensive_trs = home_offensive_trs + away_offensive_trs
    total_defensive_trs = home_defensive_trs + away_defensive_trs
    total_passing_trs = home_passing_trs + away_passing_trs
                  
    for tr in total_offensive_trs:
        player_id = int(re.findall(r'\d+', tr.find_element_by_class_name("player-link").get_attribute("href"))[0])
        performance_table[match_id][player_id] = {}
        
        total_shots = tr.find_element_by_class_name("ShotsTotal ").text
        ot_shots = tr.find_element_by_class_name("ShotOnTarget ").text
        key_passes = tr.find_element_by_class_name("KeyPassTotal ").text
        dribbles = tr.find_element_by_class_name("DribbleWon ").text
        foul_given = tr.find_element_by_class_name("FoulGiven ").text
        offsides = tr.find_element_by_class_name("OffsideGiven ").text
        disp = tr.find_element_by_class_name("Dispossessed ").text
        uns_touches = tr.find_element_by_class_name("Turnover ").text
        key_events_icons = tr.find_elements_by_class_name("incident-icon")
        key_events = ["{},{},{}".format(icon.get_attribute("data-type"), icon.get_attribute("data-minute"), icon.get_attribute("data-second")) for icon in key_events_icons]
        
        performance_table[match_id][player_id]["total_shots"] = total_shots
        performance_table[match_id][player_id]["ot_shots"] = ot_shots
        performance_table[match_id][player_id]["key_passes"] = key_passes
        performance_table[match_id][player_id]["dribbles"] = dribbles
        performance_table[match_id][player_id]["foul_given"] = foul_given
        performance_table[match_id][player_id]["offsides"] = offsides
        performance_table[match_id][player_id]["disp"] = disp
        performance_table[match_id][player_id]["uns_touches"] = uns_touches
        performance_table[match_id][player_id]["key_events"] = key_events
        
    for tr in total_defensive_trs:
        player_id = int(re.findall(r'\d+', tr.find_element_by_class_name("player-link").get_attribute("href"))[0])
        
        total_tackles = tr.find_element_by_class_name("TackleWonTotal ").text
        interception = tr.find_element_by_class_name("InterceptionAll ").text
        clearances = tr.find_element_by_class_name("ClearanceTotal ").text
        blocked_shots = tr.find_element_by_class_name("ShotBlocked ").text
        fouls_committed = tr.find_element_by_class_name("FoulCommitted ").text
        
        performance_table[match_id][player_id]["total_tackles"] = total_tackles
        performance_table[match_id][player_id]["interception"] = interception
        performance_table[match_id][player_id]["clearances"] = clearances
        performance_table[match_id][player_id]["blocked_shots"] = blocked_shots
        performance_table[match_id][player_id]["fouls_committed"] = fouls_committed
    
    for tr in total_passing_trs:
        player_id = int(re.findall(r'\d+', tr.find_element_by_class_name("player-link").get_attribute("href"))[0])
        
        total_passes = tr.find_element_by_class_name("TotalPasses ").text
        pass_acc = tr.find_element_by_class_name("PassSuccessInMatch ").text
        crosses = tr.find_element_by_class_name("PassCrossTotal ").text
        acc_crosses = tr.find_element_by_class_name("PassCrossAccurate ").text
        total_long_balls = tr.find_element_by_class_name("PassLongBallTotal ").text
        acc_long_balls = tr.find_element_by_class_name("PassLongBallAccurate ").text
        total_through_balls = tr.find_element_by_class_name("PassThroughBallTotal ").text
        acc_through_balls = tr.find_element_by_class_name("PassThroughBallAccurate ").text
        
        performance_table[match_id][player_id]["total_passes"] = total_passes
        performance_table[match_id][player_id]["pass_acc"] = pass_acc
        performance_table[match_id][player_id]["crosses"] = crosses
        performance_table[match_id][player_id]["acc_crosses"] = acc_crosses
        performance_table[match_id][player_id]["total_long_balls"] = total_long_balls
        performance_table[match_id][player_id]["acc_long_balls"] = acc_long_balls
        performance_table[match_id][player_id]["total_through_balls"] = total_through_balls
        performance_table[match_id][player_id]["acc_through_balls"] = acc_through_balls
    
print(">>> finished.")
driver.close()
subdriver.close()