/*
 * Effects for the cover page of CoreLogs
 *
 * Date: 07-07-2015
 */

/* function to auto adjust top margin for the body */
function body_slide() {
    var top = $('.navbar-fixed-top').outerHeight(true);
    console.log(top);
    $('.body').stop().animate({
        'top': top
    });
}

/* call body_slide when the window loads or resizes */
$(body_slide);
$(window).on('resize', body_slide);


$(document).ready(function() {
    // url for background image location
    var image_url = 'static/css/';
    // add background image 'div's
    $('#cover_back_default').after('<div id="cover_back_lsi" class="cover_back"></div><div id="cover_back_team" class="cover_back"></div><div id="cover_back_sme" class="cover_back"></div>');
    // set background properties
    $('.cover_back').each(function() {
        var id = $(this).attr('id');
        var $this = $(this);
        console.log(id);
        /*$(this).css({
            'background-image': 'url(' + image_url + id + '.jpg)',
            'background-size': 'cover',
            'background-position': 'center center',
            'background-repeat': 'no-repeat'
        });*/
    });

    // set properties of papas

    var cover_body_h = $('#default').outerHeight();


    // function when navigating away from default
    function change_page() {
        var $this = $(this);
        var show = $this.data('show');
        // check if its not already ative
        if (show != showing) {
            if (showing == 'default') {
                alive_awe(show);
            } else if (show == 'default') {
                alive_awe_rev(showing);
            } else
                alive(showing, show);
            showing = show;
        }
        console.log(showing);
        return 0;
    }

    function alive(showing, show) {
        var target = $('#' + show);
        //var dir = target.data('move');
        var last = $('#' + showing);
        last.find('.cover_desc').animate({
            'top': '-100px'
        }, 500, function() {
            last.find('.cover_body').animate({
                'opacity': '0'
            }, 300, 'linear', function() {
                $('#cover_back_' + show).css({
                    'display': 'block',
                    'z-index': '-9'
                });
                $('#cover_back_' + show).animate({
                    'width': '100%',
                    'height': '100%',
                    'top': '0%',
                    'opacity': '1'
                });
                target.css({
                    'display': 'block'
                });
                target.find('.cover_desc').animate({
                    'top': '0px'
                }, 500, function() {});
                target.animate({
                    'height': cover_body_h
                });
                target.find('.cover_body').animate({
                    'opacity': '1'
                });
                last.animate({
                    'height': '0px'
                }, function() {
                    last.css({
                        'display': 'none'
                    });
                });
            });
        });
    }

    function alive_awe(show) {
        var target = $('#' + show);
        //var dir = target.data('move');
        var last = $('#default');
        def_a_arr = ['.cover_desc', '#login h3', '#signup h3'];
        last.find('.cover_desc').animate({
            'top': '-100px'
        }, 500, function() {
            last.find('#login form').animate({
                'opacity': '0'
            }, 200, 'linear');
            last.find('#signup form').animate({
                'opacity': '0'
            }, 200, 'linear', function() {
                last.find('#login h3 span').animate({
                    'opacity': '0'
                }, 300, 'linear');
                last.find('#signup h3 span').animate({
                    'opacity': '0'
                }, 300, 'linear', function() {
                    last.find('#login h3').animate({
                        'right': '1000px'
                    }, 300, 'linear', function() {
                        last.find('#signup h3').animate({
                            'left': '1000px'
                        }, 300, 'linear', function() {
                            /*$('#cover_back_'+show).css({'display':'block','z-index':'-9'});
                            $('#cover_back_'+show).animate({'width':'100%','height':'100%','opacity':'1'});*/
                            target.css({
                                'display': 'block'
                            });
                            target.animate({
                                'height': cover_body_h
                            });
                            last.animate({
                                'height': 0
                            }, function() {
                                last.css({
                                    'display': 'none'
                                });
                                $('#cover_bottom_title').text('Back to base ...').css({
                                    'background-color': '#fff',
                                    'cursor': 'pointer'
                                }).hover(function() {
                                        $(this).css({
                                            'background-color': '#aaa'
                                        });
                                    },
                                    function() {
                                        $(this).css({
                                            'background-color': '#fff'
                                        });
                                    });
                                $('#cover_bottom_title').attr('data-show', 'default');
                                $('#cover_bottom_title').on('click', change_page);
                            });
                        });
                    });
                });
            });
        });
    }

    function alive_awe_rev(showing) {
        var target = $('#default');
        //var dir = target.data('move');
        var last = $('#' + showing);
        last.find('.cover_desc').animate({
            'top': '-100px'
        }, 500, function() {
            last.find('.cover_body').animate({
                'opacity': '0'
            }, 300, 'linear', function() {
                /*$('#cover_back_'+show).css({'display':'block','z-index':'-9'});
                $('#cover_back_'+show).animate({'width':'100%','height':'100%','top':'0%','opacity':'1'});*/
                last.animate({
                    'height': '0px'
                }, function() {
                    last.css({
                        'display': 'none'
                    });
                });
                target.css({
                    'display': 'block'
                });
                target.find('.cover_desc').animate({
                    'top': '0px'
                }, 500, function() {});
                target.animate({
                    'height': cover_body_h
                }, function() {
                    target.find('.cover_body').animate({
                        'opacity': '1'
                    }, function() {
                        target.find('#login h3').animate({
                            'right': '0px'
                        }, 300, 'linear', function() {
                            target.find('#signup h3').animate({
                                'left': '0px'
                            }, 300, 'linear', function() {
                                target.find('#login form').animate({
                                    'opacity': '1'
                                }, 200, 'linear');
                                target.find('#signup form').animate({
                                    'opacity': '1'
                                }, 200, 'linear', function() {
                                    target.find('#login h3 span').animate({
                                        'opacity': '1'
                                    }, 300, 'linear');
                                    target.find('#signup h3 span').animate({
                                        'opacity': '1'
                                    }, 300, 'linear', function() {
                                        $('#cover_bottom_title').text('Curious about whats in there ..?').css({
                                            'background-color': 'transparent',
                                            'cursor': ''
                                        }).off('mouseenter mouseleave');
                                        $('#cover_bottom_title').attr('data-show', '');
                                        $('#cover_bottom_title').off('click');
                                    });
                                });
                            });
                        });
                    });
                });
            });
        });
    }

    var showing = 'default';

    // action on bottom_btn events
    $('.cover_bottom_btn').on('click', change_page);

});
