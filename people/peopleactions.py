import json
import requests
from random import randint
import secrets

api_key = secrets.my_api_key()

class Person():
    """
    This is a class representing a person. People have TMDb IDs, names, images,
    and projects they've been in.
    """
    def __init__(self,JSON_DATA):
        self.data = JSON_DATA
        self.id = int(self.data['id'])
        self.name = self.data['name']
        self.combined_credits = self.data['combined_credits']

        # list of all person's credits. used for quickly finding collaborators.
        self.credit_id_list = list(set([c['id'] for r in ['cast','crew'] for c in self.combined_credits[r]]))
        self.image = self.image_url('lg')

        # dictionary of projects that Person has been in, containing their character's name (if cast) or job title (if crew),
        # the project's title, the project's media type
        self.credit_details = self.get_credit_details()

    def image_url(self,size):
        """
        If profile image is found, returns url as string. Otherwise, returns default profile.
        """

        image = self.data['profile_path']

        if size == 'sm':
            size = 'w45'
        elif size == 'md':
            size = 'w185'
        else:
            size = 'h632'

        try:
            return "https://image.tmdb.org/t/p/" + size + image

        except:
            return "/static/images/missing_profile.png"

    def get_credit_details(self):
        """
        Returns a dictionary of credit information (project title, project media type, person's roles (job title/ character)) for all projects in
        credit list. Structure:
        {
        id# :
            {
            'media_type':'',
            'role':['cast role','crew role'],
            'title':''},
            'poster_path':'',
            'year':'',
         id# :
            ...
        }
        """
        dic = {}

        # helper function to fill in media_type and title
        def fill_basic(id, credit):
            dic[id] = {'media_type' : credit['media_type']}
            try:
                dic[id]['poster_path'] = credit['poster_path']
            except:
                dic[id]['poster_path'] = 0
            if dic[id]['media_type'] == 'movie':
                dic[id]['title'] = credit['original_title']
                try:
                    dic[id]['year'] = credit['release_date'][:4]
                except:
                    dic[id]['year'] = '0'
            else:
                dic[id]['title'] = credit['original_name']
                try:
                    dic[id]['year'] = credit['first_air_date'][:4]
                except:
                    dic[id]['year'] = '0'

        # creates dic entries for pertinant CAST data
        cast_info = self.combined_credits['cast']
        for c in cast_info:
            id = int(c['id'])
            fill_basic(id,c)
            dic[id]['roles'] = [c['character']]

        # creates entries for crew info - if cast info already present, just appends job title to roles list
        crew_info = self.combined_credits['crew']
        for c in crew_info:
            id = int(c['id'])
            if id not in dic:
                fill_basic(id,c)
                dic[id]['roles'] = [c['job']]
            else:
                dic[id]['roles'].append(c['job'])

        return dic

    def random_backdrop(self):
        """
        Returns a url for an image tagged with this person's name.
        """
        if not self.checked_for_backdrops:
            self.backdrop_paths = self.get_backdrops()

        if len(self.backdrop_paths) == 0:
            return '/static/images/backdrops/holes.jpg'
        else:
            return "https://image.tmdb.org/t/p/w1280" + self.backdrop_paths[randint(0,(len(self.backdrop_paths)-1))]

    def get_backdrops(self):
        """
        Returns a list of wide images tagged with this person.
        """
        # tagged images is not currently supported by tmdbsimple, so we need to grab the json file
        request_url = "https://api.themoviedb.org/3/person/" + str(self.id) + "/tagged_images?api_key=" + api_key
        response = requests.get(request_url)
        self.checked_for_backdrops = True
        if response.status_code == 404:
            return []
        else:
            json_dic = response.json()['results']
            return [entry['file_path'] for entry in json_dic if 1900 < entry['height'] < entry['width']]

class Project():
    """
    This is a class representing movies/tv shows. They have TMDb IDs, titles, posters, backdrops, popularity score, release years, cast, and crew.
    Requires TMDb ID and MEDIA_TYPE as arguments. POSTER_PATH and TITLE are optional.
    """

    def __init__(self,ID,MEDIA_TYPE,POSTER_FILE_NAME=0,TITLE=0,YEAR='0'):
        self.id = int(ID)
        self.media_type = MEDIA_TYPE
        self.poster_file_name = POSTER_FILE_NAME
        self.link = "/movies/?q=" + str(self.id) + "," + self.media_type
        self.title = TITLE
        self.tmdb_data = 0
        self.popularity = 0
        self.poster = self.poster_url('sm')
        self.year = YEAR

    def poster_url(self,size):
        if self.poster_file_name == 0:
            return "/static/images/missing_poster.png"

        if size == 'sm':
            size = 'w92'
        elif size == 'md':
            size = 'w185'
        elif size == 'lg':
            size == 'w342'
        else:
            size == 'w780'
        try:
            return "https://image.tmdb.org/t/p/" + size + self.poster_file_name
        except:
            return "/static/images/missing_poster.png"

def find_common_projects(person1,person2):
    """
    Takes two Person objects, and returns a list of tuples,
    with each tuple containing a Project object for projects they've both worked on,
    the hero's role[s] in that project, and the collaborator's roles.
    The list is sorted by year of project release/first air date, with newest first.
    """
    common_project_id_list = []
    common_projects = []

    # Generates list of project ids common to both people
    for project in person1.credit_id_list:
        if project in person2.credit_id_list:
            common_project_id_list.append(project)

    # Removees duplicates
    common_project_id_list = list(set(common_project_id_list))

    # Creates a project obj for each item on list, and appends a tuple containing that obj plus each persons role[s] in that project to the list we'll be returning
    for pj_id in common_project_id_list:
        p1role = person1.credit_details[pj_id]['roles']
        p2role = person2.credit_details[pj_id]['roles']
        # conditional prevents talk shows / award shows on which they were guests from appearing
        if p1role[0] != '' and p2role[0] != '' and pj_id != 27023:
            pj_obj = Project(pj_id,person1.credit_details[pj_id]['media_type'], YEAR=person1.credit_details[pj_id]['year'], POSTER_FILE_NAME=person1.credit_details[pj_id]['poster_path'], TITLE=person1.credit_details[pj_id]['title'])
            common_projects.append((pj_obj, p1role, p2role))

    # sorts the list by the project's year attribute (release date for movies, original air date for tv)
    common_projects.sort(key=lambda project: project[0].year, reverse=True)

    return common_projects
