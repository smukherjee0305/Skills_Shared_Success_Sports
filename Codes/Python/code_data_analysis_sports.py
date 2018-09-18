import sys
import os
import networkx as nx
from collections import defaultdict
import glob
import fileinput
import numpy as np
from scipy import stats
from sets import Set
from itertools import combinations
from datetime import datetime

def countDuplicatesInList(dupedList):
	 uniqueSet = Set(item for item in dupedList)
	 return [(item, dupedList.count(item)) for item in uniqueSet]

def c2str(data):
	if len(str(data))==1:
		ret='0'+str(data)
	else:
		ret = str(data)
	return ret

###Code for compositional relationship!
####
####
def gen_compositional_mlb_variables(f1, f2, f3, f4, destdir, start_yr, bin1) :

	## read the datascores for MLB containing matchid and scores ##

	#file1 = open('../Data/Researchdata_MLB2/mlb_data_scores_matchid_year_team_scores.txt','r') 

	file1 = open(f1,'r') 
	data = file1.readlines()[1:]
	file1.close()

	matcid_year = defaultdict(list)

	for line in data :  
		line = line.strip()
		line = line.split('|')
		matcid = line[0]
		years = line[1]

		matcid_year[int(matcid)] = int(years)

	## read MLB batting data ###

	#file2 = open('../Data/Researchdata/data_for_analysis/mlb_playerid_batting_AVG_OBP_OPS_WAR.txt','r')

	file2 = open(f2,'r')
	data2 = file2.readlines()[1:]
	file2.close()

	team_avg1 = defaultdict(list); team_avg2 = defaultdict(list); team_avg3 = defaultdict(list); team_avg4 = defaultdict(list)

	for line in data2 :  
		line = line.strip().split('|')
		yearnew = int(line[1])

		if yearnew >= int(start_yr) - int(bin1) and yearnew < int(start_yr) :
		#if yearnew < int(start_yr) :

			team_avg1[str(line[0])].append(float(line[2])) 
			team_avg2[str(line[0])].append(float(line[3])) 
			team_avg3[str(line[0])].append(float(line[4])) 
			team_avg4[str(line[0])].append(float(line[5]))


	#file3 = open('../Data/Researchdata/data_for_analysis/mlb_playerid_pitching_ERA_WHIP_WAR.txt','r')

	file3 = open(f3,'r')
	data3 = file3.readlines()[1:]
	file3.close()

	team_pitch1 = defaultdict(list); team_pitch2 = defaultdict(list); team_pitch3 = defaultdict(list); 

	for line in data3 :  
		line = line.strip().split('|')
		yearnew = int(line[1])

		if yearnew >= int(start_yr) - int(bin1) and yearnew < int(start_yr) :
		#if yearnew < int(start_yr) :

			team_pitch1[str(line[0])].append(float(line[2])) 
			team_pitch2[str(line[0])].append(float(line[3])) 
			team_pitch3[str(line[0])].append(float(line[4])) 

	#file2 = open('../Data/Researchdata_MLB2/mlb_matchid_playerid_playernames.txt','r') 
	
	file4 = open(f4,'r') 
	data4 = file4.readlines()
	file4.close()

	team_nodes_bat_mean1 = defaultdict(list); team_nodes_bat_mean2 = defaultdict(list); team_nodes_bat_mean3 = defaultdict(list); team_nodes_bat_mean4 = defaultdict(list)
	team_nodes_pitch_mean1 = defaultdict(list); team_nodes_pitch_mean2 = defaultdict(list); team_nodes_pitch_mean3 = defaultdict(list)


	team_home_away = defaultdict(list)

	for line in data4 :
		line = line.strip()
		line = line.split()
		year = matcid_year[int(line[0])]

		try :
			if int(year) == int(start_yr) :

				if str(line[2]) in team_avg1 :

					team_nodes_bat_mean1[str(line[1].lower())+'|'+str(line[0])].append(np.mean(team_avg1[str(line[2])]))
					team_nodes_bat_mean2[str(line[1].lower())+'|'+str(line[0])].append(np.mean(team_avg2[str(line[2])]))
					team_nodes_bat_mean3[str(line[1].lower())+'|'+str(line[0])].append(np.mean(team_avg3[str(line[2])]))
					team_nodes_bat_mean4[str(line[1].lower())+'|'+str(line[0])].append(np.mean(team_avg4[str(line[2])]))

				if str(line[2]) in team_pitch1 :

					team_nodes_pitch_mean1[str(line[1].lower())+'|'+str(line[0])].append(np.mean(team_pitch1[str(line[2])]))
					team_nodes_pitch_mean2[str(line[1].lower())+'|'+str(line[0])].append(np.mean(team_pitch2[str(line[2])]))
					team_nodes_pitch_mean3[str(line[1].lower())+'|'+str(line[0])].append(np.mean(team_pitch3[str(line[2])]))

				team_home_away[str(line[1].lower())+'|'+str(line[0])] = str(line[3])

		except TypeError,e :
			continue


	fh6 = open(destdir+'MLB_compositional_batting_pitching_bin_'+str(bin1)+'_'+str(start_yr)+'.txt' , 'w')
	print >> fh6, 'MatchID|Team1|mean_AVG_t1_bin_'+str(bin1)+'|mean_OBP_t1_bin_'+str(bin1)+'|mean_OPS_t1_bin_'+str(bin1)+'|mean_bat_WAR_t1_bin_'+str(bin1)+'|mean_ERA_t1_bin_'+str(bin1)+'|mean_WHIP_t1_bin_'+str(bin1)+'|mean_pitch_WAR_t1_bin_'+str(bin1)+'|HAteam01|Team2|mean_AVG_t2_bin_'+str(bin1)+'|mean_OBP_t2_bin_'+str(bin1)+'|mean_OPS_t2_bin_'+str(bin1)+'|mean_bat_WAR_t2_bin_'+str(bin1)+'|mean_ERA_t2_bin_'+str(bin1)+'|mean_WHIP_t2_bin_'+str(bin1)+'|mean_pitch_WAR_t2_bin_'+str(bin1)+'|HAteam02'

	#fh6 = open(destdir+'MLB_compositional_batting_pitching_all'+'_'+str(start_yr)+'.txt' , 'w')
	#print >> fh6, 'MatchID|Team1|mean_AVG_t1|mean_OBP_t1|mean_OPS_t1|mean_bat_WAR_t1|mean_ERA_t1|mean_WHIP_t1|mean_pitch_WAR_t1|HAteam01|Team2|mean_AVG_t2|mean_OBP_t2|mean_OPS_t2|mean_bat_WAR_t2|mean_ERA_t2|mean_WHIP_t2|mean_pitch_WAR_t2|HAteam02'

	for line in data :
		line = line.strip()
		line = line.split('|')
		if int(line[1]) == int(start_yr) :

			team1 = line[2]
			team2 = line[4]

			keys1 = str(team1)+'|'+str(line[0]); keys2 = str(team2)+'|'+str(line[0])

			## Average batting statistics
			mean_AVG_t1 = float(np.mean(team_nodes_bat_mean1[keys1])); 	mean_AVG_t2 = float(np.mean(team_nodes_bat_mean1[keys2])); 
			mean_OBP_t1 = float(np.mean(team_nodes_bat_mean2[keys1]));	mean_OBP_t2 = float(np.mean(team_nodes_bat_mean2[keys2]));
			mean_OPS_t1 = float(np.mean(team_nodes_bat_mean3[keys1]));	mean_OPS_t2 = float(np.mean(team_nodes_bat_mean3[keys2]));
			mean_bat_WAR_t1 = float(np.mean(team_nodes_bat_mean4[keys1])); mean_bat_WAR_t2 = float(np.mean(team_nodes_bat_mean4[keys2]));

			## Average pitching statistics
			mean_ERA_t1 = float(np.mean(team_nodes_pitch_mean1[keys1])); 	mean_ERA_t2 = float(np.mean(team_nodes_pitch_mean1[keys2])); 
			mean_WHIP_t1 = float(np.mean(team_nodes_pitch_mean2[keys1]));	mean_WHIP_t2 = float(np.mean(team_nodes_pitch_mean2[keys2]));
			mean_pitch_WAR_t1 = float(np.mean(team_nodes_pitch_mean3[keys1])); mean_pitch_WAR_t2 = float(np.mean(team_nodes_pitch_mean3[keys2]));

			t1_home_away = str(team_home_away[keys1]); t2_home_away = str(team_home_away[keys2])

			print >> fh6, '%d|%s|%f|%f|%f|%f|%f|%f|%f|%s|%s|%f|%f|%f|%f|%f|%f|%f|%s' % ( int(line[0]), str(team1), mean_AVG_t1, mean_OBP_t1, mean_OPS_t1, mean_bat_WAR_t1, mean_ERA_t1, mean_WHIP_t1, mean_pitch_WAR_t1, t1_home_away,
																																									 str(team2), mean_AVG_t2, mean_OBP_t2, mean_OPS_t2, mean_bat_WAR_t2, mean_ERA_t2, mean_WHIP_t2, mean_pitch_WAR_t2, t2_home_away )


def gen_compositional_EPL_variables(f1, f2, f3, destdir, start_yr) :

	#file1 = open('../Data/Researchdata/data_for_analysis/FIFA_world_cup_matchid_year_teamscores.txt','r') 
	file1 = open(f1,'r') 
	data = file1.readlines()[1:]
	file1.close()
	matcid_year = defaultdict(list); matcid_team_result = defaultdict(list)

	for line in data :  
		line = line.strip(); line = line.split('|')
		
		matcid = line[0]; years = line[1]; matcid_year[int(matcid)] = int(years)


	#file3 = open('../Data/Researchdata/data_for_analysis/FIFA_players_stats_goals_scored_assists_competition_gameid_result.txt','r')
	file2 = open(f2,'r')
	data2 = file2.readlines()[1:]
	file2.close()

	team_avg2 = defaultdict(list); team_avg1 = defaultdict(list); team_avg3 = defaultdict(list)

	for line in data2 :  
		line = line.strip()
		line = line.split('|')
		yearnew = int(line[2])

		### We also check for only EPL past matches compositional variables 
		#if str(line[4]) == "Prem" :
			#if yearnew >= int(start_yr) - int(bin1) and yearnew < int(start_yr):
		if int(yearnew) < int(start_yr) :

				team_avg1[str(line[0])].append(float(line[5])) # goals
				team_avg2[str(line[0])].append(float(line[6])) # assists
				team_avg3[str(line[0])].append(float(line[7])) # shots

	#file3 = open('../Data/Researchdata/data_for_analysis/FIFA_WC_matchid_team_playerID_playername_sh_sg_ast.txt','r') 
	file3 = open(f3,'r') 
	data3 = file3.readlines()
	file3.close()

	team_nodes_mean1 = defaultdict(list); team_nodes_mean2 = defaultdict(list); team_nodes_mean3 = defaultdict(list)

	team_home_away = defaultdict(list)

	for line in data3 :

		line = line.strip().split()
		
		year = matcid_year[int(line[0])]

		team_home_away[str(line[1].lower())+'|'+str(line[0])] = str(line[4])

		try :

			if int(year) == int(start_yr) :

				if str(line[2]) in team_avg1 : 
					team_nodes_mean1[str(line[1].lower())+'|'+str(line[0])].append(np.mean(team_avg1[str(line[2])])) # goals

				if str(line[2]) in team_avg2 :
					team_nodes_mean2[str(line[1].lower())+'|'+str(line[0])].append(np.mean(team_avg2[str(line[2])])) # assists

				if str(line[2]) in team_avg3 :
					team_nodes_mean3[str(line[1].lower())+'|'+str(line[0])].append(np.mean(team_avg3[str(line[2])])) # shots

		except TypeError,e :
			continue


	fh6 = open(destdir+'EPL_compositional_all_championship_'+str(start_yr)+'.txt', 'w')
	print >> fh6, 'MatchID|Team1|mean_goals_t1|mean_AST_t1|mean_shots_t1|HAteam01|Team2|mean_goals_t2|mean_AST_t2|mean_shots_t2|HAteam02'
	#print >> fh6, 'MatchID|Team1|mean_goals_t1_bin_'+str(bin1)+'|mean_AST_t1_bin_'+str(bin1)+'|mean_shots_t1_bin_'+str(bin1)+'|HAteam01|Team2|mean_goals_t2_bin_'+str(bin1)+'|mean_AST_t2_bin_'+str(bin1)+'|mean_shots_t2_bin_'+str(bin1)+'|HAteam02'
	#print >> fh6, 'MatchID|Team1|epl_mean_goals_t1_bin_'+str(bin1)+'|epl_mean_AST_t1_bin_'+str(bin1)+'|epl_mean_shots_t1_bin_'+str(bin1)+'|HAteam01|Team2|epl_mean_goals_t2_bin_'+str(bin1)+'|epl_mean_AST_t2_bin_'+str(bin1)+'|epl_mean_shots_t2_bin_'+str(bin1)+'|HAteam02'
	#print >> fh6, 'MatchID|Team1|epl_mean_goals_t1|epl_mean_AST_t1|epl_mean_shots_t1|HAteam01|Team2|epl_mean_goals_t2|epl_mean_AST_t2|epl_mean_shots_t2|HAteam02'

	for line in data :
		line = line.strip()
		line = line.split('|')
		if int(line[1]) == int(start_yr) :

			team1 = line[2]

			team2 = line[4]

			keys1 = str(team1)+'|'+str(line[0]); keys2 = str(team2)+'|'+str(line[0])

			t1_home_away = str(team_home_away[keys1]); t2_home_away = str(team_home_away[keys2])

			mean_goals_t1 = float(np.mean(team_nodes_mean1[keys1])); mean_goals_t2 = float(np.mean(team_nodes_mean1[keys2]))
			mean_AST_t1 = float(np.mean(team_nodes_mean2[keys1])); mean_AST_t2 = float(np.mean(team_nodes_mean2[keys2]))
			mean_shots_t1 = float(np.mean(team_nodes_mean3[keys1])); mean_shots_t2 = float(np.mean(team_nodes_mean3[keys2]))

			print >> fh6, '%d|%s|%f|%f|%f|%s|%s|%f|%f|%f|%s' % ( int(line[0]), str(team1), mean_goals_t1, mean_AST_t1, mean_shots_t1, t1_home_away, str(team2), mean_goals_t2, mean_AST_t2, mean_shots_t2, t2_home_away)


