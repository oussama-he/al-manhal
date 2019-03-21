    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    function createProject() {
        console.log("create project is working!"); // sanity check
        $.ajax({
        url : "/projects/create-project/", // the endpoint
        type : "POST", // http method
        data : $("#o-js-project-form").serialize(), // data sent with the post request

        // handle a successful response
        success : function(json) {
            $("#o-js-project-form")[0].reset();
            console.log(">>>>>>>>><<<<<<<<<<<<<<<<<<")

        },

        // handle a non-successful response
        error : function(xhr, errmsg, err) {

        formErrors = JSON.parse(xhr.responseJSON)
        for(var key in formErrors) {
            var fieldId = "#id_" + key;
            var errorContent = formErrors[key]
            var errorMessage = errorContent[0]['message']

            var errorFeedback = $("<div class='invalid-feedback'>" + errorMessage + "</div>")
            $(fieldId).addClass("invalid is-invalid")
            $(fieldId).parent().append(errorFeedback)
        }
//            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
//                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
    };

    $("#o-js-create-project").click(function(event) {
        event.preventDefault()
        console.log('from o-js-create-project>>>>>>>>>>', $("#o-js-create-project"))
        $(".invalid-feedback").remove()
        $(".invalid").removeClass('invalid')
        createProject();
    })
