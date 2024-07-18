<script>
  $(document).ready(function() {
      $('.dropdown-submenu a.dropdown-toggle').on("click", function(e) {
          var $subMenu = $(this).next(".dropdown-menu");
          $subMenu.toggle();
          e.stopPropagation();
          e.preventDefault();
      })
  });
  </script>
  