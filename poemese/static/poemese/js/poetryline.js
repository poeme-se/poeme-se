$(function(){

   // Initialize Froala Editor
   $('#id_conteudo').froalaEditor();
   $('#id_titulo').froalaEditor({
     toolbarInline: true,
     charCounterCount: false,
     toolbarButtons: ['bold', 'italic', 'underline', 'strikeThrough', 'color', '-', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'indent', 'outdent', '-', 'insertImage', 'insertLink', 'insertFile', 'insertVideo', 'undo', 'redo']
   });

   // Initialize modals
   $('#delete-modal').modal();
   $('#comment-modal').modal();
   $('#suggest-modal').modal();
   $('#suggest-show-modal').modal();
   $('#add-book-modal').modal();

   $("#cancel-modal-button").click(function (){
     $('#delete-modal').modal("close");
   });

   // Initialize the star rateyo
   $(".rateyo").rateYo({
     rating    : 5,
     spacing   : "20px",
     numStars  : 5
   });
   // this function change dinamically the rating of stars
   $("#stars_rate").rateYo().on("rateyo.change", function (e, data) {
      var rating = data.rating;
      $("#number_of_stars").val($("#stars_rate").rateYo("option", "rating")); // Give the rating to the hidden input
   });

   // Tests to visualize or no some buttons, of the create form or edit form
   if( (window.location.pathname).toString().slice(1, 10) == "atualizar" ){
     $("#submit-edit").toggle();
     $("#btn-cancel-edit").toggle();
     $("#container-edit-form").css('display', 'block');
   }else if( (window.location.pathname).toString().slice(1, 9) == "escrever"){
     $("#submit-create").toggle();
     $("#btn-cancel-create").toggle();
     $("#container-edit-form").css('display', 'block');
   }

   // configurations of notes
   $("#notificationLink").click(function(){
     $("#notificationContainer").fadeToggle(300);
     $("#notification_count").fadeOut("slow");
     return false;
   });
   //Document Click
   $(document).click(function(){
     $("#notificationContainer").hide();
   });
   //Popup Click
   $("#notificationContainer").click(function(){
     return false
   });

   personalizar_poemas(); // Call the clean process of formatation and add event for stop the scroll

   // definition of a side nav button
   $('.button-collapse').sideNav({
      menuWidth: 300, // Default is 300
      edge: 'left', // Choose the horizontal origin
   });

   $(window).scroll(function() {
     url_path = location.pathname.split('/')[1];
     if($(window).scrollTop() + $(window).height() == $(document).height()) {
       if(url_path == "listaPoemas"){
         name_without_space = trim($("#name-user").text());
         loadMorePoems(name_without_space);
       }else if(url_path == ""){
         loadMorePoems();
       }else if(url_path == "obras"){
         console.log("Já posso carregar obras");
       }
     }
   });

   $("#search_work_field").on('input', function(){ // This function will call the view that return books
     search_work();
   });

   $("#search_friends_field").on('input', function(){ // This function will call the view that return friends
     search_follows();
   });

   $("#delete-modal-button").click(function (e){
     console.log('localhost:8000/' + $("#delete-modal-button").prop( "href"))
     window.location.replace('http://localhost:8000/' + $("#delete-modal-button").prop( "href"));
   });

});

// Functions of charge on demand
function loadMorePoems(name){
  start_point = $(".container-top-poem").length;
  $(".view-more").css('display','block');
  $.ajax({
     type: 'GET',
     url: '/carregarMaisPoemas/',
     data: {
       name: name,
       offset: start_point
     },
     success:function(data){
       $("#add_more_poems").append(data);
       personalizar_poemas();
       $(".view-more").css('display','none');
     },
     error:function(error){
       console.log("error...");
     }
  });
}

