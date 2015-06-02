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

// custom written

console.log('window height is '+$(window).height());

// function to auto adjust top margin for the body
$(function(){
  var top = $('.navbar-fixed-top').outerHeight(true);
  $('.body').stop().animate({'top':top});
});
$('body').css({'min-height':$(window).height()});
$(window).on('resize',function(){
  var top = $('.navbar-fixed-top').outerHeight(true);
  $('.body').stop().animate({'top':top});
});

// convert rendered form inputs that require tagging
$('form .taggable').each(function(){
    console.log($(this).attr('id'));
    $taggable_input = $(this);
    var name = $taggable_input.attr('name');
    $taggable_input.attr('name','');
    $taggable_input.removeClass('taggable').addClass('d_input');
    if($taggable_input.data('results') == 'multiple')
        var results = '"multiple"><div class="d_results"></div>';
    else if($taggable_input.data('results') == 'single')
        var results = '"single">';
    var old_input = $taggable_input.clone().wrap('<p>').parent().html();
    var hidden_input = '<input type="hidden" name="' + name + '" value="">';
    var new_input = '<div class="d_search" data-results='+ results + old_input + hidden_input + '<div class="dropdown"><ul class="dropdown-menu d_list"></ul></div></div>';
    $taggable_input.replaceWith(new_input);
});

// dynamic select function
$('.d_input').keyup(function(event){
    var $this = $(this);
    var query = $this.val()
    ,   search = "/search" + $this.data('search')
    ,   create = $this.data('create');
    console.log(query, search, create)
    if(!create)
        create = '';
    $.ajax({
        url : search,
        type : "GET",
        data : { the_query : query, the_create : create},

        success: function(result){
            $this.next().next().find(".d_list").html(result);
        },

        error : function(xhr,errmsg,err) {
            $this.next().next().find(".d_list").html("<li><a href='#' class='tag_multiple'>Sorry, unable to fetch results. Try later.</a></li>");
            console.log(errmsg,err);
        }
    });
    if(query != '')
        $(this).next().next().find('.d_list').css({'display':'block'});
});

$(".d_list").on('click', 'a', function(){
    aj_search($(this));
    function aj_search ($this){
        //var $this = $(this);
        var $sabke_papa = $this.closest('.d_search');
        if($this.attr('class') == 'create'){
            var value = $sabke_papa.children('input').val();
            console.log('input wala');
        }
        else if($this.attr('class').indexOf('create_new') >= 0){
            var create_now = 'create_' + $sabke_papa.children('input').first().data('search');
            console.log(create_now);
            $sabke_papa.find('.d_list').css({'display':'none'});
            $this.attr('href','#'+create_now);
            var collapse_parent = $this.closest('.panel-group').attr('id');
            $this.data('parent', '#'+collapse_parent);
            console.log($this.data('parent'))
            return 0;
        }
        else{
            var value = $this.text();
            console.log('list wala', $this.attr('class'));
        }
        var r_type = $sabke_papa.data('results');
        console.log($sabke_papa.attr('class'));
        if(r_type == 'single'){
            $sabke_papa.children('input').first().before('<div class="alert"><a href="#" class="close">&times;</a><strong>'+value+'</strong></div>').addClass('hide').next().val(value);

            $sabke_papa.find('.close').on('click', function(){
                $(this).parent('.alert').alert('close');
                $sabke_papa.children('input').removeClass('hide').focus();
            });
        }
        else if(r_type == 'multiple'){
            var $d_results = $sabke_papa.children('.d_results');
            var pre_value = $d_results.html();
            $d_results.html(pre_value+'<div class="alert alert_tag"><a href="#" class="close">&times;</a><strong>'+value+'</strong></div>');
            var pre_value_snd = $sabke_papa.children('input').next().val();
            $sabke_papa.children('input').next().val(pre_value_snd + value + ',');
            $sabke_papa.find('.close').on('click', function(){
                $(this).parent('.alert_tag').alert('close');
                $sabke_papa.children('input').focus();
            });
        }
        $sabke_papa.find('.d_list').css({'display':'none'});
    }
});

$(".d_list").on('click', '.no-select', function(){
    var $sabke_papa = $(this).closest('.d_search');
    $sabke_papa.find('.d_list').css({'display':'none'});
});

// displaying the dynamically formed list
$(".d_list").hover(function(){
    $(this).css({'display':'block'});
    $(".d_input").off('blur');
},function(){
    //  $(this).css({'display':'none'});
    $(".d_input").blur(function(){
    $(this).next().next().find('.d_list').css({'display':'none'});
});
});
$(".d_input").focus(function(){
    var $this = $(this);
    var query = $this.val();
    if(query != '')
        $this.next().next().find('.d_list').css({'display':'block'});
});
$(".d_input").blur(function(){
    $(this).next().next().find('.d_list').css({'display':'none'});
});

// function to submit form ajaxly
$(".ajax_andar").on('click','.form-ajax',function(event){
    event.preventDefault();
    console.log('default nahi');
    var $this = $(this);
    var $papa = $this.closest('.ajax_papa');
    var $form = $this.closest('form');
    console.log($form.serialize());
    $.ajax({
        url : $form.attr('action'),
        type : $form.attr('method'),
        data : $form.serialize(),

        success: function(response){
          for(i=0; i < response.fields.length; i++)
            $papa.find('.'+response.fields[i]).text(response.data[response.fields[i]]);
        },

        error : function(xhr,errmsg,err) {
            $this.next().next().find(".d_list").html("<li><a href='#' class='tag_multiple'>Sorry, unable to fetch results. Try later.</a></li>");
            console.log(errmsg,err);
        }
    });
});

//home page
var load = true;
$(window).scroll(function() {
    if (!load)
        return;
    var $this = $(this)
    ,       $pg = $('.paginator');
    var a = $this.scrollTop();
    var b = $this.outerHeight();
    var c = $pg.offset().top;
    var nxt = $pg.data('next_page');
    if((a+b-c) > 0){
        load = false;
        $.ajax({
          url : window.location,
          type : "GET",
          data : { page: nxt},

          success: function(response){
            nxt++;
            $pg.data('next_page',nxt);
            $pg.before(response);
            load = true;
          },

            error : function(xhr,errmsg,err) {
            console.log(errmsg,err);
            $pg.before("<h4 class='text-center'>Can't load further content. Refresh the page.</h4>");
        }
        });
    }
});

//profile page
$('#img_profile_box').on({
    mouseover: function(){
        $('#img_upload').stop().animate({'height':'28px','top':'-49px','padding':'4px 0px'});
        $('#img_upload').on('click',function(){
            $('#img_upload').stop().animate({'height':'0px','top':'-20px','padding':'0px'});
        });
    },
    mouseout: function(){
        $('#img_upload').stop().animate({'height':'0px','top':'-20px','padding':'0px'});
    }
});
$(function() {
$('.image-editor').cropit();
$('form').submit(function() {
  // Move cropped image data to hidden input
  var imageData = $('.image-editor').cropit('export');
  $('.hidden-image-data').val(imageData);
  $('#id_image').val(imageData);

  // Print HTTP request params
  var formValue = $(this).serialize();
});
});