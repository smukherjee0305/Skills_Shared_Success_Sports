*** OLS regressions for EPL ***

xi : reg diff_score diff_compo_goals_bin_3 diff_compo_shots_bin_3 diff_compo_ast_bin_3  dummy_team1_* dummy_team2_a* dummy_team2_c* dummy_team2_hull_city dummy_team2_everton dummy_team2_fulham dummy_team2_liverpool dummy_team2_newcastle_united dummy_team2_s* dummy_team2_tottenham_hotspur dummy_team2_west_*, robust 
estat ic

xi : reg diff_score diff_compo_goals_bin_3 diff_compo_shots_bin_3 diff_compo_ast_bin_3 diff_rel_suc dummy_team1_* dummy_team2_a* dummy_team2_c* dummy_team2_hull_city dummy_team2_everton dummy_team2_fulham dummy_team2_liverpool dummy_team2_newcastle_united dummy_team2_s* dummy_team2_tottenham_hotspur dummy_team2_west_* , robust 
estat ic



xi : reg diff_score diff_compo_goals_bin_1 diff_compo_shots_bin_1 diff_compo_ast_bin_1  dummy_team1_* dummy_team2_a* dummy_team2_c* dummy_team2_hull_city dummy_team2_everton dummy_team2_fulham dummy_team2_liverpool dummy_team2_newcastle_united dummy_team2_s* dummy_team2_tottenham_hotspur dummy_team2_west_*, robust 
estat ic

xi : reg diff_score diff_compo_goals_bin_1 diff_compo_shots_bin_1 diff_compo_ast_bin_1 diff_rel_suc dummy_team1_* dummy_team2_a* dummy_team2_c* dummy_team2_hull_city dummy_team2_everton dummy_team2_fulham dummy_team2_liverpool dummy_team2_newcastle_united dummy_team2_s* dummy_team2_tottenham_hotspur dummy_team2_west_*, robust 
estat ic



xi : reg diff_score diff_compo_goals_bin_5 diff_compo_shots_bin_5 diff_compo_ast_bin_5  dummy_team1_* dummy_team2_a* dummy_team2_c* dummy_team2_hull_city dummy_team2_everton dummy_team2_fulham dummy_team2_liverpool dummy_team2_newcastle_united dummy_team2_s* dummy_team2_tottenham_hotspur dummy_team2_west_*, robust 
estat ic

xi : reg diff_score diff_compo_goals_bin_5 diff_compo_shots_bin_5 diff_compo_ast_bin_5 diff_rel_suc dummy_team1_* dummy_team2_a* dummy_team2_c* dummy_team2_hull_city dummy_team2_everton dummy_team2_fulham dummy_team2_liverpool dummy_team2_newcastle_united dummy_team2_s* dummy_team2_tottenham_hotspur dummy_team2_west_* , robust 
estat ic


****#################################################****
**** #######Logit models with predictions #########****
****#################################################****

*** regressions for EPL 2013-14 ***

logit diff_win_loss diff_compo_goals_bin_3 diff_compo_shots_bin_3 diff_compo_ast_bin_3  dummy_team1_* dummy_team2_a* dummy_team2_c* dummy_team2_everton dummy_team2_fulham dummy_team2_hull_city dummy_team2_liverpool dummy_team2_newcastle_united  dummy_team2_s* dummy_team2_tottenham_hotspur dummy_team2_west_bromwich_albion dummy_team2_manchester_city   , robust
estat ic
estat classification

logit diff_win_loss diff_compo_goals_bin_3 diff_compo_shots_bin_3 diff_compo_ast_bin_3 diff_rel_suc dummy_team1_* dummy_team2_a* dummy_team2_c* dummy_team2_everton dummy_team2_fulham dummy_team2_hull_city dummy_team2_liverpool dummy_team2_newcastle_united  dummy_team2_s* dummy_team2_tottenham_hotspur dummy_team2_west_bromwich_albion dummy_team2_manchester_city   , robust
estat ic
estat classification



logit diff_win_loss diff_compo_goals_bin_1 diff_compo_shots_bin_1 diff_compo_ast_bin_1  dummy_team1_* dummy_team2_a* dummy_team2_c* dummy_team2_everton dummy_team2_fulham dummy_team2_hull_city dummy_team2_liverpool dummy_team2_newcastle_united  dummy_team2_s* dummy_team2_tottenham_hotspur dummy_team2_west_bromwich_albion dummy_team2_manchester_city   , robust
estat ic
estat classification

logit diff_win_loss diff_compo_goals_bin_1 diff_compo_shots_bin_1 diff_compo_ast_bin_1 diff_rel_suc dummy_team1_* dummy_team2_a* dummy_team2_c* dummy_team2_everton dummy_team2_fulham dummy_team2_hull_city dummy_team2_liverpool dummy_team2_newcastle_united  dummy_team2_s* dummy_team2_tottenham_hotspur dummy_team2_west_bromwich_albion dummy_team2_manchester_city   , robust
estat ic
estat classification



logit diff_win_loss diff_compo_goals_bin_5 diff_compo_shots_bin_5 diff_compo_ast_bin_5  dummy_team1_* dummy_team2_a* dummy_team2_c* dummy_team2_everton dummy_team2_fulham dummy_team2_hull_city dummy_team2_liverpool dummy_team2_newcastle_united  dummy_team2_s* dummy_team2_tottenham_hotspur dummy_team2_west_bromwich_albion dummy_team2_manchester_city   , robust
estat ic
estat classification

logit diff_win_loss diff_compo_goals_bin_5 diff_compo_shots_bin_5 diff_compo_ast_bin_5 diff_rel_suc dummy_team1_* dummy_team2_a* dummy_team2_c* dummy_team2_everton dummy_team2_fulham dummy_team2_hull_city dummy_team2_liverpool dummy_team2_newcastle_united  dummy_team2_s* dummy_team2_tottenham_hotspur dummy_team2_west_bromwich_albion dummy_team2_manchester_city   , robust
estat ic
estat classification
