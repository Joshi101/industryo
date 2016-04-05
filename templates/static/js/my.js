/*
 * Javascript functions for CoreLogs.com
 *
 * Date: 22-06-2015
 */

/* global parameters */
var top_nav_width, win_width, win_height, foot_height;

/* function to initialize some global parameters */
function measure() {
    top_nav_width = $('#top_nav').outerHeight(true);
    win_width = $(window).width();
    win_height = $(window).height();
    foot_height = $('footer').outerHeight(true);
    body_slide();
}

/* function to auto adjust top margin for the body */
function body_slide() {
    console.log(win_height, top_nav_width, foot_height)
    $('.body').stop().animate({
        //'margin-top': top_nav_width,
        'min-height': (win_height - top_nav_width)
    });
}

/* call body_slide when the window loads or resizes */
$(measure);
$(window).on('resize', measure);


/* handling input for dynamiac search inputs */
function doneTyping() {
    d_on = true;
    var $this = d_this;
    var $d_search = $this.closest('.d_search');
    var query = $this.val(),
        search = "/search" + $this.data('search') + "/";
    var type = $d_search.find('.d_type').val();
    console.log(type);
    if (!type)
        type = '';
    if (query.length < 3){
        console.log('e to chotu h');
        d_on = false;
    }
    if (d_on) {
        //d_on = false;
        $d_search.find('.create').addClass('hide');
        $this.siblings('.form-control-feedback').children('.fback_wait').removeClass('hide');
        console.log(query, search, type);
        $.ajax({
            url: search,
            type: "GET",
            data: {
                the_query: query,
                the_type: type
            },
            success: function(result) {
                //d_on = true;
                //console.log(result);
                $d_search.find('.dropdown')
                    .find(".d_list").html(result);
                $this.siblings('.form-control-feedback').children('.fback_wait').addClass('hide');
                $d_search.find('.create').removeClass('hide');
            },
            error: function(xhr, errmsg, err) {
                //d_on = true;
                $d_search.find('.dropdown')
                    .find(".d_list").html("<li class='list-group-item list-group-item-warning'>Sorry, unable to fetch results. Try later.</li>");
                console.log(errmsg, err);
                $this.siblings('.form-control-feedback').children('.fback_wait').addClass('hide');
            }
        });
    }
    if (query !== ''){
        $d_search.find('.dropdown').addClass('open');
        $d_search.find('.d_menu').css('z-index','1000');
    }
}

var typingTimer; //timer identifier
var doneTypingInterval = 500; //time in ms
var d_this;
var d_on = true;

function d_input_remove_error($this,sign,msg){
    if(sign){
        $this.closest('.d_search').removeClass('has-error');
        $this.closest('.form-group').find('.fback_warn').addClass('hide');
    }
    if(msg)
        $this.closest('.form-group').find('.fback_msg').addClass('hide');    
}
function d_input_show_error($this,sign,msg){
    if(sign){
        $this.closest('.d_search').addClass('has-error');
        $this.closest('.form-group').find('.fback_warn').removeClass('hide');
    }
    if(msg)
        $this.closest('.form-group').find('.fback_msg').removeClass('hide');
}


$('body').on('keydown', '.d_input', function(event) {
    $(".d_input").on('blur', d_input_blur);
    var $this = $(this);
    d_input_remove_error($this,true,false);
    d_this = $this;
    $d_search = $this.closest('.d_search');
    if (event.keyCode == '13') {
        event.preventDefault();
        if ($d_search.find('.dropdown').attr('class').indexOf('open') >= 0){
            $d_search.find('.dropdown').find('.d_menu').find('.option').first().trigger('click');
        }
    }
    else {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(doneTyping, doneTypingInterval);
    }
});


$('body').on('click', '.d_search .one_value .close', function() {
    $d_search = $(this).closest('.d_search');
    $d_search.find('.d_input').removeClass('hide').focus();
    $d_search.find('.d_value').val('');
    $(this).closest('.one_value').addClass('hide');
});

$("body").on('click', '.one_list .option', function(event) {
    //aj_search($(this));
    d_check = false;
    var $this = $(this),
        $d_search = $this.closest('.d_search'),
        value = $this.find('.option_value').text();
    d_input_remove_error($this,true,true);
    $d_search.find('.d_value').val(value).trigger('change');
    $d_search.find('.d_input').val(value);
    
    $this.closest('.dropdown').removeClass('open');
    $d_search.find('.d_menu').css('z-index','auto');
});

$('body').on('click', '.many_list .option', function(event) {
    d_check = false;
    var $this = $(this),
        $d_search = $this.closest('.d_search'),
        value = $this.find('.option_value').text();
    d_input_remove_error($this,true,true);
    var pre_value = $d_search.find('.d_value').val();        
    if (pre_value !== '')
        pre_value += ',';
    $d_search.find('.d_value').val(pre_value + value).trigger('change');
    console.log('asd');
    $d_search.find('.input_tags').append('<div class="tag"><a class="close">&times;</a><span class="value">' + value +'</span></div>');
    $this.closest('.dropdown').removeClass('open');
    $d_search.find('.d_menu').css('z-index','auto');
    $('.d_search').find('.d_input').val('');
});

$('body').on('click', '.d_search .create', function(){
    d_check = false;
    console.log('ab create to hoga');
    var $d_search = $(this).closest('.d_search'),
        value = $d_search.find('.d_input').val();
    d_input_remove_error($(this),true,true);
    var pre_value = $d_search.find('.d_value').val();
    if (pre_value !== '')
        pre_value += ',';
    $d_search.find('.d_value').val(pre_value + value).trigger('change');
    $d_search.find('.input_tags').append('<div class="tag"><a class="close">&times;</a><span class="value">' + value +'</span></div>');
    $(this).closest('.dropdown').removeClass('open');
    $d_search.find('.d_menu').css('z-index','auto');
    $('.d_search').find('.d_input').val('');
});

$('body').on('click', '.d_search .create_new', function(){
    var $d_search = $(this).closest('.d_search'),
        value = $d_search.find('.d_input').val();
    var create = $(this).attr('href');
    var $create = $(create);
    $create.find('input[name=name]').val(value);
    var $form = $create.find('form');
    $create.on('click','button[type=submit]', function(){
        console.log('bind hua h');
        d_check = false;
        d_input_remove_error($d_search.find('.d_input'),true,true);
        $d_search.find('.d_value').val(value);
        $d_search.find('.one_value').removeClass('hide')
            .children('span').text(value);
        $d_search.find('.d_input').addClass('hide');
        $d_search.find('.dropdown').removeClass('open');
        $d_search.find('.d_menu').css('z-index','auto');
    });
});

