class ProfileCommentData:
    
    def __init__(self,profileId,user,blog,comment,dateandtime,userimage):
        self.id=profileId
        self.user=user
        self.blog=blog
        self.comment=comment
        self.dateandtime=dateandtime
        self.userimage=userimage
        
    def __str__(self):
        return self.comment
        