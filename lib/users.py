##############3
# It's all about the people....
# Wed 07 Sep 2016 17:24:37 AEST

class UserManager():
        OPS = list()
        OWNERS = list()
        def __init__(self, dbconn, sc):
                self.dbconn = dbconn
                self.error = 0
                self.sc = sc
        def add_owner(self, op):
                self.OWNERS.append(op)
                self.set_op(op)

        def get_owners(self):
                return self.OWNERS
        
        def set_ops(self, ops):
                for k,v in ops.items():
                        self.set_op(v['id'])

        def set_op(self, op):
                self.OPS.append(op)

        def is_op(self, id):
                return (id in self.OPS)

        def list_users(self):
                self.error = self.dbconn.query("SELECT * FROM `users`", [])
                return self.error
                    
        def update_users(self):
                users = self.dbconn.query("SELECT `userID` FROM `users`", [])
                for user in users:
                        self.update_user(user)

                return self.error

        def update_user(self, userID):
                user_info = self.sc.api_call("users.info", user=userID)
                print("Updating {0}\n".format(user_info["user"]["name"]))
                self.error = self.dbconn.query("UPDATE `users` SET `name` = %s WHERE `userID` = %s", [user_info["user"]["name"], userID,] )
                return self.error

        def check_user(self, userID):
                self.error = self.dbconn.query("SELECT `userID` FROM `users` WHERE `userID` = %s", [userID,] )
                return self.error

        # We'll get a user structure
        def check_and_add(self, user):
                
                exists = self.check_user(user["user"]["id"])

                if not exists:
                        self.error = self.dbconn.query("INSERT INTO `users`(`userID`,  `name`) VALUES(%s, %s)", [user["user"]["id"], user["user"]["name"],] )
                        print(self.error)
                return self.error       

        #def removeop(self, id):


                