$('body').on('click','.input_tags .tag .close', function(){
    var tag = $(this).closest('.tag');
    value = tag.find('.value').text();
    var $d_search = $(this).closest('.d_search');
    var pre_value = $d_search.find('.d_value').val();
    i1 = pre_value.indexOf(value);
    i2 = i1 + value.length;
    if(i1!==0)
        i1 -= 1;
    val1 = pre_value.slice(0, i1);
    val2 = pre_value.slice(i2);
    console.log(i1,i2,val1+val2);
    $d_search.find('.d_value').val(val1+val2);
    tag.remove();
});


    function aj_search($this) {
        var $sabke_papa = $this.closest('.d_search'),
            value;
        if ($this.attr('class') == 'create') {
            value = $sabke_papa.children('input').val();
            if (value[value.length - 1] == ',') {
                value = value.substring(0, value.length - 1);
            }
            console.log('input wala');
        } else if ($this.attr('class').indexOf('create_new') >= 0) {
            $sabke_papa.find('.d_list').css({
                'display': 'none'
            });
            value = $sabke_papa.children('input').val();
            var target = $this.attr('href');
            console.log(target, value);
            $(target).find('input[type=text]').first().val(value);
            console.log('naya form');
            return 0;
        } else {
            value = $this.find('span').first().text();
            console.log('list wala', value);
        }
        var r_type = $sabke_papa.data('results');
        console.log($sabke_papa.attr('class'));
        if (r_type == 'instant') {
            $sabke_papa.children('input[name=value]').val(value)
                .nextAll('.form-ajax').trigger('click');
            console.log('1');
        } else if (r_type == 'single') {
            $sabke_papa.children('input').first().before('<div class="alert"><a class="close">&times;</a><strong>' + value + '</strong></div>').addClass('hide').next().val(value);

            $sabke_papa.on('click', '.close', function() {
                $(this).parent('.alert').alert('close');
                $sabke_papa.children('input').first().removeClass('hide').focus();
            });
        } else if (r_type == 'multiple') {
            var $d_results = $sabke_papa.children('.d_results');
            var pre_value = $d_results.html();
            $d_results.html(pre_value + '<div class="alert alert_tag"><a class="close">&times;</a><strong>' + value + '</strong></div>');
            var pre_value_snd = $sabke_papa.children('input').first().next().val();
            if (pre_value_snd !== '')
                pre_value_snd += ',';
            $sabke_papa.children('input').first().next().val(pre_value_snd + value);
            console.log($sabke_papa.children('input').first().next().val());
            $sabke_papa.find('.close').on('click', function() {
                $(this).parent('.alert_tag').alert('close');
                $sabke_papa.children('input').first().focus();
            });
            //$sabke_papa.children('input').val('');
        }
    }


var d_check = true;

function d_input_blur() {
if (d_check){
    $(this).closest('.d_search').find('.dropdown').removeClass('open');
    $d_search.find('.d_menu').css('z-index','auto');
    console.log('okkk');
    var $this = $(this);
    var value = $(this).closest('.d_search').find('.d_value').val();
    if (!value){
        /*d_input_show_error($this,true,true);*/
    }
}
}

/*$(".body").on('blur', '.d_input', d_input_blur);*/

$("body").on('mouseover', '.d_menu .dropdown-menu', function() {
    console.log('lop')
    $(".d_input").off('blur');
});
$('body').on('mouseout', '.d_menu .dropdown-menu', function() {
    $(".d_input").on('blur', d_input_blur);
});

$("body").on('focus', '.d_input', function() {
    d_check = true;
    var $this = $(this);
    var query = $this.val();
    if (query !== ''){
        $(this).closest('.d_search').find('.dropdown').addClass('open');
        $d_search.find('.d_menu').css('z-index','1000');
    }
});

// function to submit form ajaxly
$("body").on('click', '.form-ajax', function(event) {
    event.preventDefault();
    console.log('default nahi');
    var $this = $(this);
    var $papa = $this.closest('.ajax_papa');
    var $form = $this.closest('form');
    console.log($form.serialize());
    $.ajax({
        url: $form.attr('action'),
        type: $form.attr('method'),
        data: $form.serialize(),

        success: function(response) {
            $form.find('.form-control').val('');
            if (response.fields) {
                for (i = 0; i < response.fields.length; i++) {
                    $papa.find('.' + response.fields[i]).text(response.data[response.fields[i]]);
                }
            }
            if (response.inputs) {
                for (i = 0; i < response.inputs.length; i++) {
                    $papa.find('#' + response.inputs[i]).val(response.value[response.inputs[i]]);
                    var cl = $papa.find('#' + response.inputs[i]).attr('class');
                    /*if (cl.indexOf('d_input') >= 0) {
                        console.log('OKAY');
                        $papa.find('#' + response.inputs[i]).before('<div class="alert"><a class="close">&times;</a><strong>' + response.value[response.inputs[i]] + '</strong></div>').addClass('hide').next().val(response.value[response.inputs[i]]);
                    }*/
                }
            }
            if (response.elements) {
                if (response.prepend) {
                    for (i = 0; i < response.elements.length; i++) {
                        $papa.find('.' + response.elements[i]).prepend(response.html[response.elements[i]]);
                        console.log(response.elements[i], response.html[response.elements[i]]);
                    }
                    console.log('yoho');
                } else {
                    for (i = 0; i < response.elements.length; i++) {
                        $papa.find('.' + response.elements[i]).html(response.html[response.elements[i]]);
                    }
                }
            }
        },

        error: function(xhr, errmsg, err) {
            $this.next().next().find(".d_list").html("<li><a class='tag_multiple'>Sorry, unable to fetch results. Try later.</a></li>");
            console.log(errmsg, err);
        }
    });
});

