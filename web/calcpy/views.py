## @file calcpy/views.py
#  @brief calculation library interface to client

"""
calc library interface to client

export calculation results to client
"""
import calc

def getNumber(params):
    """the calculation from C++ library"""
    return {
        "number" : calc.getNumber()
    }

def getCommands(params):
    """return the commands descriptors"""
    cmdmgr = calc.CommandManager()
    ids = cmdmgr.getIds()
    out = dict()
    for i in ids:
        out[int(i)] = { "state" : str(cmdmgr.getState(i)), "progress": float(cmdmgr.getProgress(i)) }
    return out

def startCommand(params):
    """start new tick command"""
    cmdmgr = calc.CommandManager()
    cmd_id = cmdmgr.start()
    return cmd_id

def loginUser(params):
	print "Got name ",params["name"]," password ",params["pass"]
	return { "session-token": 10203 }

class GameStub:
	hit_counter = 0

def userMove(params):
	print "Got move request, token: ",params["token"],", (x,y): (",params["x"],params["y"],")"
	GameStub.hit_counter += 1
	return { "valid": 1, "hit": GameStub.hit_counter%2 }

def getBoards(params): # uwaga odwrocone osie (x/y)
	return { "ships": [[],[None, None, "up", "up", "down"],[],[],[],[],[],[]], "shots": [[],[],[None, "hit"],[],[],[],[],[]], "turn": False }
