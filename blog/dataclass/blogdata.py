class BlogsData:

    def __init__(self, id,title, image, category, content, time, liked):
        self.id=id
        self.title = title
        self.image = image
        self.category = category
        self.content = content
        self.time = time
        self.liked = liked
        
    def __str__(self):
        return self.title