// This process remove the formatation of the poem titles
function personalizar_poemas(){
  $(".titulo-poema").each(function (index){
    var title = $(".titulo-poema").eq(index).text();
    $(".titulo-poema").eq(index).empty();
    $(".titulo-poema").eq(index).addClass("truncate bolder-title");
    $(".titulo-poema").eq(index).append(title);
  });
  add_scroll_stop();
  $(".card-reveal").mCustomScrollbar({
    theme: "minimal-dark",
    scrollInertia:800
  });
}

// This function stop the scroll of the window, and let it on the '.card-reveal'
function add_scroll_stop(){
  $('.card-reveal').on( 'mousewheel DOMMouseScroll', function (e) {
     var e0 = e.originalEvent;
     var delta = e0.wheelDelta || -e0.detail;

     this.scrollTop += ( delta < 0 ? 1 : -1 ) * 30;
     e.preventDefault();
  });
}
// Functions of search
function search_work(){
  $.ajax({
      type: 'GET',
      url: '/search_works/',
      data: {
        title: $("#search_work_field").val()
      },
      success:function(data){
        $(".container-booklist").empty();
        $(".container-booklist").append(data);
      },
      error:function(error){
        console.log("error...");
      }
   });
}

function search_follows(){
  $.ajax({
      type: 'GET',
      url: '/search_friends/',
      data: {
        user: trim($("#name-user").text()),
        friend_name: $("#search_friends_field").val()
      },
      success:function(data){
        $(".container_principal_follow").empty();
        $(".container_principal_follow").append(data);
      },
      error:function(error){
        console.log("error...");
      }
   });
}
 // Define the remove url for the modal button
function delete_modal(pk, title){
  $("#delete-modal-button").prop( "href", "excluir/" + pk );
  $('#delete-modal').modal('open');
}

// Ajax Call to load comments on modal
function load_comments(id_poema, title_poem){
  $.ajax({
      type: 'GET',
      url: '/loadComments/',
      data: {
        id_poem: id_poema,
      },
      success:function(data){
        $("#comment-modal .modal-content").empty();
        $("#comment-modal .modal-content").append(data);
        $('#id-poem').empty();
        $('#id-poem').append("<pre>Título: " + title_poem.replace(/(<([^>]+)>)/ig, "") + "   ID:" + id_poema + "</pre>");
        $('#comment-modal').modal('open');
      },
      error:function(error){
        console.log("error...");
      }
   });
 }


 // Function of likes
 function toggleLike(pseudonimo, id_poema){
   data = new Date().toJSON().slice(0,10);
   $.ajax({
       type: 'GET',
       url: '/addLike/',
       data: {
         name: pseudonimo,
         id_poem: id_poema,
         date: data
       },
       success:function(data){ // Será adicionado o número de likes onde se deve
         $("#" + id_poema + " .number-likes").empty();
         msg = ""; // Será construída uma mensagem informando as pessoas que curtiram
         if(data.number == 1){
           msg= data.number.toString() + " pessoa curtiu";
           $("#" + id_poema + " .number-likes").css("border-color", "rgb(193, 179, 179)");
         }else if(data.number > 1){
           msg= data.number.toString() + " pessoas curtiram";
           $("#" + id_poema + " .number-likes").css("border-color", "rgb(193, 179, 179)");
         }else{
           msg="";
           $("#" + id_poema + " .number-likes").css("border-color", "white");
         }
         $("#" + id_poema + " .number-likes").append(msg);
       },
       error:function(error){
         console.log("error...");
       }
    });
  }

 // Ajax Call to add comments
function add_comment(id_author){
  id_poema = parseInt($("#id-poem").text().match(/\d+/));
  content_comment = $("#text-new-comment").val();
  $("#text-new-comment").val("");
  date_comment = new Date().toJSON().slice(0,10);
  $.ajax({
      type: 'GET',
      url: '/addComment/',
      data: {
        name: id_author,
        id_poem: id_poema,
        content: content_comment,
        date: date_comment
      },
      success:function(data){ // Serão carregados mais comentários
        load_comments(id_poema);
      },
      error:function(error){
        console.log("error...");
      }
   });
}

