(function ($) {
  $(function () {

    $('.sidenav').sidenav();
    $('.dropdown-trigger').dropdown();
    $('.tabs').tabs();
    $('.materialboxed').materialbox();
    $('select').formSelect();
    $('.slider').slider();
    $('.tooltipped').tooltip();
    $('.modal').modal();
    $('.collapsible').collapsible();
    $('datepicker').datepicker({ format: 'yyyy-mm-dd' });
    $('.carousel.carousel-slider').carousel({ fullWidth: true, indicators: true });
    $('.carousel.carousel-slider').carousel({ fullWidth: true });
    $('.tabs').tabs();
    $('.tooltipped').tooltip();
  }); // end of document ready
})(jQuery); // end of jQuery name space
