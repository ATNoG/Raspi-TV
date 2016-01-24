//
//    Main script of DevOOPS v1.0 Bootstrap Theme
//
//////////////////////////////////////////////////////
//////////////////////////////////////////////////////
//
//      MAIN DOCUMENT READY SCRIPT OF DEVOOPS THEME
//
//      In this script main logic of theme
//
//////////////////////////////////////////////////////
//////////////////////////////////////////////////////
$(document).ready(function () {
    $('body').on('click', '.show-sidebar', function (e) {
        e.preventDefault();
        $('div#main').toggleClass('sidebar-show');
    });
    $('.main-menu li a[href$="#"]').first().addClass('active-parent active');
    $('.dropdown:has(li:has(a.active)) > a').addClass('active-parent active');
    $('.dropdown:has(li:has(a.active)) > ul').css("display", "block");
    $('.main-menu').on('click', 'a', function (e) {
        var parents = $(this).parents('li');
        var li = $(this).closest('li.dropdown');
        var another_items = $('.main-menu li').not(parents);
        another_items.find('a').removeClass('active');
        another_items.find('a').removeClass('active-parent');
        if ($(this).hasClass('dropdown-toggle') || $(this).closest('li').find('ul').length == 0) {
            $(this).addClass('active-parent');
            var current = $(this).next();
            if (current.is(':visible')) {
                li.find("ul.dropdown-menu").slideUp('fast');
                li.find("ul.dropdown-menu a").removeClass('active')
            }
            else {
                another_items.find("ul.dropdown-menu").slideUp('fast');
                current.slideDown('fast');
            }
        }
        else {
            if (li.find('a.dropdown-toggle').hasClass('active-parent')) {
                var pre = $(this).closest('ul.dropdown-menu');
                pre.find("li.dropdown").not($(this).closest('li')).find('ul.dropdown-menu').slideUp('fast');
            }
        }
        if ($(this).hasClass('active') == false) {
            $(this).parents("ul.dropdown-menu").find('a').removeClass('active');
            $(this).addClass('active')
        }
        if ($(this).hasClass('ajax-link')) {
            e.preventDefault();
            if ($(this).hasClass('add-full')) {
                $('#content').addClass('full-content');
            }
            else {
                $('#content').removeClass('full-content');
            }
            var url = $(this).attr('href');
            window.location.hash = url;
            LoadAjaxContent(url);
        }
        if ($(this).attr('href') == '#') {
            e.preventDefault();
        }
    });
    var height = window.innerHeight - 50;
    $('#main').css('min-height', height)
        .on('click', '.expand-link', function (e) {
            var body = $('body');
            e.preventDefault();
            var box = $(this).closest('div.box');
            var button = $(this).find('i');
            button.toggleClass('fa-expand').toggleClass('fa-compress');
            box.toggleClass('expanded');
            body.toggleClass('body-expanded');
            var timeout = 0;
            if (body.hasClass('body-expanded')) {
                timeout = 100;
            }
            setTimeout(function () {
                box.toggleClass('expanded-padding');
            }, timeout);
            setTimeout(function () {
                box.resize();
                box.find('[id^=map-]').resize();
            }, timeout + 50);
        })
        .on('click', '.collapse-link', function (e) {
            e.preventDefault();
            var box = $(this).closest('div.box');
            var button = $(this).find('i');
            var content = box.find('div.box-content');
            content.slideToggle('fast');
            button.toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
            setTimeout(function () {
                box.resize();
                box.find('[id^=map-]').resize();
            }, 50);
        })
        .on('click', '.close-link', function (e) {
            e.preventDefault();
            var content = $(this).closest('div.box');
            content.remove();
        });
});


