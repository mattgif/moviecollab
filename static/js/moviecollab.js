var mcPageVars = {};
// namespace for page variables

$(document).ready(function() {
    // make initial search div appear
    var searchDisplayed = false;
    var personAction = -1;
    var projectAction = -1;
    var singleSearch = -1;
    var activeField = 0;
    function displaySearch() {
    // animates searchbox appear if it isn't already displayed
        if (searchDisplayed == false) {
            $('.initialhelp').hide();
            $('#searchdiv').slideDown();
            $('#footer').fadeIn(5000);
            searchDisplayed = true;
        }
    }

    $('.addperson').on('click',(function(){
    // "add person" button
        personAction *= -1;
        projectAction = -1;
        if (personAction == 1) {
            displaySearch();
            activeField = "person";
            $('.moviediv').css("display","none");
            $('.peoplediv').css({"display":"inherit",});
            $('#searchdiv').css({"border":"4px solid #0097cf","border-radius":"5px"});
            $('#personicon').css("color","#0097cf");
            $('#filmicon').css("color","#a7aaaf");
        } else {
            activeField = 0;
            $('#searchdiv').slideToggle();
            $('#personicon').css("color","#eee");
            $('#filmicon').css("color","#eee");
            searchDisplayed = false;
        };

    })); // end "add person button"

    $('.addmovie').on('click',(function(){
    // "add movie" button
        projectAction *= -1;
        personAction = -1;
        if ( projectAction == 1 ) {
            displaySearch();
            activeField = "movie";
            $('.peoplediv').css("display","none");
            $('.moviediv').css({"display":"inherit",});
            $('#filmicon').css("color","#60c17d");
            $('#searchdiv').css({"border":"4px solid #60c17d","border-radius":"5px"});
            $('#personicon').css("color","#a7aaaf");
        } else {
            activeField = 0;
            $('#searchdiv').slideToggle();
            $('#personicon').css("color","#eee");
            $('#filmicon').css("color","#eee");
            searchDisplayed = false;
        };

    })); // end "add movie button"

    function formatPerson (person) {
    // select2: template for people results display
        if (person.loading) return person.text;

        if (person.known_for[0]) {
            var known = person.known_for[0].title
        } else {
            var known = ""
        }

        var markup = '<div><object type="image/jpg" data="https://image.tmdb.org/t/p/w45' +
        person.profile_path +
        '"><img id="placeholder" src="/static/images/logo_placeholder.png"></object> <strong>' +
        person.name +
        "</strong> ( <em>"+
        known +
        "</em> )</div>";

        return markup;
    }

    function formatPersonSelection (person) {
    // select2: how the people results appear once selected
        return person.name;
    }

    $('.people_query').select2({
    // select2: ajax code for people
        ajax: {
            url: "https://api.themoviedb.org/3/search/person?api_key=3b6e9eed30447d42a82fa925134de4ff&language=en-US",
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    query: params.term, // search term
                };
            },
            processResults: function (data, params) {
                return {
                    // "data" is the object returned, "results" is the name of the array in the object
                    results: data.results,
                };
            },
            cache: true
        }, // ajax
        escapeMarkup: function (markup) { return markup; }, // custom formatter from Select2
        minimumInputLength: 3,
        language: {
            inputTooShort: function() {
                        return 'Search for a person...';
            }
        },
        maximumSelectionLength: 2,
        templateResult: formatPerson,
        templateSelection: formatPersonSelection,

    }); //select2 params

    function formatProject (project) {
    // select2 template for project results
        if (project.loading) return project.text;
        var mt = project.media_type
        var title;
        var date;
        if (mt != 'person') {

            if (mt == 'tv') {
                title = project.name,
                year = project.first_air_date.slice(0,4)
            } else {
                title = project.original_title,
                year = project.release_date.slice(0,4)
            };

            var markup = '<div><object type="image/jpg" data="https://image.tmdb.org/t/p/w92' +
            project.poster_path +
            '"><img id="placeholder" src="/static/images/logo_placeholder.png"></object> <strong>' +
            title +
            "</strong> ("+
            year +
            ")</div>";
        }

        return markup;
    }

    function formatProjectSelection (project) {
    // select2: how the project results appear once selected
        if (project.media_type == 'movie') {
            return project.original_title;
        } else {
            return project.name
        }

    }

    $('#hero_query').on('change', function(){
    // update button contents depending on number of items selected
        if ($('#hero_query option:selected').length == 1){
            $(this).nextAll('button').html('View filmography');
        } else if ($('#hero_query option:selected').length == 2) {
            $(this).nextAll('button').html('Find collaborations');
        }
    });

    $('#movie_query').on('change', function(){
    // update button contents depending on number of items selected
        if ($('#movie_query option:selected').length == 1){
            $(this).nextAll('button').html('View cast and crew');
        } else if ($('#movie_query option:selected').length == 2) {
            $(this).nextAll('button').html('Find collaborations');
        }
    });

    $('.movie_query').select2({
    // select2: ajax code for projects
        ajax: {
            url: "https://api.themoviedb.org/3/search/multi?api_key=3b6e9eed30447d42a82fa925134de4ff&language=en-US",
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    query: params.term, // search term
                };
            },
            processResults: function (data) {
                // "data" is the object returned, "results" is the name of the array in the object
                data = $.map(data.results, function (project) {
                // mapping needed to capture id AND media_type (which is needed to make the correct lookup on the backend)
                    project.id = project.id + "," + project.media_type;
                    return project;
                });
                return {
                    results: data,
                };
            },
            cache: true
        }, // ajax
        escapeMarkup: function (markup) { return markup; }, // custom formatter from Select2
        minimumInputLength: 3,
        language: {
            inputTooShort: function() {
                        return 'Search for a movie or tv show...';
            }
        },
        maximumSelectionLength: 2,
        templateResult: formatProject,
        templateSelection: formatProjectSelection,

    }); //select2 params

    function creditTemplate(loc, data) {
    // foldout format cast & crew results. takes in a location to update, and the json obj
        var crew = data.crew
        var cast = data.cast
        if (mcPageVars['pageType'] == 'people') {
            var url;
            if (mcPageVars['pageView'] == 'single') {
                url = "/people/?q=" + mcPageVars['heroID'] + "&q="
            } else {
                url = "/people/profile/?q="
            };
            for (var i in cast) {
                loc.find( '.cast_list' ).find( 'ul' ).append($('<li>').html("<a href=" + url + cast[i].id + "><strong>"+ cast[i].name +"</strong> </a> (as <em>" + cast[i].character + "</em>)"))
            };
            for (var i in crew) {
                loc.find( '.crew_list' ).find( 'ul' ).append($('<li>').html("<a href=" + url + crew[i].id + "><strong>" + crew[i].name +"</a></strong> (<em>" + crew[i].job + "</em>)"))
            };
        } else {
            var roleIndex = {}
            var url;
            if ( mcPageVars['pageView'] == 'single' ) {
                url = "/movies/multi/?q=" + mcPageVars['projectID'] + "," + mcPageVars['projectMT'] + "&q="
            } else {
                url = "/movies/?q="
            }
            for (var i in cast) {
                var id = cast[i]['id']
                var media_type = cast[i]['media_type']
                if (media_type == 'movie') {
                    var title = cast[i]['title'];
                    var year = cast[i]['release_date']
                    if (year != null ){
                        year = year.slice(0,4);
                    }
                } else {
                    var title = cast[i]['name'];
                    var year = cast[i]["first_air_date"]
                    if (year != null ){
                        year = year.slice(0,4);
                    }
                }

                roleIndex[id] = {'id': id.toString(), 'year': year, 'title' : title, 'media_type' : media_type, 'role' : [cast[i]['character']] }
            }
            for (var i in crew) {
                var id = crew[i]['id'];
                if (id in roleIndex) {
                    roleIndex[id]['role'].push(" " + crew[i]['job'])
                } else {
                    var media_type = crew[i]['media_type']
                    if (media_type == 'movie') {
                        var title = crew[i]['title'];
                        var year = crew[i]['release_date']
                        if (year != null ){
                            year = year.slice(0,4);
                        }
                    } else {
                        var title = crew[i]['name'];
                        var year = crew[i]["first_air_date"]
                        if (year != null ){
                            year = year.slice(0,4);
                        }
                    }
                    roleIndex[id] = {'id': id.toString(), 'title' : title, 'year' : year,  'media_type' : media_type, 'role' : [crew[i]['job']] }
                }
            }
            for (id in roleIndex) {
                var query = roleIndex[id]['id'] + "," + roleIndex[id]['media_type'];
                if (roleIndex[id]['year'] == null) {
                    roleIndex[id]['year'] = ""
                } else {
                    roleIndex[id]['year'] = "(" + roleIndex[id]['year'] + ")"
                }
                var $list = loc.find( 'ul' );
                $list.append($(
                    '<li data-year="' +
                    roleIndex[id]['year'].slice(1,5) +
                    '" >').html("<a href=" +
                    url +
                    query +
                    "><strong>" +
                    roleIndex[id]['title'] +
                    "</strong> </a> " +
                    roleIndex[id]['year'] +
                    " <em>" +
                    roleIndex[id]['role'] +
                    "</em>"));
            }
            // sort li by year attribute
            var $list = loc.find( 'ul' );
            var $listli = $list.children('li')
            $listli.sort(sort_li) // sort elements
                    .appendTo($list); // append again to the list

            function sort_li( a, b ) {
                    return $( a ).data('year') < $( b ).data('year') ? 1 : -1;
            };
        }
    };

    $( '.info_tile' ).on('click','.details',function(){
    // foldout on click functions (showing the div, ajax query)
        $(this).closest('.info_tile').toggleClass( "col-sm-4" );
        $(this).children().toggle();
        if (mcPageVars['pageType'] == 'people') {
            var [id, mediaType] = $(this).prev('.hidden_id').text().split(",");
            if ($(this).hasClass( 'loaded' )) {

            } else {
                $(this).addClass( 'loaded' );
                var details = $(this).find('.foldout');
                $.ajax({
                    type: "GET",
                    url: "https://api.themoviedb.org/3/" + mediaType + "/" + id + "/credits?api_key=3b6e9eed30447d42a82fa925134de4ff",
                    success: function(data){
                        creditTemplate(details,data)
                    },
                });
            }
        } else {
            var id = $(this).prev('.hidden_id').text();
            if ($(this).hasClass( 'loaded' )) {

            } else {
                $(this).addClass( 'loaded' );
                var details = $(this).find('.foldout');
                $.ajax({
                    type: "GET",
                    url: "https://api.themoviedb.org/3/person/" + id + "/combined_credits?api_key=3b6e9eed30447d42a82fa925134de4ff",
                    success: function(data){
                        creditTemplate(details,data)
                    },
                });
            }
        }
    });


});
