import mysql.connector
connobj=mysql.connector.connect(host='localhost',user='root',passwd='Lohith22')
if connobj.is_connected():
    print("Connection established")
else:
    print("Connection not established")

def country1():
    '''Displays a list of countries for user to choose from and displays their stats.'''
    cur=connobj.cursor()
    cur.execute("use Olympics;")
    cur.execute('select DISTINCT Country from country_table;')
    print("\n\nCountries in the database:")
    data=cur.fetchall()
    for i in data:
        print(i[0])
    cname=input("Enter country to display stats\t")
    st="select * from  country_table where Country ='{}'".format(cname)
    cur.execute(st)
    data=cur.fetchall()
    for i in data:
        print("Country name:",i[1])
        print("Ranking:",i[0])
        print("Gold Medals:",i[2],end='')
        print("\tSilver Medals:",i[3],end='')
        print("\tSilver Medals:",i[4])
    cur.close()

def sport_based2():
    '''Displays a list of sports for user to choose from and displays the names of the players, country and ranking.'''
    cur=connobj.cursor()
    cur.execute("use Olympics;")
    cur.execute('select DISTINCT Sport from player_table;')
    print("\n\nSports present in the database:")
    data=cur.fetchall()
    for i in data:
        print(i[0])
    cname=input("Enter a sport from above to display winners:\t")
    st="select * from  player_table where Sport ='{}' order by Ranking".format(cname)
    cur.execute(st)
    data=cur.fetchall()
    for i in data:
        print("Player name:",i[2])
        print("Sport:",i[4])
        print("Country:",i[3])
        print("Ranking:",i[0])
        print("\n\n")
    cur.close()



def leaderboard3():
    '''Takes user input sports and the medal won and displays the name of the player who won the medal for particular sport .'''
    cur=connobj.cursor()
    cur.execute("use Olympics;")
    cur.execute('select DISTINCT Sport from player_table;')
    data=cur.fetchall()
    for i in data:
        print(i[0])
    x=input("Choose a sport from above:") 
    y=input("Enter The medal won (Gold, Silver, Bronze):")
    st="SELECT Player_name FROM Player_table WHERE Sport ='{0}' AND Medal='{1}'".format(x,y) 
    cur.execute(st) 
    data=cur.fetchall()
    print("The name of the player is:\n")
    for row in data:
        print('Player Name:', row[0])
    cur.close()

def country_based4():
    '''Takes user input on country name and displays winners from the country.'''
    cur=connobj.cursor()
    cur.execute("use Olympics;")
    cname=input("Enter country name to display winners from the country\t")
    st="select Player_name,Country,Sport from player_table where Country='{}'".format(cname)
    cur.execute(st)
    data=cur.fetchall()
    for i in data:
        print("\nCountry name:",i[1])
        print("Player name:",i[0])
        print("Sport:",i[2])
    cur.close()

def TOP_WINNERS5():
    '''Displays top five winners of Olympics 2020.'''
    cur=connobj.cursor()
    cur.execute("use Olympics;")
    print("Top five winners of the Olympics:")
    cur.execute('select * from Country_table where Ranking BETWEEN 1 and 5 order by ranking;')
    data=cur.fetchall()
    for i in data:
        print("\nRanking:",i[0])
        print("Country name:",i[1])
    cur.close()

def team_search6():
    '''Searches if a team is taking part in Olympics'''
    cur=connobj.cursor()
    cur.execute("use Olympics;")
    cname=input("Enter team name")
    str="select * from Country_table where Country='{}'".format(cname)
    cur.execute(str)
    data=cur.fetchall()
    if data==[]:
        print(cname,"not found in participating list")
    else:
        print(cname,"is participating!")
    cur.close()

def mostgold7():
    '''Displays the gold medalist with player name, sport and nationality.'''
    cur=connobj.cursor()
    cur.execute("use Olympics;")
    cur.execute("select Player_name,Country,Sport from Player_table where Medal='Gold' ;")
    print("Details of gold medalists:")
    data=cur.fetchall()
    for i in data:
        print("\nName:",i[0])
        print("Nationality:",i[1])
        print("Sport:",i[2])
    cur.close()

def gold8():
    '''Displays the number of gold medal of each country'''
    cur=connobj.cursor()
    cur.execute("use Olympics;")
    cur.execute('select country,Gold_Medal from country_table order by Gold_Medal desc;')
    data=cur.fetchall()
    count=cur.rowcount
    print("Number of gold medals from each country:") 
    for row1 in data:
        print("\n\nCountry name:",row1[0],"\nNumber of gold medals:",row1[1],)
    cur.close()

def dispcountry9():
    cur=connobj.cursor()
    cur.execute("use Olympics;")
    cur.execute("select * from Country_table order by Ranking;")
    rec=cur.fetchall()
    for i in rec:
        print("\nRanking:",i[0])
        print("Country:",i[1])
        print("Gold Medal:",i[2])
        print("Silver Medal:",i[3])
        print("Bronze Medal:",i[4])
    cur.close()

def dispplayer10():
    cur=connobj.cursor()
    cur.execute("use Olympics;")
    cur.execute("select * from Player_table order by Sno;")
    rec=cur.fetchall()
    for i in rec:
        print("\nRanking:",i[1])
        print("Player name:",i[2])
        print("Country:",i[3])
        print("Sport:",i[4])
        print("Medal:",i[5])
    cur.close()
    
ans='n'
while ans=='n' or ans=='N':
    print("\t\t\t\t-------WELCOME TO FLAME TORCH╰*°▽°*╯-------\n")
    print("1.Display stats Country wise\t\t\t\t\t",end='')
    print("2.Display winners of a sport")
    print("3.Display name of the player who won medal for a sport\t\t",end='')
    print("4.Display winners of a country")
    print("5.Display top 5 winners in Tokyo Olympics\t\t\t",end='')
    print("6.Search participation of entered team")
    print("7.Display details of gold medalist\t\t\t\t",end='')
    print("8.Display number of gold medals for each country")
    print("9.Display Country tablet\t\t\t\t\t",end='')
    print("10.Display Player table")
    
    
    choice=int(input("\n->Which of the above function to execute?"))
    if choice==1:
        country1()
    elif choice==2:
        sport_based2()
    elif choice==3:
        leaderboard3()
    elif choice==4:
        country_based4()
    elif choice==5:
        TOP_WINNERS5()
    elif choice==6:
        team_search6()
    elif choice==7:
        mostgold7()
    elif choice==8:
        gold8()
    elif choice==9:
        dispcountry9()
    elif choice==10:
        dispplayer10()
    ans=input("\nDo you wish to exit?(y/n)")

