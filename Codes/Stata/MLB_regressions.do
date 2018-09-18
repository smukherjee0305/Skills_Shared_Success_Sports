
gen win_t1 = 1 if score01 >= score02 
replace win_t1 = 0 if score01 < score02 

gen win_t2 = 1 if score02 >= score01 
replace win_t2 = 0 if score02 < score01

gen dumm_win_loss = win_t1 - win_t2 if hateam01 == "Home"
replace dumm_win_loss = win_t2 - win_t1 if hateam02 == "Home"

gen diff_win_loss =  1 if dumm_win_loss > 0
replace diff_win_loss =  0 if dumm_win_loss <= 0

*** OLS regressions 


xi :reg diff_score diff_compo_pitch_war_bin_1 diff_compo_ops_bin_1 i.team1 i.team2, robust 
estat ic

xi :reg diff_score diff_compo_pitch_war_bin_1 diff_compo_ops_bin_1 diff_rel_suc  i.team1 i.team2, robust 
estat ic



xi :reg diff_score diff_compo_era_bin_1 diff_compo_ops_bin_1 i.team1 i.team2, robust 
estat ic

xi :reg diff_score diff_compo_era_bin_1 diff_compo_ops_bin_1 diff_rel_suc  i.team1 i.team2, robust 
estat ic




xi :reg diff_score diff_compo_pitch_war_bin_3 diff_compo_ops_bin_3 i.team1 i.team2, robust 
estat ic

xi :reg diff_score diff_compo_pitch_war_bin_3 diff_compo_ops_bin_3 diff_rel_suc  i.team1 i.team2, robust 
estat ic




xi :reg diff_score diff_compo_era_bin_3 diff_compo_ops_bin_3 i.team1 i.team2, robust 
estat ic

xi :reg diff_score diff_compo_era_bin_3 diff_compo_ops_bin_3 diff_rel_suc  i.team1 i.team2, robust 
estat ic



xi :reg diff_score diff_compo_pitch_war_bin_5 diff_compo_ops_bin_5 i.team1 i.team2, robust 
estat ic

xi :reg diff_score diff_compo_pitch_war_bin_5 diff_compo_ops_bin_5 diff_rel_suc  i.team1 i.team2, robust 
estat ic



xi :reg diff_score diff_compo_era_bin_5 diff_compo_ops_bin_5 i.team1 i.team2, robust 
estat ic

xi :reg diff_score diff_compo_era_bin_5 diff_compo_ops_bin_5 diff_rel_suc  i.team1 i.team2, robust 
estat ic


log close
}

*** logistic regressions ** ** predictions ****



xi :logit diff_win_loss diff_compo_pitch_war_bin_1 diff_compo_ops_bin_1 i.team1 i.team2, robust 
estat ic
estat classification

xi :logit diff_win_loss diff_compo_pitch_war_bin_1 diff_compo_ops_bin_1 diff_rel_suc  i.team1 i.team2, robust 
estat ic
estat classification



xi :logit diff_win_loss diff_compo_era_bin_1 diff_compo_ops_bin_1 i.team1 i.team2, robust 
estat ic
estat classification

xi :logit diff_win_loss diff_compo_era_bin_1 diff_compo_ops_bin_1 diff_rel_suc  i.team1 i.team2, robust 
estat ic
estat classification




xi :logit diff_win_loss diff_compo_pitch_war_bin_3 diff_compo_ops_bin_3 i.team1 i.team2, robust 
estat ic
estat classification

xi :logit diff_win_loss diff_compo_pitch_war_bin_3 diff_compo_ops_bin_3 diff_rel_suc  i.team1 i.team2, robust 
estat ic
estat classification



xi :logit diff_win_loss diff_compo_era_bin_3 diff_compo_ops_bin_3 i.team1 i.team2, robust 
estat ic
estat classification

xi :logit diff_win_loss diff_compo_era_bin_3 diff_compo_ops_bin_3 diff_rel_suc  i.team1 i.team2, robust 
estat ic
estat classification



xi :logit diff_win_loss diff_compo_pitch_war_bin_5 diff_compo_ops_bin_5 i.team1 i.team2, robust 
estat ic
estat classification

xi :logit diff_win_loss diff_compo_pitch_war_bin_5 diff_compo_ops_bin_5 diff_rel_suc  i.team1 i.team2, robust 
estat ic
estat classification



xi :logit diff_win_loss diff_compo_era_bin_5 diff_compo_ops_bin_5 i.team1 i.team2, robust 
estat ic
estat classification

xi :logit diff_win_loss diff_compo_era_bin_5 diff_compo_ops_bin_5 diff_rel_suc  i.team1 i.team2, robust 
estat ic
estat classification

log close
}
