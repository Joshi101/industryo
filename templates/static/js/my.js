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

// function to auto adjust top margin for the body

function body_slide () {
  var top = $('.navbar-fixed-top').outerHeight(true);
  $('.body').stop().animate({'top':top});  
}

$(body_slide);
$(window).on('resize', body_slide);

// convert rendered form inputs that require tagging
function convert_to_taggable(){
    var $this = $(this);
    var name = $this.attr('name')
    ,   result = $this.data('results');
    $this.attr('name','');
    $this.removeClass('taggable').addClass('d_input');
    if (result == 'multiple')
        var d_results = '"multiple"><div class="d_results"></div>';
    else if(result == 'single')
        var d_results = '"single">';
    var old_input = $this.clone().wrap('<p>')
        .parent().html();
    var hidden_input = '<input type="hidden" name="' + name + '" value="">';
    var new_input = '<div class="d_search" data-results='+ d_results + old_input + hidden_input + '<div class="dropdown"><ul class="dropdown-menu d_list"></ul></div></div>';
    $this.replaceWith(new_input);
}

$('form .taggable').each(convert_to_taggable);

// dynamic select function
$('.d_input').keyup(function(event){
    var $this = $(this);
    var query = $this.val()
    ,   search = "/search" + $this.data('search')
    ,   create = $this.data('create');
    $this.next().val(query);
    if(!create)
        create = '';
    console.log(query, search, create);
    $.ajax({
        url : search,
        type : "GET",
        data : { the_query : query, the_create : create},
        success: function(result){
            $this.nextAll('.dropdown')
                .children(".d_list").html(result);
            var $create_a = $this.nextAll('.dropdown')
                .find(".create_new");
            var create_now = 'create_' + $this.data('search');
            console.log(create_now);
            $create_a.attr('href','#'+create_now);
            var collapse_parent = $create_a.closest('.panel-group').attr('id');
            $create_a.data('parent', '#'+collapse_parent);
            console.log($create_a.data('parent'));
        },
        error : function(xhr,errmsg,err) {
            $this.nextAll('.dropdown')
                .children(".d_list").html("<li><a href='#' class='tag_multiple'>Sorry, unable to fetch results. Try later.</a></li>");
            console.log(errmsg,err);
        }
    });
    if(query != '')
        $(this).nextAll('.dropdown')
            .children('.d_list').css({'display':'block'});
});

$(".d_list").on('click', 'a', function(){
    aj_search($(this));
    function aj_search ($this){
        var $sabke_papa = $this.closest('.d_search');
        if($this.attr('class') == 'create'){
            var value = $sabke_papa.children('input').val();
            console.log('input wala');
        }
        else if($this.attr('class').indexOf('create_new') >= 0){
            $sabke_papa.find('.d_list').css({'display':'none'});
            var value = $sabke_papa.children('input').val();
            var target = $this.attr('href');
            console.log(target,value);
            $(target).find('input[type=text]').first().val(value);
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
          if (response.fields){
            for(i=0; i < response.fields.length; i++){
                $papa.find('.'+response.fields[i]).text(response.data[response.fields[i]]);
            }
          }
          if (response.inputs){
            for(i=0; i < response.inputs.length; i++){
                $papa.find('#'+response.inputs[i]).val(response.value[response.inputs[i]]);
            }
          }
          if (response.elements){
            for(i=0; i < response.elements.length; i++){
                $papa.find('.'+response.elements[i]).html(response.html[response.elements[i]]);
            }
          }
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

// function for main feeder
$('#form_feed').on('focus','textarea',function(){
    var $this = $(this);
    $this.attr('rows','3');
    $this.removeClass('seamless_l');
    $this.parent().find('.input-group-addon').hide();
    $this.closest('form').find('.textarea_bottom').removeClass('hide');
    autosize.update($this);
});
$('#form_feed textarea').on('blur', function(){
    var $this = $(this);
    $this.attr('rows','1');
    $this.addClass('seamless_l');
    $this.closest('form').find('.textarea_bottom').addClass('hide');
    autosize.update($this);
    $this.parent().find('.input-group-addon').show();
});
$('#form_feed .btn, .img_pre').on({
    mouseover: function(){
        $('#form_feed textarea').off('blur');
    },
    mouseout: function(){
        $('#form_feed textarea').on('blur', function(){
            var $this = $(this);
            $this.attr('rows','1');
            $this.addClass('seamless_l');
            $this.closest('form').find('.textarea_bottom').addClass('hide');
            autosize.update($this);
            $this.parent().find('.input-group-addon').show();
        });
    }
});