// Prepare suggestion modal with the ID of the poem that it refers
function prep_suggestion(id_poema, title_poem){
  $('#id-poem-suggestion').empty();
  $('#id-poem-suggestion').append("<pre>Título: " + title_poem.replace(/(<([^>]+)>)/ig, "") + "   ID:" + id_poema + "</pre>");
  $('#suggest-modal').modal('open');
}

// Ajax call to send suggestions
function send_suggestion(id_author){
  id_poema = parseInt($("#id-poem-suggestion").text().match(/\d+/));
  content_suggestion = $("#suggest_content").val();
  $("#suggest_content").val("");
  date_suggestion = new Date().toJSON().slice(0,10);
  rate_value = $("#number_of_stars").val();

  $.ajax({
      type: 'GET',
      url: '/addSuggestion/',
      data: {
        name: id_author,
        id_poem: id_poema,
        content: content_suggestion,
        date: date_suggestion,
        poem_rate: rate_value
      },
      success:function(data){
         Materialize.toast('A sugestão foi enviada com sucesso!', 3000, 'rounded')
      },
      error:function(error){
        console.log("Some error ocurred...");
      }
   });
}
function show_suggestion_modal(id_poema){
  $.ajax({
      type: 'GET',
      url: '/loadSuggestion/',
      data: {
        id_poem: id_poema
      },
      success:function(data){
        $('#suggest-show-modal .modal-content').empty();
        $('#suggest-show-modal .modal-content').append(data);
        $('#suggest-show-modal').modal("open");
      },
      error:function(error){
        console.log("Some error ocurred...");
      }
   });
}
// Funtion of follow people
function follow_profile(id_user_profile, id_user){
  relationship_date = new Date().toJSON().slice(0,10);
  $.ajax({
      type: 'GET',
      url: '/follow/',
      data: {
        id_follower: id_user,
        id_followed: id_user_profile,
        date: relationship_date
      },
      success:function(data){
        if (data.if_follow == 1){
          $("#btn-follow-unfollow").text("SEGUINDO");
        }else{
            $("#btn-follow-unfollow").text("SEGUIR");
        }
      },
      error:function(error){
        console.log("error...");
      }
   });
}

// Define conquers of the poet
function def_conquer(likes){
  if(likes >= 10 && likes < 100){
    $(".conquers-container").css("display", "block");
    empty_container_conquers();
    $(".description_level").append("Escritor iniciante");
    $(".aprovation_text_conquer").append("+10 APROVAÇÕES");
  }else if(likes >= 100 && likes < 1000){
    $(".conquers-container").css("display", "block");
    empty_container_conquers();
    $(".description_level").append("Autor amador");
    $(".aprovation_text_conquer").append("+100 APROVAÇÕES");
  }else if(likes >= 1000 && likes < 10000){
    $(".conquers-container").css("display", "block");
    empty_container_conquers();
    $(".description_level").append("Escritor experiente");
    $(".aprovation_text_conquer").append("+1000 APROVAÇÕES");
  }else if(likes >= 10000 && likes < 100000){
    $(".conquers-container").css("display", "block");
    empty_container_conquers();
    $(".description_level").append("Autor renomado");
    $(".aprovation_text_conquer").append("+10000 APROVAÇÕES");
  }else if(likes >= 100000){
    $(".conquers-container").css("display", "block");
    empty_container_conquers();
    $(".description_level").append("Mestre escritor");
    $(".aprovation_text_conquer").append("+100000 APROVAÇÕES");
  }else{}
}
function empty_container_conquers(){
  $(".description_level").empty();
  $(".aprovation_text_conquer").empty();
}

 // Plugin that return all classes name
 $.fn.allTheClasses = function() {
    return this[0].className.split(' ');
 }

 // Function that return a string without space
 function trim(str) {
   return str.replace(/^\s+|\s+$/g,"");
 }
