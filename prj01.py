import sys

def Usertxt(rbtree):
    i = 0
    totalUser = 0
    with open("user.txt") as f:
        for line in f:
            i += 1
            if i % 4 == 1:
                txt = line.strip()
                rbtree.insert_key(txt)
                totalUser +=1
    return totalUser

def Friendtxt(rbtree):
    i = 0
    totalFriendship = 0
    tmp = ""
    with open("friend.txt") as f:
        for line in f:
            i += 1
            txt = line.strip()
            
            if i % 3 == 1:
                tmp = txt
                
            elif i % 3 == 2:
                userNode = rbtree.search(tmp)
                if userNode is not rbtree.nil:
                    userNode.userData.append(txt)
                userNode1 = rbtree.search(txt)
                if userNode1 is not rbtree.nil: # 위 아래 모두 친구 관계에 추가하기 위한 코
                    userNode1.userData.append(tmp)
                totalFriendship += 1
                
    return totalFriendship
                    
                
def Wordtxt(rbtree, userTree):
    i = 0
    totalTweet = 0
    tmp = ""
    with open("word.txt") as f:
        for line in f:
            i += 1
            
            if i % 4 == 1:
                txt = line.strip()
                tmp = txt
                
            elif i % 4 == 3:
                txt = line.strip()
                rbtree.insert_key(txt)
                totalTweet += 1
                
                userNode = userTree.search(tmp) # user count
                if userNode != userTree.nil:
                    userNode.cnt = userNode.cnt + 1
                    
                textNode = rbtree.search(txt) # tweet count
                if textNode != rbtree.nil:
                    textNode.cnt = textNode.cnt + 1
                    if tmp not in textNode.userData:
                        textNode.userData.append(tmp)
    return totalTweet

def statistics(rbtree, userTree, userTreeRoot):
    userNode = userTreeRoot
    if userNode != userTree.nil:
        statistics(rbtree, userTree, userTreeRoot.left)
        
        key = userNode.key
        count = userNode.cnt
    
        rbtree.insert_key(count, key)
        
        statistics(rbtree, userTree, userTreeRoot.right)

def statistics1(rbtree, userTree, userTreeRoot):
    userNode = userTreeRoot
    if userNode != userTree.nil:
        statistics1(rbtree, userTree, userTreeRoot.left)

        key = userNode.key
        udlen = userNode.userDataLen
        
        rbtree.insert_key(udlen, key)

        statistics1(rbtree, userTree, userTreeRoot.right)

class rbnode(object):
    def __init__(self, key, data = ""):
        self._key = key
        self._red = False
        self._left = None
        self._right = None
        self._p = None
        self.cnt = 0
        self.userData = []
        self.data = data

    key = property(fget=lambda self: self._key)
    red = property(fget=lambda self: self._red)
    left = property(fget=lambda self: self._left)
    right = property(fget=lambda self: self._right)
    p = property(fget=lambda self: self._p)
    userDataLen = property(fget=lambda self: len(self.userData))

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return str(self.key)
 
