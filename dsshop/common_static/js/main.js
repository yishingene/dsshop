/* LANGUAGE SELECTION CODE */
        $('a.language_selector').on('click', function(event){
            event.preventDefault();

            var language = $(this).data('language');
            var url = $(this).parent('form').attr('action');
            var next = $('#next_page').val();
            var data = {'language': language, 'next':next};

            $.ajax({
                url: url,
                type: 'POST',
                data : { 'language' : language, 'next': next },
                success: function(data){
                    location.reload(); // Refresh pagina na succesvol POST request (language cookie is nu up to date)
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    alert(thrownError);
                }         
            });
        })
/* HEADER SEARCH INPUT SCRIPT */
        var flatSearch = function () {
            $(document).on('click', function(e) {   
                var clickID = e.target.id;   
                if ( ( clickID != 's' ) ) {
                    $('.top-search').removeClass('show');                
                } 
            });

            $('.search-box').on('click', function(event){
                event.stopPropagation();
            });

            $('.search-form').on('click', function(event){
                event.stopPropagation();
            });        

            $('.search-box').on('click', function () {
                if(!$('.top-search').hasClass( "show" ))
                    $('.top-search').addClass('show');
                else
                    $('.top-search').removeClass('show');
            });
        } 
/* RESPONSIVE MENU FOR SMARTPHONES */

        var responsiveMenu = function() {
            var menuType = 'desktop';

            $(window).on('load resize', function() {
                var currMenuType = 'desktop';
                if ( matchMedia( 'only screen and (max-width: 991px)' ).matches ) {
                    currMenuType = 'mobile';
                }

                if ( currMenuType !== menuType ) {
                    menuType = currMenuType;

                    if ( currMenuType === 'mobile' ) {
                        var $mobileMenu = $('#mainnav').attr('id', 'mainnav-mobi').hide();
                        var hasChildMenu = $('#mainnav-mobi').find('li:has(ul)');

                        $('.mega-menu .mega-menu-sub').hide();
                        $('.has-mega-menu .submenu.mega-menu').hide();

                        $('#header').after($mobileMenu);
                        hasChildMenu.children('ul').hide();
                        hasChildMenu.children('a:not(.has-mega)').after('<span class="btn-submenu"></span>');
                        $('.btn-menu').removeClass('active');
                    } else {
                        var $desktopMenu = $('#mainnav-mobi').attr('id', 'mainnav').removeAttr('style');

                        $desktopMenu.find('.submenu').removeAttr('style');
                        $('#header').find('.nav-wrap').append($desktopMenu);
                        $('.btn-submenu').remove();
                    }
                }
            });

            $('.btn-menu').on('click', function() {         
                $('#mainnav-mobi').slideToggle(300);
                $(this).toggleClass('active');
            });

            // Mega menu click
            if ( matchMedia( 'only screen and (max-width: 991px)' ).matches ) {
                $('.btn-mega').on('click', function() {      
                    $(this).parent('.mega-title').siblings().slideToggle(300);   
                    $(this).toggleClass('active');
                });

                $('.has-mega').on('click', function() {      
                    $(this).siblings().slideToggle(300);  
                    $(this).toggleClass('active');
                });
            }        

            $(document).on('click', '#mainnav-mobi li .btn-submenu', function(e) {
                $(this).toggleClass('active').next('ul').slideToggle(300);
                e.stopImmediatePropagation()
            });

        }
/* HEADER FIXED */
        var headerFixed = function() {    
            if ( $('body').hasClass('header-sticky') ) {
                var hd_height = $('#header').height();           
                $(window).on('load scroll', function(){                
                    if ( $(window).scrollTop() >  37 ) {
                        $('#header').addClass('downscrolled');                      
                    } else {                    
                        $('#header').removeClass('downscrolled');                   
                    }
                    if( $(window).scrollTop() > 37 ) {
                        $('#header').addClass('upscrolled');                    
                    } else {
                        $('#header').removeClass('upscrolled');                    
                    }
                })            
            }   
        }
        $(function() { 
            if ( matchMedia( 'only screen and (min-width: 991px)' ).matches ) {
                headerFixed();
            }
            responsiveMenu();
            flatSearch(); 
        });
/* FLAT TABS */
        var flatTabs = function () {
            $('.flat-tabs').each(function() {

                $(this).children('.content-tab').children().hide();
                $(this).children('.content-tab').children().first().show();

                $(this).find('.menu-tabs').children('li').on('click', function(e) {
                    var liActive = $(this).index(),
                        contentActive = $(this).siblings().removeClass('active').parents('.flat-tabs').children('.content-tab').children().eq(liActive);

                    contentActive.addClass('active').fadeIn('slow');
                    contentActive.siblings().removeClass('active');
                    $(this).addClass('active').parents('.flat-tabs').children('.content-tab').children().eq(liActive).siblings().hide();
                    e.preventDefault();
                });
            });
        };
