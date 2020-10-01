## PREPROCESSING DATA

f  = open("database.pgn", 'r') # Entrer ici le chemin de votre base de données

gcsv = open("games.csv", 'w')
gcsv.write("id,white,white_ELO,black,black_ELO,opening,result,length,time\n")

# player[i] == [String playerID, list playerElo_t]
player = []

openings = []

count = 0

# while l!='' :
for i in range(16000) :
    if i%1000 == 0 :
        print ("partie numero : ",i)
    
    ### READING
    
    # we're not intrested in the two first lines
    f.readline()
    f.readline()
    
    # white player
    wp = f.readline().split(sep='"')[1]
    
    # black player
    bp = f.readline().split(sep='"')[1]
    
    # result
    res = f.readline().split(sep='"')[1]
    
    # time
    date = f.readline().split(sep='"')[1].split('.')[2]
    if date == "31" :
        date = "0"
    min = f.readline().split(sep='"')[1].split(':')
    min = min[0] + min[1]
    time = date + min
    
    # players Elo
    welo = f.readline().split(sep='"')[1]
    belo = f.readline().split(sep='"')[1]
    
    # lines not important to us
    terminaison = ""
    iterat = "ignore me"
    while iterat != '\n' :
    	terminaison = iterat
    	iterat = f.readline()
    terminaison = terminaison.split('"')[1]
        
    
    # game detail, we only need the first move and the number of moves
    game = f.readline().split(sep='.')
    numoves = len(game) - 1
    
    ## WRITING
    if terminaison == "Normal" and numoves > 2 and game[1][1:-2][-1]!='l':
    	count += 1
    	firstmove = game[1].split(sep=" ")[1] + " " + game[2][1:-2].split(sep=" ")[0] 
    	if firstmove not in openings :
    		openings.append(firstmove)
    	
    	# find wp and bp in players list
    	windex = -1
    	bindex = -1
    	for j in range(len(player)) :
    	    if player[j][0] == wp :
    	        windex = j
    	    elif player[j][0] == bp :
    	        bindex = j
    	if windex == -1 :
    	    windex = len(player)
    	    player.append([wp,[]])
    	if bindex == -1 :
    	    bindex = len(player)
    	    player.append([bp,[]])
    	
    	# Players elo
    	if welo=="?" : welo='0'
    	player[windex][1].append(welo)
    	if belo=="?" : belo='0'
    	player[bindex][1].append(belo)
    	
        # write in gcsv
    	gcsv.write("0" +str(i) + "," + wp + "," + welo + "," + bp + "," + belo + "," + firstmove + "," + res + "," + str(numoves) + "," + time + "\n")
    # go to next game
    if f.readline() == '' :
        break

f.close()
gcsv.close()



pcsv = open("players.csv", 'w')
pcsv.write("id,games_number,initial_ELO,final_ELO,delta_ELO\n")
for p in player :
    delta = str(int(p[1][-1]) - int(p[1][0]))
    pcsv.write(p[0] + "," + str(len(p[1])) + "," + p[1][0] + "," + p[1][-1] + "," + delta + "\n")
pcsv.close()

ocsv = open("openings.csv", 'w')
ocsv.write("first,second\n")
for o in openings :
	ocsv.write(o.split(sep=" ")[0] + "," + o + "\n")

print("number of openings : ",len(openings))
print("number of games    : ",count)
print("number of players  : ",len(player))

