let slideIndex = 0;
    showSlide(slideIndex);
    
    function prevSlide() {
      showSlide(slideIndex -= 1);
    }
    
    function nextSlide() {
      showSlide(slideIndex += 1);
    }
    
    function showSlide(index) {
      const slides = document.getElementsByClassName("slide");
      if (index >= slides.length) {
        slideIndex = 0;
      }
      if (index < 0) {
        slideIndex = slides.length - 1;
      }
      for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
      }
      slides[slideIndex].style.display = "block";
    }