
*** OLS regressions for IPL ***
	
	xi :reg  diff_run_rate compositional_er_bin_3 compositional_sr_bin_3 i.team1 i.team2, robust
	estat ic
	
	xi :reg  diff_run_rate compositional_er_bin_3 compositional_sr_bin_3 relational_suc  i.team1 i.team2, robust
	estat ic	
	

	
	xi :reg  diff_run_rate compositional_er_bin_1 compositional_sr_bin_1 i.team1 i.team2, robust
	estat ic
	
	xi :reg  diff_run_rate compositional_er_bin_1 compositional_sr_bin_1 relational_suc  i.team1 i.team2, robust
	estat ic	

	
	
	xi :reg  diff_run_rate compositional_er_bin_5 compositional_sr_bin_5 i.team1 i.team2, robust
	estat ic
	
	xi :reg  diff_run_rate compositional_er_bin_5 compositional_sr_bin_5 relational_suc  i.team1 i.team2, robust
	estat ic	
	

	
	xi :reg  diff_score_runs compositional_er_bin_3 compositional_sr_bin_3 i.team1 i.team2, robust
	estat ic
	
	xi :reg  diff_score_runs compositional_er_bin_3 compositional_sr_bin_3 relational_suc  i.team1 i.team2, robust
	estat ic	

	
	
	xi :reg  diff_score_runs compositional_er_bin_1 compositional_sr_bin_1 i.team1 i.team2, robust
	estat ic
	
	xi :reg  diff_score_runs compositional_er_bin_1 compositional_sr_bin_1 relational_suc  i.team1 i.team2, robust
	estat ic	

	
	
	xi :reg  diff_score_runs compositional_er_bin_5 compositional_sr_bin_5 i.team1 i.team2, robust
	estat ic
	
	xi :reg  diff_score_runs compositional_er_bin_5 compositional_sr_bin_5 relational_suc  i.team1 i.team2, robust
	estat ic	
	

****#################################################****
**** #######Logit models with predictions #########****
****#################################################****
	
	xi :logit  dummy_diff_win  compositional_er_bin_3 compositional_sr_bin_3 i.team1 i.team2, robust
	estat ic
	estat classification
	 
	xi :logit  dummy_diff_win  compositional_er_bin_3 compositional_sr_bin_3 relational_suc  i.team1 i.team2, robust
	estat ic	
	estat classification

	
	
	xi :logit  dummy_diff_win  compositional_er_bin_1 compositional_sr_bin_1 i.team1 i.team2, robust
	estat ic
	estat classification
	
	xi :logit  dummy_diff_win  compositional_er_bin_1 compositional_sr_bin_1 relational_suc  i.team1 i.team2, robust
	estat ic	
	estat classification

	
	
	xi :logit  dummy_diff_win  compositional_er_bin_5 compositional_sr_bin_5 i.team1 i.team2, robust
	estat ic
	estat classification

	xi :logit  dummy_diff_win  compositional_er_bin_5 compositional_sr_bin_5 relational_suc  i.team1 i.team2, robust
	estat ic	
	estat classification
	
