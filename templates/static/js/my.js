// bootstrap-wysiwyg

$(function(){
function initToolbarBootstrapBindings() {
  var fonts = ['Serif', 'Sans', 'Arial', 'Arial Black', 'Courier', 
        'Courier New', 'Comic Sans MS', 'Helvetica', 'Impact', 'Lucida Grande', 'Lucida Sans', 'Tahoma', 'Times',
        'Times New Roman', 'Verdana'],
        fontTarget = $('[title=Font]').siblings('.dropdown-menu');
  $.each(fonts, function (idx, fontName) {
      fontTarget.append($('<li><a data-edit="fontName ' + fontName +'" style="font-family:\''+ fontName +'\'">'+fontName + '</a></li>'));
  });
  $('a[title]').tooltip({container:'body'});
    $('.dropdown-menu input').click(function() {return false;})
        .change(function () {$(this).parent('.dropdown-menu').siblings('.dropdown-toggle').dropdown('toggle');})
    .keydown('esc', function () {this.value='';$(this).change();});

  $('[data-role=magic-overlay]').each(function () { 
    var overlay = $(this), target = $(overlay.data('target')); 
    overlay.css('opacity', 0).css('position', 'absolute').offset(target.offset()).width(target.outerWidth()).height(target.outerHeight());
  });
  if ("onwebkitspeechchange"  in document.createElement("input")) {
    var editorOffset = $('#editor').offset();
    $('#voiceBtn').css('position','absolute').offset({top: editorOffset.top, left: editorOffset.left+$('#editor').innerWidth()-35});
  } else {
    $('#voiceBtn').hide();
  }
};
function showErrorAlert (reason, detail) {
    var msg='';
    if (reason==='unsupported-file-type') { msg = "Unsupported format " +detail; }
    else {
        console.log("error uploading file", reason, detail);
    }
    $('<div class="alert"> <button type="button" class="close" data-dismiss="alert">&times;</button>'+ 
     '<strong>File upload error</strong> '+msg+' </div>').prependTo('#alerts');
};
initToolbarBootstrapBindings();  
$('#editor').wysiwyg({ fileUploadError: showErrorAlert} );
window.prettyPrint && prettyPrint();
});

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
    if(event.key == ','){
        $this.siblings('.dropdown').children('.d_list').find('a').first().trigger('click');
        $this.val('');
    }
    else{
	
		console.log('loipu')
        var query = $this.val()
        ,   search = "/search" + $this.data('search')
        ,   create = $this.data('create');
        if(!create)
            create = '';
        var type = $this.siblings('input[name=type]').val();
        if(!type)
            type = '';
        console.log(query, search, create, type);
        $.ajax({
            url : search,
            type : "GET",
            data : { the_query : query, the_create : create, the_type: type},
            success: function(result){
                $this.nextAll('.dropdown')
                    .children(".d_list").html(result);
                if (create == 'create_new'){
                    var $create_a = $this.nextAll('.dropdown')
                        .find(".create_new");
                    var create_now = 'create_' + $this.data('search');
                    console.log(create_now);
                    $create_a.attr('href','#'+create_now);
                    var collapse_parent = $create_a.closest('.panel-group').attr('id');
                    $create_a.data('parent', '#'+collapse_parent);
                    console.log($create_a.data('parent'));
                }
            },
            error : function(xhr,errmsg,err) {
                $this.nextAll('.dropdown')
                    .children(".d_list").html("<li class='list-group-item-warning'><a>Sorry, unable to fetch results. Try later.</a></li>");
                console.log(errmsg,err);
            }
        });
        if(query != '')
            $(this).nextAll('.dropdown')
                .children('.d_list').css({'display':'block'});
    }
});

