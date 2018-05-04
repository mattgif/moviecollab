# moviecollab
http://moviecollab.com 

moviecollab is a django-backed webapp that allows users to easily find information about who has worked together on film and television projects, and what actors/crew different projects have in common. 

## Why?

Suppose you're a fan of both Ridley Scott and Sigourney Weaver, and want to know if they've worked on anything together besides 'Alien' (1979). You search for both names, and discover they've also collaborated on '1492: Conquest of Paradise' (1992) and 'Exodus: Gods and Kings' (2014). 

Or suppose you can't remember the name of the guy who was in both 'Deadwood' and 'Justified'. Search for both to be reminded that it's Timothy Olyphant. 

Future updates will provide deeper analytics, including finding frequent collaborators, and projects with signtificant overlap.

## How?

Data: Currently, moviecollab pulls JSON data directly from the Movie Database (TMDB), who very generously provide a free API. (This product uses the TMDb API but is not endorsed or certified by TMDb.)

Code: Backend is python/django. Front end is the usual suspects, using the wonderful select2 plugin for search, and boostrap 3 for layout.
