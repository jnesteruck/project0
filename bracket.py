from abc import ABC, abstractmethod
from competitor import Team, IndividualCasual, IndividualPro

class Matchup:
    def __init__(self, idx, tm1, tm2):
        self._idx = idx
        self._tm1 = tm1
        self._tm2 = tm2

    def getTeam1(self):
        return self._tm1

    def getTeam2(self):
        return self._tm2

class Bracket:
    def __init__(self, participants, name=""):
        self._name = str(name)
        try:
            if len(participants) <= 16:
                self._participants = list(participants)
            else:
                raise Exception
        except Exception as e:
            print("Could not set size. Too many participants. Maximum participants is 16.")
        size = len(participants)
        for i in range(5):
            if size <= 2 ** i:
                self._size = 2 ** i
                break
        self._matchups = self.matchupMaker()
            
    
    # setters
    def setName(self, name):
        self._name = str(name)
    
    def setParticipants(self, participants):
        self._style = list(participants)
        size = len(participants)
        for i in range(5):
            try:
                if size <= 2 ** i:
                    self._size = 2 ** i
                else:
                    raise Exception
            except Exception as e:
                print("Could not set size. Too many participants. Maximum participants is 16.")
            else:
                break
    
    # getters
    def getName(self) -> int:
        return self._name
    
    def getSize(self) -> int:
        return self._size
    
    def getParticipants(self) -> list:
        return self._participants

    def getMatchups(self) -> list:
        return self._matchups

    def printTeams(self):
        '''
        printTeams

        This function prints the first round matchups.

        Returns None.

        '''
        for elem in self._matchups:
            tm2_s = ""
            if elem._tm2.getSeed() == 0:
                tm2_s = "(First Round Bye)"
            else:
                tm2_s = "vs. (" + str(elem._tm2.getSeed()) + ") " + elem._tm2.getName()
            print("(" + str(elem._tm1.getSeed()) + ")", elem._tm1.getName(), tm2_s)
    
    def matchupMaker(self) -> list:
        '''
        matchupMaker

        This function sorts the team list to make it easier to properly implement the bracketMaker method.

        Returns list of matchups.

        '''
        matches = []
        l = self._size // 2
        for i in range(l):
            match = Matchup(i, None, None)
            matches.append(match)
        if self._size == len(self._participants):
            for i in range(l): 
                match = Matchup(i, self._participants[i], self._participants[-i-1])
                matches[i] = match
        else:
            diff = self._size - len(self._participants)
            for i in range(diff):
                bye = Team("BYE","","", self._size - i)
                match = Matchup(i, self._participants[i], bye)
                matches[i] = match
            for i in range(diff, l):
                match = Matchup(i, self._participants[i], self._participants[diff-i-1])
                matches[i] = match
        return matches
    
    def sortTeams(self):
        '''
        sortTeams

        This function sorts the team list to make it easier to properly implement the bracketMaker method.

        Returns None.

        '''
        size = self._size
        if size == 4:
            pass
        else:
            temp = []
            half = len(self._matchups) // 2
            for m in self._matchups:
                temp.append(m)
            self._matchups[1] = temp[-2]
            self._matchups[-2] = temp[1]
            self._matchups[2] = temp[half]
            self._matchups[half] = temp[2]

    def __str__(self):
        sp_s = f"{' ':4}"
        sp_n = f"{' ':30}"
        sp = f"{' ':12}"
        sd = []
        sd_opp = []
        t_name = []
        t_name_opp = []
        m = self.getMatchups()
        cnt = len(m)

        for i in range(cnt):
            sd.append(f"{'(' + str(m[i]._tm1.getSeed()):>3})")
            sd_opp.append(f"{'(' + str(m[i]._tm2.getSeed()):>3})")
            t_name.append(f"\033[4m{m[i]._tm1.getName():>30} \033[0m")
            t_name_opp.append(f"\033[4m{m[i]._tm2.getName():>30} \033[0m")
        nme = " " + self.getName() + " "
        br = nme.center(100,'*') + "\n\n"
        f = lambda x : x // 2 + cnt + 1
        g = lambda x : x // 4 + int(1.5 * cnt) + 1
        h = lambda x : x // 8 + int(1.75 * cnt) + 1
        nums = set()
        nums2 = set()
        if len(m) > 2:
            nums.add(1)
            nums.add(2)
        if len(m) > 4:
            nums.add(5)
            nums.add(6)
            nums2.add(2)
            nums2.add(3)
            nums2.add(4)
            nums2.add(5)

        for i in range(cnt):
            # line 1
            t1 = sd[i] + " " + t_name[i]
            if i % 2 == 0:
                t1 += sp + "  "
            else:
                t1 += sp + " |"
            if i in nums:
                t1 += sp + "|"
            else:
                t1 += sp + " "
            if i in nums2:
                t1 += sp + "|"  
    
            # line 3
            t2 = sd_opp[i] + " " + t_name_opp[i] + "|"
            if i % 2 != 0:
                t2 += sp + " "
            else:
                t2 += sp + "|"
            if i in nums:
                t2 += sp + "|"
            else:
                t2 += sp + " "
            if i in nums2:
                t2 += sp + "|"

            # line 2
            brk_fmt = ""
            if m[i]._tm2.getName() == "BYE":
                brk_fmt = f" |\033[4m{m[i]._tm1.getName():>12}\033[0m"
            else:
                brk_fmt = f" |\033[4m{'M' + str(i+1) + ' Winner':>12}\033[0m"
            sp1 = sp_s + f"{' Match ' + str(i + 1):30}" + " " + brk_fmt
            if i % 2 == 0:
                sp1 += " "
            else:
                sp1 += "|"
            if i in nums:
                sp1 += sp + "|"
            else:
                sp1 += sp + " "
            if i in nums2:
                sp1 += sp + "|"
    
            # line 4
            sp2 = sp_s + " " + sp_n + " "
            if i % 2 == 0:
                sp2 += (' Match ' + str(f(i))).center(12) + f" |\033[4m{'M' + str(f(i)) + ' Winner':>12}\033[0m"
            elif i % 2 != 0:
                sp2 += sp + " "
            if i % 2 != 0 and i % 4 != 3:
                sp2 += (' Match ' + str(g(i))).center(12) + f" |\033[4m{'M' + str(g(i)) + ' Winner':>12}\033[0m"
            if i in nums and (i % 2 == 0 or i % 8 == 5):
                sp2 += "|"
            else:
                sp2 += " "
            if i in nums2 and i % 2 == 0:
                sp2 += sp + "|"
            if i % 8 == 3:
                sp2 += sp + (' Match ' + str(h(i))).center(12) + f" |\033[4m{'M' + str(h(i)) + ' Winner':>12}\033[0m"
            if i == cnt - 1:
                sp2 = ""
            ln = t1 + "\n" + sp1 + "\n" + t2 + "\n" + sp2
            br += ln + "\n"
        
        return br