import ai, game, sys

def main():
    
    FILE = open(sys.argv[2],"w")

    FILE.write("Sequence,Score,Deducted,Hands,Discard Count\n")

    for i in range(1,int(sys.argv[1])):
        feed = ai.groups()
        testgame = game.simgame(feed)
        testgame.start()
        output = [str(i),",",str(testgame.totalscore), ",", str(testgame.nothingscore), ",",
                  testgame.handscompleted(), ",", str(len(testgame.discard)), "\n"]
        FILE.writelines(output)
        print output

    FILE.close()
    
if __name__ == '__main__': main()