$(".ajax_andar").on('click', '.form-ajax-filed', function(event) {
    event.preventDefault();
    console.log('file wala');
    var $this = $(this);
    var $papa = $this.closest('.ajax_papa');
    var $form = $this.closest('form');
    var formData = new FormData($form[0]);
    console.log(formData)
    $.ajax({
        url: $form.attr('action'),
        type: $form.attr('method'),
        data: formData,
        cache: false,
        contentType: false,
        processData: false,

        success: function(response) {
            console.log('the form with the file succesfully submited')
            $form.find('.form-control').val('');
            if (response.fields) {
                for (i = 0; i < response.fields.length; i++) {
                    $papa.find('.' + response.fields[i]).text(response.data[response.fields[i]]);
                }
            }
            if (response.inputs) {
                for (i = 0; i < response.inputs.length; i++) {
                    $papa.find('#' + response.inputs[i]).val(response.value[response.inputs[i]]);
                }
            }
            if (response.elements) {
                if (response.prepend) {
                    for (i = 0; i < response.elements.length; i++) {
                        $papa.find('.' + response.elements[i]).prepend(response.html[response.elements[i]]);
                    }
                    console.log('yoho');
                } else {
                    for (i = 0; i < response.elements.length; i++) {
                        $papa.find('.' + response.elements[i]).html(response.html[response.elements[i]]);
                    }
                }
            }
            $form.find('.close').trigger('click');
            $form.find('.index').val(parseInt($form.find('.index').val()) + 1);
            $form.closest('.modal').modal('hide');
            lazyImages();
        },

        error: function(xhr, errmsg, err) {
            console.log(errmsg, err);
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
    var $this = $(this),
        $pg = $('.paginator');
    if ($pg.length) {
        var a = $this.scrollTop();
        var b = $this.outerHeight();
        var c = $pg.offset().top;
        var nxt = $pg.data('next_page');
        //console.log('scroll', load, a + b - c);
        if ((a + b - c) > -10) {
            console.log('Yeah');
            load = false;
            var pg_url = $pg.data('url');
            console.log(pg_url);
            if (!pg_url){
                pg_url = window.location;
            }
            $.ajax({
                url: pg_url,
                type: "GET",
                data: {
                    page: nxt
                },

                success: function(response) {
                    nxt++;
                    $pg.data('next_page', nxt);
                    var $pg_parent = $pg.parent();
                    var height_before = $pg.parent().height();
                    /*$pg_parent.css({
                        'height': height_before,
                        'overflow-y': 'hidden'
                    });*/
                    $pg.before(response);
                    $('[data-toggle="tooltip"]').tooltip();
                    lazyImages();
                    /*var height_after = $pg.parent()[0].scrollHeight;
                    $pg_parent.animate({
                        'height': height_after
                    }, 500);
                    console.log(height_after,height_before);*/
                    load = true;
                },

                error: function(xhr, errmsg, err) {
                    console.log(errmsg, err);
                    $pg.before("<h5 id='last_feed' class='text-center text-muted'>Looks like you've reached the beginning of your history at CoreLogs :)</h5>");
                    $pg.addClass('hide');
                }
            });
        }
    }
});

//profile page
$('#img_profile_box').on({
    mouseover: function() {
        $('#img_upload').stop().animate({
            'height': '28px',
            'top': '-49px',
            'padding': '4px 0px'
        });
        $('#img_upload').on('click', function() {
            $('#img_upload').stop().animate({
                'height': '0px',
                'top': '-20px',
                'padding': '0px'
            });
        });
    },
    mouseout: function() {
        $('#img_upload').stop().animate({
            'height': '0px',
            'top': '-20px',
            'padding': '0px'
        });
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
$('#form_feed').on('focus', 'textarea', function() {
    var $this = $(this);
    $this.attr('rows', '3');
    $this.removeClass('seamless_l');
    $this.parent().find('.input-group-addon').hide();
    $this.closest('form').find('.textarea_bottom').removeClass('hide');
    autosize.update($this);
});
$('#form_feed textarea').on('blur', function() {
    var $this = $(this);
    $this.attr('rows', '1');
    $this.addClass('seamless_l');
    $this.closest('form').find('.textarea_bottom').addClass('hide');
    autosize.update($this);
    $this.parent().find('.input-group-addon').show();
});
$('#form_feed .btn, .img_pre').on({
    mouseover: function() {
        $('#form_feed textarea').off('blur');
    },
    mouseout: function() {
        $('#form_feed textarea').on('blur', function() {
            var $this = $(this);
            $this.attr('rows', '1');
            $this.addClass('seamless_l');
            $this.closest('form').find('.textarea_bottom').addClass('hide');
            autosize.update($this);
            $this.parent().find('.input-group-addon').show();
        });
    }
});

$('body').on('click', '.delete', function() {
    var $this = $(this);
    var from = $this.data('delete');
    var url = '/workplace/delete_tag';
    var del = $this.closest('.alert').find('.del_id').text();
    if(!del){
        del = $this.closest('.tag_short').find('.del_id').text();
    }
    console.log(del, url);
    $.ajax({
        url: url,
        type: "GET",
        data: {
            delete: del
        },

        success: function(response) {
            console.log('deleted');
            $this.tooltip("hide").parent().remove();

        },

        error: function(xhr, errmsg, err) {
            console.log(errmsg, err);
        }
    });
});

$('.ajax_andar').on('click', '.a_collapse', function() {
    var $this = $(this);
    var col = $this.siblings('.collapse');
    var text = $this.text();
    var alt = $this.data('alternate');
    var hide = $this.data('hide');
    if (hide){
        $this.addClass('hidden');
    }
    if (col.attr('class').indexOf('in') >= 0)
        col.removeClass('in');
    else {
        col.addClass('in');
        col.find('.form-control').first().focus();
    }
    if (alt){
        console.log(alt)
        $this.text(alt);
        $this.data('alternate', text);
    }
});

$('body').on('click', '.fake_btn', function() {
    var btn = $(this).data('btn');

    $(btn).trigger('click');
});


// variable to index the no.of images uploaded
var img_index = [0, 0, 0];

function check_img_index() {
    var i = img_index.indexOf(0);
    if (i == -1)
        i = 3;
    return i;
}

function send_img() {
    var i = check_img_index();
    console.log(i);
    if (i > 2) {
        console.log('premature exit');
        return 0;
    }
    img_index[i] = 1;
    var free = check_img_index();
    console.log('free: ', free);
    var img_pre = '<div class="alert"><a class="close">&times;</a><img width="90%" src="" alt=""></div>';
    var input = '<span title="Add Image" data-toggle="tooltip" data-placement="left" class="btn btn-default btn-file glyphicon glyphicon-camera input-group-addon seamless_r img_pre_in"><input id="id_image_' + free + '" type="file" name="image' + free + '"></span>';
    if ($(this).closest('form').find('.img_pre .alert').length <= i) {
        console.log('alert added', $(this).closest('form').find('.img_pre .alert').length);
        $(this).closest('form').find('.img_pre').append(img_pre);
    } else {
        console.log(i, $(this).closest('form').find('.img_pre .alert').eq(i).css('display'));
        $(this).closest('form').find('.img_pre .alert').eq(i).show();
    }
    var preview = $(this).closest('form').find('.img_pre img').eq(i);
    var file = this.files[0];
    var fd = new FormData($('#form_feed')[0]);
    fd.append('file' + i, file);
    console.log(fd, $('#form_feed').serialize());
    var reader = new FileReader();
    reader.onloadend = function() {
        preview.attr('src', reader.result).closest('.alert').show();
    };
    if (file) {
        reader.readAsDataURL(file);
        preview.closest('.img_pre').removeClass('hide').addClass('show_pre');
        console.log('img_pre showing');
        $(this).closest('form').find('.img_pre').data('index', (i + 1));
        $(this).addClass('hide');
        $(this).parent().addClass('hide').after(input);
        $('#id_image_' + (i + 1)).change(send_img);
        $(this).closest('form').find('.fake_btn').data('btn', '#id_image_' + free);
        console.log($(this).closest('form').find('.img_pre').data('index'));
    } else {
        preview.attr('src', "");
    }
    $(this).closest('form').find('textarea').trigger('focus');
}

$('.img_pre_in input').change(send_img);

$('.img_pre').on('click', '.close', function() {
    var im = $(this).closest('.alert').index();
    img_index[im] = 0;
    var free = check_img_index();
    console.log('deleted. next free: ', free);
    $(this).closest('form').find('.fake_btn').attr('data-btn', '#id_image_' + free);
    //$(this).closest('form').find('#id_image_'+im).parent().remove();
    $(this).closest('form').find('#id_image_' + im).parent().html('<input id="id_image_' + im + '" type="file" name="image' + im + '">');
    $(this).closest('form').find('#id_image_' + im).change(send_img);
    /*var i = $(this).closest('form').find('.img_pre').data('index');
    $(this).closest('form').find('#id_image_'+(i-1)).parent().nextAll().each(function() {
        var old_i = $(this).children().attr('id').slice(9);
        console.log(old_i);
        $(this).children().attr('id','id_image'+(old_i-1));
        $(this).children().attr('name','image'+(old_i-1));
    });*/
    //$(this).closest('form').find('#id_image_'+(i-1)).parent().remove();
    /*if ($(this).closest('form').find('.img_pre alert').length < 1){
        $(this).closest('form').find('.img_pre').addClass('hide');
    }*/
    //$(this).closest('form').find('.img_pre').data('index',(i-1));
    $(this).closest('form').find('.alert').eq(im).hide();
    console.log($(this).closest('form').find('input'));
});

$('.ajax_andar').on('click', '.upvote', function() {
    $this = $(this);
    console.log($(this))
    var val = parseInt($(this).closest('.ajax_papa').find('.votes').text());
    if ($this.attr('class').indexOf('done') >= 0) {
        $this.removeClass('done').tooltip('hide').attr('data-original-title', 'Vote Up').tooltip('fixTitle');
        val -= 1;
    } else {
        $this.addClass('done').tooltip('hide').attr('data-original-title', 'Cancel Vote').tooltip('fixTitle');
        val += 1;
    }
    console.log(val, $(this).closest('.ajax_papa').find('.votes').text());
    $(this).closest('.ajax_papa').find('.votes').text(val);
});

$('.ajax_andar').on('click', '.downvote', function() {
    $this = $(this);
    var val = parseInt($(this).closest('.ajax_papa').find('.votes').text());
    if ($this.attr('class').indexOf('done') >= 0) {
        $this.removeClass('done').tooltip('hide').attr('data-original-title', 'Vote Down').tooltip('fixTitle');
        val += 1;
    } else {
        $this.addClass('done').tooltip('hide').attr('data-original-title', 'Cancel Vote').tooltip('fixTitle');
        val -= 1;
    }
    console.log($this.data('original-title'));
    $(this).closest('.ajax_papa').find('.votes').text(val);
});

$('.ajax_andar').on('click', '.like', function() {
    $this = $(this);
    var val = parseInt($(this).closest('.ajax_papa').find('.likes').text());
    if ($this.attr('class').indexOf('done') >= 0) {
        $this.removeClass('done').tooltip('hide').attr('data-original-title', 'Like').tooltip('fixTitle');
        val -= 1;
    } else {
        $this.addClass('done').tooltip('hide').attr('data-original-title', 'Unlike').tooltip('fixTitle');
        val += 1;
    }
    console.log(val);
    $(this).closest('.ajax_papa').find('.likes').text(val);
});

$('.answer_form button[type="button"]').click(function(event) {
    if ($(this).attr('class').indexOf('check_btn') >= 0) {
        $(this).next().val('true');
    }
    var $this = $(this).closest('form');
    /*checkValidity();*/
    /*var $editor = $this.find('#editor');
    var content = $editor.html();
    $editor.next().val(content);*/
    $this.find('.form-ajax-filed').trigger('click');
    console.log('yaha hain bhaiya');
    $('#write_answer').trigger('click');
    /*$editor.html('');*/
});

$('.article_form button[type="button"]').click(function(event) {
    if ($(this).attr('class').indexOf('check_btn') >= 0) {
        $(this).next().val('true');
    }
    var $this = $(this).closest('form');
    //checkValidity();
    var $editor = $this.find('#editor');
    var content = $editor.html();
    //$editor.next().val(content);
    console.log('k');
    $this.find('button[type="submit"]').trigger('click');
});

$('.detail').on({
    'mouseover': function() {
        $(this).children('.detail_opt').removeClass('hide');
    },
    'mouseout': function() {
        $(this).children('.detail_opt').addClass('hide');
    }
});

$('body').on('click', '.detail_add', function(event) {
    event.preventDefault();
    console.log('clickku')
    var $this = $(this);
    console.log()
    var save = $this.attr('data-save');
    var content = $this.data('content');
    var taggy = $this.data('taggy');
    console.log(save,content,taggy)
    var $forms = $('.edit_' + content);
    if (save == 'save') {
        console.log('save hoga');
        $this.text('Add').attr('data-save', '');
        if (taggy == 'yes') {
            console.log($this.prev().text());
            $this.siblings('span').removeClass('hide').siblings('.tag_short').addClass('hide').children('.close');
        }
        $forms.each(function() {
            $(this).addClass('hide');
        });
        ajax_form($(this).siblings('form'));
    } else {
        $this.text('Done').attr('data-save', 'save');
        if (taggy == 'yes') {
            $this.siblings('span').addClass('hide').siblings('.tag_short').removeClass('hide').children('.close');
        }
        $forms.each(function() {
            $(this).removeClass('hide');
        });
    }
});


$('body').on('click', '.detail_edit', function(event) {
    event.preventDefault();
    console.log('oki')
    var $this = $(this);
    var content = $this.data('content');
    var $content = $('.content_' + content);
    var save = $this.data('save');
    if (save == 'save') {
        console.log('abhi data-save "" hoga or agli baar daba k userwa edit krega')
        console.log(('#' + content), $('#' + content).serialize());
        $content.each(function() {
            var value = $(this).next().val();
            console.log($(this).next().val());
            $(this).text(value).removeClass('hide')
                .next().addClass('hide');
        });
        $this.text('Edit').data('save', '').removeClass('form-ajax');
    } else {
        console.log('abhi data-save save hoga or agli baar dabaenge to form submit hoga')
        $content.each(function() {
            var value = $(this).text();
            console.log(value);
            $(this).addClass('hide')
                .next().val(value).removeClass('hide');
        });
        $this.text('Save').data('save', 'save').addClass('form-ajax');
    }
});


$('.hover_ajax').on({
    click: function() {
        var $this = $(this);
        var active = $this.data('active');
        var list = $this.find('.hover_box');
        if (active == 'yes') {
            list.css({
                'display': 'block'
            });
            return;
        }
        //$this.data('active', 'yes');
        var url = $this.data('url');
        console.log(url);
        $.ajax({
            url: url,
            type: 'GET',

            success: function(response) {
                console.log(response);
                for (i = 0; i < response.elements.length; i++) {
                    $this.find('.hover_box').html(response.html[response.elements[i]]);
                    /*$('.body').on('click', function() {
                        $this.find('.dropdown').removeClass('open');
                        //$this.data('active', 'no');
                        //count_notifications();
                        $('.body').off('click');
                    });*/
                }
            },

            error: function(xhr, errmsg, err) {
                $this.nextAll('.dropdown').find(".d_list").html("<li><a class='tag_multiple'>Sorry, unable to fetch results. Try later.</a></li>");
                console.log(errmsg, err);
            }
        });
        /*list.css({
            'display': 'block'
        });*/
        //$this.find('.dropdown').addClass('open');
    }
});

$(document).ready(function() {
    //fetches notifications
    count_notifications();
    count_messages();

});

function count_notifications() {
    $.ajax({
        url: 'count_notify',
        type: 'GET',

        success: function(response) {
            if (response.count)
                $('#notifications .badge').text(response.count);
        },
        error: function(xhr, errmsg, err) {
            console.log(errmsg, err);
        }
    });
}

function count_messages() {
    $.ajax({
        url: '/messages/check/',
        type: 'GET',

        success: function(response) {
            console.log(response.count, 'itna message')
            if (response.count)
                $('#messages .badge').text(response.count);
        },
        error: function(xhr, errmsg, err) {
            console.log(errmsg, err);
        }
    });
}

$('.ajax_andar').on('click', '.to_quest a', function() {
    var $this = $(this);
    $this.closest('.to_quest').find('input').val('no');
    $this.children('input').val('true');
    $this.parent('form').submit();
});

$('.little_edit').each(function() {
    var $this = $(this);
    var ed_panel = $this.closest('.panel');
    ed_panel.on({
        'mouseenter': function() {
            $(this).find('.little_edit').removeClass('hide');
        },
        'mouseleave': function() {
            $(this).find('.little_edit').addClass('hide');
        }
    });
});

$('#info_head').on({
    'mouseenter': function() {
        $(this).find('.detail_add').each(function() {
            $(this).removeClass('hide');
        });
    },
    'mouseleave': function() {
        $(this).find('.detail_add').each(function() {
            $(this).addClass('hide');
        });
    }
});

function checkValidity() {
    console.log('checking');
    var editor = $("#editor");
    var content = editor.html();
    console.log(content);
    var check = true,
        pos = -1,
        allow_pos = [],
        allowed = 0,
        att = false;
    var i = 0;
    while (i <= content.length) {
        var text = content[i];
        if (text == '<') {
            //i may is indexing the start of an opening or a closing tag
            pos = i;
            //the portion of string not yet checked
            var unchecked = content.slice(pos, content.length);
            var nxt = unchecked.search(">");
            var end = pos + nxt;
            //pos indexes the opening of tag
            //end indexes closing of tag
            var allowedy = allowed;
            if (allowed) {
                //check wether its a closing tag
                if (content[pos + 1] == '/') {
                    //check if its the closing tag of allowed (except 'img')
                    if (content[pos + 2] == 'b' || content[pos + 2] == 'i' || content[pos + 2] == 'u' || content[pos + 2] == 'a' || content[pos + 2] == 'l' || content[pos + 2] == 'o') {
                        //might be a recognised tag
                        if (content[pos + 3] == '>') {
                            //confirmed a/b/i/u
                            allowed--;
                            console.log('allowed ka closing', content[pos + 2], pos, allowed, allowedy);
                            if (content[pos + 2] == 'a')
                                att = 'href';
                        } else if (content[pos + 3] == 'r' || content[pos + 3] == 'l' || content[pos + 3] == 'i') {
                            //might be br/ul/ol/li
                            if (content[pos + 4] == '>') {
                                //confirmed br/ul/ol/li
                                allowed--;
                                console.log('allowed ka closing');
                            }
                        }
                    }
                }
            }
            if (!allowedy || (allowedy == allowed)) {
                console.log('yahi na', content[pos], pos);
                allowedy = allowed;
                //check for allowed tags
                if (content[pos + 1] == 'b' || content[pos + 1] == 'i' || content[pos + 1] == 'u' || content[pos + 1] == 'a' || content[pos + 1] == 'l' || content[pos + 2] == 'o') {
                    //might be a recognised tag
                    console.log('lvl 1 a', content[pos + 2]);
                    if (content[pos + 2] == '>' || content[pos + 2] == ' ') {
                        //confirmed a/b/i/u
                        console.log('lvl 2 a');
                        allowed++;
                        if (content[pos + 1] == 'a')
                            att = 'href';
                    } else if (content[pos + 2] == 'r' || content[pos + 2] == 'm' || content[pos + 2] == 'l' || content[pos + 2] == 'i') {
                        //might be 'br/ul/ol/li/img
                        console.log('lvl 2 b');
                        if (content[pos + 3] == '>' || content[pos + 3] == ' ') {
                            //confirmed br/ul/ol/li
                            console.log('lvl 3 a');
                            allowed++;
                        } else if (content[pos + 3] == 'g') {
                            //might be 'img'
                            console.log('lvl 3 b');
                            if (content[pos + 4] == '>' || content[pos + 4] == ' ') {
                                //confirmed img
                                console.log('lvl 4 a');
                                allowed++;
                                att = 'src';
                            }
                        }
                    }
                }
            }
            if (allowedy == allowed) {
                console.log(pos, end);
                var part1 = content.slice(0, pos);
                //console.log(part1);
                var part2 = content.slice(end + 1, content.length);
                //console.log(part2);
                content = part1 + part2;
                i--;
            } else {
                allow_pos[allowed] = pos;
                console.log(allowed, allow_pos[allowed]);
            }
        }
        i++;
    }
    console.log(content, allowed);
    editor.html(content);
    while (allowed) {
        console.log('ego adha aa giya');
        pos = allow_pos[allowed - 1];
        var nxt = unchecked.search(">");
        var end = pos + nxt;
        var part1 = content.slice(0, pos);
        //console.log(part1);
        var part2 = content.slice(end + 1, content.length);
        //console.log(part2);
        content = part1 + part2;
        allowed--;
    }
}


$(document).ready(function() {
    var ctrlDown = false;
    var ctrlKey = 17,
        vKey = 86,
        cKey = 67;
    $(document).keydown(function(e) {
        if (e.keyCode == ctrlKey) ctrlDown = true;
    }).keyup(function(e) {
        if (e.keyCode == ctrlKey) ctrlDown = false;
    });

    $('#editor').on({
        'focus': function() {
            if ($(this).attr('class') == 'empty') {
                $(this).html('').removeClass('empty');
                //setInterval(checkValidity, 5000);
            }
            //checkValidity();
        },
        'keyup': function(event) {
            if (ctrlDown && event.keyCode == 86) {
                checkValidity();
            }
        },
        'blur': function() {
            console.log('blured');
            if ($(this).html() === '') {
                $(this).html('<div class="text-muted">The Awesome Body goes here ...</div>').addClass('empty');
            }
            //checkValidity();
        }
    });


});

var nones = $('span.none');
if (nones.siblings('span').length) {
    nones.addClass('hide');
}

$('.d_results').on('click', '.alert_tag .close', function() {
    $(this).parent('.alert_tag').alert('close');
    //$(sabke_papa).children('input').first().focus();
});

$('.d_results').on('close.bs.alert', '.alert_tag', function() {
    console.log('check');
    var all_val = $(this).closest('.d_search').find('input[name=tags]').val();
    var this_val = $(this).find('strong').text();
    var pos = all_val.search(this_val);
    var pos_end = pos + this_val.length - 1;
    if (all_val[pos_end + 1] == ',') {
        console.log(pos, pos_end);
        pos_end += 1;
        console.log(pos, pos_end);
    } else if (all_val[pos - 1] == ',') {
        console.log(pos, pos_end);
        pos -= 1;
        console.log(pos, pos_end);
    }
    var part1 = all_val.slice(0, pos);
    var part2 = all_val.slice(pos_end + 1, all_val.length);
    all_val = $(this).closest('.d_search').find('input[name=tags]').val(part1 + part2);
    console.log(all_val, this_val, part1, part2);
});

$('.answers').on('click', '.edit_ans', function() {
    var editor = $('#editor');
    var $this = $(this);
    var id = $this.siblings('span').text();
    var ans = $this.closest('.feed_box').find('.a_detail').html();
    console.log('hello');
    $('#write_answer').trigger('click');
    editor.html(ans).focus();
    var form = $('.answer_form');
    form.find('input[name=aid]').val(id);
    form.find('.new').addClass('hide');
    form.find('.check_btn').removeClass('hide');
    $this.closest('.feed_box').addClass('hide');
});

$('#write_answer').on('click', function() {
    var mode = $(this).text();
    var form = $('.answer_form');
    if (mode == 'Cancel') {
        form[0].reset();
        $('#editor').html('');
    }
    //form.find('input[name=aid]').val('');
    form.find('.new').removeClass('hide');
    form.find('.check_btn').addClass('hide');
});

var c_i = $('.change_image');
if (c_i.length > 0) {
    change_image();
}

function change_image() {
    var form = $('.change_image');
    var images = form.find('.img_pre').children();
    var img_no = images.length;
    if (img_no > 0) {
        $('.img_pre').removeClass('hide').addClass('show_pre');
        $('.img_pre').attr('data-index', img_no);
        for (i = 1; i <= img_no; i++) {
            var input = '<span title="Add Image" data-toggle="tooltip" data-placement="left" class="btn btn-default btn-file glyphicon glyphicon-camera input-group-addon seamless_r img_pre_in"><input id="id_image_' + i + '" type="file" name="image' + i + '"></span>';
            $('.img_pre_in').last().after(input);
            $('#id_image_' + i).change(send_img);
            img_index[i - 1] = 1;
        }
        form.find('.fake_btn').attr('data-btn', ('#id_image_' + img_no));
    }
    console.log($('.img_pre').data('index'));
}


/*$('.feed_box_body').each(function() {
    var fig_w = (100 / ($(this).find('figure').length)) - 1;
    $(this).find('figure').css({
        'width': fig_w + '%'
    });
});
*/
$('.change_image').on('click', '.img_pre .close', function() {
    var pid = $(this).data('id');
    if (pid) {
        var pre = $(this).closest('.img_pre');
        var url = pre.data('url');
        var id = $(this).closest('form').find('input[name=id]').val();
        console.log('hello', pid);
        $.ajax({
            url: url,
            type: 'GET',
            data: {
                qid: id,
                pid: pid
            },
            success: function(response) {
                console.log('image removeed');
            },
            error: function(xhr, errmsg, err) {
                console.log(errmsg, err);
            }
        });
    }
});


$('#almost_write_answer').mouseenter(function(){
    if (win_width > 768 ){
        $('#top_login').addClass('open');
    }
    else{
        $('#top_nav_toggle').click();
        $('#top_login a').addClass('open');
    }
});


// this activates the tooltips
$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();
  autosize($('textarea'));
});

$('.body').on('click', '.call_car', function(){
    console.log('image bada ho ja')
    var $this = $(this);
    var $feed = $this.closest('.feed_box_body');
    var title = $feed.find('.summary_title').text();
    var src = $this.attr('src');
    $('#figure_modal .modal-title').text(title);
    $('#figure_modal .modal-body img').attr('src',src);
    $('#figure_modal').on('shown.bs.modal', function(){
        var h_head = $(this).find('.modal-header').outerHeight(true);
        var h_foot = $(this).find('.modal-footer').outerHeight(true);
        console.log(win_height, h_head, h_foot)
        $(this).find('.modal-body').css('height',(win_height-h_head-h_foot));
    });
});


if($('#set_workplace').length){
    console.log('b');
    $('#set_workplace').find('input[name=workplace]').change(function(){
        var $this = this;
        console.log('a',$this.find('button[type=submit]').attr('disabled'))
        $this.find('button[type=submit]').attr('disabled','false');
    });
}

    
function ajax_form($this){
    var $papa = $this.closest('.ajax_papa');
    var $form = $this;
    console.log($form.serialize());
    console.log('a form is being submitted ajaxly');
    $.ajax({
        url: $form.attr('action'),
        type: $form.attr('method'),
        data: $form.serialize(),

        success: function(response) {
            $form.find('.form-control').val('');
            if (response.fields) {
                for (i = 0; i < response.fields.length; i++) {
                    $papa.find('.' + response.fields[i]).text(response.data[response.fields[i]]);
                }
            }
            if (response.inputs) {
                for (i = 0; i < response.inputs.length; i++) {
                    $papa.find('#' + response.inputs[i]).val(response.value[response.inputs[i]]);
                    var cl = $papa.find('#' + response.inputs[i]).attr('class');
                    if (cl.indexOf('d_input') >= 0) {
                        $papa.find('#' + response.inputs[i]).before('<div class="alert"><a class="close">&times;</a><strong>' + response.value[response.inputs[i]] + '</strong></div>').addClass('hide').next().val(response.value[response.inputs[i]]);

                    }
                }
            }
            if (response.elements) {
                if (response.prepend) {
                    for (i = 0; i < response.elements.length; i++) {
                        $papa.find('.' + response.elements[i]).prepend(response.html[response.elements[i]]);
                    }
                } else {
                    for (i = 0; i < response.elements.length; i++) {
                        $papa.find('.' + response.elements[i]).html(response.html[response.elements[i]]);
                    }
                }
            }
        },

        error: function(xhr, errmsg, err) {
            $this.next().next().find(".d_list").html("<li><a class='tag_multiple'>Sorry, unable to fetch results. Try later.</a></li>");
            console.log(errmsg, err);
        }
    });
}

$(document).ready(function(){
    $('.ajax_load').each(function(index, el) {
        var $this = $(this);
        var url = $(this).data('url');
        $.ajax({
            url: url,
            type: 'GET',

            success: function(response) {
                $this.html(response);
                console.log('home_right load hua');
                lazyImages();
            },

            error: function(xhr, errmsg, err) {
                $this.html("<p class='text-center'>Yoo..<br>Content lost its way ... :/</p>");
                console.log(errmsg, err, url);
            }
        });
    });
});

$('.ajax_andar').on('click', '.show_edit', function(){
    var $form = $(this).parent().find('.d_edit');
    $form.removeClass('hide');
    $(this).addClass('hide');
    $(this).parent().find('.done_edit').removeClass('hide');
    $(this).closest('.info_field').find('.info_field_value').addClass('hide');
});

$('.ajax_andar').on('click', '.done_edit', function(){
    var $form = $(this).parent().find('.d_edit');
    ajax_form($form);
    $form.addClass('hide');
    $(this).addClass('hide');
    $(this).parent().find('.show_edit').removeClass('hide');
    $(this).closest('.info_field').find('.info_field_value').removeClass('hide');
});

$(function () {
  function check_messages() {
    $.ajax({
      url: '/messages/check/',
      cache: false,
      success: function (data) {
        $("#unread-count").text(data);
      },
      complete: function () {
        window.setTimeout(check_messages, 180000);
      }
    });
  };
  check_messages();
});

$(function () {
  $("#send").submit(function () {
    $.ajax({
      url: '/messages/send/',
      data: $("#send").serialize(),
      cache: false,
      type: 'post',
      success: function (data) {
        $(".send-message").before(data);
        $("input[name='message']").val('');
        $("input[name='message']").focus();
      }
    });
    return false;
  });
});

$(function () {
  var substringMatcher = function(strs) {
    return function findMatches(q, cb) {
      var matches, substringRegex;
      matches = [];
      substrRegex = new RegExp(q, 'i');
      $.each(strs, function(i, str) {
        if (substrRegex.test(str)) {
          matches.push({ value: str });
        }
      });
      cb(matches);
    };
  };

  $.ajax({
    url: '/messages/users/',
    cache: false,
    success: function (data) {
      /*$('#to').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
      },
      {
        name: 'data',
        displayKey: 'value',
        source: substringMatcher(data)
      });*/
    }
  });
});

$('body').on('click', '.ajax_a', function(event){
    event.preventDefault();
    //window.history.pushState({ id: 35 }, 'ajax kaam', '/op/ol');
    var target = $(this).data('place');
    var url = $(this).attr('href');
    console.log(target);
    $(target).find('.loading').removeClass('hide');
    $.ajax({
        url: url,
        success: function (response) {
            console.log(response);
            $(target).find('.content').html(response);
            $(target).find('.loading').addClass('hide');
            lazyImages();
        },
        error: function(xhr, errmsg, err) {
            console.log(errmsg, err);
            $(target).find('.loading').addClass('hide');
        }
    });
});

$('.nav_flex').on('click', 'li', function(){
    $(this).addClass('active');
    $(this).siblings('li').removeClass('active');
})

$('.select_dropdown').on('click', '.dropdown-menu a', function(){
    console.log($(this).text());
    $(this).addClass('current');
    $(this).closest('.dropdown-menu').find('.current').removeClass('current');
    var what = $(this).find('.value').text();
    var what_fa = $(this).find('i').attr('class');
    var sd = $('.select_dropdown .dropdown-toggle');
    sd.find('.value').text(what);
    sd.find('i').attr('class', what_fa);
    sd.closest('form').find('.d_input').attr('placeholder','Search '+ what + ' ...');
    sd.closest('form').find('.what').val(what.toLowerCase());
    var s_url = '/search/'+what.toLowerCase();
    /*sd.closest('form').attr('action',s_url);*/
});

$('#top_search').on('focus', '.d_input', function(){
    type = $('#top_search').find('.what').val().toLowerCase();
    $(this).closest('.d_search').find('.d_type').val(type);
    /*$(this).closest('form').tooltip('hide');*/
});

/*$('#top_search').on('keydown', '.d_input', function(){
    $(this).closest('form').tooltip('hide');
});*/

$(function(){
    var what = $('#search_typ').find('.dropdown-toggle .value').text().toLowerCase();
    $('#search_typ .dropdown-menu').find('li').each(function(){
        var typ = $(this).find('.value').text().toLowerCase();
        if (typ == what) {
            console.log('matched')
            var what_i = $(this).find('i').attr('class');
            $('#search_typ').find('.dropdown-toggle i').attr('class', what_i);
        }
    });
});


$('#search_toggle').on('click', function(){
    $(this).hide();
    if($('#pre_nav .orelogs').outerWidth(true)){
        $('#top_search').animate({'left':'0%','min-width':'250px'}).css({'overflow':'visible'});
        $('#pre_nav .orelogs').animate({'width':0});
    }
})

/*$('#top_search').on('show.bs.dropdown', '.dropdown', function(){
    $('#top_search .d_menu').css('z-index','1000');
});

$('#top_search').on('hidden.bs.dropdown', '.dropdown', function(){
    $('#top_search .d_menu').css('z-index','auto');
});*/

function lazyImages(){
    $('.lazy_img').each(function(index, el){
        console.log($(this).data('src') + 'loading');
        var $this = $(this);
        var change = true;
        var old_src = $this.attr('src');
        var src = $this.data('src');
        var $farzi = $('.farzi');
        $farzi.append('<img id="lazyimg" src=' + src + ' >');
        var $farzi_now = $farzi.children('#lazyimg');
        $farzi_now.on('load', function() {
            //console.log(index +' loaded ');
            change = true;
            changeSource($this, change, src, $farzi_now);
        });
        if($farzi_now.prop('complete')){
            //console.log(index + 'already loaded');
            change = true;
            changeSource($this, change, src, $farzi_now);
        }
        $farzi_now.on('error', function() {
            //console.log(index +' not loaded');
            change = false;
            changeSource($this, change, src, $farzi_now);
        });
        $farzi_now.attr('id', '');
        $this.removeClass('lazy_img');
    });
}

$(lazyImages);

function changeSource($this, change, src, $farzi_now){
    if (change) {    
        $this.attr('src',src);
    };
    $farzi_now.remove();
}   

$('.body').on('click', '.field_edit', function(){
    var $this = $(this);
    $this.addClass('hide').siblings('.save').removeClass('hide');
    var $info_grp = $this.closest('.info_field_grp');
    $info_grp.find('.info_field_value').addClass('hide');
    $info_grp.find('.info_field_edit').removeClass('hide');
});

$('.body').on('click', '.info_field_grp .save', function(){
    var $this = $(this);
    $this.addClass('hide').siblings('.saving').removeClass('hide');
    var $form = $this.closest('form');
    ajax_form_2($form, changeComplete);
    /*changeComplete($form)*/
    var $info_grp = $this.closest('.info_field_grp');
    $info_grp.find('.info_field_value').removeClass('hide');
    $info_grp.find('.change').addClass('changing');
    $info_grp.find('.info_field_edit').addClass('hide');
});

$('.body').on('change', '.info_field .form-control', function(){
    $(this).closest('.info_field').addClass('change');
    console.log('input value changed');
});



function ajax_form_2($this, callback){
    var $papa = $this.closest('.ajax_papa');
    var $form = $this;
    console.log($form.serialize());
    console.log('a form is being submitted ajaxly');
    $.ajax({
        url: $form.attr('action'),
        type: $form.attr('method'),
        data: $form.serialize(),
        success: function(response) {
            console.log('ajax form submission complete !');
            callback($form, response);
        },
        error: function(xhr, errmsg, err) {
            console.log(errmsg, err);
        }
    });
}

function changeComplete($form, response){
    var $info_grp = $form.closest('.info_field_grp');
    $info_grp.find('.changing').each(function(index, el) {
        $this = $(el);
        var $new_val = $this.find('.new_val');
        if (!$new_val.attr('name')){
            console.log('new_val is not a form element');
            new_val = $this.find('.new_val').html();
        }
        else
            new_val = $this.find('.new_val').val();
        $this.find('.info_field_value').html(new_val);
        console.log('content replaced successfully ',new_val);
    });
    $info_grp.find('.changing').removeClass('changing').removeClass('change').addClass('changed');
    $info_grp.find('.saving').addClass('hide').siblings('.field_edit').removeClass('hide'); 
}

$('body').on('click','.info_field_edit .close', function(){
    console.log('delete this tag')
    deleteWPTag($(this).closest('.tag'));
});

function deleteWPTag($tag){
    var url = '/workplace/delete_tag/';
    var del = $tag.find('.value').text();
    console.log(del, url);
    $.ajax({
        url: url,
        type: "POST",
        data: {
            delete: del
        },
        success: function(response) {
            console.log('deleted tag ',del);
            //$this.tooltip("hide").parent().remove();
        },
        error: function(xhr, errmsg, err) {
            console.log(errmsg, err);
        }
    });
}

$('.enq_btn').on('click',function(){
    $('#enquiry_modal').find('input[name="pid"]').val($(this).closest('.product').find('.id').text());
});

$('body').on('click', '.more', function(){
    var $this = $(this);
    $this.parent().stop().animate({'height':'120px'}, 500, function(){
        $this.parent().addClass('expanded');
        $this.removeClass('more').addClass('less').html('less <span class="fa fa-chevron-up"></span>');
    });
});

$('body').on('click', '.less', function(){
    var $this = $(this);
    $(this).parent().stop().animate({'height':'28px'},500, function(){
        $this.parent().removeClass('expanded');
        $this.removeClass('less').addClass('more').html('more <span class="fa fa-chevron-down"></span>');
    });
});

$('body').on('click', '.next_nav', function(){
    $(this).closest('.tab-content').siblings('.nav-tabs').find('.active').next().find('a').tab('show');
});
/*
$('#add_prod_category').on('click', '.nav li a', function(){
    $(this).tab('show');
});*/

$('#add_prod_category').on('click', '.select_btn', function(){
    var name = $(this).data('name');
    $('#add_prod_category').find('input[name=' + name + ']').val($(this).data('value')).attr('data-text',$(this).text());
    $('#add_prod_category').find('.active_selection').removeClass('active_selection');
    var cat = $(this).data('name');
    if (cat == 'category1') {
        $('#add_prod_category').find('input[name="category2"], input[name="category3"]').val("");
    }
    else if (cat == 'category2') {
        $('#add_prod_category').find('input[name="category3"]').val("");
    }
});

/*$('#add_prod_category').on('click', '.select_btn', function(){
    var cat1 = $('#add_prod_category').find('input[name="category1"]').attr('data-text');
    var cat2 = $('#add_prod_category').find('input[name="category2"]').attr('data-text');
    var cat3 = $('#add_prod_category').find('input[name="category3"]').attr('data-text');
    var cats = [cat1, cat2, cat3];
    var html = '';
    for (var i = 0; i < cats.length; i++) {
        if(cats[i]){
            html = html + '<span class="prod_category">'+cats[i]+'</span>'
        }
    }
    console.log(html)
    $('#add_prod_category').find('.new_val').html(html);
});*/

$('#add_prod_category').on('click', '.no_sub', function(){
    $(this).addClass('active_selection');
    var cat1 = $('#add_prod_category').find('input[name="category1"]').attr('data-text');
    var cat2 = $('#add_prod_category').find('input[name="category2"]').attr('data-text');
    var cat3 = $('#add_prod_category').find('input[name="category3"]').attr('data-text');
    var cats = [cat1, cat2, cat3];
    html = '';
    for (var i = 0; i < cats.length; i++) {
        if(cats[i]){
            if(i){
                html = html + '<span class="fa fa-chevron-right inline_fa"></span>';
            }
            html = html + '<span>' + cats[i] + '</span>';
        }
    }
    $("#selected_category").html(html);
    
});

$('#add_prod_category').on('click', '.new_category_btn', function(){
    var value = $(this).closest('.collapse').find('input').val();
    $(this).addClass('current');
    var $new_cat_form = $('#new_category_form');
    $('#new_category_form').find('input').each(function(){
        $(this).val('');
    });
    if ($(this).data('level') == 2){
        $new_cat_form.find('input[name=new_category_2]').val(value);
        $new_cat_form.find('input[name=new_category_1]').val($('#add_prod_category').find('input[name="category1"]').val());
    }
    else if ($(this).data('level') == 3){
        $new_cat_form.find('input[name=new_category_3]').val(value);
        $new_cat_form.find('input[name=new_category_2]').val($('#add_prod_category').find('input[name="category2"]').val());
        $new_cat_form.find('input[name=new_category_1]').val($('#add_prod_category').find('input[name="category1"]').val());
    }
    ajax_form_2($new_cat_form, newCategory);
});

function newCategory($form, response){
    var level = $('.new_category_btn.current').attr('data-level');
    console.log(response, level);
    if (level == 2){
        $('.new_category_btn.current').closest('ul').prepend('<li><a class="select_btn added_now" data-name="category' + level + '" data-value="' + response.id + '" data-toggle="pill" href="#category_' + response.id + '">' + response.name + '<span class="fa fa-fw fa-chevron-right"></span></a></li>');
        $('.new_category_btn.current').closest('.tab-pane').find('.tab-content').prepend('<div id="category_' + response.id + '" class="tab-pane fade"><ul class="nav nav-pills nav-stacked"><li><a class="no_sub">' + response.name + '<span class="fa fa-fw fa-check"></span></a></li><li><a class="new_category" href="#new_category_' + response.id + '" data-toggle="collapse">Add a new Category<span class="fa fa-fw fa-plus"></span></a></li><div id="new_category_' + response.id + '" class="collapse" style="padding: 10px"><div class="form-group"><input class="form-control" type="text" value="" placeholder="Name of the new category"></div><div class="panel info"><div class="panel-body bg-warning"><span class="fa fa-exclamation-circle"></span> Categories are meant to be generic so that a considerable number of products fall under it. Kindly provide an apt name keeping this in mind and only after none of the pre-existing categories satisfy your needs.</div></div><div class="form-group text-center"><button type="button" class="btn btn-sm new_category_btn" data-level=2>Add</button></div></div>');
        $('.added_now').tab('show').removeClass('added_now');
    }
    else
        $('.new_category_btn.current').closest('ul').prepend('<li><a class="select_btn no_sub" data-name="category' + level + '" data-value="' + response.id + '">' + response.name + '<span class="fa fa-fw fa-check"></span></a></li>');
    $('.new_category_btn.current').closest('ul').find('.new_category').trigger('click');
    $('.new_category_btn.current').removeClass('current');
}

$('.select_btn').on('click', function(){
    var name = $(this).data('name');
    var $input = $(this).closest('form').find('input[name=' + name + ']');
    $input.val($(this).data('value'));
    if($input.attr('type') == 'hidden'){
        $input.trigger('change');
    }
});

$('#add_product_form').on('click', '.ajx_form', function(e){
    e.preventDefault();
    ajx_form_file($(this).closest('form'), prodSuccess, showFailureModal);
});


function ajx_form_file($form, onSuccess, onFailure){
    var formData = new FormData($form[0]);
    console.log($form,formData)
    $.ajax({
        url: $form.attr('action'),
        type: $form.attr('method'),
        data: formData,
        cache: false,
        contentType: false,
        processData: false,

        success: function(response) {
            onSuccess($form, response);
        },

        error: function(xhr, errmsg, err) {
            console.log(errmsg, err);
            onFailure($form);
        }
    });
}

function ajx_form($form, onSuccess, onFailure){
    $.ajax({
        url: $form.attr('action'),
        type: $form.attr('method'),
        data: $form.serialize(),

        success: function(response) {
            onSuccess($form, response);
        },

        error: function(xhr, errmsg, err) {
            console.log(errmsg, err);
            onFailure($form);
        }
    });
}

function prodSuccess($form, response){
    showSuccessModal($form);
    $('#add_product > .container').find('.alert-info').alert("close");
    $('#add_product > .container').prepend(response.alert);
}

function showSuccessModal($form){
    var id = $form.attr('id');
    $("#" + id + "_succModal").modal();
    $form.find('input:visible, textarea').val('');
    $form.find('[type=file]').val('');
    $form.find('.img_preview img').attr('src', '');
}

function showFailureModal($form){
    var id = $form.attr('id');
    $("#" + id + "_errModal").modal();
}

$("#wp_set_form").on('click','button[type=button]', function(){
    $("#wp_set_form").find('.active').removeClass('active');
    $("#wp_set_search").animate({'opacity':'1'}, 1000);
    console.log($("#wp_set_search").offset().top);
    $('html, body').animate({
        scrollTop: ($("#wp_set_search").offset().top - 200)
    }, 1000);
    $("#wp_set_search .d_type").val($(this).val());
    $(this).addClass('active');
    $("#wp_set_search .d_input").focus();
});

$('#feedback').on('click', 'h3', function(){
    if($(this).attr('class').indexOf('active') >= 0){
        $(this).removeClass('active');
        $("#feedback form").animate({opacity: '0'}, 800, function(){
            $("#feedback").animate({width: '175px', height:'40px'}, 500);
        });
    }
    else{
        $(this).addClass('active');
        $("#feedback").animate({width: '250px', height:'165px'}, 800, function(){
            $("#feedback").css({height: 'auto'});
            $("#feedback form").animate({opacity: '1'}, 500);
        });
        console.log('not active');
    }
});

$('#feedback').on('click', '.ajx_form', function(){
    $(this).addClass('active');
    $("#feedback form").animate({opacity: '0'}, 800, function(){
        $("#feedback").animate({width: '175px', height:'40px'}, 500);
    });
    ajx_form($(this).closest('form'), showSuccessModal, showFailureModal);
});

$('.file_in_single').on('change', function(){
    var value = $(this).val();
    var id = $(this).attr('id');
    var file = this.files[0];
    if (value){
        var reader = new FileReader();
        reader.onloadend = function() {
            $('#' + id + '_preview').find('img').attr('src', reader.result);
        };
        reader.readAsDataURL(file);
    }
    else{
        $('#' + id + '_preview').find('img').attr('src', '');
    }
});

$('.d_type_ext').on('change', function(){
    /*console.log('changing type')*/
    $(this).closest('form').find('.d_type').val($(this).val());
});

$('.c1_group_title').on('click', function(){
    $(this).closest('.form-group').find('.current').removeClass('current');
    $(this).addClass('current');
    if ($(this).find('.fa').attr('class').indexOf('down') >= 0){
        $(this).find('.fa').removeClass('fa-chevron-down').addClass('fa-chevron-up');
    }
    else{
        $(this).find('.fa').removeClass('fa-chevron-up').addClass('fa-chevron-down');
    }
});

var $cover_slide = $('#cover_slide');
if($cover_slide){
    SlideInterval = 3000;
    slideTimer = setTimeout(animateSlide, SlideInterval);
}

function animateSlide(){
    var $cover_slide = $('#cover_slide');
    $cover_slide.find('.current').animate({
        'min-height': (win_height - top_nav_width)
    });
}

$("body").on('click', '.active_li a', function(){
    $('.active_li').find('.active').removeClass('active');
    $(this).closest('li').addClass('active');
});

$('body').on('change', '.dashboard .form_instant .d_value', function(){
    ajx_form($(this).closest('form'), tagAdded, showFailureModal);
});

$('body').on('click', '.suggestions .add_now', function(){
    var $form = $($(this).closest('.suggestions').data('form'));
    $form.find('.d_value').val($(this).closest('.tag_suggest_box').find('.value').text());
    ajx_form($form, tagAdded, showFailureModal);
});

function tagAdded($form, response){
    showSuccessModal($form);
    console.log(response.tag);
    var tag_c = parseInt($form.data('targettags'));
    var count_c = parseInt($form.data('targetcount'));
    console.log(tag_c,count_c);
    for (var i = tag_c; i >= 0; i--) {
        $($form.data('target')+"_tags_"+i).append(response.tag);
    }
    for (var i = count_c; i >= 0; i--) {
        count = parseInt($($form.data('target')+"_count_"+i).text()) + 1;
        $($form.data('target')+"_count_"+i).text(count);
    }
}