
*######### OLS regressions #######****

xi : reg diff_score diff_compo_bpm_bin_3 diff_compo_pts_bin_3  diff_compo_ast_bin_3   , robust
estat ic

xi : reg diff_score diff_compo_bpm_bin_3 diff_compo_pts_bin_3  diff_compo_ast_bin_3 diff_rel_suc   , robust
estat ic



xi : reg diff_score diff_compo_bpm_bin_1 diff_compo_pts_bin_1  diff_compo_ast_bin_1   , robust
estat ic

xi : reg diff_score diff_compo_bpm_bin_1 diff_compo_pts_bin_1  diff_compo_ast_bin_1 diff_rel_suc   , robust
estat ic



xi : reg diff_score diff_compo_bpm_bin_5 diff_compo_pts_bin_5  diff_compo_ast_bin_5   , robust
estat ic

xi : reg diff_score diff_compo_bpm_bin_5 diff_compo_pts_bin_5  diff_compo_ast_bin_5  diff_rel_suc   , robust
estat ic




*######### logistic regressions #######****

xi : logit diff_win_loss diff_compo_bpm_bin_3 diff_compo_pts_bin_3  diff_compo_ast_bin_3   , robust
estat ic
estat classification

xi : logit diff_win_loss diff_compo_bpm_bin_3 diff_compo_pts_bin_3  diff_compo_ast_bin_3 diff_rel_suc   , robust
estat ic
estat classification



xi : logit diff_win_loss diff_compo_bpm_bin_1 diff_compo_pts_bin_1  diff_compo_ast_bin_1   , robust
estat ic
estat classification

xi : logit diff_win_loss diff_compo_bpm_bin_1 diff_compo_pts_bin_1  diff_compo_ast_bin_1 diff_rel_suc   , robust
estat ic
estat classification



xi : logit diff_win_loss diff_compo_bpm_bin_5 diff_compo_pts_bin_5  diff_compo_ast_bin_5   , robust
estat ic
estat classification

xi : logit diff_win_loss diff_compo_bpm_bin_5 diff_compo_pts_bin_5  diff_compo_ast_bin_5  diff_rel_suc   , robust
estat ic
estat classification
