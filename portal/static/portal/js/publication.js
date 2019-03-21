$(function () {
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
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        // Send the token to same-origin, relative URLs only.
        // Send the token only if the method warrants CSRF protection
        // Using the CSRFToken value acquired earlier
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  function onDeletePublication() {
    var pub_id = $('#deleteModal').data("pub-id");
    var endpoint = "/portal/delete-publication/" + pub_id + "/"
    $.ajax({
      url: endpoint, // the endpoint
      type: "POST", // http method
      data: $(this).parent().serialize(), // data sent with the post request

      // handle a successful response
      success: function (json) {

        $('#deleteModal').modal('hide');
        $(".card[data-pub-id=" + pub_id + "]").remove();
        $("#messageModal").modal('show');
        setTimeout(function () {
          $('#messageModal').modal('hide')
        }, 2000);

      },

      // handle a non-successful response
      error: function (xhr, errmsg, err) {

      }
    });
  }


  function onArchivePublication() {
    var pub_id = $('#archiveModal').data("pub-id");
    var endpoint = "/portal/archive-publication/" + pub_id + "/"
    $.ajax({
      url: endpoint, // the endpoint
      type: "POST", // http method
      data: $(this).parent().serialize(), // data sent with the post request

      // handle a successful response
      success: function (json) {

        $('#archiveModal').modal('hide');
        console.log('from click event of archive', pub_id);
        $(".card[data-pub-id=" + pub_id + "]").remove();

        /*
        $("#messageModal").modal('show');
        setTimeout(function () {
          $('#messageModal').modal('hide')
        }, 2000);
        */
      },
      // handle a non-successful response
      error: function (xhr, errmsg, err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    });
  }

  var loadingResourceData = false;

  function onClickShowModal() {
    //        $('.o-pub-content, .o-js-show-meta').on('click', function (event) {
    $(document).on('click', '.o-pub-content, .o-js-show-meta', function (event) {
      event.preventDefault();
      if (loadingResourceData === false) {
        loadingResourceData = true;
        var parents = $(this).parents();
        var card = parents.closest(".card");
        var user = $(this).data('user');
        var pub_id = card.data('pub-id');
        console.log('from show meta ')
        var endpoint = "/portal/get-publication-meta-data/" + pub_id + '/' + user;
        $.ajax({
          url: endpoint,
          type: 'get',
          data: "html",
          success: function (data) {
          console.log('js edig pub met', $(data).find("#o-js-edit-pub-meta"));

            $("body").append(data);
            $("#pubMeta").modal("show");
            loadingResourceData = false;
            if ($('#edit-resource-form #id_source_url').val() !== "") {
              $('#edit-resource-form #id_source_url').trigger('displayEvent');
            } else {
              $('#edit-resource-form #id_source_url').trigger('hideEvent');
            }
            if ($('#edit-resource-form #id_source').parent().find('a')[0] !== undefined) {
              $('#edit-resource-form #id_source').trigger('displaySourceUrl');
            } else {
              $('#edit-resource-form #id_source').trigger('hideSourceUrl');
            }
            $(document).trigger('btnClick');
          $(document).on("#o-js-edit-pub-meta", 'btnClick', function(){
              $("#o-js-edit-pub-meta").click();
          })
          $("#o-js-edit-pub-meta").click();
          },
          failure: function (data) {
            alert('error');
          }
        });
      }
    });
  }


  function showStarRating() {
    if ($(".my-rating").length) {
    $(".my-rating").starRating({
      starSize: 20,
      initialRating: 0,
      hoverColor: 'gold',
      activeColor: 'gold',
      ratedColor: 'gold',
      disableAfterRate: false,
      //            todo: change useFullStars to false
      useFullStars: true,
    });
    }

    if ($(".my-rating.js-inactive").length) {
        $(".my-rating.js-inactive").each(function() {
            $(this).starRating("setReadOnly", true);
         })
    }

  }

  $("#js-sign-in-submit").click(function (event) {
    event.preventDefault();
    $(".invalid-feedback").remove();
    $(".invalid").removeClass('invalid');
    signIn();

  })


  function signIn() {
    console.log("sign in is working!");
    $.ajax({
      url: "/accounts/sign-in/",
      type: "POST", // http method
      data: new FormData($('#js-sign-in-form')[0]),
      cache: false,
      contentType: false,
      processData: false,
      enctype: 'multipart/form-data',

      // handle a successful response
      success: function (response) {
        window.location = "/portal/publications";
      },

      error: function (xhr, errmsg, err) {

        formErrors = JSON.parse(xhr.responseJSON);
        for (var key in formErrors) {
          var fieldId = "#js-sign-in-form #id_" + key;
          var errorContent = formErrors[key];
          var errorMessage = errorContent[0]['message'];

          var errorFeedback = $("<div class='invalid-feedback'>" + errorMessage + "</div>");
          $(fieldId).addClass("invalid is-invalid");
          $(fieldId).parent().append(errorFeedback);
        }

        console.log(xhr.status + ": " + xhr.responseText);
      }
    });
  };

  $("#js-sign-up-submit").click(function (event) {
    event.preventDefault();
    $(".invalid-feedback").remove();
    $(".invalid").removeClass('invalid');
    signUp();

  })


  function signUp() {
    console.log("sign up is working!");
    $.ajax({
      url: "/accounts/sign-up/",
      type: "POST", // http method
      data: new FormData($('#js-sign-up-form')[0]),
      cache: false,
      contentType: false,
      processData: false,
      enctype: 'multipart/form-data',

      // handle a successful response
      success: function (response) {
        window.location = "/portal/publications";
      },

      error: function (xhr, errmsg, err) {

        formErrors = JSON.parse(xhr.responseJSON);
        for (var key in formErrors) {
          var fieldId = "#js-sign-up-form #id_" + key;
          var errorContent = formErrors[key];
          var errorMessage = errorContent[0]['message'];

          var errorFeedback = $("<div class='invalid-feedback'>" + errorMessage + "</div>");
          $(fieldId).addClass("invalid is-invalid");
          $(fieldId).parent().append(errorFeedback);
        }

        console.log(xhr.status + ": " + xhr.responseText);
      }
    });
  };


  function createResource(source) {
    console.log("create resource is working!");
    var endpoint = "/portal/create-resource/" + source + "/";
    $.ajax({
      url: endpoint ,
      type: "POST", // http method
      data: new FormData($('#new-resource-form')[0]),
      cache: false,
      contentType: false,
      processData: false,
      enctype: 'multipart/form-data',

      // handle a successful response
      success: function (response) {
        if (source === "profile") {
            var firstCard = $("#resources .card[data-pub-id]").first();
            if (firstCard.length == 0) {
                $("div #resources").append(response);
            } else {
                firstCard.before(response);
            }
         } else {
            var $newDiv = $("<div class='col-md-8 offset-md-2 mb-4'></div>");
            $newDiv.append(response);
            $(".col-md-8.offset-md-2.mb-4").first().parent().prepend($newDiv);

            onClickShowModal();
            onClickShowComment();
            showStarRating();
         }
            $('#new-resource-modal').modal('hide');
            $("#new-resource-form")[0].reset();
      },

      error: function (xhr, errmsg, err) {
        formErrors = JSON.parse(xhr.responseJSON);
        for (var key in formErrors) {
          var fieldId = "#new-resource-form #id_" + key;
          var errorContent = formErrors[key];
          var errorMessage = errorContent[0]['message'];

          var errorFeedback = $("<div class='invalid-feedback'>" + errorMessage + "</div>");
          $(fieldId).addClass("invalid is-invalid");
          $(fieldId).parent().append(errorFeedback);
        }
        console.log(xhr.status + ": " + xhr.responseText);
      }
    });
  };


  function editResource() {
    var pub_id = $("#pubMeta").data("pub-id");
    var card = $(".card[data-pub-id=" + pub_id + "]");
    var action_source = card.data("action-source");

    var endpoint = "/portal/edit-resource/" + pub_id + "/" + action_source + "/";
    $.ajax({
      url: endpoint,
      type: "POST",
      data: new FormData($('#edit-resource-form')[0]),
      cache: false,
      contentType: false,
      processData: false,
      enctype: 'multipart/form-data',

      success: function (response) {
        $('#pubMeta').modal('hide');
        var oldCard = $(".card[data-pub-id=" + pub_id + "]");
        oldCard.before(response);
        oldCard.remove();

        if (action_source === 'timeline') {
            onClickShowModal();
            onClickShowComment();
            showStarRating();
            var newCard = $(".card[data-pub-id=" + pub_id + "]");
            var $ratingElement = newCard.find(".my-rating");
            var rating = $ratingElement.parent().next(".list-inline-item").text();
            $ratingElement.starRating('setRating', rating);
        }
      },

      error: function (xhr, errmsg, err) {

        formErrors = JSON.parse(xhr.responseJSON)
        console.log(formErrors)
        for (var key in formErrors) {
          var fieldId = "#edit-resource-form #id_" + key;
          var errorContent = formErrors[key]
          var errorMessage = errorContent[0]['message']

          var errorFeedback = $("<div class='invalid-feedback'>" + errorMessage + "</div>")
          $(fieldId).addClass("invalid is-invalid")
          $(fieldId).parent().append(errorFeedback)
        }
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    });
  };

  function createComment(commentForm) {
    console.log("create comment is working!") // sanity check
    var endpoint = "/portal/create-comment/" + commentForm.data("pub-id") + "/";
    $.ajax({
      url: endpoint, // the endpoint
      type: "POST", // http method
      data: commentForm.serialize(), // data sent with the post request

      // handle a successful response
      success: function (response) {
        commentForm[0].reset();
        commentForm.after(response);
      },

      // handle a non-successful response
      error: function (xhr, errmsg, err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    });
  };


  function loadProjectConfigModal(projectId, user) {
    var endpoint = "/projects/configure-project/" + projectId + "/" + user + "/";

    $.ajax({
      url: endpoint,
      type: 'get',
      data: "html",
      success: function (response) {
        $("main").prepend(response);


        $("#projectConfigurationsModal").modal("show");
        $("#projectConfigurationsModal").data('project-id', projectId);
        $("#projectConfigurationsModal").find(".md-form input, .md-form textarea").each(function () {
            $(this).prev().closest('label').addClass('active');
            $('label').addClass("active");
        });
        $(document).trigger('btnClick');
          $(document).on("#js-edit-project-data", 'btnClick', function(){
              $("#js-edit-project-data").click();
          })
          $("#js-edit-project-data").click();
        // delete the modal from the DOM when close it
        $(document).on('hidden.bs.modal', '#projectConfigurationsModal', function (e) {
          $("#projectConfigurationsModal").each(function () {
            $(this).remove();
          });
        });
      },

      failure: function (data) {
        alert('error');
      }
    });

  };

/*
  function archiveProject(projectId) {
    var endpoint = '/projects/archive-project/' + projectId + '/';
    console.log(new FormData($('.js-archive-project-form')[0]))
  }
  */

  $(document).on("click", ".js-configure-project", function (event) {
    event.stopPropagation();
    event.preventDefault();

    var card = $(this).closest('.card');
    var user = $(this).data("user");
    var projectId = card.data("project-id");


    loadProjectConfigModal(projectId, user);

  })



  onClickShowModal();
  showStarRating();

  // Submit post on submit
  $("#btnSubmit").click(function (event) {
    event.preventDefault();
    // remove error feedback
    $(".invalid-feedback").remove();
    $(".invalid").removeClass('invalid, is-invalid');
    var location = window.location.href;
    if (location.indexOf("overview") >= 0 && location.indexOf("accounts") >= 0) {
        createResource('profile');
    } else {
        createResource('timeline');
    }

  })


  $(".o-js-pub-actions.o-js-delete-pub").click(function (event) {
    var pub_id = $(this).data("pub-id");
    $("#deleteModal").data("pub-id", pub_id);

  });

  $("#deleteBtn").click(function (event) {
    event.preventDefault();
    onDeletePublication();
  });

  $(document).on("click", ".o-js-pub-actions.o-js-archive-pub", function (event) {
    event.preventDefault();

    var pub_id = $(this).closest(".card").data("pub-id");
    /* add publication title to modal
    $("#archiveModal .modal-body").prepend(col.find(".card-title").text());
    */

    // add pub id to modal
    $("#archiveModal").data("pub-id", pub_id);
    $("#archiveModal").modal("show");
  })

  $("#archiveBtn").on('click', function (event) {
    event.preventDefault();
    onArchivePublication();
  })

  $(".o-js-submit-comment").click(function (event) {
    event.preventDefault();
    var commentForm = $(this).parent();
    createComment(commentForm);
  })

  $(".jq-star").click(function () {
    var myRating = $(this).parent()
    var rating = myRating.starRating('getRating');
    var pub_id = myRating.data('pub-id');
    // myRating.starRating('setRating', rating);
    // console.log("publication-id", myRating.data('pub-id'));

    $.ajax({
      url: "/portal/rate-publication/", // the endpoint
      type: "POST", // http method
      data: {
        "publication-id": pub_id,
        "rating": rating
      }, // data sent with the post request

      // handle a successful response
      success: function (json) {
        response = JSON.parse(json)
        console.log("from success", response)
        myRating.parent().next().text(response.publication_score)
        myRating.starRating('setRating', response.publication_score)
      },

      // handle a non-successful response
      error: function (xhr, errmsg, err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    });
  });




  $(".my-rating").each(function () {
    var endpoint = "/portal/get-rating/" + $(this).data('pub-id');
    var $ratingElement = $(this);
    $.ajax({
      url: endpoint, // the endpoint
      type: "GET", // http method
      data: "json",

      // handle a successful response
      success: function (json) {
        console.log(json)
        //                $ratingElement.parent().next().append('<i class="fa fa-check"></i>')
        $ratingElement.starRating('setRating', json.rating);
        //                $ratingElement.starRating('setReadOnly', true)

      },

      // handle a non-successful response
      error: function (xhr, errmsg, err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    });

  })


  /* todo: revise this */
  $("#showMeta").click(function (event) {
    event.preventDefault();
    onClickShowModal();
  });



  $(".filter-form input").click(function (event) {
    event.preventDefault();
    console.log("input clicked");
    $(".filter-form").submit();
  });

  $(document).on('hidden.bs.modal', '#pubMeta', function (e) {
    $("#pubMeta").each(function () {
      $(this).remove();
    });
  });

  $(document).on("click", "#o-js-edit-pub-meta", function () {
    $("#pubMeta input, #pubMeta textarea, #pubMeta select").prop("disabled", false);
    $("#o-js-submit-edit").prop("disabled", false);

    $(this).remove();
  });

  $(document).on("click", "#js-edit-project-data", function () {
    $("#projectConfigurationsModal input, #projectConfigurationsModal textarea, #projectConfigurationsModal select, #projectConfigurationsModal checkbox").prop("disabled", false);
    $("#js-edit-project-submit").prop("disabled", false);

    $(this).remove();
  });

  $(document).on("click", "#o-js-submit-edit", function (event) {
    event.preventDefault();
    $(".invalid-feedback").remove();
    $(".invalid").removeClass('invalid');
    editResource();
  })

  /*
  var content = textarea.val();
  content = content.replace(/\n/g, '<br>');
  var hiddendiv = $(".hiddendiv");
  hiddendiv.html(content + '<br>');
  textarea.css('height', hiddendiv.height());
  */
  $("#js-new-project-submit").click(function (event) {

    event.preventDefault();
    $(".invalid-feedback").remove();
    $(".invalid").removeClass('invalid');

    createProject();
  })

  function createProject() {
  console.log("create resource is working!");
    $.ajax({
      url: "/projects/create-project/",
      type: "POST", // http method
      data: new FormData($('#js-new-project-form')[0]),
      cache: false,
      contentType: false,
      processData: false,
      enctype: 'multipart/form-data',

      // handle a successful response
      success: function (response) {
        $('#js-new-project-modal').modal('hide');
        $("#js-new-project-form")[0].reset();
        var response = $(response);
        if ($(".o-js-card-project").first().length == 0) {
            $("div #projects").append(response)
        } else {
            $(".o-js-card-project").first().parent().prepend(response);
        }

      },

      error: function (xhr, errmsg, err) {
        formErrors = JSON.parse(xhr.responseJSON);
        for (var key in formErrors) {
          var fieldId = "#js-new-project-form #id_" + key;
          var errorContent = formErrors[key];
          var errorMessage = errorContent[0]['message'];

          var errorFeedback = $("<div class='invalid-feedback'>" + errorMessage + "</div>");
          $(fieldId).addClass("invalid is-invalid");
          $(fieldId).parent().append(errorFeedback);
        }
        console.log(xhr.status + ": " + xhr.responseText);
      }
    });
  }


  $(document).on("click", "#js-edit-project-submit", function (event) {
    event.preventDefault();
    $(".invalid-feedback").remove();
    $(".invalid").removeClass('invalid');

    editProject();
  })


  function editProject() {
  console.log("edit project is working!");
  projectId = $('#projectConfigurationsModal').data("project-id");
  console.log(">>>>>>>>>>>>>>>>>>>>>>>project id", projectId)
  var endpoint = "/projects/edit-project/" + projectId + "/";
    $.ajax({
      url: endpoint,
      type: "POST", // http method
      data: new FormData($('#js-edit-project-form')[0]),
      cache: false,
      contentType: false,
      processData: false,
      enctype: 'multipart/form-data',

      // handle a successful response
      success: function (response) {
        $('#projectConfigurationsModal').modal('hide');
        var response = $(response);
        var oldCard = $(".card[data-project-id=" + projectId + "]");
        oldCard.before(response);
        oldCard.remove();
      },

      error: function (xhr, errmsg, err) {
        formErrors = JSON.parse(xhr.responseJSON);
        for (var key in formErrors) {
          var fieldId = "#js-edit-project-form #id_" + key;
          var errorContent = formErrors[key];
          var errorMessage = errorContent[0]['message'];

          var errorFeedback = $("<div class='invalid-feedback'>" + errorMessage + "</div>");
          $(fieldId).addClass("invalid is-invalid");
          $(fieldId).parent().append(errorFeedback);
        }
        console.log(xhr.status + ": " + xhr.responseText);
      }
    });
  }


  function archiveProject() {
    var projectId = $('.archive-project-modal').data("project-id");
    var endpoint = "/projects/archive-project/" + projectId + "/"
    $.ajax({
      url: endpoint, // the endpoint
      type: "POST", // http method
      data: $(this).parent().serialize(), // data sent with the post request

      // handle a successful response
      success: function (json) {

        $('.archive-project-modal').modal('hide');
        $(".card[data-project-id=" + projectId + "]").remove();

        $("#messageModal").modal('show');
        setTimeout(function () {
          $('#messageModal').modal('hide')
        }, 2000);

      },

      // handle a non-successful response
      error: function (xhr, errmsg, err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    });
  }

  $(".js-archive-project").click(function (event) {
    event.preventDefault();
    event.stopPropagation();
    var projectId = $(this).closest(".card").data("project-id");

    $(".archive-project-modal").data("project-id", projectId);
    $(".archive-project-modal").modal("show");
  })

  $("#js-archive-project-submit").on('click', function (event) {
    event.preventDefault();
    archiveProject();
  })

  $(document).on("click", ".js-block-member", function (event) {
    event.preventDefault();
    console.log(">>>>>>>>>>>>>>>target", event.target)
    var member = $(this).data("member");
    var projectId = $("#projectConfigurationsModal").data("project-id");
    var endpoint = "/projects/block-member/" + projectId + "/" + member + "/";
    var $element = $(this);
    var memberStatus = $element.data("member-status");

    $.ajax({
      url: endpoint, // the endpoint
      type: "POST", // http method
      data: {"member_status": memberStatus},
      // handle a successful response
      success: function (json) {

        if (memberStatus === "True") {
            $element.removeClass("fa-ban text-danger");
            $element.addClass("fa-check-circle-o text-success")
            $element.prop("title", "Activer ce membre");
            $element.data("member-status", "False");
        } else {
            $element.removeClass("fa-check-circle-o text-success");
            $element.addClass("fa-ban text-danger")
            $element.prop("title", "Bloquer ce membre");
            $element.data("member-status", "True");
        }

      },

      // handle a non-successful response
      error: function (xhr, errmsg, err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    });
//    blockMember(member);
    console.log(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ban clicked")
  })

   $("#id_source_url").parent().css('display', 'none');

    $("input[name=source-radio]").change(function () {
    var test = $(this).val();
    console.log(test)
    if (test === 'source-url') {
        $("#id_source_url").parent().show();
        $("#id_source").parent().hide();
    } else if (test === 'source-pdf') {
        $("#id_source").parent().show();
        $("#id_source_url").parent().hide();
    }
});


    $(document).on("displayEvent", "#edit-resource-form #id_source_url", function () {
        $(this).css("display", "block");
    })

    $(document).on("hideEvent", "#edit-resource-form #id_source_url", function () {
        $(this).parent().css("display", "none");
    })

    $(document).on("displaySourceUrl", "#edit-resource-form #id_source", function () {
      $(this).css("display", "block");
  })

  $(document).on("hideSourceUrl", "#edit-resource-form #id_source", function () {
      $(this).parent().css("display", "none");
  });
    $("select, input[type='file']").parent().find("label").addClass("active");

});