def gen_compositional_NBA_variables(f1, f2, f3, f4, destdir, start_yr, bin1) :
	## read the datascores for NBA containing matchid and scores ##

	#file1 = open('../Data/Researchdata/data_for_analysis/nba_data_scores_matchid_year_team_scores.txt','r') 

	file1 = open(f1,'r') 
	data = file1.readlines()[1:]
	file1.close()

	matcid_year = defaultdict(list)

	for line in data :  
		line = line.strip()
		line = line.split('|')
		matcid = line[0]
		years = line[1]

		matcid_year[int(matcid)] = int(years)

	## read NBA ESPN data ###


	file2 = open(f2,'r')
	data2 = file2.readlines()[1:]
	file2.close()

	team_pts = defaultdict(list); team_stl = defaultdict(list); team_ast = defaultdict(list); 

	for line in data2 :  
		line = line.strip().split('|')

		yrs = int(line[1].split("-'")[0].replace("'",""))
		if yrs > 20 : yearnew = 1900+yrs 
		if yrs <=20 : yearnew = 2000+yrs

		if int(yearnew) >= int(start_yr) - int(bin1) and int(yearnew) < int(start_yr) :
		#if int(yearnew) < int(start_yr) :

			team_pts[str(line[0])].append(float(line[3])) 
			team_stl[str(line[0])].append(float(line[4])) 
			team_ast[str(line[0])].append(float(line[5])) 



	file3 = open(f3,'r')
	data3 = file3.readlines()[1:]
	file3.close()

	team_dbpm = defaultdict(list); team_bpm = defaultdict(list); team_vorp = defaultdict(list); 

	for line in data3 :  
		line = line.strip().split('|')
		yearnew = int(line[2])

		if yearnew >= int(start_yr) - int(bin1) and yearnew < int(start_yr) :

		#if yearnew < int(start_yr) :

			try :
			
				team_dbpm[str(line[0])].append(float(line[4])) 
				team_bpm[str(line[0])].append(float(line[5])) 
				team_vorp[str(line[0])].append(float(line[6])) 
			
			except ValueError,e :
				print line[0], line[1], e

	#file2 = open('../Data/Researchdata/data_for_analysis/nba_matchid_playerid_playernames.txt','r') 
	#file2 = open('../Data/Researchdata/data_for_analysis/nba_matchid_playerid_playernames_noDNP.txt','r') 

	file4 = open(f4,'r') 
	data4 = file4.readlines()
	file4.close()

	team_nodes_pts = defaultdict(list); team_nodes_stl = defaultdict(list); team_nodes_ast = defaultdict(list); 
	team_nodes_dbpm = defaultdict(list); team_nodes_bpm = defaultdict(list); team_nodes_vorp = defaultdict(list)


	team_home_away = defaultdict(list)

	for line in data4 :
		line = line.strip()
		line = line.split()
		year = matcid_year[int(line[0])]

		try :
			if int(year) == int(start_yr) :

				if str(line[1]) in team_pts :

					team_nodes_pts[str(line[2].lower())+'|'+str(line[0])].append(np.mean(team_pts[str(line[1])]))
					team_nodes_stl[str(line[2].lower())+'|'+str(line[0])].append(np.mean(team_stl[str(line[1])]))
					team_nodes_ast[str(line[2].lower())+'|'+str(line[0])].append(np.mean(team_ast[str(line[1])]))

				if str(line[1]) in team_dbpm :

					team_nodes_dbpm[str(line[2].lower())+'|'+str(line[0])].append(np.mean(team_dbpm[str(line[1])]))
					team_nodes_bpm[str(line[2].lower())+'|'+str(line[0])].append(np.mean(team_bpm[str(line[1])]))
					team_nodes_vorp[str(line[2].lower())+'|'+str(line[0])].append(np.mean(team_vorp[str(line[1])]))

				team_home_away[str(line[2].lower())+'|'+str(line[0])] = str(line[3])

		except TypeError,e :
			continue


	#fh6 = open(destdir+'NBA_compositional_per_year'+'_'+str(start_yr)+'.txt' , 'w')
	#print >> fh6, 'MatchID|Team1|mean_PTS_t1|mean_STL_t1|mean_AST_t1|mean_DBPM_t1|mean_BPM_t1|mean_VORP_t1|HAteam01|Team2|mean_PTS_t2|mean_STL_t2|mean_AST_t2|mean_DBPM_t2|mean_BPM_t2|mean_VORP_t2|HAteam02'

	fh6 = open(destdir+'NBA_compositional_per_year_bin_'+str(bin1)+'_'+str(start_yr)+'.txt' , 'w')
	print >> fh6, 'MatchID|Team1|mean_PTS_t1_bin_'+str(bin1)+'|mean_STL_t1_bin_'+str(bin1)+'|mean_AST_t1_bin_'+str(bin1)+'|mean_DBPM_t1_bin_'+str(bin1)+'|mean_BPM_t1_bin_'+str(bin1)+'|mean_VORP_t1_bin_'+str(bin1)+'|HAteam01|Team2|mean_PTS_t2_bin_'+str(bin1)+'|mean_STL_t2_bin_'+str(bin1)+'|mean_AST_t2_bin_'+str(bin1)+'|mean_DBPM_t2_bin_'+str(bin1)+'|mean_BPM_t2_bin_'+str(bin1)+'|mean_VORP_t2_bin_'+str(bin1)+'|HAteam02'

	for line in data :
		line = line.strip()
		line = line.split('|')
		if int(line[1]) == int(start_yr) :

			team1 = line[2]
			team2 = line[4]

			keys1 = str(team1)+'|'+str(line[0]); keys2 = str(team2)+'|'+str(line[0])

			## Average ESPN
			mean_PTS_t1 = float(np.mean(team_nodes_pts[keys1])); 	mean_PTS_t2 = float(np.mean(team_nodes_pts[keys2]))
			mean_STL_t1 = float(np.mean(team_nodes_stl[keys1]));	mean_STL_t2 = float(np.mean(team_nodes_stl[keys2]))
			mean_AST_t1 = float(np.mean(team_nodes_ast[keys1]));	mean_AST_t2 = float(np.mean(team_nodes_ast[keys2]))

			## Average Basketball reference
			mean_DBPM_t1 = float(np.mean(team_nodes_dbpm[keys1])); 	 mean_DBPM_t2 = float(np.mean(team_nodes_dbpm[keys2]))
			mean_BPM_t1 = float(np.mean(team_nodes_bpm[keys1])); 		 mean_BPM_t2 = float(np.mean(team_nodes_bpm[keys2]))
			mean_VORP_t1 = float(np.mean(team_nodes_vorp[keys1]));   mean_VORP_t2 = float(np.mean(team_nodes_vorp[keys2]))

			t1_home_away = str(team_home_away[keys1]); t2_home_away = str(team_home_away[keys2])

			print >> fh6, '%d|%s|%f|%f|%f|%f|%f|%f|%s|%s|%f|%f|%f|%f|%f|%f|%s' % ( int(line[0]), str(team1), mean_PTS_t1, mean_STL_t1, mean_AST_t1, mean_DBPM_t1, mean_BPM_t1, mean_VORP_t1, t1_home_away,
																																									 str(team2), mean_PTS_t2, mean_STL_t2, mean_AST_t2, mean_DBPM_t2, mean_BPM_t2, mean_VORP_t2, t2_home_away )




def gen_compositional_IPL_variables(sourcedir, destdir, start_yr, bin1) :
	
	## Batting stats
	file1a = open(sourcedir+'players_T20I_stats_who_played_IPL/batting_T20I_players_stats_yearly.txt','r')
	data1a = file1a.readlines()[1:]
	file1a.close()

	p1_runs_year = defaultdict(list); p1_balls_year = defaultdict(list)

	for line in data1a :  
		line = line.strip().split('|')
		if str(line[1]) != "-" :

			yearnew = int(line[5])
			#if yearnew == int(start_yr) :

			if yearnew >= int(start_yr) - int(bin1) and yearnew < int(start_yr) :
				if float(line[2]) > 0.0 :
					p1_runs_year[str(line[0]).split('__')[1]].append(float(line[1]))
					p1_balls_year[str(line[0]).split('__')[1]].append(float(line[2]))

	p1_sr_year = defaultdict(list)

	for keys in p1_runs_year :
		if str(keys) in p1_balls_year :

			p1_sr_year[str(keys)] = np.sum(p1_runs_year[str(keys)])*100.0/np.sum(p1_balls_year[str(keys)])

	print len(p1_sr_year.keys())
	## Bowling stats
	file1b = open(sourcedir+'players_T20I_stats_who_played_IPL/bowling_T20I_players_stats_yearly.txt','r')
	data1b = file1b.readlines()[1:]
	file1b.close()

	p1_overs_year = defaultdict(list); p1_runsC_year = defaultdict(list)

	for line in data1b :  
		line = line.strip().split('|')
		if str(line[1]) != "-" :

			yearnew = int(line[5])
			#if yearnew == int(start_yr) :

			if yearnew >= int(start_yr) - int(bin1) and yearnew < int(start_yr) :
				p1_overs_year[str(line[0]).split('__')[1]].append(float(line[1]))
				p1_runsC_year[str(line[0]).split('__')[1]].append(float(line[2]))

	p1_er_year = defaultdict(list)

	for keys in p1_overs_year :
		if str(keys) in p1_runsC_year :

			p1_er_year[str(keys)] = np.sum(p1_runsC_year[str(keys)])*1.0/np.sum(p1_overs_year[str(keys)])
	#print p1_er_year


	### Get the team members
	file2 = open(sourcedir+'data_'+str(start_yr)+'/Names_IPL_Batting_avg_sr_till_'+str(start_yr)+'.txt','r')
	data2 = file2.readlines()
	file2.close()

	team_er = defaultdict(list); team_sr = defaultdict(list)
	
	for line in data2 :  
		line = line.strip().split()
  
		teams = line[0].split('_batting_averages_')[0]
		matcid = line[4]

		try :

			if str(line[1]) in p1_sr_year :
				team_sr[str(teams)+'|'+str(matcid)].append(float(p1_sr_year[str(line[1])]))

			if str(line[1]) in p1_er_year :
				team_er[str(teams)+'|'+str(matcid)].append(float(p1_er_year[str(line[1])]))

		except ValueError,e :
			continue


	### Get the team members
	#file2 = open(sourcedir+'data_'+str(start_yr)+'/Names_IPL_players_'+str(start_yr)+'.txt','r')
	#data2 = file2.readlines()
	#file2.close()

	#team_er = defaultdict(list); team_sr = defaultdict(list)
	
	#for line in data2 :  
	#	line = line.strip().split()
  
	#	teams = line[0].split('_innings')[0]
	#	matcid = line[2]

	#	try :

	#		if str(line[1]) in p1_sr_year :
	#			team_sr[str(teams)+'|'+str(matcid)].append(float(p1_sr_year[str(line[1])]))

	#		if str(line[1]) in p1_er_year :
	#			team_er[str(teams)+'|'+str(matcid)].append(float(p1_er_year[str(line[1])]))

	#	except ValueError,e :
	#		continue


	### team innings number 

	team_attr01 = defaultdict(list); team_attr02 = defaultdict(list)

	filein01 = open(sourcedir+'data_'+str(start_yr)+'/matchid_team_v_team_result_IPL'+str(start_yr)+'.txt')
	datain01 = filein01.readlines()
	filein01.close()

	for line in datain01 :
		line = line.strip().split()
		matcid = line[0]
		team1a = line[1].split("_v_")[0].split(':_')[1]; team1b = line[1].split("_v_")[1].split('_at_')[0]
		try :
			winteam =  line[2].split('_won_by_')[0]; wonby = line[2].split('_won_by_')[1]

			if "wicket" in str(wonby) :
				if str(winteam) == str(team1a) :
					team_attr01[str(team1a)+'|'+str(matcid)] = 02
					team_attr01[str(team1b)+'|'+str(matcid)] = 01

				if str(winteam) == str(team1b) :
					team_attr01[str(team1b)+'|'+str(matcid)] = 02
					team_attr01[str(team1a)+'|'+str(matcid)] = 01
 
			if "run" in str(wonby) :
				if str(winteam) == str(team1a) :
					team_attr01[str(team1a)+'|'+str(matcid)] = 01
					team_attr01[str(team1b)+'|'+str(matcid)] = 02

				if str(winteam) == str(team1b) :
					team_attr01[str(team1b)+'|'+str(matcid)] = 01
					team_attr01[str(team1a)+'|'+str(matcid)] = 02

		except IndexError,e :	
			continue

	### Run rate team
	filerr = open(sourcedir+'data_'+str(start_yr)+'/year_matchid_RunRate_IPL_'+str(start_yr)+'.txt','r')
	datarr = filerr.readlines()
	filerr.close()
	teamsrr = defaultdict(list)
	for line in datarr :
		line = line.strip().split()
		t = line[1].split('_innings')[0]; rr = line[2].split('_runs_')[0]
		teamsrr[str(t)+'|'+str(line[0])] = float(rr)


	### Run scored team
	filescore = open(sourcedir+'data_'+str(start_yr)+'/matchid_teams_runs_scored_'+str(start_yr)+'.txt','r')
	datascore = filescore.readlines()
	filescore.close()
	teamsscore = defaultdict(list)
	for line in datascore :
		line = line.strip().split()
		t = line[1]; runs = line[2]
		try :
			teamsscore[str(t)+'|'+str(line[0])] = float(runs)
		except ValueError,e :
			print line[0], e


	### Team vs Team outcome
	filer = open(sourcedir+'data_'+str(start_yr)+'/matchid_team_v_team_result_IPL'+str(start_yr)+'.txt','r')
	datar = filer.readlines()
	filer.close()

	team_result = defaultdict(list)

	errorfile = open('../Data/Errorfile'+str(start_yr)+'.txt', 'w')

