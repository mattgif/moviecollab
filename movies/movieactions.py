class Project():
    """
    This is a class representing movies/tv shows. They have TMDb IDs, titles, posters, backdrops, release years, cast, and crew.
    Requires TMDb ID as argument.
    """
    def __init__(self,JSON_DATA,MEDIA_TYPE):
        self.data = JSON_DATA
        self.media_type = MEDIA_TYPE
        self.id = int(self.data['id'])
        self.title = self.get_title()

        self.image = self.image_url('md')
        self.credit_id_list = list(set([person['id'] for r in ['cast','crew'] for person in self.data['credits'][r]]))

        # dictionary of people in this project, containing their ID, portrait character's name (if cast) or job title (if crew),
        self.credit_details = self.get_credit_details()

    def get_title(self):
        try:
            self.data['title']
            self.media_type = "movie"
            return self.data['title']
        except:
            self.media_type = "tv"
            return self.data['name']

    def image_url(self,size):
        """
        If poster image is found, returns url as string. Otherwise, returns default poster.
        """

        image = self.data['poster_path']

        if size == 'sm':
            size = 'w92'
        elif size == 'md':
            size = 'w185'
        else:
            size = 'w500'
        try:
            return "https://image.tmdb.org/t/p/" + size + image
        except:
            return "/static/images/missing_poster.png"

    def get_credit_details(self):
        """
        Returns a dictionary of credit information (key = person's id; vals = person's name, person's roles (job title/ character)), person's profile_path for all people in
        credit list. Structure:
        {
        id# :
            {
            'name':'',
            'role':['cast role','crew role'],
            'profile_path':'',
         id# :
            ...
        }
        """
        dic = {}

        crew_list = self.data['credits']['crew']
        cast_list = self.data['credits']['cast']

        for person in cast_list:
            id = int(person['id'])
            dic[id] = {
            'name' : person['name'],
            'profile_path' : person['profile_path'],
            'roles' : [person['character']]
            }

        for person in crew_list:
            id = int(person['id'])
            if person['id'] in dic:
                dic[id]['roles'].append(person['job'])
            else:
                dic[id] = {
                'name' : person['name'],
                'profile_path' : person['profile_path'],
                'roles' : [person['job']]
                }

        return dic

class Person():
    """
    This is a class representing people who worked on a project. They have names, images, and role.
    """
    def __init__(self, ID, NAME, PROFILE_PATH=0, HAS_IMAGE=0):
        self.id = ID
        self.name = NAME
        self.last = self.name[self.name.rfind(" ")+1:]
        self.profile_path = PROFILE_PATH
        self.image = self.image_url('md')
        self.has_image = HAS_IMAGE
        self.link = "/people/profile/?q=" + str(self.id)        

    def image_url(self,size):
        """
        If profile image is found, returns url as string. Otherwise, returns default profile.
        """

        if self.profile_path != 0:
            image = self.profile_path

            if size == 'sm':
                size = 'w45'
            elif size == 'md':
                size = 'w185'
            else:
                size = 'h632'
            try:
                return "https://image.tmdb.org/t/p/" + size + image

            except:
                pass

        return "/static/images/missing_profile.png"

def cast_crew(*args):
    """
    Function taking n project objects as arguments, and returning a lost of tuples (obj, role_1,...,role_n) for all people
    who worked on all of the projects sorted by last name, where obj is a person object, and role are the roles they played in each.
    """
    main = args[0].credit_details
    common_ids = main
    for arg in args:
        common_ids = list ( set(common_ids) & set(arg.credit_details) )

    return_list = []
    for id in common_ids:
        person_tup = []
        try:
            person_tup.append( Person( id, main[id]['name'], PROFILE_PATH=main[id]['profile_path'] ) )
        except:
            person_tup.append( Person( id, main[id]['name'], HAS_IMAGE=1 ) )
        for arg in args:
            person_tup.append(arg.credit_details[id]['roles'])
        return_list.append( tuple(person_tup) )
    return_list.sort(key=lambda person: person[0].last)

    return return_list