$(".d_list").on('click', 'a', function(event){
    event.preventDefault();
    aj_search($(this));
    function aj_search ($this){
        var $sabke_papa = $this.closest('.d_search');
        if ($this.attr('class') == 'create'){
            var value = $sabke_papa.children('input').val();
            if (value[value.length - 1] == ','){
                value = value.substring(0, value.length - 1);
            }
            console.log('input wala');
        }
        else if ($this.attr('class').indexOf('create_new') >= 0){
            $sabke_papa.find('.d_list').css({'display':'none'});
            var value = $sabke_papa.children('input').val();
            var target = $this.attr('href');
            console.log(target,value);
            $(target).find('input[type=text]').first().val(value);
            console.log('naya form');
            return 0;
        }
        else{
            var value = $this.text();
            console.log('list wala', $this.attr('class'));
        }
        var r_type = $sabke_papa.data('results');
        console.log($sabke_papa.attr('class'));
        if(r_type == 'instant'){
            $sabke_papa.children('input[name=value]').val(value)
                .nextAll('.form-ajax').trigger('click');
            console.log('1');
        }
        else if(r_type == 'single'){
            $sabke_papa.children('input').first().before('<div class="alert"><a class="close">&times;</a><strong>'+value+'</strong></div>').addClass('hide').next().val(value);

            $sabke_papa.find('.close').on('click', function(){
                $(this).parent('.alert').alert('close');
                $sabke_papa.children('input').first().removeClass('hide').focus();
            });
        }
        else if(r_type == 'multiple'){
            var $d_results = $sabke_papa.children('.d_results');
            var pre_value = $d_results.html();
            $d_results.html(pre_value+'<div class="alert alert_tag"><a href="#" class="close">&times;</a><strong>'+value+'</strong></div>');
            var pre_value_snd = $sabke_papa.children('input').first().next().val();
            if (pre_value_snd != '')
                pre_value_snd += ','
            $sabke_papa.children('input').first().next().val(pre_value_snd + value);
            console.log($sabke_papa.children('input').first().next().val());
            $sabke_papa.find('.close').on('click', function(){
                $(this).parent('.alert_tag').alert('close');
                $sabke_papa.children('input').first().focus();   
            });
            //$sabke_papa.children('input').val('');
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
    $(this).nextAll('.dropdown').find('.d_list').css({'display':'none'});
});
});
$(".d_input").focus(function(){
    var $this = $(this);
    var query = $this.val();
    if(query != '')
        $this.nextAll('.dropdown').find('.d_list').css({'display':'block'});
});
$(".d_input").blur(function(){
    $(this).nextAll('.dropdown').find('.d_list').css({'display':'none'});
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
          $form.find('.form-control').val('');
          if (response.fields){
            for(i=0; i < response.fields.length; i++){
                $papa.find('.'+response.fields[i]).text(response.data[response.fields[i]]);
            }
          }
          if (response.inputs){
            for(i=0; i < response.inputs.length; i++){
                $papa.find('#'+response.inputs[i]).val(response.value[response.inputs[i]]);
                var cl = $papa.find('#'+response.inputs[i]).attr('class');
                if(cl.indexOf('d_input') >= 0){
                    console.log('OKAY')
                    $papa.find('#'+response.inputs[i]).before('<div class="alert"><a href="#" class="close">&times;</a><strong>'+response.value[response.inputs[i]]+'</strong></div>').addClass('hide').next().val(response.value[response.inputs[i]]);

                }
            }
          }
          if (response.elements){
            if (response.prepend){
                for(i=0; i < response.elements.length; i++){
                    $papa.find('.'+response.elements[i]).prepend(response.html[response.elements[i]]);
                }
            console.log('yoho')
            }
            else{
                for(i=0; i < response.elements.length; i++){
                    $papa.find('.'+response.elements[i]).html(response.html[response.elements[i]]);
                }
            }
          }
        },

        error : function(xhr,errmsg,err) {
            $this.next().next().find(".d_list").html("<li><a href='#' class='tag_multiple'>Sorry, unable to fetch results. Try later.</a></li>");
            console.log(errmsg,err);
        }
    });
});

$(".ajax_andar").on('click','.form-ajax-filed',function(event){
    event.preventDefault();
    console.log('file wala');
    var $this = $(this);
    var $papa = $this.closest('.ajax_papa');
    var $form = $this.closest('form');
    var formData = new FormData($form[0]);
    $.ajax({
        url : $form.attr('action'),
        type : $form.attr('method'),
        data : formData,
        cache: false,
        contentType: false,
        processData: false,

        success: function(response){
          $form.find('.form-control').val('');
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
            if (response.prepend){
                for(i=0; i < response.elements.length; i++){
                    $papa.find('.'+response.elements[i]).prepend(response.html[response.elements[i]]);
                }
            console.log('yoho')
            }
            else{
                for(i=0; i < response.elements.length; i++){
                    $papa.find('.'+response.elements[i]).html(response.html[response.elements[i]]);
                }
            }
          }
          $form.find('.close').trigger('click');
        },

        error : function(xhr,errmsg,err) {
            $this.next().next().find(".d_list").html("<li><a href='#' class='tag_multiple'>Sorry, unable to fetch results. Try later.</a></li>");
            console.log(errmsg,err);
        }
    });
});