#	fh6 = open(destdir+'IPL_compositional_variables_'+str(start_yr)+'.txt', 'w')
#	print >> fh6, 'MatchID|Team1|InningsNumteam1|runrate_t1|score_t1|mean_sr_t1|median_sr_t1|mean_er_t1|median_er_t1|Team2|InningsNumteam2|runrate_t2|score_t2|mean_sr_t2|median_sr_t2|mean_er_t2|median_er_t2|Won_By|Winning_type'


	fh6 = open(destdir+'IPL_compositional_variables_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	print >> fh6, 'MatchID|Team1|InningsNumteam1|runrate_t1|score_t1|mean_sr_t1_bin_'+str(bin1)+'|median_sr_t1_bin_'+str(bin1)+'|mean_er_t1_bin_'+str(bin1)+'|median_er_t1_bin_'+str(bin1)+'|Team2|InningsNumteam2|runrate_t2|score_t2|mean_sr_t2_bin_'+str(bin1)+'|median_sr_t2_bin_'+str(bin1)+'|mean_er_t2_bin_'+str(bin1)+'|median_er_t2_bin_'+str(bin1)+'|Won_By|Winning_type'

	for line in datar :
		line = line.strip().split()

		team1 = line[1].split(':_')[1].split('_at_')[0].split('_v_')[0]

		team2 = line[1].split(':_')[1].split('_at_')[0].split('_v_')[1]
		keys1 = str(team1)+'|'+str(line[0]); keys2 = str(team2) + '|' + str(line[0])

		try :
			try :
					winteam = line[2].split('_won_by_')[0]; winr = line[2].split('_won_by_')[1]
					try :

						### Team 1
						MatchID = int(keys1.split('|')[1]) 
						Team1 = str(keys1.split('|')[0]); InningsNumteam1 = int(team_attr01[keys1]); runrate_t1 = float(teamsrr[str(keys1)]); score_t1 = float(teamsscore[str(keys1)])
						mean_sr_t1 = float(np.mean(team_sr[keys1])) ; median_sr_t1 = float(np.median(team_sr[keys1])) ; mean_er_t1 = float(np.mean(team_er[keys1])); median_er_t1 = float(np.median(team_er[keys1]))

						### Team 2
						Team2 = str(keys2.split('|')[0]); InningsNumteam2 = int(team_attr01[keys2]); runrate_t2 = float(teamsrr[str(keys2)]); score_t2 = float(teamsscore[str(keys2)])
						mean_sr_t2 = float(np.mean(team_sr[keys2])) ; median_sr_t2 = float(np.median(team_sr[keys2])) ; mean_er_t2 = float(np.mean(team_er[keys2])); median_er_t2 = float(np.median(team_er[keys2]))

						print >> fh6, '%d|%s|%d|%f|%f|%f|%f|%f|%f|%s|%d|%f|%f|%f|%f|%f|%f|%s|%s' % ( MatchID, Team1, InningsNumteam1, runrate_t1, score_t1, mean_sr_t1, median_sr_t1, 
																									mean_er_t1, median_er_t1, Team2, InningsNumteam2, runrate_t2, score_t2, mean_sr_t2, 
																									median_sr_t2, mean_er_t2, median_er_t2, str(winteam), str(winr) ) 

					except TypeError,e :
						continue

			except AttributeError,e :
				print >> errorfile, winteam

		except IndexError,e :
			print >> errorfile, keys1, keys2


#####	@@@@@@@		#### %%%%%% &&&&& 								
#####	Code for relational relationship!
#### 	*********** #### ******* ******


def create_relational_variable_IPL(sourcedir, destdir, start_yr) :

	matcid_team_result = defaultdict(list); matcid_team_result2 = defaultdict(list)
	team_attr01 = defaultdict(list); team_attr02 = defaultdict(list)

	filein01 = open(sourcedir+'data_'+str(start_yr)+'/matchid_team_v_team_result_IPL'+str(start_yr)+'.txt')
	datain01 = filein01.readlines()
	filein01.close()

	for line in datain01 :
		line = line.strip().split()
	
		matcid = line[0]

		team1a = line[1].split("_v_")[0].split(':_')[1]; team1b = line[1].split("_v_")[1].split('_at_')[0]
		try :
			winteam =  line[2].split('_won_by_')[0]; wonby = line[2].split('_won_by_')[1]

			if "wicket" in str(wonby) :
				if str(winteam) == str(team1a) :
					team_attr01[str(team1a)+'|'+str(matcid)] = 02
					team_attr01[str(team1b)+'|'+str(matcid)] = 01

				if str(winteam) == str(team1b) :
					team_attr01[str(team1b)+'|'+str(matcid)] = 02
					team_attr01[str(team1a)+'|'+str(matcid)] = 01
 
			if "run" in str(wonby) :
				if str(winteam) == str(team1a) :
					team_attr01[str(team1a)+'|'+str(matcid)] = 01
					team_attr01[str(team1b)+'|'+str(matcid)] = 02

				if str(winteam) == str(team1b) :
					team_attr01[str(team1b)+'|'+str(matcid)] = 01
					team_attr01[str(team1a)+'|'+str(matcid)] = 02


		except IndexError,e :
			continue

	filer = open(sourcedir+'data_2015/matchid_all_t20_matches_results_team_v_team_thru_2016.txt','r')
	data3 = filer.readlines()
	filer.close()


	for line in data3 :  

		line = line.strip()
		line = line.split()
		matcid = int(line[0])

		try :
			team1a = line[1].split("_v_")[0].split(':_')[1]; team1b = line[1].split("_v_")[1].split('_at_')[0]
			winteam = line[2].split('_won_by_')[0] 

			if str(team1a) == str(winteam) :
				matcid_team_result2[str(team1a)+'|'+str(matcid)] = "W"
				matcid_team_result2[str(team1b)+'|'+str(matcid)] = "L"

			if str(team1b) == str(winteam) :
				matcid_team_result2[str(team1b)+'|'+str(matcid)] = "W"
				matcid_team_result2[str(team1a)+'|'+str(matcid)] = "L"

		except IndexError,e :
			continue

	#### This code is to look for relationship !!! completed @Satyam Mukherjee (October 2014)

	file1 = open(sourcedir+'data_'+str(start_yr)+'/IPL_batting_partnership_data_'+str(start_yr)+'_matchid.txt','r') ## form relationship for start_yr IPL !!!
	data = file1.readlines()
	file1.close()


	team_nodes = defaultdict(list)

	for line in data :  
		line = line.strip();line = line.split()
		teams = line[0].split('__innings')[0]
		matcid = line[5]
		batsman1 = line[1].split('_(')[0]; batsman2 = line[2].split('_(')[0]

		try :
			team_nodes[str(teams)+'|'+str(matcid)].append(batsman1)

			team_nodes[str(teams)+'|'+str(matcid)].append(batsman2)

		except ValueError,e :
			continue


	players_pair = defaultdict(list)

	for k in team_nodes :
		nodes = list(set(team_nodes[k]))
		edges = combinations(nodes,2)
		G = nx.Graph()
		G.add_nodes_from(nodes)
		G.add_edges_from(edges) 

		for u,v in G.edges() :
			if u != v :
				players_pair[str(u)+'|'+str(v)+'|'+k.split('|')[0]+'|'+k.split('|')[1]] = str(k)

	sorted(players_pair.iterkeys())
	team_nodes_past = defaultdict(list)

	file3 = open(sourcedir+'data_matches_bpn_t20/bpn_all_T20_matches_thru_2016.txt','r') ## now look back and see how many times players played with each other earlier !
	data4 = file3.readlines()
	file3.close()

	team_combos = []

	for line in data4 :  
		try:
			line = line.strip(); line = line.split()

			teams = line[0].split('__innings')[0]
			matcid = line[5]
			try :
				yearnew = int(line[4])

				if int(line[4]) < start_yr :
				#if yearnew >= int(start_yr) - int(bin1) and yearnew < int(start_yr) :

					if matcid_team_result2[str(teams)+'|'+str(matcid)] == "W" :

						batsman1 = line[1].split('_(')[0]; batsman2 = line[2].split('_(')[0]
						team_nodes_past[str(teams)+'|'+str(matcid)].append(batsman1)
						team_nodes_past[str(teams)+'|'+str(matcid)].append(batsman2)

			except ValueError,e :
				continue

		except IndexError,e :
			continue

	for k in team_nodes_past :

		nodes2 = list(set(team_nodes_past[k]))
		edges2 = combinations(nodes2, 2)
		G2 = nx.Graph()
		G2.add_nodes_from(nodes2)
		G2.add_edges_from(edges2) 

		for u,v in G2.edges() :
			if u != v :
				team_combos.append(( str(u)+'|'+str(v) ))

	team_combos2 = defaultdict(list)

	for k, v in countDuplicatesInList(team_combos) :

		team_combos2[k] = int(v) 


	teams_id = defaultdict(list)

	for keys in players_pair :
		k1 = keys.split('|')[0]+'|'+keys.split('|')[1]
		k2 = keys.split('|')[2]+'|'+keys.split('|')[3]
	
		if k1 in team_combos2 :
			teams_id[k2].append(team_combos2[k1])
		if not k1 in team_combos2 :
			team_combos2[k1] = 0
			teams_id[k2].append(team_combos2[k1])

	#print teams_id

	#fh6 = open(destdir+'IPL_relational_succesful_bin_'+str(bin1)+'_'+str(start_yr)+'.txt' , 'w')
	#print >> fh6, 'MatchID|Team1|InningsNumteam1|mean_rel_suc_t1_bin_'+str(bin1)+'|median_rel_suc_t1_bin_'+str(bin1)+'|std_rel_suc_t1_bin_'+str(bin1)+'|Team2|InningsNumteam2|mean_rel_suc_t2_bin_'+str(bin1)+'|median_rel_suc_t2_bin_'+str(bin1)+'|std_rel_suc_t2_bin_'+str(bin1)+''
	
	#fh6 = open(destdir+'IPL_relational_all_bin_'+str(bin1)+'_'+str(start_yr)+'.txt' , 'w')
	#print >> fh6, 'MatchID|Team1|InningsNumteam1|mean_rel_all_t1_bin_'+str(bin1)+'|median_rel_all_t1_bin_'+str(bin1)+'|std_rel_all_t1_bin_'+str(bin1)+'|Team2|InningsNumteam2|mean_rel_all_t2_bin_'+str(bin1)+'|median_rel_all_t2_bin_'+str(bin1)+'|std_rel_all_t2_bin_'+str(bin1)+''

	fh6 = open(destdir+'IPL_relational_succesful_'+str(start_yr)+'.txt' , 'w')
	print >> fh6, 'MatchID|Team1|InningsNumteam1|mean_rel_suc_t1|median_rel_suc_t1|std_rel_suc_t1|Team2|InningsNumteam2|mean_rel_suc_t2|median_rel_suc_t2|std_rel_suc_t2'
	

	filew = open(sourcedir+'data_'+str(start_yr)+'/matchid_team_v_team_result_IPL'+str(start_yr)+'.txt','r')
	dataw = filew.readlines(); filew.close()

	for line in dataw :
		line = line.strip().split(); matcid = line[0]

		team1 = line[1].split(':_')[1].split('_at_')[0].split('_v_')[0]

		team2 = line[1].split(':_')[1].split('_at_')[0].split('_v_')[1]

		keys1 = str(team1)+'|'+str(line[0]); keys2 = str(team2) + '|' + str(line[0])
		
		try :
		
			print >> fh6, '%d|%s|%d|%f|%f|%f|%s|%d|%f|%f|%f' % ( int(keys1.split('|')[1]), str(keys1.split('|')[0]), int(team_attr01[keys1]), float(np.mean(teams_id[keys1])), 
																float(np.median(teams_id[keys1])), float(np.std(teams_id[keys1])), str(keys2.split('|')[0]), int(team_attr01[keys2]), 
																float(np.mean(teams_id[keys2])), float(np.median(teams_id[keys2])), float(np.std(teams_id[keys2])) )
		
		except TypeError,e :
			continue #print keys1, e

def create_relational_variable_NBA(f1, f2, destdir, start_yr, bin1) :

	#file1 = open('../Data/data_for_analysis/nba_data_scores_matchid_year_team_scores.txt','r') 

	file1 = open(f1,'r') 
	data = file1.readlines()[1:]
	file1.close()

	matcid_year = defaultdict(list); matcid_team_result = defaultdict(list)

	for line in data :  
		line = line.strip().split('|')
		matcid = line[0]
		years = line[1]
  
		if int(line[3]) > int(line[5]) :
			matcid_team_result[str(line[2])+'|'+str(matcid)] = "W"
			matcid_team_result[str(line[4])+'|'+str(matcid)] = "L"

		if int(line[3]) == int(line[5]) :
			matcid_team_result[str(line[2])+'|'+str(matcid)] = "D"
			matcid_team_result[str(line[4])+'|'+str(matcid)] = "D"
 
		if int(line[3]) < int(line[5]) :
			matcid_team_result[str(line[4])+'|'+str(matcid)] = "W"
			matcid_team_result[str(line[2])+'|'+str(matcid)] = "L"

		matcid_year[int(matcid)] = int(years)


	#file2 = open('../Data/nba_matchid_playerid_playernames.txt','r') ## form relationship  !!!
	
	file2 = open(f2,'r') ## form relationship  !!!
	data2 = file2.readlines()
	file2.close()

	team_nodes = defaultdict(list)

	team_home_away = defaultdict(list)

	for line in data2 :
		line = line.strip()
		line = line.split()
		year = matcid_year[int(line[0])]
		try :
			if int(year) == int(start_yr) :

				team_nodes[str(line[2].lower())+'|'+str(line[0])].append(str(line[1])) ### NBA
				team_home_away[str(line[2].lower())+'|'+str(line[0])] = str(line[3])

		except TypeError,e :
			continue


	players_pair = defaultdict(list)

	for k in team_nodes :
		nodes = list(set(team_nodes[k]))
		edges = combinations(nodes,2)

		G = nx.Graph(); G.add_nodes_from(nodes); G.add_edges_from(edges) 

		for u,v in G.edges() :
			if u != v :
				players_pair[str(u)+'|'+str(v)+'|'+k.split('|')[0]+'|'+k.split('|')[1]] = str(k)


 ## now look back and see how many times players played with each other earlier !

	team_combos = []; 	team_nodes_past = defaultdict(list)

	for line in data2 :
		line = line.strip()
		line = line.split()
		year = matcid_year[int(line[0])]

		try :
			#if int(year) < int(start_yr) :
			if int(year) >= int(start_yr) - int(bin1) and int(year) < int(start_yr) :

				if matcid_team_result[str(line[2].lower())+'|'+str(line[0])] == "W" : #NBA
					team_nodes_past[str(line[2].lower())+'|'+str(line[0])].append(str(line[1])) ### NBA
		except TypeError,e :
			continue


	for k in team_nodes_past :
		nodes2 = list(set(team_nodes_past[k]))
		edges2 = combinations(nodes2, 2)
		G2 = nx.Graph()
		G2.add_nodes_from(nodes2)
		G2.add_edges_from(edges2) 
		for u,v in G2.edges() :
			if u != v :
				team_combos.append(( str(u)+'|'+str(v) ))

	team_combos2 = defaultdict(list)

	for k, v in countDuplicatesInList(team_combos) :
		team_combos2[k] = int(v) 

	sorted(team_combos2.iterkeys())

	team_combos3 = defaultdict(list)

	for k in team_combos2 :
		k1 = k.split('|')[0]; k2 = k.split('|')[1]
		team_combos3[str(k1)+'|'+str(k2)].append(team_combos2[k]) 

	teams_id = defaultdict(list)

	for keys in players_pair :
		k1 = keys.split('|')[0]+'|'+keys.split('|')[1]
		k2 = keys.split('|')[2]+'|'+keys.split('|')[3]
		if k1 in team_combos2 :
			teams_id[k2].append(team_combos2[k1])
		if not k1 in team_combos2 :
			team_combos2[k1] = 0
			teams_id[k2].append(team_combos2[k1])


	fh6 = open(destdir+'NBA_relational_succesful_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	print >> fh6, 'MatchID|Team1|mu_rel_suc_t1_bin_'+str(bin1)+'|std_rel_suc_t1_bin_'+str(bin1)+'|med_rel_suc_t1_bin_'+str(bin1)+'|score01|HAteam01|Team2|mu_rel_suc_t2_bin_'+str(bin1)+'|std_rel_suc_t2_bin_'+str(bin1)+'|med_rel_suc_t2_bin_'+str(bin1)+'|score02|HAteam02'
	
	#fh6 = open(destdir+'NBA_relational_noDNP_succesful_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	#print >> fh6, 'MatchID|Team1|mu_rel_noDNP_suc_t1_bin_'+str(bin1)+'|std_rel_noDNP_suc_t1_bin_'+str(bin1)+'|med_rel_noDNP_suc_t1_bin_'+str(bin1)+'|score01|HAteam01|Team2|mu_rel_noDNP_suc_t2_bin_'+str(bin1)+'|std_rel_noDNP_suc_t2_bin_'+str(bin1)+'|med_rel_noDNP_suc_t2_bin_'+str(bin1)+'|score02|HAteam02'

	#fh6 = open(destdir+'NBA_relational_all_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	#print >> fh6, 'MatchID|Team1|mu_rel_all_t1_bin_'+str(bin1)+'|std_rel_all_t1_bin_'+str(bin1)+'|med_rel_all_t1_bin_'+str(bin1)+'|score01|HAteam01|Team2|mu_rel_all_t2_bin_'+str(bin1)+'|std_rel_all_t2_bin_'+str(bin1)+'|med_rel_all_t2_bin_'+str(bin1)+'|score02|HAteam02'
	
	#fh6 = open(destdir+'NBA_relational_noDNP_all_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	#print >> fh6, 'MatchID|Team1|mu_rel_noDNP_all_t1_bin_'+str(bin1)+'|std_rel_noDNP_all_t1_bin_'+str(bin1)+'|med_rel_noDNP_all_t1_bin_'+str(bin1)+'|score01|HAteam01|Team2|mu_rel_noDNP_all_t2_bin_'+str(bin1)+'|std_rel_noDNP_all_t2_bin_'+str(bin1)+'|med_rel_noDNP_all_t2_bin_'+str(bin1)+'|score02|HAteam02'

	for line in data :
		line = line.strip()
		line = line.split('|')
		if int(line[1]) == int(start_yr) :
			team1 = line[2];team2 = line[4]
			keys1 = str(team1)+'|'+str(line[0]); keys2 = str(team2) + '|' + str(line[0])
			print >> fh6, '%d|%s|%f|%f|%f|%d|%s|%s|%f|%f|%f|%d|%s' % ( int(line[0]), str(team1), float(np.mean(teams_id[keys1])), float(np.std(teams_id[keys1])), 
																	float(np.median(teams_id[keys1])), int(line[3]), str(team_home_away[keys1]), str(team2), 
																	float(np.mean(teams_id[keys2])), float(np.std(teams_id[keys2])), float(np.median(teams_id[keys2])), int(line[5]), str(team_home_away[keys2]) )




def create_relational_variable_MLB(f1, f2, destdir, string_type, start_yr, bin1) :

	#file1 = open('../Data/data_for_analysis/nba_data_scores_matchid_year_team_scores.txt','r') 

	file1 = open(f1,'r') 
	data = file1.readlines()[1:]
	file1.close()

	matcid_year = defaultdict(list); matcid_team_result = defaultdict(list)

	for line in data :  
		line = line.strip().split('|')
		matcid = line[0]
		years = line[1]
		try :

			if int(line[3]) > int(line[5]) :
				matcid_team_result[str(line[2])+'|'+str(matcid)] = "W"
				matcid_team_result[str(line[4])+'|'+str(matcid)] = "L"

			if int(line[3]) == int(line[5]) :
				matcid_team_result[str(line[2])+'|'+str(matcid)] = "D"
				matcid_team_result[str(line[4])+'|'+str(matcid)] = "D"
 
			if int(line[3]) < int(line[5]) :
				matcid_team_result[str(line[4])+'|'+str(matcid)] = "W"
				matcid_team_result[str(line[2])+'|'+str(matcid)] = "L"

		except ValueError,e :
			continue
		matcid_year[int(matcid)] = int(years)


	#file2 = open('../Data/nba_matchid_playerid_playernames.txt','r') ## form relationship  !!!
	
	file2 = open(f2,'r') ## form relationship  !!!
	data2 = file2.readlines()
	file2.close()

	team_nodes = defaultdict(list)

	team_home_away = defaultdict(list)

	for line in data2 :
		line = line.strip()
		line = line.split()
		year = matcid_year[int(line[0])]
		try :
			if int(year) == int(start_yr) :

				team_nodes[str(line[1].lower())+'|'+str(line[0])].append(str(line[2])) ### MLB
				team_home_away[str(line[1].lower())+'|'+str(line[0])] = str(line[3])

		except TypeError,e :
			continue


	players_pair = defaultdict(list)

	for k in team_nodes :
		nodes = list(set(team_nodes[k]))
		edges = combinations(nodes,2)

		G = nx.Graph(); G.add_nodes_from(nodes); G.add_edges_from(edges) 

		for u,v in G.edges() :
			if u != v :
				players_pair[str(u)+'|'+str(v)+'|'+k.split('|')[0]+'|'+k.split('|')[1]] = str(k)


 ## now look back and see how many times players played with each other earlier !

	team_combos = []; 	team_nodes_past = defaultdict(list)

	for line in data2 :
		line = line.strip()
		line = line.split()
		year = matcid_year[int(line[0])]

		try :
			#if int(year) < int(start_yr) :
			if int(year) >= int(start_yr) - int(bin1) and int(year) < int(start_yr) :

				if str(string_type) == "suc" :

					if matcid_team_result[str(line[1].lower())+'|'+str(line[0])] == "W" : #MLB

						team_nodes_past[str(line[1].lower())+'|'+str(line[0])].append(str(line[2])) 

				if str(string_type) == "all" :

						team_nodes_past[str(line[1].lower())+'|'+str(line[0])].append(str(line[2]))

		except TypeError,e :
			continue


	for k in team_nodes_past :
		nodes2 = list(set(team_nodes_past[k]))
		edges2 = combinations(nodes2, 2)
		G2 = nx.Graph()
		G2.add_nodes_from(nodes2)
		G2.add_edges_from(edges2) 
		for u,v in G2.edges() :
			if u != v :
				team_combos.append(( str(u)+'|'+str(v) ))

	team_combos2 = defaultdict(list)

	for k, v in countDuplicatesInList(team_combos) :
		team_combos2[k] = int(v) 

	sorted(team_combos2.iterkeys())

	team_combos3 = defaultdict(list)

	for k in team_combos2 :
		k1 = k.split('|')[0]; k2 = k.split('|')[1]
		team_combos3[str(k1)+'|'+str(k2)].append(team_combos2[k]) 

	teams_id = defaultdict(list)

	for keys in players_pair :
		k1 = keys.split('|')[0]+'|'+keys.split('|')[1]
		k2 = keys.split('|')[2]+'|'+keys.split('|')[3]
		if k1 in team_combos2 :
			teams_id[k2].append(team_combos2[k1])
		if not k1 in team_combos2 :
			team_combos2[k1] = 0
			teams_id[k2].append(team_combos2[k1])



	fh6 = open(destdir+'MLB_relational_'+str(string_type)+'_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	print >> fh6, 'MatchID|Team1|mu_rel_'+str(string_type)+'_t1_bin_'+str(bin1)+'|std_rel_'+str(string_type)+'_t1_bin_'+str(bin1)+'|med_rel_'+str(string_type)+'_t1_bin_'+str(bin1)+'|score01|HAteam01|Team2|mu_rel_'+str(string_type)+'_t2_bin_'+str(bin1)+'|std_rel_'+str(string_type)+'_t2_bin_'+str(bin1)+'|med_rel_'+str(string_type)+'_t2_bin_'+str(bin1)+'|score02|HAteam02'

	#fh6 = open(destdir+'MLB_relational_'+str(string_type)+'_'+str(start_yr)+'.txt', 'w')
	#print >> fh6, 'MatchID|Team1|mu_rel_'+str(string_type)+'_t1|std_rel_'+str(string_type)+'_t1|med_rel_'+str(string_type)+'_t1|score01|HAteam01|Team2|mu_rel_'+str(string_type)+'_t2|std_rel_'+str(string_type)+'_t2|med_rel_'+str(string_type)+'_t2|score02|HAteam02'

	for line in data :
		line = line.strip()
		line = line.split('|')
		if int(line[1]) == int(start_yr) :
			team1 = line[2];team2 = line[4]
			keys1 = str(team1)+'|'+str(line[0]); keys2 = str(team2) + '|' + str(line[0])

			try :
				print >> fh6, '%d|%s|%f|%f|%f|%d|%s|%s|%f|%f|%f|%d|%s' % ( int(line[0]), str(team1), float(np.mean(teams_id[keys1])), float(np.std(teams_id[keys1])), 
																	float(np.median(teams_id[keys1])), int(line[3]), str(team_home_away[keys1]), str(team2), 
																	float(np.mean(teams_id[keys2])), float(np.std(teams_id[keys2])), float(np.median(teams_id[keys2])), int(line[5]), str(team_home_away[keys2]) )

			except ValueError,e :
				continue


def create_relational_variable_EPL(f1, f2, destdir, start_yr, bin1) :

	#file1 = open('../Data/data_for_analysis/nba_data_scores_matchid_year_team_scores.txt','r') 

	file1 = open(f1,'r') 
	data = file1.readlines()[1:]
	file1.close()

	matcid_year = defaultdict(list); matcid_team_result = defaultdict(list)

	for line in data :  
		line = line.strip().split('|')
		matcid = line[0]
		years = line[1]
  
		if int(line[3]) > int(line[5]) :
			matcid_team_result[str(line[2])+'|'+str(matcid)] = "W"
			matcid_team_result[str(line[4])+'|'+str(matcid)] = "L"

		if int(line[3]) == int(line[5]) :
			matcid_team_result[str(line[2])+'|'+str(matcid)] = "D"
			matcid_team_result[str(line[4])+'|'+str(matcid)] = "D"
 
		if int(line[3]) < int(line[5]) :
			matcid_team_result[str(line[4])+'|'+str(matcid)] = "W"
			matcid_team_result[str(line[2])+'|'+str(matcid)] = "L"

		matcid_year[int(matcid)] = int(years)


	#file2 = open('../Data/nba_matchid_playerid_playernames.txt','r') ## form relationship  !!!
	
	file2 = open(f2,'r') ## form relationship  !!!
	data2 = file2.readlines()
	file2.close()

	team_nodes = defaultdict(list)

	team_home_away = defaultdict(list)

	for line in data2 :
		line = line.strip()
		line = line.split()
		year = matcid_year[int(line[0])]
		try :
			if int(year) == int(start_yr) :

				team_nodes[str(line[1].lower())+'|'+str(line[0])].append(str(line[2])+'__'+str(line[3])) # Soccer
				team_home_away[str(line[1].lower())+'|'+str(line[0])] = str(line[5])

		except TypeError,e :
			continue


	players_pair = defaultdict(list)

	for k in team_nodes :
		nodes = list(set(team_nodes[k]))
		edges = combinations(nodes,2)

		G = nx.Graph(); G.add_nodes_from(nodes); G.add_edges_from(edges) 

		for u,v in G.edges() :
			if u != v :
				players_pair[str(u)+'|'+str(v)+'|'+k.split('|')[0]+'|'+k.split('|')[1]] = str(k)


 ## now look back and see how many times players played with each other earlier !

	team_combos = []; 	team_nodes_past = defaultdict(list)

	for line in data2 :
		line = line.strip()
		line = line.split()
		year = matcid_year[int(line[0])]
		#try :
		#	shots = line[6]
  
		#	try :
		#		if int(shots) >= 1 :
		try :
						#if int(year) < int(start_yr) :
						if int(year) >= int(start_yr) - int(bin1) and int(year) < int(start_yr) :

							if matcid_team_result[str(line[1].lower())+'|'+str(line[0])] == "W" : #Soccer
								team_nodes_past[str(line[1].lower())+'|'+str(line[0])].append(str(line[2])+'__'+str(line[3])) # Soccer

		except TypeError,e :
						continue
		#	except ValueError,e :
		#		continue
		#except IndexError,e :
		#		continue


	for k in team_nodes_past :
		nodes2 = list(set(team_nodes_past[k]))
		edges2 = combinations(nodes2, 2)
		G2 = nx.Graph()
		G2.add_nodes_from(nodes2)
		G2.add_edges_from(edges2) 
		for u,v in G2.edges() :
			if u != v :
				team_combos.append(( str(u)+'|'+str(v) ))

	team_combos2 = defaultdict(list)

	for k, v in countDuplicatesInList(team_combos) :
		team_combos2[k] = int(v) 

	sorted(team_combos2.iterkeys())

	team_combos3 = defaultdict(list)

	for k in team_combos2 :
		k1 = k.split('|')[0]; k2 = k.split('|')[1]
		team_combos3[str(k1)+'|'+str(k2)].append(team_combos2[k]) 

	teams_id = defaultdict(list)

	for keys in players_pair :
		k1 = keys.split('|')[0]+'|'+keys.split('|')[1]
		k2 = keys.split('|')[2]+'|'+keys.split('|')[3]
		if k1 in team_combos2 :
			teams_id[k2].append(team_combos2[k1])
		if not k1 in team_combos2 :
			team_combos2[k1] = 0
			teams_id[k2].append(team_combos2[k1])


#	fh6 = open(destdir+'EPL_relational_succesful_ge1shot_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
#	print >> fh6, 'MatchID|Team1|mu_rel_suc_ge1_t1_bin_'+str(bin1)+'|std_rel_suc_ge1_t1_bin_'+str(bin1)+'|med_rel_suc_ge1_t1_bin_'+str(bin1)+'|score01|HAteam01|Team2|mu_rel_suc_ge1_t2_bin_'+str(bin1)+'|std_rel_suc_ge1_t2_bin_'+str(bin1)+'|med_rel_suc_ge1_t2_bin_'+str(bin1)+'|score02|HAteam02'

	fh6 = open(destdir+'EPL_relational_succesful_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	print >> fh6, 'MatchID|Team1|mu_rel_suc_t1_bin_'+str(bin1)+'|std_rel_suc_t1_bin_'+str(bin1)+'|med_rel_suc_t1_bin_'+str(bin1)+'|score01|HAteam01|Team2|mu_rel_suc_t2_bin_'+str(bin1)+'|std_rel_suc_t2_bin_'+str(bin1)+'|med_rel_suc_t2_bin_'+str(bin1)+'|score02|HAteam02'

#	fh6 = open(destdir+'EPL_relational_all_ge1shot_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
#	print >> fh6, 'MatchID|Team1|mu_rel_all_ge1_t1_bin_'+str(bin1)+'|std_rel_all_ge1_t1_bin_'+str(bin1)+'|med_rel_all_ge1_t1_bin_'+str(bin1)+'|score01|HAteam01|Team2|mu_rel_all_ge1_t2_bin_'+str(bin1)+'|std_rel_all_ge1_t2_bin_'+str(bin1)+'|med_rel_all_ge1_t2_bin_'+str(bin1)+'|score02|HAteam02'

#	fh6 = open(destdir+'EPL_relational_all_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
#	print >> fh6, 'MatchID|Team1|mu_rel_all_t1_bin_'+str(bin1)+'|std_rel_all_t1_bin_'+str(bin1)+'|med_rel_all_t1_bin_'+str(bin1)+'|score01|HAteam01|Team2|mu_rel_all_t2_bin_'+str(bin1)+'|std_rel_all_t2_bin_'+str(bin1)+'|med_rel_all_t2_bin_'+str(bin1)+'|score02|HAteam02'

	for line in data :
		line = line.strip()
		line = line.split('|')
		if int(line[1]) == int(start_yr) :
			team1 = line[2];team2 = line[4]
			keys1 = str(team1)+'|'+str(line[0]); keys2 = str(team2) + '|' + str(line[0])
			print >> fh6, '%d|%s|%f|%f|%f|%d|%s|%s|%f|%f|%f|%d|%s' % ( int(line[0]), str(team1), float(np.mean(teams_id[keys1])), float(np.std(teams_id[keys1])), 
																	float(np.median(teams_id[keys1])), int(line[3]), str(team_home_away[keys1]), str(team2), 
																	float(np.mean(teams_id[keys2])), float(np.std(teams_id[keys2])), float(np.median(teams_id[keys2])), int(line[5]), str(team_home_away[keys2]) )



######## Here we need to create the data for different NBA Seasons #######
## @@@@@@ For each match we get the data and tag of seasons @@@@@ ##
######### Compositional as well as Relational variables ############

def gen_compositional_NBA_variables_season(f1, f2, f3, f4, f5, f6, destdir, season_str, bin1) :

	format = "%Y-%m-%d" 

	#### create a dictionary for match id and date ###
	file1 = open(f1,'r') 
	data1 = file1.readlines()[1:]
	file1.close()

	matchid_dates = defaultdict(list)

	for line in data1 :  
		line = line.strip().split('|')
		matchid = line[0]
		dates = line[1]
		matchid_dates[str(dates).split(' ')[0]].append(str(matchid)+'|'+str(line[2]))

	## read the season and min max date ###
	file2 = open(f2,'r')
	data2 = file2.readlines()[1:]
	file2.close()

	matchid_season_year = defaultdict(list); season_yr_dict = defaultdict(list)

	for line in data2 :
		line = line.strip().split('|')

		mindate = datetime.strptime(str(line[1]).split(' ')[0],format)
		maxdate = datetime.strptime(str(line[2]).split(' ')[0],format)
		season = line[0]
		for keys in matchid_dates :

			match_date = datetime.strptime(str(keys).split(' ')[0],format)

			if match_date >= mindate and match_date <= maxdate :

				for m in matchid_dates[str(keys)] :

					matchid_season_year[str(m.split('|')[0])] = season+'|'+str(match_date)+'|'+m.split('|')[1]+'|'+str(mindate)+'|'+str(maxdate)
					season_yr_dict[season] = m.split('|')[1]
	#print matchid_season_year


	#### ESPN NBA player stats ####
	file3 = open(f3,'r')
	data3 = file3.readlines()[1:]
	file3.close()

	team_pts = defaultdict(list); team_stl = defaultdict(list); team_ast = defaultdict(list); 

	for line in data3 :  
		line = line.strip().split('|')

		yrs = int(line[1].split("-'")[0].replace("'",""))
		
		if yrs > 20 : yearnew = 1900+yrs ; season = str(yearnew)+'-'+str(line[1].split("-'")[1].replace("'",""))
		if yrs <=20 : yearnew = 2000+yrs ; season = str(yearnew)+'-'+str(line[1].split("-'")[1].replace("'",""))


		seasonyr = str(season_str).split('-')[0]

		#if int(yearnew) < int(seasonyr):
		if int(yearnew) >= int(seasonyr) - int(bin1) and int(yearnew) < int(seasonyr) :

			team_pts[str(line[0])].append(float(line[3])) 
			team_stl[str(line[0])].append(float(line[4])) 
			team_ast[str(line[0])].append(float(line[5])) 


	#### NBA basketball reference ####
	file4 = open(f4,'r')
	data4 = file4.readlines()[1:]
	file4.close()

	team_dbpm = defaultdict(list); team_bpm = defaultdict(list); team_vorp = defaultdict(list); 

	for line in data4 :  
		line = line.strip().split('|')
		year = int(line[2])

		
		season_1 = str(line[1])

		if season_1 in season_yr_dict :
			yearnew = int(season_yr_dict[season_1])

			seasonyr = str(season_str).split('-')[0]
			#if yearnew < int(seasonyr) :
			if yearnew >= int(seasonyr) - int(bin1) and yearnew < int(seasonyr) :

				try :
			
					team_dbpm[str(line[0])].append(float(line[4])) 
					team_bpm[str(line[0])].append(float(line[5])) 
					team_vorp[str(line[0])].append(float(line[6])) 
			
				except ValueError,e :
					print line[0], line[1], e

	#print team_dbpm

	file5 = open(f5,'r') 
	data5 = file5.readlines()
	file5.close()

	team_nodes_pts = defaultdict(list); team_nodes_stl = defaultdict(list); team_nodes_ast = defaultdict(list); 
	team_nodes_dbpm = defaultdict(list); team_nodes_bpm = defaultdict(list); team_nodes_vorp = defaultdict(list)

	team_home_away = defaultdict(list)

	for line in data5 :
		line = line.strip()
		line = line.split()
		try :
			season = matchid_season_year[str(line[0])].split('|')[0]
			#print season

			try :
				if str(season) == str(season_str) :

					if str(line[1]) in team_pts :

						team_nodes_pts[str(line[2].lower())+'|'+str(line[0])].append(np.mean(team_pts[str(line[1])]))
						team_nodes_stl[str(line[2].lower())+'|'+str(line[0])].append(np.mean(team_stl[str(line[1])]))
						team_nodes_ast[str(line[2].lower())+'|'+str(line[0])].append(np.mean(team_ast[str(line[1])]))

					if str(line[1]) in team_dbpm :

						team_nodes_dbpm[str(line[2].lower())+'|'+str(line[0])].append(np.mean(team_dbpm[str(line[1])]))
						team_nodes_bpm[str(line[2].lower())+'|'+str(line[0])].append(np.mean(team_bpm[str(line[1])]))
						team_nodes_vorp[str(line[2].lower())+'|'+str(line[0])].append(np.mean(team_vorp[str(line[1])]))

					try :
						team_home_away[str(line[2].lower())+'|'+str(line[0])] = str(line[3])
					except IndexError,e :
						continue
			except TypeError,e :
				continue

		except AttributeError,e :
			continue

	#fh7 = open(destdir+'NBA_compositional_per_season'+'_'+str(season_str)+'.txt' , 'w')
	#print >> fh7, 'MatchID|Team1|mean_PTS_t1|mean_STL_t1|mean_AST_t1|mean_DBPM_t1|mean_BPM_t1|mean_VORP_t1|HAteam01|Team2|mean_PTS_t2|mean_STL_t2|mean_AST_t2|mean_DBPM_t2|mean_BPM_t2|mean_VORP_t2|HAteam02'

	fh7 = open(destdir+'NBA_compositional_per_season_bin_'+str(bin1)+'_'+str(season_str)+'.txt' , 'w')
	print >> fh7, 'MatchID|Team1|mean_PTS_t1_bin_'+str(bin1)+'|mean_STL_t1_bin_'+str(bin1)+'|mean_AST_t1_bin_'+str(bin1)+'|mean_DBPM_t1_bin_'+str(bin1)+'|mean_BPM_t1_bin_'+str(bin1)+'|mean_VORP_t1_bin_'+str(bin1)+'|HAteam01|Team2|mean_PTS_t2_bin_'+str(bin1)+'|mean_STL_t2_bin_'+str(bin1)+'|mean_AST_t2_bin_'+str(bin1)+'|mean_DBPM_t2_bin_'+str(bin1)+'|mean_BPM_t2_bin_'+str(bin1)+'|mean_VORP_t2_bin_'+str(bin1)+'|HAteam02'
	
	file6 = open(f6,'r') 
	data6 = file6.readlines()
	file6.close()

	for line in data6 :
		line = line.strip()
		line = line.split('|')
		try :
			season = matchid_season_year[str(line[0])].split('|')[0]

			if str(season) == str(season_str) :

				team1 = line[2]
				team2 = line[4]

				keys1 = str(team1)+'|'+str(line[0]); keys2 = str(team2)+'|'+str(line[0])

				## Average ESPN
				mean_PTS_t1 = float(np.mean(team_nodes_pts[keys1])); 	mean_PTS_t2 = float(np.mean(team_nodes_pts[keys2]))
				mean_STL_t1 = float(np.mean(team_nodes_stl[keys1]));	mean_STL_t2 = float(np.mean(team_nodes_stl[keys2]))
				mean_AST_t1 = float(np.mean(team_nodes_ast[keys1]));	mean_AST_t2 = float(np.mean(team_nodes_ast[keys2]))

				## Average Basketball reference
				mean_DBPM_t1 = float(np.mean(team_nodes_dbpm[keys1])); 	 mean_DBPM_t2 = float(np.mean(team_nodes_dbpm[keys2]))
				mean_BPM_t1 = float(np.mean(team_nodes_bpm[keys1])); 		 mean_BPM_t2 = float(np.mean(team_nodes_bpm[keys2]))
				mean_VORP_t1 = float(np.mean(team_nodes_vorp[keys1]));   mean_VORP_t2 = float(np.mean(team_nodes_vorp[keys2]))

				t1_home_away = str(team_home_away[keys1]); t2_home_away = str(team_home_away[keys2])

				print >> fh7, '%d|%s|%f|%f|%f|%f|%f|%f|%s|%s|%f|%f|%f|%f|%f|%f|%s' % ( int(line[0]), str(team1), mean_PTS_t1, mean_STL_t1, mean_AST_t1, mean_DBPM_t1, mean_BPM_t1, mean_VORP_t1, t1_home_away,
																																									 str(team2), mean_PTS_t2, mean_STL_t2, mean_AST_t2, mean_DBPM_t2, mean_BPM_t2, mean_VORP_t2, t2_home_away )
		except AttributeError, e :
			continue



def create_relational_variable_NBA_season(f1, f2, f3, f4, destdir, season_str, bin1) :

	format = "%Y-%m-%d" 

	#### create a dictionary for match id and date ###
	file1 = open(f1,'r') 
	data1 = file1.readlines()[1:]
	file1.close()

	matchid_dates = defaultdict(list)

	for line in data1 :  
		line = line.strip().split('|')
		matchid = line[0]
		dates = line[1]
		matchid_dates[str(dates).split(' ')[0]].append(str(matchid)+'|'+str(line[2]))

	## read the season and min max date ###
	file2 = open(f2,'r')
	data2 = file2.readlines()[1:]
	file2.close()

	matchid_season_year = defaultdict(list); season_yr_dict = defaultdict(list); season_min_max_dict = defaultdict(list)

	for line in data2 :
		line = line.strip().split('|')

		mindate = datetime.strptime(str(line[1]).split(' ')[0],format)
		maxdate = datetime.strptime(str(line[2]).split(' ')[0],format)
		season = line[0]

		season_min_max_dict[season] = str(line[1])+'|'+str(line[2])

		for keys in matchid_dates :

			match_date = datetime.strptime(str(keys).split(' ')[0],format)

			if match_date >= mindate and match_date <= maxdate :

				for m in matchid_dates[str(keys)] :

					matchid_season_year[str(m.split('|')[0])] = season+'|'+str(match_date)+'|'+m.split('|')[1]+'|'+str(mindate)+'|'+str(maxdate)
					season_yr_dict[season] = m.split('|')[1]
	#print season_yr_dict

	file3 = open(f3,'r') 
	data3 = file3.readlines()[1:]
	file3.close()

	matcid_year = defaultdict(list); matcid_team_result = defaultdict(list)

	for line in data3 :  
		line = line.strip().split('|')
		matcid = line[0]
		years = line[1]
  
		if int(line[3]) > int(line[5]) :
			matcid_team_result[str(line[2])+'|'+str(matcid)] = "W"
			matcid_team_result[str(line[4])+'|'+str(matcid)] = "L"

		if int(line[3]) == int(line[5]) :
			matcid_team_result[str(line[2])+'|'+str(matcid)] = "D"
			matcid_team_result[str(line[4])+'|'+str(matcid)] = "D"
 
		if int(line[3]) < int(line[5]) :
			matcid_team_result[str(line[4])+'|'+str(matcid)] = "W"
			matcid_team_result[str(line[2])+'|'+str(matcid)] = "L"

		matcid_year[int(matcid)] = int(years)


	#file2 = open('../Data/nba_matchid_playerid_playernames.txt','r') ## form relationship  !!!
	
	file4 = open(f4,'r') ## form relationship  !!!
	data4 = file4.readlines()
	file4.close()

	team_nodes = defaultdict(list)

	team_home_away = defaultdict(list)

	for line in data4 :
		line = line.strip()
		line = line.split()
		try :
			season = matchid_season_year[str(line[0])].split('|')[0]

			try :

				if str(season) == str(season_str) :

					team_nodes[str(line[2].lower())+'|'+str(line[0])].append(str(line[1])) ### NBA
					try :
						team_home_away[str(line[2].lower())+'|'+str(line[0])] = str(line[3])
					except IndexError,e :
						continue	

			except TypeError,e :
				continue

		except AttributeError,e :
			continue


	players_pair = defaultdict(list)

	for k in team_nodes :
		nodes = list(set(team_nodes[k]))
		edges = combinations(nodes,2)

		G = nx.Graph(); G.add_nodes_from(nodes); G.add_edges_from(edges) 

		for u,v in G.edges() :
			if u != v :
				players_pair[str(u)+'|'+str(v)+'|'+k.split('|')[0]+'|'+k.split('|')[1]] = str(k)


 ## now look back and see how many times players played with each other earlier !

	team_combos = []; 	team_nodes_past = defaultdict(list)
	
	season_mindate = datetime.strptime(season_min_max_dict[str(season_str)].split('|')[0].split(' ')[0], format)
	season_maxdate = datetime.strptime(season_min_max_dict[str(season_str)].split('|')[1].split(' ')[0], format)

	## construct the season bin ###
	s1 = season_str.split('-')[0]; s2 = season_str.split('-')[1]

	season_bin = str(int(s1)-int(bin1))+'-'+c2str(str(int(s2)-int(bin1)))
	
	#print season_bin

	season_bin_mindate = datetime.strptime(season_min_max_dict[str(season_bin)].split('|')[0].split(' ')[0], format)
	season_bin_maxdate = datetime.strptime(season_min_max_dict[str(season_bin)].split('|')[1].split(' ')[0], format)

	for line in data4 :
		line = line.strip()
		line = line.split()
		year = matcid_year[int(line[0])]
		seasonyr = str(season_str).split('-')[0]
		try :
		
			try:
				try :
					dates = datetime.strptime(line[4], format)

					#if dates < season_mindate :
					if dates >= season_bin_mindate and dates < season_mindate :

						if matcid_team_result[str(line[2].lower())+'|'+str(line[0])] == "W" : #NBA
							team_nodes_past[str(line[2].lower())+'|'+str(line[0])].append(str(line[1])) ### NBA

				except IndexError,e :
					continue
			except ValueError,e :
				continue
		
		except AttributeError,e :
			continue

	#print team_nodes_past

	for k in team_nodes_past :
		nodes2 = list(set(team_nodes_past[k]))
		edges2 = combinations(nodes2, 2)
		G2 = nx.Graph()
		G2.add_nodes_from(nodes2)
		G2.add_edges_from(edges2) 
		for u,v in G2.edges() :
			if u != v :
				team_combos.append(( str(u)+'|'+str(v) ))

	team_combos2 = defaultdict(list)

	for k, v in countDuplicatesInList(team_combos) :
		team_combos2[k] = int(v) 

	sorted(team_combos2.iterkeys())

	team_combos3 = defaultdict(list)

	for k in team_combos2 :
		k1 = k.split('|')[0]; k2 = k.split('|')[1]
		team_combos3[str(k1)+'|'+str(k2)].append(team_combos2[k]) 

	teams_id = defaultdict(list)

	for keys in players_pair :
		k1 = keys.split('|')[0]+'|'+keys.split('|')[1]
		k2 = keys.split('|')[2]+'|'+keys.split('|')[3]
		if k1 in team_combos2 :
			teams_id[k2].append(team_combos2[k1])
		if not k1 in team_combos2 :
			team_combos2[k1] = 0
			teams_id[k2].append(team_combos2[k1])


	#fh6 = open(destdir+'NBA_relational_succesful_per_season_'+str(season_str)+'.txt', 'w')
	#print >> fh6, 'MatchID|Team1|mu_rel_suc_t1|std_rel_suc_t1|med_rel_suc_t1_bin|score01|HAteam01|Team2|mu_rel_suc_t2|std_rel_suc_t2|med_rel_suc_t2|score02|HAteam02'
	
	#fh6 = open(destdir+'NBA_relational_all_per_season_'+str(season_str)+'.txt', 'w')
	#print >> fh6, 'MatchID|Team1|mu_rel_all_t1|std_rel_all_t1|med_rel_all_t1|score01|HAteam01|Team2|mu_rel_all_t2|std_rel_all_t2|med_rel_all_t2|score02|HAteam02'

	#fh6 = open(destdir+'NBA_relational_succesful_bin_'+str(bin1)+'_'+str(season_str)+'.txt', 'w')
	#print >> fh6, 'MatchID|Team1|mu_rel_suc_t1_bin_'+str(bin1)+'|std_rel_suc_t1_bin_'+str(bin1)+'|med_rel_suc_t1_bin_'+str(bin1)+'|score01|HAteam01|Team2|mu_rel_suc_t2_bin_'+str(bin1)+'|std_rel_suc_t2_bin_'+str(bin1)+'|med_rel_suc_t2_bin_'+str(bin1)+'|score02|HAteam02'

	fh6 = open(destdir+'NBA_relational_all_bin_'+str(bin1)+'_'+str(season_str)+'.txt', 'w')
	print >> fh6, 'MatchID|Team1|mu_rel_all_t1_bin_'+str(bin1)+'|std_rel_all_t1_bin_'+str(bin1)+'|med_rel_all_t1_bin_'+str(bin1)+'|score01|HAteam01|Team2|mu_rel_all_t2_bin_'+str(bin1)+'|std_rel_all_t2_bin_'+str(bin1)+'|med_rel_all_t2_bin_'+str(bin1)+'|score02|HAteam02'
	


	#fh6 = open(destdir+'NBA_relational_noDNP_all_bin_'+str(bin1)+'_'+str(season_str)+'.txt', 'w')
	#print >> fh6, 'MatchID|Team1|mu_rel_noDNP_all_t1_bin_'+str(bin1)+'|std_rel_noDNP_all_t1_bin_'+str(bin1)+'|med_rel_noDNP_all_t1_bin_'+str(bin1)+'|score01|HAteam01|Team2|mu_rel_noDNP_all_t2_bin_'+str(bin1)+'|std_rel_noDNP_all_t2_bin_'+str(bin1)+'|med_rel_noDNP_all_t2_bin_'+str(bin1)+'|score02|HAteam02'

	#fh6 = open(destdir+'NBA_relational_noDNP_succesful_per_season_'+str(season_str)+'.txt', 'w')
	#print >> fh6, 'MatchID|Team1|mu_rel_noDNP_suc_t1|std_rel_noDNP_suc_t1|med_rel_noDNP_suc_t1|score01|HAteam01|Team2|mu_rel_noDNP_suc_t2|std_rel_noDNP_suc_t2|med_rel_noDNP_suc_t2|score02|HAteam02'

	#fh6 = open(destdir+'NBA_relational_noDNP_succesful_bin_'+str(bin1)+'_'+str(season_str)+'.txt', 'w')
	#print >> fh6, 'MatchID|Team1|mu_rel_noDNP_suc_t1_bin_'+str(bin1)+'|std_rel_noDNP_suc_t1_bin_'+str(bin1)+'|med_rel_noDNP_suc_t1_bin_'+str(bin1)+'|score01|HAteam01|Team2|mu_rel_noDNP_suc_t2_bin_'+str(bin1)+'|std_rel_noDNP_suc_t2_bin_'+str(bin1)+'|med_rel_noDNP_suc_t2_bin_'+str(bin1)+'|score02|HAteam02'

	#fh6 = open(destdir+'NBA_relational_noDNP_all_per_season_'+str(season_str)+'.txt', 'w')
	#print >> fh6, 'MatchID|Team1|mu_rel_noDNP_all_t1|std_rel_noDNP_all_t1|med_rel_noDNP_all_t1|score01|HAteam01|Team2|mu_rel_noDNP_all_t2|std_rel_noDNP_all_t2|med_rel_noDNP_all_t2|score02|HAteam02'


	for line in data3 :
		line = line.strip()
		line = line.split('|')

		try :
			season = matchid_season_year[str(line[0])].split('|')[0]

			if str(season) == str(season_str) :

				team1 = line[2];team2 = line[4]
				keys1 = str(team1)+'|'+str(line[0]); keys2 = str(team2) + '|' + str(line[0])
				
				print >> fh6, '%d|%s|%f|%f|%f|%d|%s|%s|%f|%f|%f|%d|%s' % ( int(line[0]), str(team1), float(np.mean(teams_id[keys1])), float(np.std(teams_id[keys1])), 
																	float(np.median(teams_id[keys1])), int(line[3]), str(team_home_away[keys1]), str(team2), 
																	float(np.mean(teams_id[keys2])), float(np.std(teams_id[keys2])), float(np.median(teams_id[keys2])), int(line[5]), str(team_home_away[keys2]) )

		except AttributeError, e :
			continue


######## Here we need to create the data for different EPL Seasons #######
## @@@@@@ For each match we get the data and tag of seasons @@@@@ ##
######### Compositional as well as Relational variables ############

def gen_compositional_EPL_variables_season(f1, f3, f5, f6, destdir, season_str, bin1) :

	format = "%Y-%m-%d" 

	#### create a dictionary for match id and date ###
	file1 = open(f1,'r') 
	data1 = file1.readlines()[1:]
	file1.close()

	matchid_dates = defaultdict(list); 	matchid_season_year = defaultdict(list); season_yr_dict = defaultdict(list)
	season_dict_dates = defaultdict(list)

	for line in data1 :  
		line = line.strip().split('|')

		matchid = line[0]
		dates = line[2]
		seasons = line[1]

		matchid_dates[str(dates).split(' ')[0]].append(str(matchid)+'|'+str(line[3]))
		season_yr_dict[str(seasons)] = int(line[3])

		season_dict_dates[str(seasons)].append(str(dates))


	## read the season and min max date ###

	for k in season_dict_dates :


		mindate = datetime.strptime((min(season_dict_dates[k])).split(' ')[0],format)
		maxdate = datetime.strptime((max(season_dict_dates[k])).split(' ')[0],format)

		season = k

		for keys in matchid_dates :

			match_date = datetime.strptime(str(keys).split(' ')[0],format)

			if match_date >= mindate and match_date <= maxdate :

				for m in matchid_dates[str(keys)] :

					matchid_season_year[str(m.split('|')[0])] = season+'|'+str(match_date)+'|'+m.split('|')[1]+'|'+str(mindate)+'|'+str(maxdate)

	#print matchid_season_year


	#### ESPN EPL player stats ####
	file3 = open(f3,'r')
	data3 = file3.readlines()[1:]
	file3.close()

	team_goals = defaultdict(list); team_assists = defaultdict(list); team_shots = defaultdict(list); 

	for line in data3 :  
		line = line.strip().split('|')

		try :
			yearnew = int(line[2])
			seasonyr = str(season_str).split('-')[0]
		except ValueError,e :
			continue

		#if str(line[4]) == "Prem" :
			#if int(yearnew) < int(seasonyr):
		if int(yearnew) >= int(seasonyr) - int(bin1) and int(yearnew) < int(seasonyr) :
				try :
					if float(line[7]) > 0.0 :
						team_goals[str(line[0])+'__'+str(line[1])].append(float(line[5])) 
						team_assists[str(line[0])+'__'+str(line[1])].append(float(line[6])) 
						team_shots[str(line[0])+'__'+str(line[1])].append(float(line[7])) 
				except ValueError,e :
					continue


	file5 = open(f5,'r') 
	data5 = file5.readlines()
	file5.close()

	team_nodes_goals = defaultdict(list); team_nodes_assits = defaultdict(list); team_nodes_shots = defaultdict(list); 

	team_home_away = defaultdict(list)

	for line in data5 :
		line = line.strip()
		line = line.split()
		try :
			season = matchid_season_year[str(line[0])].split('|')[0]
			#print season

			try :
				if str(season) == str(season_str) :

					if str(line[1]) in team_goals :

						team_nodes_goals[str(line[2].lower())+'|'+str(line[0])].append(np.mean(team_goals[str(line[1])]))
						team_nodes_assits[str(line[2].lower())+'|'+str(line[0])].append(np.mean(team_assists[str(line[1])]))
						team_nodes_shots[str(line[2].lower())+'|'+str(line[0])].append(np.mean(team_shots[str(line[1])]))


			except TypeError,e :
				continue

		except AttributeError,e :
			continue

	#print team_nodes_goals

	#fh7 = open(destdir+'EPL_compositional_per_season'+'_'+str(season_str)+'.txt' , 'w')
	#print >> fh7, 'MatchID|Team1ID|Team1|score_t1|mean_goals_t1|mean_assists_t1|mean_shots_t1|HAteam01|Team2ID|Team2|score_t2|mean_goals_t2|mean_assists_t2|mean_shots_t2|HAteam02'

	#fh7 = open(destdir+'EPL_compositional_per_season_bin_'+str(bin1)+'_'+str(season_str)+'.txt' , 'w')
	#print >> fh7, 'MatchID|Team1ID|Team1|score_t1|mean_goals_t1_bin_'+str(bin1)+'|mean_assists_t1_bin_'+str(bin1)+'|mean_shots_t1_bin_'+str(bin1)+'|HAteam01|Team2ID|Team2|score_t2|mean_goals_t2_bin_'+str(bin1)+'|mean_assists_t2_bin_'+str(bin1)+'|mean_shots_t2_bin_'+str(bin1)+'|HAteam02'

	#fh7 = open(destdir+'EPL_compositional_prem_per_season'+'_'+str(season_str)+'.txt' , 'w')
	#print >> fh7, 'MatchID|Team1ID|Team1|score_t1|epl_mean_goals_t1|epl_mean_assists_t1|epl_mean_shots_t1|HAteam01|Team2ID|Team2|score_t2|epl_mean_goals_t2|epl_mean_assists_t2|epl_mean_shots_t2|HAteam02'

	#fh7 = open(destdir+'EPL_compositional_prem_per_season_bin_'+str(bin1)+'_'+str(season_str)+'.txt' , 'w')
	#print >> fh7, 'MatchID|Team1ID|Team1|score_t1|epl_mean_goals_t1_bin_'+str(bin1)+'|epl_mean_assists_t1_bin_'+str(bin1)+'|epl_mean_shots_t1_bin_'+str(bin1)+'|HAteam01|Team2ID|Team2|score_t2|epl_mean_goals_t2_bin_'+str(bin1)+'|epl_mean_assists_t2_bin_'+str(bin1)+'|epl_mean_shots_t2_bin_'+str(bin1)+'|HAteam02'

	fh7 = open(destdir+'EPL_compositional_per_season_ge1shot_bin_'+str(bin1)+'_'+str(season_str)+'.txt' , 'w')
	print >> fh7, 'MatchID|Team1ID|Team1|score_t1|mean_goals_ge1shot_t1_bin_'+str(bin1)+'|mean_assists_ge1shot_t1_bin_'+str(bin1)+'|mean_shots_ge1shot_t1_bin_'+str(bin1)+'|HAteam01|Team2ID|Team2|score_t2|mean_goals_ge1shot_t2_bin_'+str(bin1)+'|mean_assists_ge1shot_t2_bin_'+str(bin1)+'|mean_shots_ge1shot_t2_bin_'+str(bin1)+'|HAteam02'
	


	file6 = open(f6,'r') 
	data6 = file6.readlines()
	file6.close()

	for line in data6 :
		line = line.strip()
		line = line.split('|')
		try :
			season = matchid_season_year[str(line[0])].split('|')[0]

			if str(season) == str(season_str) :
				#print line[0]

				team1 = line[3]; team1id = line[2]; score_t1 = line[4]
				team2 = line[7]; team2id = line[6]; score_t2 = line[9]

				keys1 = str(team1)+'|'+str(line[0]); keys2 = str(team2)+'|'+str(line[0])

				## Average EPL
				mean_goal_t1 = float(np.mean(team_nodes_goals[keys1])); 	 mean_goal_t2 = float(np.mean(team_nodes_goals[keys2]))
				mean_assists_t1 = float(np.mean(team_nodes_assits[keys1])); mean_assists_t2 = float(np.mean(team_nodes_assits[keys2]))
				mean_shots_t1 = float(np.mean(team_nodes_shots[keys1]));	 mean_shots_t2 = float(np.mean(team_nodes_shots[keys2]))

				t1_home_away = line[5]; t2_home_away = line[8]

				print >> fh7, '%d|%s|%s|%s|%f|%f|%f|%s|%s|%s|%s|%f|%f|%f|%s' % ( int(line[0]), team1id, str(team1), score_t1, mean_goal_t1, mean_assists_t1, mean_shots_t1, t1_home_away,
																					team2id, str(team2), score_t2, mean_goal_t2, mean_assists_t2, mean_shots_t2, t2_home_away )
		except AttributeError, e :
			continue


def create_relational_variable_EPL_season(f1, f3, f4, destdir, season_str) :

	format = "%Y-%m-%d" 

	#### create a dictionary for match id and date ###
	file1 = open(f1,'r') 
	data1 = file1.readlines()[1:]
	file1.close()

	matchid_dates = defaultdict(list); 	matchid_season_year = defaultdict(list); season_yr_dict = defaultdict(list)
	season_dict_dates = defaultdict(list)

	for line in data1 :  
		line = line.strip().split('|')

		matchid = line[0]
		dates = line[2]
		seasons = line[1]

		matchid_dates[str(dates).split(' ')[0]].append(str(matchid)+'|'+str(line[3]))
		season_yr_dict[str(seasons)] = int(line[3])

		season_dict_dates[str(seasons)].append(str(dates))


	## read the season and min max date ###
	season_min_max_dict = defaultdict(list)
	for k in season_dict_dates :


		mindate = datetime.strptime((min(season_dict_dates[k])).split(' ')[0],format)
		maxdate = datetime.strptime((max(season_dict_dates[k])).split(' ')[0],format)

		season = k
		season_min_max_dict[str(season)] = str(mindate)+'|'+str(maxdate)

		for keys in matchid_dates :

			match_date = datetime.strptime(str(keys).split(' ')[0],format)

			if match_date >= mindate and match_date <= maxdate :

				for m in matchid_dates[str(keys)] :

					matchid_season_year[str(m.split('|')[0])] = season+'|'+str(match_date)+'|'+m.split('|')[1]+'|'+str(mindate)+'|'+str(maxdate)
	#print season_yr_dict

	file3 = open(f3,'r') 
	data3 = file3.readlines()[1:]
	file3.close()

	matcid_year = defaultdict(list); matcid_team_result = defaultdict(list)

	for line in data3 :  
		line = line.strip().split('|')
		matcid = line[0]
		years = line[1]
		try :
			#print line[0], line[4], line[9]
			if int(line[4]) > int(line[9]) :
				matcid_team_result[str(line[3])+'|'+str(matcid)] = "W"
				matcid_team_result[str(line[7])+'|'+str(matcid)] = "L"

			if int(line[4]) == int(line[9]) :
				matcid_team_result[str(line[3])+'|'+str(matcid)] = "D"
				matcid_team_result[str(line[7])+'|'+str(matcid)] = "D"
 
			if int(line[4]) < int(line[9]) :
				matcid_team_result[str(line[3])+'|'+str(matcid)] = "W"
				matcid_team_result[str(line[7])+'|'+str(matcid)] = "L"

		except ValueError,e :
			continue
		matcid_year[int(matcid)] = int(years)


	#file2 = open('../Data/nba_matchid_playerid_playernames.txt','r') ## form relationship  !!!
	
	file4 = open(f4,'r') ## form relationship  !!!
	data4 = file4.readlines()
	file4.close()

	team_nodes = defaultdict(list)

	team_home_away = defaultdict(list)

	for line in data4 :
		line = line.strip()
		line = line.split()
		try :
			season = matchid_season_year[str(line[0])].split('|')[0]

			try :

				if str(season) == str(season_str) :

					team_nodes[str(line[2].lower())+'|'+str(line[0])].append(str(line[1])) ### EPL

			except TypeError,e :
				continue

		except AttributeError,e :
			continue


	players_pair = defaultdict(list)

	for k in team_nodes :
		nodes = list(set(team_nodes[k]))
		edges = combinations(nodes,2)

		G = nx.Graph(); G.add_nodes_from(nodes); G.add_edges_from(edges) 

		for u,v in G.edges() :
			if u != v :
				players_pair[str(u)+'|'+str(v)+'|'+k.split('|')[0]+'|'+k.split('|')[1]] = str(k)


 ## now look back and see how many times players played with each other earlier !

	team_combos = []; 	team_nodes_past = defaultdict(list)
	
	season_mindate = datetime.strptime(season_min_max_dict[str(season_str)].split('|')[0].split(' ')[0], format)
	season_maxdate = datetime.strptime(season_min_max_dict[str(season_str)].split('|')[1].split(' ')[0], format)

	## construct the season bin ###
	#s1 = season_str.split('-')[0]; s2 = season_str.split('-')[1]

	#season_bin = str(int(s1)-int(bin1))+'-'+c2str(str(int(s2)-int(bin1)))
	
	#print season_bin

	#season_bin_mindate = datetime.strptime(season_min_max_dict[str(season_bin)].split('|')[0].split(' ')[0], format)
	#season_bin_maxdate = datetime.strptime(season_min_max_dict[str(season_bin)].split('|')[1].split(' ')[0], format)

	for line in data4 :
		line = line.strip()
		line = line.split()
		year = matcid_year[int(line[0])]
		seasonyr = str(season_str).split('-')[0]
		try :
		
			try:
				try :
					dates = datetime.strptime(line[4], format)

					if dates < season_mindate :
					#if dates >= season_bin_mindate and dates < season_mindate :

						if matcid_team_result[str(line[2].lower())+'|'+str(line[0])] == "W" :
						#if matcid_team_result[str(line[2].lower())+'|'+str(line[0])] != "L" :

							team_nodes_past[str(line[2].lower())+'|'+str(line[0])].append(str(line[1])) 

				except IndexError,e :
					continue
			except ValueError,e :
				continue
		
		except AttributeError,e :
			continue

	#print team_nodes_past

	for k in team_nodes_past :
		nodes2 = list(set(team_nodes_past[k]))
		edges2 = combinations(nodes2, 2)
		G2 = nx.Graph()
		G2.add_nodes_from(nodes2)
		G2.add_edges_from(edges2) 
		for u,v in G2.edges() :
			if u != v :
				team_combos.append(( str(u)+'|'+str(v) ))

	team_combos2 = defaultdict(list)

	for k, v in countDuplicatesInList(team_combos) :
		team_combos2[k] = int(v) 

	sorted(team_combos2.iterkeys())

	team_combos3 = defaultdict(list)

	for k in team_combos2 :
		k1 = k.split('|')[0]; k2 = k.split('|')[1]
		team_combos3[str(k1)+'|'+str(k2)].append(team_combos2[k]) 

	teams_id = defaultdict(list)

	for keys in players_pair :
		k1 = keys.split('|')[0]+'|'+keys.split('|')[1]
		k2 = keys.split('|')[2]+'|'+keys.split('|')[3]
		if k1 in team_combos2 :
			teams_id[k2].append(team_combos2[k1])
		if not k1 in team_combos2 :
			team_combos2[k1] = 0
			teams_id[k2].append(team_combos2[k1])


	fh6 = open(destdir+'EPL_relational_succesful_per_season_'+str(season_str)+'.txt', 'w')
	print >> fh6, 'MatchID|Team1ID|Team1|score_t1|mu_rel_suc_t1|std_rel_suc_t1|med_rel_suc_t1|HAteam01|Team2ID|Team2|score_t2|mu_rel_suc_t2|std_rel_suc_t2|med_rel_suc_t2|HAteam02'
	
	#fh6 = open(destdir+'EPL_relational_all_per_season_'+str(season_str)+'.txt', 'w')
	#print >> fh6, 'MatchID|Team1ID|Team1|score_t1|mu_rel_all_t1|std_rel_all_t1|med_rel_all_t1|HAteam01|Team2ID|Team2|score_t2|mu_rel_all_t2|std_rel_all_t2|med_rel_all_t2|HAteam02'

	#fh6 = open(destdir+'EPL_relational_succesful_bin_'+str(bin1)+'_'+str(season_str)+'.txt', 'w')
	#print >> fh6, 'MatchID|Team1ID|Team1|score_t1|mu_rel_suc_t1_bin_'+str(bin1)+'|std_rel_suc_t1_bin_'+str(bin1)+'|med_rel_suc_t1_bin_'+str(bin1)+'|HAteam01|Team2ID|Team2|score_t2|mu_rel_suc_t2_bin_'+str(bin1)+'|std_rel_suc_t2_bin_'+str(bin1)+'|med_rel_suc_t2_bin_'+str(bin1)+'|HAteam02'

	#fh6 = open(destdir+'EPL_relational_all_bin_'+str(bin1)+'_'+str(season_str)+'.txt', 'w')
	#print >> fh6, 'MatchID|Team1ID|Team1|score_t1|mu_rel_all_t1_bin_'+str(bin1)+'|std_rel_all_t1_bin_'+str(bin1)+'|med_rel_all_t1_bin_'+str(bin1)+'|HAteam01|Team2ID|Team2|score_t2|mu_rel_all_t2_bin_'+str(bin1)+'|std_rel_all_t2_bin_'+str(bin1)+'|med_rel_all_t2_bin_'+str(bin1)+'|HAteam02'

	#fh6 = open(destdir+'EPL_rel_win_draw_per_season_'+str(season_str)+'.txt', 'w')
	#print >> fh6, 'MatchID|Team1ID|Team1|score_t1|mu_rel_windraw_t1|std_rel_windraw_t1|med_rel_windraw_t1|HAteam01|Team2ID|Team2|score_t2|mu_rel_windraw_t2|std_rel_windraw_t2|med_rel_windraw_t2|HAteam02'



	for line in data3 :
		line = line.strip()
		line = line.split('|')

		#try :
		season = matchid_season_year[str(line[0])].split('|')[0]

		if str(season) == str(season_str) :

				team1 = line[3]; team1id = line[2]; score_t1 = line[4]
				team2 = line[7]; team2id = line[6]; score_t2 = line[9]

				keys1 = str(team1)+'|'+str(line[0]); keys2 = str(team2)+'|'+str(line[0])

				t1_home_away = line[5]; t2_home_away = line[8]
				#print int(line[0]), str(team1), np.mean(teams_id[keys1]), np.std(teams_id[keys1]), np.median(teams_id[keys1]), str(team2), np.mean(teams_id[keys2]), np.std(teams_id[keys2]), np.median(teams_id[keys2])

				print >> fh6, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (line[0], team1id, team1, score_t1, np.mean(teams_id[keys1]), np.std(teams_id[keys1]), 
																	np.median(teams_id[keys1]), t1_home_away, team2id, team2, score_t2, np.mean(teams_id[keys2]), np.std(teams_id[keys2]), np.median(teams_id[keys2]), t2_home_away )

		#except AttributeError, e :
		#	continue


######## 									     #######
## @@@@@ 1B/2B/3B/SS infielder positions in MLB @@@@ ##
######### MLB Infield Relational variables ############


def create_relational_variable_infield_MLB(f1, f2, f3, destdir, string_type, start_yr) :


	file1 = open(f1,'r') 
	data = file1.readlines()[1:]
	file1.close()

	matcid_year = defaultdict(list); matcid_team_result = defaultdict(list)

	for line in data :  
		line = line.strip().split('|')
		matcid = line[0]
		years = line[1]
		try :

			if int(line[3]) > int(line[5]) :
				matcid_team_result[str(line[2])+'|'+str(matcid)] = "W"
				matcid_team_result[str(line[4])+'|'+str(matcid)] = "L"

			if int(line[3]) == int(line[5]) :
				matcid_team_result[str(line[2])+'|'+str(matcid)] = "D"
				matcid_team_result[str(line[4])+'|'+str(matcid)] = "D"
 
			if int(line[3]) < int(line[5]) :
				matcid_team_result[str(line[4])+'|'+str(matcid)] = "W"
				matcid_team_result[str(line[2])+'|'+str(matcid)] = "L"

		except ValueError,e :
			continue
		matcid_year[int(matcid)] = int(years)


	
	file2 = open(f2,'r') ## form relationship  !!!
	data2 = file2.readlines()
	file2.close()

	team_nodes = defaultdict(list)

	team_home_away = defaultdict(list)

	for line in data2 :
		line = line.strip()
		line = line.split()
		year = matcid_year[int(line[0])]
		try :
			if int(year) == int(start_yr) :

				## infield players
				if str(line[4]) == "1B" or str(line[4]) == "2B" or str(line[4]) == "3B" or str(line[4]) == "SS" : 
				
					team_nodes[str(line[1].lower())+'|'+str(line[0])].append(str(line[2])) ### MLB
					team_home_away[str(line[1].lower())+'|'+str(line[0])] = str(line[3])

		except TypeError,e :
			continue


	players_pair = defaultdict(list)

	for k in team_nodes :
		nodes = list(set(team_nodes[k]))
		edges = combinations(nodes,2)

		G = nx.Graph(); G.add_nodes_from(nodes); G.add_edges_from(edges) 

		for u,v in G.edges() :
			if u != v :
				players_pair[str(u)+'|'+str(v)+'|'+k.split('|')[0]+'|'+k.split('|')[1]] = str(k)


 ## now look back and see how many times players played with each other earlier !

	team_combos = []; 	team_nodes_past = defaultdict(list)

	file3 = open(f3,'r') ## form relationship  !!!
	data3 = file3.readlines()
	file3.close()

	for line in data3 :
		line = line.strip()
		line = line.split()
		year = matcid_year[int(line[0])]

		try :
			if int(year) < int(start_yr) :
			#if int(year) >= int(start_yr) - int(bin1) and int(year) < int(start_yr) :

				if str(string_type) == "suc" :

					if matcid_team_result[str(line[1].lower())+'|'+str(line[0])] == "W" : #MLB

						team_nodes_past[str(line[1].lower())+'|'+str(line[0])].append(str(line[2])) 

				if str(string_type) == "all" :

						team_nodes_past[str(line[1].lower())+'|'+str(line[0])].append(str(line[2]))

		except TypeError,e :
			continue


	for k in team_nodes_past :
		nodes2 = list(set(team_nodes_past[k]))
		edges2 = combinations(nodes2, 2)
		G2 = nx.Graph()
		G2.add_nodes_from(nodes2)
		G2.add_edges_from(edges2) 
		for u,v in G2.edges() :
			if u != v :
				team_combos.append(( str(u)+'|'+str(v) ))

	team_combos2 = defaultdict(list)

	for k, v in countDuplicatesInList(team_combos) :
		team_combos2[k] = int(v) 

	sorted(team_combos2.iterkeys())

	team_combos3 = defaultdict(list)

	for k in team_combos2 :
		k1 = k.split('|')[0]; k2 = k.split('|')[1]
		team_combos3[str(k1)+'|'+str(k2)].append(team_combos2[k]) 

	teams_id = defaultdict(list)

	for keys in players_pair :
		k1 = keys.split('|')[0]+'|'+keys.split('|')[1]
		k2 = keys.split('|')[2]+'|'+keys.split('|')[3]
		if k1 in team_combos2 :
			teams_id[k2].append(team_combos2[k1])
		if not k1 in team_combos2 :
			team_combos2[k1] = 0
			teams_id[k2].append(team_combos2[k1])



	#fh6 = open(destdir+'MLB_relational_infield_'+str(string_type)+'_bin_'+str(bin1)+'_'+str(start_yr)+'.txt', 'w')
	#print >> fh6, 'MatchID|Team1|mu_rel_infield_'+str(string_type)+'_t1_bin_'+str(bin1)+'|std_rel_infield_'+str(string_type)+'_t1_bin_'+str(bin1)+'|med_rel_infield_'+str(string_type)+'_t1_bin_'+str(bin1)+'|score01|HAteam01|Team2|mu_rel_infield_'+str(string_type)+'_t2_bin_'+str(bin1)+'|std_rel_infield_'+str(string_type)+'_t2_bin_'+str(bin1)+'|med_rel_infield_'+str(string_type)+'_t2_bin_'+str(bin1)+'|score02|HAteam02'

	fh6 = open(destdir+'MLB_relational_infield_'+str(string_type)+'_'+str(start_yr)+'.txt', 'w')
	print >> fh6, 'MatchID|Team1|mu_rel_infield_'+str(string_type)+'_t1|std_rel_infield_'+str(string_type)+'_t1|med_rel_infield_'+str(string_type)+'_t1|score01|HAteam01|Team2|mu_rel_infield_'+str(string_type)+'_t2|std_rel_infield_'+str(string_type)+'_t2|med_rel_infield_'+str(string_type)+'_t2|score02|HAteam02'

	for line in data :
		line = line.strip()
		line = line.split('|')
		if int(line[1]) == int(start_yr) :
			team1 = line[2];team2 = line[4]
			keys1 = str(team1)+'|'+str(line[0]); keys2 = str(team2) + '|' + str(line[0])

			try :
				print >> fh6, '%d|%s|%f|%f|%f|%d|%s|%s|%f|%f|%f|%d|%s' % ( int(line[0]), str(team1), float(np.mean(teams_id[keys1])), float(np.std(teams_id[keys1])), 
																	float(np.median(teams_id[keys1])), int(line[3]), str(team_home_away[keys1]), str(team2), 
																	float(np.mean(teams_id[keys2])), float(np.std(teams_id[keys2])), float(np.median(teams_id[keys2])), int(line[5]), str(team_home_away[keys2]) )

			except ValueError,e :
				continue

##### @@@@@@@@@@@ ########
### Ecosystem variable ###
##### @@@@@@@@@@@ ########

def create_ecosystem_variable_EPL_season(f1, f3, f4, f5, destdir, season_str) :

	format = "%Y-%m-%d" ; format1 = "%b %d, %Y"

	#### create a dictionary for match id and date ###
	file1 = open(f1,'r') 
	data1 = file1.readlines()[1:]
	file1.close()

	matchid_dates = defaultdict(list); 	matchid_season_year = defaultdict(list); season_yr_dict = defaultdict(list)
	season_dict_dates = defaultdict(list)

	for line in data1 :  
		line = line.strip().split('|')

		matchid = line[0]
		dates = line[2]
		seasons = line[1].split('_')[0].replace('/','-')

		matchid_dates[str(dates).split(' ')[0]].append(str(matchid)+'|'+str(line[3]))
		season_yr_dict[str(seasons)] = int(line[3])

		season_dict_dates[str(seasons)].append(str(dates))


	## read the season and min max date ###
	season_min_max_dict = defaultdict(list)
	for k in season_dict_dates :


		mindate = datetime.strptime((min(season_dict_dates[k])).split(' ')[0],format)
		maxdate = datetime.strptime((max(season_dict_dates[k])).split(' ')[0],format)

		season = k
		season_min_max_dict[str(season)] = str(mindate)+'|'+str(maxdate)

		for keys in matchid_dates :

			match_date = datetime.strptime(str(keys).split(' ')[0],format)

			if match_date >= mindate and match_date <= maxdate :

				for m in matchid_dates[str(keys)] :

					matchid_season_year[str(m.split('|')[0])] = season+'|'+str(match_date)+'|'+m.split('|')[1]+'|'+str(mindate)+'|'+str(maxdate)
	#print season_yr_dict

	file3 = open(f3,'r') 
	data3 = file3.readlines()[1:]
	file3.close()

	matcid_year = defaultdict(list); matcid_team_result = defaultdict(list)

	for line in data3 :  
		line = line.strip().split('|')
		matcid = line[0]
		years = line[1]
		try :
			#print line[0], line[4], line[9]
			if int(line[4]) > int(line[9]) :
				matcid_team_result[str(line[3])+'|'+str(matcid)] = "W"
				matcid_team_result[str(line[7])+'|'+str(matcid)] = "L"

			if int(line[4]) == int(line[9]) :
				matcid_team_result[str(line[3])+'|'+str(matcid)] = "D"
				matcid_team_result[str(line[7])+'|'+str(matcid)] = "D"
 
			if int(line[4]) < int(line[9]) :
				matcid_team_result[str(line[3])+'|'+str(matcid)] = "W"
				matcid_team_result[str(line[7])+'|'+str(matcid)] = "L"

		except ValueError,e :
			continue
		matcid_year[int(matcid)] = int(years)


	#file2 = open('../Data/nba_matchid_playerid_playernames.txt','r') ## form relationship  !!!
	
	file4 = open(f4,'r') ## form relationship  !!!
	data4 = file4.readlines()
	file4.close()

	team_nodes = defaultdict(list)

	team_home_away = defaultdict(list)

	for line in data4 :
		line = line.strip()
		line = line.split()
		try :
			season = matchid_season_year[str(line[0])].split('|')[0]

			try :

				if str(season) == str(season_str) :

					team_nodes[str(line[3].lower())+'|'+str(line[0])].append(str(line[1].lower().encode('ascii', 'ignore'))) ### EPL

			except TypeError,e :
				continue

		except AttributeError,e :
			continue


	players_pair = defaultdict(list)

	for k in team_nodes :
		nodes = list(set(team_nodes[k]))

		for n in nodes :
			players_pair[str(n)+'|'+k.split('|')[1]] = str(n)+'|'+k.split('|')[0]+'|'+k.split('|')[1]

	sorted(players_pair.iterkeys())

 ## now look back and see how many times players played with each other earlier !

	team_combos = []; 	team_nodes_past = defaultdict(list)
	
	season_mindate = datetime.strptime(season_min_max_dict[str(season_str)].split('|')[0].split(' ')[0], format)
	season_maxdate = datetime.strptime(season_min_max_dict[str(season_str)].split('|')[1].split(' ')[0], format)

	## construct the season bin ###
	#s1 = season_str.split('-')[0]; s2 = season_str.split('-')[1]

	#season_bin = str(int(s1)-int(bin1))+'-'+c2str(str(int(s2)-int(bin1)))
	
	#print season_bin

	#season_bin_mindate = datetime.strptime(season_min_max_dict[str(season_bin)].split('|')[0].split(' ')[0], format)
	#season_bin_maxdate = datetime.strptime(season_min_max_dict[str(season_bin)].split('|')[1].split(' ')[0], format)

	file5 = open(f5,'r') 
	data5 = file5.readlines()[1:]
	file5.close()

	for line in data5:
		
		line = line.strip()
		line = line.split('|')
		#year = matcid_year[int(line[0])]
		#seasonyr = str(season_str).split('-')[0]

		matchid = line[6].split('=')[1]
		playerid = '__'.join(line[0].split('__')[:-1]).replace('-','_')
		#print str(line[3]), datetime.strptime(str(line[3]), format1)
		try :
		
			try:
				try :
					dates = datetime.strptime(str(line[3]), format1)
					
					if dates < season_mindate :
					#if dates >= season_bin_mindate and dates < season_mindate :

						#if matcid_team_result[str(line[2].lower())+'|'+str(line[0])] == "W" :
						team_nodes_past[str(line[1].lower())+'|'+str(matchid)].append(str(playerid.encode('ascii', 'ignore'))) 

				except IndexError,e :
					continue
			except ValueError,e :
				continue
		
		except AttributeError,e :
			continue

	#print team_nodes_past
	team_nodes_past_uniq = defaultdict(list)
	for k in team_nodes_past :
		nodes2 = list(set(team_nodes_past[k]))
		edges2 = combinations(nodes2, 2)
		G2 = nx.Graph()
		G2.add_nodes_from(nodes2)
		G2.add_edges_from(edges2) 
		for u,v in G2.edges() :
			if u != v :
				team_combos.append(( str(u)+'|'+str(v) ))

	team_combos2 = defaultdict(list)

	for k, v in countDuplicatesInList(team_combos) :
		team_combos2[k] = int(v) 

	sorted(team_combos2.iterkeys())
	team_result = defaultdict(list)

	for line in data3 :
		line = line.strip()
		line = line.split('|')

		season = matchid_season_year[str(line[0])].split('|')[0]

		if str(season) == str(season_str) :

				team1 = line[3]; team1id = line[2]; score_t1 = line[4]
				team2 = line[7]; team2id = line[6]; score_t2 = line[9]

				keys1 = str(team1)+'|'+str(line[0]); keys2 = str(team2)+'|'+str(line[0])

				listbothteams = list(set(team_nodes[keys1])) + list(set(team_nodes[keys2]))

				for vals in listbothteams :
					team_result[str(line[0])].append(players_pair[str(vals)+'|'+str(line[0])])

	players_opponent_teams = defaultdict(list)

	for k in team_result :

		nodesk = team_result[k]
		edges3 = combinations(nodesk,2)

		for u, v in edges3 :
			if u.split('|')[1] != v.split('|')[1] :
				if str(u.split('|')[0])+'|'+str(v.split('|')[0]) in team_combos2 or str(v.split('|')[0])+'|'+str(u.split('|')[0]) in team_combos2 :

					players_opponent_teams[u.split('|')[1]+'|'+u.split('|')[2]].append(u.split('|')[0])
		
					players_opponent_teams[v.split('|')[1]+'|'+v.split('|')[2]].append(v.split('|')[0])


	common_players = defaultdict(list)


	for k in players_opponent_teams :
		common_players[k] = len(list(set(players_opponent_teams[k])))

	fh6 = open(destdir+'EPL_ecosystem_per_season_'+str(season_str)+'.txt', 'w')
	print >> fh6, 'MatchID|Team1ID|Team1|score_t1|ecosys_t1|HAteam01|Team2ID|Team2|score_t2|ecosys_t2|HAteam02'
	

	for line in data3 :
		line = line.strip()
		line = line.split('|')

		#try :
		season = matchid_season_year[str(line[0])].split('|')[0]

		if str(season) == str(season_str) :

				team1 = line[3]; team1id = line[2]; score_t1 = line[4]
				team2 = line[7]; team2id = line[6]; score_t2 = line[9]

				keys1 = str(team1)+'|'+str(line[0]); keys2 = str(team2)+'|'+str(line[0])

				t1_home_away = line[5]; t2_home_away = line[8]

				if not keys1 in common_players:
					common_players[keys1] = 0

				if not keys2 in common_players:
					common_players[keys2] = 0

				print >> fh6, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (line[0], team1id, team1, score_t1, common_players[keys1], t1_home_away, team2id, team2, score_t2, common_players[keys2], t2_home_away )

		#except AttributeError, e :
		#	continue



if __name__ == '__main__':

	f1 = sys.argv[1]; f2 = sys.argv[2]; f3 = sys.argv[3]; f4 = sys.argv[4]; f5 = sys.argv[5]; f6 = sys.argv[6]; #f7 = sys.argv[7]; #f8 = sys.argv[8]; f9 = sys.argv[9]

	#gen_compositional_mlb_variables(f1, f2, f3, f4, f5, f6, f7)
	#gen_compositional_EPL_variables(f1, f2, f3, f4, f5)
	#gen_compositional_NBA_variables(f1, f2, f3, f4, f5, f6, f7)
	#gen_compositional_IPL_variables(f1, f2, f3, f4)

	#create_relational_variable_IPL(f1, f2, f3)
	#create_relational_variable_NBA(f1, f2, f3, f4, f5)
	#create_relational_variable_MLB(f1, f2, f3, f4, f5)
	#create_relational_variable_EPL(f1, f2, f3, f4, f5)

	########### EPL Seasons ###############
	#gen_compositional_EPL_variables_season(f1, f2, f3, f4, f5, f6, f7)
	#create_relational_variable_EPL_season(f1, f2, f3, f4, f5)
	create_ecosystem_variable_EPL_season(f1, f2, f3, f4, f5, f6)

	########## MLB infield ################
	#create_relational_variable_infield_MLB(f1, f2, f3, f4, f5, f6)