class rbtree(object):
    def __init__(self, create_node=rbnode):
        self._nil = create_node(key=None)
        self._root = self.nil
        self._create_node = create_node

    root = property(fget=lambda self: self._root)
    nil = property(fget=lambda self: self._nil)

    def search(self, key, x=None):
        if None == x:
            x = self.root
        while x != self.nil and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x


    def minimum(self, x=None):
        if None == x:
            x = self.root
        while x.left != self.nil:
            x = x.left
        return x


    def maximum(self, x=None):
        if None == x:
            x = self.root
        while x.right != self.nil:
            x = x.right
        return x

    def insert_key(self, key, data = ""):
        self.insert_node(self._create_node(key=key, data=data))

    def insert_node(self, z):
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z._p = y
        if y == self.nil:
            self._root = z
        elif z.key < y.key:
            y._left = z
        else:
            y._right = z
        z._left = self.nil
        z._right = self.nil
        z._red = True
        self._insert_fixup(z)
        
    def _insert_fixup(self, z):
        while z.p.red:
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self._left_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self._right_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._left_rotate(z.p.p)
        self.root._red = False

    def _transplant(self, u, v):
        if u.p == self.nil:
            self._root = v
        elif u == u.p.left:
            u.p._left = v
        else:
            u.p._right = v
        v._p = u.p

    def delete_node(self, z):
        y = z
        if y.red:
            y_original_red = True
        else:
            y_original_red = False
            
        if z.left == self.nil:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            if y.red:
                y_original_red = True
            else:
                y_original_red = False
            x = y.right
            if y.p == z:
                x._p = y
            else:
                self._transplant(y, y.right)
                y._right = z.right
                y.right._p = y
            self._transplant(z, y)
            y._left = z.left
            y.left._p = y
            if y.red:
                z._red = True
            else:
                z._red = False

        if y_original_red == False:
            self._delete_fixup(x)

    def _delete_fixup(self, x):
        while x != self.root and x.red == False:
            if x == x.p.left:
                w = x.p.right
                if w.red:
                    w._red = False
                    w.p._red = True
                    self._left_rotate(x.p)
                    w = x.p.right
                if w.left.red == False and w.right.red == False:
                    w._red = True
                    x = x.p
                else:
                    if w.right.red == False:
                        w.left._red = False
                        w._red = True
                        self._right_rotate(w)
                        w = x.p.right
                    if x.p.red:
                        w._red = True
                    else:
                        w._red = False
                    x.p._red = False
                    w.right._red = False
                    self._left_rotate(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.red:
                    w._red = False
                    w.p._red = True
                    self._right_rotate(x.p)
                    w = x.p.left
                if w.right.red == False and w.left.red == False:
                    w._red = True
                    x = x.p
                else:
                    if w.left.red == False:
                        w.right._red = False
                        w._red = True
                        self._left_rotate(w)
                        w = x.p.left
                    if x.p.red:
                        w._red = True
                    else:
                        w._red = False
                    x.p._red = False
                    w.left._red = False
                    self._right_rotate(x.p)
                    x = self.root
        x._red = False
                    

    def _left_rotate(self, x):
        y = x.right
        x._right = y.left
        if y.left != self.nil:
            y.left._p = x
        y._p = x.p
        if x.p == self.nil:
            self._root = y
        elif x == x.p.left:
            x.p._left = y
        else:
            x.p._right = y
        y._left = x
        x._p = y


    def _right_rotate(self, y):
        x = y.left
        y._left = x.right
        if x.right != self.nil:
            x.right._p = y
        x._p = y.p
        if y.p == self.nil:
            self._root = x
        elif y == y.p.right:
            y.p._right = x
        else:
            y.p._left = x
        x._right = y
        y._p = x

    def _predecessor(self, x):
        if x == self.nil:
            return self.nil
        if x.left != self.nil:
            return self.maximum(x.left)
        y = x.p
        while y != self.nil and x == y.left:
            x = y
            y = y.p
            if y == None:
                return self.nil
        return y

    def _successor(self, x):
        if x == self.nil:
            return self.nil
        if x.right != self.nil:
            return self.minimum(x.right)
        y = x.p
        while y != self.nil and x == y.right:
            x = y
            y = y.p
            if y == None:
                return self.nil
        return y

    def topFive(self):
        toplist = []
        top1 = self.maximum()
        top2 = self._predecessor(top1)
        top3 = self._predecessor(top2)
        top4 = self._predecessor(top3)
        top5 = self._predecessor(top4)

        if top1 != self.nil:
            toplist.append(top1)
            if top2 != self.nil:
                toplist.append(top2)
                if top3 != self.nil:
                    toplist.append(top3)
                    if top4 != self.nil:
                        toplist.append(top4)
                        if top5 != self.nil:
                            toplist.append(top5)

        return toplist

    def check_invariants(self): 
        
        def is_red_black_node(node):
            if (node.left and not node.right) or (node.right and not node.left):
                return 0, False

            if not node.left and not node.right and node.red:
                return 0, False

            if node.red and node.left and node.right:
                if node.left.red or node.right.red:
                    return 0, False

            if node.left and node.right:

                if self.nil != node.left and node != node.left.p:
                    return 0, False
                if self.nil != node.right and node != node.right.p:
                    return 0, False

                left_counts, left_ok = is_red_black_node(node.left)
                if not left_ok:
                    return 0, False
                right_counts, right_ok = is_red_black_node(node.right)
                if not right_ok:
                    return 0, False

                if left_counts != right_counts:
                    return 0, False
                return left_counts, True
            else:
                return 0, True

        num_black, is_ok = is_red_black_node(self.root)
        return is_ok and not self.root._red
              
def main():
    
    while 1: #Interface
        print("\n0. Read data files")
        print("1. display statistics")
        print("2. Top 5 most tweeted words")
        print("3. Top 5 most tweeted users")
        print("4. Find users who tweeted a word (e.g., '연세대')")
        print("5. Find all people who are friends of the above users")
        print("6. Delete all mentions of a word")
        print("7. Delete all users who mentioned a word")
        print("8. Find strongly connected components")
        print("9. Find shortest path from a given user")
        print("99. Quit")
        print("Select Menu: ", end = "")
        menu = input()
            
        if menu == "0": #Read data files
            userTree = rbtree() #user
            wordTree = rbtree() #word
            top5Tree = rbtree() #for menu 2
            tweetTree = rbtree() #tweet
            friendTree = rbtree() #friend
            
            totalUser = Usertxt(userTree)
            totalTweet = Wordtxt(wordTree, userTree)
            totalFriendship = Friendtxt(userTree)
            statistics(top5Tree, wordTree, wordTree.root)
            statistics(tweetTree, userTree, userTree.root)
            statistics1(friendTree, userTree, userTree.root)  

            print("\n")
            print("Total users: ", end = "")
            print(totalUser)
            print("Total friendship records: ", end = "")
            print(totalFriendship)
            print("Total tweets: ", end = "")
            print(totalTweet)
            
        elif menu == "1": # 평균은 totalFriendship에 2를 곱해주어야 한다.
                          # Friendtxt에서 친구관계를 한번씩만 카운트했기 때문이다
            avgFriend = totalFriendship * 2 / totalUser
            minFriend = friendTree.minimum().key
            maxFriend = friendTree.maximum().key
            
            avgTweet = totalTweet / totalUser
            minTweet = tweetTree.minimum().key
            maxTweet = tweetTree.maximum().key
            
            print("\n")
            print("Average number of friends: ", end = "")
            print(avgFriend)
            print("Minimum number of friends: ", end = "")
            print(minFriend)
            print("Maximum number of friends: ", end = "")
            print(maxFriend)
            print("\n")
            print("Average tweets per user: ", end = "")
            print(avgTweet)
            print("Minimum tweets per user: ", end = "")
            print(minTweet)
            print("Maximum tweets per user: ", end = "")
            print(maxTweet)
            
        
        elif menu == "2": #top 5 most tweeted words
            topList = top5Tree.topFive()
            print("\n")
            print("Top 5 most tweeted words")
            print(topList[0].data)
            print(topList[1].data)
            print(topList[2].data)
            print(topList[3].data)
            print(topList[4].data)
        
        elif menu == "3": #top 5 most tweeted users
            topList = tweetTree.topFive()
            print("\n")
            print("Top 5 most tweeted users")
            print(topList[0].data)
            print(topList[1].data)
            print(topList[2].data)
            print(topList[3].data)
            print(topList[4].data)
            
        elif menu == "4": #Find users who tweeted a word
            result = []
            print("\n")
            print("Enter a word: ", end = "")
            word = input()
            wordNode = wordTree.search(word)
            if wordNode == wordTree.nil:
                print("\n")
                print("No Match")
            else:
                for item in wordNode.userData:
                    print(item)
                    result.append(item)
        
        elif menu == "5": # Find all people who are friends of the above users
            print("\n")
            print("Find all people who are friends of the above users")
            print("\n")
            for item in result:
                    userNode = userTree.search(item)
                    print("")
                    print("Friends of ", end = "")
                    print(item)
                    if userNode != userTree.nil:
                        for friend in userNode.userData:
                            print(friend)
                    
        elif menu == "6": # Delete all mentions of a word
            a = 0
            print("\n")
            print("Delete all mentions of a word")
            word = input("Enter a word: ")
            wordNode = wordTree.search(word)
            if wordNode is not wordTree.nil:
                for word in wordNode.userData:
                    if wordNode is not wordTree.nil:
                        wordTree.delete_node(wordNode)
                        totalTweet -= 1
                        a += 1
                        print(wordNode)

            else:
                print("\n")
                print("No words. cannot delete")
                
            print("\n")
            print("There were ", a, end = "")
            print(" words")
            print("All of them are deleted")

        
        elif menu == "7": # Delete all users who mentioned a word
            print("")
            print("Delete all users who mentioned a word")
            word = input("Enter a word: ")
            wordNode = wordTree.search(word)
            if wordNode is not wordTree.nil:
                for user in wordNode.userData:
                    userNode = userTree.search(user)
                    if userNode is not userTree.nil:
                        userTree.delete_node(userNode)
                        totalUser -= 1
                        print("User")
                        print(userNode)
                        print("is deleted")
                        print("\n")
                        

        elif menu =="99": # Quit
            print("")
            print("Quit")
            sys.exit()
            
main()