//home page
var load = true;
var timer = true;
/*$(setInterval(function(){
    timer = true;
    console.log(timer);
},300));*/ // works., implement after performance analysis
$(window).scroll(function() {
    //if (!timer)
        //return;
    //timer = false;
    if (!load)
        return;
    var $this = $(this)
    ,       $pg = $('.paginator');
    var a = $this.scrollTop();
    var b = $this.outerHeight();
    var c = $pg.offset().top;
    var nxt = $pg.data('next_page');
    console.log('scroll', load, a+b-c)
    if((a+b-c) > -10){
        console.log('Yeah')
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

$('.alert .delete').on('click',function(){
    var $this = $(this);
    var from = $this.data('delete');
    var url = '/workplace/delete_tag';
    var del = $this.closest('.alert').children('.del_id').text();
    console.log(del, url);
    $.ajax({
        url : url,
        type : "GET",
        data : { delete: del },

        success: function(response){
            console.log('deleted');
            $this.parent().remove();
        },

        error : function(xhr,errmsg,err) {
            console.log(errmsg,err);
        }
    });
});

$('.ajax_andar').on('click','.a_collapse',function(){
    var $this = $(this);
    var col = $this.siblings('.collapse');
    var text = $this.text();
    var alt = $this.data('alternate');
    if(col.attr('class').indexOf('in') >= 0)
        col.removeClass('in');
    else {
        col.addClass('in');
        col.find('textarea').first().focus();
    }
    $this.text(alt);
    $this.data('alternate',text);
})

$('.fake_btn').click(function(){
    var btn = $(this).data('btn');
    $(btn).trigger('click');
});
$('.img_pre_in input').change(function(){
    var preview = $(this).closest('form').find('.img_pre img');
    var file    = this.files[0];
    var fd = new FormData($('#form_feed')[0]);
    fd.append('file',file);
    console.log(fd,$('#form_feed').serialize())
    var reader  = new FileReader();
    reader.onloadend = function () {
        preview.attr('src', reader.result);
    }
    if (file) {
        reader.readAsDataURL(file);
        preview.closest('.img_pre').removeClass('hide').addClass('show_pre');
    } else {
        preview.attr('src', "");
    }
$(this).closest('form').find('textarea').trigger('focus');
});
$('.img_pre').on('click','.close',function(){
    $(this).closest('form').find('.img_pre').addClass('hide')
        .find('img').attr('src','');
    console.log($(this).closest('form').find('input'));
});

$('.ajax_andar').on('click','.upvote',function(){
    $this = $(this);
    var val = parseInt($(this).closest('.ajax_papa').find('.votes').text());
    if ($this.attr('class').indexOf('done') >= 0){
        $this.removeClass('done').tooltip('hide').attr('data-original-title','Vote Up').tooltip('fixTitle');
        val -= 1;
    }
    else{
        $this.addClass('done').tooltip('hide').attr('data-original-title','Cancel Vote').tooltip('fixTitle');
        val += 1;
    }
    console.log(val)
    $(this).closest('.ajax_papa').find('.votes').text(val);
});

$('.ajax_andar').on('click','.downvote',function(){
    $this = $(this);
    var val = parseInt($(this).closest('.ajax_papa').find('.votes').text());
    if ($this.attr('class').indexOf('done') >= 0){
        $this.removeClass('done').tooltip('hide').attr('data-original-title','Vote Down').tooltip('fixTitle');
        val += 1;
    }
    else{
        $this.addClass('done').tooltip('hide').attr('data-original-title','Cancel Vote').tooltip('fixTitle');
        val -= 1;
    }
    console.log($this.data('original-title'))
    $(this).closest('.ajax_papa').find('.votes').text(val);
});

$('.ajax_andar').on('click','.like',function(){
    $this = $(this);
    var val = parseInt($(this).closest('.ajax_papa').find('.likes').text());
    if ($this.attr('class').indexOf('done') >= 0){
        $this.removeClass('done').tooltip('hide').attr('data-original-title','Like').tooltip('fixTitle');
        val -= 1;
    }
    else{
        $this.addClass('done').tooltip('hide').attr('data-original-title','Unlike').tooltip('fixTitle');
        val += 1;
    }
    console.log(val)
    $(this).closest('.ajax_papa').find('.likes').text(val);
});

$('.answer_form').submit(function(event){
    event.preventDefault();
    var $this = $(this);
    checkValidity();
    var $editor = $this.find('#editor');
    var content = $editor.html();
    $editor.next().val(content);
    $this.find('.form-ajax').trigger('click');
});

$('.article_form button[type="button"]').click(function(event){
    if ($(this).attr('class').indexOf('check_btn') >= 0){
        $(this).next().val('true');
    }
    var $this = $(this).closest('form');
    checkValidity();
    var $editor = $this.find('#editor');
    var content = $editor.html();
    $editor.next().val(content);
    console.log('k')
    $this.find('button[type="submit"]').trigger('click');
});

$('.detail').on({
        'mouseover':function(){
            $(this).children('.detail_opt').removeClass('hide');
        },
        'mouseout':function(){
            $(this).children('.detail_opt').addClass('hide');
        }
    });

    $('.detail_add').on('click',function(event){
        event.preventDefault();
        var $this = $(this)
        var save = $this.data('save');
        var content = $this.data('content');
        var $forms = $('.edit_' + content);
        if (save == 'save'){
            $this.text('Add').data('save','');
            $forms.each(function(){
                $(this).addClass('hide');
            });
        }
        else {
            $this.text('Done').data('save','save');
            $forms.each(function(){
                $(this).removeClass('hide');
            });
        }
    });

    $('.detail_edit').on('click',function(event){
        event.preventDefault();
        var $this = $(this)
        var content = $this.data('content');
        var $content = $('.content_' + content);
        var save = $this.data('save');
        if (save == 'save'){
            console.log(('#'+content),$('#'+content).serialize());
            $content.each(function(){
                var value = $(this).next().val();
                console.log($(this).next().val())
                $(this).text(value).removeClass('hide')
                    .next().addClass('hide');
            });
            $this.text('Edit').data('save','').addClass('form-ajax');
        }
        else {
            $content.each(function(){
                var value = $(this).text();
                console.log(value);
                $(this).addClass('hide')
                    .next().val(value).removeClass('hide');
            });
            $this.text('Save').data('save','save').removeClass('form-ajax');
        }
    });


$('.hover_ajax').on({
    click: function(){
        var $this = $(this);
        var active = $this.data('active');
        var list = $this.find('.hover_box');
        if (active == 'yes') {
            list.css({'display':'block'});
            return;
        };
        $this.data('active','yes');
        var url = $this.data('url');
        console.log(url)
        $.ajax({
            url : url,
            type : 'GET',

            success: function(response){
                console.log(response)
                for(i=0; i < response.elements.length; i++){
                    $this.find('.hover_box').html(response.html[response.elements[i]]);
                    $('.body').on('click',function(){
                        list.css({'display':'none'});
                        $this.data('active','no');
                        count_notifications();
                    })
                }
            },

            error : function(xhr,errmsg,err) {
                $this.nextAll('.dropdown').find(".d_list").html("<li><a href='#' class='tag_multiple'>Sorry, unable to fetch results. Try later.</a></li>");
                console.log(errmsg,err);
            }
        });
        list.css({'display':'block'});
    }
})

$(document).ready(function(){
    //fetches notifications
    count_notifications();

});

function count_notifications(){
    $.ajax({
        url:count_url,
        type: 'GET',

        success: function(response){
            if(response.count)
                $('#notifications .badge').text(response.count);
        },
        error : function(xhr,errmsg,err) {
            console.log(errmsg,err);
        }
    });
}

$('.to_quest').on('click','a',function(){
    var $this = $(this);
    $this.closest('.to_quest').find('input').val('no');
    $this.children('input').val('true');
    $this.parent('form').submit();
});

$('.little_edit').each(function(){
    var $this= $(this);
    var ed_panel = $this.closest('.panel');
    ed_panel.on({'mouseenter':function(){
        $(this).find('.little_edit').removeClass('hide');
    },
    'mouseleave':function(){
        $(this).find('.little_edit').addClass('hide');
    }
    });
});

$('#workplace_info').on({
    'mouseenter': function(){
        $(this).find('.detail_add').removeClass('hide')
    }
})

function checkValidity(){
    console.log('checking')
    var editor = $("#editor");
    var content = editor.html();
    console.log(content);
    var check = true
    ,   pos = -1
    ,   allow_pos = []
    ,   allowed = 0
    ,   att = false;
    var i=0;
    while(i <= content.length){
        var text = content[i];
        if (text == '<'){
            //i may is indexing the start of an opening or a closing tag
            pos = i;
            //the portion of string not yet checked
            var unchecked = content.slice(pos,content.length)
            var nxt = unchecked.search(">");
            var end = pos + nxt;
            //pos indexes the opening of tag
            //end indexes closing of tag
            if (allowed){
                var allowedy = allowed;
                //check wether its a closing tag
                if(content[pos+1] == '/'){
                    //check if its the closing tag of allowed (except 'img')
                    if (content[pos+2] == 'b' || content[pos+2] == 'i' || content[pos+2] == 'u' || content[pos+2] == 'a'){
                        //might be a recognised tag
                        if (content[pos+3] == '>' || content[pos+2] == ' '){
                            //confirmed a/b/i/u
                            allowed--;
                            console.log('allowed ka closing')
                            if (content[pos+2] == 'a')
                                var att = 'href';
                        }
                        else if (content[pos+3] == 'r'){
                            //might be 'br'
                            if (content[pos+4] == '>' || content[pos+4] == ' '){
                                //confirmed br
                                allowed--;
                                console.log('allowed ka closing')
                            }
                        }
                    }
                }
            }
            else {
                var allowedy = allowed;
                //check for allowed tags
                if (content[pos+1] == 'b' || content[pos+1] == 'i' || content[pos+1] == 'u' || content[pos+1] == 'a'){
                    //might be a recognised tag
                    if (content[pos+2] == '>' || content[pos+2] == ' '){
                        //confirmed a/b/i/u
                        allowed++;
                        if (content[pos+1] == 'a')
                            var att = 'href';
                    }
                    else if (content[pos+2] == 'r' || content[pos+2] == 'm'){
                        //might be 'br'/'img'
                        if (content[pos+2] == '>' || content[pos+2] == ' '){
                            //confirmed br
                            allowed++;
                        }
                        else if (content[pos+3] == 'g'){
                            //might be 'img'
                            if (content[pos+4] == '>' || content[pos+4] == ' '){
                                //confirmed img
                                allowed++;
                                var att = 'src';
                            }
                        }
                    }
                }
            }
            if (allowedy == allowed) {
                var part1 = content.slice(0,pos);
                //console.log(part1);
                var part2 = content.slice(end+1,content.length);
                //console.log(part2);
                content = part1 + part2;
                i--;
            }
            else {
                allow_pos[allowed] = pos;
                console.log(allowed,allow_pos[allowed]);
            }
        }
        i++;
    }
    console.log(content, allowed);
    editor.html(content);
    while (allowed) {
        console.log('ego adha aa giya');
        pos = allow_pos[allowed-1];
        var nxt = unchecked.search(">");
        var end = pos + nxt;
        var part1 = content.slice(0,pos);
        //console.log(part1);
        var part2 = content.slice(end+1,content.length);
        //console.log(part2);
        content = part1 + part2;
        allowed--;
    }
}

$('#editor').on({
    'focus': function(){
        if ($(this).attr('class') == 'empty'){
            $(this).html('').removeClass('empty');
            //setInterval(checkValidity, 5000);
        }
        //checkValidity();
    },
    'keyup': function(event){
        if (event.key == 'v'){
            checkValidity();
        }
    },
    'blur': function(){
        console.log('blured')
        if ($(this).html() == ''){
            $(this).html('<div class="text-muted">The Awesome Body goes here ...</div>').addClass('empty');
        }
        //checkValidity();
    }
});